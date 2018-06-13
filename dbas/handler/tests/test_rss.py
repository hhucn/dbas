import unittest

import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import RSS, User
from dbas.handler import rss
from dbas.lib import get_global_url
from dbas.query_wrapper import get_enabled_issues_as_query


class RSSHandlerTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

    def test_create_news_rss(self):
        self.assertTrue(rss.create_news_rss(get_global_url(), 'en'))

    def test_create_initial_issue_rss(self):
        self.assertTrue(rss.create_initial_issue_rss(get_global_url(), 'en'))
        return True

    def test_append_action_to_issue_rss(self):
        db_issue = get_enabled_issues_as_query().first()
        l1 = DBDiscussionSession.query(RSS).count()
        self.assertTrue(
            rss.append_action_to_issue_rss(db_issue, self.user, 'test_title', 'test_description', get_global_url()))
        l2 = DBDiscussionSession.query(RSS).count()
        self.assertEqual(l1 + 1, l2)

        DBDiscussionSession.query(RSS).filter(RSS.issue_uid == db_issue.uid, RSS.author_uid == self.user.uid,
                                              RSS.title == 'test_title', RSS.description == 'test_description').delete()
        DBDiscussionSession.flush()
        transaction.commit()
        l3 = DBDiscussionSession.query(RSS).count()
        self.assertEqual(l2 - 1, l3, "RSS appended more than once.")
        self.assertTrue(rss.rewrite_issue_rss(1, get_global_url()))

    def test_get_list_of_all_feeds(self):
        l1 = get_enabled_issues_as_query().count()
        resp = rss.get_list_of_all_feeds('en')
        self.assertTrue(l1, len(resp))
        for f in resp:
            self.assertIn('title', f)
            self.assertIn('description', f)
            self.assertIn('link', f)
