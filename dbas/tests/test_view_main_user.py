import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class MainUserViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_main_user_page(self):
        from dbas.views import main_user as d

        matchdict = {
            'nickname': 'tobias',
        }
        request = testing.DummyRequest()
        request.matchdict = matchdict
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff
