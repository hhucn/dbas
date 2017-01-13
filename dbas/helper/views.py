"""
Helper for D-BAS Views

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Settings, Language
from dbas.logger import logger
from dbas.lib import get_text_for_statement_uid, get_discussion_language, escape_string, get_user_by_case_insensitive_nickname, is_usage_with_ldap, validate_recaptcha
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _
from validate_email import validate_email

from dbas.url_manager import UrlManager
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from dbas.review.helper.reputation import add_reputation_for
from dbas.input_validator import is_integer, check_belonging_of_argument, check_belonging_of_statement
from websocket.lib import send_request_for_info_popup_to_socketio
from dbas.review.helper.reputation import rep_reason_first_confrontation

import dbas.helper.issue as issue_helper
import dbas.recommender_system as RecommenderSystem
import dbas.helper.email as EmailHelper
import dbas.helper.history as HistoryHelper
import dbas.helper.issue as IssueHelper
import dbas.user_management as UserHandler
import dbas.handler.password as PasswordHandler
import dbas.helper.voting as VotingHelper
import transaction

from time import sleep


def get_nickname(request_authenticated_userid, for_api=None, api_data=None):
    """
    Given data from api, return nickname and session_id.

    :param request_authenticated_userid:
    :param for_api:
    :param api_data:
    :return:
    """
    nickname = api_data["nickname"] if api_data and for_api else request_authenticated_userid
    return nickname


def preparation_for_view(for_api, api_data, request, request_authenticated_userid):
    """
    Does some elementary things like: getting nickname, session id and history. Additionally boolean, if the sesseion is expired

    :param for_api: True, if the values are for the api
    :param api_data: Array with api data
    :param request: Current request
    :param request_authenticated_userid:
    :return: nickname, session_id, session_expired, history
    """
    nickname = get_nickname(request_authenticated_userid, for_api, api_data)
    session_expired = UserHandler.update_last_action(nickname)
    history         = request.params['history'] if 'history' in request.params else ''
    HistoryHelper.save_path_in_database(nickname, request.path)
    HistoryHelper.save_history_in_cookie(request, request.path, history)
    return nickname, session_expired, history


def prepare_parameter_for_justification(request, for_api):
    """

    :param request:
    :param for_api:
    :return:
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


def handle_justification_step(request, for_api, api_data, ui_locales, nickname):
    """

    :param request:
    :param for_api:
    :param api_data:
    :param ui_locales:
    :param nickname:
    :return:
    """
    slug, statement_or_arg_id, mode, supportive, relation, issue, disc_ui_locales, issue_dict = prepare_parameter_for_justification(request, for_api)
    main_page = request.application_url

    if not is_integer(statement_or_arg_id, True):
        return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([request.path[1:]], True)), None, None

    if [c for c in ('t', 'f') if c in mode] and relation == '':
        logger('ViewHelper', 'handle_justification_step', 'justify statement')
        if not get_text_for_statement_uid(statement_or_arg_id) or not check_belonging_of_statement(issue, statement_or_arg_id):
            return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, statement_or_arg_id])), None, None
        item_dict, discussion_dict, extras_dict = preparation_for_justify_statement(request, for_api, api_data,
                                                                                    main_page, slug,
                                                                                    statement_or_arg_id,
                                                                                    supportive, ui_locales,
                                                                                    nickname, mode)

    elif 'd' in mode and relation == '':
        logger('ViewHelper', 'handle_justification_step', 'do not know')
        if not check_belonging_of_argument(issue, statement_or_arg_id) and \
                not check_belonging_of_statement(issue, statement_or_arg_id):
            return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, statement_or_arg_id])), None, None
        item_dict, discussion_dict, extras_dict = preparation_for_dont_know_statement(request, for_api, api_data,
                                                                                      main_page, slug,
                                                                                      statement_or_arg_id,
                                                                                      supportive, ui_locales,
                                                                                      nickname)

    elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
        logger('ViewHelper', 'handle_justification_step', 'justify argument')
        if not check_belonging_of_argument(issue, statement_or_arg_id):
            return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, statement_or_arg_id])), None, None
        item_dict, discussion_dict, extras_dict = preparation_for_justify_argument(request, for_api, api_data,
                                                                                   main_page, slug,
                                                                                   statement_or_arg_id,
                                                                                   supportive, ui_locales,
                                                                                   nickname, relation)
        # add reputation
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_confrontation)
        # send message if the user is now able to review
        if broke_limit:
            _t = Translator(ui_locales)
            send_request_for_info_popup_to_socketio(nickname, _t.get(_.youAreAbleToReviewNow), request.application_url + '/review')

    else:
        logger('ViewHelper', 'handle_justification_step', '404')
        return HTTPFound(location=UrlManager(request.application_url, for_api=for_api).get_404([slug, 'justify', statement_or_arg_id, mode, relation])), None, None

    return item_dict, discussion_dict, extras_dict


def preparation_for_justify_statement(request, for_api, api_data, main_page, slug, statement_or_arg_id, supportive, ui_locales, request_authenticated_userid, mode):
    """

    :param request:
    :param for_api:
    :param api_data:
    :param main_page:
    :param slug:
    :param statement_or_arg_id:
    :param supportive:
    :param mode:
    :param ui_locales:
    :return:
    """
    logger('ViewHelper', 'preparation_for_justify_statement', 'main')

    nickname, session_expired, history = preparation_for_view(for_api, api_data, request, request_authenticated_userid)
    logged_in = DBDiscussionSession.query(User).filter_by(nickname=nickname).first() is not None
    _ddh, _idh, _dh = __prepare_helper(ui_locales, nickname, history, main_page, slug, for_api, request)

    VotingHelper.add_vote_for_statement(statement_or_arg_id, nickname, supportive)

    item_dict       = _idh.get_array_for_justify_statement(statement_or_arg_id, nickname, supportive)
    discussion_dict = _ddh.get_dict_for_justify_statement(statement_or_arg_id, main_page, slug, supportive, len(item_dict['elements']), nickname)
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request, request_authenticated_userid, mode == 't',
                                              application_url=main_page, for_api=for_api)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0 or len(item_dict['elements']) == 1 and logged_in:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify=True,
                                    current_premise=get_text_for_statement_uid(statement_or_arg_id),
                                    supportive=supportive)
    return item_dict, discussion_dict, extras_dict


def preparation_for_dont_know_statement(request, for_api, api_data, main_page, slug, statement_or_arg_id, supportive, ui_locales, request_authenticated_userid):
    """

    :param request:
    :param for_api:
    :param api_data:
    :param main_page:
    :param slug:
    :param statement_or_arg_id:
    :param supportive:
    :param ui_locales:
    :param request_authenticated_userid:
    :return:
    """
    logger('ViewHelper', 'preparation_for_dont_know_statement', 'main')

    nickname, session_expired, history = preparation_for_view(for_api, api_data, request, request_authenticated_userid)

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


def preparation_for_justify_argument(request, for_api, api_data, main_page, slug, statement_or_arg_id, supportive, ui_locales, request_authenticated_userid, relation):
    """

    :param request:
    :param for_api:
    :param api_data:
    :param main_page:
    :param slug:
    :param statement_or_arg_id:
    :param supportive:
    :param relation:
    :param ui_locales:
    :return:
    """
    logger('ViewHelper', 'preparation_for_justify_argument', 'main')

    nickname, session_expired, history = preparation_for_view(for_api, api_data, request, request_authenticated_userid)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    logged_in = db_user is not None
    _ddh, _idh, _dh = __prepare_helper(ui_locales, nickname, history, main_page, slug, for_api, request)

    # justifying argument
    # is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
    item_dict       = _idh.get_array_for_justify_argument(statement_or_arg_id, relation, logged_in, nickname)
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

    :param ui_locales:
    :param nickname:
    :param history:
    :param main_page:
    :param slug:
    :param for_api:
    :param request:
    :return:
    """
    issue           = IssueHelper.get_id_of_slug(slug, request, True) if len(slug) > 0 else IssueHelper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    ddh = DiscussionDictHelper(disc_ui_locales, nickname, history, main_page=main_page, slug=slug)
    idh = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=request.path, history=history)
    dh  = DictionaryHelper(ui_locales, disc_ui_locales)
    return ddh, idh, dh


def try_to_contact(request, name, email, phone, content, ui_locales, recaptcha):
    """

    :param request:
    :param name:
    :param email:
    :param phone:
    :param content:
    :param ui_locales:
    :param spamanswer:
    :return:
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

    :param request:
    :param nickname:
    :param password:
    :param for_api:
    :param keep_login:
    :param _tn:
    :return:
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

    db_user = get_user_by_case_insensitive_nickname(nickname)
    if not db_user:  # check if the user exists
        logger('ViewHelper', 'user_login', 'user \'' + nickname + '\' does not exists')
        success = False
        is_ldap = is_usage_with_ldap(request)

        # if the user does not exists and we are using LDAP, we'll grep the user
        if is_ldap:
            success, db_user = catch_user_from_ldap(request, nickname, password, _tn)

        if not success:
            error = _tn.get(_.userPasswordNotMatch)
            return error

    elif not db_user.validate_password(password):  # check password
        logger('ViewHelper', 'user_login', 'wrong password')
        error = _tn.get(_.userPasswordNotMatch)
        return error

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

    if for_api:
        logger('ViewHelper', 'user_login', 'return for api: success')
        return {'status': 'success'}
    else:
        logger('ViewHelper', 'user_login', 'return success: ' + url)
        sleep(0.5)
        return HTTPFound(
            location=url,
            headers=headers,
        )


def catch_user_from_ldap(request, nickname, password, _tn):
    """

    :param nickname:
    :param password:
    :return:
    """
    import ldap

    try:
        r = request.registry.settings
        server    = r['settings:ldap:server']
        base      = r['settings:ldap:base']
        scope     = r['settings:ldap:account.scope']
        filter    = r['settings:ldap:account.filter']
        firstname = r['settings:ldap:account.firstname']
        lastname  = r['settings:ldap:account.lastname']
        title     = r['settings:ldap:account.title']
        email     = r['settings:ldap:account.email']
        logger('ViewHelper', 'catch_user_from_ldap', 'parsed data')

        logger('ViewHelper', 'catch_user_from_ldap', 'ldap.initialize(\'' + server + '\')')
        l = ldap.initialize(server)
        l.set_option(ldap.OPT_NETWORK_TIMEOUT, 5.0)
        logger('ViewHelper', 'catch_user_from_ldap', 'simple_bind_s(\'' + nickname + scope + '\', \'***\')')
        l.simple_bind_s(nickname + scope, password)
        logger('ViewHelper', 'catch_user_from_ldap', 'l.search_s(' + base + ', ldap.SCOPE_SUBTREE, (\'' + filter + '=' + nickname + '\'))[0][1]')
        user = l.search_s(base, ldap.SCOPE_SUBTREE, (filter + '=' + nickname))[0][1]

        firstname = user[firstname][0].decode('utf-8')
        lastname = user[lastname][0].decode('utf-8')
        title = user[title][0].decode('utf-8')
        gender = 'm' if 'Herr' in title else 'f' if 'Frau' in title else 'n'
        email = user[email][0].decode('utf-8')

        # getting the authors group
        db_group = DBDiscussionSession.query(Group).filter_by(name="authors").first()

        # does the group exists?
        if not db_group:
            info = _tn.get(_.errorTryLateOrContant)
            logger('ViewHelper', 'user_ldap_login', 'Internal error occured')
            return False, info

        success, info = UserHandler.create_new_user(request, firstname, lastname, email, nickname, password, gender, db_group.uid, _tn.get_lang())

        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        if db_user:
            return success, db_user

        logger('ViewHelper', 'user_ldap_login', 'new user not found in db')
        return False, _tn.get(_.errorTryLateOrContant)

    except ldap.INVALID_CREDENTIALS:
        logger('ViewHelper', 'user_ldap_login', 'ldap credential error')
        return False, None

    except ldap.SERVER_DOWN:
        logger('ViewHelper', 'user_ldap_login', 'can\'t reach server within 5s')
        return False, None


def try_to_register_new_user_via_ajax(request, ui_locales):
    """

    :param request:
    :param ui_locales:
    :return:
    """
    success = ''
    _t = Translator(ui_locales)
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

    # database queries mail verification
    db_nick1 = get_user_by_case_insensitive_nickname(nickname)
    db_nick2 = DBDiscussionSession.query(User).filter_by(public_nickname=nickname).first()
    db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
    is_mail_valid = validate_email(email, check_mx=True)

    # are the password equal?
    if not password == passwordconfirm:
        logger('ViewHelper', 'user_registration', 'Passwords are not equal')
        info = _t.get(_.pwdNotEqual)
    # is the nick already taken?
    elif db_nick1 or db_nick2:
        logger('ViewHelper', 'user_registration', 'Nickname \'' + nickname + '\' is taken')
        info = _t.get(_.nickIsTaken)
    # is the email already taken?
    elif db_mail:
        logger('ViewHelper', 'user_registration', 'E-Mail \'' + email + '\' is taken')
        info = _t.get(_.mailIsTaken)
    # is the email valid?
    elif not is_mail_valid:
        logger('ViewHelper', 'user_registration', 'E-Mail \'' + email + '\' is not valid')
        info = _t.get(_.mailNotValid)
    # is anti-spam correct?
    elif not is_human or error:
        logger('ViewHelper', 'user_registration', 'recaptcha error')
        info = _t.get(_.maliciousAntiSpam)
    # lets go
    else:
        # getting the authors group
        db_group = DBDiscussionSession.query(Group).filter_by(name="authors").first()

        # does the group exists?
        if not db_group:
            info = _t.get(_.errorTryLateOrContant)
            logger('ViewHelper', 'user_registration', 'Error occured')
        else:
            success, info = UserHandler.create_new_user(request, firstname, lastname, email, nickname,
                                                        password, gender, db_group.uid, ui_locales)
    return success, info


def request_password(request, ui_locales):
    """

    :param request:
    :param ui_locales:
    :return:
    """
    success = ''
    error = ''
    info = ''

    _t = Translator(ui_locales)
    email = escape_string(request.params['email'])
    db_user = DBDiscussionSession.query(User).filter_by(email=email).first()

    # does the user exists?
    if db_user:
        # get password and hashed password
        pwd = PasswordHandler.get_rnd_passwd()
        hashedpwd = PasswordHandler.get_hashed_password(pwd)

        # set the hashed one
        db_user.password = hashedpwd
        DBDiscussionSession.add(db_user)
        transaction.commit()

        db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
        db_language = DBDiscussionSession.query(Language).get(db_settings.lang_uid)

        body = _t.get(_.nicknameIs) + db_user.nickname + '\n'
        body += _t.get(_.newPwdIs) + pwd
        subject = _t.get(_.dbasPwdRequest)
        reg_success, message = EmailHelper.send_mail(request, subject, body, email, db_language.ui_locales)

        if reg_success:
            success = message
        else:
            error = message
    else:
        logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
        info = _t.get(_.emailUnknown)

    return success, error, info
