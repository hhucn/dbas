import dbas.helper.history as history_helper
import dbas.helper.issue as issue_helper
import dbas.user_management as user_manager
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.language import get_language_from_cookie, set_language_for_first_visit
from dbas.input_validator import is_integer, is_statement_forbidden, check_belonging_of_statement,\
    check_belonging_of_argument
from dbas.logger import logger
from dbas.lib import get_discussion_language, resolve_issue_uid_to_slug
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _

# TODO: FIX API / CONSIDER API_DATA
# TODO: REQUEST AND NICKNAME AS PARAMS?


def init(request, nickname, for_api=False) -> dict:
    """
    Initialize the discussion. Creates helper and returns a dictionary containing the first elements needed for the
    discussion. 
    
    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection with first elements for the discussion
    """
    match_dict = request.matchdict
    set_language_for_first_visit(request)

    count_of_slugs = 1
    if 'slug' in match_dict and isinstance(match_dict['slug'], ()):
        count_of_slugs = len(match_dict['slug'])

    if count_of_slugs > 1:
        logger('Core', 'discussion.init', 'to many slugs', error=True)
        raise None

    if for_api:
        slug = match_dict['slug'] if 'slug' in match_dict else ''
    else:
        slug = match_dict['slug'][0] if 'slug' in match_dict and len(match_dict['slug']) > 0 else ''

    last_topic = history_helper.get_saved_issue(nickname)
    if len(slug) == 0 and last_topic != 0:
        issue = last_topic
    else:
        issue = issue_helper.get_id_of_slug(slug, request, True)

    slug = resolve_issue_uid_to_slug(last_topic)
    if not slug:
        slug = ''
    __handle_history(request, nickname, slug, issue)

    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, for_api)
    item_dict = ItemDictHelper(disc_ui_locales, issue, request.application_url, for_api).get_array_for_start(nickname)

    discussion_dict = DiscussionDictHelper(disc_ui_locales, nickname=nickname, main_page=request.application_url, slug=slug).get_dict_for_start(position_count=(len(item_dict['elements'])))
    extras_dict = DictionaryHelper(get_language_from_cookie(request), disc_ui_locales).prepare_extras_dict(slug, False, True, False, True,
                                                                                                           request, for_api=for_api, nickname=nickname)

    if len(item_dict['elements']) == 1:
        DictionaryHelper(disc_ui_locales, disc_ui_locales).add_discussion_end_text(discussion_dict, extras_dict,
                                                                                   nickname, at_start=True)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def attitude(request, nickname, for_api=False) -> dict:
    """
    Initialize the attitude step for a position in a discussion. Creates helper and returns a dictionary containing
    the first elements needed for the discussion.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection with first elements for the discussion
    """
    ui_locales = get_language_from_cookie(request)
    statement_id = request.matchdict['statement_id'][0] if 'statement_id' in request.matchdict else ''
    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    issue = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)

    if not is_integer(statement_id, True) \
            or not check_belonging_of_statement(issue, statement_id):
        logger('Core', 'discussion.attitude', 'param error', error=True)
        raise None

    if is_statement_forbidden(statement_id):
        logger('Core', 'discussion.attitude', 'forbidden statement', error=True)
        raise None

    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, for_api)
    history = __handle_history(request, nickname, slug, issue)

    discussion_dict = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=request.application_url, slug=slug)\
        .get_dict_for_attitude(statement_id)
    if not discussion_dict:
        logger('Core', 'discussion.attitude', 'no discussion dict', error=True)
        return None

    item_dict = ItemDictHelper(disc_ui_locales, issue, request.application_url, for_api, path=request.path, history=history)\
        .prepare_item_dict_for_attitude(statement_id)
    extras_dict = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(issue_dict['slug'], False, True,
                                                                                    False, True, request,
                                                                                    for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def reaction(request, nickname, history, for_api=False) -> dict:
    prepared_discussion = dict()
    return prepared_discussion


def support(request, nickname, history, for_api=False) -> dict:
    prepared_discussion = dict()
    return prepared_discussion


def choose(request, nickname, history, for_api=False) -> dict:
    prepared_discussion = dict()
    return prepared_discussion


def jump(request, nickname, for_api=False, api_data=None) -> dict:
    """
    Initialize the jump step for an argument in a discussion. Creates helper and returns a dictionary containing
    several feedback options regarding this argument.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection with first elements for the discussion
    """

    ui_locales = get_language_from_cookie(request)
    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''

    issue = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, for_api)
    history = __handle_history(request, nickname, slug, issue)

    if for_api and api_data:
        slug = api_data["slug"]
        arg_uid = api_data["arg_uid"]
    else:
        slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
        arg_uid = request.matchdict['arg_id'] if 'arg_id' in request.matchdict else ''

    if not check_belonging_of_argument(issue, arg_uid):
        logger('Core', 'discussion.choose', 'no item dict', error=True)
        return None

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=request.application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, request.application_url, for_api, path=request.path, history=history)
    discussion_dict = _ddh.get_dict_for_jump(arg_uid, nickname, history)
    item_dict = _idh.get_array_for_jump(arg_uid, slug, for_api)
    extras_dict = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, True,
                                                                                    True, True, request,
                                                                                    for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def finish(request) -> dict:
    """
    Exit the discussion. Creates helper and returns a dictionary containing the summary of today.

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with summary of current day's actions of the user
    """
    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)
    summary_dict = user_manager.get_summary_of_today(request.authenticated_userid, ui_locales)

    prepared_discussion = dict()
    prepared_discussion['title'] = _t.get(_.finishTitle)
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['summary'] = summary_dict
    return prepared_discussion


def __handle_history(request, nickname, slug, issue) -> str:
    """

    :param request:
    :param nickname:
    :param slug:
    :param issue:
    :rtype: str
    :return:
    """
    history = request.params['history'] if 'history' in request.params else ''
    history_helper.save_path_in_database(nickname, slug, request.path, history)
    history_helper.save_history_in_cookie(request, request.path, history)
    history_helper.save_issue_uid(issue, nickname)#
    return history