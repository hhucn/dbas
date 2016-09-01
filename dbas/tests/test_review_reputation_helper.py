import unittest

import dbas.review.helper.reputation as ReviewReputationHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewReputationHelperTEst(unittest.TestCase):

    def test_get_reputation_history(self):
        self.assertEqual(len(ReviewReputationHelper.get_reputation_history('Bla', Translator('en'))), 0)
        history = ReviewReputationHelper.get_reputation_history('Tobias', Translator('en'))
        self.assertTrue(len(history) > 0)
        self.assertTrue('count' in history)
        self.assertTrue('history' in history)
        for h in history['history']:
            self.assertTrue('date' in h)
            self.assertTrue('action' in h)
            self.assertTrue('points' in h)

    def test_get_reputation_list(self):
        some_list = ReviewReputationHelper.get_reputation_list(Translator('en'))
        self.assertTrue('gains' in some_list)
        self.assertTrue('looses' in some_list)

    def test_get_privilege_list(self):
        some_list = ReviewReputationHelper.get_privilege_list(Translator('en'))
        for element in some_list:
            self.assertTrue('points' in element)
            self.assertTrue('icon' in element)
            self.assertTrue('text' in element)

    def test_get_reputation_of(self):
        count, has_all_rights = ReviewReputationHelper.get_reputation_of('Tobias')
        self.assertTrue(count == 28)
        self.assertTrue(has_all_rights)

        count, has_all_rights = ReviewReputationHelper.get_reputation_of('Tobiass')
        self.assertTrue(count == 0)
        self.assertFalse(has_all_rights)
