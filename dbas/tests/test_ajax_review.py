import unittest
import json
from pyramid import testing

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))
DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


class AjaxReviewTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # test every ajax method, which is not used in other classes

    def tearDown(self):
        testing.tearDown()

    def test_flag_argument_or_statement(self):
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_review_delete_argument(self):
        from dbas.views import review_delete_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_review_optimization_argument(self):
        from dbas.views import review_optimization_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_review_edit_argument(self):
        from dbas.views import review_edit_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_undo_review(self):
        from dbas.views import undo_review as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_cancel_review(self):
        from dbas.views import cancel_review as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_review_lock(self):
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_revoke_content(self):
        from dbas.views import revoke_some_content as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
