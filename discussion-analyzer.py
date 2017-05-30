import arrow
import os
import shutil

from dbas.database import DBDiscussionSession as session
from dbas.database.discussion_model import Issue,  User, Statement, TextVersion, Premise, Argument, History, \
    MarkedArgument, MarkedStatement, ReviewDelete, ReviewEdit, ReviewOptimization, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, ClickedArgument, \
    ClickedStatement, ReviewDuplicate, LastReviewerDuplicate
from dbas.helper.tests import add_settings_to_appconfig
from dbas.helper.database import dbas_db_configuration
from dbas.lib import get_all_arguments_by_statement
from graph.partial_graph import get_partial_graph_for_statement
from sqlalchemy import and_

settings = add_settings_to_appconfig()
session.configure(bind=dbas_db_configuration('discussion', settings))

top_count = 5
flop_count = 5
start = arrow.get('2017-05-09T05:35:00.000000+00:00')
end = arrow.get('2017-05-28T23:59:00.000000+00:00')
path = './evaluation'

user_admin = ['anonymous', 'Tobias', 'Christian', ]
user_colleagues = ['ansel101', 'mamau002', 'chmet101', 'jurom100', 'tokra100', 'luhim001', 'toamf100',
                   'daneu102', 'hisch100', 'rabio100', 'alsch132']

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


def evaluate_users():
    db_users = [user for user in session.query(User).filter(~User.nickname.in_(user_admin)).all()]
    db_clicked_statements = [v for v in session.query(ClickedStatement).all() if session.query(Statement).get(v.statement_uid).issue_uid == db_issue.uid]
    clicks = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([click for click in db_clicked_statements if click.author_uid == user.uid]) for user in db_users}
    reputation = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): [r for r in session.query(ReputationHistory).filter_by(reputator_uid=u.uid).join(ReputationReason).all()] for u in db_users}
    for rep in reputation:
        reputation[rep] = sum([r.reputations.points for r in reputation[rep]])
    sorted_clicks = sorted(clicks.items(), key=lambda x: x[1])
    sorted_reputation = sorted(reputation.items(), key=lambda x: x[1])
    colleagues = sum([1 for user in db_users if user.nickname not in user_colleagues + user_admin])
    print('Users:')
    print('  - count:    {}'.format(len(db_users)))
    print('  - activity: {0:.2f} statement-clicks per user'.format(len(db_clicked_statements) / len(db_users)))
    print('  - Flop{} sorted by Clicks'.format(flop_count))
    for t in sorted_clicks[0:flop_count]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Top{} sorted by Clicks'.format(top_count))
    for t in sorted_clicks[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Top{} sorted by Reputation'.format(top_count))
    for t in sorted_reputation[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Students: {}'.format(colleagues))
    print('  - Colleagues: {}'.format(len(user_colleagues) - len(user_admin)))
    print('\n')


def evaluate_statements():
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
    db_disabled_statements = session.query(Statement).filter(and_(Statement.issue_uid == db_issue.uid,
                                                                  Statement.is_disabled == True)).all()
    db_statements_students = [s for s in db_statements if s.is_disabled == False and
                              s.textversions.author_uid not in [u.uid for u in db_colleagues]]
    db_statements_students_disabled = [s for s in db_statements if s.is_disabled == True and
                                       s.textversions.author_uid not in [u.uid for u in db_colleagues]]
    db_statements_colleagues = [s for s in db_statements if s.is_disabled == False and
                                s.textversions.author_uid in [u.uid for u in db_colleagues]]
    db_statements_colleagues_disabled = [s for s in db_statements if s.is_disabled == True and
                                         s.textversions.author_uid in [u.uid for u in db_colleagues]]
    print('Statements:')
    print('  - count / disabled')
    print('  - by all: {} / {}'.format(len(db_statements), len(db_disabled_statements)))
    print('  - by student: {} / {}'.format(len(db_statements_students), len(db_statements_students_disabled)))
    print('  - by colleagues: {} / {}'.format(len(db_statements_colleagues), len(db_statements_colleagues_disabled)))
    print('\n')


def evaluate_positions():
    pos_clicks = {}
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
    db_positions = [statement for statement in db_statements if statement.is_startpoint]
    for pos in db_positions:
        pos_row = []
        for day in range(0, (end - start).days + 1):
            clicks = session.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == pos.uid,
                                                                 ClickedStatement.timestamp >= start.replace(days=+day),
                                                                 ClickedStatement.timestamp < start.replace(days=+day + 1))).all()
            pos_row.append(str(len(clicks)))
        pos_clicks[pos.uid] = pos_row
    sorted_pos_clicks = sorted(pos_clicks.items(), key=lambda x: x[0])
    days = range(0, (end - start).days + 1)
    db_pos_arguments = {pos.uid: get_all_arguments_by_statement(pos.uid) if get_all_arguments_by_statement(pos.uid) else [None] for pos in db_positions}
    sorted_pos_arguments = sorted(db_pos_arguments.items(), key=lambda x: x[0])
    output_list = []
    print('Positions:')
    print('  - Count: {}'.format(len(db_positions)))
    print('  - Clicks per day (start {}):'.format(start.format('DD-MM')))
    print('      Pos\t{}\tTotal'.format('\t'.join([get_weekday(start.replace(days=+d)) for d in days])))
    for row in sorted_pos_clicks:
        print('    - {} \t{}\t{}'.format(row[0], '\t'.join(row[1]), sum([int(x) for x in row[1]])))
        output_list.append([str(row[0])] + [str(x) for x in row[1]])
    print('  - Arguments per Position:')
    for row in sorted_pos_arguments:
        print('    - Pos {}: {}  \tPro {}\tCon {}'.format(row[0], len(row[1]), len([arg for arg in row[1] if arg and arg.is_supportive]), len([arg for arg in row[1] if arg and not arg.is_supportive])))
    print('\n')


def evaluate_arguments():
    db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid)
    db_disabled_arguments = db_arguments.filter_by(is_disabled=True).all()
    db_pro_arguments = db_arguments.filter_by(is_supportive=True).all()
    db_con_arguments = db_arguments.filter_by(is_supportive=False).all()
    print('Arguments:')
    print('  - count / disabled: {} / {}'.format(len(db_arguments.all()), len(db_disabled_arguments)))
    print('  - pro / con:        {} / {}'.format(len(db_pro_arguments), len(db_con_arguments)))
    print('\n')


def evaluate_authors():
    db_users = [user for user in session.query(User).filter(~User.nickname.in_(user_admin)).all()]
    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).join(TextVersion, Statement.textversion_uid == TextVersion.uid).all()
    db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid).all()
    author_list_statement = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): len([statement for statement in db_statements if statement.textversions.author_uid == u.uid]) for u in db_users}
    author_list_argument = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): len([argument for argument in db_arguments if argument.author_uid == u.uid]) for u in db_users}
    sorted_author_list_statement = sorted(author_list_statement.items(), key=lambda x: x[1])
    sorted_author_list_argument = sorted(author_list_argument.items(), key=lambda x: x[1])
    print('Top Authors:')
    print('  - Statement:')
    for t in sorted_author_list_statement:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Argument:')
    for t in sorted_author_list_argument:
        print('    - {}: {}'.format(t[1], t[0]))
    print('\n')


def evaluate_interests():
    db_users = [user for user in session.query(User).filter(~User.nickname.in_(user_admin)).all()]
    db_clicked_arguments = session.query(ClickedArgument).all()
    db_clicked_statements = session.query(ClickedStatement).all()
    db_clicked_arguments = [vote for vote in db_clicked_arguments if session.query(Argument).get(vote.argument_uid).issue_uid == db_issue.uid]
    db_clicked_statements = [vote for vote in db_clicked_statements if session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
    db_clicked_arguments_valid = [vote for vote in db_clicked_arguments if vote.is_valid]
    db_clicked_statements_valid = [vote for vote in db_clicked_statements if vote.is_valid]
    db_clicked_arguments_invalid = [vote for vote in db_clicked_arguments if not vote.is_valid]
    db_clicked_statements_invalid = [vote for vote in db_clicked_statements if not vote.is_valid]
    print('Interests (all/valid/invalid):')
    print('  - arguments:  {} / {} / {}'.format(len(db_clicked_arguments), len(db_clicked_arguments_valid), len(db_clicked_arguments_invalid)))
    print('  - statements: {} / {} / {}'.format(len(db_clicked_statements), len(db_clicked_statements_valid), len(db_clicked_statements_invalid)))
    print('\n')

    db_votes_arguments_valid_up = [vote for vote in db_clicked_arguments_valid if vote.is_up_vote]
    db_votes_statements_valid_up = [vote for vote in db_clicked_statements_valid if vote.is_up_vote]
    db_votes_arguments_valid_down = [vote for vote in db_clicked_arguments_valid if not vote.is_up_vote]
    db_votes_statements_valid_down = [vote for vote in db_clicked_statements_valid if not vote.is_up_vote]
    print('Most up/down interests (valid):')
    print('  - arguments:  {} / {}'.format(len(db_votes_arguments_valid_up), len(db_votes_arguments_valid_down)))
    print('  - statements: {} / {}'.format(len(db_votes_statements_valid_up), len(db_votes_statements_valid_down)))
    print('\n')

    db_votes_arguments_invalid_up = [vote for vote in db_clicked_arguments_valid if vote.is_up_vote]
    db_votes_statements_invalid_up = [vote for vote in db_clicked_statements_valid if vote.is_up_vote]
    db_votes_arguments_invalid_down = [vote for vote in db_clicked_arguments_valid if not vote.is_up_vote]
    db_votes_statements_invalid_down = [vote for vote in db_clicked_statements_valid if not vote.is_up_vote]
    print('Most up/down interests (invalid):')
    print('  - arguments:  {} / {}'.format(len(db_votes_arguments_invalid_up), len(db_votes_arguments_invalid_down)))
    print('  - statements: {} / {}'.format(len(db_votes_statements_invalid_up), len(db_votes_statements_invalid_down)))
    print('\n')

    db_marked_statements = session.query(MarkedStatement).all()
    db_marked_arguments = session.query(MarkedArgument).all()
    # marked_statements_list = {statement.uid: len(session.query(MarkedStatement).filter_by(uid=statement.uid).all()) for statement in db_marked_statements}
    # marked_arguments_list = {argument.uid: len(session.query(MarkedArgument).filter_by(uid=argument.uid).all()) for argument in db_marked_arguments}
    # sorted_marked_statements_list = sorted(marked_statements_list.items(), key=lambda x: x[1])
    # sorted_marked_arguments_list = sorted(marked_arguments_list.items(), key=lambda x: x[1])

    db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).join(TextVersion, Statement.textversion_uid == TextVersion.uid).all()
    db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid).all()
    author_list_statement = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([statement for statement in db_statements if statement.textversions.author_uid == user.uid]) for user in db_users}
    author_list_argument = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([argument for argument in db_arguments if argument.author_uid == user.uid]) for user in db_users}
    sorted_author_list_statement = sorted(author_list_statement.items(), key=lambda x: x[1])
    sorted_author_list_argument = sorted(author_list_argument.items(), key=lambda x: x[1])

    print('Most marked elements:')
    print('  - arguments / statements in total: {} / {}'.format(len(db_marked_statements), len(db_marked_arguments)))
    print('  - Argument Top{}'.format(top_count))
    for t in sorted_author_list_argument[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Statement Top{}'.format(top_count))
    for t in sorted_author_list_statement[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('\n')


def evaluate_reviews():
    db_review_edits = session.query(ReviewEdit).all()
    db_review_deletes = session.query(ReviewDelete).all()
    db_review_optimizations = session.query(ReviewOptimization).all()
    db_review_duplicates = session.query(ReviewDuplicate).all()
    db_review_edits = [r for r in db_review_edits if (session.query(Statement).get(r.statement_uid).issue_uid == db_issue.uid if r.statement_uid is not None else session.query(Argument).get(r.argument_uid).issue_uid == db_issue.uid)]
    db_review_deletes = [r for r in db_review_deletes if (session.query(Statement).get(r.statement_uid).issue_uid == db_issue.uid if r.statement_uid is not None else session.query(Argument).get(r.argument_uid).issue_uid == db_issue.uid)]
    db_review_optimizations = [r for r in db_review_optimizations if (session.query(Statement).get(r.statement_uid).issue_uid == db_issue.uid if r.statement_uid is not None else session.query(Argument).get(r.argument_uid).issue_uid == db_issue.uid)]
    db_review_duplicates = [r for r in db_review_duplicates if (session.query(Statement).get(r.original_statement_uid).issue_uid == db_issue.uid if r.original_statement_uid is not None else session.query(Argument).get(r.argument_uid).issue_uid == db_issue.uid)]
    print('Reviews (Queue/executed/revoked):')
    print('  - edits:         {} / {} / {}'.format(len(db_review_edits), len([r for r in db_review_edits if r.is_executed]), len([r for r in db_review_edits if r.is_revoked])))
    print('  - deletes:       {} / {} / {}'.format(len(db_review_deletes), len([r for r in db_review_deletes if r.is_executed]), len([r for r in db_review_deletes if r.is_revoked])))
    print('  - optimizations: {} / {} / {}'.format(len(db_review_optimizations), len([r for r in db_review_optimizations if r.is_executed]), len([r for r in db_review_optimizations if r.is_revoked])))
    print('  - duplicates:    {} / {} / {}'.format(len(db_review_duplicates), len([r for r in db_review_duplicates if r.is_executed]), len([r for r in db_review_duplicates if r.is_revoked])))
    print('\n')

    db_users = [user for user in session.query(User).filter(~User.nickname.in_(user_admin)).all()]
    db_reviewer_edit = session.query(LastReviewerEdit).all()
    db_reviewer_delete = session.query(LastReviewerDelete).all()
    db_reviewer_optimization = session.query(LastReviewerOptimization).all()
    db_reviewer_duplicate = session.query(LastReviewerDuplicate).all()
    list_reviewer_edit = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): len(session.query(LastReviewerEdit).filter_by(reviewer_uid=u.uid).all()) for u in db_users}
    list_reviewer_delete = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): len(session.query(LastReviewerDelete).filter_by(reviewer_uid=u.uid).all()) for u in db_users}
    list_reviewer_optimization = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): len(session.query(LastReviewerOptimization).filter_by(reviewer_uid=u.uid).all()) for u in db_users}
    list_reviewer_duplicate = {'{} {} ({})'.format(u.firstname, u.surname, u.nickname): len(session.query(LastReviewerDuplicate).filter_by(reviewer_uid=u.uid).all()) for u in db_users}
    sorted_list_reviewer_edit = sorted(list_reviewer_edit.items(), key=lambda x: x[1])
    sorted_list_reviewer_delete = sorted(list_reviewer_delete.items(), key=lambda x: x[1])
    sorted_list_reviewer_optimization = sorted(list_reviewer_optimization.items(), key=lambda x: x[1])
    sorted_list_reviewer_duplicate = sorted(list_reviewer_duplicate.items(), key=lambda x: x[1])
    print('Reviewer:')
    print('  - edits:         {}'.format(len(db_reviewer_edit)))
    print('  - deletes:       {}'.format(len(db_reviewer_delete)))
    print('  - optimizations: {}'.format(len(db_reviewer_optimization)))
    print('  - duplicates:    {}'.format(len(db_reviewer_duplicate)))
    print('  - Edit Top{}'.format(top_count))
    for t in sorted_list_reviewer_edit[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Delete Top{}'.format(top_count))
    for t in sorted_list_reviewer_delete[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Optimization Top{}'.format(top_count))
    for t in sorted_list_reviewer_optimization[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Duplicate Top{}'.format(top_count))
    for t in sorted_list_reviewer_duplicate[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('\n')


def evaluate_history():
    db_users = [user for user in session.query(User).filter(~User.nickname.in_(user_admin)).all()]
    db_history = session.query(History).all()
    # author_history_list = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([history for history in db_history if history.author_uid == user.uid]) for user in db_users}
    # sorted_author_history_list = sorted(author_history_list.items(), key=lambda x: x[1])
    history_list = {'{}'.format(history.path): len(session.query(History).filter_by(path=history.path).all()) for history in db_history}
    history_user_list = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len(session.query(History).filter_by(author_uid=user.uid).all()) for user in db_users}
    sorted_history_list = sorted(history_list.items(), key=lambda x: x[1])
    sorted_history_user_list = sorted(history_user_list.items(), key=lambda x: x[1])
    print('History:')
    print('  - Steps: {}'.format(len(db_history)))
    print('  - Step Flop{}'.format(10))
    for t in sorted_history_list[0:10]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - Step Top{}'.format(10))
    for t in sorted_history_list[-10:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - User Flop{}'.format(flop_count))
    for t in sorted_history_user_list[0:flop_count]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('  - User Top{}'.format(top_count))
    for t in sorted_history_user_list[-top_count:]:
        print('    - {}: {}'.format(t[1], t[0]))
    print('\n')


def evaluate_quits():
    quit_count = 2
    quit_counters = [300, 600, 900]  # 5, 10, 15 Minutes
    db_users = [user for user in session.query(User).filter(~User.nickname.in_(user_admin)).all()]
    for quit_counter in quit_counters:
        print('User Specific History Quits (Quit Count >= {}, Quit Counter = {}s):'.format(quit_count + 1, quit_counter))
        history = {}
        for user in db_users:
            history[user.nickname] = session.query(History).filter_by(author_uid=user.uid).all()
            # print('  - {}: {}'.format(user.nickname, len(history[user.nickname])))
        quit_after = {}
        for user_nickname in history:
            for i in range(0, len(history[user_nickname]) - 1):
                step = history[user_nickname][i].path
                if abs((history[user_nickname][i + 1].timestamp - history[user_nickname][i].timestamp).seconds) > quit_counter \
                        and not any(x in step for x in ['admin', 'rss', 'contact', 'finish', 'settings', 'finish', 'imprint', 'news'])\
                        and len(step) > 2:
                    quit_after[step] = quit_after[step] + 1 if step in quit_after else 1
        sorted_quit_after = sorted(quit_after.items(), key=lambda x: x[1])
        for step in sorted_quit_after:
            if step[1] > quit_count:
                print('  - {} quits after step {}'.format(step[1], step[0]))
        print('\n')


def evaluate_activity():
    print('Activity per Day:')
    for day in range(0, (end - start).days + 1):
        clicks = session.query(History).filter(and_(History.timestamp >= start.replace(days=+day), History.timestamp < start.replace(days=+day + 1))).all()
        print('  - {}, {}: Page clicks = {}'.format(start.replace(days=+day).format('DD-MM-YYYY'), get_weekday(start.replace(days=+day)), len(clicks)))
    print('\n')


def evaluate_graph():
    print('Graph Data:')
    db_positions = session.query(Statement).filter(Statement.issue_uid == db_issue.uid, Statement.is_startpoint == True).all()
    max = {}
    for pos in db_positions:
        graph, error = get_partial_graph_for_statement(pos.uid, db_issue.uid, '')
        max[pos.uid] = len(graph['nodes'])
    sorted_max = sorted(max.items(), key=lambda x: x[1])
    print('  - Biggest Branches')
    for t in sorted_max[-top_count:]:
        print('    - {} nodes for position {}'.format(t[1], t[0]))

    depth = {}
    for pos in db_positions:
        d = __get_depth_of_branch(pos.uid) + 1
        depth[pos.uid] = d
    sorted_depth = sorted(depth.items(), key=lambda x: x[1])
    print('  - Depth of Branches')
    for t in sorted_depth[-top_count:]:
        print('    - Depth of {} for position {}'.format(t[1], t[0]))
    print('\n')


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
    print('-' * len('| D-BAS ANALYTICS: {} |'.format(db_issue.title.upper())))
    print('| D-BAS ANALYTICS: {} |'.format(db_issue.title.upper()))
    print('-' * len('| D-BAS ANALYTICS: {} |'.format(db_issue.title.upper())))
    print('\n')

    evaluate_users()
    # evaluate_statements()
    # evaluate_positions()
    # evaluate_arguments()
    # evaluate_authors()
    # evaluate_interests()
    # evaluate_reviews()
    # evaluate_history()
    # evaluate_quits()
    # evaluate_activity()
    evaluate_graph()
