import unittest

from pyramid import testing, httpexceptions

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, ClickedStatement, SeenArgument, ClickedArgument, \
    ReputationHistory, User
from dbas.helper.test import verify_dictionary_of_view, clear_seen_by_of, clear_clicks_of, clear_reputation_of_user
from dbas.lib import Relations
from dbas.tests.utils import construct_dummy_request
from dbas.views import reaction


class DiscussionReactionViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.default_request = construct_dummy_request(match_dict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 16,
        })
        self.user_bjoern = DBDiscussionSession.query(User).get(4)
        self.user_tobi = DBDiscussionSession.query(User).get(2)
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')
        clear_reputation_of_user(self.user_bjoern)
        clear_reputation_of_user(self.user_tobi)

    def tearDown(self):
        testing.tearDown()
        clear_seen_by_of('Tobias')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Björn')
        clear_clicks_of('Björn')
        clear_reputation_of_user(self.user_bjoern)
        clear_reputation_of_user(self.user_tobi)
        super().tearDown()

    def test_page(self):
        len_db_seen_s1 = DBDiscussionSession.query(SeenStatement).count()
        len_db_votes_s1 = DBDiscussionSession.query(ClickedStatement).count()
        len_db_seen_a1 = DBDiscussionSession.query(SeenArgument).count()
        len_db_votes_a1 = DBDiscussionSession.query(ClickedArgument).count()

        response = reaction(self.default_request)
        verify_dictionary_of_view(response)

        len_db_seen_s2 = DBDiscussionSession.query(SeenStatement).count()
        len_db_votes_s2 = DBDiscussionSession.query(ClickedStatement).count()
        len_db_seen_a2 = DBDiscussionSession.query(SeenArgument).count()
        len_db_votes_a2 = DBDiscussionSession.query(ClickedArgument).count()
        self.assertEqual(len_db_seen_s1, len_db_seen_s2)  # no more cause we are not logged in
        self.assertEqual(len_db_votes_s1, len_db_votes_s2)
        self.assertEqual(len_db_seen_a1, len_db_seen_a2)
        self.assertEqual(len_db_votes_a1, len_db_votes_a2)

    def __check_standard_counting(self, view_fn, db_user):
        count_seen_stmts_before = DBDiscussionSession.query(SeenStatement).count()
        count_clicked_stmts_before = DBDiscussionSession.query(ClickedStatement).count()
        count_seen_args_before = DBDiscussionSession.query(SeenArgument).count()
        count_clicked_args_before = DBDiscussionSession.query(ClickedArgument).count()
        count_clicked_args_for_arg_2_before = \
            DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == db_user.uid,
                                                              ClickedArgument.argument_uid == 2,
                                                              ClickedArgument.is_valid == True,
                                                              ClickedArgument.is_up_vote == True).count()

        response = view_fn(self.default_request)
        verify_dictionary_of_view(response)

        count_seen_stmts_after = DBDiscussionSession.query(SeenStatement).count()
        count_clicked_stmts_after = DBDiscussionSession.query(ClickedStatement).count()
        count_seen_args_after = DBDiscussionSession.query(SeenArgument).count()
        count_clicked_args_after = DBDiscussionSession.query(ClickedArgument).count()
        count_clicked_args_for_arg_2_after = \
            DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == db_user.uid,
                                                              ClickedArgument.argument_uid == 2,
                                                              ClickedArgument.is_valid == True,
                                                              ClickedArgument.is_up_vote == True).count()

        self.assertEqual(count_seen_stmts_after, count_seen_stmts_before)
        self.assertGreater(count_clicked_stmts_after, count_clicked_stmts_before)
        self.assertGreater(count_seen_args_after, count_seen_args_before)
        self.assertGreater(count_clicked_args_after, count_clicked_args_before)
        self.assertEqual(count_clicked_args_for_arg_2_before + 1, count_clicked_args_for_arg_2_after)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        self.__check_standard_counting(reaction, self.user_tobi)

    def test_page_rep(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        len_db_reputation_initial = DBDiscussionSession.query(ReputationHistory).count()
        self.__check_standard_counting(reaction, self.user_bjoern)
        len_db_reputation_after_first_visit = DBDiscussionSession.query(ReputationHistory).count()
        self.assertGreater(len_db_reputation_after_first_visit, len_db_reputation_initial)

    def test_page_rep_not_twice(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)

        len_db_reputation_initial = DBDiscussionSession.query(ReputationHistory).count()
        self.__check_standard_counting(reaction, self.user_bjoern)
        len_db_reputation_after_first_visit = DBDiscussionSession.query(ReputationHistory).count()

        response = reaction(self.default_request)
        self.assertIsInstance(response, dict)
        len_db_reputation_after_second_visit = DBDiscussionSession.query(ReputationHistory).count()

        self.assertGreater(len_db_reputation_after_first_visit, len_db_reputation_initial)
        self.assertEqual(len_db_reputation_after_first_visit, len_db_reputation_after_second_visit,
                         'No rep on second visit')

    def test_invalid_slug_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-doggy_dog',
            'arg_id_user': 2,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 16,
        })
        response = reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_user_argument_does_not_belong_to_issue_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-dog',
            'arg_id_user': 45,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 16,
        })
        response = reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_sys_argument_does_not_belong_to_issue_returns_error(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'relation': Relations.UNDERMINE.value,
            'arg_id_sys': 45,
        })
        response = reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)

    def test_page_failure_mode(self):
        request = construct_dummy_request(match_dict={
            'slug': 'cat-or-dog',
            'arg_id_user': 2,
            'relation': 'invalid-relation',
            'arg_id_sys': 16,
        })
        response = reaction(request)
        self.assertIsInstance(response, httpexceptions.HTTPError)
