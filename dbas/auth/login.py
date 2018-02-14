"""
Login Handler for D-BAS

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from time import sleep

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid_mailer import Mailer
from sqlalchemy import func
from validate_email import validate_email

from dbas.auth.ldap import verify_ldap_user_data
from dbas.auth.oauth import google as google, github as github, facebook as facebook, twitter as twitter
from dbas.auth.recaptcha import validate_recaptcha
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Settings
from dbas.handler import user
from dbas.handler.password import get_hashed_password
from dbas.lib import escape_string, get_user_by_case_insensitive_nickname, \
    get_user_by_case_insensitive_public_nickname
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _, Keywords
from dbas.strings.translator import Translator

oauth_providers = ['google', 'github', 'facebook', 'twitter']


def login_user(nickname: str, password: str, mailer: Mailer, lang='en') -> dict:
    """
    Try to login the user whereby she is maybe a HHU-LDAP user or known locally.

    :param nickname: User.nickname
    :param password: String
    :param mailer: request.mailer
    :param lang: current language
    :return: dict() or HTTPFound if the user is logged in and it is not the api
    """
    logger('Auth.Login', 'login_user', 'user: {}'.format(nickname))
    _tn = Translator(lang)

    # now we have several options:
    # 1. the user is unknown in our DB, maybe has HHU-LDAP account
    # 2. oauth nickname
    # 3. the user is known, but
    #  a) kept local
    #  b) kept in ldap
    db_user = get_user_by_case_insensitive_nickname(nickname)
    if not db_user:  # this is 1.
        return __register_user_with_ldap_data(mailer, nickname, password, _tn)

    # this is 2.
    if len(str(db_user.oauth_provider)) > 4 and len(str(db_user.oauth_provider_id)) > 4:  # >4 because len('None') is 4
        return {'info': _tn.get(_.userIsOAuth)}

    # this is 3.
    return __check_in_local_known_user(db_user, password, _tn)


def login_user_oauth(request, service, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param service: name of the oauth service
    :param redirect_uri:
    :param old_redirect: redirect_url without modifications
    :param ui_locales:
    :return:
    """
    logger('Auth.Login', 'login_user_oauth', 'service: {}'.format(service))
    if service == 'google':
        return __do_google_oauth(request, redirect_uri, old_redirect, ui_locales)
    elif service == 'github':
        return __do_github_oauth(request, redirect_uri, old_redirect, ui_locales)
    elif service == 'facebook':
        return __do_facebook_oauth(request, redirect_uri, old_redirect, ui_locales)
    elif service == 'twitter':
        return __do_twitter_oauth(request, redirect_uri, old_redirect, ui_locales)
    else:
        return None


def __do_google_oauth(request, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param redirect_uri:
    :param old_redirect:
    :param ui_locales:
    :return:
    """
    if 'state' in redirect_uri and 'code' in redirect_uri:
        url = '{}/{}'.format(request.application_url, 'discuss').replace('http:', 'https:')
        data = google.continue_flow(url, redirect_uri, ui_locales)
        if len(data['error']) != 0 or len(data['missing']) != 0:
            return data

        value_dict = __set_oauth_user(request, data['user'], 'google', ui_locales)
        if isinstance(value_dict, dict):
            if len(value_dict['error']) != 0:
                return value_dict
        else:
            return value_dict

        # return a HTTPFound via 'return success login'
        return __return_success_login(request, False, value_dict['user'], False, url)
    else:
        request.session['oauth_redirect_url'] = old_redirect
        return google.start_flow(redirect_uri)


def __do_github_oauth(request, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param redirect_uri:
    :param old_redirect:
    :param ui_locales:
    :return:
    """
    if 'code' in redirect_uri:
        data = github.continue_flow(redirect_uri, ui_locales)
        if len(data['error']) != 0 or len(data['missing']) != 0:
            return data

        value_dict = __set_oauth_user(request, data['user'], 'github', ui_locales)
        if isinstance(value_dict, dict):
            if len(value_dict['error']) != 0:
                return value_dict
        else:
            return value_dict

        # return a HTTPFound via 'return success login'
        url = '{}/{}'.format(request.application_url, 'discuss').replace('http:', 'https:')
        return __return_success_login(request, False, value_dict['user'], False, url)
    else:
        request.session['oauth_redirect_url'] = old_redirect
        return github.start_flow()


def __do_facebook_oauth(request, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param redirect_uri:
    :param old_redirect:
    :param ui_locales:
    :return:
    """
    if 'state' in redirect_uri and 'code' in redirect_uri:
        url = '{}/{}'.format(request.application_url, 'discuss').replace('http:', 'https:')
        data = facebook.continue_flow(url, redirect_uri, ui_locales)
        if len(data['error']) != 0 or len(data['missing']) != 0:
            return data

        value_dict = __set_oauth_user(request, data['user'], 'facebook', ui_locales)
        if isinstance(value_dict, dict):
            if len(value_dict['error']) != 0:
                return value_dict
        else:
            return value_dict

        # return a HTTPFound via 'return success login'
        return __return_success_login(request, False, value_dict['user'], False, url)
    else:
        request.session['oauth_redirect_url'] = old_redirect
        return facebook.start_flow(redirect_uri)


def __do_twitter_oauth(request, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param redirect_uri:
    :param old_redirect:
    :param ui_locales:
    :return:
    """
    if 'code' in redirect_uri:
        data = twitter.continue_flow(request, redirect_uri)
        if len(data['error']) != 0 or len(data['missing']) != 0:
            return data

        value_dict = __set_oauth_user(request, data['user'], 'twitter', ui_locales)
        if isinstance(value_dict, dict):
            if len(value_dict['error']) != 0:
                return value_dict
        else:
            return value_dict

        # return a HTTPFound via 'return success login'
        url = '{}/{}'.format(request.application_url, 'discuss').replace('http:', 'https:')
        return __return_success_login(request, False, value_dict['user'], False, url)
    else:
        request.session['oauth_redirect_url'] = old_redirect
        return twitter.start_flow(request, redirect_uri)


def __set_oauth_user(request, user_data, service, ui_locales):
    """

    :param request:
    :param user_data:
    :param service:
    :param ui_locales:
    :return:
    """
    _tn = Translator(ui_locales)

    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()
    if not db_group:
        logger('Auth.Login', '__set_oauth_user', 'Error occured')
        return {'error': _tn.get(_.errorTryLateOrContant)}

    ret_dict = user.set_new_oauth_user(user_data['firstname'], user_data['lastname'], user_data['nickname'],
                                       user_data['email'], user_data['gender'], user_data['password'], user_data['id'],
                                       service, _tn)

    if ret_dict['success']:
        url = request.session['oauth_redirect_url']
        return __return_success_login(request, False, ret_dict['user'], False, url)
    else:
        return {'error': ret_dict['error'], 'success': ret_dict['success']}


def __register_user_with_ldap_data(mailer, nickname, password, _tn) -> dict:
    """
    Asks LDAP if the user is known

    :param mailer: instance of pyramids mailer
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :return: dict() or HTTPFound if the user is logged in an it is not the api
    """
    logger('Auth.Login', '__register_user_with_ldap_data', 'user: {}'.format(nickname))
    ldap_data = verify_ldap_user_data(nickname, password, _tn)
    if ldap_data['error']:
        return {'error': ldap_data['error']}

    # register the new user
    ret_dict = user.set_new_user(mailer, ldap_data['firstname'], ldap_data['lastname'], nickname, ldap_data['gender'],
                                 ldap_data['email'], 'NO_PW_BECAUSE_LDAP', _tn)
    if 'success' not in ret_dict:
        return {'error': _tn.get(_.internalKeyError)}

    return {'user': ret_dict['user']}


def __check_in_local_known_user(db_user: User, password: str, _tn) -> dict:
    """
    Tries to check in a local known user.

    :param db_user: current instance of User
    :param password: password of the user
    :param _tn: instance of current translator
    :return: dict()
    """
    logger('Auth.Login', '__check_in_local_known_user', 'user: {}'.format(db_user.nickname))
    if db_user.validate_password(password):
        return {'user': db_user}

    if not (db_user.validate_password('NO_PW_BECAUSE_LDAP') or db_user.password is get_hashed_password(
            'NO_PW_BECAUSE_LDAP')):
        logger('Auth.Login', '__check_in_local_known_user', 'invalid password for the local user')
        return {'error': _tn.get(_.userPasswordNotMatch)}

    data = verify_ldap_user_data(db_user.nickname, password, _tn)
    if data['error']:
        return {'error': data['error']}

    return {'user': db_user}


def __return_success_login(request, for_api, db_user, keep_login, url) -> dict:
    """

    :param request: web servers request
    :param for_api:
    :param db_user:
    :param keep_login:
    :param url:
    :return:
    """
    if for_api:
        logger('Auth.Login', 'login_user', 'return for api: success')
        return {'status': 'success'}  # api
    else:
        headers, url = __refresh_headers_and_url(request, db_user, keep_login, url)
        sleep(0.5)
        logger('Auth.Login', 'login_user', 'return HTTPFound with url {}'.format(url))
        return HTTPFound(location=url, headers=headers)  # success


def register_user_with_ajax_data(data, lang, mailer: Mailer):
    """
    Consume the ajax data for an login attempt

    :param data: validated params of webserver's request
    :param lang: language
    :param mailer: Mailer
    :return: Boolean, String, User
    """
    _tn = Translator(lang)
    success = ''

    firstname = escape_string(data['firstname'])
    lastname = escape_string(data['lastname'])
    nickname = escape_string(data['nickname'])
    email = escape_string(data['email'])
    gender = escape_string(data['gender'])
    password = escape_string(data['password'])
    passwordconfirm = escape_string(data['passwordconfirm'])
    mode = escape_string(data['mode'])
    recaptcha = escape_string(data['g-recaptcha-response'])
    db_new_user = None

    msg = __check_login_params(nickname, email, password, passwordconfirm, mode, recaptcha)
    if msg:
        return success, _tn.get(msg), db_new_user

    # getting the authors group
    db_group = DBDiscussionSession.query(Group).filter_by(name="users").first()

    # does the group exists?
    if not db_group:
        msg = _tn.get(_.errorTryLateOrContant)
        logger('Auth.Login', 'user_registration', 'Error occured')
        return success, msg, db_new_user

    ret_dict = user.set_new_user(mailer, firstname, lastname, nickname, gender, email, password, _tn)
    success = ret_dict['success']
    error = ret_dict['error']
    db_new_user = ret_dict['user']

    msg = error
    if success:
        msg = _tn.get(_.accountWasAdded).format(nickname)

    return success, msg, db_new_user


def __check_login_params(nickname, email, password, passwordconfirm, mode, recaptcha) -> Keywords:
    is_human = True
    error = False
    if mode == 'manually':
        is_human, error = validate_recaptcha(recaptcha)

    # database queries mail verification
    db_nick1 = get_user_by_case_insensitive_nickname(nickname)
    db_nick2 = get_user_by_case_insensitive_public_nickname(nickname)
    db_mail = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    is_mail_valid = validate_email(email, check_mx=True)

    # are the password equal?
    if not password == passwordconfirm:
        logger('Auth.Login', 'user_registration', 'Passwords are not equal')
        return _.pwdNotEqual

    # empty password?
    if len(password) <= 5:
        logger('Auth.Login', 'user_registration', 'Password too short')
        return _.pwdShort

    # is the nick already taken?
    if db_nick1 or db_nick2:
        logger('Auth.Login', 'user_registration', 'Nickname \'' + nickname + '\' is taken')
        return _.nickIsTaken

    # is the email already taken?
    if db_mail:
        logger('Auth.Login', 'user_registration', 'E-Mail \'' + email + '\' is taken')
        return _.mailIsTaken

    if len(email) < 2 or not is_mail_valid:
        logger('Auth.Login', 'user_registration', 'E-Mail \'' + email + '\' is too short or not valid')
        return _.mailNotValid

    # is anti-spam correct?
    if not is_human or error:
        logger('Auth.Login', 'user_registration', 'recaptcha error')
        return _.maliciousAntiSpam

    return None


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
    logger('Auth.Login', '__refresh_headers_and_url', 'login', 'login successful / keep_login: {}'.format(keep_login))
    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    db_settings.should_hold_the_login(keep_login)
    logger('Auth.Login', '__refresh_headers_and_url', 'remembering headers for {}'.format(db_user.nickname))
    headers = remember(request, db_user.nickname)

    logger('Auth.Login', '__refresh_headers_and_url', 'update login timestamp')
    db_user.update_last_login()
    db_user.update_last_action()
    transaction.commit()

    ending = ['/?session_expired=true', '/?session_expired=false']
    for e in ending:
        if url.endswith(e):
            url = url[0:-len(e)]

    return headers, url
