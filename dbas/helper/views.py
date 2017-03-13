"""
Helper for D-BAS Views

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from time import sleep

import transaction
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember
from sqlalchemy import func
from validate_email import validate_email

import dbas.helper.email as EmailHelper
import dbas.helper.history as HistoryHelper
import dbas.helper.issue as IssueHelper
import dbas.helper.issue as issue_helper
import dbas.helper.voting as VotingHelper
import dbas.recommender_system as RecommenderSystem
import dbas.user_management as UserHandler
from dbas.auth.ldap import verify_ldap_user_data
from dbas.auth.recaptcha import validate_recaptcha
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Settings
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import is_integer, check_belonging_of_argument, check_belonging_of_statement
from dbas.lib import get_text_for_statement_uid, get_discussion_language, escape_string, get_user_by_case_insensitive_nickname, is_usage_with_ldap
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for
from dbas.review.helper.reputation import rep_reason_first_confrontation
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio


def get_nickname(request_authenticated_userid, for_api=None, api_data=None):
    """
    Given data from api, return nickname and session_id.

    :param request_authenticated_userid:
    :param for_api: Boolean
    :param api_data:
    :return:
    """
    nickname = api_data["nickname"] if api_data and for_api else request_authenticated_userid
    return nickname


def preparation_for_view(for_api, api_data, request, request_authenticated_userid):
    """
    Does some elementary things like: getting nickname, session id and history. Additionally boolean, if the session is expired

    :param for_api: True, if the values are for the api
    :param api_data: Array with api data
    :param request: Current request
    :param request_authenticated_userid: User.nickname
    :return: nickname, session_id, session_expired, history
    """
    nickname = get_nickname(request_authenticated_userid, for_api, api_data)
    session_expired = UserHandler.update_last_action(nickname)
    history         = request.params['history'] if 'history' in request.params else ''
    #  HistoryHelper.save_path_in_database(nickname, request.path, history)  # TODO 322
    HistoryHelper.save_history_in_cookie(request, request.path, history)
    return nickname, session_expired, history


def prepare_parameter_for_justification(request, for_api):
    """
    Prepares some paramater for the justification step

    :param request: webservers request
    :param for_api: Boolean
    :return: String, Statement.uid/Argument.uid, String, Boolean, String, Issue.uid, Language.ui_locales, dict()
    """
    slug                = request.matchdict['slug'] if 'slug' in request.matchdict else ''
    statement_or_arg_id = request.matchdict['statement_or_arg_id'] if 'statement_or_arg_id' in request.matchdict else ''
    mode                = request.matchdict['mode'] if 'mode' in request.matchdict else ''
    supportive          = mode == 't' or mode == 'd'  # supportive = t or do not know mode
    relation            = request.matchdict['relation'][0] if len(request.matchdict['relation']) > 0 else ''
    issue               = issue_helper.get_id_of_slug(slug, request, True) if len(slug) > 0 else issue_helper.get_issue_id(request)
    disc_ui_locales     = get_discussion_language(request, issue)
    issue_dict          = issue_helper.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, for_api)

    return slug, statement_or_arg_id, mode, supportive, relation, issue, disc_ui_locales, issue_dict


def handle_justification_step(request, for_api, ui_locales, nickname, history):
    """
    Handles the justification step

    :param request: webserver's request
    :param for_api: Boolean
    :param ui_locales: Language.ui_locales
    :param nickname: User.nickname
    :param history: string
    :return: dict(), dict(), dict()
    """
    slug, statement_or_arg_id, mode, supportive, relation, issue, disc_ui_locales, issue_dict = prepare_parameter_for_justification(request, for_api)
    main_page = request.application_url

    if not is_integer(statement_or_arg_id, True):
        raise HTTPNotFound()
        # return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([request.path[1:]], True)), None, None

    if [c for c in ('t', 'f') if c in mode] and relation == '':
        logger('ViewHelper', 'handle_justification_step', 'justify statement')
        if not get_text_for_statement_uid(statement_or_arg_id) or not check_belonging_of_statement(issue, statement_or_arg_id):
            raise HTTPNotFound()
            # return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, statement_or_arg_id])), None, None
        item_dict, discussion_dict, extras_dict = preparation_for_justify_statement(request, for_api, main_page, slug,
                                                                                    statement_or_arg_id, supportive,
                                                                                    ui_locales, nickname, mode,
                                                                                    nickname, history)

    elif 'd' in mode and relation == '':
        logger('ViewHelper', 'handle_justification_step', 'do not know')
        if not check_belonging_of_argument(issue, statement_or_arg_id) and \
                not check_belonging_of_statement(issue, statement_or_arg_id):
            raise HTTPNotFound()
            # return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, statement_or_arg_id])), None, None
        item_dict, discussion_dict, extras_dict = preparation_for_dont_know_statement(request, for_api, main_page,
                                                                                      slug, statement_or_arg_id,
                                                                                      supportive, ui_locales,
                                                                                      nickname, nickname, history)

    elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
        logger('ViewHelper', 'handle_justification_step', 'justify argument')
        if not check_belonging_of_argument(issue, statement_or_arg_id):
            raise HTTPNotFound()
            # return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, statement_or_arg_id])), None, None
        item_dict, discussion_dict, extras_dict = preparation_for_justify_argument(request, for_api, main_page, slug,
                                                                                   statement_or_arg_id, supportive,
                                                                                   ui_locales, nickname, relation,
                                                                                   nickname, history)
        # add reputation
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_confrontation)
        # send message if the user is now able to review
        if broke_limit:
            _t = Translator(ui_locales)
            send_request_for_info_popup_to_socketio(nickname, _t.get(_.youAreAbleToReviewNow), request.application_url + '/review')

    else:
        logger('ViewHelper', 'handle_justification_step', '404')
        raise HTTPNotFound()
        # return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, 'justify', statement_or_arg_id, mode, relation])), None, None

    return item_dict, discussion_dict, extras_dict


def preparation_for_justify_statement(request, for_api, main_page, slug, statement_uid, supportive, ui_locales,
                                      request_authenticated_userid, mode, nickname, history):
    """
    Prepares some paramater for the justification step for an statement

    :param request: webserver's request
    :param for_api: Boolean
    :param main_page: string
    :param slug: String
    :param statement_uid: Statement.uid
    :param supportive: Boolean
    :param mode: String
    :param ui_locales: Language.ui_locales
    :return: dict(), dict(), dict()
    """
    logger('ViewHelper', 'preparation_for_justify_statement', 'main')

    logged_in = DBDiscussionSession.query(User).filter_by(nickname=nickname).first() is not None
    _ddh, _idh, _dh = __prepare_helper(ui_locales, nickname, history, main_page, slug, for_api, request)

    VotingHelper.add_click_for_statement(statement_uid, nickname, supportive)

    item_dict       = _idh.get_array_for_justify_statement(statement_uid, nickname, supportive, history)
    discussion_dict = _ddh.get_dict_for_justify_statement(statement_uid, main_page, slug, supportive, len(item_dict['elements']), nickname)
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request, request_authenticated_userid, mode == 't',
                                              application_url=main_page, for_api=for_api)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0 or len(item_dict['elements']) == 1 and logged_in:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify=True,
                                    current_premise=get_text_for_statement_uid(statement_uid),
                                    supportive=supportive)
    return item_dict, discussion_dict, extras_dict


def preparation_for_dont_know_statement(request, for_api, main_page, slug, statement_or_arg_id, supportive, ui_locales, request_authenticated_userid, nickname, history):
    """
    Prepares some paramater for the "don't know" step

    :param request: webserver's request
    :param for_api: Boolean
    :param main_page: string
    :param slug: String
    :param statement_or_arg_id: Argument.uid / Statement.uid
    :param supportive: Boolean
    :param ui_locales: Language.ui_locales
    :param request_authenticated_userid: User.nickname
    :param nickname: User.nickname
    :param history: string
    :return: dict(), dict(), dict()
    """
    logger('ViewHelper', 'preparation_for_dont_know_statement', 'main')

    issue               = IssueHelper.get_id_of_slug(slug, request, True) if len(slug) > 0 else IssueHelper.get_issue_id(request)
    disc_ui_locales     = get_discussion_language(request, issue)
    _ddh                = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=main_page, slug=slug)
    _idh                = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=request.path, history=history)
    _dh                 = DictionaryHelper(ui_locales, disc_ui_locales)

    # dont know
    argument_uid    = RecommenderSystem.get_argument_by_conclusion(statement_or_arg_id, supportive)

    discussion_dict = _ddh.get_dict_for_dont_know_reaction(argument_uid, main_page, request_authenticated_userid)
    item_dict       = _idh.get_array_for_dont_know_reaction(argument_uid, supportive, nickname, discussion_dict['gender'])
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request, argument_id=argument_uid,
                                              application_url=main_page, for_api=for_api, nickname=request_authenticated_userid)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_dont_know=True,
                                    current_premise=get_text_for_statement_uid(statement_or_arg_id))
    return item_dict, discussion_dict, extras_dict


def preparation_for_justify_argument(request, for_api, main_page, slug, statement_or_arg_id, supportive, ui_locales,
                                     request_authenticated_userid, relation, nickname, history):
    """
    Prepares some paramater for the justification step for an argument

    :param request: webserver's request
    :param for_api: Boolean
    :param main_page: string
    :param slug: String
    :param statement_or_arg_id: Argument.uid / Statement.uid
    :param supportive: Boolean
    :param relation: String
    :param ui_locales: Language.ui_locales
    :return: dict(), dict(), dict()
    """
    logger('ViewHelper', 'preparation_for_justify_argument', 'main')

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    logged_in = db_user is not None
    _ddh, _idh, _dh = __prepare_helper(ui_locales, nickname, history, main_page, slug, for_api, request)

    # justifying argument
    # is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
    item_dict       = _idh.get_array_for_justify_argument(statement_or_arg_id, relation, logged_in, nickname, history)
    discussion_dict = _ddh.get_dict_for_justify_argument(statement_or_arg_id, supportive, relation)
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request,
                                              argument_id=statement_or_arg_id, application_url=main_page, for_api=for_api,
                                              nickname=request_authenticated_userid)
    # is the discussion at the end?
    if not logged_in and len(item_dict['elements']) == 1 or logged_in and len(item_dict['elements']) == 1:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify_argumentation=True)

    return item_dict, discussion_dict, extras_dict


def __prepare_helper(ui_locales, nickname, history, main_page, slug, for_api, request):
    """
    Prepares helper objects

    :param ui_locales: Language.ui_locales
    :param nickname: User.nickname
    :param history: string
    :param main_page: string
    :param slug: String
    :param for_api: Boolean
    :param request: webserver's request
    :return: dict(), dict(), dict()
    """
    issue           = IssueHelper.get_id_of_slug(slug, request, True) if len(slug) > 0 else IssueHelper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=main_page, slug=slug)
    idh = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=request.path, history=history)
    dh  = DictionaryHelper(ui_locales, disc_ui_locales)
    return ddh, idh, dh


def try_to_contact(request, name, email, phone, content, ui_locales, recaptcha):
    """
    Trys to send an contact mail

    :param request: webserver's request
    :param name: String
    :param email: String
    :param phone: String
    :param content: String
    :param ui_locales: Language.ui_locales
    :param recaptcha: Googles Recaptcha
    :return: Boolean, String, Boolean
    """
    logger('ViewHelper', 'try_to_contact', 'name: ' + name + ', email: ' + email + ', phone: ' + phone + ', content: ' + content)
    _t = Translator(ui_locales)
    send_message = False

    is_human, error = validate_recaptcha(recaptcha)

    logger('ViewHelper', 'try_to_contact', 'validating email')
    is_mail_valid = validate_email(email, check_mx=True)

    # check for empty username
    if not name:
        logger('ViewHelper', 'try_to_contact', 'username empty')
        contact_error = True
        message = _t.get(_.emptyName)

    # check for non valid mail
    elif not is_mail_valid:
        logger('ViewHelper', 'try_to_contact', 'mail is not valid')
        contact_error = True
        message = _t.get(_.invalidEmail)

    # check for empty content
    elif not content:
        logger('main_contact', 'try_to_contact', 'content is empty')
        contact_error = True
        message = _t.get(_.emtpyContent)

    # check for empty spam
    elif not is_human or error:
        logger('ViewHelper', 'try_to_contact', 'recaptcha error')
        contact_error = True
        message = _t.get(_.maliciousAntiSpam)

    else:
        subject = _t.get(_.contact) + ' D-BAS'
        body = _t.get(_.name) + ': ' + name + '\n'
        body += _t.get(_.mail) + ': ' + email + '\n'
        body += _t.get(_.phone) + ': ' + phone + '\n'
        body += _t.get(_.message) + ':\n' + content
        EmailHelper.send_mail(request, subject, body, 'dbas.hhu@gmail.com', ui_locales)
        body = '* ' + _t.get(_.thisIsACopyOfMail).upper() + ' *\n\n' + body
        subject = '[D-BAS INFO] ' + subject
        send_message, message = EmailHelper.send_mail(request, subject, body, email, ui_locales)
        contact_error = not send_message

    return contact_error, message, send_message


def login_user(request, nickname, password, for_api, keep_login, _tn):
    """
    A try to login the user

    :param request: webserver's request
    :param nickname: User.nickname
    :param password: String
    :param for_api: Boolean
    :param keep_login: Boolean
    :param _tn: Translator
    :return: dict() or HTTPFound if the user is logged in an it is not the api
    """

    # getting params from request or api
    if not nickname and not password:
        nickname = escape_string(request.params['user'])
        password = escape_string(request.params['password'])
        keep_login = escape_string(request.params['keep_login'])
        keep_login = True if keep_login == 'true' else False
        url = request.params['url']
    else:
        nickname = escape_string(nickname)
        password = escape_string(password)
        url = ''

    is_ldap = is_usage_with_ldap(request)

    db_user = get_user_by_case_insensitive_nickname(nickname)
    if not db_user:  # check if the user exists
        msg = __login_user_not_existing(request, nickname, password, _tn, is_ldap)
        if msg is not None:
            return {'error': msg}  # error

    else:
        error = __login_user_is_existing(request, nickname, password, _tn, is_ldap, db_user)
        if error is not None:
            return {'error': error}  # error

    headers, url = __refresh_headers_and_url(request, db_user, keep_login, url)

    if for_api:
        logger('ViewHelper', 'login_user', 'return for api: success')
        return {'status': 'success'}  # api
    else:
        logger('ViewHelper', 'login_user', 'return success: ' + url)
        sleep(0.5)
        return HTTPFound(location=url, headers=headers)  # success


def __login_user_not_existing(request, nickname, password, _tn, is_ldap):
    """
    First login of a user who is not registered

    :param request: webservers request
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :param is_ldap: Boolean
    :return: String or None on success
    """
    logger('ViewHelper', 'login_user', 'user \'' + nickname + '\' does not exists')

    # if the user does not exists and we are using LDAP, we'll grep the user
    if is_ldap:
        msg, db_user = __login_user_ldap(request, nickname, password, _tn)
        if msg is not None:
            return msg

    else:
        success, msg, db_user = try_to_register_new_user_via_ajax(request, _tn)
        if not success:
            return msg

    return None


def __login_user_is_existing(request, nickname, password, _tn, is_ldap, db_user):
    """
    Login of a user who is already registered

    :param request: webservers request
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :param is_ldap: Boolean
    :param db_user: User
    :return: String or None on success
    """
    logger('ViewHelper', 'login_user', 'user \'' + nickname + '\' exists')
    if is_ldap:
        local_login = db_user.validate_password(password)

        user_data = None
        if not local_login:
            user_data = verify_ldap_user_data(request, nickname, password)

        if user_data is None and not local_login:  # check password
            logger('ViewHelper', 'login_user', 'wrong password')
            error = _tn.get(_.userPasswordNotMatch)
            return error
    else:
        if not db_user.validate_password(password):  # check password
            logger('ViewHelper', 'user_login', 'wrong password')
            error = _tn.get(_.userPasswordNotMatch)
            return error


def __login_user_ldap(request, nickname, password, _tn):
    """
    Login the user via LDAP

    :param request: webservers request
    :param nickname: User.nickname
    :param password: String
    :param _tn: Translator
    :return: String, User
    """
    logger('ViewHelper', '__login_user_ldap', nickname)
    user_data = verify_ldap_user_data(request, nickname, password)

    if not user_data:
        return _tn.get(_.userPasswordNotMatch), ''
    firstname = user_data[0]
    lastname = user_data[1]
    gender = user_data[2]
    email = user_data[3]
    success, db_user = UserHandler.set_new_user(request, firstname, lastname, nickname, gender, email, password, _tn)

    if not success:
        error = _tn.get(_.userPasswordNotMatch)
        return error, db_user
    return None, db_user


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
    logger('ViewHelper', 'user_login', 'login', 'login successful / keep_login: ' + str(keep_login))
    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    db_settings.should_hold_the_login(keep_login)
    headers = remember(request, db_user.nickname)

    # update timestamp
    logger('ViewHelper', 'user_login', 'update login timestamp')
    db_user.update_last_login()
    db_user.update_last_action()
    transaction.commit()

    ending = ['/?session_expired=true', '/?session_expired=false']
    for e in ending:
        if url.endswith(e):
            url = url[0:-len(e)]

    return headers, url


def try_to_register_new_user_via_ajax(request, _tn):
    """
    Consume the ajax data for an login attempt

    :param request: webserver's request
    :param _tn: Translator
    :return: Boolean, String, User
    """
    success = ''
    params          = request.params
    firstname       = escape_string(params['firstname']) if 'firstname' in params else ''
    lastname        = escape_string(params['lastname']) if 'lastname' in params else ''
    nickname        = escape_string(params['nickname']) if 'nickname' in params else ''
    email           = escape_string(params['email']) if 'email' in params else ''
    gender          = escape_string(params['gender']) if 'gender' in params else ''
    password        = escape_string(params['password']) if 'password' in params else ''
    passwordconfirm = escape_string(params['passwordconfirm']) if 'passwordconfirm' in params else ''
    recaptcha       = request.params['g-recaptcha-response'] if 'g-recaptcha-response' in request.params else ''
    is_human, error = validate_recaptcha(recaptcha)
    db_new_user = None

    # database queries mail verification
    db_nick1 = get_user_by_case_insensitive_nickname(nickname)
    db_nick2 = DBDiscussionSession.query(User).filter(func.lower(User.public_nickname) == func.lower(nickname)).first()
    db_mail = DBDiscussionSession.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    is_mail_valid = validate_email(email, check_mx=True)

    # are the password equal?
    if not password == passwordconfirm:
        logger('ViewHelper', 'user_registration', 'Passwords are not equal')
        msg = _tn.get(_.pwdNotEqual)
    # is the nick already taken?
    elif db_nick1 or db_nick2:
        logger('ViewHelper', 'user_registration', 'Nickname \'' + nickname + '\' is taken')
        msg = _tn.get(_.nickIsTaken)
    # is the email already taken?
    elif db_mail:
        logger('ViewHelper', 'user_registration', 'E-Mail \'' + email + '\' is taken')
        msg = _tn.get(_.mailIsTaken)
    # is the email valid?
    elif not is_mail_valid:
        logger('ViewHelper', 'user_registration', 'E-Mail \'' + email + '\' is not valid')
        msg = _tn.get(_.mailNotValid)
    # is anti-spam correct?
    elif not is_human or error:
        logger('ViewHelper', 'user_registration', 'recaptcha error')
        msg = _tn.get(_.maliciousAntiSpam)
    # lets go
    else:

        # getting the authors group
        db_group = DBDiscussionSession.query(Group).filter_by(name="users").first()

        # does the group exists?
        if not db_group:
            msg = _tn.get(_.errorTryLateOrContant)
            logger('ViewHelper', 'user_registration', 'Error occured')
            return success, msg, db_new_user

        success, tmp = UserHandler.set_new_user(request, firstname, lastname, nickname, gender, email, password, _tn)
        if success:
            msg = _tn.get(_.accountWasAdded).format(nickname)
            db_new_user = db_new_user
        else:
            msg = tmp

    return success, msg, db_new_user
