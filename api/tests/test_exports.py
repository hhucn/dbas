import arrow
from webtest.response import TestResponse

from api.exports import import_aif
from api.tests.test_views import create_request_with_token_header
from dbas.database.discussion_model import Issue
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
            "edgeID": "argument_4_edge_out",
            "toID": "statement_3",
            "fromID": "argument_4"
        }, response.json_body["edges"])

    def test_import_not_allowed_for_normie(self):
        import_response = import_aif(create_request_with_token_header(nickname="Walter",
                                                                      match_dict={"slug": "cat-or-dog-2"},
                                                                      params={"title": "Cat or Dog 2", "lang": "en"},
                                                                      json_body={}))

        self.assertEqual(import_response.status_code, 401)

    def test_import(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        import_response = import_aif(create_request_with_token_header(nickname="Tobias",
                                                                      match_dict={"slug": "my-new-issue"},
                                                                      params={"title": "My new Issue", "lang": "en"},
                                                                      json_body={
                                                                          "nodes": [
                                                                              {
                                                                                  "nodeID": "argument_1",
                                                                                  "type": "CA",
                                                                                  "timestamp": "2017-08-19T11:25:09.347038+00:00"
                                                                              },
                                                                              {
                                                                                  "nodeID": "statement_1",
                                                                                  "text": "This is a Position",
                                                                                  "type": "I",
                                                                                  "timestamp": "2017-08-16T11:25:09.222796+00:00"
                                                                              },
                                                                              {
                                                                                  "nodeID": "statement_2",
                                                                                  "text": "This is a Premise",
                                                                                  "type": "I",
                                                                                  "timestamp": "2017-08-16T11:25:09.222796+00:00"
                                                                              }],
                                                                          "edges": [
                                                                              {
                                                                                  "edgeID": "argument_1_edge_out",
                                                                                  "fromID": "argument_1",
                                                                                  "toID": "statement_1"
                                                                              },
                                                                              {
                                                                                  "edgeID": "argument_1_edge_in_from_18",
                                                                                  "fromID": "statement_2",
                                                                                  "toID": "argument_1"
                                                                              }
                                                                          ]
                                                                      }))
        self.assertEqual(import_response.status_code, 201)

        new_issue = Issue.by_slug("my-new-issue")
        self.assertEqual(new_issue.lang, "en")
        self.assertCountEqual([position.get_text() for position in new_issue.positions], ["This is a Position"])
        self.assertCountEqual([statement.get_text() for statement in new_issue.statements],
                              ["This is a Position", "This is a Premise"])

        self.assertEqual(new_issue.positions[0].get_timestamp(), arrow.get("2017-08-16T11:25:09.222796+00:00"))
        self.assertEqual(new_issue.positions[0].arguments[0].timestamp,
                         arrow.get("2017-08-19T11:25:09.347038+00:00"))
        self.assertFalse(new_issue.positions[0].arguments[0].is_supportive,
                         "Argument with type CA should parse to supportive: False")

        class SaneDot(TestCaseWithConfig):
            def test_cat_or_dog_dot(self):
                response: TestResponse = test_app().get("/api/cat-or-dog/dot")

                self.assertEqual(200, response.status_code)
                self.assertIsInstance(response.body, bytes)
