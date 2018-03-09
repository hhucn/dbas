"""
Namespace to re-use commonly used components for testing.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue


class TestCaseWithConfig(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.issue_disabled: Issue = DBDiscussionSession.query(Issue).get(6)
        self.issue_cat_or_dog: Issue = DBDiscussionSession.query(Issue).get(2)

    def tearDown(self):
        testing.tearDown()
