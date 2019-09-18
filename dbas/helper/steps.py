"""
Helper for D-BAS Views
"""
import logging
from typing import Tuple, Union

import dbas.handler.voting as voting_helper
from dbas.database.discussion_model import Statement, Issue, User, Argument
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.lib import Attitudes
from dbas.review.reputation import ReputationReasons, add_reputation_and_check_review_access
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio

LOG = logging.getLogger(__name__)


def handle_justification_statement(db_issue: Issue, db_user: User, db_stmt_or_arg: Statement, attitude: str, history,
                                   path):
    """

    :param db_issue:
    :param db_user:
    :param db_stmt_or_arg:
    :param attitude:
    :param history:
    :param path:
    :return:
    """
    LOG.debug("Justify statement")
    supportive = attitude in [Attitudes.AGREE, Attitudes.DONT_KNOW]
    item_dict, discussion_dict = preparation_for_justify_statement(history, db_user, path, db_issue, db_stmt_or_arg,
                                                                   supportive)
    return item_dict, discussion_dict


def handle_justification_dontknow(db_issue: Issue, db_user: User, db_stmt_or_arg: Union[Argument, Statement], history,
                                  path) -> Tuple[dict, dict]:
    """

    :param db_issue: Current issue
    :param db_user: User
    :param db_stmt_or_arg: Statement
    :param history:
    :param path:
    :return:
    """
    LOG.debug("Do not know for %s", db_stmt_or_arg.uid)
    item_dict, discussion_dict = __preparation_for_dont_know_statement(db_issue, db_user, db_stmt_or_arg, history, path)
    return item_dict, discussion_dict


def handle_justification_argument(db_issue: Issue, db_user: User, db_argument: Argument, attitude: str,
                                  relation: str, history, path) -> Tuple[dict, dict]:
    """

    :param db_issue:
    :param db_user:
    :param db_argument:
    :param attitude:
    :param relation:
    :param history:
    :param path:
    :return:
    """
    LOG.debug("Justify argument")
    ui_locales = db_issue.lang
    nickname = db_user.nickname
    supportive = attitude in [Attitudes.AGREE, Attitudes.DONT_KNOW]

    item_dict, discussion_dict = preparation_for_justify_argument(db_issue, db_user, db_argument, relation,
                                                                  supportive, history, path)

    broke_limit = add_reputation_and_check_review_access(db_user, ReputationReasons.first_confrontation)

    if broke_limit:
        _t = Translator(ui_locales)
        send_request_for_info_popup_to_socketio(nickname, _t.get(_.youAreAbleToReviewNow), '/review')
    return item_dict, discussion_dict


def preparation_for_justify_statement(history, db_user: User, path, db_issue: Issue, db_statement: Statement,
                                      supportive: bool):
    """
    Prepares some parameter for the justification step for an statement.

    :param history: history
    :param db_user: User
    :param path:
    :param db_statement: Statement
    :param db_issue: Issue
    :param supportive: Boolean
    :return: dict(), dict(), dict()
    """
    LOG.debug("Entering preparation_for_justify_statement")
    nickname = db_user.nickname
    slug = db_issue.slug

    disc_ui_locales = db_issue.lang
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)

    voting_helper.add_click_for_statement(db_statement, db_user, supportive)

    item_dict = _idh.get_array_for_justify_statement(db_statement, db_user, supportive, history)
    discussion_dict = _ddh.get_dict_for_justify_statement(db_statement, slug, supportive,
                                                          len(item_dict['elements']), db_user)
    return item_dict, discussion_dict


def __preparation_for_dont_know_statement(db_issue: Issue, db_user: User, db_stmt_or_arg: Statement, history, path) -> \
        Tuple[dict, dict]:
    """
    Prepares some parameter for the "don't know" step

    :param db_issue: Current issue
    :param db_user: User
    :param db_stmt_or_arg: Statement
    :param history:
    :param path: request.path
    :return: dict(), dict(), dict()
    """
    LOG.debug("Entering __preparation_for_dont_know_statement")
    nickname = db_user.nickname
    slug = db_issue.slug

    disc_ui_locales = db_issue.lang
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)

    discussion_dict = _ddh.get_dict_for_dont_know_reaction(db_stmt_or_arg.uid, nickname)
    item_dict = _idh.get_array_for_dont_know_reaction(db_stmt_or_arg.uid, db_user, discussion_dict['gender'])
    return item_dict, discussion_dict


def preparation_for_justify_argument(db_issue: Issue, db_user: User, db_argument: Argument, relation: str,
                                     supportive: bool, history, path):
    """
    Prepares some parameter for the justification step for an argument

    :param db_issue:
    :param db_user:
    :param db_argument:
    :param relation:
    :param supportive:
    :param history:
    :param path:
    :return:
    """
    LOG.debug("Entering preparation_for_justify_argument")
    nickname = db_user.nickname
    slug = db_issue.slug

    disc_ui_locales = db_issue.lang
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, db_issue, path=path, history=history)

    # justifying argument
    item_dict = _idh.get_array_for_justify_argument(db_argument.uid, relation, db_user, history)
    discussion_dict = _ddh.get_dict_for_justify_argument(db_argument.uid, supportive, relation)

    return item_dict, discussion_dict
