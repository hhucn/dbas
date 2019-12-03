from nose.tools import assert_true, assert_is_not_none, assert_is_none

from api.v2.query.tests.lib import graphql_query


def test_statements_with_textversions():
    query = """
        query {
            statements {
                uid
                textversions {
                    content
                }
            }
        }
    """
    content = graphql_query(query)
    assert_true(len(content.get("statements")) > 1)


def test_query_single_statement():
    query = """
        query {
            statement (uid: 2) {
                uid
                textversions {
                    content
                }
            }
        }
    """
    content = graphql_query(query)
    statement = content.get("statement")
    assert_is_not_none(statement)
    assert_is_not_none(statement.get("uid"))
    assert_is_not_none(statement.get("textversions"))
    assert_is_not_none(statement.get("textversions").get("content"))


def test_query_statement_origin():
    query = """
        query {
            statementOrigin (uid: 2) {
                uid
            }
        }
    """
    content = graphql_query(query)
    errors = content.get("errors")
    assert_is_none(errors)
