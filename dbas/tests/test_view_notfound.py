import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config


class NotFoundViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import notfound as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        # place for additional stuff
