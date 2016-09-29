import unittest

import dbas.review.helper.subpage as ReviewPageHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import translator
from pyramid import testing
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewPageHelperTest(unittest.TestCase):

    def test_get_subpage_for(self):
        from dbas.review.helper.subpage import pages
        request = testing.DummyRequest()
        mainpage = 'http://abd'

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, 'some page', 'some nick', translator('en'), mainpage)
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, 'some page', 'Tobias', translator('en'), mainpage)
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, pages[0], 'Tobias', translator('en'), mainpage)
        self.assertIsNotNone(ret_dict['elements'])
        self.assertTrue(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, pages[0], 'some nick', translator('en'), mainpage)
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

        for page in pages:
            ret_dict = ReviewPageHelper.get_subpage_elements_for(request, page, 'Tobias', translator('en'), mainpage)
            if 'edit' in page:
                self.assertIsNone(ret_dict['elements'])
                self.assertTrue(ret_dict['no_arguments_to_review'])
            else:
                self.assertIsNotNone(ret_dict['elements'])
                self.assertFalse(ret_dict['no_arguments_to_review'])
            self.assertTrue(ret_dict['has_access'])
