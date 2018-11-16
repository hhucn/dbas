import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views import jump


class DiscussionJumpViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-dog',
            'argument_id': 12,
        })
        response = jump(request)
        verify_dictionary_of_view(response)

    def test_page_on_failure(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-dog',
            'argument_id': 35,
        })
        response = jump(request)
        self.assertEqual(400, response.status_code)
