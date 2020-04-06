"""
Class for handling votes of each user.

Functions for setting votes of users. They set votes by clicking the statements in D-BAS.
We are not deleting opposite votes for detecting opinion changes!
"""

import logging

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, ClickedArgument, ClickedStatement, User, \
    SeenStatement, SeenArgument, MarkedArgument, MarkedStatement
from dbas.input_validator import is_integer
from dbas.lib import nick_of_anonymous_user

LOG = logging.getLogger(__name__)


def add_click_for_argument(argument: Argument, user: User) -> bool:
    """
    Increases clicks of a given argument.

    :param argument: Argument from User
    :param user: User
    :return:
    """
    if user.nickname == nick_of_anonymous_user:
        LOG.debug("User is anonymous, not counting clicks")
        return False
    LOG.debug("Increasing vote for argument %s ", argument.uid)

    if argument.argument_uid is None:
        LOG.debug("Undercut depth 0")
        __add_click_for_argument(user, argument)
    else:
        db_undercuted_arg_step_1: Argument = argument.attacks

        if db_undercuted_arg_step_1.argument_uid is None:
            LOG.debug("Undercut depth 1")
            __add_click_for_undercut_step_1(argument, db_undercuted_arg_step_1, user)
        else:
            LOG.debug("Undercut depth 2")
            __add_click_for_undercut_step_2(argument, db_undercuted_arg_step_1, user)

    return True


def __add_click_for_argument(user: User, argument: Argument):
    """
    Add click for a specific argument

    :param user: User
    :param argument: Argument
    :return: None
    """
    conclusion = argument.conclusion

    # set vote for the argument (relation), its premisegroup and conclusion
    __click_argument(argument, user, True)
    __vote_premisesgroup(argument.premisegroup_uid, user, True)
    __click_statement(conclusion, user, argument.is_supportive)

    # add seen values
    __argument_seen_by_user(user, argument)


def __add_click_for_undercut_step_1(argument: Argument, undercuted_arg_step_1: Argument, user: User):
    """
    Add clicks for an first order undercut

    :param argument: Argument
    :param undercuted_arg_step_1: Argument
    :param user: User
    :return: None
    """

    undercuted_arg_step_1_concl: Statement = undercuted_arg_step_1.conclusion

    # vote for the current argument
    __click_argument(argument, user, True)
    __vote_premisesgroup(argument.premisegroup_uid, user, True)

    # vote against the undercutted argument
    __click_argument(undercuted_arg_step_1, user, argument.is_supportive)
    __vote_premisesgroup(undercuted_arg_step_1.premisegroup_uid, user, True)
    # if the conclusion of the undercutted argument was supported, we will attack it and vice versa
    __click_statement(undercuted_arg_step_1_concl, user, not argument.is_supportive)

    # add seen values
    __argument_seen_by_user(user, argument)
    __argument_seen_by_user(user, undercuted_arg_step_1)


def __add_click_for_undercut_step_2(argument: Argument, undercuted_arg_step_1: Argument, user: User):
    """
    Add clicks for an second order undercut

    :param argument: Argument
    :param undercuted_arg_step_1: Argument
    :param user: User
    :return: None
    """

    # we are undercutting an undercut
    undercuted_arg_step_2: Argument = undercuted_arg_step_1.attacks

    # vote for the current argument
    __vote_premisesgroup(argument.premisegroup_uid, user, True)
    __click_argument(argument, user, True)

    # vote against the undercutted argument
    __click_argument(undercuted_arg_step_1, user, False)
    __vote_premisesgroup(undercuted_arg_step_1.premisegroup_uid, user, False)

    # vote NOT for the undercutted undercut

    # add seen values
    __argument_seen_by_user(user, argument)
    __argument_seen_by_user(user, undercuted_arg_step_1)
    __argument_seen_by_user(user, undercuted_arg_step_2)


def add_click_for_statement(stmt_or_arg: Statement, db_user: User, supportive: bool):
    """
    Adds a clicks for the given statement.

    :param db_user: User
    :param stmt_or_arg: Statement
    :param supportive: boolean
    :return: Boolean
    """

    LOG.debug("Increasing %s vote for statement %s", 'up' if supportive else 'down', stmt_or_arg.uid)

    if db_user.nickname == nick_of_anonymous_user:
        return False

    __click_statement(stmt_or_arg, db_user, supportive)
    __statement_seen_by_user(db_user, stmt_or_arg)
    return True


def add_seen_statement(statement: Statement, user: User):
    """
    Adds the uid of the statement into the seen_by list, mapped with the given user uid

    :param user:current user
    :param statement: Statement which was seen by the user.
    :return: undefined
    """
    if not isinstance(statement, Statement) or not isinstance(user, User) or user.is_anonymous():
        return False
    LOG.debug("Statement %s, for user %s", statement, user.uid)

    val = __statement_seen_by_user(user, statement)

    return val


def add_seen_argument(argument_uid: int, user: User):
    """
    Adds the uid of the argument into the seen_by list as well as all included statements, mapped with the given user
    uid

    :param user: current user
    :param argument_uid: uid of the argument
    :return: undefined
    """
    if not is_integer(argument_uid) or not isinstance(user, User) or user.is_anonymous():
        return False
    LOG.debug("Argument %s, for user %s", argument_uid, user.uid)

    argument: Argument = DBDiscussionSession.query(Argument).get(argument_uid)

    __argument_seen_by_user(user, argument)
    for premise in argument.premisegroup.premises:
        __statement_seen_by_user(user, premise.statement)

    if argument.conclusion:
        __statement_seen_by_user(user, argument.conclusion)
    else:
        while not argument.conclusion:
            argument = argument.attacks
            __argument_seen_by_user(user, argument)

    return True


def clear_vote_and_seen_values_of_user(user: User):
    """
    Delete all votes/clicks/mards

    :param user: User
    :return: Boolean
    """
    DBDiscussionSession.query(SeenStatement).filter_by(user=user).delete()
    DBDiscussionSession.query(SeenArgument).filter_by(user_uid=user.uid).delete()
    DBDiscussionSession.query(MarkedArgument).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(MarkedStatement).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(ClickedArgument).filter_by(author_uid=user.uid).delete()
    DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=user.uid).delete()

    DBDiscussionSession.flush()
    # transaction.commit()
    return True


def __click_argument(argument, user, is_up_vote):
    """
    Check if there is a vote for the argument. If not, we will create a new one, otherwise the current one will be
    invalid and we will create a new entry.

    :param argument: Argument
    :param user: User
    :param is_up_vote: Boolean
    :return: None
    """
    if argument is None:
        LOG.debug("Argument is None")
        return

    LOG.debug("Argument %s, user %s", argument.uid, user.nickname)

    db_all_valid_votes = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.argument_uid == argument.uid,
                                                                           ClickedArgument.author_uid == user.uid,
                                                                           ClickedArgument.is_valid == True)
    db_current_vote = db_all_valid_votes.filter_by(is_up_vote=is_up_vote).first()
    db_old_votes = db_all_valid_votes.all()

    # we are not deleting opposite votes for detecting opinion changes!
    if db_current_vote in db_old_votes:
        db_old_votes.remove(db_current_vote)

    for old_vote in db_old_votes:
        LOG.debug("Setting old vote %s as invalid", old_vote.uid)
        old_vote.set_valid(False)
    DBDiscussionSession.flush()

    db_new_vote = None
    if not db_current_vote:
        LOG.debug("Add vote for argument %s", argument.uid)
        db_new_vote = ClickedArgument(argument=argument, user=user, is_up_vote=is_up_vote,
                                      is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()

    # do we have some inconsequences?
    db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=argument.conclusion_uid).all()
    for arg in db_arguments:
        db_votes_for_arg = DBDiscussionSession.query(ClickedArgument).filter(
            ClickedArgument.argument_uid == arg.uid,
            ClickedArgument.is_valid == True,
            ClickedArgument.author_uid == user.uid,
            ClickedArgument.is_up_vote == argument.is_supportive).all()
        if db_new_vote and db_new_vote in db_votes_for_arg:
            db_votes_for_arg.remove(db_new_vote)

        for vote in db_votes_for_arg:
            vote.set_valid(False)
    DBDiscussionSession.flush()


def __click_statement(statement, db_user, is_up_vote):
    """
    Check if there is a vote for the statement. If not, we will create a new one, otherwise the current one will be
    invalid and we will create a new entry.

    :param statement: Statement
    :param db_user: User
    :param is_up_vote: Boolean
    :return: None
    """
    if statement is None:
        LOG.debug("Statement is None")
        return

    LOG.debug("Statement %s, db_user %s", statement.uid, db_user.nickname)

    db_all_valid_votes = DBDiscussionSession.query(ClickedStatement).filter(
        ClickedStatement.statement_uid == statement.uid,
        ClickedStatement.author_uid == db_user.uid,
        ClickedStatement.is_valid == True)
    db_current_vote = db_all_valid_votes.filter_by(is_up_vote=is_up_vote).first()
    db_old_votes = db_all_valid_votes.all()

    # we are not deleting opposite votes for detecting opinion changes!
    if db_current_vote in db_old_votes:
        db_old_votes.remove(db_current_vote)

    for old_vote in db_old_votes:
        LOG.debug("Setting old vote %s as invalid", old_vote.uid)
        old_vote.set_valid(False)
    DBDiscussionSession.flush()

    if not db_current_vote:
        LOG.debug("Add vote for statement %s", statement.uid)
        db_new_vote = ClickedStatement(statement=statement, author_uid=db_user.uid, is_up_vote=is_up_vote,
                                       is_valid=True)
        DBDiscussionSession.add(db_new_vote)
        DBDiscussionSession.flush()


def __vote_premisesgroup(premisegroup_uid, user, is_up_vote):
    """
    Calls statements-methods for every premise.

    :param premisegroup_uid: PremiseGroup.uid
    :param user: User
    :param is_up_vote: Boolean
    :return:
    """
    if premisegroup_uid is None or premisegroup_uid == 0:
        LOG.debug("Premisegroup_uid is None")
        return

    LOG.debug("Premisegroup_uid %s, user %s", premisegroup_uid, user.nickname)

    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=premisegroup_uid).all()
    for premise in db_premises:
        db_statement = DBDiscussionSession.query(Statement).get(premise.statement_uid)
        __click_statement(db_statement, user, is_up_vote)


def __argument_seen_by_user(user: User, argument: Argument):
    """
    Adds a reference for a seen argument

    :param user: current user
    :param argument: uid of the argument
    :return: True if the argument was not seen by the user (until now), false otherwise
    """

    db_seen_by = DBDiscussionSession.query(SeenArgument).filter(SeenArgument.argument_uid == argument.uid,
                                                                SeenArgument.user_uid == user.uid).first()
    if not db_seen_by:
        DBDiscussionSession.add(SeenArgument(argument=argument, user=user))
        DBDiscussionSession.flush()
        return True

    return False


def __statement_seen_by_user(user: User, statement: Statement):
    """
    Adds a reference for a seen statement

    :param db_user: current user
    :param statement: uid of the statement
    :return: True if the statement was not seen by the user (until now), false otherwise
    """
    db_seen_by = DBDiscussionSession.query(SeenStatement).filter(SeenStatement.statement_uid == statement.uid,
                                                                 SeenStatement.user_uid == user.uid).first()
    if not db_seen_by:
        DBDiscussionSession.add(SeenStatement(statement=statement, user=user))
        DBDiscussionSession.flush()
        return True

    return False
