from api.v2.graphql.tests.lib import graphql_query
from dbas.tests.utils import TestCaseWithConfig


class TestQueryStatementReference(TestCaseWithConfig):
    def test_query_statement_reference(self):
        query = """
            query {
                statementReferences {
                    uid
                    users {
                        publicNickname
                    }
                }
            }
        """
        content = graphql_query(query)
        references = content.get("statementReferences")
        ref = references[0]
        self.assertIsNotNone(ref)
        self.assertIn('uid', ref)
        self.assertIn('users', ref)
        self.assertIsNotNone(ref.get("users").get("publicNickname"))


class TestQueryPremises(TestCaseWithConfig):
    def test_query_premises(self):
        query = """
            query {
                premises {
                    uid
                    author {
                        publicNickname
                    }
                }
            }
        """
        content = graphql_query(query)
        premises = content.get("premises")
        premise = premises[0]
        self.assertIsNotNone(premise)
        self.assertIn('uid', premise)
        self.assertIn('author', premise)
        self.assertIsNotNone(premise.get("author").get("publicNickname"))

    def test_query_premisegroups(self):
        query = """
            query {
                premisegroups {
                    uid
                    author {
                        publicNickname
                    }
                }
            }
        """
        content = graphql_query(query)
        premisegroups = content.get("premisegroups")
        group = premisegroups[0]
        self.assertIsNotNone(group)
        self.assertIn('uid', group)
        self.assertIn('author', group)
        self.assertIsNotNone(group.get("author").get("publicNickname"))

    def test_query_premises_by_premisegroup(self):
        query = """
            query {
                premises (premisegroupUid: 9) {
                    uid
                }
            }
        """
        content = graphql_query(query)
        result = content.get("premises")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn('uid', result[0])
        self.assertIn('uid', result[1])


class TestQueryArguments(TestCaseWithConfig):
    def test_query_arguments(self):
        query = """
            query {
                arguments {
                    uid
                    premisegroup {
                        uid
                    }
                    author {
                        publicNickname
                    }
                }
            }
        """
        content = graphql_query(query)
        arguments = content.get("arguments")
        group = arguments[0]
        self.assertIsNotNone(group)
        self.assertIn('uid', group)
        self.assertIn('author', group)
        self.assertIn('publicNickname', group.get('author'))
        self.assertIn('premisegroup', group)
        self.assertIn('uid', group.get("premisegroup"))
