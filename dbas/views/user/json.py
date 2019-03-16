import logging
from time import sleep

from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.view import view_config

from dbas.auth.login import login_local_user, register_user_with_json_data, __refresh_headers_and_url
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie
from dbas.handler.notification import read_notifications, delete_notifications, send_users_notification
from dbas.handler.password import request_password
from dbas.handler.settings import set_settings
from dbas.helper.query import set_user_language
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import valid_lang_cookie_fallback
from dbas.validators.core import has_keywords_in_json_path, has_maybe_keywords, validate
from dbas.validators.notifications import valid_notification_title, valid_notification_text, \
    valid_notification_recipient
from dbas.validators.user import valid_user

LOG = logging.getLogger(__name__)


@view_config(request_method='POST', route_name='user_login', renderer='json')
@validate(has_keywords_in_json_path(('user', str), ('password', str), ('keep_login', bool)),
          has_maybe_keywords(('redirect_url', str, '')))
def user_login(request):
    """
    Will login the user by his nickname and password

    :param request: request of the web server
    :return: dict() with error
    """
    LOG.debug("Login user with Nickname and Password")
    lang = get_language_from_cookie(request)
    nickname = request.validated.get('user', '')
    password = request.validated.get('password', '')
    keep_login = request.validated.get('keep_login', '')
    redirect_url = request.validated.get('redirect_url', '')

    login_data = login_local_user(nickname, password, request.mailer, lang)

    if not login_data.get('error'):
        headers, url = __refresh_headers_and_url(request, login_data['user'], keep_login, redirect_url)
        sleep(0.5)
        return HTTPFound(location=url, headers=headers)

    return {'error': Translator(lang).get(_.userPasswordNotMatch)}


@view_config(route_name='user_logout', renderer='json')
def user_logout(request, redirect_to_main=False):
    """
    Will logout the user

    :param request: request of the web server
    :param redirect_to_main: Boolean
    :return: HTTPFound with forgotten headers
    """
    LOG.debug("User: %s, Redirect Overview: %s", request.authenticated_userid, redirect_to_main)
    request.session.invalidate()
    headers = forget(request)
    if redirect_to_main:
        location = request.application_url + 'discuss?session_expired=true',
    elif (request.application_url + '/discuss') in request.path_url:  # redirect to page, where you need no login
        location = request.path_url
    else:
        location = request.application_url + '/discuss'

    return HTTPFound(
        location=location,
        headers=headers
    )


@view_config(route_name='user_delete', renderer='json')
@validate(valid_user)
def user_delete(request):
    """
    Will delete the user

    :param request: request of the web server
    :return: HTTPFound with forgotten headers
    """
    db_user = request.validated['user']
    LOG.debug("Delete user %s", db_user)
    user.delete(db_user)
    request.session.invalidate()
    return HTTPFound(
        location=request.application_url + '/discuss',
        headers=forget(request)
    )


@view_config(route_name='user_registration', renderer='json')
@validate(valid_lang_cookie_fallback,
          has_keywords_in_json_path(('firstname', str), ('lastname', str), ('nickname', str), ('email', str),
                                    ('gender', str), ('password', str),
                                    ('passwordconfirm', str)))
def user_registration(request):
    """
    Registers new user with data given in the ajax request.

    :param request: current request of the server
    :return: dict() with success and message
    """
    LOG.debug("Register new user via AJAX. %s", request.json_body)
    mailer = request.mailer
    lang = request.validated['lang']

    success, info, new_user = register_user_with_json_data(request.validated, lang, mailer)

    return {
        'success': str(success),
        'error': '',
        'info': str(info)
    }


@view_config(route_name='user_password_request', renderer='json')
@validate(valid_lang_cookie_fallback, has_keywords_in_json_path(('email', str)))
def user_password_request(request):
    """
    Sends an email, when the user requests his password

    :param request: current request of the server
    :return: dict() with success and message
    """
    LOG.debug("Send a password request E-Mail. %s", request.json_body)
    _tn = Translator(request.validated['lang'])
    return request_password(request.validated['email'], request.mailer, _tn)


@view_config(route_name='set_user_setting', renderer='json')
@validate(valid_user, has_keywords_in_json_path(('settings_value', bool), ('service', str)))
def set_user_settings(request):
    """
    Sets a specific setting of the user.

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Change a specific user setting. %s", request.json_body)
    _tn = Translator(get_language_from_cookie(request))
    db_user = request.validated['user']
    settings_value = request.validated['settings_value']
    service = request.validated['service']
    return set_settings(request.application_url, db_user, service, settings_value, _tn)


@view_config(route_name='set_user_language', renderer='json')
@validate(valid_user, valid_lang_cookie_fallback)
def set_user_lang(request):
    """
    Specify new UI language for user.

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Set a UI language. %s", request.json_body)
    return set_user_language(request.validated['user'], request.validated.get('lang'))


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################


@view_config(route_name='notifications_read', renderer='json')
@validate(valid_user, has_keywords_in_json_path(('ids', list)))
def set_notifications_read(request):
    """
    Set a notification as read

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Set a notification to read. %s", request.json_body)
    return read_notifications(request.validated['ids'], request.validated['user'])


@view_config(route_name='notifications_delete', renderer='json')
@validate(valid_user, has_keywords_in_json_path(('ids', list)))
def set_notifications_delete(request):
    """
    Request the removal of a notification

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Request a notification to be removed. %s", request.json_body)
    ui_locales = get_language_from_cookie(request)
    return delete_notifications(request.validated['ids'], request.validated['user'], ui_locales,
                                request.application_url)


@view_config(route_name='send_notification', renderer='json')
@validate(valid_user, valid_notification_title, valid_notification_text, valid_notification_recipient)
def send_some_notification(request):
    """
    Set a new message into the inbox of an recipient, and the outbox of the sender.

    :param request: current request of the server
    :return: dict()
    """
    LOG.debug("Send a notification. %s", request.json_body)
    ui_locales = get_language_from_cookie(request)
    author = request.validated['user']
    recipient = request.validated['recipient']
    title = request.validated['title']
    text = request.validated['text']
    return send_users_notification(author, recipient, title, text, ui_locales)


# ajax - for getting all users with the same opinion
@view_config(route_name='get_public_user_data', renderer='json')
@validate(has_keywords_in_json_path(('user_id', int)))
def get_public_user_data(request):
    """
    Returns dictionary with public user data

    :param request: request of the web server
    :return:
    """
    LOG.debug("Return public user data. %s", request.json_body)
    return user.get_public_data(request.validated['user_id'], get_language_from_cookie(request))
