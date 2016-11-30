import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionJustifyViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_discussion_justify_statement_page(self):
        from dbas.views import discussion_justify as d

        matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff

    def test_discussion_dont_know_statement_page(self):
        from dbas.views import discussion_justify as d

        matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'd',
            'relation': '',
        }
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff

    def test_discussion_justify_argument_page(self):
        from dbas.views import discussion_justify as d

        matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': ['undermine'],
        }
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff
