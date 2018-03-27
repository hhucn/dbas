from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDeleteReason, ReviewEdit
from dbas.review.helper.queues import review_queues
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig
from dbas.validators.reviews import valid_not_executed_review, valid_review_queue_key, valid_review_reason, \
    valid_uid_as_row_in_review_queue


class TestReviewValidators(TestCaseWithConfig):
    def test_valid_review_reason(self):
        for k, v in [('x', 'y'), ('reason', '')]:
            request = construct_dummy_request({k: v})
            response = valid_review_reason(request)
            self.assertFalse(response)
            self.assertIsInstance(response, bool)

        reasons = [r.reason for r in DBDiscussionSession.query(ReviewDeleteReason).all()]
        reasons += ['optimization', 'duplicate']
        for reason in reasons:
            request = construct_dummy_request({'reason': reason})
            response = valid_review_reason(request)
            self.assertTrue(response)
            self.assertIsInstance(response, bool)

    def test_valid_not_executed_review(self):
        request = construct_dummy_request({'': ''})
        fn = valid_not_executed_review('key', ReviewEdit)
        response = fn(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'uid': 1000})
        fn = valid_not_executed_review('uid', ReviewEdit)
        response = fn(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
        request = construct_dummy_request({'uid': db_edit.uid})
        fn = valid_not_executed_review('uid', ReviewEdit)
        response = fn(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_review_queue_key(self):
        request = construct_dummy_request({'queue': ''})
        response = valid_review_queue_key(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        for queue in review_queues:
            request = construct_dummy_request({'queue': queue})
            response = valid_review_queue_key(request)
            self.assertTrue(response)
            self.assertIsInstance(response, bool)

    def test_valid_uid_as_row_in_review_queue(self):
        request = construct_dummy_request({'queue': '', 'uid': ''})
        response = valid_uid_as_row_in_review_queue(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'queue': 'edits', 'uid': 10000})
        response = valid_uid_as_row_in_review_queue(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
        request = construct_dummy_request({'queue': 'edits', 'uid': db_edit.uid})
        response = valid_uid_as_row_in_review_queue(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('queue', request.validated)
        self.assertIn('uid', request.validated)
        self.assertIn('review', request.validated)
