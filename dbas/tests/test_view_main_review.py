import unittest

from pyramid import testing

from dbas.helper.tests import verify_dictionary_of_view


class MainReviewViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_review as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('issues', response)
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
        from dbas.views import main_review as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('issues', response)
        self.assertIn('reputation', response)
        self.assertTrue(response['reputation']['has_all_rights'])
        self.assertTrue(type(response['reputation']['count']) is int)
