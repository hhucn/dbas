"""
Testing the routes of the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import json
import random
import string

from nose.tools import assert_equals, assert_false, assert_true

from admin.lib import generate_application_token
from api.lib import json_to_dict
from api.tests.lib import get_response, parse_status, post_request


def __generate_random_string(length=50) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(length))


def __payload_add_statement() -> dict:
    return {"path": "/",
            "statement": __generate_random_string(),
            "slug": "town-has-to-cut-spending",
            "issue_id": 1,
            "conclusion_id": "None",
            "attack_type": None,
            "arg_uid": None,
            "reference": None,
            "host": "i.amgro.ot",
            "supportive": None}


# ------------------------------------------------------------------------------
# Tests

def test_server_available():
    response = get_response("hello")
    status = parse_status(response.content)
    assert_true(response.ok)
    assert_equals("ok", status)


def test_add_position_should_succeed():
    credentials = {"nickname": "Walter",
                   "password": "iamatestuser2016"}
    response = post_request("login", credentials)
    content = json_to_dict(response.content)
    payload = __payload_add_statement()
    response = post_request("add/start_statement", payload,
                            headers={"X-Authentication": json.dumps({"type": "user", "token": content.get("token")})})
    assert_true(response.ok)


def test_add_position_unsplittable_token():
    payload = __payload_add_statement()
    response = post_request("add/start_statement", payload,
                            headers={"X-Authentication": json.dumps({"type": "user", "token": "I am groot"})})
    assert_false(response.ok)


def test_add_position_splittable_invalid_token():
    payload = __payload_add_statement()
    response = post_request("add/start_statement", payload,
                            headers={"X-Authentication": json.dumps({"type": "user", "token": "Groot-iamgroot"})})
    assert_false(response.ok)


def test_correct_api_token():
    api_token = generate_application_token("Walter")
    payload = __payload_add_statement()
    response = post_request("add/start_statement", payload,
                            headers={"X-Authentication": json.dumps({"type": "user", "token": "Walter-" + api_token})})
    assert_true(response.ok)


def test_incorrect_api_token():
    api_token = "blablablab-df---df--df"
    payload = __payload_add_statement()
    response = post_request("add/start_statement", payload,
                            headers={"X-Authentication": json.dumps({"type": "user", "token": "Walter-" + api_token})})
    assert_false(response.ok)
