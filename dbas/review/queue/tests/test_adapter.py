import unittest

from pyramid import testing

import dbas.review.queue.lib
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewOptimization
from dbas.database.discussion_model import User
from dbas.review.queue import review_queues
from dbas.review.queue.abc_queue import subclass_by_name
from dbas.review.queue.adapter import QueueAdapter
from dbas.review.queue.optimization import OptimizationQueue
from dbas.strings.translator import Translator


class AdapterTest(unittest.TestCase):

    def test_get_review_queues_as_lists(self):
        _tn = Translator('en')

        db_user = DBDiscussionSession.query(User).get(2)
        queues = QueueAdapter(db_user=db_user, main_page='page', translator=_tn).get_review_queues_as_lists()
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
        self.assertEqual(0, dbas.review.queue.lib.get_complete_review_count(u1))
        self.assertLess(0, dbas.review.queue.lib.get_complete_review_count(u2))

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

    def test_get_subpage_empty_session(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        queue = subclass_by_name(review_queues[0])
        adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='url', translator=Translator('en'))
        subpage_dict = adapter.get_subpage_of_queue({}, review_queues[0])
        self.assertIsNotNone(subpage_dict['elements'])
        self.assertFalse(subpage_dict['no_arguments_to_review'])
        self.assertTrue(f'is_{review_queues[0]}' in subpage_dict['button_set'].keys())

    def test_get_all_subpages(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        for key in review_queues:
            queue = subclass_by_name(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='url', translator=Translator('en'))
            subpage_dict = adapter.get_subpage_of_queue(request.session, key)
            self.assertIsNotNone(subpage_dict['elements'])
            self.assertFalse(subpage_dict['no_arguments_to_review'])
            self.assertTrue(f'is_{key}' in subpage_dict['button_set'].keys())
