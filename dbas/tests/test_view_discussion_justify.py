import unittest
import transaction
from sqlalchemy import and_

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from dbas.database.discussion_model import StatementSeenBy, ClickedStatement, ArgumentSeenBy, ClickedArgument, ReputationHistory

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view, clear_seen_by_of, clear_votes_of
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionJustifyViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        clear_seen_by_of('Tobias')
        clear_votes_of('Tobias')
        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def tearDown(self):
        testing.tearDown()

    def test_justify_statement_page(self):
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(ClickedArgument).all())

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(ClickedArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def test_support_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())
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
        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_vote2 = len(DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.is_valid == True,
                                                                                   ClickedStatement.is_up_vote == True)).all())

        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        clear_seen_by_of('Tobias')
        clear_votes_of('Tobias')

    def test_attack_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())
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
        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_vote2 = len(DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.is_valid == True,
                                                                                   ClickedStatement.is_up_vote == False)).all())
        from dbas.logger import logger
        logger('X', 'X', str(response['items']))
        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        clear_seen_by_of('Tobias')
        clear_votes_of('Tobias')

    def test_dont_know_statement_page(self):
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(ClickedArgument).all())

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'd',
            'relation': '',
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(ClickedArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def test_justify_argument_page_no_rep(self):
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(ClickedArgument).all())
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

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(ClickedArgument).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)
        self.assertEqual(len_db_reputation1, len_db_reputation2)

    def test_justify_argument_page_rep(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(ClickedArgument).all())
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

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(ClickedArgument).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertNotEqual(len_db_seen_s1, len_db_seen_s2)
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertNotEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)
        self.assertNotEqual(len_db_reputation1, len_db_reputation2)
        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def test_justify_argument_page_rep_not_twice(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(ClickedArgument).all())
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

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(ClickedArgument).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertNotEqual(len_db_seen_s1, len_db_seen_s2)
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertNotEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)
        self.assertEqual(len_db_reputation1, len_db_reputation2)
        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def test_false_page(self):
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(ClickedArgument).all())

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

        # request = testing.DummyRequest()
        # request.matchdict = {
        #     'slug': 'cat-or-doggy-dog-dog',
        #     'statement_or_arg_id': 2,
        #     'mode': 't',
        #     'relation': '',
        # }
        # try:
        #     response = d(request)
        #     self.assertTrue(type(response) is HTTPNotFound)
        # except HTTPNotFound:
        #     pass

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(ClickedStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(ClickedArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)
