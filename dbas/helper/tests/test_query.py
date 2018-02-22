import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.helper.query import set_user_language


class QueryHelperTest(unittest.TestCase):

    def test_set_german_language(self):
        db_user = DBDiscussionSession.query(User).get(2)
        result = set_user_language(db_user, 'de')
        self.assertTrue('ui_locales' in result)
        self.assertTrue('current_lang' in result)
        self.assertTrue('error' in result)
        self.assertTrue(len(result['error']) == 0)

    def test_set_english_language(self):
        db_user = DBDiscussionSession.query(User).get(2)
        result = set_user_language(db_user, 'en')
        self.assertTrue('ui_locales' in result)
        self.assertTrue('current_lang' in result)
        self.assertTrue('error' in result)
        self.assertTrue(len(result['error']) == 0)
