import transaction
import unittest

import dbas.input_validator as iv
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
from dbas.lib import Relations


class InputValidatorTests(unittest.TestCase):

    def test_is_integer(self):
        # conditions_response
        ignore_empty_case_len_zero_true = iv.is_integer(variable='',
                                                        ignore_empty_case=True)
        self.assertEqual(ignore_empty_case_len_zero_true, True)

        long_string_false = iv.is_integer(variable=',' * 1000 + '30' + '?' * 1000,
                                          ignore_empty_case=True)
        self.assertFalse(long_string_false)

        ignore_empty_case_len_false = iv.is_integer(variable='str', ignore_empty_case=True)
        self.assertFalse(ignore_empty_case_len_false)

        not_ignore_empty_case_len_zero_false = iv.is_integer(variable='', ignore_empty_case=False)
        self.assertFalse(not_ignore_empty_case_len_zero_false)

        not_ignore_empty_case_len_false = iv.is_integer(variable='str', ignore_empty_case=False)
        self.assertFalse(not_ignore_empty_case_len_false)

        ignore_empty_case_int_true = iv.is_integer(variable=123, ignore_empty_case=True)
        self.assertTrue(ignore_empty_case_int_true)

        not_ignore_empty_case_int_true = iv.is_integer(variable=1, ignore_empty_case=False)
        self.assertTrue(not_ignore_empty_case_int_true)

        input_none_false = iv.is_integer(variable=None, ignore_empty_case=True)
        self.assertFalse(input_none_false)

        input_array_false = iv.is_integer(variable=[1, 2, 3, 'str'], ignore_empty_case=True)
        self.assertFalse(input_array_false)

    def test_check_reaction_undermine(self):
        DBDiscussionSession.query(Argument).get(1).set_disabled(True)
        transaction.commit()
        # undermine
        undermine_true = iv.check_reaction(attacked_arg_uid=3, attacking_arg_uid=20, relation=Relations.UNDERMINE)
        self.assertTrue(undermine_true, True)

        undermine_uid_array_false = iv.check_reaction(attacked_arg_uid=[2, 3, 4], attacking_arg_uid=[2, 3, 4],
                                                      relation=Relations.UNDERMINE)
        self.assertFalse(undermine_uid_array_false)

        undermine_negative_uid_false = iv.check_reaction(attacked_arg_uid=-2, attacking_arg_uid=-19,
                                                         relation=Relations.UNDERMINE)
        self.assertFalse(undermine_negative_uid_false)

        # relation_conditions_response
        undermine_not_db_attacking_arg_false = iv.check_reaction(attacked_arg_uid=2, attacking_arg_uid=1,
                                                                 relation=Relations.UNDERMINE)
        self.assertFalse(undermine_not_db_attacking_arg_false)

        undermine_db_attacked_arg_false = iv.check_reaction(attacked_arg_uid=1, attacking_arg_uid=19,
                                                            relation=Relations.UNDERMINE)
        self.assertFalse(undermine_db_attacked_arg_false)

        undermine_false = iv.check_reaction(attacked_arg_uid=0, attacking_arg_uid=0, relation=Relations.UNDERMINE)
        self.assertFalse(undermine_false)

        undermine_empty_string_false = iv.check_reaction(attacked_arg_uid='', attacking_arg_uid='',
                                                         relation=Relations.UNDERMINE)
        self.assertFalse(undermine_empty_string_false)

        undermine_string_false = iv.check_reaction(attacked_arg_uid='2str/', attacking_arg_uid='19str',
                                                   relation=Relations.UNDERMINE)
        self.assertFalse(undermine_string_false)

    def test_check_reaction_undercut(self):
        # undercut
        undercut_true = iv.check_reaction(attacked_arg_uid=42, attacking_arg_uid=43, relation=Relations.UNDERCUT)
        self.assertTrue(undercut_true)

        undercut_false = iv.check_reaction(attacked_arg_uid=0, attacking_arg_uid=0, relation=Relations.UNDERCUT)
        self.assertFalse(undercut_false)

        undercut_empty_string_false = iv.check_reaction(attacked_arg_uid='', attacking_arg_uid='', relation=Relations.UNDERCUT)
        self.assertFalse(undercut_empty_string_false)

        undercut_string_false = iv.check_reaction(attacked_arg_uid='1str/', attacking_arg_uid='17str',
                                                  relation=Relations.UNDERCUT)
        self.assertFalse(undercut_string_false)

    def test_check_reaction_rebut(self):
        # rebut
        rebut_true = iv.check_reaction(attacked_arg_uid=58, attacking_arg_uid=51, relation=Relations.REBUT)
        self.assertTrue(rebut_true)

        rebut_not_db_attacked_arg_false = iv.check_reaction(attacked_arg_uid=1, attacking_arg_uid=35, relation=Relations.REBUT)
        self.assertFalse(rebut_not_db_attacked_arg_false)

        rebut_not_db_attacking_arg_false = iv.check_reaction(attacked_arg_uid=31, attacking_arg_uid=1, relation=Relations.REBUT)
        self.assertFalse(rebut_not_db_attacking_arg_false)

        rebut_not_db_attacked_arg_false = iv.check_reaction(attacked_arg_uid=1, attacking_arg_uid=35, relation=Relations.REBUT)
        self.assertFalse(rebut_not_db_attacked_arg_false)

        # db_attacked_arg and db_attacking_arg are False
        rebut_false = iv.check_reaction(attacked_arg_uid=0, attacking_arg_uid=0, relation=Relations.REBUT)
        self.assertFalse(rebut_false)

        rebut_empty_string_false = iv.check_reaction(attacked_arg_uid='', attacking_arg_uid='', relation=Relations.REBUT)
        self.assertFalse(rebut_empty_string_false)

        rebut_string_false = iv.check_reaction(attacked_arg_uid='31str/', attacking_arg_uid='35str', relation=Relations.REBUT)
        self.assertFalse(rebut_string_false)

    def test_check_reaction_end(self):
        # end
        end_attacking_arg_uid_not_zero_true = iv.check_reaction(attacked_arg_uid=1, attacking_arg_uid=0, relation='end')
        self.assertFalse(end_attacking_arg_uid_not_zero_true)

        end_attacking_arg_uid_not_zero_false = iv.check_reaction(attacked_arg_uid=1, attacking_arg_uid=1,
                                                                 relation='end')
        self.assertFalse(end_attacking_arg_uid_not_zero_false)

        end_not_is_history_false = iv.check_reaction(attacked_arg_uid=1, attacking_arg_uid=0, relation='end')
        self.assertFalse(end_not_is_history_false)

        end_empty_string_false = iv.check_reaction(attacked_arg_uid='', attacking_arg_uid='', relation='end')
        self.assertFalse(end_empty_string_false)

        end_string_false = iv.check_reaction(attacked_arg_uid='1str/', attacking_arg_uid='str', relation='end')
        self.assertFalse(end_string_false)

        end_string_long_false = iv.check_reaction(attacked_arg_uid=',' * 1000 + '30' + 'str' * 1000,
                                                  attacking_arg_uid=',' * 1000 + '30' + 'str' * 1000, relation='end')
        self.assertFalse(end_string_long_false)

        # no relation
        no_relation_false = iv.check_reaction(attacked_arg_uid='', attacking_arg_uid='3', relation='')
        self.assertFalse(no_relation_false)

        no_relation_uid_none_false = iv.check_reaction(attacked_arg_uid=None, attacking_arg_uid=None, relation='')
        self.assertFalse(no_relation_uid_none_false)

    def test_check_belonging_of_statement(self):
        self.assertTrue(iv.check_belonging_of_statement(2, 3))
        self.assertFalse(iv.check_belonging_of_statement(2, 39))

    def test_check_belonging_of_premisegroups(self):
        self.assertTrue(iv.check_belonging_of_premisegroups(2, [2, 3]))
        self.assertFalse(iv.check_belonging_of_premisegroups(2, [2, 39]))

    def test_is_position(self):
        self.assertTrue(iv.is_position(1))
        self.assertTrue(iv.is_position(2))
        self.assertFalse(iv.is_position(9))

    def test_related_with_undermine(self):
        self.assertTrue(iv.related_with_undermine(3, 20))
        self.assertFalse(iv.related_with_undermine(3, 22))

    def test_related_with_undercut(self):
        self.assertTrue(iv.related_with_undercut(42, 43))
        self.assertFalse(iv.related_with_undercut(42, 44))

    def test_related_with_rebut(self):
        self.assertTrue(iv.related_with_rebut(58, 51))
        self.assertFalse(iv.related_with_rebut(58, 52))

    def test_related_with_support(self):
        self.assertTrue(iv.related_with_support(11, 12))
        self.assertFalse(iv.related_with_support(11, 13))

    def test_get_relation_between_arguments(self):
        self.assertEqual(iv.get_relation_between_arguments(3, 20), Relations.UNDERMINE)
        self.assertEqual(iv.get_relation_between_arguments(42, 43), Relations.UNDERCUT)
        self.assertEqual(iv.get_relation_between_arguments(58, 51), Relations.REBUT)
        self.assertEqual(iv.get_relation_between_arguments(11, 12), Relations.SUPPORT)
        self.assertIsNone(iv.get_relation_between_arguments(11, 28))

    def test_is_argument_forbidden(self):
        DBDiscussionSession.query(Argument).get(1).set_disabled(True)
        transaction.commit()
        self.assertTrue(iv.is_argument_forbidden(1))
        self.assertFalse(iv.is_argument_forbidden(9))
