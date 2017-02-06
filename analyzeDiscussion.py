from dbas.database import DBDiscussionSession as session
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, \
    StatementReferences, StatementSeenBy, ArgumentSeenBy, TextVersion, PremiseGroup, Premise, \
    Argument, History, VoteArgument, VoteStatement, Message, ReviewDelete, ReviewEdit, \
    ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, \
    OptimizationReviewLocks, ReviewCanceled, RevokedContent, RevokedContentHistory, \
    RSS
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config, and_

settings = add_settings_to_appconfig()
session.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

print(' ----------------- ')
print('| D-BAS ANALYTICS |')
print(' ----------------- ')
print('')

db_issue = session.query(Issue).filter_by(title='Verbesserung des Informatik-Studiengangs').first()

db_statements = session.query(Statement).filter_by(issue_uid=db_issue.uid).all()
db_disabled_statements = session.query(Statement).filter(and_(Statement.issue_uid == db_issue.uid,
                                                              Statement.is_disabled == True)).all()
print('Statements:')
print('  - count:    ' + str(len(db_statements)))
print('  - disabled: ' + str(len(db_disabled_statements)))
print('')

db_arguments = session.query(Argument).filter_by(issue_uid=db_issue.uid).all()
db_disabled_arguments = session.query(Argument).filter(and_(Argument.issue_uid == db_issue.uid,
                                                            Argument.is_disabled == True)).all()
db_pro_arguments = session.query(Argument).filter(and_(Argument.issue_uid == db_issue.uid,
                                                       Argument.is_supportive == True)).all()
db_con_arguments = session.query(Argument).filter(and_(Argument.issue_uid == db_issue.uid,
                                                       Argument.is_supportive == False)).all()
print('Arguments:')
print('  - count:    ' + str(len(db_arguments)))
print('  - pro:      ' + str(len(db_pro_arguments)))
print('  - con:      ' + str(len(db_con_arguments)))
print('  - disabled: ' + str(len(db_disabled_arguments)))
print('')


db_votes_arguments = session.query(VoteArgument).all()
db_votes_statements = session.query(VoteStatement).all()
db_votes_arguments = [vote for vote in db_votes_arguments if session.query(Argument).get(vote.argument_uid).issue_uid == db_issue.uid]
db_votes_statements = [vote for vote in db_votes_statements if session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
db_votes_arguments_valid = [vote for vote in db_votes_arguments if vote.is_valid and session.query(Argument).get(vote.argument_uid).issue_uid == db_issue.uid]
db_votes_statements_valid = [vote for vote in db_votes_statements if vote.is_valid and session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
print('Votes:')
print('  - arguments:  ' + str(len(db_votes_arguments)) + ', valid: ' + str(len(db_votes_arguments_valid)))
print('  - statements: ' + str(len(db_votes_statements)) + ', valid: ' + str(len(db_votes_statements_valid)))
print('')

db_votes_arguments_up = [vote for vote in db_votes_arguments if vote.is_valid and session.query(Argument).get(vote.argument_uid).issue_uid == db_issue.uid]
db_votes_statements_up = [vote for vote in db_votes_statements if vote.is_valid and session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
db_votes_arguments_down = [vote for vote in db_votes_arguments if not vote.is_up_vote and vote.is_valid and session.query(Argument).get(vote.argument_uid).issue_uid == db_issue.uid]
db_votes_statements_down = [vote for vote in db_votes_statements if not vote.is_up_vote and vote.is_valid and session.query(Statement).get(vote.statement_uid).issue_uid == db_issue.uid]
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

