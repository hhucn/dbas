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

        # correct argument id
        response_correct_id = opinion.get_user_and_opinions_for_argument(argument_uids=[1, 1])
        self.assertTrue(verify_structure_of_argument_dictionary(self, response_correct_id))
        response_correct_id_2 = opinion.get_user_and_opinions_for_argument(argument_uids=[10, 12])
        self.assertTrue(verify_structure_of_argument_dictionary(self, response_correct_id_2))

        # unknown argument id
        response_wrong_id = opinion.get_user_and_opinions_for_argument(argument_uids=[0, 0])
        self.assertTrue('Internal Error' in response_wrong_id['title'])

    def test_get_user_with_same_opinion_for_statements(self):
        opinion = self._makeOne(lang='en',
                                nickname='nickname',
                                mainpage='url')

        # correct statement id
        response_correct_id_supportive_true = opinion.get_user_with_same_opinion_for_statements(statement_uids=[1, 1],
                                                                                                is_supportive=True)
        self.assertTrue(verify_structure_of_statement_dictionary(self, response_correct_id_supportive_true))
        response_correct_id_supportive_false = opinion.get_user_with_same_opinion_for_statements(statement_uids=[2, 3],
                                                                                                 is_supportive=False)
        self.assertTrue(verify_structure_of_statement_dictionary(self, response_correct_id_supportive_false))


def verify_structure_of_argument_dictionary(self, response):
    # test structure of dictionary

    self.assertTrue('opinions' in response)
    self.assertTrue('title' in response)

    # test structure of ...
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

    return True

def verify_structure_of_statement_dictionary(self, response):
    self.assertTrue('opinions' in response)
    self.assertTrue('title' in response)

    # test structure of ...
    # ... value of key 'opinions'
    self.assertTrue('uid' in response['opinions'][0])
    self.assertTrue('text' in response['opinions'][0])
    self.assertTrue('message' in response['opinions'][0])
    self.assertTrue('users' in response['opinions'][0])
    self.assertTrue('seen_by' in response['opinions'][0])

    # ... value of key 'users' in 'opinions'
    self.assertTrue('nickname' in response['opinions'][0]['users'][0])

    return True
