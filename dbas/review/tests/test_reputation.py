import unittest

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory
from dbas.lib import nick_of_anonymous_user
from dbas.review.reputation import get_reputation_reasons_list, get_privilege_list, get_reputation_of, \
    ReputationReasons, get_reason_by_action, add_reputation_for, has_access_to_review_system, get_history_of, \
    add_reputation_and_check_review_access
from dbas.strings.translator import Translator


class TestReviewReputationHelper(unittest.TestCase):

    def test_get_privilege_list(self):
        some_list = get_privilege_list(Translator('en'))
        for element in some_list:
            self.assertTrue('points' in element)
            self.assertTrue('icon' in element)
            self.assertTrue('text' in element)

    def test_get_reputation_list(self):
        some_list = get_reputation_reasons_list(Translator('en'))
        self.assertTrue('gains' in some_list)
        self.assertTrue('looses' in some_list)

    def test_get_reputation_of(self):
        db_user = DBDiscussionSession.query(User).get(2)
        count, has_all_rights = get_reputation_of(db_user)
        self.assertTrue(count > 20)
        self.assertTrue(has_all_rights)

    def test_add_reputation_for(self):
        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=9).delete()

        db_user = DBDiscussionSession.query(User).get(9)
        for reason in ReputationReasons:
            db_reason = get_reason_by_action(reason)
            self.assertTrue(add_reputation_for(db_user, db_reason))

        db_reason = get_reason_by_action(ReputationReasons.first_argument_click)
        self.assertFalse(add_reputation_for(db_user, db_reason))

        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=9).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_add_reputation_for_anonymous(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
        db_reason = get_reason_by_action(ReputationReasons.first_argument_click)
        self.assertFalse(add_reputation_for(db_user, db_reason))

    def test_get_reason_by_action(self):
        for reason in ReputationReasons:
            self.assertIsNotNone(get_reason_by_action(reason))

    def test_has_access_to_review_system(self):
        db_user = DBDiscussionSession.query(User).get(9)
        self.assertFalse(has_access_to_review_system(db_user))

        db_user = DBDiscussionSession.query(User).get(3)
        self.assertTrue(has_access_to_review_system(db_user))

    def test_get_history_of(self):
        db_user = DBDiscussionSession.query(User).get(3)
        response = get_history_of(db_user, Translator('en'))
        self.assertIn('count', response)
        self.assertIn('all_rights', response)
        self.assertIn('history', response)
        for element in response['history']:
            self.assertIn('date', element)
            self.assertIn('points_data', element)
            self.assertIn('action', element)
            self.assertIn('points', element)

    def test_add_reputation_and_check_review_access(self):
        # user has no access
        db_user = DBDiscussionSession.query(User).get(2)
        self.assertFalse(has_access_to_review_system(db_user))

        # add points
        db_reason = get_reason_by_action(ReputationReasons.success_flag)
        add_reputation_and_check_review_access(db_user, db_reason, 'page', Translator('en'))

        # now we have access
        self.assertTrue(has_access_to_review_system(db_user))
        db_last = DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=2).order_by(
            ReputationHistory.uid.asc()).first()
        DBDiscussionSession.query(ReputationHistory).filter_by(uid=db_last.uid).delete()

        # we lost access
        self.assertFalse(has_access_to_review_system(db_user))
        DBDiscussionSession.flush()
        transaction.commit()
