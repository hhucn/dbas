import unittest

from pyramid import testing

import dbas.review.helper.subpage as ReviewPageHelper
from dbas.strings.translator import Translator


class ReviewPageHelperTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_get_subpage_failure_nick_and_page(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='some nick', permissive=True)

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, 'some page', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_failure_page(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, 'some page', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_failure_nick(self):
        from dbas.review.helper.subpage import pages
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='some nick', permissive=True)

        ret_dict = ReviewPageHelper.get_subpage_elements_for(request, pages[0], Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_all_subpages(self):
        from dbas.review.helper.subpage import pages
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        for page in pages:
            ret_dict = ReviewPageHelper.get_subpage_elements_for(request, page, Translator('en'))
            self.assertIsNotNone(ret_dict['elements'])
            self.assertFalse(ret_dict['no_arguments_to_review'])
            self.assertTrue(ret_dict['has_access'])
            print(ret_dict['button_set'])
            self.assertTrue(el.startswith('is_' + page[0:4]) for el in ret_dict['button_set'])
