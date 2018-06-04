import unittest

import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewOptimization, ReviewDuplicate, RevokedDuplicate, \
    LastReviewerDuplicate, ReviewCanceled, ReviewMergeValues, ReviewMerge, ReviewSplit, ReviewSplitValues, PremiseGroup
from dbas.lib import nick_of_anonymous_user
from dbas.review.flags import flag_element, flag_statement_for_merge_or_split, flag_pgroup_for_merge_or_split
from dbas.review.queue import key_merge, key_split, key_optimization, key_duplicate
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class TestFlagElement(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.some_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
        self.user_tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.user_christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()
        self.tn = Translator('en')

    def tearDown(self):
        testing.tearDown()
        DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=self.user_tobias.uid,
                                                                argument_uid=4).delete()
        DBDiscussionSession.flush()
        transaction.commit()

        tmp = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=self.user_tobias.uid,
                                                                   duplicate_statement_uid=5)
        if tmp.first():
            DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=tmp.first().uid).delete()
            DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=tmp.first().uid).delete()
            DBDiscussionSession.query(ReviewCanceled).filter_by(review_duplicate_uid=tmp.first().uid).delete()
            tmp.delete()

        DBDiscussionSession.flush()
        transaction.commit()

    def test_flag_element_for_opti(self):
        return_dict = flag_element(4, key_optimization, self.user_tobias, True, 'en')
        self.assertEqual(self.tn.get(_.thxForFlagText), return_dict['success'])
        self.assertEqual('', return_dict['info'])

    def test_double_flag_element_by_me_for_opti(self):
        return_dict = flag_element(4, key_optimization, self.user_tobias, True, 'en')
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByYou), return_dict['info'])

    def test_double_flag_element_by_other_for_opti(self):
        return_dict = flag_element(4, key_optimization, self.user_christian, True, 'en')
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByOthers), return_dict['info'])

    def test_flag_element_for_dupli(self):
        return_dict = flag_element(5, key_duplicate, self.user_tobias, False, 'en', 1)
        self.assertEqual(self.tn.get(_.thxForFlagText), return_dict['success'])
        self.assertEqual('', return_dict['info'])

    def test_double_flag_element_by_me_for_dupli(self):
        return_dict = flag_element(5, key_duplicate, self.user_tobias, False, 'en', 1)
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByYou), return_dict['info'])

    def test_double_flag_element_by_other_for_dupli(self):
        return_dict = flag_element(5, key_duplicate, self.user_christian, False, 'en', 1)
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByOthers), return_dict['info'])


class TestFlagElementForSplit(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.some_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
        self.user_tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.user_christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()
        self.tn = Translator('en')
        self.db_pg = DBDiscussionSession.query(PremiseGroup).get(11)

    def tearDown(self):
        testing.tearDown()
        delete_splits(self.db_pg.uid)
        delete_merges(self.db_pg.uid)

    def flag_statement_for_split_no_rights(self):
        success, info, error = flag_statement_for_merge_or_split('some_key', self.db_pg, ['value1', 'value2'],
                                                                 self.some_user, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

    def flag_statement_for_split_with_key_error(self):
        success, info, error = flag_statement_for_merge_or_split('some_key', self.db_pg, ['value1', 'value2'],
                                                                 self.user_tobias, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

    def flag_statement_for_split(self):
        success, info, error = flag_statement_for_merge_or_split(key_merge, self.db_pg, ['value1', 'value2'], self.user_tobias, self.tn)
        assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

    def flag_statement_for_split_double_flagged(self):
        success, info, error = flag_statement_for_merge_or_split(key_merge, self.db_pg, ['value1', 'value2'], self.user_tobias, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_statement_for_split_double_flagged_different_key(self):
        success, info, error = flag_statement_for_merge_or_split(key_split, self.db_pg, ['value1', 'value2'], self.user_tobias, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_statement_for_split_double_flagged_by_another_user(self):
        success, info, error = flag_statement_for_merge_or_split(key_merge, self.db_pg, ['value1', 'value2'], self.user_christian, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])


class TestFlagElementForMerge(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.some_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
        self.user_tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.user_christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()
        self.tn = Translator('en')
        self.db_pg = DBDiscussionSession.query(PremiseGroup).get(11)

    def tearDown(self):
        testing.tearDown()
        delete_merges(self.db_pg.uid)
        delete_splits(self.db_pg.uid)

    def flag_pgroup_for_merge_no_rights(self):
        success, info, error = flag_pgroup_for_merge_or_split('some_key', self.db_pg.uid, self.some_user, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

    def flag_pgroup_for_merge_with_key_error(self):
        success, info, error = flag_pgroup_for_merge_or_split('some_key', self.db_pg.uid, self.user_tobias, self.tn)
        assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

    def flag_pgroup_for_merge(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_merge, self.db_pg.uid, self.user_tobias, self.tn)
        assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

    def flag_pgroup_for_merge_double_flagged(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_merge, self.db_pg.uid, self.user_tobias, self.tn)
        assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

    def flag_pgroup_for_merge_double_flagged_different_key(self):
        success, info, error = flag_pgroup_for_merge_or_split(key_split, self.db_pg.uid, self.user_tobias, self.tn)
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
