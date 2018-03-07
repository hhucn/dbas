import unittest

from cornice import Errors
from pyramid import testing

import dbas.validators.user as user


class Usertest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_valid_user(self):
        request = testing.DummyRequest(json_body={})
        request.validated = {}
        setattr(request, 'errors', Errors())
        response = user.valid_user(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='hello', permissive=True)
        response = user.valid_user(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.valid_user(request)
        self.assertTrue(response)
        self.assertEqual(bool, type(response))

    def test_valid_user_as_author_of_statement(self):
        request = testing.DummyRequest()
        request.validated = {}
        setattr(request, 'errors', Errors())
        response = user.valid_user_as_author_of_statement(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        for id in ['', 'hello', 'anonymous']:
            self.config.testing_securitypolicy(userid=id, permissive=True)
            for el in ['', 'a', '0', '1', 1]:
                request = testing.DummyRequest(json_body={'uid': el})
                request.validated = {}
                setattr(request, 'errors', Errors())
                response = user.valid_user_as_author_of_statement(request)
                self.assertEqual(bool, type(response))
                if id == 'anonymous' and el in ['1', 1]:
                    self.assertTrue(response)
                else:
                    self.assertFalse(response)

    def test_valid_user_as_author_of_argument(self):
        request = testing.DummyRequest()
        request.validated = {}
        setattr(request, 'errors', Errors())
        response = user.valid_user_as_author_of_argument(request)
        self.assertFalse(response)

        for id in ['', 'hello', 'anonymous']:
            self.config.testing_securitypolicy(userid=id, permissive=True)
            for el in ['', 'a', '0', '1', 1]:
                request = testing.DummyRequest(json_body={'uid': el})
                request.validated = {}
                setattr(request, 'errors', Errors())
                response = user.valid_user_as_author_of_argument(request)
                self.assertEqual(bool, type(response))
                if id == 'anonymous' and el in ['1', 1]:
                    self.assertTrue(response)
                else:
                    self.assertFalse(response)

    def test_valid_user_as_author(self):
        request = testing.DummyRequest()
        request.validated = {}
        setattr(request, 'errors', Errors())
        response = user.valid_user_as_author(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        response = user.valid_user_as_author(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.valid_user_as_author(request)
        self.assertTrue(response)
        self.assertEqual(bool, type(response))

    def test_valid_user_as_admin(self):
        request = testing.DummyRequest()
        request.validated = {}
        setattr(request, 'errors', Errors())
        response = user.valid_user_as_admin(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        response = user.valid_user_as_admin(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.valid_user_as_admin(request)
        self.assertTrue(response)
        self.assertEqual(bool, type(response))

    def test_invalid_user(self):
        request = testing.DummyRequest()
        request.validated = {}
        response = user.invalid_user(request)
        self.assertFalse(response)
        self.assertEqual(bool, type(response))

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        response = user.invalid_user(request)
        self.assertTrue(response)
        self.assertEqual(bool, type(response))
