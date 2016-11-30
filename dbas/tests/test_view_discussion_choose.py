import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionChhoseViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_discussion_choose_page(self):
        from dbas.views import discussion_choose as d

        matchdict = {
            'slug': 'cat-or-dog',
            'is_argument': 'f',
            'supportive': 't',
            'id': 5,
            'pgroup_ids': [15, 17],
        }
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff
