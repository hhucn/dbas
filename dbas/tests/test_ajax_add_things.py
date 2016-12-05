import unittest
import json
from pyramid import testing

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))
DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


class AjaxAddThingsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # test every ajax method, which is not used in other classes

    def tearDown(self):
        testing.tearDown()

    def test_set_new_start_statement(self):
        from dbas.views import set_new_start_statement as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_set_new_start_premise(self):
        from dbas.views import set_new_start_premise as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_set_new_premises_for_argument(self):
        from dbas.views import set_new_premises_for_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_set_correction_of_statement(self):
        from dbas.views import set_correction_of_statement as ajax
        request = testing.DummyRequest(selfparams={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_set_new_issue(self):
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_set_seen_statements(self):  # todo rename ajax route
        from dbas.views import set_seen_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
