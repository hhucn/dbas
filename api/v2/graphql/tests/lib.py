from nose.tools import assert_true

from api.lib import json_to_dict
from api.tests.lib import get_response

API = "http://localhost:4284/api/v2/"


def graphql_query(query) -> dict:
    response = get_response("query", API, {"q": query})
    assert_true(response.ok)
    return json_to_dict(response.content)
