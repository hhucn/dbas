import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import News, User
from dbas.tests.utils import construct_dummy_request


class AjaxNewsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

        # test every ajax method, which is not used in other classes

    def test_get_news_view(self):
        from dbas.views import get_news as ajax
        request = construct_dummy_request(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_get_news(self):
        from dbas.handler.news import get_news
        return_dict = get_news('en')
        for news in return_dict:
            for key in ['title', 'author', 'date', 'news', 'title_id', 'date_id', 'author_id', 'uid']:
                self.assertIn(key, news)

    def get_latest_news(self):
        from dbas.handler.news import get_latest_news
        return_dict = get_latest_news('en')
        for news in return_dict:
            for key in ['indicatorclass', 'blockclass', 'title', 'author', 'date', 'news', 'id']:
                self.assertIn(key, news)

    def test_send_news(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_news as ajax
        request = construct_dummy_request(json_body={
            'title': 'some new title',
            'text': 'some new text'
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual('success', response['status'])
        DBDiscussionSession.query(News).filter_by(title='some new title').delete()

    def test_send_news_failure(self):
        from dbas.views import send_news as ajax
        request = construct_dummy_request(json_body={
            'title': 'some new title',
            'text': 'some new text'
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        DBDiscussionSession.query(News).filter_by(title='some new title').delete()

    def test_set_news(self):
        from dbas.handler.news import set_news
        db_user = DBDiscussionSession.query(User).get(2)
        return_dict = set_news('some new title', 'some new text', db_user, 'en', 'url')
        self.assertEqual('success', return_dict['status'])
        DBDiscussionSession.query(News).filter_by(title='some new title').delete()
