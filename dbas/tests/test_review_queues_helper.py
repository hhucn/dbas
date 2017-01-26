import unittest

import dbas.review.helper.queues as ReviewQueuesHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewQueuesHelperTest(unittest.TestCase):

    def test_get_review_array(self):
        _tn = Translator('en')
        self.assertIsNone(ReviewQueuesHelper.get_review_queues_as_lists('page', _tn, 'Pikachu'))

        array = ReviewQueuesHelper.get_review_queues_as_lists('page', _tn, 'Tobias')
        for d in array:
            self.assertTrue('task_name' in d)
            self.assertTrue('url' in d)
            self.assertTrue('icon' in d)
            self.assertTrue('task_count' in d)
            self.assertTrue('is_allowed' in d)
            self.assertTrue('is_allowed_text' in d)
            self.assertTrue('is_not_allowed_text' in d)
            self.assertTrue('last_reviews' in d)

    def test_lock(self):
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

    def test_unlock(self):
        ReviewQueuesHelper.unlock_optimization_review(2)
        self.assertFalse(ReviewQueuesHelper.is_review_locked(2))

    def is_review_locked(self):
        self.assertFalse(ReviewQueuesHelper.is_review_locked(2))
