import unittest

import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, PremiseGroup
from dbas.database.discussion_model import User, ReviewCanceled, ReviewEditValue, PremiseGroupSplitted, \
    PremiseGroupMerged
from dbas.review.mapper import get_queue_by_key, get_review_model_by_key, get_last_reviewer_by_key
from dbas.review.queue import review_queues, key_delete, key_merge, key_split, key_duplicate, key_edit, key_optimization
from dbas.review.queue.adapter import QueueAdapter
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class SubpageQueueTest(TestCaseWithConfig):
    def setUp(self):
        super(SubpageQueueTest, self).setUp()
        self.config = testing.setUp()
        self.db_user: User = self.user_bjoern
        self.issue: Issue = self.issue_cat_or_dog
        self.tn = Translator('en')

    def test_get_subpage_of_queue(self):
        self.db_user.participates_in.append(self.issue)
        for key in review_queues:
            queue = get_queue_by_key(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.db_user, application_url='main', translator=self.tn)
            subpage = adapter.get_subpage_of_queue({}, key)
            self.assertIn('elements', subpage)
            self.assertIn('no_arguments_to_review', subpage)
            self.assertIn('button_set', subpage)
            self.assertIn('session', subpage)
            self.assertTrue(key, subpage['elements']['page_name'])
            self.assertIn('reviewed_element', subpage['elements'])


class QueueTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).get(1)
        self.other_user = DBDiscussionSession.query(User).get(4)
        self.tn = Translator('en')

    def tearDown(self):
        testing.tearDown()

    def test_add_vote(self):
        # function is called in a more complex test/setting
        pass

    def test_add_review(self):
        # function is called in a more complex test/setting
        pass

    def test_get_review_count(self):
        for key in review_queues:
            queue = get_queue_by_key(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='main', translator=self.tn)
            review_table = get_review_model_by_key(key)
            db_review = DBDiscussionSession.query(review_table).filter_by(is_executed=False, is_revoked=False).first()
            okay, not_okay = adapter.get_review_count(db_review.uid)
            self.assertTrue(isinstance(okay, int))
            self.assertTrue(isinstance(not_okay, int))

    def test_cancel_ballot(self):
        for key in review_queues:
            self.__test_cancel_ballot(key)

    def __test_cancel_ballot(self, key):
        queue = get_queue_by_key(key)
        adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='main', translator=self.tn)
        review_table = get_review_model_by_key(key)
        last_reviewer_table = get_last_reviewer_by_key(key)

        # count of elements before we add new things to cancel
        review_count_1 = DBDiscussionSession.query(review_table).count()

        # add things which we can cancel
        if key in [key_merge, key_split]:
            test_user = DBDiscussionSession.query(User).get(4)
            test_premisegroup = DBDiscussionSession.query(PremiseGroup).get(5)
            db_new_review = review_table(detector=test_user, premisegroup=test_premisegroup)
        elif key is key_duplicate:
            original_statement = DBDiscussionSession.query(Statement).get(4)
            duplicate_statement = DBDiscussionSession.query(Statement).get(5)
            db_new_review = review_table(detector=self.other_user, duplicate_statement=duplicate_statement,
                                         original_statement=original_statement)
        elif key in [key_delete, key_edit, key_optimization]:
            db_new_review = review_table(detector=DBDiscussionSession.query(User).get(4))
        else:
            db_new_review = review_table(detector=4)

        DBDiscussionSession.add(db_new_review)
        DBDiscussionSession.flush()

        test_user = DBDiscussionSession.query(User).get(3)
        if key == key_split:
            DBDiscussionSession.add(
                last_reviewer_table(reviewer=test_user, review=db_new_review, should_split=True))
        elif key == key_merge:
            DBDiscussionSession.add(
                last_reviewer_table(reviewer=test_user, review=db_new_review, should_merge=True))
        else:
            DBDiscussionSession.add(last_reviewer_table(reviewer=test_user, review=db_new_review, is_okay=True))

        DBDiscussionSession.flush()

        # count of elements after we add new things to cancel
        review_count_2 = DBDiscussionSession.query(review_table).count()
        review_canceled_1 = DBDiscussionSession.query(ReviewCanceled).count()

        # cancel things
        adapter.cancel_ballot(db_new_review)

        # count of elements after we canceled
        review_count_3 = DBDiscussionSession.query(review_table).count()
        review_canceled_2 = DBDiscussionSession.query(ReviewCanceled).count()

        self.assertLess(review_count_1, review_count_2)
        self.assertEqual(review_count_3, review_count_2)
        self.assertTrue(db_new_review.is_revoked)

        self.assertLess(review_canceled_1, review_canceled_2)
        self.__delete_review_in_test_cancel_ballot(key, db_new_review, last_reviewer_table, review_table)

    def __delete_review_in_test_cancel_ballot(self, key, db_new_review, last_reviewer_table, review_table):
        if key == key_edit:
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_edit_uid=db_new_review.uid).delete()
        if key == key_delete:
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_delete_uid=db_new_review.uid).delete()
        if key == key_optimization:
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_optimization_uid=db_new_review.uid).delete()
        if key == key_duplicate:
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_duplicate_uid=db_new_review.uid).delete()
        if key == key_merge:
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_merge_uid=db_new_review.uid).delete()
        if key == key_split:
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_split_uid=db_new_review.uid).delete()
        if key is key_edit:
            DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_new_review.uid).delete()
        if key is key_split:
            DBDiscussionSession.query(PremiseGroupSplitted).filter_by(review_uid=db_new_review.uid).delete()
        if key is key_merge:
            DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=db_new_review.uid).delete()
        DBDiscussionSession.query(last_reviewer_table).filter_by(review_uid=db_new_review.uid).delete()
        DBDiscussionSession.query(review_table).filter_by(uid=db_new_review.uid).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_revoke_ballot(self):
        # function is called in a more complex test/setting
        pass

    def test_element_in_queue(self):
        # function is called in a more complex test/setting
        pass

    def test_get_history_table_row(self):
        for key in review_queues:
            queue = get_queue_by_key(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='main', translator=self.tn)
            review_table = get_review_model_by_key(key)
            db_review = DBDiscussionSession.query(review_table).filter_by(is_executed=False, is_revoked=False).first()
            row = adapter.get_history_table_row(db_review, {}, is_executed=False, short_text='short',
                                                full_text='.' * 40)
            if not row:
                continue

            if key == key_delete:
                self.assertIn('reason', row.keys())
                continue

            self.assertTrue(any(['_shorttext' in key for key in row.keys()]))
            self.assertTrue(any(['_fulltext' in key for key in row.keys()]))

    def test_get_text_of_element(self):
        for key in review_queues:
            queue = get_queue_by_key(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='main', translator=self.tn)
            review_table = get_review_model_by_key(key)
            db_review = DBDiscussionSession.query(review_table).filter_by(is_executed=False, is_revoked=False).first()
            text = adapter.get_text_of_element(db_review)
            self.assertTrue(isinstance(text, str))

    def test_get_all_votes_for(self):
        for key in review_queues:
            queue = get_queue_by_key(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='main', translator=self.tn)
            review_table = get_review_model_by_key(key)
            db_review = DBDiscussionSession.query(review_table).filter_by(is_executed=False, is_revoked=False).first()
            pro, con = adapter.get_all_votes_for(db_review)
            self.assertTrue(isinstance(pro, list))
            self.assertTrue(isinstance(con, list))
