"""
Unit tests for our validators

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

from dbas.database.discussion_model import ReviewDelete
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request
from dbas.validators.core import has_keywords_in_json_path, spec_keyword_in_json_body
from dbas.validators.reviews import valid_not_executed_review


class TestHasKeywords(TestCaseWithConfig):
    def test_has_one_keyword(self):
        request = construct_dummy_request(json_body={'string': 'foo'})
        response = has_keywords_in_json_path(('string', str))(request)
        self.assertTrue(response)
        self.assertIn('string', request.validated)

    def test_has_multiple_keywords(self):
        request = construct_dummy_request(json_body={
            'string': 'foo',
            'bool': True
        })
        response = has_keywords_in_json_path(('string', str), ('bool', bool))(request)
        self.assertTrue(response)
        self.assertIn('string', request.validated)
        self.assertIn('bool', request.validated)

    def test_has_number_keywords(self):
        request = construct_dummy_request(json_body={
            'int': 4,
            'float': 4.0
        })
        response = has_keywords_in_json_path(('int', int), ('float', float))(request)
        self.assertTrue(response)
        self.assertIn('int', request.validated)
        self.assertIn('float', request.validated)

    def test_has_list_keywords(self):
        request = construct_dummy_request(json_body={'list': ['<:)']})
        response = has_keywords_in_json_path(('list', list))(request)
        self.assertTrue(response)
        self.assertIn('list', request.validated)

    def test_has_keywords_with_wrong_type(self):
        request = construct_dummy_request(json_body={'int': 4})
        response = has_keywords_in_json_path(('int', float))(request)
        self.assertFalse(response)
        self.assertNotIn('int', request.validated)

    def test_has_keywords_without_keyword(self):
        request = construct_dummy_request(json_body={'foo': 42})
        response = has_keywords_in_json_path(('bar', int))(request)
        self.assertFalse(response)
        self.assertNotIn('bar', request.validated)


class TestExecutedReviews(TestCaseWithConfig):
    def test_valid_not_executed_review(self):
        request = construct_dummy_request(json_body={'ruid': 4})
        response = valid_not_executed_review('ruid', ReviewDelete)(request)
        self.assertTrue(response)

    def test_valid_not_executed_review_error(self):
        request = construct_dummy_request(json_body={'ruid': 1})
        response = valid_not_executed_review('ruid', ReviewDelete)(request)
        self.assertFalse(response)


class TestSpecKeywords(TestCaseWithConfig):
    def test_empty_dummy_request_should_fail(self):
        request = construct_dummy_request()
        fn = spec_keyword_in_json_body((int, 'foo', lambda foo, varType: isinstance(foo, varType)))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_string_expected_int_should_fail(self):
        request = construct_dummy_request(json_body={'foo': 'bar'})
        fn = spec_keyword_in_json_body((int, 'foo', lambda foo, varType: isinstance(foo, varType)))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_int_expected_int_should_succed(self):
        request = construct_dummy_request(json_body={'foo': 2})
        fn = spec_keyword_in_json_body((int, 'foo', lambda foo, varType: isinstance(foo, varType)))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertTrue(response)

    def test_provided_empty_string_should_fail(self):
        request = construct_dummy_request(json_body={'foo': ''})
        fn = spec_keyword_in_json_body((str, 'foo', lambda foo, varType: isinstance(foo, varType) and foo != ''))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_string_should_succed(self):
        request = construct_dummy_request(json_body={'foo': 'bar'})
        fn = spec_keyword_in_json_body((str, 'foo', lambda foo, varType: isinstance(foo, varType) and foo != ''))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertTrue(response)
