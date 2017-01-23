import unittest
import transaction

from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementSeenBy, VoteStatement, ArgumentSeenBy, VoteArgument, User, ReputationHistory
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view, clear_seen_by_of, clear_votes_of
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionReactionViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        clear_seen_by_of('Tobias')
        clear_votes_of('Tobias')
        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def tearDown(self):
        testing.tearDown()
        clear_seen_by_of('Tobias')
        clear_votes_of('Tobias')
        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def test_page(self):
        from dbas.views import discussion_reaction as d

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
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

    def test_page_logged_in(self):
        from dbas.views import discussion_reaction as d
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())
        len_db_vote_arg1 = len(DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == db_user.uid,
                                                                                   VoteArgument.argument_uid == 2,
                                                                                   VoteArgument.is_valid == True,
                                                                                   VoteArgument.is_up_vote == True)).all())

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        response = d(request)
        transaction.commit()
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        len_db_vote_arg2 = len(DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == db_user.uid,
                                                                                   VoteArgument.argument_uid == 2,
                                                                                   VoteArgument.is_valid == True,
                                                                                   VoteArgument.is_up_vote == True)).all())

        self.assertEqual(len_db_seen_s1, len_db_seen_s2)
        self.assertLess(len_db_votes_s1, len_db_votes_s2)
        self.assertLess(len_db_seen_a1, len_db_seen_a2)
        self.assertLess(len_db_votes_a1, len_db_votes_a2)
        self.assertEqual(len_db_vote_arg1 + 1, len_db_vote_arg2)

        clear_seen_by_of('Tobias')
        clear_votes_of('Tobias')

    def test_page_rep(self):
        from dbas.views import discussion_reaction as d
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())
        len_db_vote_arg1 = len(DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == db_user.uid,
                                                                                   VoteArgument.argument_uid == 2,
                                                                                   VoteArgument.is_valid == True,
                                                                                   VoteArgument.is_up_vote == True)).all())
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        response = d(request)
        transaction.commit()
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        len_db_vote_arg2 = len(DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == db_user.uid,
                                                                                   VoteArgument.argument_uid == 2,
                                                                                   VoteArgument.is_valid == True,
                                                                                   VoteArgument.is_up_vote == True)).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())

        self.assertEqual(len_db_seen_s1, len_db_seen_s2)
        self.assertLess(len_db_votes_s1, len_db_votes_s2)
        self.assertLess(len_db_seen_a1, len_db_seen_a2)
        self.assertLess(len_db_votes_a1, len_db_votes_a2)
        self.assertEqual(len_db_vote_arg1 + 1, len_db_vote_arg2)
        self.assertNotEqual(len_db_reputation1, len_db_reputation2)

        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def test_page_rep_not_twice(self):
        from dbas.views import discussion_reaction as d
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()

        len_db_seen_s1 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s1 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a1 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a1 = len(DBDiscussionSession.query(VoteArgument).all())
        len_db_vote_arg1 = len(DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == db_user.uid,
                                                                                   VoteArgument.argument_uid == 2,
                                                                                   VoteArgument.is_valid == True,
                                                                                   VoteArgument.is_up_vote == True)).all())
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        response = d(request)
        transaction.commit()
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        len_db_votes_s2 = len(DBDiscussionSession.query(VoteStatement).all())
        len_db_seen_a2 = len(DBDiscussionSession.query(ArgumentSeenBy).all())
        len_db_votes_a2 = len(DBDiscussionSession.query(VoteArgument).all())
        len_db_vote_arg2 = len(DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.author_uid == db_user.uid,
                                                                                   VoteArgument.argument_uid == 2,
                                                                                   VoteArgument.is_valid == True,
                                                                                   VoteArgument.is_up_vote == True)).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())

        self.assertEqual(len_db_seen_s1, len_db_seen_s2)
        self.assertLess(len_db_votes_s1, len_db_votes_s2)
        self.assertLess(len_db_seen_a1, len_db_seen_a2)
        self.assertLess(len_db_votes_a1, len_db_votes_a2)
        self.assertEqual(len_db_vote_arg1 + 1, len_db_vote_arg2)
        self.assertEqual(len_db_reputation1, len_db_reputation2)

        clear_seen_by_of('Björn')
        clear_votes_of('Björn')

    def test_page_failure_slug(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-doggy_dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        response = d(request)
        verify_dictionary_of_view(self, response)

    def test_page_failure_argument1(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 45,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

    def test_page_failure_argument2(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 45,
        })
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

    def test_page_failure_mode(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'rebut',
            'arg_id_sys': 16,
        })
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)
