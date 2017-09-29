import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import News


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
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_send_news(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_news as ajax
        request = testing.DummyRequest(params={
            'title': 'some new title',
            'text': 'some new text'
        }, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)

        DBDiscussionSession.query(News).filter_by(title='some new title').delete()

    def test_send_news_failure(self):
        from dbas.views import send_news as ajax
        request = testing.DummyRequest(params={
            'title': 'some new title',
            'text': 'some new text'
        }, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

        DBDiscussionSession.query(News).filter_by(title='some new title').delete()
