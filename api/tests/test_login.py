import unittest

from api.login import validate_credentials
from api.tests.lib import construct_dummy_request


class ValidateCredentials(unittest.TestCase):
    def test_valid_credentials(self):
        request = construct_dummy_request()
        request.validated = {'nickname': 'Walter',
                             'password': 'iamatestuser2016'}
        validate_credentials(request)
        self.assertEqual(0, len(request.errors))
        self.assertIn('nickname', request.validated)
        self.assertIn('token', request.validated)

    def test_invalid_credentials(self):
        request = construct_dummy_request()
        request.validated = {'nickname': 'Walter',
                             'password': 'somerandomstuffwhichisdefinitelynotapassword'}
        validate_credentials(request)
        self.assertNotIn('db_user', request.validated)
        self.assertGreater(len(request.errors), 0)
