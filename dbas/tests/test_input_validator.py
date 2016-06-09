import unittest

import os

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config

from dbas import DBDiscussionSession

dir_name = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
settings = appconfig('config:' + os.path.join(dir_name, 'development.ini'))


class InputValidatorTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.input_validator import Validator
        return Validator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_check_reaction(self):
        reaction = self._makeOne()

        DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

        # undermine

        # relation_ishistory
        undermine_true = reaction.check_reaction(attacked_arg_uid=2,
                                                 attacking_arg_uid=19,
                                                 relation='undermine',
                                                 is_history=False)
        self.assertEqual(undermine_true, True)

        undermine_not_db_attacking_arg_false = reaction.check_reaction(attacked_arg_uid=2,
                                                                       attacking_arg_uid=1,
                                                                       relation='undermine',
                                                                       is_history=False)
        self.assertEqual(undermine_not_db_attacking_arg_false, False)

        undermine_db_attacked_arg_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                  attacking_arg_uid=19,
                                                                  relation='undermine',
                                                                  is_history=False)
        self.assertEqual(undermine_db_attacked_arg_false, False)

        undermine_false = reaction.check_reaction(attacked_arg_uid=0,
                                                  attacking_arg_uid=0,
                                                  relation='undermine',
                                                  is_history=False)
        self.assertEqual(undermine_false, False)

        # undercut
        undercut_true = reaction.check_reaction(attacked_arg_uid=1,
                                                attacking_arg_uid=17,
                                                relation='undercut',
                                                is_history=False)
        self.assertEqual(undercut_true, True)

        undercut_false = reaction.check_reaction(attacked_arg_uid=0,
                                                 attacking_arg_uid=0,
                                                 relation='undercut',
                                                 is_history=False)
        self.assertEqual(undercut_false, False)

        # rebut
        rebut_not_db_attacked_arg_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                  attacking_arg_uid=35,
                                                                  relation='rebut',
                                                                  is_history=False)
        self.assertEqual(rebut_not_db_attacked_arg_false, False)

        rebut_not_db_attacking_arg_false = reaction.check_reaction(attacked_arg_uid=31,
                                                                   attacking_arg_uid=1,
                                                                   relation='rebut',
                                                                   is_history=False)
        self.assertEqual(rebut_not_db_attacking_arg_false, False)

        rebut_not_db_attacked_arg_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                  attacking_arg_uid=35,
                                                                  relation='rebut',
                                                                  is_history=False)
        self.assertEqual(rebut_not_db_attacked_arg_false, False)

        # db_attacked_arg and db_attacking_arg are False
        rebut_false = reaction.check_reaction(attacked_arg_uid=0,
                                              attacking_arg_uid=0,
                                              relation='rebut',
                                              is_history=False)
        self.assertEqual(rebut_false, False)

        rebut_true = reaction.check_reaction(attacked_arg_uid=31,
                                             attacking_arg_uid=35,
                                             relation='rebut',
                                             is_history=False)
        self.assertEqual(rebut_true, True)

        # end
        end_attacking_arg_uid_not_zero_true = reaction.check_reaction(attacked_arg_uid=1,
                                                                      attacking_arg_uid=0,
                                                                      relation='end',
                                                                      is_history=False)
        self.assertEqual(end_attacking_arg_uid_not_zero_true, True)

        end_attacking_arg_uid_not_zero_false = reaction.check_reaction(attacked_arg_uid=1,
                                                                       attacking_arg_uid=1,
                                                                       relation='end',
                                                                       is_history=False)
        self.assertEqual(end_attacking_arg_uid_not_zero_false, False)

        end_not_is_history_false = reaction.check_reaction(attacked_arg_uid=1,
                                                           attacking_arg_uid=0,
                                                           relation='end',
                                                           is_history=True)
        self.assertEqual(end_not_is_history_false, False)

