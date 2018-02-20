import unittest

from dbas.database import DBDiscussionSession, get_dbas_db_configuration
from dbas.helper.tests import add_settings_to_appconfig
from search.requester import get_suggestions, get_duplicates_or_reasons, get_statements_with_value, get_edits


class TestRequester(unittest.TestCase):
    def setUp(self):
        settings = add_settings_to_appconfig()
        DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))

    def test_suggestions_not_empty_1(self):
        results = get_suggestions(2, True)
        self.assertNotEqual(0, len(results))

    def test_suggestions_not_empty_2(self):
        results = get_suggestions(2, False)
        self.assertNotEqual(0, len(results))

    def test_duplicates_or_reasons_1(self):
        results = get_duplicates_or_reasons(2, 4)
        self.assertNotEqual(0, len(results))

    def test_statements_with_value_has_url_1(self):
        url = get_statements_with_value(2, "http://localhost:4284")[0]["url"]
        self.assertIsNotNone(url)

    def test_edits_not_empty_1(self):
        results = get_edits(4, 58)
        self.assertNotEqual(0, len(results))

    def teardown_package(self):
        pass
