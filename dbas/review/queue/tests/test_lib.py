import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewEdit, Premise, Argument
from dbas.review.lib import get_reputation_reason_by_action
from dbas.review.queue.lib import is_statement_in_edit_queue, is_arguments_premise_in_edit_queue


class LibTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_get_reputation_reason_by_wrong_action(self):
        self.assertIsNone(get_reputation_reason_by_action('foo'))

    def test_get_reputation_reason_by_action(self):
        actions = [
            'first_position',
            'first_justification',
            'first_argument_click',
            'first_confrontation',
            'first_new_argument',
            'new_statement',
            'success_flag',
            'success_edit',
            'success_duplicate',
            'bad_flag',
            'bad_edit',
            'bad_duplicate'
        ]
        for action in actions:
            self.assertIsNotNone(get_reputation_reason_by_action(action))

    def test_is_statement_in_edit_queue(self):
        db_review_edits = DBDiscussionSession.query(ReviewEdit).all()
        for review in db_review_edits:
            self.assertTrue(is_statement_in_edit_queue(review.statement_uid, review.is_executed))
        self.assertFalse(is_statement_in_edit_queue(50))

    def test_is_arguments_premise_in_edit_queue(self):
        db_review = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).all()
        for review in db_review:
            db_p = DBDiscussionSession.query(Premise).filter_by(statement_uid=review.statement_uid).first()
            if db_p:
                db_arg = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_p.premisegroup_uid).first()
                self.assertTrue(is_arguments_premise_in_edit_queue(db_arg, False))
                break
