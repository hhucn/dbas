"""
Login Handler for D-BAS

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging

import transaction
from pyramid.security import remember
from pyramid_mailer import Mailer
from sqlalchemy import func
from validate_email import validate_email

from dbas.auth.ldap import verify_ldap_user_data
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group
from dbas.handler import user
from dbas.lib import escape_string, get_user_by_case_insensitive_nickname, \
    get_user_by_case_insensitive_public_nickname
from dbas.strings.keywords import Keywords as _, Keywords
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)
oauth_providers = ['google', 'github', 'facebook', 'twitter']

PW_FOR_LDAP_USER = 'NO_PW_BECAUSE_LDAP'


def login_local_user(nickname: str, password: str, mailer: Mailer, lang='en') -> dict:
    """
    Try to login the user whereby she is maybe a HHU-LDAP user or known locally

    :param nickname: User.nickname
    :param password: String
    :param mailer: request.mailer
    :param lang: current language
    :return: dict() or HTTPFound if the user is logged in and it is not the api
    """
    LOG.debug("Trying to login user: %s", nickname)
    _tn = Translator(lang)

    # now we have several options:
    # 1. the user is unknown in our DB, maybe has HHU-LDAP account
    # 2. oauth nickname
    # 3. the user is known, but
    #  a) keep local
    #  b) keep in ldap
    db_user = get_user_by_case_insensitive_nickname(nickname)
    if not db_user:  # this is 1.
        return __register_user_with_ldap_data(mailer, nickname, password, _tn)

    # this is 2.
    if len(str(db_user.oauth_provider)) > 4 and len(str(db_user.oauth_provider_id)) > 4:  # >4 because len('None') is 4
        return {'info': _tn.get(_.userIsOAuth)}

    # this is 3.
    return __check_in_local_known_user(db_user, password, _tn)


def __register_user_with_ldap_data(mailer, nickname, password, _tn) -> dict:
    """
    Asks LDAP if the user is known

    :param mailer: instance of pyramids mailer
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :return: dict() or HTTPFound if the user is logged in an it is not the api
    """
    LOG.debug("user: %s", nickname)
    ldap_data = verify_ldap_user_data(nickname, password, _tn)
    if ldap_data['error']:
        return {'error': ldap_data['error']}

    # register the new user

    ldap_data['nickname'] = nickname
    ret_dict = user.set_new_user(mailer, ldap_data, PW_FOR_LDAP_USER, _tn)
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
    LOG.debug("user: %s", db_user.nickname)

    if db_user.validate_password(PW_FOR_LDAP_USER):
        # is ldap
        data = verify_ldap_user_data(db_user.nickname, password, _tn)
        if data['error']:
            LOG.debug("Invalid password for the ldap user")
            return {'error': data['error']}
        else:
            return {'user': db_user}

    # check no-ldap user
    elif db_user.validate_password(password):
        return {'user': db_user}
    else:
        LOG.debug("Invalid password for the local user")
        return {'error': _tn.get(_.userPasswordNotMatch)}


def register_user_with_json_data(data, lang, mailer: Mailer):
    """
    Consume the ajax data for an login attempt

    :param data: validated params of webserver's request
    :param lang: language
    :param mailer: Mailer
    :return: Boolean, String, User
    """
    _tn = Translator(lang)
    success = ''

    firstname = ""
    lastname = ""
    nickname = ""
    email = ""
    gender = ""
    password = ""
    passwordconfirm = ""
    db_new_user = None

    try:
        firstname = escape_string(data['firstname'])
        lastname = escape_string(data['lastname'])
        nickname = escape_string(data['nickname'])
        email = escape_string(data['email'])
        gender = escape_string(data['gender'])
        password = escape_string(data['password'])
        passwordconfirm = escape_string(data['passwordconfirm'])
    except:
        pass

    msg = __check_login_params(firstname, lastname, nickname, email, password, passwordconfirm)
    if msg:
        return success, _tn.get(msg), db_new_user

    # getting the authors group
    db_group = DBDiscussionSession.query(Group).filter_by(name="users").first()

    # does the group exists?
    if not db_group:
        msg = _tn.get(_.errorTryLateOrContant)
        LOG.debug("Error occured")
        return success, msg, db_new_user

    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'nickname': nickname,
        'gender': gender,
        'email': email
    }
    ret_dict = user.set_new_user(mailer, user_data, password, _tn)
    success = ret_dict['success']
    error = ret_dict['error']
    db_new_user = ret_dict['user']

    msg = error
    if success:
        msg = _tn.get(_.accountWasAdded).format(nickname)

    return success, msg, db_new_user


def __check_login_params(firstname, lastname, nickname, email, password, passwordconfirm) -> Keywords:
    db_nick1 = get_user_by_case_insensitive_nickname(nickname)
    db_nick2 = get_user_by_case_insensitive_public_nickname(nickname)
    db_mail = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    is_mail_valid = validate_email(email, check_mx=True)

    if len(firstname) == 0:
        LOG.debug("firstname is empty", firstname)
        return _.checkFirstname

    if len(lastname) == 0:
        LOG.debug("lastename is empty", lastname)
        return _.checkLastname

    if len(nickname) == 0:
        LOG.debug("username is empty", nickname)
        return _.checkNickname

    if len(email) == 0:
        LOG.debug("email is empty", email)
        return _.checkEmail

    if len(password) == 0:
        LOG.debug("password is emtpy", email)
        return _.checkPassword

    if len(passwordconfirm) == 0:
        LOG.debug("password-confirm is empty", passwordconfirm)
        return _.checkPasswordConfirm

    # are the password equal?
    if not password == passwordconfirm:
        LOG.debug("Passwords are not equal")
        return _.pwdNotEqual

    # empty password?
    if len(password) <= 5:
        LOG.debug("Password too short")
        return _.pwdShort

    # is the nick already taken?
    if db_nick1 or db_nick2:
        LOG.debug("Nickname '%s' is taken", nickname)
        return _.nickIsTaken

    # is the email already taken?
    if db_mail:
        LOG.debug("E-Mail '%s' is taken", email)
        return _.mailIsTaken

    if len(email) < 2 or not is_mail_valid:
        LOG.debug("E-Mail '%s' is too short or not valid otherwise", email)
        return _.mailNotValid

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
    LOG.debug("Login successful / keep_login: %s", keep_login)
    db_settings = db_user.settings
    db_settings.should_hold_the_login(keep_login)
    LOG.debug("Remembering headers for %s", db_user.nickname)
    headers = remember(request, db_user.nickname)

    LOG.debug("Update login timestamp")
    db_user.update_last_login()
    db_user.update_last_action()
    transaction.commit()

    ending = ['/?session_expired=true', '/?session_expired=false']
    for e in ending:
        if url.endswith(e):
            url = url[0:-len(e)]

    return headers, url
