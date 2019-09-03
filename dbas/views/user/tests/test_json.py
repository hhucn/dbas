import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.password import get_hashed_password
from dbas.tests.utils import construct_dummy_request
from dbas.views import user_password_request


class AjaxTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.include('pyramid_mailer.testing')

    def test_user_login_wrong_nick(self):
        from dbas.views import user_login as ajax
        request = construct_dummy_request(json_body={
            'user': 'Tobiass',
            'password': 'tobias',
            'keep_login': False,
            'url': ''
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_user_login_wrong_password(self):
        from dbas.views import user_login as ajax
        request = construct_dummy_request(json_body={
            'user': 'Tobias',
            'password': 'tobiass',
            'keep_login': False,
            'url': ''
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertNotEqual(len(response['error']), 0)

    def test_user_login(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()
        from dbas.views import user_login as ajax
        request = construct_dummy_request(json_body={
            'user': 'Tobias',
            'password': 'tobias',
            'keep_login': False,
            'url': ''
        })
        response = ajax(request)
        self.assertIsInstance(response, HTTPFound)

    def test_user_logout(self):
        from dbas.views import user_logout as ajax
        request = construct_dummy_request(params={})
        response = ajax(request)
        self.assertIsInstance(response, HTTPFound)

    def test_user_password_request_failure_wrong_email(self):
        request = construct_dummy_request(json_body={'email': 'penguinswillrule@theworld.com'})
        response = user_password_request(request)
        self.assertIsNotNone(response)
        self.assertFalse(response['success'])
        self.assertNotEqual(len(response['message']), 0)

    def test_user_password_request_failure_wrong_key(self):
        request = construct_dummy_request(json_body={'emai': 'krauthoff@cs.hhu.de'})
        response = user_password_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_user_password_request(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        request = construct_dummy_request(json_body={'email': 'krauthoff@cs.hhu.de'})
        response = user_password_request(request)
        self.assertIsNotNone(response)
        self.assertNotEqual(db_user.password, get_hashed_password('tobias'))
        db_user.password = get_hashed_password('tobias')
        transaction.commit()

    def test_set_user_language(self):
        from dbas.views import set_user_lang as ajax
        request = construct_dummy_request(json_body={'lang': 'en'})
        response = ajax(request)
        self.assertEqual(response.status_code, 400)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'lang': 'en'})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'en')
        self.assertTrue(response['current_lang'] == 'English')
        request = construct_dummy_request(json_body={'lang': 'de'})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'de')
        self.assertTrue(response['current_lang'] == 'Deutsch')
        request = construct_dummy_request(json_body={'lang': 'li'})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['ui_locales'] == 'li')
        self.assertTrue(response['current_lang'] == '')

    def test_set_user_setting_mail(self):
        from dbas.views import set_user_settings as ajax
        request = construct_dummy_request(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertEqual(response.status_code, 400)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'service': 'mail', 'settings_value': False})
        response = ajax(request)
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
        request = construct_dummy_request(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertEqual(response.status_code, 400)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'service': 'notification', 'settings_value': True})
        response = ajax(request)
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
        request = construct_dummy_request(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertEqual(response.status_code, 400)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'service': 'public_nick', 'settings_value': False})
        response = ajax(request)
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
        request = construct_dummy_request(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertEqual(response.status_code, 400)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'service': 'oha', 'settings_value': False})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')
