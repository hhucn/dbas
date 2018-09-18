"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import json
import unittest
from typing import List

import hypothesis.strategies as st
import transaction
from hypothesis import given, settings
from pyramid import httpexceptions
from pyramid.interfaces import IRequest
from pyramid.response import Response
from pyramid.testing import DummyRequest

import api.views as apiviews
from admin.lib import generate_application_token
from api.login import token_to_database
# ------------------------------------------------------------------------------
# Tests
from api.models import Reference
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, StatementReferences
from dbas.lib import get_user_by_case_insensitive_nickname, Relations, Attitudes
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig


def create_request_with_token_header(json_body=None, match_dict=None, nickname='Walter', token='mytoken') -> IRequest:
    token_to_database(get_user_by_case_insensitive_nickname(nickname), token)
    request: IRequest = construct_dummy_request(json_body=json_body, match_dict=match_dict)
    request.headers['X-Authentication'] = json.dumps({'nickname': nickname, 'token': token})
    return request


def create_request_with_api_token_header(json_body=None, match_dict=None, nickname='Walter'):
    token = generate_application_token("TEST_API_TOKEN_FOR_" + nickname)
    request: IRequest = construct_dummy_request(json_body=json_body, match_dict=match_dict)
    request.headers['X-Authentication'] = json.dumps({'nickname': nickname, 'token': token})
    return request


class ValidateUserLoginLogoutRoute(unittest.TestCase):
    header = 'X-Authentication'

    def test_valid_login_attempt(self):
        request = construct_dummy_request({
            'nickname': 'Walter',
            'password': 'iamatestuser2016'
        })
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
        request = construct_dummy_request({
            'nickname': 'Walter',
            'password': pwd
        })
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_login_wrong_user(self):
        request = construct_dummy_request({
            'nickname': '¯\_(ツ)_/¯',
            'password': 'thankgoditsfriday'
        })
        response = apiviews.user_login(request)
        self.assertIn('nickname', request.validated)
        self.assertIn('password', request.validated)
        self.assertEqual(401, response.status_code)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_login_empty_user_is_not_allowed_to_login(self):
        request = construct_dummy_request({
            'nickname': '',
            'password': 'thankgoditsfriday'
        })
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
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': self.position_cat_or_dog.uid
        })
        response = apiviews.discussion_attitude(request)
        self.assertTrue(response)
        self.assertIsInstance(response, dict)
        self.assertIn('position', request.validated)
        self.assertIn('issue', request.validated)
        self.assertIn('user', request.validated)

    def test_wrong_slug_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': '',
            'position_id': 2
        })
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

        request = construct_dummy_request(match_dict={
            'slug': 'this-is-not-a-valid-slug',
            'position_id': 2
        })
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_position_id_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': self.position_town.uid
        })
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': -1
        })
        response = apiviews.discussion_attitude(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestDiscussionJustifyStatement(TestCaseWithConfig):
    def test_successful_discussion_justify_statement(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'statement_id': self.statement_cat_or_dog.uid,
            'attitude': Attitudes.AGREE.value
        })
        response = apiviews.discussion_justify_statement(request)
        self.assertTrue(response)
        self.assertIsInstance(response, dict)
        self.assertIn('statement', request.validated)
        self.assertIn('issue', request.validated)
        self.assertIn('user', request.validated)
        self.assertIn('attitude', request.validated)

    def test_wrong_slug_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_town.slug,
            'statement_id': self.statement_cat_or_dog.uid,
            'attitude': Attitudes.AGREE.value
        })
        response = apiviews.discussion_justify_statement(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_statement_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'statement_id': -1,
            'attitude': Attitudes.AGREE.value
        })
        response = apiviews.discussion_justify_statement(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_attitude_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'statement_id': self.statement_cat_or_dog.uid,
            'attitude': 'not-an-attitude'
        })
        response = apiviews.discussion_justify_statement(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestDiscussionJustifyStatementPOST(TestCaseWithConfig):

    def test_add_valid_reason(self):
        # Add position
        request = create_request_with_token_header(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'statement_id': 2,
            'attitude': Attitudes.DISAGREE.value
        }, json_body={'reason': "because i need to"})

        response: Response = apiviews.add_premise_to_statement(request)
        self.assertEqual(response.status_code, 303, response.body)

    def test_invalid_body(self):
        request: IRequest = create_request_with_token_header(match_dict={
            'slug': self.issue_cat_or_dog.slug
        }, json_body={
            'position': 'we should do something entirely else'
        })
        response: Response = apiviews.add_premise_to_statement(request)
        self.assertEqual(response.status_code, 400)

    def test_valid_reference_should_be_assigned_to_new_statement(self):
        test_reference = 'awesome reference'
        request: IRequest = create_request_with_token_header(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'statement_id': 2,
            'attitude': Attitudes.DISAGREE.value
        }, json_body={
            'reason': 'i am groot',
            'reference': test_reference
        })
        response: Response = apiviews.add_premise_to_statement(request)
        added_references: List[StatementReferences] = DBDiscussionSession.query(StatementReferences) \
            .filter_by(reference=test_reference).all()

        self.assertGreater(len(added_references), 0)
        self.assertEqual(request.validated['reference'], test_reference)
        self.assertEqual(response.status_code, 303)

        DBDiscussionSession.query(StatementReferences).filter_by(reference=test_reference).delete()
        transaction.commit()


class TestDiscussionJustifyArgument(TestCaseWithConfig):
    def test_successful_discussion_justify_argument(self):
        request: DummyRequest = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': self.argument_cat_or_dog.uid,
            'attitude': Attitudes.AGREE.value,
            'relation': Relations.UNDERMINE.value
        })
        response = apiviews.discussion_justify_argument(request)
        self.assertTrue(response)
        self.assertIsInstance(response, dict)
        self.assertIn('argument', request.validated)
        self.assertIn('issue', request.validated)
        self.assertIn('user', request.validated)
        self.assertIn('attitude', request.validated)
        self.assertIn('relation', request.validated)

    def test_wrong_slug_returns_error(self):
        request: DummyRequest = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': self.argument_town.uid,
            'attitude': Attitudes.AGREE.value,
            'relation': Relations.UNDERMINE.value
        })
        response = apiviews.discussion_justify_argument(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_statement_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': -1,
            'attitude': Attitudes.AGREE.value,
            'relation': Relations.UNDERMINE.value
        })
        response = apiviews.discussion_justify_argument(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_attitude_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': self.argument_cat_or_dog.uid,
            'attitude': 'not-an-attitude',
            'relation': Relations.UNDERMINE.value
        })
        response = apiviews.discussion_justify_argument(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_relation_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': self.argument_cat_or_dog.uid,
            'attitude': Attitudes.AGREE.value,
            'relation': 'not-a-valid-relation'
        })
        response = apiviews.discussion_justify_argument(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestDiscussionJustifyArgumentPOST(TestCaseWithConfig):
    def test_add_valid_reason(self):
        # Add position
        request: IRequest = create_request_with_token_header(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': '18',
            'attitude': 'agree',
            'relation': 'undercut'
        }, json_body={
            'reason': 'because i need to'
        })

        response: Response = apiviews.add_premise_to_argument(request)
        self.assertEqual(response.status_code, 303, response.body)

    def test_invalid_body(self):
        request = create_request_with_token_header(match_dict={'slug': self.issue_cat_or_dog.slug})

        request.json_body = {'position': 'we should do something entirely else'}

        response: Response = apiviews.add_premise_to_argument(request)
        self.assertEqual(response.status_code, 400)


class TestDiscussionReaction(TestCaseWithConfig):
    def test_invalid_slug_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-doggy_dog',
            'arg_id_user': 2,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 16,
        })
        response = apiviews.discussion_reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_user_argument_does_not_belong_to_issue_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 45,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 16,
        })
        response = apiviews.discussion_reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_sys_argument_does_not_belong_to_issue_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 2,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 45,
        })
        response = apiviews.discussion_reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_page_failure_mode(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 2,
            'relation': 'invalid-relation',
            'arg_id_sys': 16,
        })
        response = apiviews.discussion_reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)


class TestDiscussionFinish(TestCaseWithConfig):
    def test_valid_slug_and_issue_returns_bubbles(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': self.argument_cat_or_dog.uid
        })
        response = apiviews.discussion_finish(request)
        self.assertIsInstance(response, dict)
        self.assertIn('bubbles', response)

    def test_argument_does_not_belong_to_issue(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_cat_or_dog.slug,
            'argument_id': self.argument_town.uid
        })
        response = apiviews.discussion_finish(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)
        self.assertEqual(response.status_code, 400)

    def test_issue_is_disabled(self):
        request = construct_dummy_request(match_dict={
            'slug': self.issue_disabled.slug,
            'argument_id': self.argument_town.uid
        })
        response: Response = apiviews.discussion_finish(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)
        self.assertEqual(response.status_code, 410)


class TestPosition(TestCaseWithConfig):
    test_body = {
        'position': 'we should do something entirely else',
        'reason': 'because i need to'
    }

    def test_add_valid_position(self):
        # Add position
        request = create_request_with_token_header(match_dict={'slug': self.issue_cat_or_dog.slug},
                                                   json_body=self.test_body)

        response: Response = apiviews.add_position_with_premise(request)
        self.assertEqual(response.status_code, 303)

        # Check if position was added
        response: dict = apiviews.discussion_init(
            construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug}))

        positions = [position.texts[0] for position in response['positions']]
        self.assertIn(self.test_body['position'], positions)

    def test_invalid_body(self):
        request = create_request_with_token_header(match_dict={'slug': self.issue_cat_or_dog.slug})

        request.json_body = {'position': 'we should do something entirely else'}

        response: Response = apiviews.add_position_with_premise(request)
        self.assertEqual(response.status_code, 400)

    def test_without_authentication(self):
        request = construct_dummy_request(match_dict={'slug': self.issue_cat_or_dog.slug})

        request.json_body = self.test_body

        response: Response = apiviews.add_position_with_premise(request)
        self.assertEqual(response.status_code, 401)


class TestUser(TestCaseWithConfig):
    test_body = {
        'firstname': 'This',
        'lastname': 'Is',
        'nickname': 'TEST-nick',
        'service': 'Jeb?',
        'locale': 'de_DE',
        'email': 'bla@bla.de',
        'gender': 'n',
        'id': 1236
    }

    def test_add_user(self):
        request = create_request_with_api_token_header(json_body=self.test_body)
        response: Response = apiviews.ApiUser(request).collection_post()
        print(response)
        self.assertIsInstance(response, dict)
        self.assertIn('id', response)

    def test_add_user_with_user_token(self):
        request = create_request_with_token_header(json_body=self.test_body)
        response: Response = apiviews.ApiUser(request).collection_post()
        self.assertGreaterEqual(response.status_code, 400)

    def assertUser(self, user):  # camel case to be consistent with unittest
        """
        Asserts that the user-data is in correct shape.
        :param user: Something which should be a user.
        """
        self.assertIsInstance(user, dict)
        self.assertIn('id', user)
        self.assertIn('nickname', user)

    def test_list_users(self):
        response = apiviews.ApiUser(DummyRequest()).collection_get()
        self.assertIsInstance(response, list)
        for user in response:
            self.assertUser(user)

    def test_single_user(self):
        tobias_krauthoff = {'id': 2, 'nickname': 'Tobias'}
        response = apiviews.ApiUser(construct_dummy_request(match_dict={'id': 2})).get()
        self.assertUser(response)
        self.assertDictEqual(response, tobias_krauthoff)


class TestReferences(TestCaseWithConfig):
    def __assert_valid_references(self, response, expected_references: List[Reference] = None):
        references = response.get('references')
        self.assertIn('references', response)
        self.assertIsInstance(references, list)
        if expected_references:
            expected = [ref.uid for ref in expected_references]
            actual = [ref.uid for ref in references]
            self.assertCountEqual(expected, actual)

    def test_missing_parameters_should_return_error(self):
        request: IRequest = construct_dummy_request(params={})
        response = apiviews.get_references(request)
        self.__assert_valid_references(response, [])

    def test_missing_path_should_return_error(self):
        request: IRequest = construct_dummy_request()
        request.host = 'foo'
        response = apiviews.get_references(request)
        self.__assert_valid_references(response, [])

    def test_missing_host_should_return_error(self):
        request: IRequest = construct_dummy_request()
        request.path = 'foo'
        response = apiviews.get_references(request)
        self.__assert_valid_references(response, [])

    def test_empty_list_when_no_references_in_database(self):
        request: IRequest = construct_dummy_request()
        request.host = 'foo'
        request.path = 'foo'
        response = apiviews.get_references(request)
        self.__assert_valid_references(response, [])

    def test_query_one_reference_should_return_list_of_references(self):
        request: IRequest = construct_dummy_request()
        request.host = 'localhost:3449'
        request.path = '/'
        response = apiviews.get_references(request)
        self.__assert_valid_references(response, [Reference(self.statement_reference)])
