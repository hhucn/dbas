import dbas.handler.issue as issue_helper
from dbas.database.discussion_model import Argument, User, Issue, Statement, PremiseGroup
from dbas.handler import user
from dbas.handler.voting import add_click_for_argument
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.views import handle_justification_statement, handle_justification_dontknow, \
    handle_justification_argument
from dbas.lib import Attitudes, Relations
from dbas.logger import logger
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


def justify_statement(db_issue: Issue, db_user: User, db_statement: Statement, attitude: str, history, path) -> dict:
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
    if attitude in [Attitudes.AGREE, Attitudes.DISAGREE]:
        item_dict, discussion_dict = handle_justification_statement(db_issue, db_user, db_statement, attitude,
                                                                    history, path)
    else:
        item_dict, discussion_dict = handle_justification_dontknow(db_issue, db_user, db_statement, attitude,
                                                                   history, path)

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def justify_argument(db_issue: Issue, db_user: User, db_argument: Argument, attitude: str, relation: str, history: str,
                     path: str) -> dict:
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

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def reaction(db_issue: Issue, db_user: User, db_arg_user: Argument, db_arg_sys: Argument, relation: Relations, history,
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
    # set votes and reputation
    add_rep, broke_limit = add_reputation_for(db_user, reason=rep_reason_first_argument_click)
    add_click_for_argument(db_arg_user, db_user)

    _ddh = DiscussionDictHelper(db_issue.lang, db_user.nickname, history, slug=db_issue.slug, broke_limit=broke_limit)
    _idh = ItemDictHelper(db_issue.lang, db_issue, path=path, history=history)
    discussion_dict = _ddh.get_dict_for_argumentation(db_arg_user, db_arg_sys.uid, relation, history, db_user)
    item_dict = _idh.get_array_for_reaction(db_arg_sys.uid, db_arg_user.uid, db_arg_user.is_supportive, relation,
                                            discussion_dict['gender'])

    return {
        'issues': issue_helper.prepare_json_of_issue(db_issue, db_user),
        'discussion': discussion_dict,
        'items': item_dict,
        'title': db_issue.title
    }


def support(db_issue: Issue, db_user: User, db_arg_user: Argument, db_arg_sys: Argument, history: str,
            path: str) -> dict:
    """
    Initialize the support step for the end of a branch in a discussion. Creates helper and returns a dictionary
    containing the first elements needed for the discussion.

    :param db_issue:
    :param db_user:
    :param db_arg_user:
    :param db_arg_sys:
    :param history:
    :param path:
    :return:
    """
    logger('Core', 'Entering discussion.support')
    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, history, slug=db_issue.slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)
    discussion_dict = _ddh.get_dict_for_supporting_each_other(db_arg_sys.uid, db_arg_user.uid, db_user.nickname)
    item_dict = _idh.get_array_for_support(db_arg_sys.uid, db_issue.slug)

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def choose(db_issue: Issue, db_user: User, is_argument: bool, is_supportive: bool, pgroup: PremiseGroup, pgroup_ids: list,
           history: str, path: str) -> dict:
    """
    Initialize the choose step for more than one premise in a discussion. Creates helper and returns a dictionary
    containing several feedback options regarding this argument.

    :param db_issue:
    :param db_user:
    :param is_argument:
    :param is_supportive:
    :param uid:
    :param pgroup:
    :param history:
    :param path:
    :return:
    """
    logger('Core', 'Entering discussion.choose')
    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, history, slug=db_issue.slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)
    discussion_dict = _ddh.get_dict_for_choosing(pgroup.uid, is_argument, is_supportive)
    item_dict = _idh.get_array_for_choosing(pgroup.uid, pgroup_ids, is_argument, is_supportive, db_user.nickname)

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def jump(db_issue: Issue, db_user: User, db_argument: Argument, history: str, path: str) -> dict:
    """
    Initialize the jump step for an argument in a discussion. Creates helper and returns a dictionary containing
    several feedback options regarding this argument.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :rtype: dict
    :return: prepared collection matchdict for the discussion
    """
    logger('Core', 'Entering discussion.jzmp')

    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, db_user.nickname, history, slug=db_issue.slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)
    discussion_dict = _ddh.get_dict_for_jump(db_argument.uid)
    item_dict = _idh.get_array_for_jump(db_argument.uid, db_issue.slug)

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def finish(db_issue: Issue, db_user: User, db_argument: Argument, history: str) -> dict:
    issue_dict = issue_helper.prepare_json_of_issue(db_issue, db_user)

    _ddh = DiscussionDictHelper(db_issue.lang, db_user.nickname, history, slug=db_issue.slug)
    discussion_dict = _ddh.get_dict_for_argumentation(db_argument, None, None, history, db_user)
    item_dict = ItemDictHelper.get_empty_dict()

    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'title': issue_dict['title']
    }


def dexit(ui_locales: str, db_user: User) -> dict:
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
