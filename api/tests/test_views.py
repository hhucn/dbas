"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from nose.tools import assert_equals, assert_false, assert_true

from api.lib import json_to_dict
from api.tests.lib import get_response, parse_status, post_request


# ------------------------------------------------------------------------------
# Tests

def test_server_available():
    response = get_response("hello")
    status = parse_status(response.content)
    assert_true(response.ok)
    assert_equals("ok", status)


def test_login_invalid():
    credentials = {"nickname": "foo",
                   "password": "bar"}
    response = post_request("login", credentials)
    content = json_to_dict(response.content)
    assert_false(response.ok)
    assert_equals("error", content.get("status"))
    assert_false(content.get("token"))
    assert_false(content.get("csrf"))


def test_login_valid():
    credentials = {"nickname": "Walter",
                   "password": "iamatestuser2016"}
    response = post_request("login", credentials)
    content = json_to_dict(response.content)
    assert_true(response.ok)
    assert_true(content.get("token"))
    assert_true(content.get("csrf"))
