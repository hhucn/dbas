import unittest
from dbas import lib

class LibTests(unittest.TestCase):

    def test_escape_string(self):
        self.assertEqual(lib.escape_string('str'), 'str')
