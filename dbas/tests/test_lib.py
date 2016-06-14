import unittest
from dbas import lib

class LibTests(unittest.TestCase):

    def test_escape_string(self):
        self.assertEqual(lib.escape(''), '')

        # normal string
        self.assertEqual(lib.escape_string('str'), 'str')

        # strings with html special chars
        self.assertEqual(lib.escape_string('&'), '&amp;')

        self.assertEqual(lib.escape_string('" str & str2'), '&quot; str &amp; str2')

        long_str_with_special_char = 'str'
        long_str_without_special_char = 'str'
        for i in range(1, 1000):
            long_str_with_special_char += '"'
        for i in range(1, 1000):
            long_str_without_special_char += '&quot;'
        self.assertEqual(lib.escape_string(long_str_with_special_char), long_str_without_special_char)
