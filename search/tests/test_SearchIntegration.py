import unittest
import requests
import json
from search import SEARCH_REQUEST_STRING


class TestIntegrationSearch(unittest.TestCase):

    def test_get_response_status_200(self):
        response = requests.get(SEARCH_REQUEST_STRING + "/suggestions")
        self.assertEqual(response.status_code, 200)

    def test_invalid_request_has_404(self):
        response = requests.get(SEARCH_REQUEST_STRING + "/coconut")
        self.assertEqual(response.status_code, 404)

    def test_valid_path_empty_result(self):
        response = requests.get(SEARCH_REQUEST_STRING + "/suggestions?id=1")
        response = json.loads(response.text)
        self.assertEqual(len(response), 0)

    def test_valid_path_no_empty_result(self):
        response = requests.get(SEARCH_REQUEST_STRING + "/suggestions?id=5")
        response = json.loads(response.text)
        self.assertGreaterEqual(len(response), 1)

    def test_invalid_path_empty_result(self):
        response = requests.get(SEARCH_REQUEST_STRING + "/suggestions")
        response = json.loads(response.text)
        self.assertEqual(len(response), 0)


