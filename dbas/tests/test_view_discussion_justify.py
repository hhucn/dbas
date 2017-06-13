import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, ClickedStatement, SeenArgument, ClickedArgument, ReputationHistory
from dbas.helper.tests import verify_dictionary_of_view, clear_seen_by_of, clear_clicks_of


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
            'seen_s': len(DBDiscussionSession.query(SeenStatement).all()),
            'click_s': len(DBDiscussionSession.query(ClickedStatement).all()),
            'seen_a': len(DBDiscussionSession.query(SeenArgument).all()),
            'click_a': len(DBDiscussionSession.query(ClickedArgument).all())
        }
        if include_history:
            d['rep_h'] = len(DBDiscussionSession.query(ReputationHistory).all())
        return d

    def __check_meta_clicks(self, vote_dict):
        self.assertEqual(vote_dict['seen_s'], len(DBDiscussionSession.query(SeenStatement).all()))
        self.assertEqual(vote_dict['click_s'], len(DBDiscussionSession.query(ClickedStatement).all()))
        self.assertEqual(vote_dict['seen_a'], len(DBDiscussionSession.query(SeenArgument).all()))
        self.assertEqual(vote_dict['click_a'], len(DBDiscussionSession.query(ClickedArgument).all()))
        if 'rep_h' in vote_dict:
            self.assertEqual(vote_dict['rep_h'], len(DBDiscussionSession.query(ReputationHistory).all()))

    def test_justify_statement_page(self):
        from dbas.views import discussion_justify as d
        vote_dict = self.__get_meta_clicks(False)
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.__check_meta_clicks(vote_dict)
        self.__check_meta_clicks(vote_dict)

    def test_support_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = len(DBDiscussionSession.query(SeenStatement).all())
        len_db_vote1 = len(DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.is_valid == True,
                                                                                   ClickedStatement.is_up_vote == True)).all())
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        transaction.commit()
        verify_dictionary_of_view(self, response)
        len_db_seen2 = len(DBDiscussionSession.query(SeenStatement).all())
        len_db_vote2 = len(DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.is_valid == True,
                                                                                   ClickedStatement.is_up_vote == True)).all())

        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')

    def test_attack_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = len(DBDiscussionSession.query(SeenStatement).all())
        len_db_vote1 = len(DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.is_valid == True,
                                                                                   ClickedStatement.is_up_vote == False)).all())
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'f',
            'relation': ''
        }
        response = d(request)
        transaction.commit()
        verify_dictionary_of_view(self, response)
        len_db_seen2 = len(DBDiscussionSession.query(SeenStatement).all())
        len_db_vote2 = len(DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.is_valid == True,
                                                                                   ClickedStatement.is_up_vote == False)).all())

        # minus 1 for 'none of the above'
        count = sum([len(el['premises']) for el in response['items']['elements']]) - 1
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
            'mode': 'd',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.__check_meta_clicks(vote_dict)

    def test_justify_argument_page_no_rep(self):
        from dbas.views import discussion_justify as d
        vote_dict = self.__get_meta_clicks(True)
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': ['undermine'],
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.__check_meta_clicks(vote_dict)
        self.assertEqual(len_db_reputation1, len_db_reputation2)

    def test_justify_argument_page_rep(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import discussion_justify as d
        vote_dict = self.__get_meta_clicks(True)
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': ['undermine'],
        }
        response = d(request)
        verify_dictionary_of_view(self, response)
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.__check_meta_clicks(vote_dict)
        self.assertNotEqual(len_db_reputation1, len_db_reputation2)
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_justify_argument_page_rep_not_twice(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import discussion_justify as d

        vote_dict = self.__get_meta_clicks(True)
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': ['undermine'],
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.__check_meta_clicks(vote_dict)
        self.assertEqual(len_db_reputation1, len_db_reputation2)
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_false_page(self):
        from dbas.views import discussion_justify as d

        vote_dict = self.__get_meta_clicks(False)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
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
            'mode': 't',
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
