import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ShortLinks
from dbas.helper.query import set_user_language, get_short_url


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

    def test_get_short_url(self):
        url = 'https://dbas.cs.uni-duesseldorf.de'
        db_url = DBDiscussionSession.query(ShortLinks).filter_by(long_url=url).first()
        self.assertIsNone(db_url)

        pdict = get_short_url(url)

        from pprint import pprint
        pprint(pdict)
        self.assertIn('url', pdict)
        self.assertIn('service', pdict)
        self.assertIn('service_url', pdict)
        self.assertIn('service_text', pdict)
        self.assertNotEqual(0, len(pdict['service_text']))

        db_url = DBDiscussionSession.query(ShortLinks).filter_by(long_url=url).first()
        if len(pdict['url']) > 0:
            self.assertIsNotNone(db_url)
        else:
            self.assertIsNone(db_url)
