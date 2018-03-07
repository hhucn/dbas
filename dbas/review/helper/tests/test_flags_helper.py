import unittest
import transaction

import dbas.review.helper.flags as rf_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewOptimization, ReviewDuplicate, RevokedDuplicate, \
    LastReviewerDuplicate, ReviewCanceled, ReviewMergeValues, ReviewMerge, ReviewSplit, ReviewSplitValues
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class TestReviewFlagHelper(unittest.TestCase):

    def setUp(self):
        self.some_nick = 'some_nick'
        self.tobias = 'Tobias'
        self.christian = 'Christian'
        self.user_some_nick = DBDiscussionSession.query(User).filter_by(nickname='some_nick').first()
        self.user_tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.user_christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()
        self.tn = Translator('en')

    def test_flag_argument(self):
        return_dict = rf_helper.flag_element(4, 'optimization', self.user_tobias, True, 'en')
        self.assertEqual(self.tn.get(_.thxForFlagText), return_dict['success'])
        self.assertEqual('', return_dict['info'])

        return_dict = rf_helper.flag_element(4, 'optimization', self.user_tobias, True, 'en')
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByYou), return_dict['info'])

        return_dict = rf_helper.flag_element(4, 'optimization', self.user_christian, True, 'en')
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByOthers), return_dict['info'])

        return_dict = rf_helper.flag_element(5, 'duplicate', self.user_tobias, False, 'en', 1)
        self.assertEqual(self.tn.get(_.thxForFlagText), return_dict['success'])
        self.assertEqual('', return_dict['info'])

        return_dict = rf_helper.flag_element(5, 'duplicate', self.user_tobias, False, 'en', 1)
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByYou), return_dict['info'])

        return_dict = rf_helper.flag_element(5, 'duplicate', self.user_christian, False, 'en', 1)
        self.assertEqual('', return_dict['success'])
        self.assertEqual(self.tn.get(_.alreadyFlaggedByOthers), return_dict['info'])

        DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=self.user_tobias.uid, argument_uid=4).delete()
        DBDiscussionSession.flush()
        transaction.commit()

        tmp = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=self.user_tobias.uid, duplicate_statement_uid=5).first()
        DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewCanceled).filter_by(review_duplicate_uid=tmp.uid).delete()

        DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=self.user_tobias.uid, duplicate_statement_uid=5).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def flag_statement_for_merge_or_split(self):
        keys = ['some_key', 'merge', 'split']

        success, info, error = rf_helper.flag_statement_for_merge_or_split(keys[0], 11, ['value1', 'value2'], self.some_nick)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

        success, info, error = rf_helper.flag_statement_for_merge_or_split(keys[0], 11, ['value1', 'value2'], self.tobias)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = rf_helper.flag_statement_for_merge_or_split(keys[1], 11, ['value1', 'value2'], self.tobias)
        self.__assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

        success, info, error = rf_helper.flag_statement_for_merge_or_split(keys[1], 11, ['value1', 'value2'], self.tobias)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = rf_helper.flag_statement_for_merge_or_split(keys[2], 11, ['value1', 'value2'], self.tobias)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = rf_helper.flag_statement_for_merge_or_split(keys[1], 11, ['value1', 'value2'], self.christian)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])

        tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=11).first()
        if tmp:
            DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=11).delete()

        tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=11).first()
        if tmp:
            DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=11).delete()

        DBDiscussionSession.flush()
        transaction.commit()

    def flag_pgroup_for_merge_or_split(self):
        keys = ['some_key', 'merge', 'split']

        success, info, error = rf_helper.flag_pgroup_for_merge_or_split(keys[0], 11, self.some_nick)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

        success, info, error = rf_helper.flag_pgroup_for_merge_or_split(keys[0], 11, self.tobias)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = rf_helper.flag_pgroup_for_merge_or_split(keys[1], 11, self.tobias)
        self.__assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

        success, info, error = rf_helper.flag_pgroup_for_merge_or_split(keys[1], 11, self.tobias)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = rf_helper.flag_pgroup_for_merge_or_split(keys[2], 11, self.tobias)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = rf_helper.flag_pgroup_for_merge_or_split(keys[1], 11, self.christian)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])

        tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=11).first()
        if tmp:
            DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=11).delete()

        tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=11).first()
        if tmp:
            DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=11).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def __assert_equal_text(self, values):
        for v1, v2 in values:
            self.assertEqual(v1, v2)
