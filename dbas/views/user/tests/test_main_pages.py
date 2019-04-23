import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.password import get_hashed_password
from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views.user.rendered import notifications, settings, user


class MainNotificationsViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = construct_dummy_request()
        response = notifications(request)
        verify_dictionary_of_view(response)


class MainSettingsViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        request = construct_dummy_request()
        self.assertEqual(400, settings(request).status_code)


class MainSettingsViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def test_page(self):
        request = construct_dummy_request()
        response = settings(request)
        verify_dictionary_of_view(response)

        # check settings
        self.assertIn('send_notifications', response['settings'])
        self.assertIn('send_mails', response['settings'])
        self.assertIn('public_nick', response['settings'])


class MainSettingsViewTestsPassword(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def test_page_failure(self):
        request = construct_dummy_request(params={
            'form.passwordchange.submitted': '',
            'passwordold': 'tobia',
            'password': 'tobias',
            'passwordconfirm': 'tobias'
        })
        response = settings(request)
        verify_dictionary_of_view(response)

        # check settings
        self.assertTrue(len(response['settings']['passwordold']) != 0)
        self.assertTrue(len(response['settings']['password']) != 0)
        self.assertTrue(len(response['settings']['passwordconfirm']) != 0)

    def test_page_success(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()

        request = construct_dummy_request(params={
            'form.passwordchange.submitted': '',
            'passwordold': 'tobias',
            'password': 'tobiass',
            'passwordconfirm': 'tobiass'
        })
        response = settings(request)
        verify_dictionary_of_view(response)

        # check settings
        self.assertTrue(len(response['settings']['passwordold']) == 0)
        self.assertTrue(len(response['settings']['password']) == 0)
        self.assertTrue(len(response['settings']['passwordconfirm']) == 0)

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()


class MainUserView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_settings = db_user.settings
        db_settings.set_show_public_nickname(True)
        transaction.commit()

    def test_page(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        request = construct_dummy_request(matchdict={'uid': db_user.uid})
        response = user(request)
        verify_dictionary_of_view(response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertFalse(response['can_send_notification'])

    def test_page_myself(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        request = construct_dummy_request(matchdict={'uid': db_user.uid})
        response = user(request)
        verify_dictionary_of_view(response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertFalse(response['can_send_notification'])

    def test_page_other(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()

        request = construct_dummy_request(matchdict={'uid': db_user.uid})
        response = user(request)
        verify_dictionary_of_view(response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertTrue(response['can_send_notification'])

    def test_page_error1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = construct_dummy_request(matchdict={'uid': 0})
        try:
            user(request)
        except HTTPNotFound:
            pass

    def test_page_error2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = construct_dummy_request(matchdict={'uid': 1000})
        try:
            user(request)
        except HTTPNotFound:
            pass

    def test_page_error3(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = construct_dummy_request(matchdict={'uid1': 3})
        try:
            user(request)
        except HTTPNotFound:
            pass

    def test_page_error4(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = construct_dummy_request(matchdict={'uid': 'a'})
        try:
            user(request)
        except HTTPNotFound:
            pass
