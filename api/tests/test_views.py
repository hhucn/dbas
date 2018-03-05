"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import json
import unittest

import hypothesis.strategies as st
from hypothesis import given, settings
from pyramid import httpexceptions

from api.login import token_to_database
from api.tests.lib import construct_dummy_request
from api.views import user_login, hello, user_logout, whoami_fn
# ------------------------------------------------------------------------------
# Tests
from dbas.lib import get_user_by_case_insensitive_nickname


def create_request_with_token_header(nickname='Walter', token='mytoken'):
    token_to_database(get_user_by_case_insensitive_nickname(nickname), token)
    request = construct_dummy_request()
    request.headers['X-Authentication'] = json.dumps({'nickname': nickname, 'token': token})
    return request


class ValidateUserLoginLogoutRoute(unittest.TestCase):
    header = 'X-Authentication'

    def test_valid_login_attempt(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': 'Walter',
                             'password': 'iamatestuser2016'}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertIn('token', response)
        self.assertIn('nickname', response)

    def test_login_without_password(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': 'Walter'}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertNotIn('password', request.validated)
        self.assertEqual(400, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    @given(password=st.text())
    @settings(deadline=400)
    def test_login_wrong_password(self, password: str):
        pwd = password.replace('\x00', '')
        pwd = pwd.replace('iamatestuser2016', '¯\_(ツ)_/¯')
        request = construct_dummy_request()
        request.json_body = {'nickname': 'Walter',
                             'password': pwd}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_login_wrong_user(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': '¯\_(ツ)_/¯',
                             'password': 'thankgoditsfriday'}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_login_empty_user_is_not_allowed_to_login(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': '',
                             'password': 'thankgoditsfriday'}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_logout_valid_user(self):
        request = create_request_with_token_header()
        response = user_logout(request)
        self.assertEqual(len(request.errors), 0)
        self.assertEqual('ok', response['status'])

    def test_logout_invalid_user(self):
        nickname = 'Walter'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': 'notavalidtoken'})
        response = user_logout(request)
        self.assertGreater(len(request.errors), 0)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_logout_missing_header(self):
        request = construct_dummy_request()
        response = user_logout(request)
        self.assertGreater(len(request.errors), 0)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestSystemRoutes(unittest.TestCase):
    def test_server_available(self):
        request = construct_dummy_request()
        response = hello(request)
        self.assertEqual(response['status'], 'ok')

    def test_whoami_and_check_for_valid_token(self):
        nickname = 'Walter'
        request = create_request_with_token_header(nickname)
        response = whoami_fn(request)
        self.assertEqual(len(request.errors), 0)
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(response['nickname'], nickname)

# def test_add_position_should_succeed():
#     credentials = {"nickname": "Walter",
#                    "password": "iamatestuser2016"}
#     response = post_request("login", credentials)
#     content = json_to_dict(response.content)
#     payload = __payload_add_statement()
#     response = post_request("add/start_statement", payload,
#                             headers={"X-Authentication": json.dumps({"type": "user", "token": content.get("token")})})
#     assert_true(response.ok)
#
#
# def test_add_position_unsplittable_token():
#     payload = __payload_add_statement()
#     response = post_request("add/start_statement", payload,
#                             headers={"X-Authentication": json.dumps({"type": "user", "token": "I am groot"})})
#     assert_false(response.ok)
#
#
# def test_add_position_splittable_invalid_token():
#     payload = __payload_add_statement()
#     response = post_request("add/start_statement", payload,
#                             headers={"X-Authentication": json.dumps({"type": "user", "token": "Groot-iamgroot"})})
#     assert_false(response.ok)
#
#
# def test_correct_api_token():
#     api_token = generate_application_token("Walter")
#     payload = __payload_add_statement()
#     response = post_request("add/start_statement", payload,
#                             headers={"X-Authentication": json.dumps({"type": "user", "token": "Walter-" + api_token})})
#     assert_true(response.ok)
#
#
# def test_incorrect_api_token():
#     api_token = "blablablab-df---df--df"
#     payload = __payload_add_statement()
#     response = post_request("add/start_statement", payload,
#                             headers={"X-Authentication": json.dumps({"type": "user", "token": "Walter-" + api_token})})
#     assert_false(response.ok)
