import dbas.handler.issue as issue_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
from dbas.handler import user
from dbas.handler.voting import add_click_for_argument
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.views import handle_justification_step
from dbas.input_validator import is_integer, is_statement_forbidden, check_belonging_of_statement, \
    check_belonging_of_argument, check_belonging_of_premisegroups, related_with_support, check_reaction, \
    check_belonging_of_arguments
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_arguments_as_query
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_argument_click
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def init(request_dict, for_api=False) -> dict:
    """
    Initialize the discussion. Creates helper and returns a dictionary containing the first elements needed for the
    discussion.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection with first elements for the discussion
    """
    logger('Core', 'discussion.init', 'main')

    matchdict = request_dict['matchdict']
    application_url = request_dict['app_url']

    count_of_slugs = 1
    if 'slug' in matchdict and isinstance(matchdict['slug'], ()):
        count_of_slugs = len(matchdict['slug'])

    if count_of_slugs > 1:
        logger('Core', 'discussion.init', 'to many slugs', error=True)
        return None

    nickname = request_dict['nickname']
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']
    item_dict = ItemDictHelper(disc_ui_locales, issue, application_url, for_api).get_array_for_start(nickname)

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname=nickname, main_page=application_url, slug=request_dict['slug'])
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    discussion_dict = _ddh.get_dict_for_start(position_count=(len(item_dict['elements'])))
    extras_dict = _dh.prepare_extras_dict(request_dict['slug'], False, True, True, request_dict['registry'],
                                          request_dict['app_url'], request_dict['path'],
                                          for_api=for_api, nickname=nickname)

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


def attitude(request_dict, for_api=False) -> dict:
    """
    Initialize the attitude step for a position in a discussion. Creates helper and returns a dictionary containing
    the first elements needed for the discussion.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection matchdict for the discussion
    """
    logger('Core', 'discussion.attitude', 'main')

    nickname = request_dict['nickname']
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    slug = request_dict['slug']
    application_url = request_dict['app_url']
    history = request_dict['history']
    statement_id = request_dict['matchdict']['statement_id'][0] if 'statement_id' in request_dict['matchdict'] else ''

    if not is_integer(statement_id, True) \
            or not check_belonging_of_statement(issue, statement_id):
        logger('Core', 'discussion.attitude', 'param error', error=True)
        return None

    if is_statement_forbidden(statement_id):
        logger('Core', 'discussion.attitude', 'forbidden statement', error=True)
        return None

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    discussion_dict = _ddh.get_dict_for_attitude(statement_id)
    if not discussion_dict:
        logger('Core', 'discussion.attitude', 'no discussion dict', error=True)
        return None

    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request_dict['path'], history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    item_dict = _idh.prepare_item_dict_for_attitude(statement_id)
    extras_dict = _dh.prepare_extras_dict(issue_dict['slug'], False, True, True, request_dict['registry'],
                                          request_dict['app_url'], request_dict['path'], for_api=for_api,
                                          nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def justify(request_dict, for_api=False) -> dict:
    """
    Initialize the justification step for a statement or an argument in a discussion. Creates helper and
    returns a dictionary containing the necessary elements needed for the discussion.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.justify', 'main')

    nickname = request_dict['nickname']
    issue = request_dict['issue']
    application_url = request_dict['app_url']

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)

    item_dict, discussion_dict, extras_dict = handle_justification_step(request_dict, for_api)
    if item_dict is None or discussion_dict is None or extras_dict is None:
        return None

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def reaction(request_dict, for_api=False) -> dict:
    """
    Initialize the reaction step for a position in a discussion. Creates helper and returns a dictionary containing
    different feedback options for the confrontation with an argument in a discussion.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection matchdict for the discussion
    """
    logger('Core', 'discussion.reaction', 'main')

    nickname = request_dict['nickname']
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    slug = request_dict['slug']
    application_url = request_dict['app_url']
    history = request_dict['history']

    # get parameters
    arg_id_user = request_dict['matchdict'].get('arg_id_user')
    attack = request_dict['matchdict'].get('mode')
    arg_id_sys = request_dict['matchdict'].get('arg_id_sys')
    tmp_argument = DBDiscussionSession.query(Argument).get(arg_id_user)

    if not check_reaction(arg_id_user, arg_id_sys, attack) or not check_belonging_of_arguments(issue, [arg_id_user, arg_id_sys]):
        logger('discussion_reaction', 'def', 'wrong belonging of arguments', error=True)
        return None

    # set votes and reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_argument_click)
    add_click_for_argument(arg_id_user, nickname)

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']

    supportive = tmp_argument.is_supportive
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request_dict['path'], history=history)
    discussion_dict = _ddh.get_dict_for_argumentation(arg_id_user, supportive, arg_id_sys, attack, history, nickname)
    item_dict = _idh.get_array_for_reaction(arg_id_sys, arg_id_user, supportive, attack, discussion_dict['gender'])
    extras_dict = _dh.prepare_extras_dict(slug, True, True, True, request_dict['registry'], request_dict['app_url'],
                                          request_dict['path'], for_api=for_api, nickname=nickname,
                                          broke_limit=broke_limit)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def support(request_dict, for_api=False, api_data=None) -> dict:
    """
    Initialize the support step for the end of a branch in a discussion. Creates helper and returns a dictionary
    containing the first elements needed for the discussion.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.support', 'main')

    nickname = request_dict['nickname']
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    history = request_dict['history']

    if for_api and api_data:
        slug = api_data['slug']
        arg_user_uid = api_data['arg_user_uid']
        arg_system_uid = api_data['arg_system_uid']
    else:
        slug = request_dict.get('slug', '')
        arg_user_uid = request_dict['matchdict'].get('arg_id_user', '')
        arg_system_uid = request_dict['matchdict'].get('arg_id_sys', '')

    application_url = request_dict['app_url']
    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']

    if not check_belonging_of_argument(issue, arg_user_uid) or \
            not check_belonging_of_argument(issue, arg_system_uid) or \
            not related_with_support(arg_user_uid, arg_system_uid):
        logger('Core', 'discussion.support', 'no item dict', error=True)
        return None

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request_dict['path'], history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    discussion_dict = _ddh.get_dict_for_supporting_each_other(arg_system_uid, arg_user_uid, nickname, application_url)
    item_dict = _idh.get_array_for_support(arg_system_uid, slug, for_api)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, request_dict['registry'], request_dict['app_url'],
                                          request_dict['path'], for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def choose(request_dict, for_api=False) -> dict:
    """
    Initialize the choose step for more than one premise in a discussion. Creates helper and returns a dictionary
    containing several feedback options regarding this argument.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection matchdictfor the discussion
    """
    logger('Core', 'discussion.choose', 'main')

    is_argument = request_dict['matchdict'].get('is_argument', '')
    is_supportive = request_dict['matchdict'].get('supportive', '')
    uid = request_dict['matchdict'].get('id', '')
    pgroup_ids = request_dict['matchdict'].get('pgroup_ids', '')

    nickname = request_dict['nickname']
    issue = request_dict['issue']
    ui_locales = request_dict['ui_locales']
    slug = request_dict['slug']
    application_url = request_dict['app_url']
    history = request_dict['history']

    is_argument = True if is_argument is 't' else False
    is_supportive = True if is_supportive is 't' else False

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']

    for pgroup in pgroup_ids:
        if not is_integer(pgroup):
            logger('core', 'discussion.choose', 'integer error', error=True)
            return None

    if not check_belonging_of_premisegroups(issue, pgroup_ids) or not is_integer(uid):
        logger('core', 'discussion.choose', 'wrong belonging of pgroup', error=True)
        return None

    _ddh = DiscussionDictHelper(ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request_dict['path'], history=history)
    discussion_dict = _ddh.get_dict_for_choosing(uid, is_argument, is_supportive)
    item_dict = _idh.get_array_for_choosing(uid, pgroup_ids, is_argument, is_supportive, nickname)

    if not item_dict:
        logger('discussion_choose', 'def', 'no item dict', error=True)
        return None

    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    extras_dict = _dh.prepare_extras_dict(slug, False, True, True, request_dict['registry'], request_dict['app_url'],
                                          request_dict['path'], for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def jump(request_dict, for_api=False, api_data=None) -> dict:
    """
    Initialize the jump step for an argument in a discussion. Creates helper and returns a dictionary containing
    several feedback options regarding this argument.

    :param request_dict: dict out of pyramid's request object including issue, slug and history and more
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: prepared collection matchdict for the discussion
    """
    logger('Core', 'discussion.jump', 'main')

    tmp_dict = request_dict
    if for_api and api_data:
        slug = api_data.get('slug')
        arg_uid = api_data.get('arg_uid')
        tmp_dict = api_data
    else:
        slug = request_dict['matchdict'].get('slug')
        arg_uid = request_dict['matchdict'].get('arg_id')

    nickname = tmp_dict.get('nickname')
    issue = tmp_dict.get('issue')
    ui_locales = tmp_dict.get('ui_locales', 'en')
    history = tmp_dict.get('history')
    application_url = tmp_dict.get('app_url')

    if not check_belonging_of_argument(issue, arg_uid) or not issue and not slug and not arg_uid:
        logger('Core', 'discussion.choose', 'no item dict', error=True)
        return None

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']

    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    _idh = ItemDictHelper(disc_ui_locales, issue, application_url, for_api, path=request_dict['path'], history=history)
    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    discussion_dict = _ddh.get_dict_for_jump(arg_uid)
    item_dict = _idh.get_array_for_jump(arg_uid, slug, for_api)
    extras_dict = _dh.prepare_extras_dict(slug, True, True, True, request_dict['registry'], request_dict['app_url'],
                                          request_dict['path'], for_api=for_api, nickname=nickname)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion


def finish(request_dict, for_api=False) -> dict:
    logger('Core', 'discussion_finish', 'main')

    nickname = request_dict['nickname']
    ui_locales = request_dict['ui_locales']
    application_url = request_dict['app_url']
    issue = request_dict['issue']
    slug = request_dict['slug']
    history = request_dict['history']

    # get parameters
    arg_id = request_dict['matchdict'].get('arg_id')
    if not arg_id:
        logger('Core', 'discussion_finish', 'no argument', error=True)
        return None

    last_arg = get_not_disabled_arguments_as_query().filter_by(uid=arg_id).first()
    if not last_arg:
        logger('Core', 'discussion_finish', 'no argument', error=True)
        return None

    issue_dict = issue_helper.prepare_json_of_issue(issue, application_url, for_api, nickname)
    disc_ui_locales = issue_dict['lang']

    _dh = DictionaryHelper(ui_locales, disc_ui_locales)
    _ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=application_url, slug=slug)
    discussion_dict = _ddh.get_dict_for_argumentation(arg_id, last_arg.is_supportive, None, 'end_attack', history, nickname)
    item_dict = ItemDictHelper.get_empty_dict()
    extras_dict = _dh.prepare_extras_dict(slug, True, True, True, request_dict['registry'], request_dict['app_url'],
                                          request_dict['path'], for_api=for_api, nickname=nickname)
    return {
        'issues': issue_dict,
        'discussion': discussion_dict,
        'items': item_dict,
        'extras': extras_dict,
        'title': issue_dict['title']
    }


def dexit(request_dict) -> dict:
    """
    Exit the discussion. Creates helper and returns a dictionary containing the summary of today.

    :param request_dict: dict with registry, appurl, nickname, path and ui_locales of pyramid's request object
    :rtype: dict
    :return: prepared collection with summary of current day's actions of the user
    """
    _t = Translator(request_dict['ui_locales'])

    extras_dict = DictionaryHelper(request_dict['ui_locales']).prepare_extras_dict_for_normal_page(
        request_dict['registry'], request_dict['app_url'], request_dict['path'], request_dict['nickname'])
    summary_dict = user.get_summary_of_today(request_dict['nickname'], request_dict['ui_locales'])

    prepared_discussion = dict()
    prepared_discussion['title'] = _t.get(_.finishTitle)
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['summary'] = summary_dict
    return prepared_discussion
