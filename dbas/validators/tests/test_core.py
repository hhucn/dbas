from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request
from dbas.validators import core
from dbas.validators.core import validate


class TestHasKeywords(TestCaseWithConfig):
    def test_empty_dummy_request(self):
        request = construct_dummy_request(json_body={})
        fn = core.has_keywords_in_json_path(('foo', int))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_string_expected_int_should_fail(self):
        request = construct_dummy_request(json_body={'foo': 'bar'})
        fn = core.has_keywords_in_json_path(('foo', int))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_int_expected_int_should_succeed(self):
        request = construct_dummy_request(json_body={'foo': 2})
        fn = core.has_keywords_in_json_path(('foo', int))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertTrue(response)


class TestHasKeywordsInPath(TestCaseWithConfig):
    def test_empty_dummy_request(self):
        request = construct_dummy_request(json_body={})
        fn = core.has_keywords_in_path(('foo', int))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_string_expected_int_should_fail(self):
        request = construct_dummy_request(matchdict={'foo': 'bar'})
        fn = core.has_keywords_in_path(('foo', int))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_provided_string_expected_string_should_succeed(self):
        request = construct_dummy_request(matchdict={'foo': 2})
        fn = core.has_keywords_in_path(('foo', int))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertTrue(response)


class TestHasMaybeKeywords(TestCaseWithConfig):
    def test_provided_int_expected_int_should_succeed(self):
        request = construct_dummy_request(json_body={'foo': 9000})
        fn = core.has_maybe_keywords(('foo', int, 2))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertEqual(len(request.validated), 1)
        self.assertEqual(request.validated.get('foo'), 9000)
        self.assertTrue(response)

    def test_empty_dummy_request(self):
        request = construct_dummy_request(json_body={})
        fn = core.has_maybe_keywords(('foo', int, 2))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertEqual(len(request.validated), 1)
        self.assertEqual(request.validated.get('foo'), 2)
        self.assertTrue(response)

    def test_provided_string_expected_int_should_fail(self):
        request = construct_dummy_request(json_body={'foo': 'bar'})
        fn = core.has_maybe_keywords(('foo', int, 2))
        response = fn(request)
        self.assertIsInstance(response, bool)
        self.assertEqual(len(request.validated), 0)
        self.assertFalse(response)


class TestValidate(TestCaseWithConfig):

    def test_validate(self):
        def __dummy_func(request):
            return request

        request = construct_dummy_request()
        self.assertEqual(request.validated, {})
        self.assertFalse(hasattr(request, 'errors'))
        self.assertFalse(hasattr(request, 'info'))
        inner = validate()
        func = inner(__dummy_func)
        func(request)
        self.assertTrue(len(request.validated) > 0)
        self.assertTrue(hasattr(request, 'errors'))
        self.assertTrue(hasattr(request, 'info'))
