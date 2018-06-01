import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, TextVersion, ReviewEdit
from dbas.handler.statements import set_correction_of_statement
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class StatementsHandlerTest(unittest.TestCase):

    def test_set_correction_of_statement(self):
        db_tv = DBDiscussionSession.query(TextVersion).get(7)
        db_edit = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()
        trans = Translator('en')
        wrong_elements = [{'uid': 0, 'text': 'oh...this will crash'}]
        dupl_elements = [{'uid': db_edit.uid, 'text': 'duplicate uid, already in review'}]
        no_corr_elements = [{'uid': db_tv.statement_uid, 'text': db_tv.content}]
        right_elements = [{'uid': db_tv.statement_uid, 'text': db_tv.content + 'new part for edit'}]
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        text, error = set_correction_of_statement(wrong_elements, db_user, trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.internalKeyError))

        text, error = set_correction_of_statement(dupl_elements, db_user, trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.alreadyEditProposals))

        text, error = set_correction_of_statement(no_corr_elements, db_user, trans)
        self.assertTrue(error)
        self.assertEqual(text, trans.get(_.noCorrections))

        text, error = set_correction_of_statement(right_elements, db_user, trans)
        self.assertFalse(error)
