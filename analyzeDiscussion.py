from dbas.database import DBDiscussionSession as session
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, \
    StatementReferences, StatementSeenBy, ArgumentSeenBy, TextVersion, PremiseGroup, Premise, \
    Argument, History, MarkedArgument, MarkedStatement, Message, ReviewDelete, ReviewEdit, \
    ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, \
    OptimizationReviewLocks, ReviewCanceled, RevokedContent, RevokedContentHistory, \
    RSS, ClickedArgument, ClickedStatement
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config, and_

settings = add_settings_to_appconfig()
session.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

print(' ----------------- ')
print('| D-BAS ANALYTICS |')
print(' ----------------- ')
print('')

db_issue = session.query(Issue).filter_by(title='Verbesserung des Informatik-Studiengangs').first()
if db_issue is None:
    print('WRONG DATABASE')
    exit()
elif db_issue.is_disabled:
    print('ISSUE DISABLED')
    exit()

print(str(db_issue.title))

db_users = session.query(User).all()
db_users = [user for user in db_users if user.nickname != 'anonymous' and user.nickname != 'admin']
db_votes_statements = session.query(VoteStatement).all()
db_votes_statements = [vote for vote in db_votes_statements if session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
l = [len([vote for vote in db_votes_statements if vote.author_uid == u.uid]) for u in db_users]

print('Users:')
print('  - count:    ' + str(len(db_users)))
print('  - activity: ' + str(len(db_votes_statements) / len(db_users)) + ' per user')
print('  - activity: (max): ' + str(max(l)))
print('  - activity: (min): ' + str(min(l)))
print('')


db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
db_disabled_statements = session.query(Statement).filter(and_(Statement.issue_uid == db_issue.uid,
                                                              Statement.is_disabled == True)).all()
print('Statements:')
print('  - count:     ' + str(len(db_statements)))
print('  - disabled:  ' + str(len(db_disabled_statements)))
print('  - positions: ' + str(len([statement for statement in db_statements if statement.is_startpoint])))
print('')

db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid)
db_disabled_arguments = db_arguments.filter_by(is_disabled=True).all()
db_pro_arguments = db_arguments.filter_by(is_supportive=True).all()
db_con_arguments = db_arguments.filter_by(is_supportive=False).all()
print('Arguments:')
print('  - count:    ' + str(len(db_arguments.all())))
print('  - pro:      ' + str(len(db_pro_arguments)))
print('  - con:      ' + str(len(db_con_arguments)))
print('  - disabled: ' + str(len(db_disabled_arguments)))
print('')


db_votes_arguments = session.query(VoteArgument).all()
db_votes_statements = session.query(VoteStatement).all()
db_votes_arguments = [vote for vote in db_votes_arguments if session.query(Argument).get(vote.argument_uid).issue_uid == db_issue.uid]
db_votes_statements = [vote for vote in db_votes_statements if session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
db_votes_arguments_valid = [vote for vote in db_votes_arguments if vote.is_valid]
db_votes_statements_valid = [vote for vote in db_votes_statements if vote.is_valid]
print('Votes:')
print('  - arguments:  ' + str(len(db_votes_arguments)) + ', valid: ' + str(len(db_votes_arguments_valid)))
print('  - statements: ' + str(len(db_votes_statements)) + ', valid: ' + str(len(db_votes_statements_valid)))
print('')

db_votes_arguments_up = [vote for vote in db_votes_arguments_valid if vote.is_up_vote]
db_votes_statements_up = [vote for vote in db_votes_statements_valid if vote.is_up_vote]
db_votes_arguments_down = [vote for vote in db_votes_arguments_valid if not vote.is_up_vote]
db_votes_statements_down = [vote for vote in db_votes_statements_valid if not vote.is_up_vote]
print('Most up/down voted (valid):')
print('  - arguments:  ' + str(len(db_votes_arguments_up)) + ' / ' + str(len(db_votes_arguments_down)))
print('  - statements: ' + str(len(db_votes_statements_up)) + ' / ' + str(len(db_votes_statements_down)))
print('')


db_review_edits = session.query(ReviewEdit).all()
db_review_deletes = session.query(ReviewDelete).all()
db_review_optimizations = session.query(ReviewOptimization).all()
db_review_edits = [review for review in db_review_edits if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
db_review_deletes = [review for review in db_review_deletes if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
db_review_optimizations = [review for review in db_review_optimizations if (session.query(Statement).get(review.statement_uid).issue_uid == db_issue.uid if review.statement_uid is not None else session.query(Argument).get(review.argument_uid).issue_uid == db_issue.uid)]
print('Reviews:')
print('  - edits:         ' + str(len(db_review_edits)))
print('    - executed:    ' + str(len([review for review in db_review_edits if review.is_executed])))
print('    - revoked:     ' + str(len([review for review in db_review_edits if review.is_revoked])))
print('  - deletes:       ' + str(len(db_review_deletes)))
print('    - executed:    ' + str(len([review for review in db_review_deletes if review.is_executed])))
print('    - revoked:     ' + str(len([review for review in db_review_deletes if review.is_revoked])))
print('  - optimizations: ' + str(len(db_review_optimizations)))
print('    - executed:    ' + str(len([review for review in db_review_optimizations if review.is_executed])))
print('    - revoked:     ' + str(len([review for review in db_review_optimizations if review.is_revoked])))
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
session.query(VoteArgument).all()
session.query(VoteStatement).all()
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