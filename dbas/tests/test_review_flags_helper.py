import unittest
from dbas.views import transaction

import dbas.review.helper.flags as ReviewFlagHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config
from dbas.database.discussion_model import User, Argument, Statement

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TestReviewFlagHelper(unittest.TestCase):

    def setUp(self):
        self.some_nick = DBDiscussionSession.query(User).filter_by(nickname='some_nick').first()
        self.tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()

    def test_flag_argument(self):
        translator = Translator('en')

        success, info, error = ReviewFlagHelper.flag_argument(0, 'reason', self.some_nick, translator, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'reason', self.some_nick, translator, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'reason', self.tobias, translator, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(0, 'reason', self.tobias, translator, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.internalKeyError]])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'optimization', self.tobias, translator, Argument, transaction)
        self.__assert_equal_text([[success, translator.thxForFlagText], [info, ''], [error, '']])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'optimization', self.tobias, translator, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, translator.alreadyFlaggedByYou], [error, '']])

        success, info, error = ReviewFlagHelper.flag_argument(4, 'optimization', self.christian, translator, Argument, transaction)
        self.__assert_equal_text([[success, ''], [info, translator.alreadyFlaggedByOthers], [error, '']])

    def __assert_equal_text(self, values):
        for pair in values:
            self.assertEqual(pair[0], pair[1])
