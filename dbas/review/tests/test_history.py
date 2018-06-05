import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.review.history import get_review_history, get_ongoing_reviews
from dbas.review.reputation import get_history_of
from dbas.strings.translator import Translator


class TestReviewHistoryHelper(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_get_review_history_for_with_special_access(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        history = get_review_history('mainpage', db_user, Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertTrue(history['has_access'])

    def test_get_review_history_for_without_special_access(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Pascal').first()
        history = get_review_history('mainpage', db_user, Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertFalse(history['has_access'])

    def test_get_ongoing_review_for_with_special_access(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        ongoing = get_ongoing_reviews('mainpage', db_user, Translator('en'))
        self.assertTrue('has_access' in ongoing)
        self.assertTrue('past_decision' in ongoing)
        self.assertFalse(ongoing['has_access'])

    def test_get_ongoing_review_for_without_special_access(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Pascal').first()
        ongoing = get_ongoing_reviews('mainpage', db_user, Translator('en'))
        self.assertTrue('has_access' in ongoing)
        self.assertTrue('past_decision' in ongoing)
        self.assertFalse(ongoing['has_access'])

    def test_get_reputation_history_of(self):
        db_user = DBDiscussionSession.query(User).get(2)
        history = get_history_of(db_user, Translator('en'))
        self.assertTrue(len(history) > 0)
        self.assertTrue('count' in history)
        self.assertTrue('history' in history)

        for h in history['history']:
            self.assertTrue('date' in h)
            self.assertTrue('action' in h)
            self.assertTrue('points' in h)
