import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.views.discussion.rendered import attitude


class DiscussionAttitudeViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'statement_id': 2,
        })
        response = attitude(request)
        verify_dictionary_of_view(response)
