import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view


class ReviewOngoingViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import ongoing_history as d

        request = testing.DummyRequest()
        self.assertEqual(400, d(request).status_code)

    def test_page_logged_in(self):
        from dbas.views import ongoing_history as d
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        self.assertIn('history', response)
        self.assertTrue(len(response['history']) != 0)
