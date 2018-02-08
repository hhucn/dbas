import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
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
        count = rqh.get_complete_review_count('anonymous')
        self.assertEquals(count, 0)

        count = rqh.get_complete_review_count('Tobias')
        self.assertTrue(count > 0)

        count = rqh.get_complete_review_count('tobias')
        self.assertTrue(count is 0)

    def test_add_proposals_for_statement_corrections(self):
        trans = Translator('en')
        dupl_elements = [{'uid': 22, 'text': 'duuuuplicaate'}]
        wrong_elements = [{'uid': 0, 'text': 'oh...this will crash'}]
        no_corr_elements = [{'uid': 7, 'text': 'dogs can act as watch dogs'}]
        right_elements = [{'uid': 7, 'text': 'dogs can act as brutal watch dogs'}]
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
        self.assertTrue(rqh.is_statement_in_edit_queue(1))
        self.assertTrue(rqh.is_statement_in_edit_queue(2, True))
        self.assertFalse(rqh.is_statement_in_edit_queue(2))
        self.assertTrue(rqh.is_statement_in_edit_queue(22))

    def test_is_arguments_premise_in_edit_queue(self):
        self.assertTrue(rqh.is_arguments_premise_in_edit_queue(1))
        self.assertTrue(rqh.is_arguments_premise_in_edit_queue(4))

    def test_lock_optimization_review(self):
        _tn = Translator('en')
        success, info, error, is_locked = rqh.lock_optimization_review('nickname', 0, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) == 0)
        self.assertTrue(len(error) > 0)
        self.assertFalse(is_locked)

        success, info, error, is_locked = rqh.lock_optimization_review('Tobias', 0, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) == 0)
        self.assertTrue(len(error) > 0)
        self.assertFalse(is_locked)

        success, info, error, is_locked = rqh.lock_optimization_review('Tobias', 2, _tn)
        self.assertTrue(len(success) != 0)
        self.assertTrue(len(info) == 0)
        self.assertTrue(len(error) == 0)
        self.assertTrue(is_locked)

        success, info, error, is_locked = rqh.lock_optimization_review('Tobias', 2, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) > 0)
        self.assertTrue(len(error) == 0)
        self.assertTrue(is_locked)

        success, info, error, is_locked = rqh.lock_optimization_review('Christian', 2, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) > 0)
        self.assertTrue(len(error) == 0)
        self.assertTrue(is_locked)

    def test_unlock_optimization_review(self):
        rqh.unlock_optimization_review(2)
        self.assertFalse(rqh.is_review_locked(2))

    def is_review_locked(self):
        self.assertFalse(rqh.is_review_locked(2))
