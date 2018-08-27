from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ShortLinks
from dbas.helper.query import set_user_language, generate_short_url
from dbas.tests.utils import TestCaseWithConfig


class QueryHelperTest(TestCaseWithConfig):

    def test_set_german_language(self):
        result = set_user_language(self.user_tobi, 'de')
        self.assertIn('ui_locales', result)
        self.assertIn('current_lang', result)
        self.assertIn('error', result)
        self.assertEqual(len(result['error']), 0)

    def test_set_english_language(self):
        result = set_user_language(self.user_tobi, 'en')
        self.assertIn('ui_locales', result)
        self.assertIn('current_lang', result)
        self.assertIn('error', result)
        self.assertEqual(len(result['error']), 0)

    def test_generate_short_url(self):
        url = 'https://dbas.cs.uni-duesseldorf.de'
        db_url = DBDiscussionSession.query(ShortLinks).filter_by(long_url=url).first()
        self.assertIsNone(db_url)

        pdict = generate_short_url(url)

        self.assertIn('url', pdict)
        self.assertIn('service', pdict)
        self.assertIn('service_url', pdict)
        self.assertIn('service_text', pdict)
        self.assertNotEqual(len(pdict['service_text']), 0)

        db_url = DBDiscussionSession.query(ShortLinks).filter_by(long_url=url).first()
        if len(pdict['url']) > 0:
            self.assertIsNotNone(db_url)
        else:
            self.assertIsNone(db_url)

        # Remove generated ShortLink
        DBDiscussionSession.query(ShortLinks).filter_by(long_url=url).delete()
