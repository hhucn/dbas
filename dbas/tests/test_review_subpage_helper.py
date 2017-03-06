import unittest

from pyramid import testing

import dbas.review.helper.subpage as ReviewPageHelper
from dbas.strings.translator import Translator


class ReviewPageHelperTest(unittest.TestCase):

    def test_get_subpage_failure_nick_and_page(self):
        request = testing.DummyRequest()

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, 'some page', 'some nick', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_failure_page(self):
        request = testing.DummyRequest()

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, 'some page', 'Tobias', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_failure_nick(self):
        from dbas.review.helper.subpage import pages
        request = testing.DummyRequest()

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, pages[0], 'some nick', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_all_subpages(self):
        from dbas.review.helper.subpage import pages
        request = testing.DummyRequest()

        for page in pages:
            ret_dict = ReviewPageHelper.get_subpage_elements_for(request, page, 'Tobias', Translator('en'))
            self.assertIsNotNone(ret_dict['elements'])
            self.assertFalse(ret_dict['no_arguments_to_review'])
            self.assertTrue(ret_dict['has_access'])
