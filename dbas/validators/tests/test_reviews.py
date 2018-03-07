from cornice import Errors
from nose.tools import assert_false, assert_equal, assert_true
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDeleteReason, ReviewEdit
from dbas.review.helper.queues import review_queues
from dbas.validators.reviews import valid_not_executed_review, valid_review_queue_key, valid_review_reason, valid_uid_as_row_in_review_queue


def __prepare_dict(jbody):
    request = testing.DummyRequest(json_body=jbody)
    setattr(request, 'errors', Errors())
    setattr(request, 'cookies', {'_LOCALE_': 'en'})
    request.validated = {}
    return request


def test_valid_review_reason():
    for k, v in [('x', 'y'), ('reason', '')]:
        request = __prepare_dict({k: v})
        response = valid_review_reason(request)
        assert_false(response)
        assert_equal(bool, type(response))

    reasons = [r.reason for r in DBDiscussionSession.query(ReviewDeleteReason).all()]
    reasons += ['optimization', 'duplicate']
    for reason in reasons:
        request = __prepare_dict({'reason': reason})
        response = valid_review_reason(request)
        assert_true(response)
        assert_equal(bool, type(response))


def test_valid_not_executed_review():
    request = __prepare_dict({'': ''})
    fn = valid_not_executed_review('key', ReviewEdit)
    response = fn(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = __prepare_dict({'uid': 1000})
    fn = valid_not_executed_review('uid', ReviewEdit)
    response = fn(request)
    assert_false(response)
    assert_equal(bool, type(response))

    db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
    request = __prepare_dict({'uid': db_edit.uid})
    fn = valid_not_executed_review('uid', ReviewEdit)
    response = fn(request)
    assert_true(response)
    assert_equal(bool, type(response))


def test_valid_review_queue_key():
    request = __prepare_dict({'queue': ''})
    response = valid_review_queue_key(request)
    assert_false(response)
    assert_equal(bool, type(response))

    for queue in review_queues:
        request = __prepare_dict({'queue': queue})
        response = valid_review_queue_key(request)
        assert_true(response)
        assert_equal(bool, type(response))


def test_valid_uid_as_row_in_review_queue():
    request = __prepare_dict({'queue': '', 'uid': ''})
    response = valid_uid_as_row_in_review_queue(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = __prepare_dict({'queue': 'ReviewEdit', 'uid': 10000})
    response = valid_uid_as_row_in_review_queue(request)
    assert_false(response)
    assert_equal(bool, type(response))

    db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
    request = __prepare_dict({'queue': 'ReviewEdit', 'uid': db_edit.uid})
    response = valid_uid_as_row_in_review_queue(request)
    assert_false(response)
    assert_equal(bool, type(response))
