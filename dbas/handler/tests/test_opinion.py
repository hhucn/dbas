import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.opinion import get_user_and_opinions_for_argument, get_user_with_same_opinion_for_statements, \
    get_user_with_same_opinion_for_premisegroups_of_args, get_user_with_same_opinion_for_argument, \
    get_user_with_opinions_for_attitude


class OpinionHandlerTests(unittest.TestCase):
    def test_get_user_and_opinions_for_argument(self):
        lang = 'en'
        main_page = 'url'
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        for uid in [11, 12, 13]:
            response = get_user_and_opinions_for_argument(argument_uid=uid,
                                                          db_user=db_user,
                                                          lang=lang,
                                                          main_page=main_page,
                                                          path='')
            verify_structure_of_statement_premisgroup_argument_dictionary(self, response)

    def test_get_user_with_same_opinion_for_statements(self):
        lang = 'en'
        main_page = 'url'
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        for uid in [1, 2, 3]:
            response = get_user_with_same_opinion_for_statements(statement_uids=[uid],
                                                                 is_supportive=True,
                                                                 db_user=db_user,
                                                                 lang=lang,
                                                                 main_page=main_page)
            verify_structure_of_statement_premisgroup_argument_dictionary(self, response)

    def test_get_user_with_same_opinion_for_premisegroups(self):
        lang = 'en'
        main_page = 'url'
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        for uid in [1, 2, 61, 62]:
            response = get_user_with_same_opinion_for_premisegroups_of_args(argument_uids=[uid],
                                                                            db_user=db_user,
                                                                            lang=lang,
                                                                            main_page=main_page)
            verify_structure_of_statement_premisgroup_argument_dictionary(self, response)

    def test_get_user_with_same_opinion_for_argument(self):
        lang = 'en'
        main_page = 'url'
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        # correct argument id
        response_correct_id = get_user_with_same_opinion_for_argument(argument_uid=1, db_user=db_user,
                                                                      lang=lang, main_page=main_page)
        verify_structure_of_user_dictionary_for_argument(self, response_correct_id)

        response_correct_id2 = get_user_with_same_opinion_for_argument(argument_uid=62, db_user=db_user,
                                                                       lang=lang, main_page=main_page)
        verify_structure_of_user_dictionary_for_argument(self, response_correct_id2)

        # wrong id
        response_wrong_id = get_user_with_same_opinion_for_argument(argument_uid=0, db_user=db_user,
                                                                    lang=lang, main_page=main_page)
        map(lambda x: self.assertEqual(x, None), response_wrong_id.items())

        response_wrong_id2 = get_user_with_same_opinion_for_argument(argument_uid=None, db_user=db_user,
                                                                     lang=lang, main_page=main_page)
        map(lambda x: self.assertEqual(x, None), response_wrong_id2.items())

    def test_get_user_with_opinions_for_attitude(self):
        lang = 'en'
        main_page = 'url'
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        # correct statement id
        response_correct_id = get_user_with_opinions_for_attitude(statement_uid=1, db_user=db_user,
                                                                  lang=lang, main_page=main_page)
        verify_structure_of_attitude_dictionary(self, response_correct_id)
        response_correct_id2 = get_user_with_opinions_for_attitude(statement_uid=74, db_user=db_user,
                                                                   lang=lang, main_page=main_page)
        verify_structure_of_attitude_dictionary(self, response_correct_id2)

        # wrong id
        response_wrong_id = get_user_with_opinions_for_attitude(statement_uid=0, db_user=db_user, lang=lang,
                                                                main_page=main_page)
        self.assertEqual(response_wrong_id['text'], None)
        response_wrong_id2 = get_user_with_opinions_for_attitude(statement_uid=None, db_user=db_user,
                                                                 lang=lang, main_page=main_page)
        self.assertEqual(response_wrong_id2['text'], None)


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
    self.assertTrue('text' in response['opinions'][0])
    self.assertTrue('message' in response['opinions'][0])
    self.assertTrue('users' in response['opinions'][0])
    self.assertTrue('seen_by' in response['opinions'][0])

    # ... value of key 'users' in 'opinions'
    if len(response['opinions'][0]['users']) > 0:
        self.assertTrue('nickname' in response['opinions'][0]['users'][0])

    # wrong structure
    self.assertTrue('' not in response)
    self.assertTrue('uid' not in response)
    self.assertTrue(None not in response)


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


def verify_structure_of_attitude_dictionary(self, response):
    # correct structure
    self.assertTrue('text' in response)
    self.assertTrue('agree' in response)
    self.assertTrue('disagree' in response)
    self.assertTrue('users' in response['agree'])
    self.assertTrue('text' in response['agree'])
    self.assertTrue('users' in response['disagree'])
    self.assertTrue('text' in response['disagree'])
    self.assertTrue('title' in response)
    self.assertTrue('seen_by' in response)

    # wrong structure
    self.assertTrue('' not in response)
    self.assertTrue('text ' not in response)
    self.assertTrue(None not in response)
