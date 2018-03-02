import json
import unittest

from api.login import validate_credentials, valid_token, token_to_database
from api.tests.lib import construct_dummy_request


class ValidateCredentialsTest(unittest.TestCase):
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


class ValidTokenTest(unittest.TestCase):
    header = 'X-Authentication'

    def test_invalid_token(self):
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': 'Walter', 'token': 'thisisnotarealtoken'})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('db_user', request.validated)

    def test_valid_token(self):
        nickname = 'Walter'
        token = 'mytoken'
        token_to_database(nickname, token)
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token(request)
        self.assertEqual(len(request.errors), 0)
        self.assertIn('db_user', request.validated)
