import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, ClickedStatement, SeenArgument, ClickedArgument, \
    ReputationHistory
from dbas.helper.test import verify_dictionary_of_view, clear_seen_by_of, clear_clicks_of, refresh_user


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

    def __get_meta_clicks(self, include_history):
        d = {
            'seen_s': DBDiscussionSession.query(SeenStatement).count(),
            'click_s': DBDiscussionSession.query(ClickedStatement).count(),
            'seen_a': DBDiscussionSession.query(SeenArgument).count(),
            'click_a': DBDiscussionSession.query(ClickedArgument).count()
        }
        if include_history:
            d['rep_h'] = DBDiscussionSession.query(ReputationHistory).count()
        return d

    def __check_meta_clicks(self, vote_dict):
        self.assertEqual(vote_dict['seen_s'], DBDiscussionSession.query(SeenStatement).count())
        self.assertEqual(vote_dict['click_s'], DBDiscussionSession.query(ClickedStatement).count())
        self.assertEqual(vote_dict['seen_a'], DBDiscussionSession.query(SeenArgument).count())
        self.assertEqual(vote_dict['click_a'], DBDiscussionSession.query(ClickedArgument).count())
        if 'rep_h' in vote_dict:
            self.assertEqual(vote_dict['rep_h'], DBDiscussionSession.query(ReputationHistory).count())

    def test_justify_statement_page(self):
        from dbas.views import discussion_justify as d
        vote_dict = self.__get_meta_clicks(False)
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'agree',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(response)
        self.__check_meta_clicks(vote_dict)
        self.__check_meta_clicks(vote_dict)

    def test_support_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_vote1 = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.is_valid == True,
                                                                          ClickedStatement.is_up_vote == True).count()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'agree',
            'relation': '',
        }
        response = d(request)
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
        from dbas.views import discussion_justify as d

        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_vote1 = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.is_valid == True,
                                                                          ClickedStatement.is_up_vote == False).count()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'disagree',
            'relation': ''
        }
        response = d(request)
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
        from dbas.views import discussion_justify as d
        vote_dict = self.__get_meta_clicks(False)
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'dontknow',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(response)
        self.__check_meta_clicks(vote_dict)

    def test_justify_argument_page_no_rep(self):
        from dbas.views import discussion_justify as d
        vote_dict = self.__get_meta_clicks(True)
        len_db_reputation1 = DBDiscussionSession.query(ReputationHistory).count()
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'agree',
            'relation': ['undermine'],
        }
        response = d(request)
        verify_dictionary_of_view(response)

        len_db_reputation2 = DBDiscussionSession.query(ReputationHistory).count()
        self.__check_meta_clicks(vote_dict)
        self.assertEqual(len_db_reputation1, len_db_reputation2)

    def __test_base_for_justify_argument_page_rep(self, view):
        vote_dict = self.__get_meta_clicks(True)
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'agree',
            'relation': ['undermine'],
        }
        response = view(request)
        verify_dictionary_of_view(response)
        self.assertNotEqual(vote_dict['seen_s'], DBDiscussionSession.query(SeenStatement).count())
        self.assertEqual(vote_dict['click_s'], DBDiscussionSession.query(ClickedStatement).count())
        self.assertNotEqual(vote_dict['seen_a'], DBDiscussionSession.query(SeenArgument).count())
        self.assertEqual(vote_dict['click_a'], DBDiscussionSession.query(ClickedArgument).count())
        return vote_dict

    def test_justify_argument_page_rep(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        refresh_user('Björn')
        from dbas.views import discussion_justify as d
        vote_dict = self.__test_base_for_justify_argument_page_rep(d)
        self.assertNotEqual(vote_dict['rep_h'], DBDiscussionSession.query(ReputationHistory).count())
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_justify_argument_page_rep_not_twice(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import discussion_justify as d
        vote_dict = self.__test_base_for_justify_argument_page_rep(d)
        self.assertEqual(vote_dict['rep_h'], DBDiscussionSession.query(ReputationHistory).count())
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_false_page(self):
        from dbas.views import discussion_justify as d

        vote_dict = self.__get_meta_clicks(False)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'agree',
            'relation': 'blabla',
        }
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 40,
            'mode': 'agree',
            'relation': '',
        }
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'babla',
            'relation': '',
        }
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

        self.__check_meta_clicks(vote_dict)
