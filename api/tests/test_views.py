"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import random
import string
import unittest

import hypothesis.strategies as st
from cornice.util import _JSONError
from hypothesis import given
from nose.tools import assert_equals, assert_true

from api.tests.lib import get_response, parse_status, construct_dummy_request
from api.views import user_login


def __generate_random_string(length=50) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(length))


def __payload_add_statement() -> dict:
    return {"path": "/",
            "statement": __generate_random_string(),
            "slug": "town-has-to-cut-spending",
            "issue_id": 1,
            "conclusion_id": "None",
            "attack_type": None,
            "arg_uid": None,
            "reference": None,
            "host": "i.amgro.ot",
            "supportive": None}


# ------------------------------------------------------------------------------
# Tests

class ValidateUserLoginRoute(unittest.TestCase):
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
        self.assertIsInstance(response, _JSONError)

    @given(password=st.text())
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
        self.assertIsInstance(response, _JSONError)

    def test_login_wrong_user(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': '¯\_(ツ)_/¯',
                             'password': 'thankgoditsfriday'}
        response = user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, _JSONError)


def test_server_available():
    response = get_response("hello")
    status = parse_status(response.content)
    assert_true(response.ok)
    assert_equals("ok", status)

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
