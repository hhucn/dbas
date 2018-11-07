"""
Validators for the review-section.
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDeleteReason
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer
from dbas.review.mapper import get_review_model_by_key
from dbas.review.queue import review_queues, all_queues
from dbas.review.reputation import get_reputation_of, reputation_borders
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.lib import add_error


def valid_review_reason(request):
    """
    Given an reason, validates the correctness for our review system.

    :param request:
    :return:
    """
    reason = request.json_body.get('reason')
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).first()

    if db_reason or reason in ['optimization', 'duplicate']:
        request.validated['reason'] = reason
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid reason', _tn.get(_.internalError))
        return False


def valid_review_queue_name(request):
    """
    Given a name for a queue, validates the correctness for our review system

    :param request:
    :return:
    """
    queue = request.matchdict.get('queue')
    if queue in all_queues:
        request.validated['queue'] = queue
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid queue', _tn.get(_.internalError))
        return False


def valid_user_has_review_access(request):
    """
    Given a user and a name for a queue, validates the access to our review system

    :param request:
    :return:
    """
    db_user = request.validated.get('user')
    queue = request.validated.get('queue')
    if not db_user or not queue:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid user or queue', _tn.get(_.internalError))
        return False
    rep_count, all_rights = get_reputation_of(db_user)
    if rep_count >= reputation_borders[queue] or all_rights:
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid user rights', _tn.get(_.internalError))
        return False


def valid_not_executed_review(keyword, model):
    def valid_model(request):
        uid = request.json_body.get(keyword)
        db_review = DBDiscussionSession \
            .query(model).filter(model.uid == uid,
                                 model.is_executed == False).first() if is_integer(uid) else None
        if db_review:
            request.validated['db_review'] = db_review
            return True
        else:
            add_error(request, 'Database has no row {} of {}'.format(uid, model))
            return False

    return valid_model


def valid_review_queue_key(request):
    """
    Validates the correct keyword for a review queue

    :param request:
    :return:
    """
    queue = request.json_body.get('queue')
    if queue in review_queues:
        request.validated[queue] = queue
        return True
    else:
        add_error(request, 'No queue found: {}'.format(queue))
        return False


def valid_uid_as_row_in_review_queue(request):
    uid = request.json_body.get('uid')
    queue = request.json_body.get('queue', '')
    model = get_review_model_by_key(queue)

    db_review = DBDiscussionSession.query(model).get(uid) if is_integer(uid) and model else None
    if db_review:
        request.validated['queue'] = queue
        request.validated['uid'] = uid
        request.validated['review'] = db_review
        return True
    else:
        add_error(request, 'Invalid id for any review queue found: {}'.format(queue))
    return False
