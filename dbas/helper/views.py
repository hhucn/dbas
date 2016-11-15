"""
Helper for D-BAS Views

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Settings, Language
from dbas.logger import logger
from dbas.lib import get_text_for_statement_uid, get_discussion_language, escape_string, get_user_by_case_insensitive_nickname
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import is_integer
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _
from validate_email import validate_email

import dbas.recommender_system as RecommenderSystem
import dbas.helper.email as EmailHelper
import dbas.helper.history as HistoryHelper
import dbas.helper.issue as IssueHelper
import dbas.user_management as UserHandler
import dbas.handler.password as PasswordHandler
import dbas.helper.voting as VotingHelper
import transaction


def get_nickname_and_session(request, for_api=None, api_data=None):
    """
    Given data from api, return nickname and session_id.

    :param for_api:
    :param api_data:
    :return:
    """
    nickname = api_data["nickname"] if api_data and for_api else request.authenticated_userid
    session_id = api_data["session_id"] if api_data and for_api else request.session.id
    return nickname, session_id


def preparation_for_view(for_api, api_data, request):
    """
    Does some elementary things like: getting nickname, sessioniod and history. Additionally boolean, if the sesseion is expired

    :param for_api: True, if the values are for the api
    :param api_data: Array with api data
    :param request: Current request
    :return: nickname, session_id, session_expired, history
    """
    nickname, session_id = get_nickname_and_session(request, for_api, api_data)
    session_expired = UserHandler.update_last_action(nickname)
    history         = request.params['history'] if 'history' in request.params else ''
    HistoryHelper.save_path_in_database(nickname, request.path)
    HistoryHelper.save_history_in_cookie(request, request.path, history)
    return nickname, session_id, session_expired, history


def preparation_for_justify_statement(request, for_api, api_data, main_page, slug, statement_or_arg_id, supportive, mode, ui_locales):
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
    logger('View Helper', 'preparation_for_justify_statement', 'main')

    nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, request)
    logged_in = UserHandler.is_user_logged_in(nickname)
    _ddh, _idh, _dh = __prepare_helper(ui_locales, session_id, nickname, history, main_page, slug, for_api, request)

    VotingHelper.add_vote_for_statement(statement_or_arg_id, nickname, supportive)

    item_dict       = _idh.get_array_for_justify_statement(statement_or_arg_id, nickname, supportive)
    discussion_dict = _ddh.get_dict_for_justify_statement(statement_or_arg_id, main_page, slug, supportive, len(item_dict['elements']), nickname)
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request, mode == 't',
                                              application_url=main_page, for_api=for_api)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0 or len(item_dict['elements']) == 1 and logged_in:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify=True,
                                    current_premise=get_text_for_statement_uid(statement_or_arg_id),
                                    supportive=supportive)
    return item_dict, discussion_dict, extras_dict


def preparation_for_dont_know_statement(request, for_api, api_data, main_page, slug, statement_or_arg_id, supportive, ui_locales):
    """

    :param request:
    :param for_api:
    :param api_data:
    :param main_page:
    :param slug:
    :param statement_or_arg_id:
    :param supportive:
    :param ui_locales:
    :return:
    """
    logger('View Helper', 'preparation_for_dont_know_statement', 'main')

    nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, request)

    issue               = IssueHelper.get_id_of_slug(slug, request, True) if len(slug) > 0 else IssueHelper.get_issue_id(request)
    disc_ui_locales     = get_discussion_language(request, issue)
    _ddh                = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, main_page=main_page, slug=slug)
    _idh                = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=request.path, history=history)
    _dh                 = DictionaryHelper(ui_locales, disc_ui_locales)

    # dont know
    argument_uid    = RecommenderSystem.get_argument_by_conclusion(statement_or_arg_id, supportive)
    discussion_dict = _ddh.get_dict_for_dont_know_reaction(argument_uid)
    item_dict       = _idh.get_array_for_dont_know_reaction(argument_uid, supportive, nickname)
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request, argument_id=argument_uid,
                                              application_url=main_page, for_api=for_api)
    # is the discussion at the end?
    if len(item_dict['elements']) == 0:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_dont_know=True,
                                    current_premise=get_text_for_statement_uid(statement_or_arg_id))
    return item_dict, discussion_dict, extras_dict


def preparation_for_justify_argument(request, for_api, api_data, main_page, slug, statement_or_arg_id, supportive, relation, ui_locales):
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

    nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, request)
    logged_in = UserHandler.is_user_logged_in(nickname)
    _ddh, _idh, _dh = __prepare_helper(ui_locales, session_id, nickname, history, main_page, slug, for_api, request)

    # justifying argument
    # is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
    item_dict       = _idh.get_array_for_justify_argument(statement_or_arg_id, relation, logged_in, nickname)
    discussion_dict = _ddh.get_dict_for_justify_argument(statement_or_arg_id, supportive, relation)
    extras_dict     = _dh.prepare_extras_dict(slug, False, True, False, True, request,
                                              argument_id=statement_or_arg_id, application_url=main_page, for_api=for_api)
    # is the discussion at the end?
    if not logged_in and len(item_dict['elements']) == 1 or logged_in and len(item_dict['elements']) == 1:
        _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify_argumentation=True)

    return item_dict, discussion_dict, extras_dict


def __prepare_helper(ui_locales, session_id, nickname, history, main_page, slug, for_api, request):
    """

    :param ui_locales:
    :param session_id:
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
    ddh = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, main_page=main_page, slug=slug)
    idh = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=request.path, history=history)
    dh  = DictionaryHelper(ui_locales, disc_ui_locales)
    return ddh, idh, dh


def try_to_contact(request, username, email, phone, content, ui_locales, spamanswer):
    """

    :param request:
    :param username:
    :param email:
    :param phone:
    :param content:
    :param ui_locales:
    :param spamanswer:
    :return:
    """
    _t = Translator(ui_locales)
    send_message = False

    spamanswer = spamanswer if is_integer(spamanswer) else '#'
    key = 'contact-antispamanswer'
    antispamanswer = request.session[key] if key in request.session else ''
    spamsolution = int(antispamanswer) if len(antispamanswer) > 0 else '*#*'

    logger('ViewHelper', 'try_to_contact', 'validating email')
    is_mail_valid = validate_email(email, check_mx=True)

    # check for empty username
    if not username:
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
    elif str(spamanswer) != str(spamsolution):
        logger('ViewHelper', 'try_to_contact', 'empty or wrong anti-spam answer' + ', given answer ' +
               str(spamanswer) + ', right answer ' + str(antispamanswer))
        contact_error = True
        message = _t.get(_.maliciousAntiSpam)

    else:
        subject = _t.get(_.contact) + ' D-BAS'
        body = _t.get(_.name) + ': ' + username + '\n'
        body += _t.get(_.mail) + ': ' + email + '\n'
        body += _t.get(_.phone) + ': ' + phone + '\n'
        body += _t.get(_.message) + ':\n' + content
        EmailHelper.send_mail(request, subject, body, 'dbas.hhu@gmail.com', ui_locales)
        body = '* ' + _t.get(_.thisIsACopyOfMail).upper() + ' *\n\n' + body
        subject = '[D-BAS INFO] ' + subject
        send_message, message = EmailHelper.send_mail(request, subject, body, email, ui_locales)
        contact_error = not send_message

    return contact_error, message, send_message


def try_to_register_new_user_via_ajax(request, ui_locales):
    """

    :param request:
    :param ui_locales:
    :return:
    """
    success = ''
    _t = Translator(ui_locales)
    params = request.params
    firstname = escape_string(params['firstname'] if 'firstname' in params else '')
    lastname = escape_string(params['lastname'] if 'lastname' in params else '')
    nickname = escape_string(params['nickname'] if 'nickname' in params else '')
    email = escape_string(params['email'] if 'email' in params else '')
    gender = escape_string(params['gender'] if 'gender' in params else '')
    password = escape_string(params['password'] if 'password' in params else '')
    passwordconfirm = escape_string(params['passwordconfirm'] if 'passwordconfirm' in params else '')
    spamanswer = escape_string(params['spamanswer'] if 'spamanswer' in params else '')

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
        info = _.get(_.mailNotValid)
    # is anti-spam correct?
    elif str(spamanswer) != str(request.session['antispamanswer']):
        logger('ViewHelper', 'user_registration', 'Anti-Spam answer \'' + str(spamanswer) + '\' is not equal ' + str(
            request.session['antispamanswer']))
        info = _.get(_.maliciousAntiSpam)
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
    email = escape_string(request.params['email'] if 'email' in request.params else '')
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

        db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
        db_language = DBDiscussionSession.query(Language).filter_by(uid=db_settings.lang_uid).first()

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
