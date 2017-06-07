import arrow
import os
import shutil

from dbas.database import DBDiscussionSession as session, get_dbas_db_configuration
from dbas.database.discussion_model import Issue, User, Statement, Argument, ClickedStatement, History, TextVersion, \
    ReviewEdit, ReviewOptimization, ReviewDelete, ReviewDuplicate, LastReviewerDelete, LastReviewerDuplicate, \
    LastReviewerEdit, LastReviewerOptimization
from dbas.helper.tests import add_settings_to_appconfig
from dbas.lib import get_text_for_statement_uid, get_text_for_premisesgroup_uid
from sqlalchemy import and_
from dbas.handler.opinion import get_user_with_same_opinion_for_statements, get_user_with_same_opinion_for_premisegroups

settings = add_settings_to_appconfig()
session.configure(bind=get_dbas_db_configuration('discussion', settings))

top_count = 5
flop_count = 5
start = arrow.get('2017-05-09T05:35:00.000000+00:00')
end = arrow.get('2017-05-28T23:59:00.000000+00:00')
path = './evaluation'

user_admin = ['anonymous', 'Tobias', 'Christian', ]
user_colleagues = ['ansel101', 'mamau002', 'chmet101', 'jurom100', 'tokra100',
                   'luhim001', 'toamf100', 'daneu102', 'hisch100', 'rabio100', 'alsch132']

db_colleagues = session.query(User).filter(User.nickname.in_(user_colleagues + user_admin))


def get_weekday(arrow_time):
    return {
        0: 'Mo', 1: 'Tu', 2: 'We', 3: 'Th', 4: 'Fr', 5: 'Sa', 6: 'Su',
    }[arrow_time.weekday()]


db_issue = session.query(Issue).filter_by(title='Verbesserung des Informatik-Studiengangs').first()
if db_issue is None:
    print('WRONG DATABASE')
    exit()
elif db_issue.is_disabled:
    print('ISSUE DISABLED')
    exit()

db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
db_positions = [statement for statement in db_statements if statement.is_startpoint]
user_with_same_opinion = get_user_with_same_opinion_for_statements([pos.uid for pos in db_positions], True, '', 'de', 'url')
sorted_positions = {}
opinions = {}
for opinion in user_with_same_opinion['opinions']:
    sorted_positions[int(opinion['uid'])] = len(opinion['users'])
    s = (' {}' if opinion['seen_by'] < 10 else '{}').format(opinion['seen_by'])
    u = (' {}' if len(opinion['users']) < 10 else '{}').format(len(opinion['users']))
    opinions[int(opinion['uid'])] = '{} von {}'.format(u, s)
sorted_positions = sorted(sorted_positions.items(), key=lambda x: x[1])


def print_positions_history():
    pos_clicks = {}
    for pos in db_positions:
        pos_row = []
        for day in range(0, (end - start).days + 1):
            clicks = session.query(ClickedStatement).filter(and_(
                ClickedStatement.statement_uid == pos.uid,
                ClickedStatement.timestamp >= start.replace(days=+day),
                ClickedStatement.timestamp < start.replace(days=+day + 1))).all()
            pos_row.append(str(len(clicks)))
        pos_clicks[pos.uid] = pos_row
    sorted_pos_clicks = sorted(pos_clicks.items(), key=lambda x: x[0])
    output_list = []
    for row in sorted_pos_clicks:
        output_list.append([str(row[0])] + [str(x) for x in row[1]])

    # verlauf der positionen
    target = open(path + '/positions.csv', 'w')
    output_list = list(map(list, zip(*output_list)))
    for l in output_list:
        target.write(','.join(l) + '\n')
    target.close()


def print_opitions_for_positions():
    # barometer der positionen
    target = open(path + '/positions_opionions.csv', 'w')
    target.write('#uid,usercount,seen_by\n')
    for opinion in user_with_same_opinion['opinions']:
        target.write('{},{},{}\n'.format(opinion['uid'], len(opinion['users']), opinion['seen_by']))
    target.close()


def print_summary():
    # schriftliche zusammenfassung
    target = open(path + '/positions_summary.txt', 'w')
    for el in reversed(sorted_positions):
        key = el[0]
        uid = ('  {}' if key < 10 else ' {}' if key < 100 else '{}').format(key)
        target.write('{}: {} möchten darüber reden, dass {}.\n'.format(uid, opinions[key],
                                                                       get_text_for_statement_uid(key)))

        db_pro = session.query(Argument).filter(Argument.conclusion_uid == key, Argument.is_supportive == True).all()
        db_con = session.query(Argument).filter(Argument.conclusion_uid == key, Argument.is_supportive == False).all()

        for pro in db_pro:
            users = get_user_with_same_opinion_for_premisegroups([pro.uid], '', 'de', 'url')
            d = users['opinions'][0]
            s = (' {}' if d['seen_by'] < 10 else '{}').format(d['seen_by'])
            u = (' {}' if len(d['users']) < 10 else '{}').format(len(d['users']))
            text, tmp = get_text_for_premisesgroup_uid(pro.premisesgroup_uid)
            target.write('\t+ {} von {} denken, dass es richtig sei, weil {}\n'.format(u, s, text))
        if len(db_pro) == 0:
            target.write('\t+ Niemand hat eine Unterstützung eingeben.\n')

        for con in db_con:
            users = get_user_with_same_opinion_for_premisegroups([con.uid], '', 'de', 'url')
            d = users['opinions'][0]
            s = (' {}' if d['seen_by'] < 10 else '{}').format(d['seen_by'])
            u = (' {}' if len(d['users']) < 10 else '{}').format(len(d['users']))
            text, tmp = get_text_for_premisesgroup_uid(con.premisesgroup_uid)
            target.write('\t- {} von {} denken, dass es falsch sei,  weil {}\n'.format(u, s, text))
        if len(db_con) == 0:
            target.write('\t- Niemand hat einen Angriff eingeben.\n')

        target.write('\n')
    target.close()


def print_activity_per_day():
    # action per day
    target = open(path + '/day_clicks.csv', 'w')
    for day in range(0, (end - start).days + 1):
        clicks = session.query(History).filter(and_(History.timestamp >= start.replace(days=+day),
                                                    History.timestamp < start.replace(days=+day + 1))).all()
        target.write('{},{}\n'.format(day, len(clicks)))
    target.close()


def print_user_activity():
    target = open(path + '/users_activity.csv', 'w')
    db_users = session.query(User).all()
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
    author_dict = {user.uid: len([s for s in db_statements if s.get_first_author() == user.uid]) for user in db_users}

    sorted_author_dict = sorted(author_dict.items(), key=lambda x: x[1])
    target.write('#User, Count\n')
    line1 = ', '.join([str(t[0]) for t in sorted_author_dict])
    line2 = ', '.join([str(t[1] / len(db_statements) * 100) for t in sorted_author_dict])
    target.write('# {}\n{}\n'.format(line1, line2))

    # reviews
    f = []
    e = []
    af = len(session.query(ReviewEdit).all())
    af += len(session.query(ReviewDelete).all())
    af += len(session.query(ReviewOptimization).all())
    af += len(session.query(ReviewDuplicate).all())
    ae = len(session.query(LastReviewerEdit).all())
    ae += len(session.query(LastReviewerDelete).all())
    ae += len(session.query(LastReviewerOptimization).all())
    ae += len(session.query(LastReviewerDuplicate).all())
    for t in sorted_author_dict:
        flags = len(session.query(ReviewEdit).filter_by(detector_uid=t[0]).all())
        flags += len(session.query(ReviewDelete).filter_by(detector_uid=t[0]).all())
        flags += len(session.query(ReviewOptimization).filter_by(detector_uid=t[0]).all())
        flags += len(session.query(ReviewDuplicate).filter_by(detector_uid=t[0]).all())
        executed = len(session.query(LastReviewerEdit).filter_by(reviewer_uid=t[0]).all())
        executed += len(session.query(LastReviewerDelete).filter_by(reviewer_uid=t[0]).all())
        executed += len(session.query(LastReviewerOptimization).filter_by(reviewer_uid=t[0]).all())
        executed += len(session.query(LastReviewerDuplicate).filter_by(reviewer_uid=t[0]).all())
        f.append(str(flags / af * 100))
        e.append(str(executed / ae * 100))

    target.write('{}\n{}\n'.format(', '.join(f), ', '.join(e)))
    target.close()


def print_textversion_history():
    target = open(path + '/textversion_history.csv', 'w')
    db_st = [s.uid for s in session.query(Statement).filter_by(issue_uid=db_issue.uid).all()]
    db_h = session.query(History).filter(
        History.timestamp >= start,
        History.timestamp <= end
    ).all()
    his_count = len([h for h in db_h if db_issue.get_slug() in h.path])
    count_tv = 0
    st = []
    count_h = 0
    target.write('# day, tv_count, st_count, user_activity\n')
    for day in range(0, (end - start).days + 1):
        tvs = session.query(TextVersion).filter(and_(
            TextVersion.statement_uid.in_(db_st),
            TextVersion.timestamp >= start.replace(days=+day),
            TextVersion.timestamp < start.replace(days=+day + 1))).all()
        st = list(set(st + list(set([tv.statement_uid for tv in tvs]))))
        his = session.query(History).filter(and_(
            History.path.contains(db_issue.get_slug()),
            History.timestamp >= start.replace(days=+day),
            History.timestamp < start.replace(days=+day + 1))).all()
        count_tv += len(tvs)
        count_st = len(st)
        count_h += len(his)
        target.write('{}, {}, {}, {}\n'.format(day, count_tv, count_st, count_h / his_count))

    target.close()


if __name__ == '__main__':
    # mk dir
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        print('')
    finally:
        os.mkdir(path)

    print('\n')
    print('-' * len('| D-BAS ANALYTICS PRINTER: {} |'.format(db_issue.title.upper())))
    print('| D-BAS ANALYTICS PRINTER: {} |'.format(db_issue.title.upper()))
    print('-' * len('| D-BAS ANALYTICS PRINTER: {} |'.format(db_issue.title.upper())))
    print('\n')

    # print_positions_history()
    # print_opitions_for_positions()
    # print_summary()
    # print_activity_per_day()
    # print_user_activity()
    print_textversion_history()
