import time

from dbas.tests.utils import TestCaseWithConfig
from search import ROUTE_API
from search.requester import get_suggestions, get_duplicates_or_reasons, get_statements_with_value, get_edits, \
    response_as_dict


class TestRequester(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        time.sleep(8)

    def test_request_as_dict_returns_dict(self):
        result = response_as_dict(ROUTE_API + '/suggestions?id=2')
        self.assertEqual(type(result), dict)

    def test_request_as_dict_is_not_empty(self):
        result = response_as_dict(ROUTE_API + '/suggestions?id=2')
        self.assertNotEqual(0, len(result.get('results')))

    def test_suggestions_not_empty_1(self):
        results = get_suggestions(2, True)
        self.assertNotEqual(0, len(results))

    def test_suggestions_not_empty_2(self):
        results = get_suggestions(2, False)
        self.assertNotEqual(0, len(results))

    def test_duplicates_or_reasons_1(self):
        results = get_duplicates_or_reasons(2, 4)
        self.assertNotEqual(0, len(results))

    def test_statements_with_value_has_url_1(self):
        url = get_statements_with_value(2)[0]['url']
        self.assertIsNotNone(url)

    def test_edits_not_empty_1(self):
        results = get_edits(4, 58)
        self.assertNotEqual(0, len(results))
