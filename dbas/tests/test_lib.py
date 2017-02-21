import unittest

from sqlalchemy import engine_from_config
from dbas import lib
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from datetime import date
from dbas.database.discussion_model import Argument

settings = add_settings_to_appconfig()

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

    def test_python_datetime_pretty_print(self):
        # datetime corresponding to Gregorian ordinal
        d = date.fromordinal(736132)

        # Verify, that if 'lang' is 'de' format of date is 'month. year'
        self.assertEqual(lib.python_datetime_pretty_print(ts=d, lang='de'), 'Jun. 2016')

        # Verify, that if 'lang' is not 'de' format of date is 'day. month.'
        self.assertEqual(lib.python_datetime_pretty_print(ts=d, lang='en'), '17. Jun.')

        self.assertEqual(lib.python_datetime_pretty_print(ts='2016-01-01', lang=''), '01. Jan.')

    def test_get_text_for_premisesgroup_uid(self):
        # premise, which is in db_premises and premise_group contains only one premise
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=2), ('cats are very independent', ['5']))

        # premise_group with more than one premises
        self.assertNotEqual(lib.get_text_for_premisesgroup_uid(uid=13), ('cats are fluffy und cats are small', ['14', '15']))

        values = lib.get_text_for_premisesgroup_uid(uid=12)
        solution1 = 'cats are fluffy and cats are small', ['15', '16']
        solution2 = 'cats are small and cats are fluffy', ['16', '15']
        if values[1] == solution1[1]:
            self.assertEqual(values, solution1)
        else:
            self.assertEqual(values, solution2)

        # premise, which is not in db_premises
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0), ('', []))

        # negative uid
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=-1), ('', []))

        # language is empty string
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0), ('', []))

    def test_get_text_for_statement_uid(self):
        # id for no statement
        self.assertEqual(lib.get_text_for_statement_uid(uid=0), None)

        self.assertEqual(lib.get_text_for_statement_uid(uid='22222222'), None)
        self.assertEqual(lib.get_text_for_statement_uid(uid="str"), None)

        # id for statement, which ends with '.'
        self.assertEqual(lib.get_text_for_statement_uid(uid=3), 'we should get a dog')

        # id for statement, which ends with '!'
        self.assertEqual(lib.get_text_for_statement_uid(uid=31), 'it is important, that pets are small and fluffy')

        # negative uid
        self.assertEqual(lib.get_text_for_statement_uid(uid=-30), None)

    def test_get_text_for_conclusion(self):
        argument1 = Argument(premisegroup=4, issupportive=True, author=1, conclusion=3, issue=1)
        # 'argument' is an argument
        self.assertEqual(lib.get_text_for_conclusion(argument=argument1,
                                                     start_with_intro=False,
                                                     rearrange_intro=False), 'we should get a dog')

        argument2 = Argument(premisegroup=1, issupportive=False, author=1, issue=1)
        # 'argument' is a statement
        self.assertEqual(lib.get_text_for_conclusion(argument=argument2,
                                                     start_with_intro=True,
                                                     rearrange_intro=True), None)

        # unknown conclusion id
        argument3 = Argument(premisegroup=0, issupportive=True, author=0, conclusion=0, issue=0)
        self.assertEqual(lib.get_text_for_conclusion(argument=argument3,
                                                     start_with_intro=False,
                                                     rearrange_intro=True), None)

    def test_resolve_issue_uid_to_slug(self):
        # id for issue
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=1), 'town-has-to-cut-spending')
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=5), 'unterstutzung-der-sekretariate')

        # id for no issue
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=0), None)
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=22222222), None)
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=-4), None)

    def test_get_all_attacking_arg_uids_from_history(self):
        none_history = None
        correct_history = "/attitude/60-/justify/60/t-/reaction/52/rebut/53"
        broken_history = "/attitude/60/justify/60/t/broooken/52/rebut/53"
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(correct_history), ['53'], "Missing element")
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(broken_history), [], "Should match nothing")
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(none_history), [], "No history has no elements in list")

    def test_get_all_arguments_by_statement(self):
        argument_list = lib.get_all_arguments_by_statement(3)
        self.assertEqual(len(argument_list), 4)
        for argument in argument_list:
            self.assertTrue(argument.uid in [4, 5, 6, 7])

        self.assertEqual(len(lib.get_all_arguments_by_statement(17, True)), 2)
        self.assertEqual(len(lib.get_all_arguments_by_statement(15, False)), 5)
        self.assertEqual(len(lib.get_all_arguments_by_statement(12, True)), 1)
        self.assertEqual(lib.get_all_arguments_by_statement(-1), None)
