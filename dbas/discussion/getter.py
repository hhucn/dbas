import json

from dbas import user_management as user_manager
from dbas.lib import get_all_arguments_with_text_and_url_by_statement_id, get_slug_by_statement_uid
from dbas.handler.opinion import get_infos_about_argument, get_user_with_same_opinion_for_argument, \
    get_user_with_same_opinion_for_statements, get_user_with_opinions_for_attitude, \
    get_user_with_same_opinion_for_premisegroups, get_user_and_opinions_for_argument
from dbas.helper.language import get_language_from_cookie
from dbas.helper.references import get_references_for_argument, get_references_for_statements
from dbas.input_validator import is_integer
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager

from pyshorteners.shorteners import Shortener, Shorteners
from requests.exceptions import ReadTimeout


def shortened_url(url, nickname, ui_locales) -> dict:
    """
    Shortens the url via external service.

    :param url: Url as string, which should be shortened
    :param nickname: current users nickname
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: dictionary with the url, services name and the url of the service or an error
    """
    user_manager.update_last_action(nickname)

    try:
        service = Shorteners.TINYURL
        service_url = 'http://tinyurl.com/'
        shortener = Shortener(service)
        short_url = format(shortener.short(url))
    except ReadTimeout as e:
        logger('getter', 'get_shortened_url', repr(e), error=True)
        _tn = Translator(ui_locales)
        prepared_dict = {'error': _tn.get(_.serviceNotAvailable)}
        return prepared_dict

    prepared_dict = dict()
    prepared_dict['url'] = short_url
    prepared_dict['service'] = service
    prepared_dict['service_url'] = service_url
    prepared_dict['error'] = ''

    return prepared_dict


def all_infos_about_argument(uid, application_url, nickname, ui_locales) -> dict:
    """
    Returns bunch of information about the given argument

    :param uid: ID of the argument
    :param application_url: url of the application
    :param nickname: current users nickname
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: dictionary with many information or an error
    """

    _t = Translator(ui_locales)

    if not is_integer(uid):
        prepared_dict = {'error': _t.get(_.internalError)}
    else:
        prepared_dict = get_infos_about_argument(uid, application_url, nickname, _t)
        prepared_dict['error'] = ''

    return prepared_dict


def users_with_same_opinion(uids, application_url, path, nickname, is_arg, is_att, is_rea, is_pos, ui_locales) -> dict:
    """
    Based on current discussion step information about other users will be given

    :param uids: IDs of statements or argument for the information request
    :param application_url: url of the application
    :param path: current path of the user
    :param nickname: users nickname
    :param is_arg: boolean, if the request is for an argument
    :param is_att: boolean, if the request is during the attitude step
    :param is_rea: boolean, if the request is during the attitude step
    :param is_pos: boolean, if the request is for a position
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: prepared collection with information about other users with the same opinion or an error
    """
    prepared_dict = dict()
    _tn = Translator(ui_locales)

    if is_arg and is_rea:
        uids = json.loads(uids)
        prepared_dict = get_user_and_opinions_for_argument(uids, nickname, ui_locales, application_url, path)
    elif is_arg and not is_rea:
        prepared_dict = get_user_with_same_opinion_for_argument(uids, nickname, ui_locales, application_url)
    elif is_pos:
        uids = json.loads(uids)
        uids = uids if isinstance(uids, list) else [uids]
        prepared_dict = get_user_with_same_opinion_for_statements(uids, True, nickname, ui_locales, application_url)
    elif is_att:
            prepared_dict = get_user_with_opinions_for_attitude(uids, nickname, ui_locales, application_url)
    elif not is_att:
        uids = json.loads(uids)
        uids = uids if isinstance(uids, list) else [uids]
        prepared_dict = get_user_with_same_opinion_for_premisegroups(uids, nickname, ui_locales, application_url)
    prepared_dict['info'] = _tn.get(_.otherParticipantsDontHaveOpinionForThisStatement) if len(uids) == 0 else ''
    prepared_dict['error'] = ''

    return prepared_dict


def arguments_by_statement_uid(uid, application_url, ui_locales) -> dict:
    """
    Collects every argument which uses the given statement

    :param uid: ID of statement to request all arguments
    :param application_url: url of the application
    :param ui_locales: language of the discussion
    :rtype: dict
    :return: prepared collection with several arguments
    """
    if not is_integer(uid):
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError)}

    slug = get_slug_by_statement_uid(uid)
    _um = UrlManager(application_url, slug)
    prepared_dict = dict()
    prepared_dict['arguments'] = get_all_arguments_with_text_and_url_by_statement_id(uid, _um, True, is_jump=True)
    prepared_dict['error'] = ''

    return prepared_dict


def references(uids, is_argument, application_url) -> dict:
    """
    Returns references for an argument or statement.

    :param uids: IDs of statements or arguments as list
    :param is_argument: boolean if the ids are for arguments
    :param application_url: url of the application
    :rtype: dict
    :return: prepared collection with error, data and text field
    """
    if is_argument:
        data, text = get_references_for_argument(uids, application_url)
    else:
        data, text = get_references_for_statements(uids, application_url)

    prepared_dict = {
        'error': '',
        'data': data,
        'text': text
    }

    return prepared_dict
