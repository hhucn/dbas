import unittest

from pyramid import testing
from dbas.review.helper.subpage import pages
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewContentViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_review_content_page_deletes(self):
        from dbas.views import review_content as d

        matchdict = {'queue': 'deletes'}
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff

    def test_review_content_page_edits(self):
        from dbas.views import review_content as d

        matchdict = {'queue': 'edits'}
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff

    def test_review_content_page_optimizations(self):
        from dbas.views import review_content as d

        matchdict = {'queue': 'optimizations'}
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff

    def test_review_content_page_history(self):
        from dbas.views import review_content as d

        matchdict = {'queue': 'history'}
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff
