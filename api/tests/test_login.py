import unittest

from api.login import validate_credentials
from api.tests.lib import construct_dummy_request
from api.views import user_login
from dbas.database.discussion_model import User


class ValidateCredentials(unittest.TestCase):
    def test_valid_credentials(self):
        request = construct_dummy_request()
        request.validated = {'nickname': 'Walter',
                             'password': 'iamatestuser2016'}
        validate_credentials(request)
        self.assertIn('db_user', request.validated)
        self.assertIsInstance(request.validated.get('db_user'), User)

    def test_invalid_credentials(self):
        request = construct_dummy_request()
        request.validated = {'nickname': 'Walter',
                             'password': 'somerandomstuffwhichisdefinitelynotapassword'}
        validate_credentials(request)
        self.assertNotIn('db_user', request.validated)
        self.assertGreater(len(request.errors), 0)


class ValidateUserLoginRoute(unittest.TestCase):
    def test_valid_login_attempt(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': 'Walter',
                             'password': 'iamatestuser2016'}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertIn('db_user', request.validated)
        self.assertIn('token', response)
