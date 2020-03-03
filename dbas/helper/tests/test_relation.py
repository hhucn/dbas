import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Premise, ClickedArgument, SeenArgument, PremiseGroup
from dbas.helper.relation import get_undermines_for_argument_uid, get_undercuts_for_argument_uid, \
    get_rebuts_for_argument_uid, get_supports_for_argument_uid, set_new_undermine_or_support_for_pgroup, \
    set_new_undercut, set_new_rebut, set_new_support
from dbas.tests.utils import TestCaseWithConfig


class RelationHelperTest(TestCaseWithConfig):
    def tearDown(self):
        for uid in [arg.uid for arg in
                    DBDiscussionSession.query(Argument).filter_by(author_uid=self.user_christian.uid).all()]:
            DBDiscussionSession.query(ClickedArgument).filter_by(argument_uid=uid).delete()
            DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=uid).delete()
        DBDiscussionSession.query(Argument).filter_by(author_uid=self.user_christian.uid).delete()
        DBDiscussionSession.flush()
        transaction.commit()
        super().tearDown()

    def test_get_undermines_for_argument_uid(self):
        val = get_undermines_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_undermines_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_undermines_for_argument_uid(100)
        self.assertEqual(len(val), 0)

        val = get_undermines_for_argument_uid(11)
        self.assertEqual(len(val), 1)

        val = get_undermines_for_argument_uid('11')
        self.assertEqual(len(val), 1)

    def test_get_undercuts_for_argument_uid(self):
        val = get_undercuts_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_undercuts_for_argument_uid(100)
        self.assertIsNone(val)

        val = get_undercuts_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_undercuts_for_argument_uid(36)
        self.assertGreaterEqual(len(val), 1)

        val = get_undercuts_for_argument_uid('36')
        self.assertGreaterEqual(len(val), 1)

    def test_get_rebuts_for_argument_uid(self):
        val = get_rebuts_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_rebuts_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_rebuts_for_argument_uid(100)
        self.assertIsNone(val)

        val = get_rebuts_for_argument_uid(62)
        self.assertEqual(len(val), 2)

        val = get_rebuts_for_argument_uid('62')
        self.assertEqual(len(val), 2)

    def test_get_supports_for_argument_uid(self):
        val = get_supports_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_supports_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_supports_for_argument_uid(100)
        self.assertEqual(len(val), 0)

        val = get_supports_for_argument_uid(3)
        self.assertEqual(len(val), 1)

        val = get_supports_for_argument_uid('3')
        self.assertEqual(len(val), 1)

    def test_set_new_undermine_or_support_for_pgroup(self):
        db_argument = DBDiscussionSession.query(Argument).get(1)
        db_premise = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).first()

        before = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == 1,
                                                            Argument.conclusion_uid == db_premise.statement_uid).all()
        set_new_undermine_or_support_for_pgroup(DBDiscussionSession.query(PremiseGroup).get(1), db_argument, False,
                                                self.user_christian, self.issue_cat_or_dog)
        after = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == 1,
                                                           Argument.conclusion_uid == db_premise.statement_uid).all()
        self.assertEqual(len(before), len(after))

    def test_set_new_undercut(self):
        db_argument: Argument = DBDiscussionSession.query(Argument).get(1)

        before = db_argument.arguments
        set_new_undercut(DBDiscussionSession.query(PremiseGroup).get(1), db_argument, self.user_christian,
                         self.issue_cat_or_dog)
        after = DBDiscussionSession.query(Argument).filter_by(argument_uid=1).all()
        self.assertLess(len(before), len(after))

    def test_set_new_rebut(self):
        db_argument = DBDiscussionSession.query(Argument).get(1)

        before = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_argument.conclusion_uid).all()
        set_new_rebut(DBDiscussionSession.query(PremiseGroup).get(1), db_argument, self.user_christian,
                      self.issue_cat_or_dog)
        after = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_argument.conclusion_uid).all()
        self.assertLess(len(before), len(after))

    def test_set_new_support(self):
        db_argument = DBDiscussionSession.query(Argument).get(1)

        before = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == 1,
                                                            Argument.conclusion_uid == db_argument.conclusion_uid).all()
        set_new_support(DBDiscussionSession.query(PremiseGroup).get(1), db_argument, self.user_christian,
                        self.issue_cat_or_dog)
        after = DBDiscussionSession.query(Argument).filter(Argument.premisegroup_uid == 1,
                                                           Argument.conclusion_uid == db_argument.conclusion_uid).all()
        self.assertLess(len(before), len(after))
