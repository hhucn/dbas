"""
Class for handling votes of each user.

Functions for setting votes of users. They set votes by clicking the statements in D-BAS.
We are not deleting opposite votes for detecting opinion changes!

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, ClickedArgument, ClickedStatement, User, \
    SeenStatement, SeenArgument, MarkedArgument, MarkedStatement
from dbas.input_validator import is_integer
from dbas.logger import logger


def add_click_for_argument(argument_uid, nickname):
    """
    Increases clicks of a given argument.

    :param argument_uid: id of the argument
    :param nickname: request.authenticated_userid
    :return: Boolean
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user or not is_integer(argument_uid):
        logger('VotingHelper', 'add_click_for_argument', 'User or argument does not exists', error=True)
        return False

    logger('VotingHelper', 'add_click_for_argument', 'increasing argument ' + str(argument_uid) + ' vote')
    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)

    if db_argument.argument_uid is None:
        logger('VotingHelper', 'add_click_for_argument', 'Undercut depth 0')
        __add_click_for_argument(db_user, db_argument)

    else:
        db_undercuted_arg_step_1 = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)

        if db_undercuted_arg_step_1.argument_uid is None:
            logger('VotingHelper', 'add_click_for_argument', 'Undercut depth 1')
            __add_click_for_undercut_step_1(db_argument, db_undercuted_arg_step_1, db_user)

        else:
            logger('VotingHelper', 'add_click_for_argument', 'Undercut depth 2')
            __add_click_for_undercut_step_2(db_argument, db_undercuted_arg_step_1, db_user)

    transaction.commit()

    return True


def __add_click_for_argument(db_user, db_argument):
    """
    Add click for a specific argument

    :param db_user: User
    :param db_argument: Argument
    :return: None
    """
    db_conclusion = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)

    # set vote for the argument (relation), its premisegroup and conclusion
    __click_argument(db_argument, db_user, True)
    __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)
    __click_statement(db_conclusion, db_user, db_argument.is_supportive)

    # add seen values
    __argument_seen_by_user(db_user, db_argument.uid)
    # __premisegroup_seen_by_user(db_user, db_argument.premisesgroup_uid)
    # __statement_seen_by_user(db_user, db_argument.conclusion_uid)


def __add_click_for_undercut_step_1(db_argument, db_undercuted_arg_step_1, db_user):
    """
    Add clicks for an first order undercut

    :param db_argument: Argument
    :param db_undercuted_arg_step_1: Argument
    :param db_user: User
    :return: None
    """

    db_undercuted_arg_step_1_concl = DBDiscussionSession.query(Statement).get(db_undercuted_arg_step_1.conclusion_uid)

    # vote for the current argument
    __click_argument(db_argument, db_user, True)
    __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)

    # vote against the undercutted argument
    __click_argument(db_undercuted_arg_step_1, db_user, db_argument.is_supportive)
    __vote_premisesgroup(db_undercuted_arg_step_1.premisesgroup_uid, db_user, True)
    # if the conclusion of the undercutted argument was supported, we will attack it and vice versa
    __click_statement(db_undercuted_arg_step_1_concl, db_user, not db_argument.is_supportive)

    # add seen values
    __argument_seen_by_user(db_user, db_argument.uid)
    __argument_seen_by_user(db_user, db_undercuted_arg_step_1.uid)
    # __premisegroup_seen_by_user(db_user, db_argument.premisesgroup_uid)
    # __premisegroup_seen_by_user(db_user, db_undercuted_arg_step_1.premisesgroup_uid)
    # __statement_seen_by_user(db_user, db_undercuted_arg_step_1.conclusion_uid)


def __add_click_for_undercut_step_2(db_argument, db_undercuted_arg_step_1, db_user):
    """
    Add clicks for an second order undercut

    :param db_argument: Argument
    :param db_undercuted_arg_step_1: Argument
    :param db_user: User
    :return: None
    """

    # we are undercutting an undercut
    db_undercuted_arg_step_2 = DBDiscussionSession.query(Argument).get(db_undercuted_arg_step_1.argument_uid)

    # vote for the current argument
    __vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)
    __click_argument(db_argument, db_user, True)

    # vote against the undercutted argument
    __click_argument(db_undercuted_arg_step_1, db_user, False)
    __vote_premisesgroup(db_undercuted_arg_step_1.premisesgroup_uid, db_user, False)

    # vote NOT for the undercutted undercut

    # add seen values
    __argument_seen_by_user(db_user, db_argument.uid)
    __argument_seen_by_user(db_user, db_undercuted_arg_step_1.uid)
    __argument_seen_by_user(db_user, db_undercuted_arg_step_2.uid)
    # __premisegroup_seen_by_user(db_user, db_argument.premisesgroup_uid)
    # __premisegroup_seen_by_user(db_user, db_undercuted_arg_step_1.premisesgroup_uid)
    # __premisegroup_seen_by_user(db_user, db_undercuted_arg_step_2.premisesgroup_uid)
    # __statement_seen_by_user(db_user, db_undercuted_arg_step_2.conclusion_uid)


def add_click_for_statement(statement_uid, nickname, supportive):
    """
    Adds a clicks for the given statements

    :param statement_uid: Statement.uid
    :param nickname: User.nickname
    :param supportive: boolean
    :return: Boolean
    """

    logger('VotingHelper', 'add_click_for_statement', 'increasing {} vote for statement {}'.format('up' if supportive else 'down', str(statement_uid)))
    if not is_integer(statement_uid):
        return False

    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user or not db_statement:
        return False

    __click_statement(db_statement, db_user, supportive)
    __statement_seen_by_user(db_user, statement_uid)
    transaction.commit()
    return True


def add_seen_statement(statement_uid, db_user):
    """
    Adds the uid of the statement into the seen_by list, mapped with the given user uid

    :param db_user:current user
    :param statement_uid: uid of the statement
    :return: undefined
    """
    if not is_integer(statement_uid) or not isinstance(db_user, User):
        return False
    logger('VotingHelper', 'add_seen_statement', 'statement ' + str(statement_uid) + ', for user ' + str(db_user.uid))

    val = __statement_seen_by_user(db_user, statement_uid)
    if val:
        transaction.commit()

    return val


def add_seen_argument(argument_uid, db_user):
    """
    Adds the uid of the argument into the seen_by list as well as all included statements, mapped with the given user uid

    :param db_user: current user
    :param argument_uid: uid of the argument
    :return: undefined
    """
    if not is_integer(argument_uid) or not isinstance(db_user, User):
        return False
    logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', for user ' + str(db_user.uid))

    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)
    if not db_argument:
        return False

    __argument_seen_by_user(db_user, argument_uid)

    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    if not db_premises:
        return False

    logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', premise count ' + str(len(db_premises)))
    for p in db_premises:
        logger('VotingHelper', 'add_seen_argument', 'argument ' + str(argument_uid) + ', add premise ' + str(p.statement_uid))
        __statement_seen_by_user(db_user, p.statement_uid)

    # find the conclusion and mark all arguments on the way
    while db_argument.conclusion_uid is None:
        db_argument = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)
        __argument_seen_by_user(db_user, argument_uid)

    logger('VotingHelper', 'add_seen_argument', 'conclusion ' + str(db_argument.conclusion_uid))
    __statement_seen_by_user(db_user, db_argument.conclusion_uid)

    transaction.commit()

    return True


def clear_vote_and_seen_values_of_user(nickname):
    """
    Delete all votes/clicks/mards

    :param nickname: User.nickname
    :return: Boolean
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return False

    __clear_seen_by_values_of_user(db_user.uid)
    __clear_marks_of_user(db_user.uid)
    __clear_clicks_of_user(db_user.uid)

    DBDiscussionSession.flush()
    transaction.commit()
    return True


def __clear_marks_of_user(user_uid):
    """
    Deletes all marks of given user

    :param user_uid: User.uid
    :return:
    """
    DBDiscussionSession.query(MarkedArgument).filter_by(author_uid=user_uid).delete()
    DBDiscussionSession.query(MarkedStatement).filter_by(author_uid=user_uid).delete()


def __clear_clicks_of_user(user_uid):
    """
    Deletes all votes of given user

    :param user_uid: User.uid
    :return:
    """
    DBDiscussionSession.query(ClickedArgument).filter_by(author_uid=user_uid).delete()
    DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=user_uid).delete()


def __clear_seen_by_values_of_user(user_uid):
    """
    Deletes all seen by values of given user

    :param user_uid: User.uid
    :return:
    """
    DBDiscussionSession.query(SeenStatement).filter_by(user_uid=user_uid).delete()
    DBDiscussionSession.query(SeenArgument).filter_by(user_uid=user_uid).delete()


def __click_argument(argument, user, is_up_vote):
    """
    Check if there is a vote for the argument. If not, we will create a new one, otherwise the current one will be
    invalid an we will create a new entry.

    :param argument: Argument
    :param user: User
    :param is_up_vote: Boolean
    :return: None
    """
    if argument is None:
        logger('VotingHelper', '__click_argument', 'argument is None')
        return

    logger('VotingHelper', '__click_argument', 'argument ' + str(argument.uid) + ', user ' + user.nickname)

    db_all_valid_votes = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == argument.uid,
                                                                                ClickedArgument.author_uid == user.uid,
                                                                                ClickedArgument.is_valid == True))
    db_current_vote = db_all_valid_votes.filter_by(is_up_vote=is_up_vote).first()
    db_old_votes = db_all_valid_votes.all()

    # we are not deleting opposite votes for detecting opinion changes!
    if db_current_vote in db_old_votes:
        db_old_votes.remove(db_current_vote)

    for old_vote in db_old_votes:
        logger('VotingHelper', '__click_argument', 'setting old vote ' + str(old_vote.uid) + ' as invalid')
        old_vote.set_valid(False)
    DBDiscussionSession.flush()

    db_new_vote = None
    if not db_current_vote:
        logger('VotingHelper', '__click_argument', 'add vote for argument ' + str(argument.uid))
        db_new_vote = ClickedArgument(argument_uid=argument.uid, author_uid=user.uid, is_up_vote=is_up_vote, is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()

    # do we have some inconsequences?
    db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=argument.conclusion_uid).all()
    for arg in db_arguments:
        db_votes_for_arg = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == arg.uid,
                                                                                  ClickedArgument.is_valid == True,
                                                                                  ClickedArgument.author_uid == user.uid,
                                                                                  ClickedArgument.is_up_vote == argument.is_supportive)).all()
        if db_new_vote and db_new_vote in db_votes_for_arg:
            db_votes_for_arg.remove(db_new_vote)

        for vote in db_votes_for_arg:
            vote.set_valid(False)
    DBDiscussionSession.flush()


def __click_statement(statement, db_user, is_up_vote):
    """
    Check if there is a vote for the statement. If not, we will create a new one, otherwise the current one will be
    invalid an we will create a new entry.

    :param statement: Statement
    :param db_user: User
    :param is_up_vote: Boolean
    :return: None
    """
    if statement is None:
        logger('VotingHelper', '__click_statement', 'statement is None')
        return

    logger('VotingHelper', '__click_statement', 'statement ' + str(statement.uid) + ', db_user ' + db_user.nickname)

    db_all_valid_votes = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == statement.uid,
                                                                                 ClickedStatement.author_uid == db_user.uid,
                                                                                 ClickedStatement.is_valid == True))
    db_current_vote = db_all_valid_votes.filter_by(is_up_vote=is_up_vote).first()
    db_old_votes = db_all_valid_votes.all()

    # we are not deleting opposite votes for detecting opinion changes!
    if db_current_vote in db_old_votes:
        db_old_votes.remove(db_current_vote)

    for old_vote in db_old_votes:
        logger('VotingHelper', '__click_statement', 'setting old vote' + str(old_vote.uid) + 'as invalid')
        old_vote.set_valid(False)
    DBDiscussionSession.flush()

    if not db_current_vote:
        logger('VotingHelper', '__click_statement', 'add vote for statement ' + str(statement.uid))
        db_new_vote = ClickedStatement(statement_uid=statement.uid, author_uid=db_user.uid, is_up_vote=is_up_vote, is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()


def __vote_premisesgroup(premisesgroup_uid, user, is_up_vote):
    """
    Calls statements-methods for every premise.

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
        __click_statement(db_statement, user, is_up_vote)


def __argument_seen_by_user(db_user, argument_uid):
    """
    Adds an reference for an seen argument

    :param db_user: current user
    :param argument_uid: uid of the argument
    :return: True if the argument was not seen by the user (until now), false otherwise
    """

    logger('VotingHelper', '__argument_seen_by_user', 'argument ' + str(argument_uid) + ', for user ' + str(db_user.uid))
    db_seen_by = DBDiscussionSession.query(SeenArgument).filter(and_(SeenArgument.argument_uid == argument_uid,
                                                                     SeenArgument.user_uid == db_user.uid)).first()
    if not db_seen_by:
        DBDiscussionSession.add(SeenArgument(argument_uid=argument_uid, user_uid=db_user.uid))
        DBDiscussionSession.flush()
        return True

    logger('VotingHelper', '__argument_seen_by_user', 'argument ' + str(argument_uid) + ', for user ' + str(db_user.uid) + ' was already seen')
    return False


def __statement_seen_by_user(db_user, statement_uid):
    """
    Adds an reference for an seen statement

    :param db_user: current user
    :param statement_uid: uid of the statement
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    db_seen_by = DBDiscussionSession.query(SeenStatement).filter(and_(SeenStatement.statement_uid == statement_uid,
                                                                      SeenStatement.user_uid == db_user.uid)).first()
    if not db_seen_by:
        logger('VotingHelper', '__statement_seen_by_user', 'statement ' + str(statement_uid) + ', for user ' + str(db_user.uid) + ' is now marked as seen')
        DBDiscussionSession.add(SeenStatement(statement_uid=statement_uid, user_uid=db_user.uid))
        DBDiscussionSession.flush()
        return True

    logger('VotingHelper', '__statement_seen_by_user', 'statement ' + str(statement_uid) + ', for user ' + str(db_user.uid) + ' was already seen')
    return False


def __premisegroup_seen_by_user(db_user, premisesgroup_uid):
    """
    Adds an reference for an seen premisesgroup

    :param db_user: current user
    :param premisesgroup_uid: uid of the premisesgroup
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    logger('VotingHelper', '__premisegroup_seen_by_user', 'Check premises of group ' + str(premisesgroup_uid))
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisesgroup_uid).all()
    for premise in db_premises:
        __statement_seen_by_user(db_user, premise.statement_uid)
