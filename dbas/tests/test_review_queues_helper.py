import unittest

import dbas.review.helper.queues as ReviewQueuesHelper
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class ReviewQueuesHelperTest(unittest.TestCase):

    def test_get_review_queues_as_lists(self):
        _tn = Translator('en')
        self.assertIsNone(ReviewQueuesHelper.get_review_queues_as_lists('page', _tn, 'Pikachu'))

        queues = ReviewQueuesHelper.get_review_queues_as_lists('page', _tn, 'Tobias')
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
        count = ReviewQueuesHelper.get_complete_review_count('anonymous')
        self.assertEquals(count, 0)

        count = ReviewQueuesHelper.get_complete_review_count('Tobias')
        self.assertTrue(count > 0)

        count = ReviewQueuesHelper.get_complete_review_count('tobias')
        self.assertTrue(count is 0)

    def test_add_proposals_for_statement_corrections(self):
        trans = Translator('en')
        dupl_elements = [{'uid': 2, 'text': 'we should get a cat'}]
        wrong_elements = [{'uid': 0, 'text': 'oh...this will crash'}]
        no_corr_elements = [{'uid': 7, 'text': 'dogs can act as watch dogs'}]
        right_elements = [{'uid': 7, 'text': 'dogs can act as brutal watch dogs'}]

        text, error = ReviewQueuesHelper.add_proposals_for_statement_corrections(right_elements, 'tobias', trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.noRights))

        text, error = ReviewQueuesHelper.add_proposals_for_statement_corrections(wrong_elements, 'Tobias', trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.internalKeyError))

        text, error = ReviewQueuesHelper.add_proposals_for_statement_corrections(dupl_elements, 'Tobias', trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.alreadyEditProposals))

        text, error = ReviewQueuesHelper.add_proposals_for_statement_corrections(no_corr_elements, 'Tobias', trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.noCorrections))

        text, error = ReviewQueuesHelper.add_proposals_for_statement_corrections(right_elements, 'Tobias', trans)
        self.assertFalse(error)

    def test_is_statement_in_edit_queue(self):
        self.assertFalse(ReviewQueuesHelper.is_statement_in_edit_queue(1))
        self.assertTrue(ReviewQueuesHelper.is_statement_in_edit_queue(2))

    def test_is_arguments_premise_in_edit_queue(self):
        self.assertFalse(ReviewQueuesHelper.is_arguments_premise_in_edit_queue(1))
        self.assertTrue(ReviewQueuesHelper.is_arguments_premise_in_edit_queue(4))

    def test_lock_optimization_review(self):
        _tn = Translator('en')
        success, info, error, is_locked = ReviewQueuesHelper.lock_optimization_review('nickname', 0, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) == 0)
        self.assertTrue(len(error) > 0)
        self.assertFalse(is_locked)

        success, info, error, is_locked = ReviewQueuesHelper.lock_optimization_review('Tobias', 0, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) == 0)
        self.assertTrue(len(error) > 0)
        self.assertFalse(is_locked)

        success, info, error, is_locked = ReviewQueuesHelper.lock_optimization_review('Tobias', 2, _tn)
        self.assertTrue(len(success) != 0)
        self.assertTrue(len(info) == 0)
        self.assertTrue(len(error) == 0)
        self.assertTrue(is_locked)

        success, info, error, is_locked = ReviewQueuesHelper.lock_optimization_review('Tobias', 2, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) > 0)
        self.assertTrue(len(error) == 0)
        self.assertTrue(is_locked)

        success, info, error, is_locked = ReviewQueuesHelper.lock_optimization_review('Christian', 2, _tn)
        self.assertTrue(len(success) == 0)
        self.assertTrue(len(info) > 0)
        self.assertTrue(len(error) == 0)
        self.assertTrue(is_locked)

    def test_unlock_optimization_review(self):
        ReviewQueuesHelper.unlock_optimization_review(2)
        self.assertFalse(ReviewQueuesHelper.is_review_locked(2))

    def is_review_locked(self):
        self.assertFalse(ReviewQueuesHelper.is_review_locked(2))
