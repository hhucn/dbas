import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view
from dbas.views.discussion.rendered import dexit


class DiscussionFinishViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = testing.DummyRequest()
        response = dexit(request)
        verify_dictionary_of_view(response)
