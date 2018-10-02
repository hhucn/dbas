# coding=utf-8
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Issue
from dbas.tests.utils import TestCaseWithConfig


class StatementTests(TestCaseWithConfig):

    def test_issues(self):
        some_statments = DBDiscussionSession.query(Statement).all()[:10]

        for statement in some_statments:
            issues = statement.issues
            self.assertIsInstance(issues, set)
            for issue in issues:
                self.assertIsInstance(issue, Issue)
