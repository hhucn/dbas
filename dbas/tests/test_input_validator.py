import unittest


class InputValidatorTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.input_validator import Validator
        return Validator
