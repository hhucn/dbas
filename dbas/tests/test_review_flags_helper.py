import unittest

import dbas.review.helper.flags as rf_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewOptimization, ReviewDuplicate, RevokedDuplicate, \
    LastReviewerDuplicate, ReviewCanceled
from dbas.strings.keywords import Keywords as _
from dbas.views import transaction


class TestReviewFlagHelper(unittest.TestCase):

    def setUp(self):
        self.some_nick = 'some_nick'
        self.tobias = 'Tobias'
        self.christian = 'Christian'

    def test_flag_argument(self):
        success, info, error = rf_helper.flag_element(0, 'reason', self.some_nick, True)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

        success, info, error = rf_helper.flag_element(4, 'reason', self.some_nick, True)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.noRights]])

        success, info, error = rf_helper.flag_element(0, 'reason', self.tobias, True)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = rf_helper.flag_element(4, 'reason', self.tobias, True)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = rf_helper.flag_element(0, 'reason', self.tobias, True)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = rf_helper.flag_element(4, 'optimization', self.tobias, True)
        self.__assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

        success, info, error = rf_helper.flag_element(4, 'optimization', self.tobias, True)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = rf_helper.flag_element(4, 'optimization', self.christian, True)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])

        success, info, error = rf_helper.flag_element(5, 'duplicate', self.tobias, False, 1)
        self.__assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

        success, info, error = rf_helper.flag_element(5, 'duplicate', self.tobias, False, 1)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = rf_helper.flag_element(5, 'duplicate', self.christian, False, 1)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])

        tobias = DBDiscussionSession.query(User).filter_by(nickname=self.tobias).first()

        DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=tobias.uid, argument_uid=4).delete()
        DBDiscussionSession.flush()
        transaction.commit()

        tmp = DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=tobias.uid, duplicate_statement_uid=5).first()
        DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewCanceled).filter_by(review_duplicate_uid=tmp.uid).delete()

        DBDiscussionSession.query(ReviewDuplicate).filter_by(detector_uid=tobias.uid, duplicate_statement_uid=5).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def __assert_equal_text(self, values):
        for pair in values:
            self.assertEqual(pair[0], pair[1])
