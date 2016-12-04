import unittest
import json
from pyramid import testing

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.news_model import News
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))
DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


class AjaxNewsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

        # test every ajax method, which is not used in other classes

    def tearDown(self):
        testing.tearDown()

    def test_get_news(self):
        from dbas.views import get_news as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_send_news(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_news as ajax
        request = testing.DummyRequest(params={
            'title': 'some new title',
            'text': 'some new text'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)

        DBNewsSession.query(News).filter_by(title='some new title').delete()

    def test_send_news_failure(self):
        from dbas.views import send_news as ajax
        request = testing.DummyRequest(params={
            'title': 'some new title',
            'text': 'some new text'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

        DBNewsSession.query(News).filter_by(title='some new title').delete()
