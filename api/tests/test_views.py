"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from nose.tools import assert_true
from pprint import pprint as pp
import requests

API = "http://localhost:4284/api/"


def test_server_available():
    response = requests.get(API + "hello")
    assert_true(response.ok)