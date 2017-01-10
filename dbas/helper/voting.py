"""
Class for handling votes of each user.

Functions for setting votes of users. They set votes by clicking the statements in D-BAS.
We are not deleting opposite votes for detecting opinion changes!

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


import transaction

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, VoteArgument, VoteStatement, User, StatementSeenBy, ArgumentSeenBy
from dbas.logger import logger


def add_vote_for_argument(argument_uid, user):
    """
    Increases the votes of a given argument.

    :param argument_uid: id of the argument
    :param user: request.authenticated_userid
    :return: increased votes of the argument
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if not db_user:
        logger('VotingHelper', 'add_vote_for_argument', 'User does not exists', error=True)
        return None

    logger('VotingHelper', 'add_vote_for_argument', 'increasing argument ' + str(argument_uid) + ' vote')
    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)

    # user has seen this argument
    if db_user:
        __argument_seen_by_user(db_user.uid, argument_uid)
        __premisegroup_seen_by_user(db_user.uid, db_argument.premisesgroup_uid)

    if db_argument.argument_uid is None:
        db_conclusion = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)
        # set vote for the argument (relation), its premisegroup and conclusion
        __vote_argument(db_argument, db_user, True)
        __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)
        __vote_statement(db_conclusion, db_user, True)

    else:
        db_conclusion_argument = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)
        db_conclusion_conclusion = DBDiscussionSession.query(Statement).get(db_conclusion_argument.conclusion_uid)

        # vote for conclusions argument based on support property of current argument
        __vote_argument(db_conclusion_argument, db_user, db_argument.is_supportive)
        # vote for conclusions pgroup is always true based on the language of the reaction
        __vote_premisesgroup(db_conclusion_argument.premisesgroup_uid, db_user, True)
        # vote vor conclusions conclusion is always false
        __vote_statement(db_conclusion_conclusion, db_user, False)

    # return count of votes for this argument
    db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == db_argument.uid,
                                                                   VoteArgument.is_valid == True)).all()

    transaction.commit()

    return len(db_votes)


def add_vote_for_statement(statement_uid, user, supportive):
    """
    Adds a vote for the given statements

    :param statement_uid: Statement.uid
    :param user: User.nickname
    :param supportive: boolean
    :return: Boolean
    """
    logger('VotingHelper', 'add_vote_for_statement', 'increasing statement ' + str(statement_uid) + ' vote')

    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if db_user:
        __vote_statement(db_statement, db_user, supportive)
        __statement_seen_by_user(db_user.uid, statement_uid)
        transaction.commit()
        return True

    return False


def add_seen_statement(statement_uid, user_uid):
    """
    Adds the uid of the statement into the seen_by list, mapped with the given user uid

    :param user_uid: uid of current user
    :param statement_uid: uid of the statement
    :return: undefined
    """
    logger('VotingHelper', 'add_seen_statement', 'statement ' + str(statement_uid) + ', for user ' + str(user_uid))
    if __statement_seen_by_user(user_uid, statement_uid):
        transaction.commit()


def add_seen_argument(argument_uid, user_uid):
    """
    Adds the uid of the argument into the seen_by list as well as all included statements, mapped with the given user uid

    :param user_uid: uid of current user
    :param argument_uid: uid of the argument
    :return: undefined
    """
    logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', for user ' + str(user_uid))
    __argument_seen_by_user(user_uid, argument_uid)

    # getting all statements out of the premise
    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', premise count ' + str(len(db_premises)))
    for p in db_premises:
        logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', add premise ' + str(p.statement_uid))
        __statement_seen_by_user(user_uid, p.statement_uid)

    # find the conclusion and mark all arguments on the way
    while db_argument.conclusion_uid is None:
        db_argument = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)
        __argument_seen_by_user(user_uid, argument_uid)
    logger('VotingHelper', 'add_seen_argument', 'conclusion ' + str(db_argument.conclusion_uid))
    __statement_seen_by_user(user_uid, db_argument.conclusion_uid)

    transaction.commit()


def clear_votes_of_user(user):
    """
    Deletes all votes of given user

    :param user: User.nickname
    :return: None
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if not db_user:
        return False

    DBDiscussionSession.query(VoteArgument).filter_by(author_uid=db_user.uid).delete()
    DBDiscussionSession.query(VoteStatement).filter_by(author_uid=db_user.uid).delete()
    DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).delete()
    DBDiscussionSession.query(ArgumentSeenBy).filter_by(user_uid=db_user.uid).delete()
    DBDiscussionSession.flush()
    transaction.commit()
    return True


def __vote_argument(argument, user, is_up_vote):
    """
    Check if there is a vote for the argument. If not, we will create a new one, otherwise the current one will be
    invalid an we will create a new entry.

    :param argument: Argument
    :param user: User
    :param is_up_vote: Boolean
    :return: None
    """
    if argument is None:
        logger('VotingHelper', '__vote_argument', 'argument is None')
        return

    logger('VotingHelper', '__vote_argument', 'argument ' + str(argument.uid) + ', user ' + user.nickname)

    db_vote = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
                                                                  VoteArgument.author_uid == user.uid,
                                                                  VoteArgument.is_up_vote == is_up_vote,
                                                                  VoteArgument.is_valid == True)).first()

    # old one will be invalid
    db_old_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
                                                                       VoteArgument.author_uid == user.uid,
                                                                       VoteArgument.is_valid == True)).all()

    # we are not deleting oppositve votes for detecting opinion changes!

    if db_vote in db_old_votes:
        db_old_votes.remove(db_vote)

    for old_vote in db_old_votes:
        old_vote.set_valid(False)
        old_vote.update_timestamp()
    DBDiscussionSession.flush()

    if not db_vote:
        db_new_vote = VoteArgument(argument_uid=argument.uid, author_uid=user.uid, is_up_vote=is_up_vote, is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()


def __vote_statement(statement, user, is_up_vote):
    """
    Check if there is a vote for the statement. If not, we will create a new one, otherwise the current one will be
    invalid an we will create a new entry.

    :param statement: Statement
    :param user: User
    :param is_up_vote: Boolean
    :return: None
    """
    if statement is None:
        logger('VotingHelper', '__vote_statement', 'statement is None')
        return

    logger('VotingHelper', '__vote_statement', 'statement ' + str(statement.uid) + ', user ' + user.nickname)

    # check for duplicate
    db_vote = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
                                                                   VoteStatement.author_uid == user.uid,
                                                                   VoteStatement.is_up_vote == is_up_vote,
                                                                   VoteStatement.is_valid == True)).first()

    # old one will be invalid
    db_old_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
                                                                        VoteStatement.author_uid == user.uid,
                                                                        VoteStatement.is_valid == True)).all()

    # we are not deleting oppositve votes for detecting opinion changes!

    if db_vote in db_old_votes:
        db_old_votes.remove(db_vote)

    for old_vote in db_old_votes:
        logger('VotingHelper', '__vote_statement', 'setting old votes as invalid')
        old_vote.set_valid(False)
        old_vote.update_timestamp()
    DBDiscussionSession.flush()

    if not db_vote:
        logger('VotingHelper', '__vote_statement', 'add vote for statement ' + str(statement.uid))
        db_new_vote = VoteStatement(statement_uid=statement.uid, author_uid=user.uid, is_up_vote=is_up_vote, is_valid=True)
        DBDiscussionSession.add(db_new_vote)
    else:
        logger('VotingHelper', '__vote_statement', 'update vote for statement ' + str(statement.uid))
        db_vote.update_timestamp()
    DBDiscussionSession.flush()


def __vote_premisesgroup(premisesgroup_uid, user, is_up_vote):
    """
    Calls statemens-methods for every premise.

    :param premisegroup_uid: PremiseGroup.uid
    :param user: User
    :param is_up_vote: Boolean
    :return:
    """
    if premisesgroup_uid is None or premisesgroup_uid == 0:
        logger('VotingHelper', '__vote_premisesgroup', 'premisegroup_uid is None')
        return

    logger('VotingHelper', '__vote_premisesgroup', 'premisegroup_uid ' + str(premisesgroup_uid) + ', user ' + user.nickname)

    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisesgroup_uid).all()
    for premise in db_premises:
        db_statement = DBDiscussionSession.query(Statement).get(premise.statement_uid)
        __vote_statement(db_statement, user, is_up_vote)


def __argument_seen_by_user(user_uid, argument_uid):
    """
    Adds an reference for an seen argument

    :param user_uid: uid of current user
    :param argument_uid: uid of the argument
    :return: True if the argument was not seen by the user (until now), false otherwise
    """
    logger('VotingHelper', '__argument_seen_by_user', 'argument ' + str(argument_uid) + ', for user ' + str(user_uid))
    db_seen_by = DBDiscussionSession.query(ArgumentSeenBy).filter(and_(ArgumentSeenBy.argument_uid == argument_uid,
                                                                       ArgumentSeenBy.user_uid == user_uid)).first()
    if not db_seen_by:
        DBDiscussionSession.add(ArgumentSeenBy(argument_uid=argument_uid, user_uid=user_uid))
        DBDiscussionSession.flush()
        return True
    return False


def __statement_seen_by_user(user_uid, statement_uid):
    """
    Adds an reference for an seen statement

    :param user_uid: uid of current user
    :param statement_uid: uid of the statement
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    db_seen_by = DBDiscussionSession.query(StatementSeenBy).filter(and_(StatementSeenBy.statement_uid == statement_uid,
                                                                        StatementSeenBy.user_uid == user_uid)).first()
    if not db_seen_by:
        logger('VotingHelper', '__statement_seen_by_user', 'statement ' + str(statement_uid) + ', for user ' + str(user_uid) + ' is now marked as seen')
        DBDiscussionSession.add(StatementSeenBy(statement_uid=statement_uid, user_uid=user_uid))
        DBDiscussionSession.flush()
        return True

    logger('VotingHelper', '__statement_seen_by_user', 'statement ' + str(statement_uid) + ', for user ' + str(user_uid) + ' was already seen')
    return False


def __premisegroup_seen_by_user(user_uid, premisesgroup_uid):
    """
    Adds an reference for an seen premisesgroup

    :param user_uid: uid of current user
    :param premsiegroup_uid: uid of the premisesgroup
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    logger('VotingHelper', '__premisegroup_seen_by_user', 'Check premises of group ' + str(premisesgroup_uid))
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisesgroup_uid).all()
    for premise in db_premises:
        __statement_seen_by_user(user_uid, premise.statement_uid)
