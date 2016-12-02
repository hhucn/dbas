import unittest
import transaction
from sqlalchemy import and_

from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from dbas.database.discussion_model import StatementSeenBy, VoteStatement, ArgumentSeenBy, VoteArgument, User

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionJustifyViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.clear_seen_by()
        self.clear_votes()

    def tearDown(self):
        testing.tearDown()

    @staticmethod
    def clear_seen_by():
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).delete()
        DBDiscussionSession.query(ArgumentSeenBy).filter_by(user_uid=db_user.uid).delete()
        transaction.commit()

    @staticmethod
    def clear_votes():
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        DBDiscussionSession.query(VoteStatement).filter_by(author_uid=db_user.uid).delete()
        DBDiscussionSession.query(VoteArgument).filter_by(author_uid=db_user.uid).delete()
        transaction.commit()

    def test_justify_statement_page(self):
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())

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
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def test_support_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_vote1 = len(DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.is_valid == True,
                                                                                VoteStatement.is_up_vote == True)).all())
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
        len_db_vote2 = len(DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.is_valid == True,
                                                                                VoteStatement.is_up_vote == True)).all())

        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        self.clear_seen_by()
        self.clear_votes()

    def test_attack_statement_page(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_justify as d

        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_vote1 = len(DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.is_valid == True,
                                                                                VoteStatement.is_up_vote == False)).all())
        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'f',
            'relation': '',
        }
        response = d(request)
        transaction.commit()
        verify_dictionary_of_view(self, response)
        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_vote2 = len(DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.is_valid == True,
                                                                                VoteStatement.is_up_vote == False)).all())

        count = sum([len(el['premises']) for el in response['items']['elements']])
        self.assertEqual(len_db_seen1 + count, len_db_seen2)
        self.assertEqual(len_db_vote1 + 1, len_db_vote2)
        self.clear_seen_by()
        self.clear_votes()

    def test_dont_know_statement_page(self):
        from dbas.views import discussion_justify as d


        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())

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
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def test_justify_argument_page(self):
        from dbas.views import discussion_justify as d


        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())

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
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def test_false_page(self):
        from dbas.views import discussion_justify as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': 'blabla',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 40,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'statement_or_arg_id': 2,
            'mode': 'babla',
            'relation': '',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-doggy-dog-dog',
            'statement_or_arg_id': 2,
            'mode': 't',
            'relation': '',
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)
