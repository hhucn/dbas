from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReference, User, Statement, Issue
from dbas.handler.references import get_references_for_argument, get_references_for_statements, set_reference
from dbas.lib import get_text_for_statement_uid
from dbas.tests.utils import TestCaseWithConfig


class ReferenceHelperTest(TestCaseWithConfig):
    def test_get_references_for_argument(self):
        val_data, val_text = get_references_for_argument(0, 'base_url')
        self.__validate_reference_text([], val_text)
        self.__validate_reference_data([], val_data)

        val_data, val_text = get_references_for_argument(None, 'base_url')
        self.__validate_reference_text([], val_text)
        self.__validate_reference_data([], val_data)

        val_data, val_text = get_references_for_argument(12, 'base_url')
        self.__validate_reference_text([2, 15, 16], val_text)
        self.__validate_reference_data([2, 15, 16], val_data)

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
        user: User = DBDiscussionSession.query(User).get(2)
        statement: Statement = DBDiscussionSession.query(Statement).get(3)
        issue: Issue = statement.issues[0]
        val: bool = set_reference('some_reference#42', 'http://www.fortschrittskolleg.de/', user, statement, issue)
        self.assertTrue(val)

        DBDiscussionSession.query(StatementReference).filter_by(text='some_reference#42').delete()

    def __validate_reference_data(self, uids, ddict):
        for key in ddict:
            self.assertIn(key, uids)
            refs = ddict[key]
            for ref in refs:
                self.assertIn('uid', ref)
                self.assertIn('statement_text', ref)
                self.assertEquals(ref['statement_text'], get_text_for_statement_uid(key))
                db_ref = DBDiscussionSession.query(StatementReference).get(ref['uid'])
                self.assertEquals(ref['statement_text'], get_text_for_statement_uid(db_ref.statement_uid))

    def __validate_reference_text(self, uids, ddict):
        for key in ddict:
            self.assertIn(key, uids)
            self.assertEquals(ddict[key], get_text_for_statement_uid(key))
