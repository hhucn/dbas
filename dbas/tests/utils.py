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
from dbas.database.discussion_model import Issue, Statement, Argument, User


class TestCaseWithConfig(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

        self.issue_disabled: Issue = DBDiscussionSession.query(Issue).get(6)
        self.issue_read_only: Issue = DBDiscussionSession.query(Issue).get(7)
        self.issue_cat_or_dog: Issue = DBDiscussionSession.query(Issue).get(2)
        self.issue_town: Issue = DBDiscussionSession.query(Issue).get(1)
        self.position_cat_or_dog: Statement = DBDiscussionSession.query(Statement).get(2)
        self.position_town: Statement = DBDiscussionSession.query(Statement).get(36)
        self.statement_cat_or_dog: Statement = DBDiscussionSession.query(Statement).get(5)
        self.statement_town: Statement = DBDiscussionSession.query(Statement).get(40)
        self.statement_argument_town: Statement = DBDiscussionSession.query(Statement).get(39)
        self.argument_town: Argument = DBDiscussionSession.query(Argument).get(34)
        self.argument_cat_or_dog: Argument = DBDiscussionSession.query(Argument).get(2)
        self.user_anonymous: User = DBDiscussionSession.query(User).get(1)
        self.user_tobi: User = DBDiscussionSession.query(User).get(2)
        self.user_christian: User = DBDiscussionSession.query(User).get(3)
        self.user_bjoern: User = DBDiscussionSession.query(User).get(4)

    def tearDown(self):
        testing.tearDown()


def construct_dummy_request(json_body: dict = None, match_dict: dict = None) -> DummyRequest:
    """
    Creates a Dummy-Request. Optionally takes a json_body, which can directly be injected into the request.

    :param json_body: dict
    :param match_dict: dict
    :return: DummyRequest
    :rtype: DummyRequest
    """
    if json_body is None:
        json_body = dict()
    if match_dict is None:
        match_dict = dict()
    return DummyRequest(json_body=json_body, matchdict=match_dict, validated={}, errors=Errors(), mailer=DummyMailer,
                        cookies={'_LOCALE_': 'en'})
