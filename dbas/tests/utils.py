"""
Namespace to re-use commonly used components for testing.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import unittest

import transaction
from cornice import Errors
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid_mailer.mailer import DummyMailer
from typing import Dict, Any

from dbas import get_key_pair
from dbas.database import DBDiscussionSession, get_dbas_db_configuration
from dbas.database.discussion_model import Issue, Statement, Argument, User, StatementReference
from dbas.helper.test import add_settings_to_appconfig


class TestCaseWithDatabase(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings=settings_dict_for_tests())
        self.config.include('pyramid_chameleon')
        settings = add_settings_to_appconfig()
        DBDiscussionSession.remove()
        DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))

    def tearDown(self):
        transaction.abort()
        DBDiscussionSession.remove()
        testing.tearDown()


class TestCaseWithConfig(TestCaseWithDatabase):
    def setUp(self):
        super().setUp()
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
        self.user_antonia: User = DBDiscussionSession.query(User).get(28)
        self.statement_reference: StatementReference = DBDiscussionSession.query(StatementReference).get(2)

        DBDiscussionSession.query(Argument).get(1).set_disabled(True)

    def tearDown(self):
        DBDiscussionSession.query(Argument).get(1).set_disabled(False)
        super().tearDown()


def settings_dict_for_tests() -> Dict[str, Any]:
    """
    Builds a dictionary with settings that are needed for the tests to function directly.
    Do not build the settings elsewhere. Use this method instead.
    :return: A dictionary of settings, that can be used in test requests.
    """
    settings_dict = {'beaker.session.timeout': 3600}
    settings_dict.update(get_key_pair())
    return settings_dict


def construct_dummy_request(json_body: dict = None, match_dict: dict = None, validated: dict = None,
                            params: dict = None) -> DummyRequest:
    """
    Creates a Dummy-Request. Optionally takes a json_body etc, which can directly be injected into the request.

    :param json_body: dict
    :param match_dict: dict
    :param validated: dict
    :param params: dict
    :return: DummyRequest
    :rtype: DummyRequest
    """
    json_body = json_body if json_body else {}
    match_dict = match_dict if match_dict else {}
    validated = validated if validated else {}
    params = params if params else {}

    d_request = DummyRequest(json_body=json_body, matchdict=match_dict, validated=validated, params=params,
                             errors=Errors(),
                             mailer=DummyMailer, cookies={'_LOCALE_': 'en'}, decorated={'extras': {}})

    if d_request.registry.settings:
        d_request.registry.settings.update(settings_dict_for_tests())
    else:
        d_request.registry.settings = settings_dict_for_tests()

    return d_request
