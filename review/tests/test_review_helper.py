import unittest

import review.review_helper as ReviewHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewHelperTest(unittest.TestCase):

    def test_get_review_array(self):
        _tn = Translator('en')
        self.assertIsNone(ReviewHelper.get_review_array('page', 'cat-or-dog', _tn, 'Pikachu'))
        self.assertIsNone(ReviewHelper.get_review_array('page', 'cat-or-cat', _tn, 'Pikachu'))

        array = ReviewHelper.get_review_array('page', 'cat-or-dog', _tn, 'Tobias')
        for d in array:
            self.assertTrue('task_name' in d)
            self.assertTrue('url' in d)
            self.assertTrue('icon' in d)
            self.assertTrue('task_count' in d)
            self.assertTrue('is_allowed' in d)
            self.assertTrue('is_allowed_text' in d)
            self.assertTrue('is_not_allowed_text' in d)
            self.assertTrue('last_reviews' in d)

    def test_get_subpage_for(self):
        self.assertIsNone(ReviewHelper.get_subpage_for('test', 'some nick'))
        self.assertIsNone(ReviewHelper.get_subpage_for('test', 'Tobias'))
        self.assertIsNone(ReviewHelper.get_subpage_for('edits', 'some nick'))
        self.assertIsNotNone(ReviewHelper.get_subpage_for('edits', 'Tobias'))

    def test_get_reputation_history(self):
        self.assertEqual(len(ReviewHelper.get_reputation_history('Bla')), 0)
        history = ReviewHelper.get_reputation_history('Tobias')
        self.assertTrue(len(history) > 0)
        self.assertTrue('count' in history)
        self.assertTrue('history' in history)
        for h in history['history']:
            self.assertTrue('date' in h)
            self.assertTrue('action' in h)
            self.assertTrue('points' in h)
