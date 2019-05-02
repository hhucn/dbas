import unittest

from pyramid import testing

import dbas.review.queue.lib
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewOptimization, User, Issue
from dbas.review import FlaggedBy
from dbas.review.queue.adapter import QueueAdapter
from dbas.review.queue.optimization import OptimizationQueue
from dbas.strings.translator import Translator


class AdapterTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).get(2)
        self.other_user = DBDiscussionSession.query(User).get(21)

    def test_get_review_queues_as_lists(self):
        _tn = Translator('en')

        queues = QueueAdapter(db_user=self.user, main_page='page', translator=_tn).get_review_queues_as_lists()
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
        u1: User = DBDiscussionSession.query(User).get(1)
        u2: User = DBDiscussionSession.query(User).get(2)
        issue_cat_or_dog: Issue = DBDiscussionSession.query(Issue).get(2)
        u2.participates_in.append(issue_cat_or_dog)
        self.assertEqual(0, dbas.review.queue.lib.get_complete_review_count(u1))
        self.assertLess(0, dbas.review.queue.lib.get_complete_review_count(u2))
        u2.participates_in.remove(issue_cat_or_dog)

    def test_lock_optimization_review(self):
        _tn = Translator('en')
        tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()
        db_review = DBDiscussionSession.query(ReviewOptimization).get(2)

        return_dict = OptimizationQueue().lock_optimization_review(tobias, db_review, _tn)
        self.assertTrue(len(return_dict['success']) != 0)
        self.assertTrue(len(return_dict['info']) == 0)
        self.assertTrue(return_dict['is_locked'])

        return_dict = OptimizationQueue().lock_optimization_review(tobias, db_review, _tn)
        self.assertTrue(len(return_dict['success']) == 0)
        self.assertTrue(len(return_dict['info']) > 0)
        self.assertTrue(return_dict['is_locked'])

        return_dict = OptimizationQueue().lock_optimization_review(christian, db_review, _tn)
        self.assertTrue(len(return_dict['success']) == 0)
        self.assertTrue(len(return_dict['info']) > 0)
        self.assertTrue(return_dict['is_locked'])

    def test_unlock_optimization_review(self):
        _tn = Translator('en')
        db_review = DBDiscussionSession.query(ReviewOptimization).get(2)
        OptimizationQueue().unlock_optimization_review(db_review, _tn)
        self.assertFalse(OptimizationQueue().is_review_locked(db_review.uid))

    def is_review_locked(self):
        tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        _tn = Translator('en')
        db_review = DBDiscussionSession.query(ReviewOptimization).get(2)
        OptimizationQueue().lock_optimization_review(db_review, tobias, _tn)
        self.assertTrue(OptimizationQueue().is_review_locked(2))
        OptimizationQueue().unlock_optimization_review(db_review, _tn)
        self.assertFalse(OptimizationQueue().is_review_locked(2))

    def test_element_in_queue(self):
        adapter = QueueAdapter(db_user=self.user, application_url='url', translator=Translator('en'))

        status = adapter.element_in_queue(argument_uid=30, statement_uid=None, premisegroup_uid=None)
        self.assertIsNone(status)

        status = adapter.element_in_queue(argument_uid=None, statement_uid=9, premisegroup_uid=None)
        self.assertEqual(FlaggedBy.other, status)

        adapter = QueueAdapter(db_user=self.other_user, application_url='url', translator=Translator('en'))
        status = adapter.element_in_queue(argument_uid=None, statement_uid=9, premisegroup_uid=None)
        self.assertEqual(FlaggedBy.user, status)
