import json

from pyramid.httpexceptions import HTTPBadRequest

import dbas.review.helper.flags as review_flag_helper
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.main as review_main_helper
import dbas.review.helper.queues as review_queue_helper
from dbas.database.discussion_model import User, PremiseGroup

from dbas.logger import logger
from dbas.input_validator import is_integer
from dbas.lib import get_discussion_language, is_user_author_or_admin
from dbas.helper.query import revoke_content
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_recent_reviewer_socketio, get_port


def merge_or_split_statement(key: str, pgroup: PremiseGroup, text_values: list(), db_user: User, _tn: Translator) -> dict:
    """
    Adds review for splitting/merging a statement

    :param key: 'split' or 'merge'
    :param pgroup: PremiseGroup
    :param text_values: text values
    :param db_user: User
    :rtype: dict
    :return: collection with success, info and error key
    """
    if key not in ['merge', 'split']:
        raise HTTPBadRequest()
    return review_flag_helper.flag_statement_for_merge_or_split(key, pgroup, text_values, db_user, _tn)


def merge_or_split_premisegroup(key: str, pgroup: PremiseGroup, db_user: User, _tn: Translator) -> dict:
    """
    Adds review for splitting/merging a pgroup

    :param key: 'split' or 'merge'
    :param pgroup: PremiseGroup
    :param db_user: User
    :param ui_locales: current ui_locales
    :rtype: dict
    :return: collection with success, info and error key
    """
    if key not in ['merge', 'split']:
        raise HTTPBadRequest()
    return review_flag_helper.flag_pgroup_for_merge_or_split(key, pgroup, db_user, _tn)


def delete_argument(request) -> dict:
    """
    Sets feedback for an review element of the delete-queue

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    review_uid = request.params['review_uid'] if 'review_uid' in request.params else None
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
            send_request_for_recent_reviewer_socketio(nickname, main_page, port, 'deletes')

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
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
            send_request_for_recent_reviewer_socketio(nickname, main_page, port, 'edits')

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
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
            send_request_for_recent_reviewer_socketio(nickname, main_page, port, 'duplicates')

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

    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
            send_request_for_recent_reviewer_socketio(nickname, main_page, port, 'optimizations')

    prepared_dict = {'error': error}
    return prepared_dict


def split_premisegroup(request) -> dict:
    """
    Sets feedback for a review element of a splitted premisegroup

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _t = Translator(ui_locales)
    review_uid = request.params['review_uid']
    should_split = request.params['should_split']

    if not is_integer(review_uid):
        logger('additives', 'split_premisegroup', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
    else:
        error = review_main_helper.add_review_opinion_for_split(request, review_uid, should_split, _t)
        if len(error) == 0:
            nickname = request.authenticated_userid
            main_page = request.application_url
            port = get_port(request)
            send_request_for_recent_reviewer_socketio(nickname, main_page, port, 'splits')

    prepared_dict = {'error': error}
    return prepared_dict


def merge_premisegroup(request) -> dict:
    """
    Sets feedback for a review element of a merged premisegroup

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _t = Translator(ui_locales)
    review_uid = request.params['review_uid']
    should_merge = request.params['should_merge']

    if not is_integer(review_uid):
        logger('additives', 'merge_premisegroup', 'invalid uid', error=True)
        error = _t.get(_.internalKeyError)
    else:
        error = review_main_helper.add_review_opinion_for_merge(request, review_uid, should_merge, _t)
        if len(error) == 0:
            nickname = request.authenticated_userid
            main_page = request.application_url
            port = get_port(request)
            send_request_for_recent_reviewer_socketio(nickname, main_page, port, 'merges')

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
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _t = Translator(ui_locales)

    if not is_integer(uid):
        logger('additives', 'undo_review', 'invalid uid', error=True)
        prepared_dict = {
            'info': '',
            'success': '',
            'error': _t.get(_.internalKeyError)
        }
        return prepared_dict

    nickname = request.authenticated_userid
    queue = request.params['queue']
    if is_user_author_or_admin(nickname):
        success, error = review_history_helper.revoke_old_decision(queue, uid, ui_locales, nickname)
        prepared_dict = {
            'info': '',
            'success': success,
            'error': error
        }
    else:
        logger('additives', 'undo_review', 'user has no rights', error=True)
        prepared_dict = {
            'info': _t.get(_.justLookDontTouch),
            'success': '',
            'error': ''
        }

    return prepared_dict


def cancel(request) -> dict:
    """
    Tries to cancel a review process.

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error key
    """
    uid = request.params['uid']
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _t = Translator(ui_locales)

    if not is_integer(uid):
        logger('additives', 'cancel_review', 'invalid uid', error=True)
        return {
            'error': _t.get(_.internalKeyError),
            'info': '',
            'success': ''
        }

    prepared_dict = {}
    nickname = request.authenticated_userid
    queue = request.params['queue']
    if is_user_author_or_admin(nickname):
        success, error = review_history_helper.cancel_ongoing_decision(queue, uid, ui_locales, nickname)
        prepared_dict['success'] = success
        prepared_dict['error'] = error
        prepared_dict['info'] = ''
    else:
        prepared_dict['info'] = _t.get(_.justLookDontTouch)
        prepared_dict['success'] = ''
        prepared_dict['error'] = ''

    return prepared_dict


def lock(request) -> dict:
    """
    Tries to lock an optimization element, so the user can propose an edit

    :param request: pyramid's request object
    :rtype: dict
    :return: collection with error, success, info key
    """
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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

    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
