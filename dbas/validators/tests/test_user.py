from cornice import Errors

import dbas.validators.user as user
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request


class Usertest(TestCaseWithConfig):
    def test_valid_user(self):
        request = construct_dummy_request()
        response = user.valid_user(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='hello', permissive=True)
        response = user.valid_user(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.valid_user(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_user_as_author_of_argument(self):
        request = construct_dummy_request()
        response = user.valid_user_as_author_of_argument(request)
        self.assertFalse(response)

        for id in ['', 'hello', 'anonymous']:
            self.config.testing_securitypolicy(userid=id, permissive=True)
            for el in ['', 'a', '0', '1', 1]:
                request = construct_dummy_request(json_body={'uid': el})
                request.validated = {}
                setattr(request, 'errors', Errors())
                response = user.valid_user_as_author_of_argument(request)
                self.assertIsInstance(response, bool)
                if id == 'anonymous' and el in ['1', 1]:
                    self.assertTrue(response)
                else:
                    self.assertFalse(response)

    def test_valid_user_as_author(self):
        request = construct_dummy_request()
        response = user.valid_user_as_author(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        response = user.valid_user_as_author(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.valid_user_as_author(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_user_as_admin(self):
        request = construct_dummy_request()
        response = user.valid_user_as_admin(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        response = user.valid_user_as_admin(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.valid_user_as_admin(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_optional_user(self):
        db_user = DBDiscussionSession.query(User).get(1)
        request = construct_dummy_request()
        response = user.valid_user_optional(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertEqual(db_user, request.validated['user'])

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        request = construct_dummy_request()
        response = user.valid_user_optional(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertEqual(db_user, request.validated['user'])


class TestValidUserAsAuthorOfStatement(TestCaseWithConfig):
    def __assertValidResponse(self, validated, response):
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('statement', validated)

    def __assertInvalidResponse(self, validated, response):
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
        self.assertNotIn('statement', validated)

    def test_missing_user_and_statement_is_false(self):
        request = construct_dummy_request()
        response = user.valid_user_as_author_of_statement(request)
        self.__assertInvalidResponse(request.validated, response)

    def test_missing_statement_id(self):
        self.config.testing_securitypolicy(userid='Christian', permissive=True)
        request = construct_dummy_request()
        response = user.valid_user_as_author_of_statement(request)
        self.__assertInvalidResponse(request.validated, response)

    def test_valid_user_and_statement_gives_statement(self):
        self.config.testing_securitypolicy(userid='Christian', permissive=True)
        request = construct_dummy_request({'statement_id': 36})
        response = user.valid_user_as_author_of_statement(request)
        self.__assertValidResponse(request.validated, response)

    def test_user_is_not_author_of_statement(self):
        self.config.testing_securitypolicy(userid='Christian', permissive=True)
        request = construct_dummy_request({'statement_id': 2})
        response = user.valid_user_as_author_of_statement(request)
        self.__assertInvalidResponse(request.validated, response)
