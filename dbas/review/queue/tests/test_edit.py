import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewEdit, Premise, Argument
from dbas.review.queue.edit import EditQueue


class EditQueueTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()


    def test_is_statement_in_edit_queue(self):
        db_review_edits = DBDiscussionSession.query(ReviewEdit).all()
        for review in db_review_edits:
            self.assertTrue(EditQueue().is_statement_in_edit_queue(review.statement_uid, review.is_executed))
        self.assertFalse(EditQueue().is_statement_in_edit_queue(50))

    def test_is_arguments_premise_in_edit_queue(self):
        db_reviews = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False, is_revoked=False).all()
        for db_review in db_reviews:
            db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=db_review.statement_uid).first()
            if not db_premise:  # skip this cause we just have random data
                continue
            db_arg = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_premise.premisegroup_uid).first()
            self.assertTrue(EditQueue().is_arguments_premise_in_edit_queue(db_arg))
