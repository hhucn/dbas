import unittest

from pyramid import testing

from dbas.helper.tests import verify_dictionary_of_view


class ReviewHistoryViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import review_history as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        self.assertIn('history', response)
        self.assertTrue(len(response['history']) == 0)

    def test_page_logged_in(self):
        from dbas.views import review_history as d
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        self.assertIn('history', response)
        self.assertTrue(len(response['history']) != 0)
