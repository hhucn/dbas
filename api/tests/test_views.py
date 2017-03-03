"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from nose.tools import assert_true, assert_false, assert_equals
from pprint import pprint as pp
import json
import requests

API = "http://localhost:4284/api/"


def get_response(route):
    return requests.get(API + route)


def parse_status(response):
    data = json.loads(response.content).get("status")
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return data


def test_server_available():
    response = get_response("hello")
    status = parse_status(response)
    assert_true(response.ok)
    assert_equals("ok", status)


def test_login_error():
    credentials = json.dumps({"nickname": "foo",
                              "password": "bar"})
    response = requests.post(API + "login", data=credentials)
    status = parse_status(response)
    assert_false(response.ok)
    assert_equals("error", status)
