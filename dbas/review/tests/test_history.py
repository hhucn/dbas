from dbas.review.history import get_review_history, get_ongoing_reviews
from dbas.review.reputation import get_history_of
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class TestReviewHistoryHelper(TestCaseWithConfig):
    translator = Translator('en')

    def test_get_review_history_for_with_special_access(self):
        history = get_review_history('mainpage', self.user_tobi, self.translator)
        self.assertIn('has_access', history)
        self.assertIn('past_decision', history)
        self.assertTrue(history['has_access'])

    def test_get_review_history_for_without_special_access(self):
        history = get_review_history('mainpage', self.user_anonymous, self.translator)
        self.assertIn('has_access', history)
        self.assertIn('past_decision', history)
        self.assertFalse(history['has_access'])

    def test_get_ongoing_review_for_with_special_access(self):
        ongoing = get_ongoing_reviews('mainpage', self.user_tobi, self.translator)
        self.assertIn('has_access', ongoing)
        self.assertIn('past_decision', ongoing)
        self.assertTrue(ongoing['has_access'])

    def test_get_ongoing_review_for_without_special_access(self):
        ongoing = get_ongoing_reviews('mainpage', self.user_anonymous, self.translator)
        self.assertIn('has_access', ongoing)
        self.assertIn('past_decision', ongoing)
        self.assertFalse(ongoing['has_access'])

    def test_get_reputation_history_of(self):
        history = get_history_of(self.user_tobi, self.translator)
        self.assertGreater(len(history), 0)
        self.assertIn('count', history)
        self.assertIn('history', history)

        for h in history['history']:
            self.assertIn('date', h)
            self.assertIn('action', h)
            self.assertIn('points', h)
