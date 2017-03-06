"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from nose.tools import assert_true, assert_false, assert_equals
from api.lib import json_bytes_to_dict
import json
import requests

API = "http://localhost:4284/api/"

# ------------------------------------------------------------------------------
# Helper functions


def get_response(route):
    """
    Place get request to API.

    :param route: route in API
    :returns: response from API
    :rtype: Response
    """
    return requests.get(API + route)


def post_request(route, payload):
    """
    Send post request to API with given payload. Adds json headers.

    :param route: route in API
    :param payload: data to be send
    :type payload: dict
    :returns: response from API
    :rtype: Response
    """
    return requests.post(API + route, json=json.dumps(payload))


def parse_status(content):
    """
    Extract :status field from JSON String.

    :param content: json string
    :returns: status
    :rtype: str
    """
    return json_bytes_to_dict(content).get("status")


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
    content = json_bytes_to_dict(response.content)
    assert_false(response.ok)
    assert_equals("error", content.get("status"))
    assert_false(content.get("token"))
    assert_false(content.get("csrf"))


def test_login_valid():
    credentials = {"nickname": "Walter",
                   "password": "iamatestuser2016"}
    response = post_request("login", credentials)
    content = json_bytes_to_dict(response.content)
    assert_true(response.ok)
    assert_true(content.get("token"))
    assert_true(content.get("csrf"))
