from dbas.handler import news
from dbas.tests.utils import TestCaseWithConfig


class NewsHandlerTests(TestCaseWithConfig):
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
            self.assertIn('title', element)
            self.assertIn('author', element)
            self.assertIn('date', element)
            self.assertIn('news', element)
            self.assertIn('uid', element)
        return True
