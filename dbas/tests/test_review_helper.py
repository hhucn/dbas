import unittest

import dbas.review.helper.page_manager as ReviewHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config
from pyramid import testing

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewHelperTest(unittest.TestCase):

    def test_get_review_array(self):
        _tn = Translator('en')
        self.assertIsNone(ReviewHelper.get_review_queues_array('page', _tn, 'Pikachu'))

        array = ReviewHelper.get_review_queues_array('page', _tn, 'Tobias')
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
        from dbas.review.helper.page_manager import pages
        request = testing.DummyRequest()

        ret_dict = ReviewHelper.get_subpage_elements_for(request, 'some page', 'some nick', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        ret_dict = ReviewHelper.get_subpage_elements_for(request, 'some page', 'Tobias', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        ret_dict = ReviewHelper.get_subpage_elements_for(request, pages[0], 'Tobias', Translator('en'))
        self.assertIsNotNone(ret_dict['elements'])
        self.assertTrue(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        ret_dict = ReviewHelper.get_subpage_elements_for(request, pages[0], 'some nick', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        for page in pages:
            ret_dict = ReviewHelper.get_subpage_elements_for(request, page, 'Tobias', Translator('en'))
            self.assertIsNotNone(ret_dict['elements'])
            self.assertTrue(ret_dict['has_access'])
            self.assertFalse(ret_dict['no_arguments_to_review'])

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

    def test_get_reputation_list(self):
        some_list = ReviewHelper.get_reputation_list(Translator('en'))
        for element in some_list:
            self.assertTrue('points' in element)
            self.assertTrue('icon' in element)
            self.assertTrue('text' in element)

    def test_get_privilege_list(self):
        some_list = ReviewHelper.get_privilege_list(Translator('en'))
        for element in some_list:
            self.assertTrue('points' in element)
            self.assertTrue('icon' in element)
            self.assertTrue('text' in element)

    def test_get_reputation_of(self):
        count, has_all_rights = ReviewHelper.get_reputation_of('Tobias')
        self.assertTrue(count == 0)
        self.assertTrue(has_all_rights)

        count, has_all_rights = ReviewHelper.get_reputation_of('Tobiass')
        self.assertTrue(count == 0)
        self.assertFalse(has_all_rights)
