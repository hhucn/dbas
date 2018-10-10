import json
import time

import requests

from dbas.tests.utils import TestCaseWithConfig
from search import ROUTE_API


class TestRoutes(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        time.sleep(8)

    def test_get_suggestions_status_200(self):
        response = requests.get(ROUTE_API + '/suggestions?id=1')
        self.assertEqual(response.status_code, 200)

    def test_get_edits_status_200(self):
        response = requests.get(ROUTE_API + '/edits?id=1&statement_uid=1')
        self.assertEqual(response.status_code, 200)

    def test_get_duplicates_reasons_status_200(self):
        response = requests.get(ROUTE_API + '/duplicates_reasons?id=1&statement_uid=1')
        self.assertEqual(response.status_code, 200)

    def test_get_statements_status_200(self):
        response = requests.get(ROUTE_API + '/statements?id=1')
        self.assertEqual(response.status_code, 200)

    def test_invalid_request_has_404(self):
        response = requests.get(ROUTE_API + '/coconut')
        self.assertEqual(response.status_code, 404)

    def test_valid_path_empty_result(self):
        response = requests.get(ROUTE_API + '/suggestions?id=1')
        response = json.loads(response.text)
        self.assertEqual(len(response), 1)
        self.assertEqual(len(response.get('results')), 0)

    def test_valid_path_no_empty_result(self):
        response = requests.get(ROUTE_API + '/suggestions?id=5')
        print(ROUTE_API + '/suggestions?id=5')
        response = json.loads(response.text)
        self.assertGreaterEqual(len(response), 1)
        self.assertNotEqual(len(response.get('results')), 0)
