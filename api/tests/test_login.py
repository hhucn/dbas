import unittest

from api.login import validate_credentials, valid_token
from dbas.tests.utils import construct_dummy_request


class ValidateCredentialsTest(unittest.TestCase):
    def test_valid_credentials(self):
        request = construct_dummy_request()
        request.validated = {
            'nickname': 'Walter',
            'password': 'iamatestuser2016'
        }
        validate_credentials(request)
        self.assertEqual(0, len(request.errors))
        self.assertIn('nickname', request.validated)
        self.assertIn('token', request.validated)

    def test_invalid_credentials(self):
        request = construct_dummy_request()
        request.validated = {
            'nickname': 'Walter',
            'password': 'somerandomstuffwhichisdefinitelynotapassword'
        }
        validate_credentials(request)
        self.assertNotIn('user', request.validated)
        self.assertGreater(len(request.errors), 0)


class ValidTokenTest(unittest.TestCase):
    header = 'Authorization'

    def test_invalid_token(self):
        request = construct_dummy_request()
        request.headers[self.header] = 'Bearer thisisnotarealtoken'
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('user', request.validated)

    def test_valid_token(self):
        nickname = 'Walter'
        # token = jwt.encode({"nickname": nickname}, request.registry.settings['secret_key'], algorithm='ES256')
        request = construct_dummy_request()
        request.headers[self.header] = 'Bearer ' + token
        valid_token(request)
        self.assertEqual(len(request.errors), 0)
        self.assertIn('user', request.validated)
