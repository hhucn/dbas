# coding=utf-8
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Issue, User, UserParticipation, StatementOrigins, Premise, \
    PremiseGroup, sql_timestamp_pretty_print
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


class PremiseTests(TestCaseWithConfig):
    def test_set_disabled(self):
        premise: Premise = DBDiscussionSession.query(Premise).get(2)
        self.assertFalse(premise.is_disabled)

        premise.set_disabled(True)

        self.assertTrue(premise.is_disabled)

    def test_set_premisegroup(self):
        premise: Premise = DBDiscussionSession.query(Premise).get(1)
        new_premisegroup: PremiseGroup = DBDiscussionSession.query(PremiseGroup).get(2)

        premise.set_premisegroup(new_premisegroup)

        self.assertEqual(new_premisegroup, premise.premisegroup)

    def test_set_statement(self):
        premise: Premise = DBDiscussionSession.query(Premise).get(1)
        new_statement: Statement = DBDiscussionSession.query(Statement).get(5)

        premise.set_statement(new_statement)

        self.assertEqual(new_statement, premise.statement)

    def test_get_text(self):
        premise: Premise = DBDiscussionSession.query(Premise).get(1)
        self.assertEqual(premise.statement.get_text(), premise.get_text())

    def test_to_dict(self):
        premise: Premise = DBDiscussionSession.query(Premise).get(1)

        expected_dict = {
            'premisegroup_uid': premise.premisegroup.uid,
            'statement_uid': premise.statement.uid,
            'is_negated': premise.is_negated,
            'author_uid': premise.author.uid,
            'timestamp': sql_timestamp_pretty_print(premise.timestamp),
            'issue_uid': premise.issue.uid,
            'is_disabled': premise.is_disabled
        }

        self.assertEqual(expected_dict, premise.to_dict())
