from time import sleep

import logging
from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from dbas.auth.login import __refresh_headers_and_url
from dbas.auth.oauth import facebook
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Group
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

PROVIDER = {"facebook": facebook}


@view_config(route_name='oauth_start', renderer='json')
def oauth_start(request: Request) -> dict:
    service = request.json_body.get("service")
    redirect_uri = request.json_body["redirect_uri"]
    return PROVIDER[service].start_flow(request, redirect_uri)


@view_config(route_name='oauth', renderer='json')
def oauth_endpoint(request: Request):
    service = request.matchdict.get("service")
    ui_local = get_language_from_cookie(request)
    log = logging.getLogger(__name__)
    log.debug("%s", service)

    data, next_url = PROVIDER[service].continue_flow(request)
    oauth_user = set_oauth_user(data, service, ui_local)["user"]

    headers, url = __refresh_headers_and_url(request, oauth_user, False, next_url)
    sleep(0.5)
    return HTTPFound(location=url, headers=headers)


def set_oauth_user(user_data, service, ui_locales):
    """

    :param user_data:
    :param service:
    :param ui_locales:
    :return:
    """
    _tn = Translator(ui_locales)

    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()
    log = logging.getLogger(__name__)
    if not db_group:
        log.debug("Error occured: No db_group for users during `set_oauth_user`")
        return {'error': _tn.get(_.errorTryLateOrContant)}

    ret_dict = user.set_new_oauth_user(user_data, user_data['id'], service, _tn)

    return {
        'status': ret_dict['success'] if ret_dict['success'] else ret_dict['error'],
        'error': ret_dict.get('error', ''),
        'user': ret_dict.get('user')
    }
