import unittest

from pyramid import testing

from dbas.helper.test import verify_dictionary_of_view


class DiscussionAttitudeViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import discussion_attitude as d

        matchdict = {
            'slug': 'cat-or-dog',
            'statement_id': [2],
        }
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(response)

        # TODO test votes and seen
