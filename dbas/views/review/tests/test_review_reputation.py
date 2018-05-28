import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.views.review.rendered import reputation


class ReviewReputationViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):

        request = testing.DummyRequest()
        response = reputation(request)
        verify_dictionary_of_view(response)
        self.assertIn('reputation', response)
        self.assertTrue(len(response['reputation']) == 0)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = testing.DummyRequest()
        response = reputation(request)
        verify_dictionary_of_view(response)
        self.assertIn('reputation', response)
        self.assertTrue(len(response['reputation']) != 0)
