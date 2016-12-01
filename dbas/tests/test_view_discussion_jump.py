import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionJumpViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_discussion_jump_page(self):
        from dbas.views import discussion_jump as d

        matchdict = {
            'slug': 'cat-or-dog',
            'arg_id': 12,
        }
        request = testing.DummyRequest(matchdict=matchdict)
        response = d(request)
        verify_dictionary_of_view(self, response)

    def test_discussion_jump_page_on_failure(self):
        from dbas.views import discussion_jump as d

        matchdict = {
            'slug': 'cat-or-dog',
            'arg_id': 35,
        }
        request = testing.DummyRequest(matchdict=matchdict)
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)
