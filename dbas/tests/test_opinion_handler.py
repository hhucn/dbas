import unittest

from sqlalchemy import engine_from_config

from dbas import DBDiscussionSession
from dbas.helper.tests_helper import add_settings_to_appconfig


settings = add_settings_to_appconfig()


class OpinionHandlerTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.opinion_handler import OpinionHandler
        return OpinionHandler

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_init(self):
        opinion = self._makeOne(lang='en',
                                nickname='nickname',
                                mainpage='url')

        self.assertEqual(opinion.lang, 'en')

        self.assertEqual(opinion.nickname, 'nickname')

        self.assertEqual(opinion.mainpage, 'url')