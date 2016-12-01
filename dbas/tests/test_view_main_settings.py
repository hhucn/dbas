import unittest
import json
import transaction

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Settings
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class MainSettingsViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_main_settings_page(self):
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

    def test_main_settings_page(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        # check settings
        self.assertIn('send_notifications', response['settings'])
        self.assertIn('send_mails', response['settings'])
        self.assertIn('public_nick', response['settings'])


class MainSettingsViewTestsAjax(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
        db_settings.set_send_notifications(True)
        db_settings.set_show_public_nickname(True)
        db_settings.set_send_mails(False)

        transaction.commit()

    def test_set_user_language(self):
        from dbas.views import set_user_language as ajax

        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'en')
        self.assertTrue(response['current_lang'] == 'English')

        request = testing.DummyRequest(params={'ui_locales': 'de'})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'de')
        self.assertTrue(response['current_lang'] == 'Deutsch')

        request = testing.DummyRequest(params={'ui_locales': 'li'})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['ui_locales'] == 'li')
        self.assertTrue(response['current_lang'] == '')

    def test_set_user_setting_mail(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'service': 'mail', 'settings_value': False})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_set_user_setting_notification(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'service': 'notification', 'settings_value': True})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_set_user_setting_nick(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'service': 'public_nick', 'settings_value': False})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_set_user_setting_no_service(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'service': 'oha', 'settings_value': False})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')
