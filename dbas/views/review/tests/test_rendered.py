import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.views.review.rendered import overview


class MainReviewViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = testing.DummyRequest()
        response = overview(request)
        verify_dictionary_of_view(response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('reputation', response)
        self.assertFalse(response['reputation']['has_all_rights'])
        self.assertTrue(response['reputation']['count'] == 0)


class MainReviewViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = testing.DummyRequest()
        response = overview(request)
        verify_dictionary_of_view(response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('reputation', response)
        self.assertTrue(response['reputation']['has_all_rights'])
        self.assertTrue(type(response['reputation']['count']) is int)
