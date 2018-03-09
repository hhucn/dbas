"""
Namespace to re-use commonly used components for testing.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import unittest

from cornice import Errors
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid_mailer.mailer import DummyMailer

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue


class TestCaseWithConfig(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.issue_disabled: Issue = DBDiscussionSession.query(Issue).get(6)
        self.issue_cat_or_dog: Issue = DBDiscussionSession.query(Issue).get(2)

    def tearDown(self):
        testing.tearDown()


def construct_dummy_request(json_body=None) -> DummyRequest:
    """
    Creates a Dummy-Request. Optionally takes a json_body, which can directly be injected into the request.

    :param json_body: dict
    :return: DummyRequest
    :rtype: DummyRequest
    """
    if json_body is None:
        json_body = dict()
    return DummyRequest(json_body=json_body, validated={}, errors=Errors(), mailer=DummyMailer,
                        cookies={'_LOCALE_': 'en'})
