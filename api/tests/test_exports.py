from webtest.response import TestResponse

from dbas.tests.utils import TestCaseWithConfig, test_app


class SaneAIF(TestCaseWithConfig):
    def test_cat_or_dog_aif(self):
        response: TestResponse = test_app().get("/api/cat-or-dog/aif")

        self.assertEqual(response.status_code, 200)
        self.assertIn("nodes", response.json_body)
        self.assertIn("edges", response.json_body)
        self.assertIn({
            "nodeID": "statement_24",
            "text": "the fact, that cats are capricious, is based on the cats race",
            "type": "I",
            "timestamp": "2017-08-09T11:25:09.222604+00:00"
        }, response.json_body["nodes"])

        self.assertIn({
            "edgeID": "argument_edge_out_4",
            "toID": "statement_3",
            "fromID": "argument_4"
        }, response.json_body["edges"])


class SaneDot(TestCaseWithConfig):
    def test_cat_or_dog_aif(self):
        response: TestResponse = test_app().get("/api/cat-or-dog/dot")

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.body, bytes)
