import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, ClickedStatement, SeenArgument, ClickedArgument, User, \
    ReputationHistory
from dbas.helper.test import verify_dictionary_of_view, clear_seen_by_of, clear_clicks_of


class DiscussionReactionViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.default_request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def tearDown(self):
        testing.tearDown()
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_page(self):
        from dbas.views import discussion_reaction as d

        len_db_seen_s1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_votes_s1 = DBDiscussionSession.query(ClickedStatement).count()
        len_db_seen_a1 = DBDiscussionSession.query(SeenArgument).count()
        len_db_votes_a1 = DBDiscussionSession.query(ClickedArgument).count()

        response = d(self.default_request)
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = DBDiscussionSession.query(SeenStatement).count()
        len_db_votes_s2 = DBDiscussionSession.query(ClickedStatement).count()
        len_db_seen_a2 = DBDiscussionSession.query(SeenArgument).count()
        len_db_votes_a2 = DBDiscussionSession.query(ClickedArgument).count()
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def __check_standard_counting(self, route, db_user):
        len_db_seen_s1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_votes_s1 = DBDiscussionSession.query(ClickedStatement).count()
        len_db_seen_a1 = DBDiscussionSession.query(SeenArgument).count()
        len_db_votes_a1 = DBDiscussionSession.query(ClickedArgument).count()
        len_db_vote_arg1 = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == db_user.uid,
                                                                             ClickedArgument.argument_uid == 2,
                                                                             ClickedArgument.is_valid == True,
                                                                             ClickedArgument.is_up_vote == True).count()

        response = route(self.default_request)
        transaction.commit()
        verify_dictionary_of_view(self, response)

        len_db_seen_s2 = DBDiscussionSession.query(SeenStatement).count()
        len_db_votes_s2 = DBDiscussionSession.query(ClickedStatement).count()
        len_db_seen_a2 = DBDiscussionSession.query(SeenArgument).count()
        len_db_votes_a2 = DBDiscussionSession.query(ClickedArgument).count()
        len_db_vote_arg2 = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == db_user.uid,
                                                                             ClickedArgument.argument_uid == 2,
                                                                             ClickedArgument.is_valid == True,
                                                                             ClickedArgument.is_up_vote == True).count()

        self.assertEqual(len_db_seen_s1, len_db_seen_s2)
        self.assertLess(len_db_votes_s1, len_db_votes_s2)
        self.assertLess(len_db_seen_a1, len_db_seen_a2)
        self.assertLess(len_db_votes_a1, len_db_votes_a2)
        self.assertEqual(len_db_vote_arg1 + 1, len_db_vote_arg2)

    def test_page_logged_in(self):
        from dbas.views import discussion_reaction as d
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        self.__check_standard_counting(d, db_user)

        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')

    def test_page_rep(self):
        from dbas.views import discussion_reaction as d
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()

        len_db_reputation1 = DBDiscussionSession.query(ReputationHistory).count()
        self.__check_standard_counting(d, db_user)
        len_db_reputation2 = DBDiscussionSession.query(ReputationHistory).count()
        self.assertNotEqual(len_db_reputation1, len_db_reputation2)

        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_page_rep_not_twice(self):
        from dbas.views import discussion_reaction as d
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()
        len_db_reputation1 = DBDiscussionSession.query(ReputationHistory).count()
        self.__check_standard_counting(d, db_user)
        len_db_reputation2 = DBDiscussionSession.query(ReputationHistory).count()
        self.assertEqual(len_db_reputation1, len_db_reputation2)

        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')

    def test_page_failure_slug(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-doggy_dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

    def test_page_failure_argument1(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 45,
            'mode': 'undermine',
            'arg_id_sys': 16,
        })
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

    def test_page_failure_argument2(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'undermine',
            'arg_id_sys': 45,
        })
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

    def test_page_failure_mode(self):
        from dbas.views import discussion_reaction as d

        request = testing.DummyRequest(matchdict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'mode': 'rebut',
            'arg_id_sys': 16,
        })
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass
