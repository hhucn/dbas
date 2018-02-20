import unittest

import transaction
from pyramid import testing

from nose.tools import assert_false, assert_true, assert_less, assert_equal, assert_greater, assert_is_none
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, History, Settings, Issue
from dbas.handler import history


class HistoryHandlerTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).first()
        self.settings = DBDiscussionSession.query(Settings).get(self.user.uid)
        self.settings.set_last_topic_uid(self.issue.uid)
        DBDiscussionSession.add(self.settings)
        DBDiscussionSession.flush()
        transaction.commit()
        self.history = '/attitude/2-/justify/2/t-/reaction/12/undercut/13'

    def test_save_issue_uid(self):
        assert_false(history.save_issue_uid(self.issue.uid, 'Tobia'))
        assert_true(history.save_issue_uid(self.issue.uid, 'Tobias'))
        assert_equal(self.issue.uid, self.settings.last_topic_uid)

    def test_get_saved_issue(self):
        assert_is_none(history.get_saved_issue('Tobia'))
        assert_equal(self.settings.last_topic_uid, history.get_saved_issue(self.user.nickname))

    def test_get_splitted_history(self):
        hist = history.get_splitted_history(self.history)
        assert_greater(len(hist), 0)

    def test_create_bubbles_from_history(self):
        bubbles = history.create_bubbles_from_history(self.history)
        assert_greater(len(bubbles), 0)

    def test_get_bubble_from_reaction_step(self):
        # TODO history.get_bubble_from_reaction_step
        return True

    def test_save_path_in_database(self):
        db_hist1 = DBDiscussionSession.query(History).filter_by(author_uid=self.user.uid).all()
        big_fucking_link = 'cat-or-dog/justify/13/t/undercut?history=/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        history.save_path_in_database(self.user.nickname, 'cat-or-dog', big_fucking_link, self.history)
        db_hist2 = DBDiscussionSession.query(History).filter_by(author_uid=self.user.uid).all()
        assert_less(len(db_hist1), len(db_hist2))

    def test_get_history_from_database(self):
        big_fucking_link = 'cat-or-dog/justify/13/t/undercut?history=/attitude/2-/justify/2/t-/reaction/12/undercut/13'
        history.save_path_in_database(self.user.nickname, 'cat-or-dog', big_fucking_link, self.history)
        hist = history.get_history_from_database(self.user, 'en')
        assert_greater(len(hist), 0)

    def test_delete_history_in_database(self):
        assert_true(history.delete_history_in_database(self.user))

    def test_handle_history(self):
        # TODO history.handle_history
        return True
