import unittest

from dbas.handler import news


class NewsHandlerTests(unittest.TestCase):
    def test_get_news(self):
        # correct id
        response_correct_id = news.get_news(1)
        # access elements in OrderedDict
        self.verify_structure_news_list(response_correct_id)

        response_correct_id2 = news.get_news(70)
        # access elements in OrderedDict
        self.verify_structure_news_list(response_correct_id2)

        response = news.get_news(None)
        # access elements in OrderedDict
        self.verify_structure_news_list(response)

    def verify_structure_news_list(self, response):
        for element in response:
            self.assertTrue('title' in element)
            self.assertTrue('author' in element)
            self.assertTrue('date' in element)
            self.assertTrue('news' in element)
            self.assertTrue('uid' in element)
        return True
