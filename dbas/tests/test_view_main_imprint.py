import unittest

from pyramid import testing

from dbas.helper.tests import verify_dictionary_of_view


class MainImprintViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_imprint as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff
