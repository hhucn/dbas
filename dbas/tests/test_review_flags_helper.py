import unittest
from dbas.views import transaction

import dbas.review.helper.flags as ReviewFlagHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.keywords import Keywords as _
from sqlalchemy import engine_from_config
from dbas.database.discussion_model import User, Argument, Statement

settings = add_settings_to_appconfig()

DBDiscussionSession.remove()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TestReviewFlagHelper(unittest.TestCase):

    def setUp(self):
        self.some_nick = DBDiscussionSession.query(User).filter_by(nickname='some_nick').first()
        self.tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()

    def test_flag_argument(self):
        success, info, error = ReviewFlagHelper.flag_argument(0, 'reason', self.some_nick, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'reason', self.some_nick, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'reason', self.tobias, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(0, 'reason', self.tobias, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, _.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'optimization', self.tobias, Argument, transaction)
        self.__assert_equal_text([[success, _.thxForFlagText], [info, ''], [error, '']])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'optimization', self.tobias, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByYou], [error, '']])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'optimization', self.christian, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, _.alreadyFlaggedByOthers], [error, '']])

    def __assert_equal_text(self, values):
        for pair in values:
            self.assertEqual(pair[0], pair[1])
