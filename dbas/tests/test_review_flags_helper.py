import unittest

import dbas.review.helper.flags as rf_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewOptimization
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.keywords import Keywords as _
from dbas.views import transaction
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.remove()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TestReviewFlagHelper(unittest.TestCase):

    def setUp(self):
        self.some_nick = DBDiscussionSession.query(User).filter_by(nickname='some_nick').first()
        self.tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()

    def test_flag_argument(self):
        success, info, error = rf_helper.flag_element(0, 'reason', self.some_nick, True)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = rf_helper.flag_element(4, 'reason', self.some_nick, True)
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

        DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=self.tobias.uid, argument_uid=4).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def __assert_equal_text(self, values):
        for pair in values:
            self.assertEqual(pair[0], pair[1])
