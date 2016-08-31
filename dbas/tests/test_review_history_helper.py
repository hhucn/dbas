import unittest

import dbas.review.helper.history as ReviewHistoryHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TestReviewHistoryHelper(unittest.TestCase):

    def test_flag_argument(self):
        history = ReviewHistoryHelper.get_history('mainpage', 'nickname', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertFalse(history['has_access'])

        history = ReviewHistoryHelper.get_history('mainpage', 'Tobias', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertTrue(history['has_access'])

        history = ReviewHistoryHelper.get_history('mainpage', 'Pascal', Translator('en'))
        self.assertTrue('has_access' in history)
        self.assertTrue('past_decision' in history)
        self.assertFalse(history['has_access'])
