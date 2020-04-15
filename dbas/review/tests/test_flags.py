import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewOptimization, ReviewDuplicate, RevokedDuplicate, \
    LastReviewerDuplicate, ReviewCanceled, ReviewMergeValues, ReviewMerge, ReviewSplit, ReviewSplitValues, PremiseGroup
from dbas.review.flags import flag_element, flag_statement_for_merge_or_split, flag_pgroup_for_merge_or_split
from dbas.review.queue import key_merge, key_split, key_optimization, key_duplicate
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class TestFlagElement(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.tn = Translator('en')

    def tearDown(self):
        DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=self.user_tobi.uid,
                                                                argument_uid=4).delete()
        DBDiscussionSession.flush()
        transaction.commit()

        tmp = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=self.user_tobi.uid,
                                                                   duplicate_statement_uid=5)
        if tmp.first():
            DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=tmp.first().uid).delete()
            DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=tmp.first().uid).delete()
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_duplicate_uid=tmp.first().uid).delete()
            tmp.delete()

        DBDiscussionSession.flush()
        transaction.commit()
        super().tearDown()

    def test_flag_element_for_optimizations(self):
        return_dict = flag_element(self.seventh_argument, key_optimization, self.user_tobi, True, 'en')
        self.assertEqual(self.tn.get(_.thxForFlagText), return_dict['success'])
        self.assertEqual('', return_dict['info'])

        return_dict = flag_element(self.seventh_argument, key_optimization, self.user_tobi, True, 'en')
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByYou), return_dict['info'])

        return_dict = flag_element(self.seventh_argument, key_optimization, self.user_christian, True, 'en')
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByOthers), return_dict['info'])

    def test_flag_element_for_duplicates(self):
        return_dict = flag_element(self.statement_cat_or_dog, key_duplicate, self.user_tobi, False, 'en',
                                   self.first_position_cat_or_dog)
        self.assertEqual(self.tn.get(_.thxForFlagText), return_dict['success'])
        self.assertEqual('', return_dict['info'])

        return_dict = flag_element(self.statement_cat_or_dog, key_duplicate, self.user_tobi, False, 'en',
                                   self.first_position_cat_or_dog)
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByYou), return_dict['info'])

        return_dict = flag_element(self.statement_cat_or_dog, key_duplicate, self.user_christian, False, 'en',
                                   self.first_position_cat_or_dog)
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByOthers), return_dict['info'])


class TestFlagElementForSplit(TestCaseWithConfig):

    def setUp(self):
        super().setUp()
        self.tn = Translator('en')
        self.db_pg = DBDiscussionSession.query(PremiseGroup).get(11)

    def tearDown(self):
        delete_splits(self.db_pg.uid)
        delete_merges(self.db_pg.uid)
        super().tearDown()

    def flag_statement_for_split_no_rights(self):
        success, info, error = flag_statement_for_merge_or_split('some_key', self.db_pg, ['value1', 'value2'],
                                                                 self.user_anonymous, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

    def flag_statement_for_split_with_key_error(self):
        success, info, error = flag_statement_for_merge_or_split('some_key', self.db_pg, ['value1', 'value2'],
                                                                 self.user_tobi, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

    def flag_statement_for_split(self):
        success, info, error = flag_statement_for_merge_or_split(key_merge, self.db_pg, ['value1', 'value2'],
                                                                 self.user_tobi, self.tn)
        assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

    def flag_statement_for_split_double_flagged(self):
        success, info, error = flag_statement_for_merge_or_split(key_merge, self.db_pg, ['value1', 'value2'],
                                                                 self.user_tobi, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_statement_for_split_double_flagged_different_key(self):
        success, info, error = flag_statement_for_merge_or_split(key_split, self.db_pg, ['value1', 'value2'],
                                                                 self.user_tobi, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_statement_for_split_double_flagged_by_another_user(self):
        success, info, error = flag_statement_for_merge_or_split(key_merge, self.db_pg, ['value1', 'value2'],
                                                                 self.user_christian, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])


class TestFlagElementForMerge(TestCaseWithConfig):

    def setUp(self):
        super().setUp()
        self.tn = Translator('en')
        self.db_pg = DBDiscussionSession.query(PremiseGroup).get(11)

    def tearDown(self):
        delete_merges(self.db_pg.uid)
        delete_splits(self.db_pg.uid)
        super().tearDown()

    def flag_pgroup_for_merge_no_rights(self):
        success, info, error = flag_pgroup_for_merge_or_split('some_key', self.db_pg.uid, self.user_anonymous, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

    def flag_pgroup_for_merge_with_key_error(self):
        success, info, error = flag_pgroup_for_merge_or_split('some_key', self.db_pg.uid, self.user_tobi, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

    def flag_pgroup_for_merge(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_merge, self.db_pg.uid, self.user_tobi, self.tn)
        assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

    def flag_pgroup_for_merge_double_flagged(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_merge, self.db_pg.uid, self.user_tobi, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_pgroup_for_merge_double_flagged_different_key(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_split, self.db_pg.uid, self.user_tobi, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_pgroup_for_merge_double_flagged_by_another_user(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_merge, self.db_pg.uid, self.user_christian, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])


def delete_merges(uid):
    tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisegroup_uid=uid).first()
    if tmp:
        DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=uid).delete()
        DBDiscussionSession.query(ReviewMerge).filter_by(premisegroup_uid=uid).delete()
    DBDiscussionSession.flush()
    transaction.commit()


def delete_splits(uid):
    tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisegroup_uid=uid).first()
    if tmp:
        DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=uid).delete()
        DBDiscussionSession.query(ReviewSplit).filter_by(premisegroup_uid=uid).delete()
    DBDiscussionSession.flush()
    transaction.commit()


def assert_equal_text(values):
    for v1, v2 in values:
        assert v1 == v2
