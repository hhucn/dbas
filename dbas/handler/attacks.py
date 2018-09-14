"""
This script handles attacks for given arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
import random
from typing import List, Tuple, Optional

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
from dbas.helper.relation import get_undermines_for_argument_uid, get_rebuts_for_argument_uid, \
    get_undercuts_for_argument_uid
from dbas.input_validator import is_integer
from dbas.lib import Relations, get_enabled_arguments_as_query

LOG = logging.getLogger(__name__)


def get_attack_for_argument(argument_uid: int, restrictive_attacks: List[Relations] = None,
                            restrictive_arg_uids: List[int] = None, last_attack: Relations = None,
                            history: str = '', redirected_from_jump: bool = False) -> Tuple[Optional[int],
                                                                                            Optional[Relations]]:
    """
    Selects an attack out of the web of reasons.

    :param argument_uid: Argument.uid
    :param restrictive_attacks: Array of Relations or None
    :param restrictive_arg_uids: Argument.uid
    :param last_attack: String
    :param history: History
    :param redirected_from_jump: Boolean
    :return: Returns a tuple with an attacking Argument.uid as well as the type of attack
    """
    restrictive_arg_uids = list(set(restrictive_arg_uids)) if restrictive_arg_uids else []
    history, redirected_from_jump = __setup_history(history, redirected_from_jump)
    restrictive_attacks = __setup_restrictive_attack_keys(argument_uid, restrictive_attacks, redirected_from_jump)
    LOG.debug("arg: %s, restricts: %s, %s, from_jump: %s", argument_uid, restrictive_attacks, restrictive_arg_uids,
              redirected_from_jump)

    attack_uids, attack_key, no_new_attacks = __get_attack_for_argument_by_random_in_range(argument_uid,
                                                                                           restrictive_attacks,
                                                                                           restrictive_arg_uids,
                                                                                           last_attack, history)

    if len(attack_uids) == 0 or attack_key not in Relations:
        return None, None

    attack_uid = random.choice(attack_uids)['id']
    LOG.debug("Return %s by %s", attack_key, attack_uid)
    return attack_uid, attack_key


def __setup_restrictive_attack_keys(argument_uid: int, restrictive_attacks: List[Relations],
                                    redirected_from_jump: bool) -> List[Relations]:
    """

    :param argument_uid:
    :param restrictive_attacks:
    :param redirected_from_jump:
    :return:
    """
    if not restrictive_attacks:
        return []

    is_current_arg_undercut = DBDiscussionSession.query(Argument).get(argument_uid).argument_uid is not None
    if is_current_arg_undercut and not redirected_from_jump:
        restrictive_attacks.append(Relations.UNDERCUT)

    return restrictive_attacks


def __setup_history(history: str, redirected_from_jump: bool) -> Tuple[str, bool]:
    """

    :param history:
    :param redirected_from_jump:
    :return:
    """
    if len(history) > 0 and not redirected_from_jump:
        history = history.split('-')
        index = -2 if len(history) > 1 else -1
        redirected_from_jump = 'jump' in history[index] or redirected_from_jump
    return history, redirected_from_jump


def get_arguments_by_conclusion(statement_uid: int, is_supportive: bool) -> List[Argument]:
    """
    Returns all arguments by their conclusion

    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :return: [Argument]
    """
    db_arguments = get_enabled_arguments_as_query()
    db_arguments = db_arguments.filter(Argument.is_supportive == is_supportive,
                                       Argument.conclusion_uid == statement_uid).all()
    if not db_arguments:
        return []

    return db_arguments


def get_forbidden_attacks_based_on_history(history: str) -> List[int]:
    """
    Returns all attacking uids from reaction steps of the history string

    :param history: String - history of the user
    :return: list of uids
    """
    forbidden_uids = []
    for split in history.split('-'):
        if 'reaction' in split and len(split.split('/')) > 4:
            uid = split.split('/')[4]
            if is_integer(uid):
                forbidden_uids.append(int(uid))
    return forbidden_uids


def __get_attack_for_argument_by_random_in_range(argument_uid: int, restrictive_attacks: List[Relations],
                                                 restrictive_arg_uids: List, last_attack: Relations,
                                                 history: str) -> Tuple[List[int], Optional[Relations], bool]:
    """
    Returns a dictionary with attacks. The attack itself is random out of the set of attacks, which were not done yet.
    Additionally returns id's of premises groups with [key + str(index) + 'id']

    :param argument_uid: Argument.uid
    :param restrictive_attacks: List of attacks which are forbidden
    :param restrictive_arg_uids: List of Arguments.uids which are forbidden
    :param last_attack: last attack of the user/system
    :param history: Users history
    :return: [Argument.uid], String, Boolean if no new attacks are found
    """
    list_of_attacks: List[Relations] = [relation for relation in Relations if relation is not Relations.SUPPORT]
    attack_list: List[Relations] = list(set(list_of_attacks) - set(restrictive_attacks))
    is_supportive = False
    new_attack_step = ''
    arg_uids = []
    attack_key = None

    while len(attack_list) > 0:
        attack = random.choice(attack_list)
        attack_list.remove(attack)

        # get attacks and kick all malicious steps
        arg_uids, is_supportive, attack_key = __get_attacks(attack, argument_uid, last_attack, is_supportive)
        arg_uids = list(__filter_malicious_steps(arg_uids, restrictive_arg_uids, history))

        if len(arg_uids) > 0 and isinstance(arg_uids[0], list):
            arg_uids = []

        if not arg_uids or len(arg_uids) == 0:
            continue

        # check if the step is already in history
        new_attack_step = '{}/{}/{}'.format(argument_uid, attack_key, arg_uids[0]['id'])

        if attack_key not in restrictive_attacks and new_attack_step not in history:  # no duplicated attacks
            break  # found an attack

        attack_key = None  # reset, because maybe the while loop is not triggered again
        arg_uids = []

    return arg_uids, attack_key, new_attack_step in history


def __filter_malicious_steps(seq: List[dict], restriction_on_args: List[Relations], history) -> List[dict]:
    """
    Filters every step which was already shown based on the users history or which is restricted

    :param seq: List of dicts with id and text as field, which maybe the current attack step
    :param restriction_on_args: list of forbidden attacks
    :param history: users history as string
    :return: List of dicts with id and text as field
    """
    if not seq or len(seq) == 0:
        yield []
    else:
        for el in seq:
            if el['id'] not in restriction_on_args and '/{}'.format(el['id']) not in str(history):
                yield el


def __get_attacks(attack: Relations, argument_uid: int, last_attack: Relations,
                  is_supportive: bool) -> Tuple[List[dict], bool, Relations]:
    """
    Returns a list of all attacking arguments based on input...

    :param attack:
    :param argument_uid:
    :param last_attack:
    :param is_supportive:
    :return: List of dicts with id and text as field
    """
    mod_attack = attack

    if attack == Relations.UNDERMINE:
        attacks = get_undermines_for_argument_uid(argument_uid, is_supportive)
        # special case when undermining an undermine (docs/dbas/logic.html?highlight=undermine#dialog-sequence)
        is_supportive = last_attack == Relations.UNDERMINE

    elif attack == Relations.REBUT:
        db_arg = DBDiscussionSession.query(Argument).get(argument_uid)
        if not (db_arg and db_arg.argument_uid is None):
            mod_attack = Relations.UNDERCUT
        attacks = get_rebuts_for_argument_uid(argument_uid)

    else:
        attacks = get_undercuts_for_argument_uid(argument_uid)

    return attacks, is_supportive, mod_attack
