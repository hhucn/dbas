"""
Class for handling relations of arguments
"""

import random
from typing import Tuple, Union

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Premise, PremiseGroup, User, Issue
from dbas.input_validator import is_integer
from dbas.lib import get_enabled_arguments_as_query, get_enabled_premises_as_query
from dbas.strings.lib import start_with_capital


def get_undermines_for_argument_uid(argument_uid, is_supportive=False):
    """
    Returns all uid's of undermines for the argument.

    :return argument_uid: UID of the argument
    :return is_supportive: Boolean
    :return: array with dict() with id (of argument) and text.
    """
    # logger('RelationHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(self.argument_uid))
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    db_arguments = get_enabled_arguments_as_query()
    db_attacked_argument = db_arguments.filter_by(uid=argument_uid).first()
    if not db_attacked_argument:
        return []

    db_premises = get_enabled_premises_as_query()
    db_attacked_premises = db_premises \
        .filter_by(premisegroup_uid=db_attacked_argument.premisegroup_uid) \
        .order_by(Premise.premisegroup_uid.desc()).all()

    premises_as_statements_uid = set()
    for premise in db_attacked_premises:
        premises_as_statements_uid.add(premise.statement_uid)

    if len(premises_as_statements_uid) == 0:
        return []

    return __get_undermines_for_premises(premises_as_statements_uid, is_supportive)


def get_undercuts_for_argument_uid(argument_uid):
    """
    Calls self.__get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, False)

    :return argument_uid: UID of the argument
    :return: array with dict() with id (of argumet) and text.
    """
    # logger('RelationHelper', 'get_undercuts_for_argument_uid', 'main ' + str(self.argument_uid))
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    return __get_attack_or_support_for_justification_of_argument_uid(argument_uid, False)


def get_rebuts_for_argument_uid(argument_uid):
    """
    Returns all uid's of rebuts for the argument.

    :return argument_uid: UID of the argument
    :return: array with dict() with id (of argumet) and text.
    """
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    # logger('RelationHelper', 'get_rebuts_for_argument_uid', 'main ' + str(self.argument_uid))
    db_arguments = get_enabled_arguments_as_query()
    db_argument = db_arguments.filter_by(uid=int(argument_uid)).first()
    if not db_argument:
        return None

    if db_argument.conclusion_uid is not None:
        return __get_rebuts_for_arguments_conclusion_uid(db_argument)
    else:
        return get_undercuts_for_argument_uid(argument_uid)


def __get_rebuts_for_arguments_conclusion_uid(db_argument):
    """
    Returns a list with dict(). They contain id and text of the rebuttal's pgroups

    :return argument_uid: UID of the argument
    :param db_argument: Argument
    :return: [dict()]
    """
    return_array = []
    given_rebuts = set()
    db_arguments = get_enabled_arguments_as_query()
    db_rebuts = db_arguments.filter(Argument.is_supportive == (not db_argument.is_supportive),
                                    Argument.conclusion_uid == db_argument.conclusion_uid).all()
    for rebut in db_rebuts:

        if rebut.premisegroup_uid not in given_rebuts:
            given_rebuts.add(rebut.premisegroup_uid)
            tmp_dict = dict()
            tmp_dict['id'] = rebut.uid
            text = rebut.get_premisegroup_text()
            tmp_dict['text'] = start_with_capital(text)
            return_array.append(tmp_dict)
    return return_array


def get_supports_for_argument_uid(argument_uid):
    """
    Returns all uid's of supports for the argument.

    :return argument_uid: UID of the argument
    :return: array with dict() with id (of argumet) and text
    """
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    return_array = []
    given_supports = set()
    db_arguments = get_enabled_arguments_as_query()
    db_argument = db_arguments.filter_by(uid=argument_uid).join(PremiseGroup).first()
    if not db_argument:
        return []

    db_arguments_premises = DBDiscussionSession.query(Premise).filter_by(
        premisegroup_uid=db_argument.premisegroup_uid).all()

    for arguments_premises in db_arguments_premises:
        db_arguments = get_enabled_arguments_as_query()
        db_supports = db_arguments.filter(Argument.conclusion_uid == arguments_premises.statement_uid,
                                          Argument.is_supportive == True).join(PremiseGroup).all()
        if not db_supports:
            continue

        for support in db_supports:
            if support.premisegroup_uid not in given_supports:
                tmp_dict = dict()
                tmp_dict['id'] = support.uid
                tmp_dict['text'] = support.get_premisegroup_text()
                return_array.append(tmp_dict)
                given_supports.add(support.premisegroup_uid)

    return [] if len(return_array) == 0 else return_array


def set_new_undermine_or_support_for_pgroup(premisegroup: PremiseGroup, current_argument: Argument,
                                            is_supportive: bool,
                                            db_user: User, db_issue: Issue):
    """
    Inserts a new undermine or support with the given parameters.

    :param premisegroup: premisegroup
    :param current_argument: Argument
    :param is_supportive: Boolean
    :param db_user: User
    :param issue: Issue.uid
    :return: Argument, Boolean if the argument is a duplicate
    """
    already_in = []

    # all premises out of current pgroup
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=current_argument.premisegroup_uid).all()
    for premise in db_premises:
        new_arguments = []
        db_arguments = get_enabled_arguments_as_query()
        db_argument = db_arguments.filter(Argument.premisegroup_uid == premisegroup.uid,
                                          Argument.is_supportive == True,
                                          Argument.conclusion_uid == premise.statement_uid).first()
        if db_argument:
            continue

        db_tmp = premisegroup.premises
        if any([p.statement_uid == premise.statement_uid for p in db_tmp]):
            return False

        new_arguments.append(
            Argument(premisegroup=premisegroup, is_supportive=is_supportive, author=db_user.uid, issue=db_issue.uid,
                     conclusion=premise.statement_uid))

        if len(new_arguments) > 0:
            DBDiscussionSession.add_all(new_arguments)
            DBDiscussionSession.flush()
            transaction.commit()

            already_in += new_arguments

    rnd = random.randint(0, len(already_in) - 1)
    return already_in[rnd]


def set_new_undercut(premisegroup: PremiseGroup, current_argument: Argument, db_user: User, issue: Issue) \
        -> Tuple[Argument, bool]:
    """
    Inserts a new undercut with the given parameters.

    :param premisegroup: premisegroup
    :param current_argument: Argument
    :param db_user: User
    :param issue: Issue.uid
    :return: Argument, Boolean if the argument is a duplicate
    """
    # duplicate?
    db_argument = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == premisegroup.uid,
                                                             Argument.is_supportive == False,
                                                             Argument.argument_uid == current_argument.uid).first()
    if db_argument:
        return db_argument, True
    else:
        new_argument = Argument(premisegroup=premisegroup,
                                is_supportive=False,
                                author=db_user.uid,
                                issue=issue.uid)
        new_argument.set_conclusions_argument(current_argument.uid)
        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()
        transaction.commit()
        return new_argument, False


def set_new_rebut(premisegroup: PremiseGroup, current_argument: Argument, db_user: User, db_issue: Issue) \
        -> Tuple[Union[Argument, bool], bool]:
    """
    Inserts a new rebut with the given parameters.

    :param premisegroup: premisegroup
    :param current_argument: Argument
    :param db_user: User
    :return: Argument, Boolean if the argument is a duplicate
    """
    return __set_rebut_or_support(premisegroup, current_argument, db_user, db_issue, False)


def set_new_support(premisegroup: PremiseGroup, current_argument: Argument, db_user: User, db_issue: Issue) \
        -> Tuple[Union[Argument, bool], bool]:
    """
    Inserts a new support with the given parameters.

    :param premisegroup: premisegroup
    :param current_argument: Argument
    :param db_user: User
    :param db_issue: Issue
    :return: Argument, Boolean if the argument is a duplicate
    """
    return __set_rebut_or_support(premisegroup, current_argument, db_user, db_issue, True)


def __set_rebut_or_support(premisegroup: PremiseGroup, current_argument: Argument, db_user: User, db_issue: Issue,
                           is_supportive: bool) -> Tuple[Union[Argument, bool], bool]:
    db_arguments = get_enabled_arguments_as_query()
    db_argument = db_arguments.filter(Argument.premisegroup_uid == premisegroup.uid,
                                      Argument.is_supportive == True,
                                      Argument.conclusion_uid == current_argument.conclusion_uid).first()
    if db_argument:
        return db_argument, True
    else:
        db_tmp = premisegroup.premises
        if any([p.statement_uid == current_argument.conclusion_uid for p in db_tmp]):
            return False, False
        new_argument = Argument(premisegroup=premisegroup,
                                is_supportive=is_supportive,
                                author=db_user.uid,
                                issue=db_issue.uid,
                                conclusion=current_argument.conclusion_uid)
        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()
        transaction.commit()
        return new_argument, False


def __get_attack_or_support_for_justification_of_argument_uid(argument_uid, is_supportive):
    """
    Querys all

    :param argument_uid: Argument.uid
    :param is_supportive: Boolean
    :return: [{id, text}] or 0
    """
    return_array = []
    db_arguments = get_enabled_arguments_as_query()
    db_related_arguments = db_arguments.filter(Argument.is_supportive == is_supportive,
                                               Argument.argument_uid == argument_uid).all()
    given_relations = set()

    if not db_related_arguments:
        return None

    __add_to_return_array(return_array, db_related_arguments, given_relations)

    return return_array


def __get_undermines_for_premises(premises_as_statements_uid, is_supportive=False):
    """
    Querys all undermines for the given statements

    :param premises_as_statements_uid:
    :param is_supportive
    :return: [{id, text}]
    """
    return_array = []
    given_undermines = set()
    for s_uid in premises_as_statements_uid:
        db_arguments = get_enabled_arguments_as_query()
        db_undermines = db_arguments.filter(Argument.is_supportive == is_supportive,
                                            Argument.conclusion_uid == s_uid).all()
        __add_to_return_array(return_array, db_undermines, given_undermines)
    return return_array


def __add_to_return_array(return_array, db_arguments, given_argument):
    for argument in db_arguments:
        if argument.premisegroup_uid not in given_argument:
            given_argument.add(argument.premisegroup_uid)
            tmp_dict = dict()
            tmp_dict['id'] = argument.uid
            tmp_dict['text'] = argument.get_premisegroup_text()
            return_array.append(tmp_dict)
