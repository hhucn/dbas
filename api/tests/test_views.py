"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import json
import unittest

import hypothesis.strategies as st
from hypothesis import given, settings
from pyramid import httpexceptions

import api.views as apiviews
from api.login import token_to_database
# ------------------------------------------------------------------------------
# Tests
from dbas.database.discussion_model import Issue
from dbas.lib import get_user_by_case_insensitive_nickname
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig


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
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertIn('token', response)
        self.assertIn('nickname', response)

    def test_login_without_password(self):
        request = construct_dummy_request()
        request.json_body = {'nickname': 'Walter'}
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertNotIn('password', request.validated)
        self.assertEqual(400, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    @given(password=st.text())
    @settings(deadline=1000)
    def test_login_wrong_password(self, password: str):
        pwd = password.replace('\x00', '')
        pwd = pwd.replace('iamatestuser2016', '¯\_(ツ)_/¯')
        request = construct_dummy_request()
        request.json_body = {'nickname': 'Walter',
                             'password': pwd}
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_login_wrong_user(self):
        request = construct_dummy_request({'nickname': '¯\_(ツ)_/¯',
                                           'password': 'thankgoditsfriday'})
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_login_empty_user_is_not_allowed_to_login(self):
        request = construct_dummy_request({'nickname': '',
                                           'password': 'thankgoditsfriday'})
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_logout_valid_user(self):
        request = create_request_with_token_header()
        response = apiviews.user_logout(request)
        self.assertEqual(len(request.errors), 0)
        self.assertEqual('ok', response['status'])

    def test_logout_invalid_user(self):
        nickname = 'Walter'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': 'notavalidtoken'})
        response = apiviews.user_logout(request)
        self.assertGreater(len(request.errors), 0)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_logout_missing_header(self):
        request = construct_dummy_request()
        response = apiviews.user_logout(request)
        self.assertGreater(len(request.errors), 0)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestSystemRoutes(unittest.TestCase):
    def test_server_available(self):
        request = construct_dummy_request()
        response = apiviews.hello(request)
        self.assertEqual(response['status'], 'ok')

    def test_whoami_and_check_for_valid_token(self):
        nickname = 'Walter'
        request = create_request_with_token_header(nickname)
        response = apiviews.whoami_fn(request)
        self.assertEqual(len(request.errors), 0)
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(response['nickname'], nickname)


class TestIssues(unittest.TestCase):
    def test_get_issues(self):
        request = construct_dummy_request()
        response = apiviews.get_issues(request)
        self.assertIsInstance(response, list)
        for issue in response:
            self.assertIsInstance(issue, Issue)


class TestDiscussionAttitude(TestCaseWithConfig):
    def test_successful_discussion_attitude(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
                                                      'position_id': self.position_cat_or_dog.uid})
        response = apiviews.discussion_attitude(request)
        self.assertTrue(response)
        self.assertIsInstance(response, dict)
        self.assertIn('position', request.validated)
        self.assertIn('issue', request.validated)
        self.assertIn('user', request.validated)

    def test_wrong_slug_returns_error(self):
        request = construct_dummy_request(match_dict={'slug': '',
                                                      'position_id': 2})
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

        request = construct_dummy_request(match_dict={'slug': 'this-is-not-a-valid-slug',
                                                      'position_id': 2})
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_position_id_returns_error(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
                                                      'position_id': self.position_town.uid})
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
                                                      'position_id': -1})
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestDiscussionJustifyStatement(TestCaseWithConfig):
    def test_successful_discussion_justify_statement(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
                                                      'statement_id': self.statement_cat_or_dog.uid,
                                                      'attitude': 'agree'})
        response = apiviews.discussion_justify_statement(request)
        self.assertTrue(response)
        self.assertIsInstance(response, dict)
        self.assertIn('statement', request.validated)
        self.assertIn('issue', request.validated)
        self.assertIn('user', request.validated)
        self.assertIn('attitude', request.validated)

    def test_wrong_slug_returns_error(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_town.slug,
                                                      'statement_id': self.statement_cat_or_dog.uid,
                                                      'attitude': 'agree'})
        response = apiviews.discussion_justify_statement(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_statement_returns_error(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
                                                      'statement_id': -1,
                                                      'attitude': 'agree'})
        response = apiviews.discussion_justify_statement(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_attitude_returns_error(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
                                                      'statement_id': self.statement_cat_or_dog.uid,
                                                      'attitude': 'not-an-attitude'})
        response = apiviews.discussion_justify_statement(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    # def test_wrong_slug_returns_error(self):
    #     request = construct_dummy_request(match_dict={'slug': '',
    #                                                   'position_id': 2})
    #     response = apiviews.discussion_attitude(request)
    #     self.assertIsInstance(response, httpexceptions.HTTPError)
    #
    #     request = construct_dummy_request(match_dict={'slug': 'this-is-not-a-valid-slug',
    #                                                   'position_id': 2})
    #     response = apiviews.discussion_attitude(request)
    #     self.assertIsInstance(response, httpexceptions.HTTPError)
    #
    # def test_wrong_position_id_returns_error(self):
    #     request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
    #                                                   'position_id': self.position_town.uid})
    #     response = apiviews.discussion_attitude(request)
    #     self.assertIsInstance(response, httpexceptions.HTTPError, 'Position does not belong to issue')
    #
    #     request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug,
    #                                                   'position_id': -1})
    #     response = apiviews.discussion_attitude(request)
    #     self.assertIsInstance(response, httpexceptions.HTTPError)
