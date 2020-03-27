# coding=utf-8
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Issue, User, UserParticipation, StatementOrigins
from dbas.tests.utils import TestCaseWithConfig


class TestStatementOrigins(TestCaseWithConfig):
    def test_initialization(self):
        origin = StatementOrigins("my-id", "my-host", 1, self.user_christian.nickname, self.statement_cat_or_dog)
        self.assertTrue(origin)


class StatementTests(TestCaseWithConfig):

    def test_issues(self):
        some_statments = DBDiscussionSession.query(Statement).all()[:10]

        for statement in some_statments:
            issues = statement.issues
            for issue in issues:
                self.assertIsInstance(issue, Issue)


class UserParticipatesInIssueTest(TestCaseWithConfig):

    def test_user_to_issues(self):
        db_user: User = User.by_nickname("Björn")
        issue: Issue = DBDiscussionSession.query(Issue).get(8)

        self.assertNotIn(issue, db_user.participates_in)
        db_user.participates_in.append(issue)
        self.assertIn(issue, db_user.participates_in)

        association: UserParticipation = DBDiscussionSession.query(UserParticipation).filter_by(
            user_uid=db_user.uid, issue_uid=issue.uid).one_or_none()

        self.assertIsNotNone(association)

        DBDiscussionSession.query(UserParticipation).filter_by(
            user_uid=db_user.uid, issue_uid=issue.uid).delete()
