import unittest

from dbas.views import notfound, main_api

from dbas.tests.utils import construct_dummy_request
from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view


class NotFoundViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = construct_dummy_request()
        response = notfound(request)
        verify_dictionary_of_view(response)

    def test_empty_route(self):
        request = testing.DummyRequest()
        response = main_api(request)
        self.assertEqual(response['status'], 'error')
