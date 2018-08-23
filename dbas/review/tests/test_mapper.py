from dbas.review.mapper import get_title_by_key, get_review_model_by_key, get_last_reviewer_by_key, get_queue_by_key
from dbas.review.queue import review_queues


class TestMapper(TestCaseWithConfig):
    def test_get_title_by_key(self):
        try:
            get_title_by_key('asd')
        except KeyError:
            pass

        for key in review_queues:
            get_title_by_key(key)

    def test_get_review_model_by_key(self):
        self.assertIsNone(get_review_model_by_key(''))

        for key in review_queues:
            self.assertIsNotNone(get_review_model_by_key(key))

    def test_get_queue_by_key(self):
        self.assertIsNone(get_queue_by_key('FOO'))

        for key in review_queues:
            self.assertIsNotNone(get_queue_by_key(key))

    def test_get_last_reviewer_by_key(self):
        self.assertIsNone(get_last_reviewer_by_key(''))

        for key in review_queues:
            self.assertIsNotNone(get_last_reviewer_by_key(key))
