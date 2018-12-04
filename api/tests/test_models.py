from api.models import DataItem, DataBubble, DataReference, DataIssue, DataStatement
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReference, Issue, Statement, TextVersion
from dbas.tests.utils import TestCaseWithConfig


class TestModels(TestCaseWithConfig):

    def test_DataItem_to_json(self):
        di = DataItem(htmls=['foo', 'bar', 'baz'], url='http://coconut.com')
        self.assertIsInstance(di.__json__(), dict)
        for key in di.__json__().keys():
            self.assertIn(key, ['url', 'htmls', 'texts'])

    def test_DataBubble_to_json(self):
        bubble = {
            'is_user': True,
            'is_system': True,
            'is_info': True,
            'bubble_url': 'Coconut',
            'message': 'Coconut'
        }
        db = DataBubble(bubble)
        self.assertIsInstance(db.__json__(), dict)
        for key in db.__json__().keys():
            self.assertIn(key, ['type', 'html', 'url', 'text'])

    def test_DataReference_to_json(self):
        ref = DBDiscussionSession.query(StatementReference).filter_by(statement_uid=15).first()
        sr = DataReference(ref)
        self.assertIsInstance(sr.__json__(), dict)
        for key in sr.__json__().keys():
            self.assertIn(key, ['uid', 'text', 'url'])

    def test_DataIssue_to_json(self):
        issue = DBDiscussionSession.query(Issue).filter_by(uid=1).first()
        di = DataIssue(issue)
        self.assertIsInstance(di.__json__(), dict)
        for key in di.__json__().keys():
            self.assertIn(key, ['uid', 'slug', 'lang', 'title', 'info'])

    def test_DataStatement_to_json(self):
        statement = DBDiscussionSession.query(Statement).filter_by(uid=1).first()
        issue = DBDiscussionSession.query(TextVersion).filter_by(uid=1).first()
        ds = DataStatement(statement, issue)
        self.assertIsInstance(ds.__json__(), dict)
        for key in ds.__json__().keys():
            self.assertIn(key, ['uid', 'isPosition', 'text'])
