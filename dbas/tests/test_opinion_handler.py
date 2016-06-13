import unittest

import os

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config

from dbas import DBDiscussionSession

dir_name = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
settings = appconfig('config:' + os.path.join(dir_name, 'development.ini'))


class OpinionHandlerTests(unittest.TestCase):

    @staticmethod
    def _getTargetClass():
        from dbas.opinion_handler import OpinionHandler
        return OpinionHandler

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_init(self):
        opinion = self._makeOne(lang='1',
                                nickname='nickname',
                                mainpage='url')

        self.assertEqual(opinion.lang, '1')

        self.assertEqual(opinion.nickname, 'nickname')

        self.assertEqual(opinion.mainpage, 'url')

    def test_get_user_and_opinions_for_argument(self):
        opinion = self._makeOne(lang='1',
                                nickname='nickname',
                                mainpage='url')

        DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

