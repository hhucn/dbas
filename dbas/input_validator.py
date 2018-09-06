"""
Methods for validating input params given via url or ajax

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import logging
from typing import Optional, Union

from dbas.lib import Relations
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, StatementToIssue


def is_integer(variable, ignore_empty_case=False):
    """
    Validates if variable is an integer.

    :param variable: some input
    :param ignore_empty_case:
    :rtype: boolean
    """
    if variable is None:
        return False
    if ignore_empty_case and len(str(variable)) == 0:
        return True
    try:
        int(variable)
        return True
    except (ValueError, TypeError):
        return False


def check_reaction(attacked_arg_uid: Union[int, str], attacking_arg_uid: Union[int, str], relation: Relations):
    """
    Checks whether the attacked argument uid and the attacking argument uid are connected via the given relation

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :param relation: Relations
    :return: Boolean
    """
    log = logging.getLogger(__name__)
    log.debug("%s from %s to %s", relation.value, attacking_arg_uid, attacked_arg_uid)

    malicious_val = [
        not is_integer(attacked_arg_uid),
        not is_integer(attacking_arg_uid),
        is_argument_forbidden(attacked_arg_uid),
        is_argument_forbidden(attacking_arg_uid)
    ]

    if any(malicious_val):
        return False

    relation_mapper = {
        Relations.UNDERMINE: related_with_undermine,
        Relations.UNDERCUT: related_with_undercut,
        Relations.REBUT: related_with_rebut,
        Relations.SUPPORT: related_with_support
    }

    if relation in relation_mapper:
        return relation_mapper[relation](attacked_arg_uid, attacking_arg_uid)

    log.debug("else-case")
    return False


def check_belonging_of_statement(issue_uid, statement_uid):
    """
    Check whether current Statement.uid belongs to the given Issue

    :param issue_uid: Issue.uid
    :param statement_uid: Statement.uid
    :return:
    """
    db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter(
        StatementToIssue.statement_uid == statement_uid,
        StatementToIssue.issue_uid == issue_uid).first()
    return db_statement2issue is not None


def check_belonging_of_arguments(issue_uid: int, argument_uids: list) -> bool:
    """
    Check whether current Argument.uid belongs to the given Issue

    :param issue_uid: Issue.uid
    :param argument_uids: Argument.uid
    :return: Boolean
    """
    db_argument = DBDiscussionSession.query(Argument).filter(Argument.uid.in_(argument_uids),
                                                             Argument.issue_uid == issue_uid).all()
    return len(db_argument) == len(argument_uids)


def check_belonging_of_premisegroups(issue_uid, premisegroups):
    """
    Check whether all Groups in Premisgroups belongs to the given Issue

    :param issue_uid: Issue.uid
    :param premisegroups: [PremiseGroup.uid]
    :return: Boolean
    """
    all_premises = []
    for pgroup in premisegroups:
        all_premises += DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=pgroup).all()
    related = [premise.issue_uid == issue_uid for premise in all_premises]
    return all(related)


def is_position(statement_uid):
    """
    True if current statement is a position

    :param statement_uid: Statement.uid
    :return: Boolean
    """
    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    return db_statement.is_position


def related_with_undermine(attacked_arg_uid, attacking_arg_uid):
    """
    Check if first argument is undermines by the second one

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    # conclusion of the attacking argument
    db_attacking_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacking_arg_uid).first()
    if not db_attacking_arg:
        return False

    # which pgroups has the conclusion as premise
    db_attacked_premises = DBDiscussionSession.query(Premise).filter_by(
        statement_uid=db_attacking_arg.conclusion_uid).all()
    if not db_attacked_premises:
        return False

    attacked_args = DBDiscussionSession.query(Argument).filter_by(uid=attacked_arg_uid)
    undermines = [attacked_args.filter_by(premisegroup_uid=p.premisegroup_uid).first() for p in db_attacked_premises]
    return any(undermines)


def related_with_undercut(attacked_arg_uid, attacking_arg_uid):
    """
    Check if first argument is undercutted by the second one

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    db_attacking_arg = DBDiscussionSession.query(Argument).filter(Argument.uid == attacking_arg_uid,
                                                                  Argument.argument_uid == attacked_arg_uid).first()
    return db_attacking_arg is not None


def related_with_rebut(attacked_arg_uid, attacking_arg_uid):
    """
    Check if first argument is rebutted by the second one

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    db_attacking_arg = DBDiscussionSession.query(Argument).get(attacking_arg_uid)
    db_attacked_arg = DBDiscussionSession.query(Argument).get(attacked_arg_uid)
    if not db_attacked_arg or not db_attacking_arg or not db_attacked_arg.conclusion_uid:
        return False

    # do have both arguments the same conclusion?
    same_conclusion = db_attacking_arg.conclusion_uid == db_attacked_arg.conclusion_uid
    attacking1 = not db_attacking_arg.is_supportive and db_attacked_arg.is_supportive
    attacking2 = not db_attacked_arg.is_supportive and db_attacking_arg.is_supportive
    attacking = attacking1 or attacking2
    return same_conclusion and attacking


def related_with_support(attacked_arg_uid, attacking_arg_uid):
    """
    Check if both arguments support/attack the same conclusion

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    db_first_arg = DBDiscussionSession.query(Argument).get(attacking_arg_uid)
    db_second_arg = DBDiscussionSession.query(Argument).get(attacked_arg_uid)
    if not db_first_arg or not db_second_arg:
        return False

    not_none = db_first_arg.conclusion_uid is not None
    same_conclusion = db_first_arg.conclusion_uid == db_second_arg.conclusion_uid
    supportive = db_first_arg.is_supportive is db_second_arg.is_supportive

    return same_conclusion and not_none and supportive


def get_relation_between_arguments(arg1_uid: int, arg2_uid: int) -> Optional[Relations]:
    """
    Get the relation between given arguments

    :param arg1_uid: Argument.uid
    :param arg2_uid: Argument.uid
    :return: String or None
    """

    if related_with_undermine(arg1_uid, arg2_uid):
        return Relations.UNDERMINE

    if related_with_undercut(arg1_uid, arg2_uid):
        return Relations.UNDERCUT

    if related_with_rebut(arg1_uid, arg2_uid):
        return Relations.REBUT

    if related_with_support(arg1_uid, arg2_uid):
        return Relations.SUPPORT

    log = logging.getLogger(__name__)
    log.debug("%s NONE %s", arg1_uid, arg2_uid)
    return None


def is_argument_forbidden(uid):
    """
    Is the given argument disabled?

    :param uid: Argument.uid
    :return: Boolean
    """
    if not is_integer(uid):
        return False

    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        return False
    return db_argument.is_disabled
