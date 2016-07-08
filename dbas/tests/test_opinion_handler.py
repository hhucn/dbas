import unittest

from sqlalchemy import engine_from_config

from dbas import DBDiscussionSession
from dbas.helper.tests_helper import add_settings_to_appconfig


settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

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

    def test_get_user_and_opinions_for_argument(self):
        opinion = self._makeOne(lang='en',
                                nickname='nickname',
                                mainpage='url')

        response = opinion.get_user_and_opinions_for_argument(argument_uids=[1, 1])
        # test structure of dictionary

        # test structure of ...
        self.assertTrue('opinions' in response)
        self.assertTrue('title' in response)

        # ... value of key 'opinions'
        self.assertTrue('undermine' in response['opinions'])
        self.assertTrue('support' in response['opinions'])
        self.assertTrue('undercut' in response['opinions'])
        self.assertTrue('rebut' in response['opinions'])

        # ... value of key 'attack_type' in 'opinions'
        self.assertTrue('users' in response['opinions']['undermine'])
        self.assertTrue('message' in response['opinions']['support'])
        self.assertTrue('text' in response['opinions']['undercut'])
        self.assertTrue('seen_by' in response['opinions']['rebut'])

        # ... value of key 'users' in {'opinions': {'attack_type': {'users': ...}}}
        self.assertTrue('nickname' in response['opinions']['rebut']['users'][0])
        self.assertTrue('public_profile_url' in response['opinions']['undercut']['users'][0])
        self.assertTrue('avatar_url' in response['opinions']['support']['users'][0])
        self.assertTrue('vote_timestamp' in response['opinions']['undermine']['users'][0])

        # wrong structure
        self.assertTrue('' not in response)
        self.assertTrue('opinion' not in response)