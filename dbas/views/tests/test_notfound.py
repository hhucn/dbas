import unittest

from cornice.util import _JSONError
from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views import notfound, main_api


class NotFoundViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = construct_dummy_request()
        response = notfound(request)
        verify_dictionary_of_view(response)

    def test_empty_route(self):
        request = construct_dummy_request()
        response = main_api(request)
        self.assertEqual(_JSONError, type(response))
