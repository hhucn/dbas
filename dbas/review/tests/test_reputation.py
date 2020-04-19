import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory
from dbas.review.reputation import get_reputation_reasons_list, get_privilege_list, get_reputation_of, \
    ReputationReasons, get_reason_by_action, add_reputation_for, has_access_to_review_system, get_history_of, \
    add_reputation_and_check_review_access, add_reputation_and_send_popup
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class TestReviewReputationHelper(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.user_torben = DBDiscussionSession.query(User).get(9)

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
        count, has_all_rights = get_reputation_of(self.user_tobi)
        self.assertTrue(count > 20)
        self.assertTrue(has_all_rights)

    def test_add_reputation_for(self):
        DBDiscussionSession.query(ReputationHistory).filter_by(user=self.user_torben).delete()

        for reason in ReputationReasons:
            db_reason = get_reason_by_action(reason)
            self.assertTrue(add_reputation_for(self.user_torben, db_reason))

        db_reason = get_reason_by_action(ReputationReasons.first_argument_click)
        self.assertFalse(add_reputation_for(self.user_torben, db_reason))

        DBDiscussionSession.query(ReputationHistory).filter_by(user=self.user_torben).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_add_reputation_for_anonymous(self):
        db_reason = get_reason_by_action(ReputationReasons.first_argument_click)
        self.assertFalse(add_reputation_for(self.user_anonymous, db_reason))

    def test_get_reason_by_action(self):
        for reason in ReputationReasons:
            self.assertIsNotNone(get_reason_by_action(reason))

    def test_has_access_to_review_system(self):
        self.assertFalse(has_access_to_review_system(self.user_torben))
        self.assertTrue(has_access_to_review_system(self.user_christian))

    def test_add_reputation_and_send_popup(self):
        db_reason = get_reason_by_action(ReputationReasons.success_flag)
        self.assertFalse(add_reputation_and_send_popup(self.user_torben, db_reason, 'asd', Translator('en')))

        DBDiscussionSession.query(ReputationHistory).filter_by(user=self.user_torben).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_get_history_of(self):
        response = get_history_of(self.user_christian, Translator('en'))
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
        self.assertFalse(has_access_to_review_system(self.user_tobi))

        # add points
        broke_limit = add_reputation_and_check_review_access(self.user_tobi, ReputationReasons.success_flag)
        self.assertTrue(broke_limit)

        # now we have access
        self.assertTrue(has_access_to_review_system(self.user_tobi))
        db_last = DBDiscussionSession.query(ReputationHistory).filter_by(user=self.user_tobi).order_by(
            ReputationHistory.uid.asc()).first()
        DBDiscussionSession.query(ReputationHistory).filter_by(uid=db_last.uid).delete()

        # we lost access
        self.assertFalse(has_access_to_review_system(self.user_tobi))
        DBDiscussionSession.flush()
        transaction.commit()
