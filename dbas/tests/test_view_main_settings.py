import unittest
import transaction

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from dbas.handler.password import get_hashed_password
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class MainSettingsViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest()
        response = d(request)
        from pyramid.httpexceptions import HTTPFound
        self.assertTrue(type(response) is HTTPFound)


class MainSettingsViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        # check settings
        self.assertIn('send_notifications', response['settings'])
        self.assertIn('send_mails', response['settings'])
        self.assertIn('public_nick', response['settings'])


class MainSettingsViewTestsPassword(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page_failure(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest(params={
            'form.passwordchange.submitted': '',
            'passwordold': 'tobia',
            'password': 'tobias',
            'passwordconfirm': 'tobias'
        })
        response = d(request)
        verify_dictionary_of_view(self, response)

        # check settings
        self.assertTrue(len(response['settings']['passwordold']) != 0)
        self.assertTrue(len(response['settings']['password']) != 0)
        self.assertTrue(len(response['settings']['passwordconfirm']) != 0)

    def test_page_success(self):
        from dbas.views import main_settings as d

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()

        request = testing.DummyRequest(params={
            'form.passwordchange.submitted': '',
            'passwordold': 'tobias',
            'password': 'tobiass',
            'passwordconfirm': 'tobiass'
        })
        response = d(request)
        verify_dictionary_of_view(self, response)

        # check settings
        self.assertTrue(len(response['settings']['passwordold']) == 0)
        self.assertTrue(len(response['settings']['password']) == 0)
        self.assertTrue(len(response['settings']['passwordconfirm']) == 0)

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()
