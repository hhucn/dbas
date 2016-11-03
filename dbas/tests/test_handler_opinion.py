import unittest

from dbas.database import DBDiscussionSession
from dbas.handler.opinion import OpinionHandler
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

opinion = OpinionHandler(lang='en',
                         nickname='nickname',
                         mainpage='url')


class OpinionHandlerTests(unittest.TestCase):

    def test_init(self):
        self.assertEqual(opinion.lang, 'en')
        self.assertEqual(opinion.nickname, 'nickname')
        self.assertEqual(opinion.mainpage, 'url')

    def test_get_user_and_opinions_for_argument(self):
        # correct argument id
        response_correct_id = opinion.get_user_and_opinions_for_argument(argument_uids=[11, 12])
        self.assertTrue(verify_structure_of_argument_dictionary(self, response_correct_id))
        response_correct_id_2 = opinion.get_user_and_opinions_for_argument(argument_uids=[11, 13])
        self.assertTrue(verify_structure_of_argument_dictionary(self, response_correct_id_2))

        # unknown argument id
        response_wrong_id = opinion.get_user_and_opinions_for_argument(argument_uids=[0, 0])
        self.assertIn('Internal Error', response_wrong_id['title'])

        # none id
        response_single_id = opinion.get_user_and_opinions_for_argument(argument_uids=1)
        self.assertEqual(response_single_id, None)
        response_none_id = opinion.get_user_and_opinions_for_argument(argument_uids=None)
        self.assertEqual(response_none_id, None)

    def test_get_user_with_same_opinion_for_statements(self):
        # correct statement id
        response_correct_id_supportive_true = opinion.get_user_with_same_opinion_for_statements(statement_uids=[1, 1],
                                                                                                is_supportive=True)
        self.assertTrue(verify_structure_of_statement_premisgroup_argument_dictionary(self, response_correct_id_supportive_true))
        response_correct_id_supportive_false = opinion.get_user_with_same_opinion_for_statements(statement_uids=[2, 3],
                                                                                                 is_supportive=False)
        self.assertTrue(verify_structure_of_statement_premisgroup_argument_dictionary(self, response_correct_id_supportive_false))

    def test_get_user_with_same_opinion_for_premisegroups(self):
        # correct premisegroup id
        response_correct_id = opinion.get_user_with_same_opinion_for_premisegroups(argument_uids=[1, 2])
        self.assertTrue(verify_structure_of_statement_premisgroup_argument_dictionary(self, response_correct_id))
        response_correct_id2 = opinion.get_user_with_same_opinion_for_premisegroups(argument_uids=[61, 62])
        self.assertTrue(verify_structure_of_statement_premisgroup_argument_dictionary(self, response_correct_id2))

    def test_get_user_with_same_opinion_for_argument(self):
        # correct argument id
        response_correct_id = opinion.get_user_with_same_opinion_for_argument(argument_uid=1)
        self.assertTrue(verify_structure_of_user_dictionary_for_argument(self, response_correct_id))
        response_correct_id2 = opinion.get_user_with_same_opinion_for_argument(argument_uid=62)
        self.assertTrue(verify_structure_of_user_dictionary_for_argument(self, response_correct_id2))

        # wrong id
        response_wrong_id = opinion.get_user_with_same_opinion_for_argument(argument_uid=0)
        self.assertEqual(response_wrong_id, None)
        response_wrong_id2 = opinion.get_user_with_same_opinion_for_argument(argument_uid=None)
        self.assertEqual(response_wrong_id2, None)

    def test_get_user_with_opinions_for_attitude(self):
        # correct statement id
        response_correct_id = opinion.get_user_with_opinions_for_attitude(statement_uid=1)
        self.assertTrue(verify_structure_of_attitude_dictionary(self, response_correct_id))
        response_correct_id2 = opinion.get_user_with_opinions_for_attitude(statement_uid=74)
        self.assertTrue(verify_structure_of_attitude_dictionary(self, response_correct_id2))

        # wrong id
        response_wrong_id = opinion.get_user_with_opinions_for_attitude(statement_uid=0)
        self.assertEqual(response_wrong_id, None)
        response_wrong_id2 = opinion.get_user_with_opinions_for_attitude(statement_uid=None)
        self.assertEqual(response_wrong_id2, None)


def verify_structure_of_argument_dictionary(self, response):
    # test structure of dictionary

    self.assertTrue('opinions' in response)
    self.assertTrue('title' in response)

    # test structure of ...
    # ... value of key 'opinions'
    undermine = 0
    support = 1
    undercut = 2
    rebut = 3

    # ... value of key 'attack_type' in 'opinions'
    self.assertTrue('users' in response['opinions'][undermine])
    self.assertTrue('message' in response['opinions'][support])
    self.assertTrue('text' in response['opinions'][undercut])
    self.assertTrue('seen_by' in response['opinions'][rebut])

    # ... value of key 'users' in {'opinions': {'attack_type': {'users': ...}}}
    # self.assertTrue(len(response['opinions'][rebut]['users']) > 0)
    # self.assertTrue(len(response['opinions'][undercut]['users']) > 0)
    # self.assertTrue(len(response['opinions'][support]['users']) > 0)
    # self.assertTrue(len(response['opinions'][undermine]['users']) > 0)

    # self.assertTrue('nickname' in response['opinions'][rebut]['users'][0])
    # self.assertTrue('public_profile_url' in response['opinions'][undercut]['users'][0])
    # self.assertTrue('avatar_url' in response['opinions'][support]['users'][0])
    # self.assertTrue('vote_timestamp' in response['opinions'][undermine]['users'][0])

    # wrong structure
    self.assertTrue('' not in response)
    self.assertTrue('opinion' not in response)

    return True


def verify_structure_of_statement_premisgroup_argument_dictionary(self, response):
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

    # wrong structure
    self.assertTrue('' not in response)
    self.assertTrue('uid' not in response)
    self.assertTrue(None not in response)

    return True


def verify_structure_of_user_dictionary_for_argument(self, response):
    self.assertTrue('opinions' in response)
    self.assertTrue('title' in response)

    # test structure of ...
    # ... value of key 'opinions'
    self.assertTrue('uid' in response['opinions'])
    self.assertTrue('text' in response['opinions'])
    self.assertTrue('message' in response['opinions'])
    self.assertTrue('users' in response['opinions'])

    # wrong structure
    self.assertTrue('' not in response)
    self.assertTrue('uid' not in response)
    self.assertTrue(None not in response)

    return True


def verify_structure_of_attitude_dictionary(self, response):
    # correct structure
    self.assertTrue('text' in response)
    self.assertTrue('agree' in response)
    self.assertTrue('disagree' in response)
    self.assertTrue('agree_users' in response)
    self.assertTrue('agree_text' in response)
    self.assertTrue('disagree_users' in response)
    self.assertTrue('disagree_text' in response)
    self.assertTrue('title' in response)
    self.assertTrue('seen_by' in response)

    # wrong structure
    self.assertTrue('' not in response)
    self.assertTrue('text ' not in response)
    self.assertTrue(None not in response)

    return True
