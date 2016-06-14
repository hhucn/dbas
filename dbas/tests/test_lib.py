import unittest
from dbas import lib
import arrow


class LibTests(unittest.TestCase):

    def test_escape_string(self):
        self.assertEqual(lib.escape_string(text=''), '')

        # normal string
        self.assertEqual(lib.escape_string(text='str'), 'str')

        # strings with html special chars
        self.assertEqual(lib.escape_string(text='&'), '&amp;')

        self.assertEqual(lib.escape_string(text='" str & str2'), '&quot; str &amp; str2')

        long_str_with_special_char = 'str'
        long_str_without_special_char = 'str'
        for i in range(1, 1000):
            long_str_with_special_char += '"'
        for i in range(1, 1000):
            long_str_without_special_char += '&quot;'
        self.assertEqual(lib.escape_string(long_str_with_special_char), long_str_without_special_char)

    def test_sql_timestamp_pretty_print(self):
        utc = arrow.utcnow()

        time_humanize_de = utc.to('Europe/Berlin').humanize(locale='de')
        self.assertEqual(lib.sql_timestamp_pretty_print(ts=utc,
                                                        lang='de',
                                                        humanize=True,
                                                        with_exact_time=False), time_humanize_de)

        time_humanize_en = utc.to('US/Pacific').humanize()
        self.assertEqual(lib.sql_timestamp_pretty_print(ts=utc,
                                                        lang='en',
                                                        humanize=True,
                                                        with_exact_time=True), time_humanize_en)

        time_format_de_with_exact_time = utc.format('DD.MM.YYYY, HH:mm:ss ')
        self.assertEqual(lib.sql_timestamp_pretty_print(ts=utc,
                                                        lang='de',
                                                        humanize=False,
                                                        with_exact_time=True), time_format_de_with_exact_time)

        time_format_de_without_exact_time = utc.format('DD.MM.YYYY')
        self.assertEqual(lib.sql_timestamp_pretty_print(ts=utc,
                                                        lang='de',
                                                        humanize=False,
                                                        with_exact_time=False), time_format_de_without_exact_time)

        time_format_en_with_exact_time = utc.format('YYYY-MM-DD, HH:mm:ss ')
        self.assertEqual(lib.sql_timestamp_pretty_print(ts=utc,
                                                        lang='en',
                                                        humanize=False,
                                                        with_exact_time=True), time_format_en_with_exact_time)

        time_format_en_without_exact_time = utc.format('YYYY-MM-DD')
        self.assertEqual(lib.sql_timestamp_pretty_print(ts=utc,
                                                        lang='en',
                                                        humanize=False,
                                                        with_exact_time=False), time_format_en_without_exact_time)

