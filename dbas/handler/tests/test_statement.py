import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, TextVersion, ReviewEdit
from dbas.handler.statements import set_correction_of_statement
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class StatementsHandlerTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.trans = Translator('en')
        self.user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.tv = DBDiscussionSession.query(TextVersion).get(7)
        self.edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()

    def test_set_correction_of_statement(self):
        wrong_elements = [{'uid': 0, 'text': 'oh...this will crash'}]
        ret_dict = set_correction_of_statement(wrong_elements, self.user, self.trans)
        self.assertTrue(ret_dict['error'])
        self.assertEqual(ret_dict['info'], self.trans.get(_.internalKeyError))

        dupl_elements = [{'uid': self.edit.statement_uid, 'text': 'duplicate uid, statement already in review queue'}]
        ret_dict = set_correction_of_statement(dupl_elements, self.user, self.trans)
        self.assertTrue(ret_dict['error'])
        self.assertEqual(ret_dict['info'], self.trans.get(_.alreadyEditProposals))

        no_corr_elements = [{'uid': self.tv.statement_uid, 'text': self.tv.content}]
        ret_dict = set_correction_of_statement(no_corr_elements, self.user, self.trans)
        self.assertTrue(ret_dict['error'])
        self.assertEqual(ret_dict['info'], self.trans.get(_.noCorrections))

        right_elements = [{'uid': self.tv.statement_uid, 'text': self.tv.content + 'new part for edit'}]
        ret_dict = set_correction_of_statement(right_elements, self.user, self.trans)
        self.assertFalse(ret_dict['error'])
