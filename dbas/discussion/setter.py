import transaction
import json

import dbas.helper.issue as issue_helper
import dbas.review.helper.queues as review_queue_helper
from dbas import user_management as user_manager
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import sql_timestamp_pretty_print, User, Settings, Language, Issue, Message
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.helper.language import get_language_from_cookie
from dbas.helper.notification import send_notification, count_of_new_notifications, get_box_for
from dbas.helper.query import insert_as_statements, process_input_of_start_premises_and_receive_url, \
    process_input_of_premises_for_arguments_and_receive_url, process_seen_statements,\
    mark_or_unmark_statement_or_argument, get_text_for_justification_or_reaction_bubble
from dbas.lib import get_user_by_private_or_public_nickname, get_profile_picture, get_discussion_language, escape_string
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_position,\
    rep_reason_first_justification, rep_reason_new_statement, rep_reason_first_new_argument
from dbas.url_manager import UrlManager
from websocket.lib import send_request_for_info_popup_to_socketio


def user_language(nickname, ui_locales) -> dict:
    """
    Changes the users language of the web frontend

    :param nickname: the user's nickname creating the request
    :param ui_locales: current ui_locales
    :rtype: dict
    :return: prepared collection with status information
    """
    _tn = Translator(ui_locales)

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return {'error': _tn.get(_.checkNickname), 'ui_locales': ui_locales, 'current_lang': ''}

    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    if not db_settings:
        return {'error': _tn.get(_.checkNickname), 'ui_locales': ui_locales, 'current_lang': ''}

    db_language = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
    if not db_language:
        return {'error': _tn.get(_.internalError), 'ui_locales': ui_locales, 'current_lang': ''}

    current_lang = db_language.name
    db_settings.set_lang_uid(db_language.uid)
    transaction.commit()

    return {'error': '', 'ui_locales': ui_locales, 'current_lang': current_lang}


def notification(request, recipient, title , text, nickname, ui_locales) -> dict:
    """
    Send a notification from user a to user b

    :param request: pyramid's request object
    :üaram recipient: Nickname of the recipient
    :üaram title: Title of the notification
    :üaram text: Text of the notification
    :üaram nickname: Users nickname
    :üaram ui_locales: Current used language
    :rtype: dict
    :return: prepared collection with status information
    """
    _tn = Translator(ui_locales)

    db_recipient = get_user_by_private_or_public_nickname(recipient)
    if len(title) < 5 or len(text) < 5:
        error = '{} ({}: 5)'.format(_tn.get(_.empty_notification_input), _tn.get(_.minLength))
        prepared_dict = {'error': error, 'timestamp': '', 'uid': '', 'recipient_avatar': ''}
        return prepared_dict

    if not db_recipient or recipient == 'admin' or recipient == nick_of_anonymous_user:
        error = _tn.get(_.recipientNotFound)
        prepared_dict = {'error': error, 'timestamp': '', 'uid': '', 'recipient_avatar': ''}
        return prepared_dict

    db_author = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_author:
        error = _tn.get(_.notLoggedIn)
        prepared_dict = {'error': error, 'timestamp': '', 'uid': '', 'recipient_avatar': ''}
        return prepared_dict

    if db_author.uid == db_recipient.uid:
        error = _tn.get(_.senderReceiverSame)
        prepared_dict = {'error': error, 'timestamp': '', 'uid': '', 'recipient_avatar': ''}
        return prepared_dict

    else:
        db_notification = send_notification(request, db_author, db_recipient, title, text, nickname)
        uid = db_notification.uid
        ts = sql_timestamp_pretty_print(db_notification.timestamp, ui_locales)
        gravatar = get_profile_picture(db_recipient, 20)

    prepared_dict = {}
    prepared_dict['error'] = ''
    prepared_dict['timestamp'] = ts
    prepared_dict['uid'] = uid
    prepared_dict['recipient_avatar'] = gravatar
    return prepared_dict


def position(request, for_api, api_data) -> dict:
    """
    Set new position for current discussion and returns collection with the next url for the discussion.

    :param request: pyramid's request object
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: Prepared collection with statement_uids of the new positions and next url or an error
    """
    discussion_lang = get_discussion_language(request)
    _tn = Translator(discussion_lang)
    prepared_dict = dict()
    prepared_dict['error'] = ''
    prepared_dict['statement_uids'] = []

    try:
        if for_api and api_data:
            nickname = api_data["nickname"]
            statement = api_data["statement"]
            issue = api_data["issue_id"]
            slug = api_data["slug"]
        else:
            nickname = request.authenticated_userid
            statement = request.params['statement']
            issue = issue_helper.get_issue_id(request)
            slug = DBDiscussionSession.query(Issue).get(issue).get_slug()

    except KeyError as e:
        logger('setter', 'set_new_start_statement', repr(e), error=True)
        prepared_dict['error'] = _tn.get(_.notInsertedErrorBecauseInternal)
        return prepared_dict

    # escaping will be done in QueryHelper().set_statement(...)
    user_manager.update_last_action(nickname)
    new_statement = insert_as_statements(request, statement, nickname, issue, discussion_lang, is_start=True)

    if new_statement == -1:
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = _tn.get(_.eachStatement)
        error = '{} ({}: {} {})'.format(a, b, 10, c)
        prepared_dict['error'] = error
    elif new_statement == -2:
        prepared_dict['error'] = _tn.get(_.noRights)
    else:
        url = UrlManager(request.application_url, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
        prepared_dict['url'] = url
        prepared_dict['statement_uids'].append(new_statement[0].uid)

        # add reputation
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_position)
        if not add_rep:
            add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
            # send message if the user is now able to review
        if broke_limit:
            url += '#access-review'
            prepared_dict['url'] = url

    return prepared_dict


def positions_premise(request, for_api, api_data) -> dict:
    """
    Set new premise for a given position and returns dictionary with url for the next step of the discussion

    :param request: pyramid's request object
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    prepared_dict = dict()
    lang = get_discussion_language(request)
    _tn = Translator(lang)
    try:
        if for_api and api_data:
            nickname = api_data['nickname']
            premisegroups = api_data['statement']
            issue = api_data['issue_id']
            conclusion_id = api_data['conclusion_id']
            supportive = api_data['supportive']
        else:
            nickname = request.authenticated_userid
            issue = issue_helper.get_issue_id(request)
            premisegroups = json.loads(request.params['premisegroups'])
            conclusion_id = request.params['conclusion_id']
            supportive = True if request.params['supportive'].lower() == 'true' else False
    except KeyError as e:
        logger('setter', 'set_new_start_premise', repr(e), error=True)
        prepared_dict['error'] = _tn.get(_.notInsertedErrorBecauseInternal)
        return prepared_dict

    # escaping will be done in QueryHelper().set_statement(...)
    user_manager.update_last_action(nickname)

    url, statement_uids, error = process_input_of_start_premises_and_receive_url(request, premisegroups, conclusion_id,
                                                                                 supportive, issue, nickname, for_api,
                                                                                 request.application_url, lang)

    prepared_dict['error'] = error
    prepared_dict['statement_uids'] = statement_uids

    # add reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_justification)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        ui_locales = get_language_from_cookie(request)
        _t = Translator(ui_locales)
        send_request_for_info_popup_to_socketio(request, _t.get(_.youAreAbleToReviewNow),  request.application_url + '/review')
        prepared_dict['url'] = str(url) + str('#access-review')

    if url == -1:
        return prepared_dict

    prepared_dict['url'] = url

    return prepared_dict


def arguments_premises(request, for_api, api_data) -> dict:
    """
    Set new premise for a given conclusion and returns dictionary with url for the next step of the discussion

    :param request: pyramid's request object
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :rtype: dict
    :return: Prepared collection with statement_uids of the new premises and next url or an error
    """
    prepared_dict = dict()
    lang = get_language_from_cookie(request)
    _tn = Translator(lang)

    try:
        if for_api and api_data:
            nickname      = api_data['nickname']
            premisegroups = api_data['statement']
            issue         = api_data['issue_id']
            arg_uid       = api_data['arg_uid']
            attack_type   = api_data['attack_type']
        else:
            nickname = request.authenticated_userid
            premisegroups = json.loads(request.params['premisegroups'])
            issue = issue_helper.get_issue_id(request)
            arg_uid = request.params['arg_uid']
            attack_type = request.params['attack_type']

    except KeyError as e:
        logger('setter', 'set_new_premises_for_argument', repr(e), error=True)
        prepared_dict['error'] = _tn.get(_.notInsertedErrorBecauseInternal)
        return prepared_dict

    # escaping will be done in QueryHelper().set_statement(...)
    discussion_lang = get_discussion_language(request)
    url, statement_uids, error = process_input_of_premises_for_arguments_and_receive_url(request, arg_uid, attack_type,
                                                                                         premisegroups, issue, nickname,
                                                                                         for_api,
                                                                                         request.application_url,
                                                                                         discussion_lang)
    user_manager.update_last_action(nickname)

    prepared_dict['error'] = error
    prepared_dict['statement_uids'] = statement_uids

    # add reputation
    add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_new_argument)
    if not add_rep:
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
        # send message if the user is now able to review
    if broke_limit:
        # send_request_for_info_popup_to_socketio(nickname, _t.get(_.youAreAbleToReviewNow), request.application_url + '/review')
        url += '#access-review'
        prepared_dict['url'] = url

    if url == -1:
        return prepared_dict

    prepared_dict['url'] = url

    logger('setter', 'set_new_premises_for_argument', 'returning {}'.format(prepared_dict))
    return prepared_dict


def correction_of_statement(request) -> dict:
    """
    Adds a proposol for a statements correction and returns info if the proposal could be set

    :param request: pyramid's request object
    :rtype: dict
    :return: Dictionary with info and/or error
    """
    prepared_dict = dict()
    nickname = request.authenticated_userid
    user_manager.update_last_action(nickname)

    _tn = Translator(get_language_from_cookie(request))
    try:
        elements = json.loads(request.params['elements'])
        msg, error = review_queue_helper.add_proposals_for_statement_corrections(elements, nickname, _tn)
        prepared_dict['error'] = msg if error else ''
        prepared_dict['info'] = msg if len(msg) > 0 else ''
    except KeyError as e:
        prepared_dict['error'] = _tn.get(_.internalError)
        prepared_dict['info'] = ''
        logger('setter', 'set_correction_of_statement', repr(e), error=True)

    return prepared_dict


def notification_read(request) -> dict:
    """
    Simply marks a notification as read

    :param request: pyramid's request object
    :rtype: dict
    :return: Dictionary with info and/or error
    """
    prepared_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)
    request_authenticated_userid = request.authenticated_userid
    user_manager.update_last_action(request_authenticated_userid)

    try:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=request_authenticated_userid).first()
        if db_user:
            DBDiscussionSession.query(Message).filter(and_(Message.uid == request.params['id'],
                                                           Message.to_author_uid == db_user.uid,
                                                           Message.is_inbox == True)).first().set_read(True)
            transaction.commit()
            prepared_dict['unread_messages'] = count_of_new_notifications(request_authenticated_userid)
            prepared_dict['error'] = ''
        else:
            prepared_dict['error'] = _t.get(_.noRights)
    except KeyError as e:
        logger('setter', 'set_message_read', repr(e), error=True)
        prepared_dict['error'] = _t.get(_.internalKeyError)

    return prepared_dict


def notification_delete(request) -> dict:
    """
    Simply deletes a specific notification

    :param request: pyramid's request object
    :rtype: dict
    :return: Dictionary with info and/or error
    """
    prepared_dict = dict()

    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)
    request_authenticated_userid = request.authenticated_userid
    user_manager.update_last_action(request_authenticated_userid)

    try:
        uid = request.params['id']
    except KeyError as e:
        logger('setter', 'set_notification_delete', repr(e), error=True)
        prepared_dict['error'] = _t.get(_.internalKeyError)
        prepared_dict['success'] = ''
        return prepared_dict

    db_user = DBDiscussionSession.query(User).filter_by(nickname=request_authenticated_userid).first()
    if not db_user:
        prepared_dict['error'] = _t.get(_.noRights)
        prepared_dict['success'] = ''
        return prepared_dict

    # inbox
    DBDiscussionSession.query(Message).filter(and_(Message.uid == uid,
                                                   Message.to_author_uid == db_user.uid,
                                                   Message.is_inbox == True)).delete()
    # send
    DBDiscussionSession.query(Message).filter(and_(Message.uid == uid,
                                                   Message.from_author_uid == db_user.uid,
                                                   Message.is_inbox == False)).delete()
    transaction.commit()
    prepared_dict['unread_messages'] = count_of_new_notifications(request_authenticated_userid)
    prepared_dict['total_in_messages'] = str(len(get_box_for(request_authenticated_userid, ui_locales, request.application_url, True)))
    prepared_dict['total_out_messages'] = str(len(get_box_for(request_authenticated_userid, ui_locales, request.application_url, False)))
    prepared_dict['error'] = ''
    prepared_dict['success'] = _t.get(_.messageDeleted)

    return prepared_dict


def issue(nickname, info, long_info, title, lang, application_url, ui_locales) -> dict:
    """
    Sets new issue, which will be a new discussion

    :param nickname: Users nickname
    :param info: Short information about the new issue
    :param long_info: Long information about the new issue
    :param title: Title of the new issue
    :param lang: Language of the new issue
    :param application_url: Url of the app itself
    :param ui_locales: Current language
    :rtype: dict
    :return: Collection with information about the new issue
    """
    user_manager.update_last_action(nickname)

    logger('setter', 'set_new_issue', 'main')
    prepared_dict = dict()

    was_set, error = issue_helper.set_issue(info, long_info, title, lang, nickname, ui_locales)
    if was_set:
        db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
                                                                Issue.info == info)).first()
        prepared_dict['issue'] = issue_helper.get_issue_dict_for(db_issue, application_url, False, 0, ui_locales)
    prepared_dict['error'] = '' if was_set else error

    return prepared_dict


def seen_statements(uids, path, nickname, ui_locales) -> dict:
    """
    Marks several statements as already seen.

    :param uids: Uids of statements which should be marked as seen
    :param path: Current path of the user
    :param nickname: Users nickname
    :param ui_locales: Current language
    :rtype: dict
    :return: Dictionary with an error field
    """
    # are the statements connected to an argument?
    additional_argument = None
    _tn = Translator(ui_locales)
    if 'justify' in path:
        url = path[path.index('justify/') + len('justify/'):]
        additional_argument = int(url[:url.index('/')])

    errorCode = process_seen_statements(uids, nickname, additional_argument=additional_argument)
    error = _tn.get(errorCode) if len(errorCode) > 0 else ''
    return {'error': error}


def mark_statement_or_argument(uid, step, is_argument, is_supportive, should_mark, history, ui_locales, nickname) -> dict:
    """
    Marks statement or argument as current users opinion and returns status about the action

    :param uid: ID of statement or argument
    :param step: kind of step in current discussion
    :param is_argument: Boolean if the id is for an argument
    :param is_supportive: Boolean if the mark is supportive
    :param should_mark: Boolean if it should be (un-)marked
    :param history: Users history
    :param ui_locales: Current language
    :param nickname: Users nickname
    :rtype: dict
    :return: Dictionary with new text for the current bubble, where the user marked her opinion
    """
    prepared_dict = dict()
    _t = Translator(ui_locales)

    success, error = mark_or_unmark_statement_or_argument(uid, is_argument, should_mark, nickname, _t)
    prepared_dict['success'] = success
    prepared_dict['error'] = error
    prepared_dict['text'] = get_text_for_justification_or_reaction_bubble(uid, is_argument, is_supportive,
                                                                          nickname, step, history, _t)
    return prepared_dict
