import dbas.helper.history as HistoryHelper
import dbas.helper.issue as IssueHelper
import dbas.user_management as UserHandler
import transaction

from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry

from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import Validator
from dbas.lib import get_language, get_discussion_language
from dbas.logger import logger
from dbas.url_manager import UrlManager


def get_nickname_and_session(request, for_api=None, api_data=None):
    """
    Given data from api, return nickname and session_id.

    :param for_api:
    :param api_data:
    :return:
    """
    nickname = api_data["nickname"] if api_data and for_api else request.authenticated_userid
    session_id = api_data["session_id"] if api_data and for_api else request.session.id
    return nickname, session_id


def preperation_for_view(for_api, api_data, request):
    """
    Does some elementary things like: getting nickname, sessioniod and history. Additionally boolean, if the sesseion is expired

    :param for_api: True, if the values are for the api
    :param api_data: Array with api data
    :param request: Current request
    :return: nickname, session_id, session_expired, history
    """
    nickname, session_id = get_nickname_and_session(request, for_api, api_data)
    session_expired = UserHandler.update_last_action(transaction, nickname)
    history         = request.params['history'] if 'history' in request.params else ''
    HistoryHelper.save_path_in_database(nickname, request.path, transaction)
    HistoryHelper.save_history_in_cookie(request, request.path, history)
    return nickname, session_id, session_expired, history


def main_function_for_jump(request, for_api, api_data, is_decision, mainpage, base_layout, project_name, user_logout):
    """

    :param request:
    :param for_api:
    :param api_data:
    :param is_decision:
    :param mainpage:
    :param base_layout:
    :param project_name:
    :param user_logout:
    :return:
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    matchdict = request.matchdict
    params = request.params
    logger('__main_function_for_jump', 'def', 'main, self.request.matchdict: ' + str(matchdict))
    logger('__main_function_for_jump', 'def', 'main, self.request.params: ' + str(params))

    nickname, session_id = get_nickname_and_session(request, for_api, api_data)
    history = params['history'] if 'history' in params else ''

    if for_api and api_data:
        slug = api_data["slug"]
        arg_uid = api_data["arg_uid"]
    else:
        slug = matchdict['slug'] if 'slug' in matchdict else ''
        arg_uid = matchdict['arg_id'] if 'arg_id' in matchdict else ''

    session_expired = UserHandler.update_last_action(transaction, nickname)
    HistoryHelper.save_path_in_database(nickname, request.path, transaction)
    HistoryHelper.save_history_in_cookie(request, request.path, history)
    if session_expired:
        return user_logout(True)

    ui_locales = get_language(request, get_current_registry())
    issue = IssueHelper.get_id_of_slug(slug, request, True) if len(slug) > 0 else IssueHelper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, for_api)

    if not Validator.check_belonging_of_argument(issue, arg_uid):
        return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]]))

    _ddh = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, mainpage, for_api, path=request.path, history=history)
    if is_decision:
        discussion_dict = _ddh.get_dict_for_jump_decision(arg_uid)
        item_dict = _idh.get_array_for_jump_decision(arg_uid, slug, for_api)
    else:
        discussion_dict = _ddh.get_dict_for_jump(arg_uid)
        item_dict = _idh.get_array_for_jump(arg_uid, slug, for_api)
    extras_dict = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, False, True,
                                                                                    True, True, nickname,
                                                                                    application_url=mainpage,
                                                                                    for_api=for_api,
                                                                                    request=request)

    return_dict = dict()
    return_dict['issues'] = issue_dict
    return_dict['discussion'] = discussion_dict
    return_dict['items'] = item_dict
    return_dict['extras'] = extras_dict

    if for_api:
        return return_dict
    else:
        return_dict['layout'] = base_layout
        return_dict['language'] = str(ui_locales)
        return_dict['title'] = issue_dict['title']
        return_dict['project'] = project_name
        return return_dict
