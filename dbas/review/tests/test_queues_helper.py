import unittest

import dbas.review.queue.lib
import dbas.review.queues as rqh
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewOptimization
from dbas.strings.translator import Translator


class ReviewQueuesHelperTest(unittest.TestCase):

    def test_get_review_queues_as_lists(self):
        _tn = Translator('en')

        db_user = DBDiscussionSession.query(User).get(2)
        queues = rqh.get_review_queues_as_lists('page', _tn, db_user)
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
