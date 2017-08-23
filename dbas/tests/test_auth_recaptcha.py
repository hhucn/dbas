import unittest

from pyramid import testing
from dbas.auth.recaptcha import validate_recaptcha


class AuthRecaptchaTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_validate_recaptcha(self):
        success, error = validate_recaptcha('somestring')
        self.assertFalse(success)
        self.assertTrue(error)
