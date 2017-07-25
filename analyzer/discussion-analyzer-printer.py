import arrow
import os
import shutil

from dbas.database import DBDiscussionSession as session, get_dbas_db_configuration
from dbas.database.discussion_model import Issue, User, Statement, Argument, ClickedStatement, History, TextVersion, \
    ReviewEdit, ReviewOptimization, ReviewDelete, ReviewDuplicate, LastReviewerDelete, LastReviewerDuplicate, \
    LastReviewerEdit, LastReviewerOptimization, Premise
from dbas.helper.tests import add_settings_to_appconfig
from dbas.lib import get_text_for_statement_uid, get_text_for_premisesgroup_uid
from sqlalchemy import and_
from dbas.handler.opinion import get_user_with_same_opinion_for_statements
from graph.partial_graph import get_partial_graph_for_statement
from dbas.lib import get_all_arguments_by_statement

settings = add_settings_to_appconfig()
session.configure(bind=get_dbas_db_configuration('discussion', settings))

top_count = 5
flop_count = 5
start = arrow.get('2017-05-09T05:35:00.000000+00:00')
end = arrow.get('2017-05-28T23:59:00.000000+00:00')
path = './analyzer/evaluation'

user_admin = ['anonymous', 'Tobias', 'Christian', ]
user_colleagues = ['ansel101', 'mamau002', 'chmet101', 'jurom100', 'tokra100',
                   'luhim001', 'toamf100', 'daneu102', 'hisch100', 'rabio100', 'alsch132']

db_colleagues = session.query(User).filter(User.nickname.in_(user_colleagues + user_admin))


def get_weekday(arrow_time):
    return {
        0: 'Mo', 1: 'Tu', 2: 'We', 3: 'Th', 4: 'Fr', 5: 'Sa', 6: 'Su',
    }[arrow_time.weekday()]


db_issue = session.query(Issue).filter_by(slug='verbesserung-des-informatik-studiengangs').first()
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
    target = open(path + '/analyze_positions_opionions.csv', 'w')
    target.write('#uid,usercount,seen_by\n')
    for opinion in user_with_same_opinion['opinions']:
        target.write('{},{},{}\n'.format(opinion['uid'], len(opinion['users']), opinion['seen_by']))
    target.close()


def print_summary():
    # schriftliche zusammenfassung
    target = open(path + '/analyze_positions_summary.txt', 'w')
    for el in reversed(sorted_positions):
        key = el[0]
        author = session.query(User).get(session.query(TextVersion).filter_by(statement_uid=key).order_by(TextVersion.uid.desc()).first().author_uid).nickname
        target.write('{} möchte darüber reden, dass {}.\n'.format(author, get_text_for_statement_uid(key)))

        db_pro = session.query(Argument).filter(Argument.conclusion_uid == key, Argument.is_supportive == True).all()
        db_con = session.query(Argument).filter(Argument.conclusion_uid == key, Argument.is_supportive == False).all()

        __print_pros(target, db_pro, '\t')
        __print_cons(target, db_con, '\t')

        target.write('\n')
    target.close()


def __print_pros(target, db_pro, t):
    for pro in db_pro:
        author = session.query(User).get(pro.author_uid).nickname
        text, tmp = get_text_for_premisesgroup_uid(pro.premisesgroup_uid)
        target.write('\t+ {} meint, dass es ist richtig, weil {}\n'.format(author, text))
        __print_more_for(target, pro, t + '\t')
    # if len(db_pro) == 0:
    #    target.write(t + '+ Niemand hat eine Unterstützung eingeben.\n')


def __print_cons(target, db_con, t, is_undercut=False):
    for con in db_con:
        author = session.query(User).get(con.author_uid).nickname
        text, tmp = get_text_for_premisesgroup_uid(con.premisesgroup_uid)
        if is_undercut:
            target.write(t + '- {} meint, dass die Begründung von gerade nicht zur Behauptung passt, weil {}\n'.format(author, text))
        else:
            target.write(t + '- {} meint, dass es ist falsch,  weil {}\n'.format(author, text))
        __print_more_for(target, con, t + '\t')
    # if len(db_con) == 0:
    #    target.write('\t- Niemand hat einen Angriff eingeben.\n')


def __print_more_for(target, arg, t):
    db_premises = session.query(Premise).filter_by(premisesgroup_uid=arg.premisesgroup_uid).all()
    ids = [p.statement_uid for p in db_premises]
    db_args1 = session.query(Argument).filter(Argument.conclusion_uid.in_(ids))
    db_args2 = session.query(Argument).filter_by(argument_uid=arg.uid).all()
    db_pros = db_args1.filter_by(is_supportive=True).all()
    db_cons = db_args1.filter_by(is_supportive=False).all()
    __print_pros(target, db_pros, t)
    __print_cons(target, db_cons, t)
    __print_cons(target, db_args2, t, is_undercut=True)


def print_activity_per_day():
    # action per day
    target = open(path + '/analyze_day_clicks.csv', 'w')
    for day in range(0, (end - start).days + 1):
        clicks = session.query(History).filter(and_(History.timestamp >= start.replace(days=+day),
                                                    History.timestamp < start.replace(days=+day + 1))).all()
        target.write('{},{}\n'.format(day, len(clicks)))
    target.close()


def print_user_activity():
    target = open(path + '/analyze_users_activity.csv', 'w')
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
    target = open(path + '/analyze_textversion_history.csv', 'w')
    db_st = [s.uid for s in session.query(Statement).filter_by(issue_uid=db_issue.uid).all()]
    db_p = [s.uid for s in session.query(Statement).filter(Statement.issue_uid == db_issue.uid, Statement.is_startpoint == True).all()]
    db_h = session.query(History).filter(
        History.timestamp >= start,
        History.timestamp <= end
    ).all()
    his_count = len([h for h in db_h if db_issue.slug in h.path])
    count_tv = 0
    count_h = 0
    count_r = 0
    count_p = 0
    statements = []
    positions = []
    target.write('# day, tv_count, st_count, user_activity, review_count, position\n')
    for day in range(0, (end - start).days + 1):
        textversions = session.query(TextVersion).filter(and_(
            TextVersion.timestamp >= start.replace(days=+day),
            TextVersion.timestamp < start.replace(days=+day + 1)))
        textversions_s = textversions.filter(TextVersion.statement_uid.in_(db_st)).all()
        textversions_p = textversions.filter(TextVersion.statement_uid.in_(db_p)).all()
        print('{} {} {}'.format(len(textversions_p), len([tv.statement_uid for tv in textversions_p]), count_p))
        statements = list(set(statements + list(set([tv.statement_uid for tv in textversions_s]))))
        positions = list(set(positions + list(set([tv.statement_uid for tv in textversions_p]))))

        history = session.query(History).filter(and_(
            History.path.contains(db_issue.slug),
            History.timestamp >= start.replace(days=+day),
            History.timestamp < start.replace(days=+day + 1))).all()
        count_r += len(session.query(ReviewEdit).filter(
            ReviewEdit.timestamp >= start.replace(days=+day),
            ReviewEdit.timestamp < start.replace(days=+day + 1)).all())
        count_r += len(session.query(ReviewDelete).filter(
            ReviewDelete.timestamp >= start.replace(days=+day),
            ReviewDelete.timestamp < start.replace(days=+day + 1)).all())
        count_r += len(session.query(ReviewOptimization).filter(
            ReviewOptimization.timestamp >= start.replace(days=+day),
            ReviewOptimization.timestamp < start.replace(days=+day + 1)).all())
        count_r += len(session.query(ReviewDuplicate).filter(
            ReviewDuplicate.timestamp >= start.replace(days=+day),
            ReviewDuplicate.timestamp < start.replace(days=+day + 1)).all())

        count_tv += len(textversions_s)
        count_st = len(statements)
        count_h += len(history)
        count_p = len(positions)

        target.write('{}, {}, {}, {}, {}, {}\n'.format(day, count_tv, count_st, count_h / his_count, count_r, count_p))

    target.close()


def print_textversion_length():
    target = open(path + '/analyze_textversion_length.csv', 'w')
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
    tvs = session.query(TextVersion).filter(TextVersion.statement_uid.in_([x.uid for x in db_statements])).all()
    l = [len(tv.content) for tv in tvs]
    import numpy as np
    for i in range(0, 101):
        target.write('{},{}\n'.format(i / 100, np.percentile(l, i)))
    target.close()


def print_textversions_audit():
    target = open(path + '/analyze_textversions.csv', 'w')
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid)
    statement_uids = [s.uid for s in db_statements.all()]
    target.write('Kürzel;Audit;ID;Position;Content;Opener;Translation\n')
    for tv in session.query(TextVersion).filter(TextVersion.statement_uid.in_(statement_uids)).order_by(TextVersion.uid.asc()).all():
        is_position = db_statements.filter_by(uid=tv.statement_uid).first().is_startpoint
        mark = '✓' if is_position else '×'
        opener = 'I want to talk about the position that ...' if is_position else '...because...'
        content = tv.content.replace('&quot;', '"').replace('&#x27;', '\'')
        target.write(';;{};{};{};{}\n'.format(tv.uid, mark, content, opener))
    target.close()


def print_argumentation_index():
    target = open(path + '/analyze_argumentation_index.csv', 'w')
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).order_by(Statement.uid.asc())
    db_positions = db_statements.filter_by(is_startpoint=True).all()
    for pos in db_positions:
        graph, error = get_partial_graph_for_statement(pos.uid, db_issue.uid, '')
        statements_uids = [int(node['id'].split('statement_')[1]) for node in graph['nodes'] if 'statement' in node['id']]
        without_self = [uid for uid in statements_uids if session.query(Statement).get(uid).textversions.author_uid != pos.textversions.author_uid]
        # print('{} {}'.format(len(statements_uids), len(without_self)))
        arg_index1 = len(statements_uids) / len(db_statements.all())
        arg_index2 = len(without_self) / len(db_statements.all())
        target.write('{},{},{}\n'.format(pos.uid, arg_index1, arg_index2))
    target.close()


def print_review_summary():
    reviews = [
        session.query(LastReviewerEdit).all(),
        session.query(LastReviewerDelete).all(),
        # session.query(LastReviewerOptimization).all(),
        session.query(LastReviewerDuplicate).all()
    ]
    keys = [
        'LastReviewerEdit',
        'LastReviewerDelete',
        # 'LastReviewerOptimization',
        'LastReviewerDuplicate'
    ]
    summary = {k: {} for k in keys}
    for index, query in enumerate(reviews):
        summary[keys[index]] = {last.review_uid: [0, 0] for last in query}
        for last in query:
            key = str(type(last))[39:-2]
            i = 0 if last.is_okay else 1
            summary[key][last.review_uid][i] += 1

    votes = {
        '00': 0,
        '10': 0,
        '11': 0,
        '20': 0,
        '21': 0,
        '22': 0,
        '30': 0,
        '31': 0,
        '32': 0,
        '33': 0,
        '40': 0,
        '41': 0,
        '52': 0,
        '53': 0,
        '54': 0
    }
    for key in keys:
        target = open(path + '/analyze_reviews_{}.csv'.format(key.lower()), 'w')
        target.write('id, okay, not_okay\n')
        for row in summary[key]:
            target.write('{},{},{}\n'.format(row, summary[key][row][0], summary[key][row][1]))
            vote_key = '{}{}'.format(summary[key][row][0], summary[key][row][1])
            if vote_key not in votes:
                vote_key = vote_key[::-1]
            if vote_key in votes:
                votes[vote_key] += 1
            else:
                print('Error with key {}:{}'.format(summary[key][row][0], summary[key][row][1]))
        target.close()

    # check zero votes

    from collections import OrderedDict
    votes = OrderedDict(sorted(votes.items(), key=lambda t: t[0]))
    target = open(path + '/analyze_reviews_summary.csv', 'w')
    target.write('vote,result\n')
    index = 0
    votes['00'] = 0
    votes['00'] += len([row for row in session.query(ReviewEdit).all() if len(session.query(LastReviewerEdit).filter_by(review_uid=row.uid).all()) == 0])
    votes['00'] += len([row for row in session.query(ReviewDelete).all() if len(session.query(LastReviewerDelete).filter_by(review_uid=row.uid).all()) == 0])
    # votes['00'] += len([row for row in session.query(ReviewOptimization).all() if len(session.query(LastReviewerOptimization).filter_by(review_uid=row.uid).all()) == 0])
    votes['00'] += len([row for row in session.query(ReviewDuplicate).all() if len(session.query(LastReviewerDuplicate).filter_by(review_uid=row.uid).all()) == 0])
    for v in votes:
        if votes[v] > 0:
            target.write('{},{}:{},{}\n'.format(index, v[0], v[1], votes[v]))
            index += 1


def print_graph_data():
    from collections import OrderedDict
    target = open(path + '/graph_data.csv', 'w')
    db_positions = session.query(Statement).filter(Statement.issue_uid == db_issue.uid,
                                                   Statement.is_startpoint == True,
                                                   Statement.is_disabled == False).order_by(Statement.uid.asc()).all()
    max = OrderedDict()
    for pos in db_positions:
        graph, error = get_partial_graph_for_statement(pos.uid, db_issue.uid, '')
        for n in graph['nodes']:
            if len(n['label']) is 0 or len(n['type']) is 0:
                graph['nodes'].remove(n)
        max[pos.uid] = len(graph['nodes']) - 1  # minus issue

    depth = OrderedDict()
    for pos in db_positions:
        d = __get_depth_of_branch(pos.uid) + 1
        depth[pos.uid] = d
    target.write('index,uid,size,depth\n')
    for index, pos in enumerate(db_positions):
        target.write('{},{},{},{}\n'.format(index, pos.uid, max[pos.uid], depth[pos.uid]))
    target.close()


def __get_depth_of_branch(statement_uid, todos=[], dones=[], depth=0):
    arguments = get_all_arguments_by_statement(statement_uid)
    dones = list(set(dones + [statement_uid]))
    if not arguments or len(arguments) == 0:
        return 1

    statements = []
    db_premises = session.query(Premise).filter(Premise.premisesgroup_uid.in_([a.premisesgroup_uid for a in arguments])).all()
    statements += [premise.statement_uid for premise in db_premises]
    statements = list(set([x for x in statements if x not in dones and x not in todos and x != statement_uid]))
    if len(statements) == 0:
        return 1

    todo = statements[0]
    todos = list(set(todos + (statements[1:] if len(statements) > 1 else [])))
    return __get_depth_of_branch(todo, todos, dones, depth) + 1


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
    # print_textversion_history()
    # print_textversion_length()
    # print_textversions_audit()
    # print_argumentation_index()
    # print_review_summary()
    print_graph_data()
