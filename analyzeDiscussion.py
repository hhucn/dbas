import arrow

from dbas.database import DBDiscussionSession as session
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, \
    StatementReferences, StatementSeenBy, ArgumentSeenBy, TextVersion, PremiseGroup, Premise, \
    Argument, History, MarkedArgument, MarkedStatement, Message, ReviewDelete, ReviewEdit, \
    ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, \
    OptimizationReviewLocks, ReviewCanceled, RevokedContent, RevokedContentHistory, \
    RSS, ClickedArgument, ClickedStatement, ReviewDuplicate
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config, and_

settings = add_settings_to_appconfig()
session.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

top_count = 3
flop_count = 5
start = arrow.get('2017-01-26T00:00:00.000000+00:00')
end = arrow.get('2017-02-06T23:59:59.000000+00:00')


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


print('')
print('-' * len('| D-BAS ANALYTICS: {} |'.format(db_issue.title.upper())))
print('| D-BAS ANALYTICS: {} |'.format(db_issue.title.upper()))
print('-' * len('| D-BAS ANALYTICS: {} |'.format(db_issue.title.upper())))
print('')


db_users = [user for user in session.query(User).filter(~User.nickname.in_(['anonymous', 'admin', 'tobias'])).all()]
db_clicked_statements = [vote for vote in session.query(ClickedStatement).all() if session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
clicks = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([click for click in db_clicked_statements if click.author_uid == user.uid]) for user in db_users}
sorted_clicks = sorted(clicks.items(), key=lambda x: x[1])

print('Users:')
print('  - count:    {}'.format(len(db_users)))
print('  - activity: {0:.2f} statement-clicks per user'.format(len(db_clicked_statements) / len(db_users)))
print('  - Flop{}'.format(flop_count))
for t in sorted_clicks[0:flop_count]:
    print('    - {}: {}'.format(t[1], t[0]))
print('  - Top{}'.format(top_count))
for t in sorted_clicks[-top_count:]:
    print('    - {}: {}'.format(t[1], t[0]))
print('')


db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
db_disabled_statements = session.query(Statement).filter(and_(Statement.issue_uid == db_issue.uid, Statement.is_disabled == True)).all()
db_positions = [statement for statement in db_statements if statement.is_startpoint]
print('Statements:')
print('  - count / disabled: {} / {}'.format(len(db_statements), len(db_disabled_statements)))
print('')


print('positions:')
print('  - count: {}'.format(len(db_positions)))
print('  - clicks per day (start {})'.format(start.format('DD-MM')))
pos_clicks = {}
for pos in db_positions:
    pos_row = []
    for day in range(0, (end-start).days+1):
        clicks = session.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == pos.uid, ClickedStatement.timestamp >= start.replace(days=+day), ClickedStatement.timestamp < start.replace(days=+day+1))).all()
        pos_row.append(str(len(clicks)))
    pos_clicks[str(pos.uid)] = pos_row
sorted_pos_clicks = sorted(pos_clicks.items(), key=lambda x: x[0])
days = range(0, (end-start).days+1)
print('      Pos\t{}'.format('\t'.join([get_weekday(start.replace(days=+d)) for d in days])))
for row in sorted_pos_clicks:
    print('    - {} \t{}'.format(row[0], '\t'.join(row[1])))
print('')


db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid)
db_disabled_arguments = db_arguments.filter_by(is_disabled=True).all()
db_pro_arguments = db_arguments.filter_by(is_supportive=True).all()
db_con_arguments = db_arguments.filter_by(is_supportive=False).all()
print('Arguments:')
print('  - count / disabled: {} / {}'.format(len(db_arguments.all()), len(db_disabled_arguments)))
print('  - pro / con:        {} / {}'.format(len(db_pro_arguments), len(db_con_arguments)))
print('')


db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).join(TextVersion, Statement.textversion_uid == TextVersion.uid).all()
db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid).all()
author_list_statement = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([statement for statement in db_statements if statement.textversions.author_uid == user.uid]) for user in db_users}
author_list_argument = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([argument for argument in db_arguments if argument.author_uid == user.uid]) for user in db_users}
sorted_author_list_statement = sorted(author_list_statement.items(), key=lambda x: x[1])
sorted_author_list_argument = sorted(author_list_argument.items(), key=lambda x: x[1])
print('Top Authors:')
print('  - Statement: Flop{}'.format(flop_count))
for t in sorted_author_list_statement[0:flop_count]:
    print('    - {}: {}'.format(t[1], t[0]))
print('  - Statement: Top{}'.format(top_count))
for t in sorted_author_list_statement[-top_count:]:
    print('    - {}: {}'.format(t[1], t[0]))
print('  - Argument: Flop{}'.format(flop_count))
for t in sorted_author_list_argument[0:flop_count]:
    print('    - {}: {}'.format(t[1], t[0]))
print('  - Argument: Top{}'.format(top_count))
for t in sorted_author_list_argument[-top_count:]:
    print('    - {}: {}'.format(t[1], t[0]))
print('')


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
print('')


db_votes_arguments_valid_up = [vote for vote in db_clicked_arguments_valid if vote.is_up_vote]
db_votes_statements_valid_up = [vote for vote in db_clicked_statements_valid if vote.is_up_vote]
db_votes_arguments_valid_down = [vote for vote in db_clicked_arguments_valid if not vote.is_up_vote]
db_votes_statements_valid_down = [vote for vote in db_clicked_statements_valid if not vote.is_up_vote]
print('Most up/down interests (valid):')
print('  - arguments:  {} / {}'.format(len(db_votes_arguments_valid_up), len(db_votes_arguments_valid_down)))
print('  - statements: {} / {}'.format(len(db_votes_statements_valid_up), len(db_votes_statements_valid_down)))
print('')


db_votes_arguments_invalid_up = [vote for vote in db_clicked_arguments_valid if vote.is_up_vote]
db_votes_statements_invalid_up = [vote for vote in db_clicked_statements_valid if vote.is_up_vote]
db_votes_arguments_invalid_down = [vote for vote in db_clicked_arguments_valid if not vote.is_up_vote]
db_votes_statements_invalid_down = [vote for vote in db_clicked_statements_valid if not vote.is_up_vote]
print('Most up/down interests (invalid):')
print('  - arguments:  {} / {}'.format(len(db_votes_arguments_invalid_up), len(db_votes_arguments_invalid_down)))
print('  - statements: {} / {}'.format(len(db_votes_statements_invalid_up), len(db_votes_statements_invalid_down)))
print('')


db_marked_statements = session.query(MarkedStatement).all()
db_marked_arguments = session.query(MarkedArgument).all()
marked_statements_list = {statement.uid: len(session.query(MarkedStatement).filter_by(uid=statement.uid).all()) for statement in db_marked_statements}
marked_arguments_list = {argument.uid: len(session.query(MarkedArgument).filter_by(uid=argument.uid).all()) for argument in db_marked_arguments}
sorted_marked_statements_list = sorted(marked_statements_list.items(), key=lambda x: x[1])
sorted_marked_arguments_list = sorted(marked_arguments_list.items(), key=lambda x: x[1])
print('Most marked elements:')
print('  - arguments / statements in total: {} / {}'.format(len(db_marked_statements), len(db_marked_arguments)))
print('  - Argument Top{}'.format(top_count))
for t in sorted_author_list_argument[-top_count:]:
    print('    - {}: {}'.format(t[1], t[0]))
print('  - Statement Top{}'.format(top_count))
for t in sorted_author_list_argument[-top_count:]:
    print('    - {}: {}'.format(t[1], t[0]))
print('')


db_review_edits = session.query(ReviewEdit).all()
db_review_deletes = session.query(ReviewDelete).all()
db_review_optimizations = session.query(ReviewOptimization).all()
db_review_duplicates = session.query(ReviewDuplicate).all()
db_review_edits = [review for review in db_review_edits if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
db_review_deletes = [review for review in db_review_deletes if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
db_review_optimizations = [review for review in db_review_optimizations if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
db_review_duplicates = [review for review in db_review_duplicates if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
print('Reviews (Queue/executed/revoked):')
print('  - edits:         {} / {} / {}'.format(len(db_review_edits), len([review for review in db_review_edits if review.is_executed]), len([review for review in db_review_edits if review.is_revoked])))
print('  - deletes:       {} / {} / {}'.format(len(db_review_deletes), len([review for review in db_review_deletes if review.is_executed]), len([review for review in db_review_deletes if review.is_revoked])))
print('  - optimizations: {} / {} / {}'.format(len(db_review_optimizations), len([review for review in db_review_optimizations if review.is_executed]), len([review for review in db_review_optimizations if review.is_revoked])))
print('  - duplicates:    {} / {} / {}'.format(len(db_review_duplicates), len([review for review in db_review_duplicates if review.is_executed]), len([review for review in db_review_duplicates if review.is_revoked])))
print('')


db_history = session.query(History).all()
author_history_list = {'{} {} ({})'.format(user.firstname, user.surname, user.nickname): len([history for history in db_history if history.author_uid == user.uid]) for user in db_users}
# sorted_author_history_list = sorted(author_history_list.items(), key=lambda x: x[1])
history_list = {'{}'.format(history.path): len(session.query(History).filter_by(path=history.path).all()) for history in db_history}
sorted_history_list = sorted(history_list.items(), key=lambda x: x[1])
print('History:')
print('  - Steps: {}'.format(len(db_history)))
print('  - Flop{}'.format(10))
for t in sorted_history_list[0:10]:
    print('    - {}: {}'.format(t[1], t[0]))
print('  - Top{}'.format(10))
for t in sorted_history_list[-10:]:
    print('    - {}: {}'.format(t[1], t[0]))
print('')


print('User Specific History:')
print('')


print('Activity per Day:')
for day in range(0, (end-start).days+1):
    clicks = session.query(History).filter(and_(History.timestamp >= start.replace(days=+day), History.timestamp < start.replace(days=+day+1))).all()
    print('  - {}, {}: Page calls = {}'.format(start.replace(days=+day).format('DD-MM-YYYY'), get_weekday(start.replace(days=+day)), len(clicks)))
print('')


session.query(Issue).all()
session.query(Language).all()
session.query(Group).all()
session.query(User).all()
session.query(Settings).all()
session.query(Statement).all()
session.query(StatementReferences).all()
session.query(StatementSeenBy).all()
session.query(ArgumentSeenBy).all()
session.query(TextVersion).all()
session.query(PremiseGroup).all()
session.query(Premise).all()
session.query(Argument).all()
session.query(History).all()
session.query(ClickedArgument).all()
session.query(ClickedStatement).all()
session.query(MarkedArgument).all()
session.query(MarkedStatement).all()
session.query(Message).all()
session.query(ReviewDelete).all()
session.query(ReviewEdit).all()
session.query(ReviewEditValue).all()
session.query(ReviewOptimization).all()
session.query(ReviewDeleteReason).all()
session.query(LastReviewerDelete).all()
session.query(LastReviewerEdit).all()
session.query(LastReviewerOptimization).all()
session.query(ReputationHistory).all()
session.query(ReputationReason).all()
session.query(OptimizationReviewLocks).all()
session.query(ReviewCanceled).all()
session.query(RevokedContent).all()
session.query(RevokedContentHistory).all()
session.query(RSS).all()
