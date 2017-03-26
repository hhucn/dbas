"""
Helper functions for tests.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import json

import requests
from nose.tools import assert_equals, assert_true

from api.lib import json_to_dict

API = "http://localhost:4284/api/"


def has_json_header(response):
    assert_equals("application/json", response.headers['content-type'])


def get_response(route):
    """
    Place get request to API.

    :param route: route in API
    :returns: response from API
    :rtype: Response
    """
    response = requests.get(API + route)
    has_json_header(response)
    return response


def post_request(route, payload):
    """
    Send post request to API with given payload. Adds json headers.

    :param route: route in API
    :param payload: data to be send
    :type payload: dict
    :returns: response from API
    :rtype: Response
    """
    response = requests.post(API + route, json=json.dumps(payload))
    has_json_header(response)
    return response


def parse_status(content):
    """
    Extract :status field from JSON String.

    :param content: json string
    :returns: status
    :rtype: str
    """
    return json_to_dict(content).get("status")


def json_response_ok(url):
    """
    Make GET request to url and assert, that the response is JSON.

    :param url:
    :return:
    """
    response = get_response(url)
    assert_true(response.ok)
