import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import History, Issue
from dbas.handler import history
from dbas.handler.history import split, get_last_relation, SessionHistory
from dbas.tests.utils import TestCaseWithConfig


class HistoryBubblesTests(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.first_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).first()
        self.last_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).order_by(
            Issue.uid.desc()).first()
        self.history_justify = '/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        self.history_dontknow = '/attitude/3-/justify/4/dontknow'
        self.history_disagree = '/attitude/3-attitude/3-justify/3/disagree-/reaction/5/undercut/7'
        self.history_agree = '/attitude/3-justify/3/agree-/reaction/4/rebut/5'
        self.session_history_justify = SessionHistory(self.history_justify)
        self.session_history_dontknow = SessionHistory(self.history_dontknow)
        self.session_history_disagree = SessionHistory(self.history_disagree)
        self.session_history_agree = SessionHistory(self.history_agree)
        settings = self.user_tobi.settings
        settings.last_topic = self.first_issue
        DBDiscussionSession.add(settings)
        DBDiscussionSession.flush()

    def test_create_bubbles_from_history_justify(self):
        bubbles = self.session_history_justify.create_bubbles()
        self.assertGreater(len(bubbles), 0)

    def test_create_bubbles_from_history_dontknow(self):
        bubbles = self.session_history_dontknow.create_bubbles()
        self.assertGreater(len(bubbles), 0)

    def test_create_bubbles_from_history_disagree(self):
        bubbles = self.session_history_disagree.create_bubbles()
        self.assertGreater(len(bubbles), 0)

    def test_create_bubbles_from_history_agree(self):
        bubbles = self.session_history_agree.create_bubbles()
        self.assertGreater(len(bubbles), 0)


class HistoryHandlerTests(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.first_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).first()
        self.last_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).order_by(
            Issue.uid.desc()).first()
        self.history = '/attitude/3-/justify/4/dontknow'
        self.session_history = SessionHistory(self.history)
        settings = self.user_tobi.settings
        settings.last_topic = self.first_issue
        DBDiscussionSession.add(settings)
        DBDiscussionSession.flush()

    def test_save_issue(self):
        settings = self.user_tobi.settings
        self.assertNotEqual(self.last_issue.uid, settings.last_topic_uid)
        history.save_issue(self.last_issue, self.user_tobi)
        DBDiscussionSession.flush()
        settings = self.user_tobi.settings
        self.assertEqual(self.last_issue.uid, settings.last_topic_uid)

    def test_get_saved_issue(self):
        settings = self.user_tobi.settings
        self.assertEqual(settings.last_topic_uid, history.get_last_issue_of(self.user_tobi).uid)

    def test_get_splitted_history(self):
        hist = history.split(self.history)
        self.assertGreater(len(hist), 0)

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
        self.assertIsNone(DBDiscussionSession.query(History).filter_by(author=self.user_tobi).one_or_none())


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
