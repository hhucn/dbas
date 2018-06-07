import unittest

import transaction
from pyramid import testing

from nose.tools import assert_true, assert_less, assert_equal, assert_greater, assert_is_none, assert_not_equal
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, History, Issue
from dbas.handler import history


class HistoryHandlerTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.first_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).first()
        self.last_issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).order_by(Issue.uid.desc()).first()
        self.history = '/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        settings = self.user.settings
        settings.set_last_topic_uid(self.first_issue.uid)
        DBDiscussionSession.add(settings)
        DBDiscussionSession.flush()
        transaction.commit()

    def test_save_issue_uid(self):
        settings = self.user.settings
        assert_not_equal(self.last_issue.uid, settings.last_topic_uid)
        history.save_issue_uid(self.last_issue.uid, self.user)
        settings = self.user.settings
        assert_equal(self.last_issue.uid, settings.last_topic_uid)

    def test_get_saved_issue(self):
        assert_is_none(history.get_last_issue_of(None))
        settings = self.user.settings
        assert_equal(settings.last_topic_uid, history.get_last_issue_of(self.user).uid)

    def test_get_splitted_history(self):
        hist = history.split(self.history)
        assert_greater(len(hist), 0)

    def test_create_bubbles_from_history(self):
        bubbles = history.create_bubbles(self.history)
        assert_greater(len(bubbles), 0)

    def test_save_path_in_database(self):
        db_hist1 = DBDiscussionSession.query(History).filter_by(author_uid=self.user.uid).all()
        big_fucking_link = 'cat-or-dog/justify/13/agree/undercut?history=/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        history.save_database(self.user, 'cat-or-dog', big_fucking_link, self.history)
        db_hist2 = DBDiscussionSession.query(History).filter_by(author_uid=self.user.uid).all()
        assert_less(len(db_hist1), len(db_hist2))

    def test_get_history_from_database(self):
        big_fucking_link = 'cat-or-dog/justify/13/agree/undercut?history=/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        history.save_database(self.user, 'cat-or-dog', big_fucking_link, self.history)
        hist = history.get_from_database(self.user, 'en')
        assert_greater(len(hist), 0)

    def test_delete_history_in_database(self):
        assert_true(history.delete_in_database(self.user))
