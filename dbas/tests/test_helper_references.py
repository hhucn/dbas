import unittest

import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences
from dbas.helper.references import get_references_for_argument, get_references_for_statements, set_reference
from dbas.lib import get_text_for_statement_uid


class ReferenceHelperTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_get_references_for_argument(self):
        val_data, val_text = get_references_for_argument(0, 'base_url')
        self.__validate_reference_text([], val_text)
        self.__validate_reference_data([], val_data)

        val_data, val_text = get_references_for_argument(None, 'base_url')
        self.__validate_reference_text([], val_text)
        self.__validate_reference_data([], val_data)

        val_data, val_text = get_references_for_argument(12, 'base_url')
        self.__validate_reference_text([15, 16], val_text)
        self.__validate_reference_data([15, 16], val_data)

        val_data, val_text = get_references_for_argument([12, 13], 'base_url')
        self.__validate_reference_text([12, 13], val_text)
        self.__validate_reference_data([12, 13], val_data)

    def test_get_references_for_statements(self):
        val_data, val_text = get_references_for_statements([], 'base_url')
        self.__validate_reference_text([], val_text)
        self.__validate_reference_data([], val_data)

        val_data, val_text = get_references_for_statements([15], 'base_url')
        self.__validate_reference_text([15], val_text)
        self.__validate_reference_data([15], val_data)

        val_data, val_text = get_references_for_statements([14, 15], 'base_url')
        self.__validate_reference_text([14, 15], val_text)
        self.__validate_reference_data([14, 15], val_data)

        val_data, val_text = get_references_for_statements([14, 15, 16], 'base_url')
        self.__validate_reference_text([14, 15, 16], val_text)
        self.__validate_reference_data([14, 15, 16], val_data)

    def test_set_reference(self):
        self.assertEqual(1, 1)

        val = set_reference('some_reference#42', 'some_url', 'bla_user', 3, 1)
        self.assertFalse(val)

        val = set_reference('some_reference#42', 'http://www.fortschrittskolleg.de/', 'bla_user', 3, 1)
        self.assertFalse(val)

        val = set_reference('some_reference#42', 'http://www.fortschrittskolleg.de/', 'tobias', 3, 1)
        self.assertFalse(val)

        val = set_reference('some_reference#42', 'http://www.fortschrittskolleg.de/', 'Tobias', 3, 1)
        self.assertTrue(val)

        DBDiscussionSession.query(StatementReferences).filter_by(reference='some_reference#42').delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def __validate_reference_data(self, uids, dict):
        for key in dict:
            self.assertIn(key, uids)
            refs = dict[key]
            for ref in refs:
                self.assertIn('uid', ref)
                self.assertIn('statement_text', ref)
                self.assertEquals(ref['statement_text'], get_text_for_statement_uid(key))
                db_ref = DBDiscussionSession.query(StatementReferences).get(ref['uid'])
                self.assertEquals(ref['statement_text'], get_text_for_statement_uid(db_ref.statement_uid))

    def __validate_reference_text(self, uids, dict):
        for key in dict:
            self.assertIn(key, uids)
            self.assertEquals(dict[key], get_text_for_statement_uid(key))
