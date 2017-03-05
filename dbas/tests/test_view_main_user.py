import unittest
import transaction

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Settings
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config
from pyramid.httpexceptions import HTTPNotFound


class MainUserView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
        db_settings.set_show_public_nickname(True)
        transaction.commit()

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_user as d
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        request = testing.DummyRequest(matchdict={'uid': db_user.uid})
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertFalse(response['can_send_notification'])

    def test_page_myself(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        request = testing.DummyRequest(matchdict={'uid': db_user.uid})
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertFalse(response['can_send_notification'])

    def test_page_other(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()

        request = testing.DummyRequest(matchdict={'uid': db_user.uid})
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertTrue(response['can_send_notification'])

    def test_page_error1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid': 0})
        try:
            d(request)
        except HTTPNotFound:
            pass

    def test_page_error2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid': 1000})
        try:
            d(request)
        except HTTPNotFound:
            pass

    def test_page_error3(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid1': 3})
        try:
            d(request)
        except HTTPNotFound:
            pass

    def test_page_error4(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid': 'a'})
        try:
            d(request)
        except HTTPNotFound:
            pass
