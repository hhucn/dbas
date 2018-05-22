import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
import dbas.review.history as rhh
from dbas.strings.translator import Translator


class TestReviewHistoryHelper(unittest.TestCase):

    def setUp(self):
        from dbas.review.queues import add_proposals_for_statement_corrections
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        elements = [{'uid': 4, 'text': 'some random text'}]
        add_proposals_for_statement_corrections(elements, db_user, Translator('en'))

    def test_flag_argument(self):
        history = rhh.get_review_history('mainpage', 'nickname', Translator('en'))
        self.assertNotIn('has_access', history)
        self.assertNotIn('past_decision', history)
        self.assertNotIn('has_access', history)

        history = rhh.get_review_history('mainpage', 'Tobias', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertTrue(history['has_access'])

        history = rhh.get_review_history('mainpage', 'Pascal', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertFalse(history['has_access'])

    def test_get_reputation_history_of(self):
        self.assertEqual(len(rhh.get_reputation_history_of('Bla', Translator('en'))), 0)
        history = rhh.get_reputation_history_of('Tobias', Translator('en'))
        self.assertTrue(len(history) > 0)
        self.assertTrue('count' in history)
        self.assertTrue('history' in history)

        for h in history['history']:
            self.assertTrue('date' in h)
            self.assertTrue('action' in h)
            self.assertTrue('points' in h)
