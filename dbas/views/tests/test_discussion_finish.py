import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.views import discussion_finish


class DiscussionFinishViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = testing.DummyRequest(matchdict={'argument_id': 10, 'slug': 'cat-or-dog'})
        response = discussion_finish(request)
        verify_dictionary_of_view(response)
