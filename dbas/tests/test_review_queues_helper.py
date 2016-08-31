import unittest

import dbas.review.helper.queues as ReviewQueuesHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewQueuesHelperTest(unittest.TestCase):

    def test_get_review_array(self):
        _tn = Translator('en')
        self.assertIsNone(ReviewQueuesHelper.get_review_queues_array('page', _tn, 'Pikachu'))

        array = ReviewQueuesHelper.get_review_queues_array('page', _tn, 'Tobias')
        for d in array:
            self.assertTrue('task_name' in d)
            self.assertTrue('url' in d)
            self.assertTrue('icon' in d)
            self.assertTrue('task_count' in d)
            self.assertTrue('is_allowed' in d)
            self.assertTrue('is_allowed_text' in d)
            self.assertTrue('is_not_allowed_text' in d)
            self.assertTrue('last_reviews' in d)