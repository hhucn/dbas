import unittest

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, Premise
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config
from dbas.helper.relation import get_undermines_for_argument_uid, get_undercuts_for_argument_uid, \
    get_rebuts_for_argument_uid, get_supports_for_argument_uid, set_new_undermine_or_support_for_pgroup, \
    set_new_undercut, set_new_rebut, set_new_support

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class RelationHelperTest(unittest.TestCase):

    def test_get_undermines_for_argument_uid(self):
        val = get_undermines_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_undermines_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_undermines_for_argument_uid(100)
        self.assertEqual(len(val), 0)

        val = get_undermines_for_argument_uid(3)
        self.assertEqual(len(val), 2)

        val = get_undermines_for_argument_uid('3')
        self.assertEqual(len(val), 2)

    def test_get_undercuts_for_argument_uid(self):
        val = get_undercuts_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_undercuts_for_argument_uid(100)
        self.assertIsNone(val)

        val = get_undercuts_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_undercuts_for_argument_uid(2)
        self.assertEqual(len(val), 1)

        val = get_undercuts_for_argument_uid('2')
        self.assertEqual(len(val), 1)

    def test_get_rebuts_for_argument_uid(self):
        val = get_rebuts_for_argument_uid('a')
        self.assertIsNone(val)

        val = get_rebuts_for_argument_uid(0)
        self.assertIsNone(val)

        val = get_rebuts_for_argument_uid(100)
        self.assertIsNone(val)

        val = get_rebuts_for_argument_uid(2)
        self.assertEqual(len(val), 1)

        val = get_rebuts_for_argument_uid('2')
        self.assertEqual(len(val), 1)

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
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_argument = DBDiscussionSession.query(Argument).get(1)
        db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).first()

        before = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == 1,
                                                                 Argument.conclusion_uid == db_premise.statement_uid)).all()
        set_new_undermine_or_support_for_pgroup(1, db_argument, False, db_user, 2)
        after = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == 1,
                                                                Argument.conclusion_uid == db_premise.statement_uid)).all()
        self.assertLess(len(before), len(after))

        before = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == 1,
                                                                 Argument.conclusion_uid == db_premise.statement_uid)).all()
        set_new_undermine_or_support_for_pgroup(1, db_argument, True, db_user, 2)
        after = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == 1,
                                                                Argument.conclusion_uid == db_premise.statement_uid)).all()
        self.assertLess(len(before), len(after))

    def test_set_new_undercut(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_argument = DBDiscussionSession.query(Argument).get(1)

        before = DBDiscussionSession.query(Argument).filter_by(argument_uid=1).all()
        set_new_undercut(1, db_argument, db_user, 2)
        after = DBDiscussionSession.query(Argument).filter_by(argument_uid=1).all()
        self.assertLess(len(before), len(after))

    def test_set_new_rebut(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_argument = DBDiscussionSession.query(Argument).get(1)

        before = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_argument.conclusion_uid).all()
        set_new_rebut(1, db_argument, db_user, 2)
        after = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_argument.conclusion_uid).all()
        self.assertLess(len(before), len(after))

    def test_set_new_support(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_argument = DBDiscussionSession.query(Argument).get(1)

        before = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == 1,
                                                                 Argument.conclusion_uid == db_argument.conclusion_uid)).all()
        set_new_support(1, db_argument, db_user, 2)
        after = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == 1,
                                                                Argument.conclusion_uid == db_argument.conclusion_uid)).all()
        self.assertLess(len(before), len(after))
