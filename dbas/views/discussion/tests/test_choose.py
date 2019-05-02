import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Premise, SeenStatement, User
from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views import choose


class DiscussionChoseViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.arg_uid = 15
        self.pgroup_uid = 28
        self.is_supportive = False
        self.is_argument = True

    def test_page(self):
        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()

        request = construct_dummy_request(matchdict={
            'slug': 'cat-or-dog',
            'pgroup_ids': [self.pgroup_uid],
        })
        response = choose(request)
        verify_dictionary_of_view(response)

        len_db_seen2 = DBDiscussionSession.query(SeenStatement).count()
        # not logged in, no change
        self.assertEqual(len_db_seen1, len_db_seen2)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        DBDiscussionSession.query(User).filter_by(nickname='Tobias').first().update_last_login()
        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()

        request = construct_dummy_request(matchdict={
            'slug': 'cat-or-dog',
            'pgroup_ids': [self.pgroup_uid],
        })
        response = choose(request)
        verify_dictionary_of_view(response)

        len_db_seen2 = DBDiscussionSession.query(SeenStatement).count()

        count = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=self.pgroup_uid).count()
        self.assertEqual(len_db_seen1 + count, len_db_seen2)

    def test_page_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': 'cat-or-dog',
            'pgroup_ids': [self.pgroup_uid, 'a'],
        })
        response = choose(request)
        self.assertEqual(400, response.status_code)

        request = construct_dummy_request(matchdict={
            'slug': 'cat-or-doggy-dog',
            'pgroup_ids': [self.pgroup_uid, 'a'],
        })
        response = choose(request)
        self.assertEqual(400, response.status_code)

        request = construct_dummy_request(matchdict={
            'slug': 'cat-or-doggy-dog',
            'pgroup_ids': [self.pgroup_uid, 55],
        })
        response = choose(request)
        self.assertEqual(400, response.status_code)
