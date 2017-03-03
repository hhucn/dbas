"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from nose.tools import assert_true, assert_false, assert_equals
import json
import requests

API = "http://localhost:4284/api/"


def json_to_dict(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return json.loads(data)


def get_response(route):
    return requests.get(API + route)


def parse_status(content):
    return json_to_dict(content).get("status")


def test_server_available():
    response = get_response("hello")
    status = parse_status(response.content)
    assert_true(response.ok)
    assert_equals("ok", status)


def test_login_error():
    credentials = json.dumps({"nickname": "foo",
                              "password": "bar"})
    response = requests.post(API + "login", data=credentials)
    status = parse_status(response.content)
    assert_false(response.ok)
    assert_equals("error", status)
