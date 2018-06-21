import json
import unittest

from api.login import validate_credentials, valid_token, token_to_database, valid_token_optional
from dbas.lib import get_user_by_case_insensitive_nickname
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
    header = 'X-Authentication'

    def test_invalid_token(self):
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': 'Walter', 'token': 'thisisnotarealtoken'})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('user', request.validated)

    def test_valid_token(self):
        nickname = 'Walter'
        token = 'mytoken'
        token_to_database(get_user_by_case_insensitive_nickname(nickname), token)
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token(request)
        self.assertEqual(len(request.errors), 0)
        self.assertIn('user', request.validated)

    def test_invalid_nickname(self):
        nickname = 'Walter_not_in_db'
        token = 'mytoken'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('user', request.validated)

    def test_anonymous_user_never_authorized(self):
        nickname = 'anonymous'
        token = 'mytoken'
        token_to_database(get_user_by_case_insensitive_nickname(nickname), token)
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('user', request.validated)

    def test_anonymous_user_ignore_optional(self):
        nickname = 'anonymous'
        token = 'mytoken'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token_optional(request)
        self.assertListEqual(request.errors, [])
        self.assertIn('user', request.validated)
