import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

class DiscussionJumpViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import discussion_jump as d

        matchdict = {
            'slug': 'cat-or-dog',
            'arg_id': 12,
        }
        request = testing.DummyRequest(matchdict=matchdict)
        response = d(request)
        verify_dictionary_of_view(self, response)

    def test_page_on_failure(self):
        from dbas.views import discussion_jump as d

        matchdict = {
            'slug': 'cat-or-dog',
            'arg_id': 35,
        }
        request = testing.DummyRequest(matchdict=matchdict)
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass
