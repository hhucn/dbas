"""
Login Handler for D-BAS

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from time import sleep

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from sqlalchemy import func
from validate_email import validate_email

from dbas.auth.ldap import verify_ldap_user_data
from dbas.auth.recaptcha import validate_recaptcha
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Settings
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie
from dbas.lib import escape_string, get_user_by_case_insensitive_nickname, is_usage_with_ldap, \
    get_user_by_case_insensitive_public_nickname
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def login_user(request, nickname, password, for_api, keep_login, _tn):
    """
    A try to login the user

    :param request: web servers request
    :param nickname: User.nickname
    :param password: String
    :param for_api: Boolean
    :param keep_login: Boolean
    :param _tn: Translator
    :return: dict() or HTTPFound if the user is logged in an it is not the api
    """

    nickname, password, keep_login, url = __get_data(request, nickname, password, keep_login)
    is_ldap = is_usage_with_ldap(request)
    logger('Auth.Login', 'login_user', 'user: {}, api: {}'.format(nickname, for_api))

    db_user = get_user_by_case_insensitive_nickname(nickname)
    if not db_user:  # check if the user exists
        ret_dict = __login_not_existing_user(request, nickname, password, _tn, is_ldap)
        db_user = ret_dict['user']
    else:
        ret_dict = __login_existing_user(request, nickname, password, _tn, is_ldap, db_user)

    if not ret_dict['success']:
        return {'error': ret_dict['error']}  # error

    if for_api:
        logger('Auth.Login', 'login_user', 'return for api: success')
        return {'status': 'success'}  # api
    else:
        headers, url = __refresh_headers_and_url(request, db_user, keep_login, url)
        logger('Auth.Login', 'login_user', 'return success: ' + url)
        sleep(0.5)
        return HTTPFound(location=url, headers=headers)  # success


def __get_data(request, nickname, password, keep_login):
    """
    Read input params for returning nickname and password of the user as well as a boolean if she wants to keep
    the login and an url for forwarding

    :param request: web servers request
    :param nickname: User.nickname
    :param password: String
    :param keep_login: Boolean
    :return: String, String, Boolean, String
    """
    is_ldap = is_usage_with_ldap(request)
    if not nickname and not password:
        nickname = escape_string(request.params['user'])
        password = request.params['password'] if is_ldap else escape_string(request.params['password'])
        keep_login = escape_string(request.params['keep_login'])
        keep_login = True if keep_login == 'true' else False
        url = request.params['url']
    else:
        nickname = escape_string(nickname)
        password = escape_string(password)
        url = ''
    return nickname, password, keep_login, url


def register_with_ajax_data(request):
    """
    Consume the ajax data for an login attempt

    :param request: webserver's request
    :return: Boolean, String, User
    """
    ui_locales = request.params['lang'] if 'lang' in request.params else get_language_from_cookie(request)
    _tn = Translator(ui_locales)
    success = ''
    params  = request.params
    firstname  = escape_string(params['firstname']) if 'firstname' in params else ''
    lastname  = escape_string(params['lastname']) if 'lastname' in params else ''
    nickname  = escape_string(params['nickname']) if 'nickname' in params else ''
    email  = escape_string(params['email']) if 'email' in params else ''
    gender  = escape_string(params['gender']) if 'gender' in params else ''
    password  = escape_string(params['password']) if 'password' in params else ''
    passwordconfirm = escape_string(params['passwordconfirm']) if 'passwordconfirm' in params else ''
    recaptcha  = request.params['g-recaptcha-response'] if 'g-recaptcha-response' in request.params else ''
    is_human, error = validate_recaptcha(recaptcha)
    db_new_user = None

    # database queries mail verification
    db_nick1 = get_user_by_case_insensitive_nickname(nickname)
    db_nick2 = get_user_by_case_insensitive_public_nickname(nickname)
    db_mail = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    is_mail_valid = validate_email(email, check_mx=True)

    # are the password equal?
    if not password == passwordconfirm:
        logger('Auth.Login', 'user_registration', 'Passwords are not equal')
        msg = _tn.get(_.pwdNotEqual)
    # is the nick already taken?
    elif db_nick1 or db_nick2:
        logger('Auth.Login', 'user_registration', 'Nickname \'' + nickname + '\' is taken')
        msg = _tn.get(_.nickIsTaken)
    # is the email already taken?
    elif db_mail:
        logger('Auth.Login', 'user_registration', 'E-Mail \'' + email + '\' is taken')
        msg = _tn.get(_.mailIsTaken)
    # is the email valid?
    elif not is_mail_valid:
        logger('Auth.Login', 'user_registration', 'E-Mail \'' + email + '\' is not valid')
        msg = _tn.get(_.mailNotValid)
    # is anti-spam correct?
    elif not is_human or error:
        logger('Auth.Login', 'user_registration', 'recaptcha error')
        msg = _tn.get(_.maliciousAntiSpam)
    # lets go
    else:

        # getting the authors group
        db_group = DBDiscussionSession.query(Group).filter_by(name="users").first()

        # does the group exists?
        if not db_group:
            msg = _tn.get(_.errorTryLateOrContant)
            logger('Auth.Login', 'user_registration', 'Error occured')
            return success, msg, db_new_user

        ret_dict = user.set_new_user(request, firstname, lastname, nickname, gender, email, password, _tn)
        success = ret_dict['success']
        error = ret_dict['message']
        db_new_user = ret_dict['user']

        if success:
            msg = _tn.get(_.accountWasAdded).format(nickname)
        else:
            msg = error

    return success, msg, db_new_user


def __login_not_existing_user(request, nickname, password, _tn, is_ldap):
    """
    First login of a user who is not registered

    :param request: webservers request
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :param is_ldap: Boolean
    :return: String or None on success
    """
    logger('Auth.Login', '__login_not_existing_user', 'user \'' + nickname + '\' does not exists')

    # if the user does not exists and we are using LDAP, we'll grep the user
    if is_ldap:
        data = __login_user_with_ldap(request, nickname, password, _tn)
        error = data['error']
        db_user = data['user']
        if error is not None:
            return {
                'success': False,
                'error': error,
                'user': db_user
            }

    else:
        success, error, db_user = register_with_ajax_data(request)
        if not success:
            return {
                'success': False,
                'error': error,
                'user': db_user
            }

    return {
        'success': True,
        'error': error,
        'user': db_user
    }


def __login_existing_user(request, nickname, password, _tn, is_ldap, db_user):
    """
    Login of a user who is already registered

    :param request: webservers request
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :param is_ldap: Boolean
    :param db_user: User
    :return: dict
    """
    logger('Auth.Login', '__login_existing_user', 'user \'' + nickname + '\' exists')
    if is_ldap:
        local_login = db_user.validate_password(password)
        # logger('Auth.Login', '__login_user_is_existing', 'password is {}'.format('right' if local_login else 'wrong'))

        # if not local_login:
        error = _tn.get(_.userPasswordNotMatch)
        if not local_login:
            data = verify_ldap_user_data(request.registry.settings, nickname, password, _tn)
            # we jsut need the error field, because the user already exists in out database
            error = data['error']

        if not error and not local_login:
            logger('Auth.Login', '__login_user_is_existing', 'Error ' + error)
            return {
                'success': False,
                'error': error
            }
    else:
        if not db_user.validate_password(password):  # check password
            logger('Auth.Login', '__login_user_is_existing', 'wrong password')
            error = _tn.get(_.userPasswordNotMatch)
            return {
                'success': False,
                'error': error
            }

    return {
        'success': True,
        'error': None
    }


def __login_user_with_ldap(request, nickname, password, _tn):
    """
    Login the user via LDAP

    :param request: webservers request
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :return: String, User
    """
    logger('Auth.Login', '__login_user_with_ldap', nickname)
    data = verify_ldap_user_data(request.registry.settings, nickname, password, _tn)

    if not data['error']:
        return data['error'], ''

    firstname = data['firstname']
    lastname = data['lastname']
    gender = data['gender']
    email = data['email']
    ret_dict = user.set_new_user(request, firstname, lastname, nickname, gender, email, 'NO_PW_BECAUSE_LDAP', _tn)

    if 'success' not in ret_dict:
        error = _tn.get(_.userPasswordNotMatch)
        return {
            'error': error,
            'user': None
        }

    return {
        'error': None,
        'user': ret_dict['user']
    }


def __refresh_headers_and_url(request, db_user, keep_login, url):
    """
    Refreshed headers for the request. Returns a sequence of header tuples (e.g. ``[('Set-Cookie', 'foo=abc')]``)
    on this request's response.

    :param request: webservers request
    :param db_user: User
    :param keep_login: Boolean
    :param url: String
    :return: Headers, String
    """
    logger('Auth.Login', '__refresh_headers_and_url', 'login', 'login successful / keep_login: ' + str(keep_login))
    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    db_settings.should_hold_the_login(keep_login)
    logger('Auth.Login', '__refresh_headers_and_url', 'remembering headers for {}'.format(db_user.nickname))
    headers = remember(request, db_user.nickname)

    # update timestamp
    logger('Auth.Login', '__refresh_headers_and_url', 'update login timestamp')
    db_user.update_last_login()
    db_user.update_last_action()
    transaction.commit()

    ending = ['/?session_expired=true', '/?session_expired=false']
    for e in ending:
        if url.endswith(e):
            url = url[0:-len(e)]

    return headers, url
