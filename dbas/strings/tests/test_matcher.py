import unittest

from dbas.strings import matcher


class StringMatcherTest(unittest.TestCase):
    matcher.MECHANISM = 'Levensthein'

    def test_get_strings_for_start(self):
        return_array = matcher.get_suggestions_for_positions('cat', 2, True)
        self.check_string_matcher_array(return_array)

        return_array = matcher.get_suggestions_for_positions('cat', 2, False)
        self.check_string_matcher_array(return_array)

    def test_get_strings_for_reasons(self):
        return_array = matcher.get_strings_for_duplicates_or_reasons('cat', 2, 2)
        self.check_string_matcher_array(return_array)

    def test_get_strings_for_search(self):
        return_dict = matcher.get_strings_for_search('cat')
        for key in return_dict:
            self.assertIn('cat', return_dict[key]['text'].lower())
            self.assertGreater(return_dict[key]['statement_uid'], 0)

    def test_get_distance(self):
        self.assertEqual(3, int(matcher.get_lev_distance('cat', 'dog')))
        self.assertEqual(2, int(matcher.get_lev_distance('cat', 'dag')))
        self.assertEqual(2, int(matcher.get_lev_distance('cat', 'doT')))

    def check_string_matcher_array(self, return_array):
        for entry in return_array:
            self.assertIn('cat', entry['text'].lower())
            self.assertGreaterEqual(int(entry['distance']), 0)
            self.assertNotEqual(entry['statement_uid'], 0)
