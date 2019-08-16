from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import TextVersion, ReviewEdit, Statement
from dbas.handler.statements import set_correction_of_statement, find_existing_premisegroup
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class StatementsHandlerTest(TestCaseWithConfig):

    def setUp(self):
        super().setUp()
        self.trans = Translator('en')
        self.tv = DBDiscussionSession.query(TextVersion).get(7)
        self.edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()

    def test_set_correction_of_statement(self):
        wrong_elements = [{'uid': 0, 'text': 'oh...this will crash'}]
        ret_dict = set_correction_of_statement(wrong_elements, self.user_tobi, self.trans)
        self.assertTrue(ret_dict['error'])
        self.assertEqual(ret_dict['info'], self.trans.get(_.internalKeyError))

        dupl_elements = [{'uid': self.edit.statement_uid, 'text': 'duplicate uid, statement already in review queue'}]
        ret_dict = set_correction_of_statement(dupl_elements, self.user_tobi, self.trans)
        self.assertTrue(ret_dict['error'])
        self.assertEqual(ret_dict['info'], self.trans.get(_.alreadyEditProposals))

        no_corr_elements = [{'uid': self.tv.statement_uid, 'text': self.tv.content}]
        ret_dict = set_correction_of_statement(no_corr_elements, self.user_tobi, self.trans)
        self.assertTrue(ret_dict['error'])
        self.assertEqual(ret_dict['info'], self.trans.get(_.noCorrections))

        right_elements = [{'uid': self.tv.statement_uid, 'text': self.tv.content + 'new part for edit'}]
        ret_dict = set_correction_of_statement(right_elements, self.user_tobi, self.trans)
        self.assertFalse(ret_dict['error'])

    def test_find_existing_premisegroup(self):
        statement_fluffy = DBDiscussionSession.query(Statement).get(15)
        statement_small = DBDiscussionSession.query(Statement).get(16)
        premisegroup = find_existing_premisegroup([statement_fluffy, statement_small])
        self.assertEqual(premisegroup.uid, 12)

        statement_fluffy = DBDiscussionSession.query(Statement).get(15)
        premisegroup = find_existing_premisegroup([statement_fluffy])
        self.assertEqual(premisegroup, None)

        statement_capricious = DBDiscussionSession.query(Statement).get(6)
        premisegroup = find_existing_premisegroup([statement_capricious])
        self.assertEqual(premisegroup.uid, 3)
