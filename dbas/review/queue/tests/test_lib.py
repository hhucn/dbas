from dbas.database.discussion_model import ReviewDuplicate, LastReviewerDuplicate
from dbas.review.queue.lib import get_review_count_for
from dbas.review.reputation import get_reason_by_action, ReputationReasons
from dbas.tests.utils import TestCaseWithConfig


class LibTest(TestCaseWithConfig):
    def test_get_reputation_reason_by_action(self):
        for action in ReputationReasons.list():
            db_reason = get_reason_by_action(action)
            self.assertIsNotNone(db_reason)
            self.assertTrue(db_reason.points != 0)

    def test_get_review_count_for_if_not_participating(self):
        self.assertEqual(get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, self.user_bjoern), 0)
        self.assertEqual(get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, self.user_antonia), 0)

    def test_get_review_count_for_if_participating(self):
        self.user_bjoern.participates_in.append(self.issue_cat_or_dog)
        self.user_antonia.participates_in.append(self.issue_cat_or_dog)

        self.assertEqual(get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, self.user_bjoern), 2)
        self.assertEqual(get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, self.user_antonia), 1)

        self.user_bjoern.participates_in.remove(self.issue_cat_or_dog)
        self.user_antonia.participates_in.remove(self.issue_cat_or_dog)
