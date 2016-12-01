import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class ReviewReputationViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

        # TODO test review system

    def tearDown(self):
        testing.tearDown()

    def test_review_reputation_page(self):
        from dbas.views import review_reputation as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertIn('reputation', response)
        self.assertTrue(len(response['reputation']) == 0)

    def test_review_reputation_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_reputation as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertIn('reputation', response)
        self.assertTrue(len(response['reputation']) != 0)
