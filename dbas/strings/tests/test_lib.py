import unittest

from dbas.strings.lib import start_with_capital, start_with_small, replace_multiple_chars


class TestLib(unittest.TestCase):

    def test_start_with_capital(self):
        self.assertEqual(start_with_capital(''), '')
        self.assertEqual(start_with_capital('asd'), 'Asd')
        self.assertEqual(start_with_capital('Asd'), 'Asd')
        self.assertEqual(start_with_capital('ASD'), 'ASD')

    def test_start_with_small(self):
        self.assertEqual(start_with_small(''), '')
        self.assertEqual(start_with_small('asd'), 'asd')
        self.assertEqual(start_with_small('aSD'), 'aSD')
        self.assertEqual(start_with_small('Asd'), 'asd')
        self.assertEqual(start_with_small('ASD'), 'aSD')

    def test_replace_multiple_chars(self):
        self.assertEqual(replace_multiple_chars('Foo/Bar/Baz', ['/'], ' '), 'Foo Bar Baz')
        self.assertEqual(replace_multiple_chars('Foo/Bar-Baz', ['/', '-'], ' '), 'Foo Bar Baz')
        self.assertEqual(replace_multiple_chars('Foo-Bar-Baz', ['/', '+', '-'], ' '), 'Foo Bar Baz')
        self.assertEqual(replace_multiple_chars('Foo/Bar/Baz', ['/'], '.'), 'Foo.Bar.Baz')
        self.assertEqual(replace_multiple_chars('Foo/Bar/Baz', ['Foo', 'Bar', 'Baz'], 'Gull'), 'Gull/Gull/Gull')
