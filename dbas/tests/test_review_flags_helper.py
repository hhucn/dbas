import unittest
from dbas.views import transaction

import dbas.review.helper.flags as ReviewFlagHelper
from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TestReviewFlagHelper(unittest.TestCase):

    def test_flag_argument(self):
        translator = Translator('en')
        
        bad_arg_id = 0
        rel_arg_id = 1
        bad_reason = 'reason'
        real_reason = 'optimization'
        bad_nick = 'some_nick'
        real_nick1 = 'Tobias'
        real_nick2 = 'Christian'

        success, info, error = ReviewFlagHelper.flag_argument(bad_arg_id, bad_reason, bad_nick, translator, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.get(translator.internalKeyError)]])

        success, info, error = ReviewFlagHelper.flag_argument(rel_arg_id, bad_reason, bad_nick, translator, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.get(translator.internalKeyError)]])

        success, info, error = ReviewFlagHelper.flag_argument(rel_arg_id, bad_reason, real_nick1, translator, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.get(translator.internalKeyError)]])

        success, info, error = ReviewFlagHelper.flag_argument(bad_arg_id, bad_reason, real_nick1, translator, transaction)
        self.__assert_equal_text([[success, ''], [info, ''], [error, translator.get(translator.internalKeyError)]])

        success, info, error = ReviewFlagHelper.flag_argument(rel_arg_id, real_reason, real_nick1, translator, transaction)
        self.__assert_equal_text([[success, translator.get(translator.thxForFlagText)], [info, ''], [error, '']])

        success, info, error = ReviewFlagHelper.flag_argument(rel_arg_id, real_reason, real_nick1, translator, transaction)
        self.__assert_equal_text([[success, ''], [info, translator.get(translator.alreadyFlaggedByYou)], [error, '']])

        success, info, error = ReviewFlagHelper.flag_argument(rel_arg_id, real_reason, real_nick2, translator, transaction)
        self.__assert_equal_text([[success, ''], [info, translator.get(translator.alreadyFlaggedByOthers)], [error, '']])

    def __assert_equal_text(self, values):
        for pair in values:
            self.assertEqual(pair[0], pair[1])
