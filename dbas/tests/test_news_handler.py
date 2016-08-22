import unittest

from dbas.database import DBNewsSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.handler import news
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


class NewsHandlerTests(unittest.TestCase):
    def test_get_news(self):
        # correct id
        response_correct_id = news.get_news(1)
        # access elements in OrderedDict
        items = list(response_correct_id.items())
        self.assertTrue(verify_structure_news_dictionary(self, items[0][1]))

        response_correct_id2 = news.get_news(70)
        # access elements in OrderedDict
        items2 = list(response_correct_id2.items())
        self.assertTrue(verify_structure_news_dictionary(self, items2[0][1]))

        response = news.get_news(None)
        # access elements in OrderedDict
        items3 = list(response.items())
        self.assertTrue(verify_structure_news_dictionary(self, items3[0][1]))


def verify_structure_news_dictionary(self, response):
    self.assertTrue('title' in response)
    self.assertTrue('author' in response)
    self.assertTrue('date' in response)
    self.assertTrue('news' in response)
    self.assertTrue('uid' in response)
    return True
