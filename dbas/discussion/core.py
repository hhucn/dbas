from pyramid.httpexceptions import HTTPNotFound

import dbas.handler.history as history_helper
import dbas.handler.issue as issue_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie, set_language_for_first_visit
from dbas.handler.voting import add_click_for_argument
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.views import handle_justification_step
from dbas.input_validator import is_integer, is_statement_forbidden, check_belonging_of_statement, \
    check_belonging_of_argument, check_belonging_of_premisegroups, related_with_support, check_reaction
from dbas.lib import get_discussion_language, resolve_issue_uid_to_slug
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_argument_click
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


# TODO: REQUEST AND NICKNAME AS PARAMS? (LETS KILL REQUESTS)


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
    logger('Core', 'discussion.init', 'main')

    matchdict = request.matchdict
    set_language_for_first_visit(request)
    application_url = request.application_url

    count_of_slugs = 1
    if 'slug' in matchdict and isinstance(matchdict['slug'], ()):
        count_of_slugs = len(matchdict['slug'])

    if count_of_slugs > 1:
        logger('Core', 'discussion.init', 'to many slugs', error=True)
        raise None

    if for_api:
        slug = matchdict['slug'] if 'slug' in matchdict else ''
    else:
        slug = matchdict['slug'][0] if 'slug' in matchdict and len(matchdict['slug']) > 0 else ''

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
    logger('X', 'X', str(disc_ui_locales))
    logger('X', 'X', str(disc_ui_locales))
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)
    item_dict = ItemDictHelper(disc_ui_locales, issue, application_url, for_api).get_array_for_start(nickname)

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname=nickname, main_page=application_url, slug=slug)
    _dh = DictionaryHelper(get_language_from_cookie(request), disc_ui_locales)
    discussion_dict = _ddh.get_dict_for_start(position_count=(len(item_dict['elements'])))
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, request, for_api=for_api, nickname=nickname)

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
    :return: prepared collection matchdict for the discussion
    """

    ui_locales = get_language_from_cookie(request)
    statement_id = request.matchdict['statement_id'][0] if 'statement_id' in request.matchdict else ''
    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    application_url = request.application_url
    if len(slug) > 0:
        issue = issue_helper.get_id_of_slug(slug, request, True)
    else:
        issue = issue_helper.get_issue_id(request)

    if not is_integer(statement_id, True) \
            or not check_belonging_of_statement(issue, statement_id):
        logger('Core', 'discussion.attitude', 'param error', error=True)
        return None

    if is_statement_forbidden(statement_id):
        logger('Core', 'discussion.attitude', 'forbidden statement', error=True)
        return None

    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)
    history = __handle_history(request, nickname, slug, issue)

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    discussion_dict = _ddh.get_dict_for_attitude(statement_id)
    if not discussion_dict:
        logger('Core', 'discussion.attitude', 'no discussion dict', error=True)
        return None

    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request.path, history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    item_dict = _idh.prepare_item_dict_for_attitude(statement_id)
    extras_dict = _dh.prepare_extras_dict(issue_dict['slug'], False, True, True, request, for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def justify(request, nickname, for_api=False) -> dict:
    """
    Initialize the justification step for a statement or an argument in a discussion. Creates helper and
    returns a dictionary containing the necessary elements needed for the discussion.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.justify', 'main')

    ui_locales = get_language_from_cookie(request)
    application_url = request.application_url

    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    if len(slug) > 0:
        issue = issue_helper.get_id_of_slug(slug, request, True)
    else:
        issue = issue_helper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)

    history = __handle_history(request, nickname, slug, issue)

    item_dict, discussion_dict, extras_dict = handle_justification_step(request, for_api, ui_locales, nickname, history)
    if item_dict is None or discussion_dict is None or extras_dict is None:
        return None

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def reaction(request, nickname, for_api=False) -> dict:
    """
    Initialize the reaction step for a position in a discussion. Creates helper and returns a dictionary containing
    different feedback options for the confrontation with an argument in a discussion.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.reaction', 'main')

    # get parameters
    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    arg_id_user = request.matchdict['arg_id_user'] if 'arg_id_user' in request.matchdict else ''
    attack = request.matchdict['mode'] if 'mode' in request.matchdict else ''
    arg_id_sys = request.matchdict['arg_id_sys'] if 'arg_id_sys' in request.matchdict else ''
    tmp_argument = DBDiscussionSession.query(Argument).get(arg_id_user)
    issue = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)
    application_url = request.application_url

    valid_reaction = check_reaction(arg_id_user, arg_id_sys, attack)
    if not tmp_argument or not valid_reaction\
            or not valid_reaction and not check_belonging_of_argument(issue, arg_id_user)\
            or not valid_reaction and not check_belonging_of_argument(issue, arg_id_sys):
        logger('discussion_reaction', 'def', 'wrong belonging of arguments', error=True)
        raise HTTPNotFound()

    supportive = tmp_argument.is_supportive

    # sanity check
    if not [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid', 'end') if c in attack]:
        logger('core', 'discussion.reaction', 'wrong value in attack', error=True)
        return None
    ui_locales = get_language_from_cookie(request)

    # set votes and reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_argument_click)
    add_click_for_argument(arg_id_user, nickname)

    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)

    history = __handle_history(request, nickname, slug, issue)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request.path, history=history)
    discussion_dict = _ddh.get_dict_for_argumentation(arg_id_user, supportive, arg_id_sys, attack, history, nickname)
    item_dict = _idh.get_array_for_reaction(arg_id_sys, arg_id_user, supportive, attack, discussion_dict['gender'])
    extras_dict = _dh.prepare_extras_dict(slug, True, True, True, request, for_api=for_api, nickname=nickname, broke_limit=broke_limit)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def support(request, nickname, for_api=False, api_data=None) -> dict:
    """
    Initialize the support step for the end of a branch in a discussion. Creates helper and returns a dictionary
    containing the first elements needed for the discussion.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.support', 'main')

    if for_api and api_data:
        slug = api_data['slug']
        arg_user_uid = api_data['arg_user_uid']
        arg_system_uid = api_data['arg_system_uid']
    else:
        slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
        arg_user_uid = request.matchdict['arg_id_user'] if 'arg_id_user' in request.matchdict else ''
        arg_system_uid = request.matchdict['arg_id_sys'] if 'arg_id_sys' in request.matchdict else ''

    application_url = request.application_url
    ui_locales = get_language_from_cookie(request)
    issue = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)

    if not check_belonging_of_argument(issue, arg_user_uid) or \
            not check_belonging_of_argument(issue, arg_system_uid) or \
            not related_with_support(arg_user_uid, arg_system_uid):
        logger('Core', 'discussion.support', 'no item dict', error=True)
        return None

    history = __handle_history(request, nickname, slug, issue)
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request.path, history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    discussion_dict = _ddh.get_dict_for_supporting_each_other(arg_system_uid, arg_user_uid, nickname, application_url)
    item_dict = _idh.get_array_for_support(arg_system_uid, slug, for_api)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, request, for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def choose(request, nickname, for_api=False) -> dict:
    """
    Initialize the choose step for more than one premise in a discussion. Creates helper and returns a dictionary
    containing several feedback options regarding this argument.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.choose', 'main')

    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    is_argument = request.matchdict['is_argument'] if 'is_argument' in request.matchdict else ''
    is_supportive = request.matchdict['supportive'] if 'supportive' in request.matchdict else ''
    uid = request.matchdict['id'] if 'id' in request.matchdict else ''
    pgroup_ids = request.matchdict['pgroup_ids'] if 'id' in request.matchdict else ''
    application_url = request.application_url

    is_argument = True if is_argument is 't' else False
    is_supportive = True if is_supportive is 't' else False

    ui_locales = get_language_from_cookie(request)
    issue = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)

    for pgroup in pgroup_ids:
        if not is_integer(pgroup):
            logger('core', 'discussion.choose', 'integer error', error=True)
            return None

    if not check_belonging_of_premisegroups(issue, pgroup_ids) or not is_integer(uid):
        logger('core', 'discussion.choose', 'wrong belonging of pgroup', error=True)
        return None

    history = __handle_history(request, nickname, slug, issue)
    _ddh = DiscussionDictHelper(ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request.path, history=history)
    discussion_dict = _ddh.get_dict_for_choosing(uid, is_argument, is_supportive)
    item_dict = _idh.get_array_for_choosing(uid, pgroup_ids, is_argument, is_supportive, nickname)

    if not item_dict:
        logger('discussion_choose', 'def', 'no item dict', error=True)
        return None

    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, request, for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def jump(request, nickname, for_api=False, api_data=None) -> dict:
    """
    Initialize the jump step for an argument in a discussion. Creates helper and returns a dictionary containing
    several feedback options regarding this argument.

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: prepared collection matchdict for the discussion
    """
    logger('Core', 'discussion.jump', 'main')

    ui_locales = get_language_from_cookie(request)
    slug = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    application_url = request.application_url

    issue = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, disc_ui_locales, for_api)
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

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request.path, history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    discussion_dict = _ddh.get_dict_for_jump(arg_uid, nickname, history)
    item_dict = _idh.get_array_for_jump(arg_uid, slug, for_api)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, request, for_api=for_api, nickname=nickname)

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
    summary_dict = user.get_summary_of_today(request.authenticated_userid, ui_locales)

    prepared_discussion = dict()
    prepared_discussion['title'] = _t.get(_.finishTitle)
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['summary'] = summary_dict
    return prepared_discussion


def __handle_history(request, nickname, slug, issue) -> str:
    """

    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param slug: the discussion's slugified title
    :param issue: the discussion's issue od
    :rtype: str
    :return: current user's history
    """
    history = request.params['history'] if 'history' in request.params else ''
    history_helper.save_path_in_database(nickname, slug, request.path, history)
    history_helper.save_history_in_cookie(request, request.path, history)
    history_helper.save_issue_uid(issue, nickname)
    return history
