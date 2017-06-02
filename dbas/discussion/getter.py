import json

from dbas import user_management as user_manager
from dbas.lib import get_all_arguments_with_text_and_url_by_statement_id, get_slug_by_statement_uid,\
    get_discussion_language
from dbas.handler.opinion import get_infos_about_argument, get_user_with_same_opinion_for_argument, \
    get_user_with_same_opinion_for_statements, get_user_with_opinions_for_attitude, \
    get_user_with_same_opinion_for_premisegroups, get_user_and_opinions_for_argument
from dbas.helper.query import get_logfile_for_statements
from dbas.helper.language import  get_language_from_cookie
from dbas.helper.references import get_references_for_argument, get_references_for_statements
from dbas.input_validator import is_integer
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager

from pyshorteners.shorteners import Shortener, Shorteners
from requests.exceptions import ReadTimeout


def logfile_for_some_statements(request) -> dict:
    """
    Collects the complete history/log of statements uid, which is given via request.params.

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with textversions for every statement or error
    """
    ui_locales = get_language_from_cookie(request)
    user_manager.update_last_action(request.authenticated_userid)

    try:
        uids = json.loads(request.params['uids'])
        issue = request.params['issue']
        ui_locales = get_discussion_language(request, issue)
        prepared_dict = get_logfile_for_statements(uids, ui_locales, request.application_url)
        prepared_dict['error'] = ''
    except KeyError as e:
        logger('getter', 'get_logfile_for_statements', repr(e), error=True)
        _tn = Translator(ui_locales)
        prepared_dict = {'error': _tn.get(_.noCorrections)}

    return prepared_dict


def shortened_url(request) -> dict:
    """
    Shortens the url via external service.

    :param request: pyramid's request object
    :rtype: dict
    :return: dictionary with the url, services name and the url of the service or an error
    """
    prepared_dict = dict()
    user_manager.update_last_action(request.authenticated_userid)

    try:
        url = request.params['url']
        service = Shorteners.TINYURL
        service_url = 'http://tinyurl.com/'
        shortener = Shortener(service)

        short_url = format(shortener.short(url))
        prepared_dict['url'] = short_url
        prepared_dict['service'] = service
        prepared_dict['service_url'] = service_url

        prepared_dict['error'] = ''
    except KeyError as e:
        logger('getter', 'get_shortened_url', repr(e), error=True)
        _tn = Translator(get_discussion_language(request))
        prepared_dict['error'] = _tn.get(_.internalKeyError)
    except ReadTimeout as e:
        logger('getter', 'get_shortened_url', repr(e), error=True)
        _tn = Translator(get_discussion_language(request))
        prepared_dict['error'] = _tn.get(_.serviceNotAvailable)

    return prepared_dict


def all_infos_about_argument(request) -> dict:
    """
    Returns bunch of information about the given argument

    :param request: pyramid's request object
    :rtype: dict
    :return: dictionary with many information or an error
    """

    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    try:
        uid = request.params['uid']
        if not is_integer(uid):
            prepared_dict = {'error': _t.get(_.internalError)}
        else:
            prepared_dict = get_infos_about_argument(uid, request.application_url, request.authenticated_userid, _t)
            prepared_dict['error'] = ''
    except KeyError as e:
        logger('getter', 'get_all_infos_about_argument', repr(e), error=True)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return prepared_dict


def users_with_same_opinion(request) -> dict:
    """
    Based on current discussion step information about other users will be given

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with information about other users with the same opinion or an error
    """
    prepared_dict = dict()
    nickname = request.authenticated_userid
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        params = request.params
        ui_locales = params['lang'] if 'lang' in params else 'en'
        uids = params['uids']
        is_arg = params['is_argument'] == 'true' if 'is_argument' in params else False
        is_att = params['is_attitude'] == 'true' if 'is_attitude' in params else False
        is_rea = params['is_reaction'] == 'true' if 'is_reaction' in params else False
        is_pos = params['is_position'] == 'true' if 'is_position' in params else False
    except KeyError as e:
        logger('getter', 'get_users_with_same_opinion', repr(e), error=True)
        prepared_dict['error'] = _tn.get(_.internalKeyError)
        return prepared_dict

    if is_arg and is_rea:
        uids = json.loads(uids)
        prepared_dict = get_user_and_opinions_for_argument(uids, nickname, ui_locales, request.application_url, request.path)
    elif is_arg and not is_rea:
        prepared_dict = get_user_with_same_opinion_for_argument(uids, nickname, ui_locales, request.application_url)
    elif is_pos:
        uids = json.loads(uids)
        uids = uids if isinstance(uids, list) else [uids]
        prepared_dict = get_user_with_same_opinion_for_statements(uids, True, nickname, ui_locales, request.application_url)
    elif is_att:
            prepared_dict = get_user_with_opinions_for_attitude(uids, nickname, ui_locales, request.application_url)
    elif not is_att:
        uids = json.loads(uids)
        uids = uids if isinstance(uids, list) else [uids]
        prepared_dict = get_user_with_same_opinion_for_premisegroups(uids, nickname, ui_locales, request.application_url)
    prepared_dict['info'] = _tn.get(_.otherParticipantsDontHaveOpinionForThisStatement) if len(uids) == 0 else ''
    prepared_dict['error'] = ''

    return prepared_dict


def public_user_data(request) -> dict:
    """
    Returns public information for a specific user.

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with public users data
    """
    prepared_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        nickname = request.params['nickname']
        return_dict = user_manager.get_public_information_data(nickname, ui_locales)
        return_dict['error'] = '' if len(return_dict) != 0 else _tn.get(_.internalKeyError)

    except KeyError as e:
        logger('getter', 'get_public_user_data', repr(e), error=True)
        prepared_dict['error'] = _tn.get(_.internalKeyError)
    return prepared_dict


def arguments_by_statement_uid(request) -> dict:
    """
    Collects every argument which uses the given statement

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with several arguments
    """
    prepared_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        uid = request.matchdict['uid']
        if not is_integer(uid):
            prepared_dict['error'] = _tn.get(_.internalKeyError)
        else:
            slug = get_slug_by_statement_uid(uid)
            _um = UrlManager(request.application_url, slug)
            prepared_dict['arguments'] = get_all_arguments_with_text_and_url_by_statement_id(uid, _um, True, is_jump=True)
            prepared_dict['error'] = ''

    except KeyError as e:
        logger('getter', 'get_arguments_by_statement_uid', repr(e), error=True)
        prepared_dict['error'] = _tn.get(_.internalKeyError)
    return prepared_dict


def references(request) -> dict:
    """
    Returns references for an argument or statement.

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with error, data and text field
    """
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)
    data = ''
    text = ''

    try:
        # uid is an integer if it is an argument and a list otherwise
        uid = json.loads(request.params['uid'])
        is_argument = str(request.params['is_argument']) == 'true'
        are_all_integer = all(is_integer(tmp) for tmp in uid) if isinstance(uid, list) else is_integer(uid)

        error = ''
        if are_all_integer:
            if is_argument:
                data, text = get_references_for_argument(uid, request.application_url)
            else:
                data, text = get_references_for_statements(uid, request.application_url)
        else:
            logger('getter', 'get_references', 'uid is not an integer')
            data = ''
            text = ''
            error = _tn.get(_.internalKeyError)

    except KeyError as e:
        logger('getter', 'get_references', repr(e), error=True)
        error = _tn.get(_.internalKeyError)

    prepared_dict = {
        'error': error,
        'data': data,
        'text': text
    }

    return prepared_dict
