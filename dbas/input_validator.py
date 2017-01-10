"""
Methods for validating input params given via url or ajax

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise
from .logger import logger
from sqlalchemy import and_


def is_integer(variable, ignore_empty_case=False):
    """
    Validates if variable is an integer.

    :param variable: some input
    :param ignore_empty_case:
    :rtype: boolean
    """
    if variable is None:
        return False
    if ignore_empty_case:
        if len(str(variable)) == 0:
            return True
    try:
        int(variable)
        return True
    except (ValueError, TypeError):
        return False


def check_reaction(attacked_arg_uid, attacking_arg_uid, relation, is_history=False):
    """
    Checks whether the attacked argument uid and the attacking argument uid are connected via the given relation

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :param relation: String
    :param is_history: Boolean
    :return: Boolean
    """
    logger('Validator', 'check_reaction', relation + ' from ' + str(attacking_arg_uid) + ' to ' + str(attacked_arg_uid))

    if not is_integer(attacked_arg_uid) or not is_integer(attacking_arg_uid):
        return False

    if is_argument_forbidden(attacked_arg_uid) or is_argument_forbidden(attacking_arg_uid):
        return False

    if relation == 'undermine':
        return related_with_undermine(attacked_arg_uid, attacking_arg_uid)

    elif relation == 'undercut':
        return related_with_undercut(attacked_arg_uid, attacking_arg_uid)

    elif relation == 'rebut':
        return related_with_rebut(attacked_arg_uid, attacking_arg_uid)

    elif relation.startswith('end') and not is_history:
        if str(attacking_arg_uid) != '0':
            return False
        return True

    else:
        logger('Validator', 'check_reaction', 'else-case')
        return False


def check_belonging_of_statement(issue_uid, statement_uid):
    """
    Check whether current Statement.uid belongs to the given Issue

    :param issue_uid: Issue.uid
    :param statement_uid: Statement.uid
    :return:
    """
    db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == statement_uid,
                                                                    Statement.issue_uid == issue_uid)).first()
    return True if db_statement else False


def check_belonging_of_argument(issue_uid, argument_uid):
    """
    Check whether current Argument.uid belongs to the given Issue

    :param issue_uid: Issue.uid
    :param argument_uid: Argument.uid
    :return: Boolean
    """
    db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == argument_uid,
                                                                  Argument.issue_uid == issue_uid)).first()
    return True if db_argument else False


def check_belonging_of_premisegroups(issue_uid, premisegroups):
    """
    Check whether all Groups in Premisgroups belongs to the given Issue

    :param issue_uid: Issue.uid
    :param premisegroups: [PremiseGroup.uid]
    :return: Boolean
    """
    for group_id in premisegroups:
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group_id).all()
        for premise in db_premises:
            if premise.issue_uid != issue_uid:
                return False
    return True


def is_position(statement_uid):
    """
    True if current statement is a position

    :param statement_uid: Statement.uid
    :return: Boolean
    """
    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    return True if db_statement.is_startpoint else False


def related_with_undermine(attacked_arg_uid, attacking_arg_uid):
    """

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    # conclusion of the attacking argument
    db_attacking_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacking_arg_uid).first()
    if not db_attacking_arg:
        return False

    # which pgroups has the conclusion as premise
    db_attacked_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=db_attacking_arg.conclusion_uid).all()
    if not db_attacked_premise:
        return False

    # and does the attacked argument has this premisegroup as premisegroup
    for premise in db_attacked_premise:
        db_attacked_arg = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == attacked_arg_uid,
                                                                          Argument.premisesgroup_uid == premise.premisesgroup_uid,
                                                                          Argument.is_supportive == False)).first()
        if db_attacked_arg:
            return True
    return False


def related_with_undercut(attacked_arg_uid, attacking_arg_uid):
    """

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    db_attacking_arg = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == attacking_arg_uid,
                                                                       Argument.argument_uid == attacked_arg_uid)).first()
    return True if db_attacking_arg else False


def related_with_rebut(attacked_arg_uid, attacking_arg_uid):
    """

    :param attacked_arg_uid: Argument.uid
    :param attacking_arg_uid: Argument.uid
    :return: Boolean
    """
    db_attacking_arg = DBDiscussionSession.query(Argument).get(attacking_arg_uid)
    db_attacked_arg = DBDiscussionSession.query(Argument).get(attacked_arg_uid)
    if not db_attacked_arg or not db_attacking_arg:
        return False

    # do have both arguments the same conclusion?
    same_conclusion = db_attacking_arg.conclusion_uid == db_attacked_arg.conclusion_uid
    not_none = db_attacked_arg.conclusion_uid is not None
    attacking1 = not db_attacking_arg.is_supportive and db_attacked_arg.is_supportive
    attacking2 = not db_attacked_arg.is_supportive and db_attacking_arg.is_supportive
    attacking = attacking1 or attacking2
    return True if same_conclusion and not_none and attacking else False


def related_with_support(attacked_arg_uid, attacking_arg_uid):
    """

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
    supportive = db_first_arg.is_supportive and db_second_arg.is_supportive
    return True if same_conclusion and not_none and supportive else False


def get_relation_between_arguments(arg1_uid, arg2_uid):
    """

    :param arg1_uid: Argument.uid
    :param arg2_uid: Argument.uid
    :return: String or None
    """

    if related_with_undermine(arg1_uid, arg2_uid):
        logger('InputValidator', 'get_relation_between_arguments', str(arg1_uid) + ' undermine ' + str(arg2_uid))
        return 'undermine'

    elif related_with_undercut(arg1_uid, arg2_uid):
        logger('InputValidator', 'get_relation_between_arguments', str(arg1_uid) + ' undermine ' + str(arg2_uid))
        return 'undercut'

    elif related_with_rebut(arg1_uid, arg2_uid):
        logger('InputValidator', 'get_relation_between_arguments', str(arg1_uid) + ' undermine ' + str(arg2_uid))
        return 'rebut'

    elif related_with_support(arg1_uid, arg2_uid):
        logger('InputValidator', 'get_relation_between_arguments', str(arg1_uid) + ' support ' + str(arg2_uid))
        return 'support'

    logger('InputValidator', 'get_relation_between_arguments', str(arg1_uid) + ' NONE ' + str(arg2_uid))
    return None


def is_argument_forbidden(uid):
    """

    :param uid:
    :return:
    """
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        return False
    return db_argument.is_disabled


def is_statement_forbidden(uid):
    """

    :param uid:
    :return:
    """
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    if not db_statement:
        return False
    return db_statement.is_disabled
