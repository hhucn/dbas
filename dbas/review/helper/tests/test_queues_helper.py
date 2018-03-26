import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewOptimization, TextVersion, ReviewEdit, Argument, Premise
import dbas.review.helper.queues as rqh
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class ReviewQueuesHelperTest(unittest.TestCase):

    def test_get_review_queues_as_lists(self):
        _tn = Translator('en')
        self.assertIsNone(rqh.get_review_queues_as_lists('page', _tn, 'Pikachu'))

        queues = rqh.get_review_queues_as_lists('page', _tn, 'Tobias')
        for q in queues:
            self.assertTrue('task_name' in q)
            self.assertTrue('url' in q)
            self.assertTrue('icon' in q)
            self.assertTrue('task_count' in q)
            self.assertTrue('is_allowed' in q)
            self.assertTrue('is_allowed_text' in q)
            self.assertTrue('is_not_allowed_text' in q)
            self.assertTrue('last_reviews' in q)

    def test_get_complete_review_count(self):
        u1 = DBDiscussionSession.query(User).get(1)
        u2 = DBDiscussionSession.query(User).get(2)
        self.assertEqual(0, rqh.get_complete_review_count(u1))
        self.assertLess(0, rqh.get_complete_review_count(u2))

    def test_add_proposals_for_statement_corrections(self):
        db_tv = DBDiscussionSession.query(TextVersion).get(7)
        db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
        trans = Translator('en')
        wrong_elements = [{'uid': 0, 'text': 'oh...this will crash'}]
        dupl_elements = [{'uid': db_edit.uid, 'text': 'duplicate uid, already in review'}]
        no_corr_elements = [{'uid': db_tv.statement_uid, 'text': db_tv.content}]
        right_elements = [{'uid': db_tv.statement_uid, 'text': db_tv.content + 'new part for edit'}]
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        text, error = rqh.add_proposals_for_statement_corrections(wrong_elements, db_user, trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.internalKeyError))

        text, error = rqh.add_proposals_for_statement_corrections(dupl_elements, db_user, trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.alreadyEditProposals))

        text, error = rqh.add_proposals_for_statement_corrections(no_corr_elements, db_user, trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.noCorrections))

        text, error = rqh.add_proposals_for_statement_corrections(right_elements, db_user, trans)
        self.assertFalse(error)

    def test_is_statement_in_edit_queue(self):
        db_review_edits = DBDiscussionSession.query(ReviewEdit).all()
        for review in db_review_edits:
            self.assertTrue(rqh.is_statement_in_edit_queue(review.statement_uid, review.is_executed))
        self.assertFalse(rqh.is_statement_in_edit_queue(50))

    def test_is_arguments_premise_in_edit_queue(self):
        db_review = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).all()
        for review in db_review:
            db_p = DBDiscussionSession.query(Premise).filter_by(statement_uid=review.statement_uid).first()
            if db_p:
                db_arg = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_p.premisegroup_uid).first()
                self.assertTrue(rqh.is_arguments_premise_in_edit_queue(db_arg, False))
                break

    def test_lock_optimization_review(self):
        _tn = Translator('en')
        tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()
        db_review = DBDiscussionSession.query(ReviewOptimization).get(2)

        return_dict = rqh.lock_optimization_review(tobias, db_review, _tn)
        self.assertTrue(len(return_dict['success']) != 0)
        self.assertTrue(len(return_dict['info']) == 0)
        self.assertTrue(return_dict['is_locked'])

        return_dict = rqh.lock_optimization_review(tobias, db_review, _tn)
        self.assertTrue(len(return_dict['success']) == 0)
        self.assertTrue(len(return_dict['info']) > 0)
        self.assertTrue(return_dict['is_locked'])

        return_dict = rqh.lock_optimization_review(christian, db_review, _tn)
        self.assertTrue(len(return_dict['success']) == 0)
        self.assertTrue(len(return_dict['info']) > 0)
        self.assertTrue(return_dict['is_locked'])

    def test_unlock_optimization_review(self):
        _tn = Translator('en')
        db_review = DBDiscussionSession.query(ReviewOptimization).get(2)
        rqh.unlock_optimization_review(db_review, _tn)
        self.assertFalse(rqh.is_review_locked(db_review.uid))

    def is_review_locked(self):
        tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        _tn = Translator('en')
        db_review = DBDiscussionSession.query(ReviewOptimization).get(2)
        rqh.lock_optimization_review(db_review, tobias, _tn)
        self.assertTrue(rqh.is_review_locked(2))
        rqh.unlock_optimization_review(db_review, _tn)
        self.assertFalse(rqh.is_review_locked(2))
