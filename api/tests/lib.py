"""
Helper functions for tests.
"""
import requests
from nose.tools import assert_equals, assert_true
from requests import Response

from api.lib import json_to_dict

API = "http://localhost:4284/api/"


def has_json_header(response):
    assert_equals("application/json", response.headers['content-type'])


def get_response(route: str, api: str = API, params: dict = None) -> Response:
    """
    Place get request to API.

    :param route: route in API
    :param api: route to API
    :param params: parameters, which can be sent via the GET request
    :type params: dict
    :returns: response from API
    :rtype: Response
    """
    if params is None:
        params = dict()
    response = requests.get(api + route, params)
    has_json_header(response)
    return response


def post_request(route, payload, headers=None):
    """
    Send post request to API with given payload. Adds json headers.

    :param headers: Additional dictionary of headers
    :param route: route in API
    :param payload: data to be send
    :type payload: dict
    :returns: response from API
    :rtype: Response
    """
    if headers is None:
        headers = dict()
    response = requests.post(API + route, json=payload, headers=headers)
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
