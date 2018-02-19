"""
Helper for D-BAS Views

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import dbas.handler.voting as voting_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.handler import user
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import is_integer, check_belonging_of_argument, check_belonging_of_statement
from dbas.lib import get_text_for_statement_uid, nick_of_anonymous_user
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for
from dbas.review.helper.reputation import rep_reason_first_confrontation
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio


def get_nickname(request_authenticated_userid, for_api=None, api_data=None):
    """
    Given data from api, return nickname and session_id.

    :param request_authenticated_userid:
    :param for_api: Boolean
    :param api_data:
    :return:
    """
    nickname = api_data.get("nickname") if api_data and for_api else request_authenticated_userid
    return nickname


def preparation_for_view(for_api, api_data, request):
    """
    Does some elementary things like: getting nickname, session id and history.
    Additionally boolean, if the session is expired

    :param for_api: True, if the values are for the api
    :param api_data: Array with api data
    :param request: Current request
    :return: nickname, session_id, session_expired, history
    """
    nickname = get_nickname(request.authenticated_userid, for_api, api_data)
    session_expired = user.update_last_action(nickname)
    return nickname, session_expired


def handle_justification_step(request_dict, for_api):
    """
    Handles the justification step
    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: Boolean
    :return: dict(), dict(), dict()
    """
    matchdict = request_dict['matchdict']
    statement_or_arg_id = matchdict.get('statement_or_arg_id')
    mode = matchdict.get('mode', '')
    relation = matchdict['relation'][0] if len(matchdict['relation']) > 0 else ''

    if not is_integer(statement_or_arg_id, True):
        return None, None, None

    if [c for c in ('t', 'f') if c in mode] and relation == '':
        item_dict, discussion_dict, extras_dict = __handle_justification_statement(request_dict, for_api,
                                                                                   statement_or_arg_id, mode)

    elif 'd' in mode and relation == '':
        item_dict, discussion_dict, extras_dict = __handle_justification_dont_know(request_dict, for_api,
                                                                                   statement_or_arg_id, mode)

    elif [c for c in ('undermine', 'rebut', 'undercut', 'support') if c in relation]:
        item_dict, discussion_dict, extras_dict = __handle_justification_argument(request_dict, for_api,
                                                                                  statement_or_arg_id, relation, mode)

    else:
        logger('ViewHelper', 'handle_justification_step', '404')
        return None, None, None

    return item_dict, discussion_dict, extras_dict


def __handle_justification_statement(request_dict, for_api, statement_or_arg_id, mode):
    """

    :param request_dict:
    :param for_api:
    :param statement_or_arg_id:
    :param mode:
    :return:
    """
    logger('ViewHelper', 'handle_justification_step', 'justify statement')
    issue = request_dict['issue']
    supportive = mode == 't' or mode == 'd'  # supportive = t or do not know mode

    if not get_text_for_statement_uid(statement_or_arg_id) or not check_belonging_of_statement(issue,
                                                                                               statement_or_arg_id):
        return None, None, None
    item_dict, discussion_dict, extras_dict = preparation_for_justify_statement(request_dict, for_api,
                                                                                statement_or_arg_id, supportive)
    return item_dict, discussion_dict, extras_dict


def __handle_justification_dont_know(request_dict, for_api, statement_or_arg_id, mode):
    """

    :param request_dict:
    :param for_api:
    :param statement_or_arg_id:
    :param mode:
    :return:
    """
    logger('ViewHelper', '__handle_justification_dont_know', 'do not know for {}'.format(statement_or_arg_id))
    issue = request_dict['issue']
    supportive = mode == 't' or mode == 'd'  # supportive = t or do not know mode

    if int(statement_or_arg_id) != 0 and \
            not check_belonging_of_argument(issue, statement_or_arg_id) and \
            not check_belonging_of_statement(issue, statement_or_arg_id):
        return None, None, None
    item_dict, discussion_dict, extras_dict = preparation_for_dont_know_statement(request_dict, for_api,
                                                                                  statement_or_arg_id, supportive)
    return item_dict, discussion_dict, extras_dict


def __handle_justification_argument(request_dict, for_api, statement_or_arg_id, relation, mode):
    """

    :param request_dict:
    :param for_api:
    :param statement_or_arg_id:
    :param relation:
    :param mode:
    :return:
    """
    logger('ViewHelper', '__handle_justification_argument', 'justify argument')
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    nickname = request_dict['nickname']
    main_page = request_dict['app_url']
    port = request_dict['port']
    supportive = mode == 't' or mode == 'd'  # supportive = t or do not know mode

    if not check_belonging_of_argument(issue, statement_or_arg_id):
        return None, None, None
    item_dict, discussion_dict, extras_dict = preparation_for_justify_argument(request_dict, for_api,
                                                                               statement_or_arg_id, supportive,
                                                                               relation)
    # add reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_confrontation)
    # send message if the user is now able to review
    if broke_limit:
        _t = Translator(ui_locales)
        send_request_for_info_popup_to_socketio(nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                main_page + '/review')
    return item_dict, discussion_dict, extras_dict


def preparation_for_justify_statement(request_dict, for_api, statement_uid, supportive):
    """
    Prepares some paramater for the justification step for an statement

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: Boolean
    :param statement_uid: Statement.uid
    :param supportive: Boolean
    :return: dict(), dict(), dict()
    """
    logger('ViewHelper', 'preparation_for_justify_statement', 'main')

    slug = request_dict['slug']
    ui_locales = request_dict['ui_locales']
    history = request_dict['history']
    nickname = request_dict['nickname']
    app_url = request_dict['app_url']
    registry = request_dict['registry']
    path = request_dict['path']
    issue = request_dict['issue']
    db_user = request_dict['user']

    logged_in = db_user and db_user.nickname != nick_of_anonymous_user

    disc_ui_locales = DBDiscussionSession.query(Issue).get(issue).lang
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=app_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, app_url, for_api, path=path, history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)

    voting_helper.add_click_for_statement(statement_uid, nickname, supportive)

    item_dict = _idh.get_array_for_justify_statement(statement_uid, db_user, supportive, history)
    discussion_dict = _ddh.get_dict_for_justify_statement(statement_uid, app_url, slug, supportive,
                                                          len(item_dict['elements']), db_user)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, registry, app_url, path, db_user, for_api=for_api)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0 or len(item_dict['elements']) == 1 and logged_in:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify=True,
                                    current_premise=get_text_for_statement_uid(statement_uid),
                                    supportive=supportive)
    return item_dict, discussion_dict, extras_dict


def preparation_for_dont_know_statement(request_dict, for_api, argument_uid, supportive):
    """
    Prepares some parameter for the "don't know" step

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: Boolean
    :param argument_uid: Argument.uid
    :param supportive: Boolean
    :return: dict(), dict(), dict()
    """
    logger('ViewHelper', 'preparation_for_dont_know_statement', 'main')

    slug = request_dict['slug']
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    history = request_dict['history']
    nickname = request_dict['nickname']
    app_url = request_dict['app_url']
    registry = request_dict['registry']
    path = request_dict['path']
    db_user = request_dict['user']

    disc_ui_locales = DBDiscussionSession.query(Issue).get(issue).lang
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=app_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, app_url, for_api, path=path, history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)

    discussion_dict = _ddh.get_dict_for_dont_know_reaction(argument_uid, app_url, nickname)
    item_dict = _idh.get_array_for_dont_know_reaction(argument_uid, supportive, db_user, discussion_dict['gender'])
    extras_dict = _dh.prepare_extras_dict(slug, True, True, True, registry, app_url, path, for_api=for_api,
                                          db_user=db_user)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0:
        if int(argument_uid) == 0:
            argument_uid = history.split('/')[-1]
            if not is_integer(argument_uid):
                argument_uid = 0

        text = ''
        if int(argument_uid) != 0:
            text = get_text_for_statement_uid(argument_uid)

        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_dont_know=True, current_premise=text)
    return item_dict, discussion_dict, extras_dict


def preparation_for_justify_argument(request_dict, for_api, statement_or_arg_id, supportive, relation):
    """
    Prepares some paramater for the justification step for an argument

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: Boolean
    :param statement_or_arg_id: Argument.uid / Statement.uid
    :param supportive: Boolean
    :param relation: String
    :return: dict(), dict(), dict()
    """
    logger('ViewHelper', 'preparation_for_justify_argument', 'main')

    slug = request_dict['slug']
    ui_locales = request_dict['ui_locales']
    history = request_dict['history']
    nickname = request_dict['nickname']
    app_url = request_dict['app_url']
    registry = request_dict['registry']
    path = request_dict['path']
    issue = request_dict['issue']
    db_user = request_dict['user']
    logged_in = db_user and db_user.nickname != nick_of_anonymous_user is not None

    disc_ui_locales = DBDiscussionSession.query(Issue).get(issue).lang
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=app_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, app_url, for_api, path=path, history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)

    # justifying argument
    # is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
    item_dict = _idh.get_array_for_justify_argument(statement_or_arg_id, relation, logged_in, db_user, history)
    discussion_dict = _ddh.get_dict_for_justify_argument(statement_or_arg_id, supportive, relation)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, False, registry, app_url, path, for_api=for_api,
                                          db_user=db_user)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0 or len(item_dict['elements']) == 1 and logged_in:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify_argumentation=True)

    return item_dict, discussion_dict, extras_dict
