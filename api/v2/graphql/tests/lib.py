from nose.tools import assert_true, assert_is_not_none

from api.lib import json_to_dict
from api.tests.lib import get_response

API = "http://localhost:4284/api/v2/"


def graphql_query(query) -> dict:
    response = get_response("query", API, {"q": query})
    assert_true(response.ok)
    ret = json_to_dict(response.content)
    assert_is_not_none(ret)
    return ret
