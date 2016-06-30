import unittest

from sqlalchemy import engine_from_config
from dbas import lib, DBDiscussionSession
from dbas.helper.tests_helper import add_settings_to_appconfig
from datetime import date
from dbas.database.discussion_model import Argument

settings = add_settings_to_appconfig("development.ini")

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class LibTests(unittest.TestCase):

    def test_escape_string(self):
        self.assertEqual(lib.escape_string(text=''), '')

        # normal string
        self.assertEqual(lib.escape_string(text='str'), 'str')

        # strings with html special chars
        self.assertEqual(lib.escape_string(text='&'), '&amp;')

        self.assertEqual(lib.escape_string(text='" str & str2'), '&quot; str &amp; str2')

        long_str_with_special_char = 'str' + '"' * 1000
        long_str_without_special_char = 'str' + '&quot;' * 1000
        self.assertEqual(lib.escape_string(long_str_with_special_char), long_str_without_special_char)

    """
    def test_sql_timestamp_pretty_print(self):
        utc = arrow.utcnow()

        # TODO replace docker
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
    """
    def test_python_datetime_pretty_print(self):
        # datetime corresponding to Gregorian ordinal
        d = date.fromordinal(736132)

        # Verify, that if 'lang' is 'de' format of date is 'month. year'
        self.assertEqual(lib.python_datetime_pretty_print(ts=d,
                                                          lang='de'), 'Jun. 2016')

        # Verify, that if 'lang' is not 'de' format of date is 'day. month.'
        self.assertEqual(lib.python_datetime_pretty_print(ts=d,
                                                          lang='en'), '17. Jun.')

        self.assertEqual(lib.python_datetime_pretty_print(ts='2016-01-01',
                                                          lang=''), '01. Jan.')

    def test_get_text_for_premisesgroup_uid(self):
        # premise, which is in db_premises and premise_group contains only one premise
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=1,
                                                            lang='de'), ('Cats are very independent', ['4']))

        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=1,
                                                            lang='en'), ('Cats are very independent', ['4']))


        # premise_group with more than one premises
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=11,
                                                            lang='de'), ('Cats are fluffy und Cats are small', ['14', '15']))

        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=11,
                                                            lang='en'), ('Cats are fluffy and Cats are small', ['14', '15']))

        # unknown language
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=11,
                                                            lang='fr'),
                         ('own language: fr Cats are fluffy unknown language: fr Cats are small', ['14', '15']))


        # premise, which is not in db_premises
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0,
                                                            lang='de'), ('', []))

        # language is empty string
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0,
                                                            lang=''), ('', []))

    def test_get_text_for_statement_uid(self):
        # id for no statement
        self.assertEqual(lib.get_text_for_statement_uid(uid=0), None)

        self.assertEqual(lib.get_text_for_statement_uid(uid='22222222'), None)
        self.assertEqual(lib.get_text_for_statement_uid(uid="str"), None)

        # id for statement, which ends with '.'
        self.assertEqual(lib.get_text_for_statement_uid(uid=1), 'We should get a cat')

        # id for statement, which ends with '!'
        self.assertEqual(lib.get_text_for_statement_uid(uid=30), 'It is important, that pets are small and fluffy')

    def test_get_text_for_conclusion(self):
        argument1 = Argument(premisegroup=1, issupportive=True, author=1, conclusion=1, issue=1)
        # 'argument' is an argument
        self.assertEqual(lib.get_text_for_conclusion(argument=argument1,
                                                     lang='de',
                                                     start_with_intro=False,
                                                     rearrange_intro=False), 'We should get a cat')

        argument2 = Argument(premisegroup=1, issupportive=False, author=1, issue=1)
        # 'argument' is a statement
        self.assertEqual(lib.get_text_for_conclusion(argument=argument2,
                                                     lang='en',
                                                     start_with_intro=True,
                                                     rearrange_intro=True), None)

        # unknown conclusion id
        argument3 = Argument(premisegroup=0, issupportive=True, author=0, conclusion=0, issue=0)
        self.assertEqual(lib.get_text_for_conclusion(argument=argument3,
                                                     lang='de',
                                                     start_with_intro=False,
                                                     rearrange_intro=True), None)

    def test_resolve_issue_uid_to_slug(self):
        # id for issue
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=1), 'town-has-to-cut-spending')
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=4), 'unterstutzung-der-sekretariate')

        # id for no issue
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=0), None)

        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=22222222), None)

