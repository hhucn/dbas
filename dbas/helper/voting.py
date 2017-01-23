"""
Class for handling votes of each user.

Functions for setting votes of users. They set votes by clicking the statements in D-BAS.
We are not deleting opposite votes for detecting opinion changes!

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


import transaction

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, VoteArgument, VoteStatement, User, \
    StatementSeenBy, ArgumentSeenBy
from dbas.logger import logger
from dbas.input_validator import is_integer


def add_vote_for_argument(argument_uid, nickname):
    """
    Increases the votes of a given argument.

    :param argument_uid: id of the argument
    :param nickname: request.authenticated_userid
    :return: increased votes of the argument
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user or not is_integer(argument_uid):
        logger('VotingHelper', 'add_vote_for_argument', 'User or argument does not exists', error=True)
        return False

    logger('VotingHelper', 'add_vote_for_argument', 'increasing argument ' + str(argument_uid) + ' vote')
    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)

    if db_argument.argument_uid is None:
        logger('VotingHelper', 'add_vote_for_argument', 'Undercut depth 0')
        __add_vote_for_argument(db_user, db_argument)

    else:
        db_undercuted_arg_step_1 = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)

        if db_undercuted_arg_step_1.argument_uid is None:
            logger('VotingHelper', 'add_vote_for_argument', 'Undercut depth 1')
            __add_vote_for_undercut_step_1(db_argument, db_undercuted_arg_step_1, db_user)

        else:
            logger('VotingHelper', 'add_vote_for_argument', 'Undercut depth 2')
            __add_vote_for_undercut_step_2(db_argument, db_undercuted_arg_step_1, db_user)

    transaction.commit()

    return True


def __add_vote_for_argument(db_user, db_argument):
    """

    :param db_user:
    :param db_argument:
    :return:
    """
    db_conclusion = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)

    # set vote for the argument (relation), its premisegroup and conclusion
    __vote_argument(db_argument, db_user, True)
    __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)
    __vote_statement(db_conclusion, db_user, db_argument.is_supportive)

    # add seen values
    __argument_seen_by_user(db_user.uid, db_argument.uid)
    # __premisegroup_seen_by_user(db_user.uid, db_argument.premisesgroup_uid)
    # __statement_seen_by_user(db_user.uid, db_argument.conclusion_uid)


def __add_vote_for_undercut_step_1(db_argument, db_undercuted_arg_step_1, db_user):
    """

    :param db_argument:
    :param db_undercuted_arg_step_1:
    :param db_user:
    :return:
    """

    db_undercuted_arg_step_1_concl = DBDiscussionSession.query(Statement).get(db_undercuted_arg_step_1.conclusion_uid)

    # vote for the current argument
    __vote_argument(db_argument, db_user, True)
    __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)

    # vote against the undercutted argument
    __vote_argument(db_undercuted_arg_step_1, db_user, db_argument.is_supportive)
    __vote_premisesgroup(db_undercuted_arg_step_1.premisesgroup_uid, db_user, True)
    # if the conclusion of the undercutted argument was supported, we will attack it and vice versa
    __vote_statement(db_undercuted_arg_step_1_concl, db_user, not db_argument.is_supportive)

    # add seen values
    __argument_seen_by_user(db_user.uid, db_argument.uid)
    __argument_seen_by_user(db_user.uid, db_undercuted_arg_step_1.uid)
    # __premisegroup_seen_by_user(db_user.uid, db_argument.premisesgroup_uid)
    # __premisegroup_seen_by_user(db_user.uid, db_undercuted_arg_step_1.premisesgroup_uid)
    # __statement_seen_by_user(db_user.uid, db_undercuted_arg_step_1.conclusion_uid)


def __add_vote_for_undercut_step_2(db_argument, db_undercuted_arg_step_1, db_user):
    """

    :param db_argument:
    :param db_undercuted_arg_step_1:
    :param db_user:
    :return:
    """

    # we are undercutting an undercut
    db_undercuted_arg_step_2 = DBDiscussionSession.query(Argument).get(db_undercuted_arg_step_1.argument_uid)

    # vote for the current argument
    __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)
    __vote_argument(db_argument, db_user, True)

    # vote against the undercutted argument
    __vote_argument(db_undercuted_arg_step_1, db_user, False)
    __vote_premisesgroup(db_undercuted_arg_step_1.premisesgroup_uid, db_user, False)

    # vote NOT for the undercutted undercut

    # add seen values
    __argument_seen_by_user(db_user.uid, db_argument.uid)
    __argument_seen_by_user(db_user.uid, db_undercuted_arg_step_1.uid)
    __argument_seen_by_user(db_user.uid, db_undercuted_arg_step_2.uid)
    # __premisegroup_seen_by_user(db_user.uid, db_argument.premisesgroup_uid)
    # __premisegroup_seen_by_user(db_user.uid, db_undercuted_arg_step_1.premisesgroup_uid)
    # __premisegroup_seen_by_user(db_user.uid, db_undercuted_arg_step_2.premisesgroup_uid)
    # __statement_seen_by_user(db_user.uid, db_undercuted_arg_step_2.conclusion_uid)


def add_vote_for_statement(statement_uid, nickname, supportive):
    """
    Adds a vote for the given statements

    :param statement_uid: Statement.uid
    :param nickname: User.nickname
    :param supportive: boolean
    :return: Boolean
    """
    logger('VotingHelper', 'add_vote_for_statement', 'increasing statement ' + str(statement_uid) + ' vote')
    if not is_integer(statement_uid):
        return False

    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user or not db_statement:
        return False

    __vote_statement(db_statement, db_user, supportive)
    __statement_seen_by_user(db_user.uid, statement_uid)
    transaction.commit()
    return True


def add_seen_statement(statement_uid, user_uid):
    """
    Adds the uid of the statement into the seen_by list, mapped with the given user uid

    :param user_uid: uid of current user
    :param statement_uid: uid of the statement
    :return: undefined
    """
    logger('VotingHelper', 'add_seen_statement', 'statement ' + str(statement_uid) + ', for user ' + str(user_uid))
    if not is_integer(statement_uid) or not is_integer(user_uid):
        return False

    val = __statement_seen_by_user(user_uid, statement_uid)
    if val:
        transaction.commit()

    return val


def add_seen_argument(argument_uid, user_uid):
    """
    Adds the uid of the argument into the seen_by list as well as all included statements, mapped with the given user uid

    :param user_uid: uid of current user
    :param argument_uid: uid of the argument
    :return: undefined
    """
    logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', for user ' + str(user_uid))
    if not is_integer(argument_uid) or not is_integer(user_uid):
        return False

    db_user = DBDiscussionSession.query(User).get(user_uid)
    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)
    if not db_user or not db_argument:
        return False

    __argument_seen_by_user(user_uid, argument_uid)

    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    if not db_premises:
        return False

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

    return True


def clear_vote_and_seen_values_of_user(nickname):
    """
    Delete all votes and seen values

    :param nickname: User.nickname
    :return: Boolean
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return False

    __clear_seen_by_values_of_user(db_user.uid)
    __clear_votes_of_user(db_user.uid)

    DBDiscussionSession.flush()
    transaction.commit()
    return True


def __clear_votes_of_user(user_uid):
    """
    Deletes all votes of given user

    :param user_uid: User.uid
    :return:
    """
    DBDiscussionSession.query(VoteArgument).filter_by(author_uid=user_uid).delete()
    DBDiscussionSession.query(VoteStatement).filter_by(author_uid=user_uid).delete()


def __clear_seen_by_values_of_user(user_uid):
    """
    Deletes all seen by values of given user

    :param user_uid: User.uid
    :return:
    """
    DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=user_uid).delete()
    DBDiscussionSession.query(ArgumentSeenBy).filter_by(user_uid=user_uid).delete()


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

    db_all_valid_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
                                                                             VoteArgument.author_uid == user.uid,
                                                                             VoteArgument.is_valid == True))
    db_current_vote = db_all_valid_votes.filter_by(is_up_vote=is_up_vote).first()
    db_old_votes = db_all_valid_votes.all()

    # we are not deleting opposite votes for detecting opinion changes!
    if db_current_vote in db_old_votes:
        db_old_votes.remove(db_current_vote)

    for old_vote in db_old_votes:
        logger('VotingHelper', '__vote_argument', 'setting old vote ' + str(old_vote.uid) + ' as invalid')
        old_vote.set_valid(False)
    DBDiscussionSession.flush()

    db_new_vote = None
    if not db_current_vote:
        logger('VotingHelper', '__vote_argument', 'add vote for argument ' + str(argument.uid))
        db_new_vote = VoteArgument(argument_uid=argument.uid, author_uid=user.uid, is_up_vote=is_up_vote, is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()

    # do we have some inconsequences?
    db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=argument.conclusion_uid).all()
    for arg in db_arguments:
        db_votes_for_arg = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == arg.uid,
                                                                               VoteArgument.is_valid == True,
                                                                               VoteArgument.author_uid == user.uid,
                                                                               VoteArgument.is_up_vote == argument.is_supportive)).all()
        if db_new_vote and db_new_vote in db_votes_for_arg:
            db_votes_for_arg.remove(db_new_vote)

        for vote in db_votes_for_arg:
            vote.set_valid(False)
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

    db_all_valid_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
                                                                              VoteStatement.author_uid == user.uid,
                                                                              VoteStatement.is_valid == True))
    db_current_vote = db_all_valid_votes.filter_by(is_up_vote=is_up_vote).first()
    db_old_votes = db_all_valid_votes.all()

    # we are not deleting opposite votes for detecting opinion changes!
    if db_current_vote in db_old_votes:
        db_old_votes.remove(db_current_vote)

    for old_vote in db_old_votes:
        logger('VotingHelper', '__vote_statement', 'setting old vote' + str(old_vote.uid) + 'as invalid')
        old_vote.set_valid(False)
    DBDiscussionSession.flush()

    if not db_current_vote:
        logger('VotingHelper', '__vote_statement', 'add vote for statement ' + str(statement.uid))
        db_new_vote = VoteStatement(statement_uid=statement.uid, author_uid=user.uid, is_up_vote=is_up_vote, is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()


def __vote_premisesgroup(premisesgroup_uid, user, is_up_vote):
    """
    Calls statemens-methods for every premise.

    :param premisesgroup_uid: PremiseGroup.uid
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

    if not DBDiscussionSession.query(User).get(user_uid) or not DBDiscussionSession.query(Argument).get(argument_uid):
        return False
    logger('VotingHelper', '__argument_seen_by_user', 'argument ' + str(argument_uid) + ', for user ' + str(user_uid))
    db_seen_by = DBDiscussionSession.query(ArgumentSeenBy).filter(and_(ArgumentSeenBy.argument_uid == argument_uid,
                                                                       ArgumentSeenBy.user_uid == user_uid)).first()
    if not db_seen_by:
        DBDiscussionSession.add(ArgumentSeenBy(argument_uid=argument_uid, user_uid=user_uid))
        DBDiscussionSession.flush()
        return True

    logger('VotingHelper', '__argument_seen_by_user', 'argument ' + str(argument_uid) + ', for user ' + str(user_uid) + ' was already seen')
    return False


def __statement_seen_by_user(user_uid, statement_uid):
    """
    Adds an reference for an seen statement

    :param user_uid: uid of current user
    :param statement_uid: uid of the statement
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    if not DBDiscussionSession.query(User).get(user_uid) or not DBDiscussionSession.query(Statement).get(statement_uid):
        return False

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
    :param premisesgroup_uid: uid of the premisesgroup
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    if not DBDiscussionSession.query(User).get(user_uid) or not DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisesgroup_uid).all():
        return False
    logger('VotingHelper', '__premisegroup_seen_by_user', 'Check premises of group ' + str(premisesgroup_uid))
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisesgroup_uid).all()
    for premise in db_premises:
        __statement_seen_by_user(user_uid, premise.statement_uid)
