import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views import finish


class DiscussionFinishViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')


    def test_page(self):
        request = construct_dummy_request(match_dict={'argument_id': 10, 'slug': 'cat-or-dog'})
        response = finish(request)
        verify_dictionary_of_view(response)
