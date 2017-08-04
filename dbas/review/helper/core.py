import json
import dbas.review.helper.flags as review_flag_helper
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.main as review_main_helper
import dbas.review.helper.queues as review_queue_helper

from dbas.logger import logger
from dbas.input_validator import is_integer
from dbas.lib import get_discussion_language, is_user_author_or_admin
from dbas.helper.query import revoke_content
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from webhook.lib import send_request_for_recent_delete_review_to_socketio, get_port,\
    send_request_for_recent_edit_review_to_socketio, send_request_for_recent_optimization_review_to_socketio


def flag(uid, reason, extra_uid, is_argument, nickname, ui_locales) -> dict:
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
    logger('additives', 'flag_argument_or_statement', 'uid {}'.format(uid))
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


def delete_argument(request) -> dict:
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
            nickname = request.authenticated_userid
            main_page = request.application_url
            port = get_port(request)
            send_request_for_recent_delete_review_to_socketio(nickname, main_page, port)

    prepared_dict = {'error': error}
    return prepared_dict


def edit_argument(request) -> dict:
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
            nickname = request.authenticated_userid
            main_page = request.application_url
            port = get_port(request)
            send_request_for_recent_edit_review_to_socketio(nickname, main_page, port)

    prepared_dict = {'error': error}
    return prepared_dict


def duplicate_statement(request) -> dict:
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
            nickname = request.authenticated_userid
            main_page = request.application_url
            port = get_port(request)
            send_request_for_recent_edit_review_to_socketio(nickname, main_page, port)

    prepared_dict = {'error': error}
    return prepared_dict


def optimization_argument(request) -> dict:
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
            nickname = request.authenticated_userid
            main_page = request.application_url
            port = get_port(request)
            send_request_for_recent_optimization_review_to_socketio(nickname, main_page, port)

    prepared_dict = {'error': error}
    return prepared_dict


def undo(request) -> dict:
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


def cancel(request) -> dict:
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


def lock(request) -> dict:
    """
    Tries to lock an optimization element, so the user can propose an edit

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error, success, info key
    """
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)
    prepared_dict = dict()

    review_uid = request.params['review_uid'] if 'review_uid' in request.params else None
    lock = True if request.params['lock'] == 'true' else False

    if not is_integer(review_uid):
        info = ''
        success = ''
        error = _t.get(_.internalKeyError)
        is_locked = False
    else:
        if lock:
            success, info, error, is_locked = review_queue_helper.lock_optimization_review(request.authenticated_userid, review_uid, _t)
        else:
            review_queue_helper.unlock_optimization_review(review_uid)
            is_locked = False
            success = _t.get(_.dataUnlocked)
            error = ''
            info = ''

    prepared_dict['info'] = info
    prepared_dict['error'] = error
    prepared_dict['success'] = success
    prepared_dict['is_locked'] = is_locked

    return prepared_dict


def revoke(request) -> dict:
    """
    Tries to revoke content from an review element

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error success key
    """

    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)
    uid = request.params['uid'] if 'uid' in request.params else None

    is_argument = True if request.params['is_argument'] == 'true' else False

    if not is_integer(uid):
        logger('additives', 'undo_review', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
        success = False
    else:
        error, success = revoke_content(uid, is_argument, request.authenticated_userid, _t)

    prepared_dict = dict()
    prepared_dict['error'] = error
    prepared_dict['success'] = success

    return prepared_dict
