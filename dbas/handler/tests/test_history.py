import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import History, Issue
from dbas.handler import history
from dbas.handler.history import split, get_last_relation
from dbas.tests.utils import TestCaseWithConfig


class HistoryHandlerTests(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.first_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).first()
        self.last_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).order_by(
            Issue.uid.desc()).first()
        self.history = '/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        settings = self.user_tobi.settings
        settings.set_last_topic_uid(self.first_issue.uid)
        DBDiscussionSession.add(settings)
        DBDiscussionSession.flush()

    def test_save_issue_uid(self):
        settings = self.user_tobi.settings
        self.assertNotEqual(self.last_issue.uid, settings.last_topic_uid)
        history.save_issue_uid(self.last_issue.uid, self.user_tobi)
        settings = self.user_tobi.settings
        self.assertEqual(self.last_issue.uid, settings.last_topic_uid)

    def test_get_saved_issue(self):
        settings = self.user_tobi.settings
        self.assertEqual(settings.last_topic_uid, history.get_last_issue_of(self.user_tobi).uid)

    def test_get_splitted_history(self):
        hist = history.split(self.history)
        self.assertGreater(len(hist), 0)

    def test_create_bubbles_from_history(self):
        bubbles = history.create_bubbles(self.history)
        self.assertGreater(len(bubbles), 0)

    def test_save_path_in_database(self):
        db_hist1 = DBDiscussionSession.query(History).filter_by(author_uid=self.user_tobi.uid).all()
        big_fucking_link = 'cat-or-dog/justify/13/agree/undercut?history=/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        history.save_database(self.user_tobi, 'cat-or-dog', big_fucking_link, self.history)
        db_hist2 = DBDiscussionSession.query(History).filter_by(author_uid=self.user_tobi.uid).all()
        self.assertLess(len(db_hist1), len(db_hist2))

    def test_get_history_from_database(self):
        big_fucking_link = 'cat-or-dog/justify/13/agree/undercut?history=/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        history.save_database(self.user_tobi, 'cat-or-dog', big_fucking_link, self.history)
        hist = history.get_from_database(self.user_tobi, 'en')
        self.assertGreater(len(hist), 0)

    def test_delete_history_in_database(self):
        self.assertTrue(history.delete_in_database(self.user_tobi))


class GetLastRelationTest(unittest.TestCase):
    def test_histry_empty(self):
        split_history = split('/')
        last_relation = get_last_relation(split_history)
        self.assertEqual(last_relation, '')

    def test_agree_at_end(self):
        split_history = split('/attitude/2-/justify/2/agree-/jump/11-/reaction/11/undermine/23-/justify/14/agree')
        last_relation = get_last_relation(split_history)
        self.assertEqual(last_relation, 'agree')

    def test_jump_at_end(self):
        split_history = split(
            '/attitude/2-/justify/2/agree-/jump/11-/reaction/11/undermine/23-/justify/14/agree-/jump/24')
        last_relation = get_last_relation(split_history)
        self.assertEqual(last_relation, '')
