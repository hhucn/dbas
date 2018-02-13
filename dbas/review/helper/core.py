import dbas.review.helper.history as review_history_helper
import dbas.review.helper.queues as review_queue_helper

from dbas.logger import logger
from dbas.input_validator import is_integer
from dbas.lib import get_discussion_language, is_user_author_or_admin
from dbas.helper.query import revoke_content
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


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
