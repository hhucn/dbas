import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config
from dbas.strings import matcher

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class StringMatcherTest(unittest.TestCase):
    matcher.mechanism = 'Levensthein'

    def test_get_strings_for_start(self):
        mechanism, return_array = matcher.get_strings_for_start('cat', 2, True)
        self.check_string_matcher_array(return_array)

        mechanism, return_array = matcher.get_strings_for_start('cat', 2, False)
        self.check_string_matcher_array(return_array)

    def test_get_strings_for_reasons(self):
        mechanism, return_array = matcher.get_strings_for_reasons('cat', 2)
        self.check_string_matcher_array(return_array)

    def test_get_strings_for_issues(self):
        mechanism, return_array = matcher.get_strings_for_issues('cat')
        self.assertEqual(len(DBDiscussionSession.query(Issue).all()), len(return_array))
        count = 0
        for entry in return_array:
            if 'cat' in entry['text'].lower():
                count += 1
        self.assertEqual(count, 1)

        mechanism, return_array = matcher.get_strings_for_issues('ccaatt')
        count = 0
        for entry in return_array:
            if 'ccaatt' in entry['text'].lower():
                count += 1
        self.assertEqual(count, 0)

    def test_get_strings_for_search(self):
        return_dict = matcher.get_strings_for_search('cat')
        for key in return_dict:
            self.assertTrue('cat' in return_dict[key]['text'].lower())
            self.assertGreater(return_dict[key]['statement_uid'], 0)

    def test_get_distance(self):
        self.assertEqual(3, int(matcher.get_distance('cat', 'dog')))
        self.assertEqual(2, int(matcher.get_distance('cat', 'dag')))
        self.assertEqual(2, int(matcher.get_distance('cat', 'doT')))

    def check_string_matcher_array(self, return_array):
        for entry in return_array:
            self.assertTrue('cat' in entry['text'].lower())
            self.assertGreaterEqual(int(entry['distance']), 0)
            self.assertNotEqual(entry['statement_uid'], 0)
