import unittest

import transaction
from pyramid import testing, httpexceptions

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, ClickedStatement, SeenArgument, ClickedArgument, \
    ReputationHistory, User
from dbas.helper.test import verify_dictionary_of_view, clear_seen_by_of, clear_clicks_of, refresh_user
from dbas.views import discussion_justify


class DiscussionJustifyViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def tearDown(self):
        testing.tearDown()

    @staticmethod
    def __get_meta_clicks():
        d = {
            'seen_s': DBDiscussionSession.query(SeenStatement).count(),
            'click_s': DBDiscussionSession.query(ClickedStatement).count(),
            'seen_a': DBDiscussionSession.query(SeenArgument).count(),
            'click_a': DBDiscussionSession.query(ClickedArgument).count()
        }
        return d

    @staticmethod
    def __delete_reputation_for_user(db_user):
        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).delete()
        transaction.commit()

    def __check_meta_clicks(self, vote_dict):
        self.assertEqual(vote_dict['seen_s'], DBDiscussionSession.query(SeenStatement).count())
        self.assertEqual(vote_dict['click_s'], DBDiscussionSession.query(ClickedStatement).count())
        self.assertEqual(vote_dict['seen_a'], DBDiscussionSession.query(SeenArgument).count())
        self.assertEqual(vote_dict['click_a'], DBDiscussionSession.query(ClickedArgument).count())

    def test_justify_statement_page(self):
        vote_dict = self.__get_meta_clicks()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'agree',
            'relation': '',
        }
        response = discussion_justify(request)
        self.assertNotIsInstance(response, httpexceptions.HTTPError)
        verify_dictionary_of_view(response)
        self.__check_meta_clicks(vote_dict)
        self.__check_meta_clicks(vote_dict)

    def test_support_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_vote1 = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.is_valid == True,
                                                                          ClickedStatement.is_up_vote == True).count()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'agree',
            'relation': '',
        }
        response = discussion_justify(request)
        transaction.commit()
        verify_dictionary_of_view(response)
        len_db_seen2 = DBDiscussionSession.query(SeenStatement).count()
        len_db_vote2 = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.is_valid == True,
                                                                          ClickedStatement.is_up_vote == True).count()

        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')

    def test_attack_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_vote1 = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.is_valid == True,
                                                                          ClickedStatement.is_up_vote == False).count()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'disagree',
            'relation': ''
        }
        response = discussion_justify(request)
        self.assertNotIsInstance(response, httpexceptions.HTTPError)
        transaction.commit()
        verify_dictionary_of_view(response)
        len_db_seen2 = DBDiscussionSession.query(SeenStatement).count()
        len_db_vote2 = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.is_valid == True,
                                                                          ClickedStatement.is_up_vote == False).count()

        # minus 1 for 'none of the above'
        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')

    def test_dont_know_statement_page(self):
        vote_dict = self.__get_meta_clicks()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'dontknow',
            'relation': '',
        }
        response = discussion_justify(request)
        self.assertNotIsInstance(response, httpexceptions.HTTPError)
        verify_dictionary_of_view(response)
        self.__check_meta_clicks(vote_dict)

    def test_justify_argument_page_no_rep(self):
        vote_dict = self.__get_meta_clicks()
        len_db_reputation1 = DBDiscussionSession.query(ReputationHistory).count()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'agree',
            'relation': ['undermine'],
        }
        response = discussion_justify(request)
        self.assertNotIsInstance(response, httpexceptions.HTTPError)
        verify_dictionary_of_view(response)

        len_db_reputation2 = DBDiscussionSession.query(ReputationHistory).count()
        self.__check_meta_clicks(vote_dict)
        self.assertEqual(len_db_reputation1, len_db_reputation2)

    def __test_base_for_justify_argument_page_rep(self):
        vote_dict = self.__get_meta_clicks()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'agree',
            'relation': ['undermine'],
        }
        response = discussion_justify(request)
        self.assertNotIsInstance(response, httpexceptions.HTTPError)
        verify_dictionary_of_view(response)
        self.assertNotEqual(vote_dict['seen_s'], DBDiscussionSession.query(SeenStatement).count())
        self.assertEqual(vote_dict['click_s'], DBDiscussionSession.query(ClickedStatement).count())
        self.assertNotEqual(vote_dict['seen_a'], DBDiscussionSession.query(SeenArgument).count())
        self.assertEqual(vote_dict['click_a'], DBDiscussionSession.query(ClickedArgument).count())
        return vote_dict

    def test_justify_argument_page_rep(self):
        db_user: User = refresh_user('Björn')
        self.config.testing_securitypolicy(userid=db_user.nickname, permissive=True)

        self.__delete_reputation_for_user(db_user)
        rep_history_before_new_rep = DBDiscussionSession.query(ReputationHistory).count()

        self.__test_base_for_justify_argument_page_rep()
        rep_history_after_new_rep = DBDiscussionSession.query(ReputationHistory).count()

        self.assertGreater(rep_history_after_new_rep, rep_history_before_new_rep,
                           'Reputation should be granted on first confrontation')

        self.__delete_reputation_for_user(db_user)
        clear_seen_by_of(db_user.nickname)
        clear_clicks_of(db_user.nickname)

    def test_justify_argument_page_rep_not_twice(self):
        db_user: User = refresh_user('Björn')
        self.config.testing_securitypolicy(userid=db_user.nickname, permissive=True)

        self.__delete_reputation_for_user(db_user)
        rep_history_before_new_rep = DBDiscussionSession.query(ReputationHistory).count()

        self.__test_base_for_justify_argument_page_rep()
        rep_history_after_new_rep = DBDiscussionSession.query(ReputationHistory).count()
        self.assertGreater(rep_history_after_new_rep, rep_history_before_new_rep,
                           'Reputation should be granted on first confrontation')
        clear_seen_by_of(db_user.nickname)
        clear_clicks_of(db_user.nickname)

        self.__test_base_for_justify_argument_page_rep()
        rep_history_after_second_try = DBDiscussionSession.query(ReputationHistory).count()
        self.assertEqual(rep_history_after_new_rep, rep_history_after_second_try,
                         'Reputation should NOT be granted twice for the first confrontation')

        self.__delete_reputation_for_user(db_user)
        clear_seen_by_of(db_user.nickname)
        clear_clicks_of(db_user.nickname)

    def test_wrong_attitude(self):
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'not-a-valid-attitude',
            'relation': '',
        }
        response = discussion_justify(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_relation(self):
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'attitude': 'agree',
            'relation': 'i am groot',
        }
        response = discussion_justify(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_wrong_slug(self):
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'kitty-or-doggy-is-a-wrong-slug',
            'statement_or_arg_id': 2,
            'attitude': 'agree',
            'relation': '',
        }
        response = discussion_justify(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_stmt_or_arg_id_does_not_belong_to_issue(self):
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 40,
            'attitude': 'agree',
            'relation': '',
        }
        response = discussion_justify(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)
