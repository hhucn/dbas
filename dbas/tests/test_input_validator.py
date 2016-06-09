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

        # relation_ishistory
        end_true = reaction.check_reaction(attacked_arg_uid=1,
                                           attacking_arg_uid=0,
                                           relation='end',
                                           is_history=False)
        self.assertEqual(end_true, True)

        end_false = reaction.check_reaction(attacked_arg_uid=1,
                                            attacking_arg_uid=1,
                                            relation='end',
                                            is_history=False)
        self.assertEqual(end_false, False)


        DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

        rebut_false = reaction.check_reaction(attacked_arg_uid=1,
                                              attacking_arg_uid=0,
                                              relation='rebut',
                                              is_history=False)
        self.assertEqual(rebut_false, False)


