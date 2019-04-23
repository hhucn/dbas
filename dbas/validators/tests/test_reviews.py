from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDeleteReason, ReviewEdit, User
from dbas.review.queue import review_queues, all_queues, key_edit, key_split
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig
from dbas.validators.reviews import valid_not_executed_review, valid_review_queue_key, valid_review_reason, \
    valid_uid_as_row_in_review_queue, valid_review_queue_name, valid_user_has_review_access


class TestReviewValidators(TestCaseWithConfig):
    def test_valid_review_reason(self):
        for k, v in [('x', 'y'), ('reason', '')]:
            request = construct_dummy_request(json_body={k: v})
            response = valid_review_reason(request)
            self.assertFalse(response)
            self.assertEqual(bool, type(response))

        reasons = [r.reason for r in DBDiscussionSession.query(ReviewDeleteReason).all()]
        reasons += ['optimization', 'duplicate']
        for reason in reasons:
            request = construct_dummy_request(json_body={'reason': reason})
            response = valid_review_reason(request)
            self.assertTrue(response)
            self.assertEqual(bool, type(response))

    def test_valid_not_executed_review(self):
        request = construct_dummy_request(json_body={'': ''})
        fn = valid_not_executed_review('key', ReviewEdit)
        response = fn(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        request = construct_dummy_request(json_body={'uid': 1000})
        fn = valid_not_executed_review('uid', ReviewEdit)
        response = fn(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
        request = construct_dummy_request(json_body={'uid': db_edit.uid})
        fn = valid_not_executed_review('uid', ReviewEdit)
        response = fn(request)
        self.assertTrue(response)
        self.assertEqual(bool, type(response))

    def test_valid_review_queue_key(self):
        request = construct_dummy_request(json_body={'queue': ''})
        response = valid_review_queue_key(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        for queue in review_queues:
            request = construct_dummy_request(json_body={'queue': queue})
            response = valid_review_queue_key(request)
            self.assertTrue(response)
            self.assertEqual(bool, type(response))

    def test_valid_uid_as_row_in_review_queue(self):
        request = construct_dummy_request(json_body={'queue': '', 'uid': ''})
        response = valid_uid_as_row_in_review_queue(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        request = construct_dummy_request(json_body={'queue': key_edit, 'uid': 10000})
        response = valid_uid_as_row_in_review_queue(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
        request = construct_dummy_request(json_body={'queue': key_edit, 'uid': db_edit.uid})
        response = valid_uid_as_row_in_review_queue(request)
        self.assertTrue(response)
        self.assertEqual(bool, type(response))
        self.assertIn('queue', request.validated)
        self.assertIn('uid', request.validated)
        self.assertIn('review', request.validated)

    def test_valid_review_queue_name_error(self):
        request = construct_dummy_request(json_body={'queue': 'foo'})
        response = valid_review_queue_name(request)
        self.assertFalse(response)

    def test_valid_review_queue_name(self):
        for queue in all_queues:
            request = construct_dummy_request(matchdict={'queue': queue})
            response = valid_review_queue_name(request)
            self.assertTrue(response)

    def test_valid_user_has_review_access(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        request = construct_dummy_request(validated={'queue': key_split, 'user': db_user})
        response = valid_user_has_review_access(request)
        self.assertTrue(response)

    def test_valid_user_has_not_review_access(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Elias').first()
        request = construct_dummy_request(validated={'queue': key_split, 'user': db_user})
        response = valid_user_has_review_access(request)
        self.assertFalse(response)
