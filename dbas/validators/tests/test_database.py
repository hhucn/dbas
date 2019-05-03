from dbas.database.discussion_model import Statement
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request
from dbas.validators.database import valid_table_name, valid_database_model


class TestValidDatabase(TestCaseWithConfig):
    def test_valid_table_name(self):
        request = construct_dummy_request()
        response = valid_table_name(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(json_body={'table': 'Stateme'})
        response = valid_table_name(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        for t in ['statement', 'StAtement']:
            request = construct_dummy_request(json_body={'table': t})
            response = valid_table_name(request)
            self.assertTrue(response)
            self.assertIsInstance(response, bool)

    def test_valid_database_model(self):
        request = construct_dummy_request()
        response = valid_database_model('', '')(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request()
        response = valid_database_model('k', '')(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request()
        response = valid_database_model('', 't')(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(json_body={'k': 0})
        response = valid_database_model('k', Statement)(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(json_body={'k': 1})
        response = valid_database_model('k', Statement)(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
