import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, User
from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views.discussion.rendered import init, discussion_overview


class DiscussionInitViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')


    def test_page(self):
        # check count of seen by statements
        len_db_seen1 = DBDiscussionSession.query(SeenStatement).count()

        request = construct_dummy_request(match_dict={'slug': 'cat-or-dog'})
        response = init(request)
        verify_dictionary_of_view(response)

        len_db_seen2 = DBDiscussionSession.query(SeenStatement).count()
        # not logged in, no change
        self.assertEqual(len_db_seen1, len_db_seen2)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # check count of seen by statements
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        len_db_seen1 = DBDiscussionSession.query(SeenStatement).filter_by(user_uid=db_user.uid).count()

        request = construct_dummy_request(match_dict={'slug': 'cat-or-dog'})
        response = init(request)
        verify_dictionary_of_view(response)

        # elements, which were seen
        self.assertIn('elements', response['items'])
        el_count = len(response['items']['elements']) - 1  # -1 for login / add
        len_db_seen2 = DBDiscussionSession.query(SeenStatement).filter_by(user_uid=db_user.uid).count()
        self.assertEqual(len_db_seen1 + el_count, len_db_seen2)

    def test_page_logged_in_again(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # check count of seen by statements
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        len_db_seen1 = DBDiscussionSession.query(SeenStatement).filter_by(user_uid=db_user.uid).count()

        request = construct_dummy_request(match_dict={'slug': 'cat-or-dog'})
        response = init(request)
        verify_dictionary_of_view(response)

        # elements, which were seen are now equals the first, cause we have seen them already
        len_db_seen2 = DBDiscussionSession.query(SeenStatement).filter_by(user_uid=db_user.uid).count()
        self.assertEqual(len_db_seen1, len_db_seen2)

        # remove seen statements
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        DBDiscussionSession.query(SeenStatement).filter_by(user_uid=db_user.uid).delete()


class MainMyDiscussionViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')


    def test_page(self):
        request = testing.DummyRequest()
        response = discussion_overview(request)
        verify_dictionary_of_view(response)

        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('issues', response)


class MainMyDiscussionViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)


    def test_page(self):
        request = testing.DummyRequest()
        response = discussion_overview(request)
        verify_dictionary_of_view(response)

        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('issues', response)
