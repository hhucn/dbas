import json
import transaction
import dbas.review.helper.flags as review_flag_helper
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.main as review_main_helper

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import sql_timestamp_pretty_print, User, Settings, Language
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.logger import logger
from dbas.helper.language import get_language_from_cookie
from dbas.helper.notification import send_notification
from dbas.input_validator import is_integer
from dbas.lib import get_user_by_private_or_public_nickname, get_profile_picture, get_discussion_language, is_user_author_or_admin
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_recent_delete_review_to_socketio,\
    send_request_for_recent_edit_review_to_socketio, send_request_for_recent_optimization_review_to_socketio


def set_user_language(nickname, ui_locales) -> dict:
    """
    Changes the users language of the web frontend

    :param nickname: the user's nickname creating the request
    :param ui_locales: current ui_locales
    :rtype: dict
    :return: prepared collection with status information
    """
    _tn = Translator(ui_locales)
    error = ''
    current_lang = ''

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
        if db_settings:
            db_language = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
            if db_language:
                current_lang = db_language.name
                db_settings.set_lang_uid(db_language.uid)
                transaction.commit()
            else:
                error = _tn.get(_.internalError)
        else:
            error = _tn.get(_.checkNickname)
    else:
        error = _tn.get(_.checkNickname)

    prepared_dict = {}
    prepared_dict['error'] = error
    prepared_dict['ui_locales'] = ui_locales
    prepared_dict['current_lang'] = current_lang
    return prepared_dict


def send_some_notification(request) -> dict:
    """
    Send a notification from user a to user b

    :param request: pyramid's request object
    :rtype: dict
    :return: prepared collection with status information
    """
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)
    recipient = str(request.params['recipient']).replace('%20', ' ')
    title = request.params['title']
    text = request.params['text']
    error = ''
    ts = ''
    uid = ''
    gravatar = ''

    db_recipient = get_user_by_private_or_public_nickname(recipient)
    if len(title) < 5 or len(text) < 5:
        error = '{} ({}: 5)'.format(_tn.get(_.empty_notification_input), _tn.get(_.minLength))
    elif not db_recipient or recipient == 'admin' or recipient == nick_of_anonymous_user:
        error = _tn.get(_.recipientNotFound)
    else:
        db_author = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
        if not db_author:
            error = _tn.get(_.notLoggedIn)
        if db_author.uid == db_recipient.uid:
            error = _tn.get(_.senderReceiverSame)
        else:
            db_notification = send_notification(request, db_author, db_recipient, title, text, request.application_url)
            uid = db_notification.uid
            ts = sql_timestamp_pretty_print(db_notification.timestamp, ui_locales)
            gravatar = get_profile_picture(db_recipient, 20)

    prepared_dict = {}
    prepared_dict['error'] = error
    prepared_dict['timestamp'] = ts
    prepared_dict['uid'] = uid
    prepared_dict['recipient_avatar'] = gravatar
    return prepared_dict


def flag_argument_or_statement(uid, reason, extra_uid, is_argument, nickname, ui_locales) -> dict:
    """
    Flags and argument or statement for the review system

    :param uid: ID of the argument of statement, which should be flagged
    :param reason: Reason, why the id should be flagged
    :param extra_uid: Statement.id if the reason is a duplicate, otherwise none
    :param is_argument: Boolean if the uid for is an argument
    :param nickname: the user's nickname creating the request
    :param ui_locales: current ui_locales
    :rtype: dict
    :return: collection with success, info and error key
    """
    _t = Translator(ui_locales)

    if not is_integer(uid):
        logger('additives', 'flag_argument_or_statement', 'invalid uid', error=True)
        return {'error': _t.get(_.internalError), 'info': '', 'success': ''}
    else:
        success, info, error = review_flag_helper.flag_element(uid, reason, nickname, is_argument, extra_uid)
        prepared_dict = {}
        prepared_dict['success'] = '' if isinstance(success, str) else _t.get(success)
        prepared_dict['info'] = '' if isinstance(info, str) else _t.get(info)
        prepared_dict['error'] = '' if isinstance(error, str) else _t.get(error)

    return prepared_dict


def review_delete_argument(request) -> dict:
    """
    Sets feedback for an review element of the delete-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    review_uid = request.params['review_uid'] if 'review_uid' in request.params else None
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    if not is_integer(review_uid):
        logger('additives', 'review_delete_argument', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
    else:
        error = review_main_helper.add_review_opinion_for_delete(request, review_uid, _t)
        if len(error) == 0:
            send_request_for_recent_delete_review_to_socketio(request)

    prepared_dict = {'error': error}
    return prepared_dict


def review_edit_argument(request) -> dict:
    """
    Sets feedback for an review element of the edit-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    review_uid = request.params['review_uid'] if 'review_uid' in request.params else None
    is_edit_okay = True if str(request.params['is_edit_okay']) == 'true' else False
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    if not is_integer(review_uid):
        logger('additives', 'review_edit_argument', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
    else:
        error = review_main_helper.add_review_opinion_for_edit(request, is_edit_okay, review_uid, _t)
        if len(error) == 0:
            send_request_for_recent_edit_review_to_socketio(request)

    prepared_dict = {'error': error}
    return prepared_dict


def review_duplicate_statement(request) -> dict:
    """
    Sets feedback for an review element of the duplicate-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    is_duplicate = True if str(request.params['is_duplicate']) == 'true' else False
    review_uid = request.params['review_uid']
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    if not is_integer(review_uid):
        logger('additives', 'review_duplicate_statement', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
    else:
        error = review_main_helper.add_review_opinion_for_duplicate(request, is_duplicate, review_uid, _t)
        if len(error) == 0:
            send_request_for_recent_edit_review_to_socketio(request)

    prepared_dict = {'error': error}
    return prepared_dict


def review_optimization_argument(request) -> dict:
    """
    Sets feedback for an review element of the optimization-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    should_optimized = True if str(request.params['should_optimized']) == 'true' else False
    review_uid = request.params['review_uid'] if 'review_uid' in request.params else None
    new_data = json.loads(request.params['new_data']) if 'new_data' in request.params else None

    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    if not is_integer(review_uid):
        logger('additives', 'review_optimization_argument', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
    else:
        error = review_main_helper.add_review_opinion_for_optimization(request, should_optimized, review_uid, new_data, _t)
        if len(error) == 0:
            send_request_for_recent_optimization_review_to_socketio(request)

    prepared_dict = {'error': error}
    return prepared_dict


def undo_review(request) -> dict:
    """
    Tries to undo a review process.

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error, success, info key
    """
    uid = request.params['uid']
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    if not is_integer(uid):
        logger('additives', 'undo_review', 'invalid uid', error=True)
        return {'error': _t.get(_.internalKeyError)}

    prepared_dict = {}
    nickname = request.authenticated_userid
    queue = request.params['queue']
    if is_user_author_or_admin(nickname):
        success, error = review_history_helper.revoke_old_decision(queue, uid, ui_locales, nickname)
        prepared_dict['success'] = success
        prepared_dict['error'] = error
    else:
        prepared_dict['info'] = _t.get(_.justLookDontTouch)

    return prepared_dict


def cancel_review(request) -> dict:
    """
    Tries to cancel a review process.

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    uid = request.params['uid']
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    if not is_integer(uid):
        logger('additives', 'cancel_review', 'invalid uid', error=True)
        return {'error': _t.get(_.internalKeyError)}

    prepared_dict = {}
    nickname = request.authenticated_userid
    queue = request.params['queue']
    if is_user_author_or_admin(nickname):
        success, error = review_history_helper.cancel_ongoing_decision(queue, uid, ui_locales, nickname)
        prepared_dict['success'] = success
        prepared_dict['error'] = error
    else:
        prepared_dict['info'] = _t.get(_.justLookDontTouch)

    return prepared_dict


def review_lock(request) -> dict:
    """
    Sets feedback for an review element of the optimization-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    prepared_dict = {}

    if not is_integer(uid):
        logger('additives', 'undo_review', 'invalid uid', error=True)
        return {'error': _t.get(_.internalKeyError)}

    return prepared_dict


def revoke_some_content(request) -> dict:
    """
    Sets feedback for an review element of the optimization-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    prepared_dict = {}

    if not is_integer(uid):
        logger('additives', 'undo_review', 'invalid uid', error=True)
        return {'error': _t.get(_.internalKeyError)}

    return prepared_dict
