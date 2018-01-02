"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

from enum import Enum, auto
from sqlalchemy import and_
from dbas.helper.relation import get_undermines_for_argument_uid, get_rebuts_for_argument_uid, \
    get_undercuts_for_argument_uid
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, ClickedArgument
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_arguments_as_query

# Millers Magic Number are 6 (https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two)
# Buddeley says 3-4
max_count = 5


class Attacks(Enum):
    UNDERMINE = auto()
    UNDERCUT = auto()
    REBUT = auto()


attack_mapping = {
    Attacks.UNDERMINE: 'undermine',
    Attacks.UNDERCUT: 'undercut',
    Attacks.REBUT: 'rebut',
    '': ''
}


def get_uids_of_best_positions(db_statements):
    """
    Returns the uids of the n best positions

    :param db_statements: [Statement]
    :return: [Statement.uid]
    """
    if db_statements is None:
        return []
    if len(db_statements) <= max_count:
        return [element.uid for element in db_statements]
    return __select_random([element.uid for element in db_statements])


def get_uids_of_best_statements_for_justify_position(db_arguments):
    """
    Get the best statements to justify the position

    :param db_arguments: [Statement]
    :return: [Statement.uid]
    """
    if db_arguments is None:
        return []
    if len(db_arguments) <= max_count:
        return [element.uid for element in db_arguments]
    return __select_random([element.uid for element in db_arguments])


def get_uids_of_best_statements_for_justify_argument(db_arguments):
    """
    Get the best statements to support an argument

    :param db_arguments: [Argument]
    :return: [Argument.uid]
    """
    if db_arguments is None:
        return []
    if len(db_arguments) <= max_count:
        return [element.uid for element in db_arguments]
    return __select_random([element.uid for element in db_arguments])


def __select_random(some_list):
    """
    If the input list is to long, a ordered list with random subset is returned as well as a boolean, if the list is to long

    :param some_list: any kind of list
    :return: list, boolean
    """
    return some_list  # TODO 166 currently disabled
    # return some_list[:max_count] # we do not need to shuffle cause we everything is randomized based on the users nick
    # return [some_list[i] for i in sorted(random.sample(range(len(some_list)), max_count))]


def get_attack_for_argument(argument_uid, lang, restriction_on_attacks=None, restriction_on_args=None,
                            last_attack=None, history=None, redirected_from_jump=False):
    """
    Selects an attack out of the web of reasons.

    :param argument_uid: Argument.uid
    :param lang: ui_locales
    :param restriction_on_attacks: Array of Attacks or None
    :param restriction_on_args: Argument.uid
    :param last_attack: String
    :param history: History
    :param redirected_from_jump: Boolean
    :return: Argument.uid, String, Boolean if no new attacks are found
    """
    if not restriction_on_args:
        restriction_on_args = []
        restriction_on_args = list(set(restriction_on_args))

    if history and not redirected_from_jump:
        history = history.split('-')
        index = -2 if len(history) > 1 else -1
        redirected_from_jump = 'jump' in history[index] or redirected_from_jump
    else:
        history = str(history)

    # COMMA16 Special Case (forbid: undercuts of undercuts)
    # one URL for testing: /discuss/cat-or-dog/reaction/12/undercut/13?history=/attitude/2-/justify/2/t
    if not restriction_on_attacks:
        restriction_on_attacks = []

    is_current_arg_undercut = DBDiscussionSession.query(Argument).get(argument_uid).argument_uid is not None
    if is_current_arg_undercut and not redirected_from_jump:
        restriction_on_attacks.append(Attacks.UNDERCUT)

    logger('RecommenderSystem', 'get_attack_for_argument',
           'arg: {}, reststricts: {}, {}, from_jump: {}'.format(argument_uid, restriction_on_attacks,
                                                                restriction_on_args, redirected_from_jump))

    attacks_array, key, no_new_attacks = __get_attack_for_argument(argument_uid, lang, restriction_on_attacks,
                                                                   restriction_on_args, last_attack, history)

    if not attacks_array or len(attacks_array) == 0:
        end = 'end'
        if no_new_attacks:
            end += '_attack'
        return 0, end

    else:
        attack_no = random.randrange(0, len(attacks_array))  # Todo fix random
        attack_uid = attacks_array[attack_no]['id']

        logger('RecommenderSystem', 'get_attack_for_argument', 'main return {} by {}'.format(key, attack_uid))

        return attack_uid, attack_mapping[key]


def get_argument_by_conclusion(statement_uid, is_supportive):
    """
    Returns a random argument by its conclusion

    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :return: Argument
    """
    logger('RecommenderSystem', 'get_argument_by_conclusion', 'statement: {}, supportive: {}'.format(statement_uid, is_supportive))
    db_arguments = get_arguments_by_conclusion(statement_uid, is_supportive)

    if len(db_arguments) == 0:
        return 0
    rnd = random.randint(0, len(db_arguments) - 1)  # TODO fix random
    return db_arguments[0 if len(db_arguments) == 1 else rnd].uid


def get_arguments_by_conclusion(statement_uid, is_supportive):
    """
    Returns all arguments by their conclusion

    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :return: [Argument]
    """
    logger('RecommenderSystem', 'get_arguments_by_conclusion', 'statement: {}, supportive: {}'.format(statement_uid, is_supportive))
    db_arguments = get_not_disabled_arguments_as_query()
    db_arguments = db_arguments.filter(and_(Argument.is_supportive == is_supportive,
                                            Argument.conclusion_uid == statement_uid)).all()
    if not db_arguments:
        return []

    logger('RecommenderSystem', 'get_argument_by_conclusion', 'found ' + str(len(db_arguments)) + ' arguments')
    # TODO sort arguments and return a subset

    return db_arguments


def get_forbidden_attacks_based_on_history(history):
    """
    Returns all attacking uids from reaction steps of the history string

    :param history: String - history of the user
    :return: list of uids
    """
    tmp = []
    for split in history.split('-'):
        if 'reaction' in split and len(split.split('/')) > 4:
            tmp.append(split.split('/')[4])

    tmp = list(set(tmp))

    forbidden_uids = []
    for uid in tmp:
        try:
            forbidden_uids.append(int(uid))
        except ValueError:
            logger('RecommenderSystem', 'get_forbidden_attacks_based_on_history', 'malicious attack in history {}'.format(uid))
    return forbidden_uids


def __get_attack_for_argument(argument_uid, lang, restriction_on_attacks, restriction_on_args, last_attack, history):
    """
    Returns a dictionary with attacks. The attack itself is random out of the set of attacks, which were not done yet.
    Additionally returns id's of premises groups with [key + str(index) + 'id']

    :param argument_uid: Argument.uid
    :param lang: ui_locales
    :param restriction_on_attacks: String
    :param restriction_on_args: Argument.uid
    :param last_attack: String
    :param history: History
    :return: [Argument.uid], String, Boolean if no new attacks are found
    """
    complete_list_of_attacks = [attack for attack in Attacks]
    attacks = [attack for attack in Attacks]

    logger('RecommenderSystem', '__get_attack_for_argument', 'attack_list: {}'.format(attacks))
    attack_list = complete_list_of_attacks if len(attacks) == 0 else attacks
    return_array, key, no_new_attacks = __get_attack_for_argument_by_random_in_range(argument_uid, attack_list,
                                                                                     complete_list_of_attacks,
                                                                                     lang, restriction_on_attacks,
                                                                                     restriction_on_args,
                                                                                     last_attack, history)

    # sanity check if we could not found an attack for a left attack in out set
    if not return_array and len(attacks) > 0:
        return_array, key, no_new_attacks = __get_attack_for_argument_by_random_in_range(argument_uid, [],
                                                                                         complete_list_of_attacks,
                                                                                         lang, restriction_on_attacks,
                                                                                         restriction_on_args,
                                                                                         last_attack,
                                                                                         history)

    return return_array, key, no_new_attacks


def __get_attack_for_argument_by_random_in_range(argument_uid, attack_list, list_of_all_attacks, lang,
                                                 restriction_on_attacks, restriction_on_args, last_attack,
                                                 history):
    """

    :param argument_uid: Argument.uid
    :param attack_list:
    :param list_of_all_attacks:
    :param lang: ui_locales
    :param restriction_on_attacks: String
    :param restriction_on_args: Argument.uid
    :param last_attack: String
    :param history: History
    :return: [Argument.uid], String, Boolean if no new attacks are found
    """
    return_array = None
    key = ''
    left_attacks = list(set(list_of_all_attacks) - set(attack_list))
    attack_found = False
    is_supportive = False
    new_attack_step = ''

    # randomize at least 1, maximal 3 times for getting an attack or
    # if the attack type and the only attacking argument are the same as the restriction
    while len(attack_list) > 0:
        attack = random.choice(attack_list)
        attack_list.remove(attack)

        return_array, is_supportive, key = __get_attacks(attack, argument_uid, last_attack, is_supportive)

        if not return_array or len(return_array) == 0:
            continue

        # check if the step is already in history
        new_attack_step = '{}/{}/{}'.format(argument_uid, attack_mapping[key], return_array[0]['id'])

        # kick all malicious steps
        real_return_array = [item for item in return_array if item['id'] not in restriction_on_args and '/{}'.format(str(item['id'])) not in str(history)]
        return_array = real_return_array

        if key not in restriction_on_attacks \
                and len(return_array) > 0\
                and return_array[0]['id'] not in restriction_on_args \
                and new_attack_step not in history:  # no duplicated attacks
            attack_found = True
            break

        key = ''
        return_array = []

    if not attack_found and len(left_attacks) > 0:
        return_array, key, is_attack_in_history = __get_attack_for_argument_by_random_in_range(argument_uid,
                                                                                               left_attacks,
                                                                                               left_attacks, lang,
                                                                                               restriction_on_attacks,
                                                                                               restriction_on_args,
                                                                                               last_attack, history)

    return return_array, key, new_attack_step in history


def __get_attacks(attack, argument_uid, last_attack, is_supportive):
    key = attack

    if attack == Attacks.UNDERMINE:
        attacks = get_undermines_for_argument_uid(argument_uid, is_supportive)
        # special case when undermining an undermine (docs/dbas/logic.html?highlight=undermine#dialog-sequence)
        is_supportive = last_attack == 'undermine'

    elif attack == Attacks.REBUT:
        tmp_arg = DBDiscussionSession.query(Argument).get(argument_uid)
        if not (tmp_arg and tmp_arg.argument_uid is None):
            key = Attacks.UNDERCUT
        attacks = get_rebuts_for_argument_uid(argument_uid)

    else:
        attacks = get_undercuts_for_argument_uid(argument_uid)

    return attacks, is_supportive, key


def __get_best_argument(argument_list):
    """

    :param argument_list: Argument[]
    :return: Argument
    """
    logger('RecommenderSystem', '__get_best_argument', 'main')
    evaluations = []
    for argument in argument_list:
        evaluations.append(__evaluate_argument(argument.uid))

    best = max(evaluations)
    index = [i for i, j in enumerate(evaluations) if j == best]
    return index[0]


def __evaluate_argument(argument_uid):
    """

    :param argument_uid: Argument.uid Argument.uid
    :return:
    """
    logger('RecommenderSystem', '__evaluate_argument', 'argument {}'.format(argument_uid))

    db_votes = DBDiscussionSession.query(ClickedArgument).filter_by(argument_uid=argument_uid)
    db_valid_votes = db_votes.filter(is_valid=True)
    db_valid_upvotes = db_valid_votes.filter(is_up_vote=True)

    votes = len(db_votes.all())
    valid_votes = len(db_valid_votes.all())
    valid_upvotes = len(db_valid_upvotes.all())
    all_users = len(DBDiscussionSession.query(User).all())

    if valid_votes == 0:
        valid_votes = 1

    if all_users == 0:
        all_users = 1

    index_up_vs_down = valid_upvotes / valid_votes
    index_participation = votes / all_users

    return index_participation, index_up_vs_down
