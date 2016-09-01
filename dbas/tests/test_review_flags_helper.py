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
        arg_id = 1

        success, info, error = ReviewFlagHelper.flag_argument(0, 'reason', 'nickname', translator, transaction)
        self.assertEqual(success, '')
        self.assertEqual(info, '')
        self.assertEqual(error, translator.get(translator.internalKeyError))

        success, info, error = ReviewFlagHelper.flag_argument(arg_id, 'reason', 'nickname', translator, transaction)
        self.assertEqual(success, '')
        self.assertEqual(info, '')
        self.assertEqual(error, translator.get(translator.internalKeyError))

        success, info, error = ReviewFlagHelper.flag_argument(arg_id, 'reason', 'Tobias', translator, transaction)
        self.assertEqual(success, '')
        self.assertEqual(info, '')
        self.assertEqual(error, translator.get(translator.internalKeyError))

        success, info, error = ReviewFlagHelper.flag_argument(0, 'reason', 'Tobias', translator, transaction)
        self.assertEqual(success, '')
        self.assertEqual(info, '')
        self.assertEqual(error, translator.get(translator.internalKeyError))

        success, info, error = ReviewFlagHelper.flag_argument(arg_id, 'optimization', 'Tobias', translator, transaction)
        self.assertEqual(success, translator.get(translator.thxForFlagText))
        self.assertEqual(info, '')
        self.assertEqual(error, '')

        success, info, error = ReviewFlagHelper.flag_argument(arg_id, 'optimization', 'Tobias', translator, transaction)
        self.assertEqual(success, '')
        self.assertEqual(info, translator.get(translator.alreadyFlaggedByYou))
        self.assertEqual(error, '')

        success, info, error = ReviewFlagHelper.flag_argument(arg_id, 'optimization', 'Martin', translator, transaction)
        self.assertEqual(success, '')
        self.assertEqual(info, translator.get(translator.alreadyFlaggedByOthers))
        self.assertEqual(error, '')
