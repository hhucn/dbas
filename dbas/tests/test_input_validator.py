import unittest
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, VoteArgument


class InputValidatorTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.input_validator import Validator
        return Validator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_check_reaction(self):
        url = self._makeOne()

        self.assertEqual(url.check_reaction(attacked_arg_uid=1,
                                            attacking_arg_uid=1,
                                            relation='end',
                                            is_history=False), False);

        self.assertEqual(url.check_reaction(attacked_arg_uid=1,
                                            attacking_arg_uid=0,
                                            relation='end',
                                            is_history=False), True);




