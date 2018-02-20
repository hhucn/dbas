import json
import unittest

import requests

from search import ROUTE_API
from search.routes import get_suggestions_path, get_edits_path, get_duplicates_or_reasons_path, \
    get_statements_with_value_path


class TestRoutes(unittest.TestCase):

    def test_get_suggestions_status_200(self):
        response = requests.get(ROUTE_API + "/suggestions")
        self.assertEqual(response.status_code, 200)

    def test_get_edits_status_200(self):
        response = requests.get(ROUTE_API + "/edits")
        self.assertEqual(response.status_code, 200)

    def test_get_duplicates_reasons_status_200(self):
        response = requests.get(ROUTE_API + "/duplicates_reasons")
        self.assertEqual(response.status_code, 200)

    def test_get_statements_status_200(self):
        response = requests.get(ROUTE_API + "/statements")
        self.assertEqual(response.status_code, 200)

    def test_invalid_request_has_404(self):
        response = requests.get(ROUTE_API + "/coconut")
        self.assertEqual(response.status_code, 404)

    def test_valid_path_empty_result(self):
        response = requests.get(ROUTE_API + "/suggestions?id=1")
        response = json.loads(response.text)
        self.assertEqual(len(response), 0)

    def test_valid_path_no_empty_result(self):
        response = requests.get(ROUTE_API + "/suggestions?id=5")
        response = json.loads(response.text)
        self.assertGreaterEqual(len(response), 1)

    def test_invalid_path_empty_result(self):
        response = requests.get(ROUTE_API + "/suggestions")
        response = json.loads(response.text)
        self.assertEqual(len(response), 0)

    def test_valid_suggestions_path(self):
        path = get_suggestions_path(1, True, "coconut")
        self.assertEqual(path, "http://search:5000/suggestions?id=1&start=True&search=coconut")

    def test_valid_edits_path(self):
        path = get_edits_path(1, 1, "coconut")
        self.assertEqual(path, "http://search:5000/edits?id=1&statement_uid=1&search=coconut")

    def test_duplicates_or_reasons_path(self):
        path = get_duplicates_or_reasons_path(1, 1, "coconut")
        self.assertEqual(path, "http://search:5000/duplicates_reasons?id=1&statement_uid=1&search=coconut")

    def test_statements_with_value_path(self):
        path = get_statements_with_value_path(1, "coconut")
        self.assertEqual(path, "http://search:5000/statements?id=1&search=coconut")

    def test_valid_suggestions_path_empty_search(self):
        path = get_suggestions_path(1, True)
        self.assertEqual(path, "http://search:5000/suggestions?id=1&start=True&search=")

    def test_valid_edits_path_empty_search(self):
        path = get_edits_path(1, 1)
        self.assertEqual(path, "http://search:5000/edits?id=1&statement_uid=1&search=")

    def test_duplicates_or_reasons_path_empty_search(self):
        path = get_duplicates_or_reasons_path(1, 1)
        self.assertEqual(path, "http://search:5000/duplicates_reasons?id=1&statement_uid=1&search=")

    def test_statements_with_value_path_empty_search(self):
        path = get_statements_with_value_path(1)
        self.assertEqual(path, "http://search:5000/statements?id=1&search=")
