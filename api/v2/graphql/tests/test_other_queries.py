from nose.tools import assert_is_not_none

from api.v2.graphql.tests.lib import graphql_query


def test_query_statement_reference():
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
    assert_is_not_none(ref)
    assert_is_not_none(ref.get("uid"))
    assert_is_not_none(ref.get("users"))
    assert_is_not_none(ref.get("users").get("publicNickname"))


def test_query_premises():
    query = """
        query {
            premises {
                uid
                users {
                    publicNickname
                }
            }
        }
    """
    content = graphql_query(query)
    premises = content.get("premises")
    premise = premises[0]
    assert_is_not_none(premise)
    assert_is_not_none(premise.get("uid"))
    assert_is_not_none(premise.get("users"))
    assert_is_not_none(premise.get("users").get("publicNickname"))


def test_query_premisegroups():
    query = """
        query {
            premisegroups {
                uid
                users {
                    publicNickname
                }
            }
        }
    """
    content = graphql_query(query)
    premisegroups = content.get("premisegroups")
    group = premisegroups[0]
    assert_is_not_none(group)
    assert_is_not_none(group.get("uid"))
    assert_is_not_none(group.get("users"))
    assert_is_not_none(group.get("users").get("publicNickname"))


def test_query_arguments():
    query = """
        query {
            arguments {
                uid
                premisegroups {
                    uid
                }
                users {
                    publicNickname
                }
            }
        }
    """
    content = graphql_query(query)
    arguments = content.get("arguments")
    group = arguments[0]
    assert_is_not_none(group)
    assert_is_not_none(group.get("uid"))
    assert_is_not_none(group.get("users"))
    assert_is_not_none(group.get("users").get("publicNickname"))
    assert_is_not_none(group.get("premisegroups"))
    assert_is_not_none(group.get("premisegroups").get("uid"))
