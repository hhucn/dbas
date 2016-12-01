import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPFound

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

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        # TODO VOTES ???
        # wo kommen die votes ins spiel?

    def test_discussion_dont_know_statement_page(self):
        from dbas.views import discussion_justify as d

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'd',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

    def test_discussion_justify_argument_page(self):
        from dbas.views import discussion_justify as d

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': ['undermine'],
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

    def test_discussion_justify_false_page(self):
        from dbas.views import discussion_justify as d

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': 'blabla',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 40,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'babla',
            'relation': '',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-doggy-dog-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)
