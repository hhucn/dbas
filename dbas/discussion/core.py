from typing import Union

import dbas.handler.issue as issue_helper
from dbas.database.discussion_model import Argument, User, Issue, Statement
from dbas.handler import user
from dbas.handler.voting import add_click_for_argument
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.views import handle_justification_statement, handle_justification_dontknow, \
    handle_justification_argument
from dbas.input_validator import is_integer, check_belonging_of_argument, check_belonging_of_premisegroups, \
    related_with_support
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_arguments_as_query
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_argument_click
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def init(db_issue: Issue, db_user: User) -> dict:
    """
    Initialize the discussion. Creates helper and returns a dictionary containing the first elements needed for the
    discussion.

    :param db_issue: Issue
    :param db_user: User
    :return: prepared collection with first elements for the discussion
    """
    logger('Core', 'main')
    slug = db_issue.slug

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname=db_user.nickname, slug=slug)

    item_dict = ItemDictHelper(disc_ui_locales, db_issue).get_array_for_start(db_user)
    discussion_dict = _ddh.get_dict_for_start(position_count=(len(item_dict['elements'])))

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def attitude(db_issue: Issue, db_user: User, db_position: Statement, history: str, path: str) -> dict:
    """
    Initialize the attitude step for a position in a discussion. Creates helper and returns a dictionary containing
    the first elements needed for the discussion.

    :param db_issue: Issue
    :param db_user: User
    :param db_position: Statement with is_position == True
    :param history: Current history
    :param path:
    :return: prepared collection dict for the discussion
    :rtype: dict
    """
    logger('Core', 'attitude')

    position_uid = db_position.uid

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = db_issue.lang

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, slug=db_issue.slug)
    discussion_dict = _ddh.get_dict_for_attitude(db_position)

    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)
    item_dict = _idh.prepare_item_dict_for_attitude(position_uid)

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def justify_statement(db_issue: Issue, db_user: User, db_statement: Statement, attitude: str, history, path) -> \
        Union[dict, None]:
    """
    Initialize the justification step for a statement or an argument in a discussion. Creates helper and
    returns a dictionary containing the necessary elements needed for the discussion.

    :param db_issue:
    :param db_user:
    :param db_statement:
    :param attitude:
    :param history:
    :param path:
    :return:
    """
    logger('Justify discussion', 'main')

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    if attitude in ['agree', 'disagree']:
        item_dict, discussion_dict = handle_justification_statement(db_issue, db_user, db_statement, attitude,
                                                                    history, path)
    else:
        item_dict, discussion_dict = handle_justification_dontknow(db_issue, db_user, db_statement, attitude,
                                                                   history, path)

    if not all([item_dict, discussion_dict]):
        return None

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def justify_argument(db_issue: Issue, db_user: User, db_argument: Argument, attitude: str, relation: str, history: str,
                     path: str) -> Union[dict, None]:
    """
    Initialize the justification step for a statement or an argument in a discussion. Creates helper and
    returns a dictionary containing the necessary elements needed for the discussion.

    :param db_issue:
    :param db_user:
    :param db_argument:
    :param attitude:
    :param relation:
    :param history:
    :param path:
    :return:
    """
    logger('Justify discussion', 'main')

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    item_dict, discussion_dict = handle_justification_argument(db_issue, db_user, db_argument, attitude, relation,
                                                               history, path)
    if not all([item_dict, discussion_dict]):
        return None

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def reaction(db_issue: Issue, db_user: User, db_arg_user: Argument, db_arg_sys: Argument, relation: str, history,
             path) -> dict:
    """
    Initialize the reaction step for a position in a discussion. Creates helper and returns a dictionary containing
    different feedback options for the confrontation with an argument in a discussion.

    :param db_issue:
    :param db_user:
    :param db_arg_user:
    :param db_arg_sys:
    :param relation:
    :param history:
    :param path:
    :return:
    """
    logger('Core', 'Entering discussion.reaction')

    arg_id_user = db_arg_user.uid
    arg_id_sys = db_arg_sys.uid

    # set votes and reputation
    add_rep, broke_limit = add_reputation_for(db_user, reason=rep_reason_first_argument_click)
    add_click_for_argument(db_arg_user, db_user)

    supportive = db_arg_user.is_supportive
    _ddh = DiscussionDictHelper(db_issue.lang, db_user.nickname, history, slug=db_issue.slug, broke_limit=broke_limit)
    _idh = ItemDictHelper(db_issue.lang, db_issue, path=path, history=history)
    discussion_dict = _ddh.get_dict_for_argumentation(arg_id_user, supportive, arg_id_sys, relation, history, db_user)
    item_dict = _idh.get_array_for_reaction(arg_id_sys, arg_id_user, supportive, relation, discussion_dict['gender'])

    return {
        'issues': issue_helper.prepare_json_of_issue(db_issue, db_user),
        'discussion': discussion_dict,
        'items': item_dict,
        'title': db_issue.title
    }


def support(request_dict: dict) -> Union[dict, None]:
    """
    Initialize the support step for the end of a branch in a discussion. Creates helper and returns a dictionary
    containing the first elements needed for the discussion.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'main')

    db_issue = request_dict['issue']
    history = request_dict['history']
    db_user = request_dict['user']
    slug = db_issue.slug
    arg_user_uid = request_dict.get('arg_user_uid', request_dict['matchdict'].get('arg_id_user', ''))
    arg_system_uid = request_dict.get('arg_system_uid', request_dict['matchdict'].get('arg_id_sys', ''))

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    if not check_belonging_of_argument(db_issue.uid, arg_user_uid) or \
            not check_belonging_of_argument(db_issue.uid, arg_system_uid) or \
            not related_with_support(arg_user_uid, arg_system_uid):
        logger('Core', 'no item dict', error=True)
        return None

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, history, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=request_dict['path'], history=history)
    discussion_dict = _ddh.get_dict_for_supporting_each_other(arg_system_uid, arg_user_uid, db_user.nickname)
    item_dict = _idh.get_array_for_support(arg_system_uid, slug)

    prepared_discussion = {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }

    return prepared_discussion


def choose(request_dict: dict) -> Union[dict, None]:
    """
    Initialize the choose step for more than one premise in a discussion. Creates helper and returns a dictionary
    containing several feedback options regarding this argument.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'main')

    is_argument = request_dict['matchdict'].get('is_argument', '')
    is_supportive = request_dict['matchdict'].get('supportive', '')
    uid = request_dict['matchdict'].get('id', '')
    pgroup_ids = request_dict['matchdict'].get('pgroup_ids', '')

    db_issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    history = request_dict['history']
    db_user = request_dict['user']
    slug = db_issue.slug

    is_argument = True if isinstance(is_argument, bool) and is_argument or is_argument == 'true' else False
    is_supportive = True if isinstance(is_supportive, bool) and is_supportive or is_supportive == 'true' else False

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    for pgroup in pgroup_ids:
        if not is_integer(pgroup):
            logger('core', 'integer error', error=True)
            return None

    if not check_belonging_of_premisegroups(db_issue.uid, pgroup_ids) or not is_integer(uid):
        logger('core', 'wrong belonging of pgroup', error=True)
        return None

    _ddh = DiscussionDictHelper(ui_locales, db_user.nickname, history, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=request_dict['path'], history=history)
    discussion_dict = _ddh.get_dict_for_choosing(uid, is_argument, is_supportive)
    item_dict = _idh.get_array_for_choosing(uid, pgroup_ids, is_argument, is_supportive, db_user.nickname)

    if not item_dict:
        logger('discussion_choose', 'no item dict', error=True)
        return None

    prepared_discussion = {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }

    return prepared_discussion


def jump(request_dict: dict) -> Union[dict, None]:
    """
    Initialize the jump step for an argument in a discussion. Creates helper and returns a dictionary containing
    several feedback options regarding this argument.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :rtype: dict
    :return: prepared collection matchdict for the discussion
    """
    logger('Core', 'main')

    arg_uid = request_dict.get('arg_uid', request_dict['matchdict'].get('arg_id'))
    db_issue = request_dict.get('issue')
    history = request_dict.get('history')
    db_user = request_dict['user']
    slug = db_issue.slug

    if not check_belonging_of_argument(db_issue.uid, arg_uid):
        logger('Core', 'no item dict', error=True)
        return None

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, history, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=request_dict['path'], history=history)
    discussion_dict = _ddh.get_dict_for_jump(arg_uid)
    item_dict = _idh.get_array_for_jump(arg_uid, slug)

    prepared_discussion = {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }

    return prepared_discussion


def finish(request_dict: dict) -> Union[dict, None]:
    logger('Core', 'main')

    db_issue = request_dict['issue']
    history = request_dict['history']
    slug = db_issue.slug
    db_user = request_dict['user']

    # get parameters
    arg_id = request_dict['matchdict'].get('arg_id')
    last_arg = get_not_disabled_arguments_as_query().filter_by(uid=arg_id).first()
    if not last_arg:
        logger('Core', 'no argument', error=True)
        return None

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, history, slug=slug)
    discussion_dict = _ddh.get_dict_for_argumentation(arg_id, last_arg.is_supportive, None, None, history, db_user)
    item_dict = ItemDictHelper.get_empty_dict()

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def dexit(ui_locales: str, db_user: User) -> Union[dict, None]:
    """
    Exit the discussion. Creates helper and returns a dictionary containing the summary of today.

    :param ui_locales:
    :param db_user:
    :rtype: dict
    :return: prepared collection with summary of current day's actions of the user
    """
    return {
        'title': Translator(ui_locales).get(_.finishTitle),
        'summary': user.get_summary_of_today(db_user)
    }
