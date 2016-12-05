import unittest
import transaction

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementSeenBy, User
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionInitViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import discussion_init as d

        # check count of seen by statements
        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        # not logged in, no change
        self.assertEqual(len_db_seen1, len_db_seen2)

    def test_page_logged_in(self):
        from dbas.views import discussion_init as d
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # check count of seen by statements
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).all())

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        # elements, which were seen
        self.assertIn('elements', response['items'])
        el_count = len(response['items']['elements']) - 1  # -1 for login / add
        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).all())
        self.assertEqual(len_db_seen1 + el_count, len_db_seen2)
        transaction.commit()  # normally pyramid_tm does this

    def test_page_logged_in_again(self):
        from dbas.views import discussion_init as d
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # check count of seen by statements
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).all())

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        # elements, which were seen are now equals the first, cause we have seen them already
        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).all())
        self.assertEqual(len_db_seen1, len_db_seen2)

        # remove seen statements
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        DBDiscussionSession.query(StatementSeenBy).filter_by(user_uid=db_user.uid).delete()
        transaction.commit()
