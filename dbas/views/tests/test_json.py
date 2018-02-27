import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer.mailer import DummyMailer

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.password import get_hashed_password
from dbas.views import user_password_request


class AjaxTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.include('pyramid_mailer.testing')

    def tearDown(self):
        testing.tearDown()

    def test_user_login_wrong_nick(self):
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(json_body={
            'user': 'Tobiass',
            'password': 'tobias',
            'keep_login': False,
            'url': ''
        }, mailer=DummyMailer)
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_user_login_wrong_password(self):
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(json_body={
            'user': 'Tobias',
            'password': 'tobiass',
            'keep_login': False,
            'url': ''
        }, mailer=DummyMailer)
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_user_login(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(json_body={
            'user': 'Tobias',
            'password': 'tobias',
            'keep_login': False,
            'url': ''
        }, mailer=DummyMailer)
        response = ajax(request)
        self.assertTrue(type(response) is HTTPFound)

    def test_user_logout(self):
        from dbas.views import user_logout as ajax
        request = testing.DummyRequest(params={})
        response = ajax(request)
        self.assertTrue(type(response) is HTTPFound)

    def test_user_password_request_failure_wrong_email(self):
        request = testing.DummyRequest(json_body={'email': 'penguinswillrule@theworld.com'}, mailer=DummyMailer)
        response = user_password_request(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['info']) != 0)

    def test_user_password_request_failure_wrong_key(self):
        request = testing.DummyRequest(json_body={'emai': 'krauthoff@cs.uni-duesseldorf.de'}, mailer=DummyMailer)
        response = user_password_request(request)
        self.assertIsNotNone(response)
        self.assertTrue(400 == response.status_code)

    def test_user_password_request(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        request = testing.DummyRequest(json_body={'email': 'krauthoff@cs.uni-duesseldorf.de'}, mailer=DummyMailer)
        response = user_password_request(request)
        self.assertIsNotNone(response)
        self.assertTrue(db_user.password != get_hashed_password('tobias'))
        db_user.password = get_hashed_password('tobias')
        transaction.commit()

    def test_fuzzy_search_mode_0(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 0, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_1(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 1, 'statement_uid': 1})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_2(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 2, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_3(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 3, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_4(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 4, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_5(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 5, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_8(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 8, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_9(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 9, 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_failure_mode(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': '6', 'statement_uid': 0})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_switch_language(self):
        from dbas.views import switch_language as ajax
        lang = ['de', 'en']
        for l in lang:
            request = testing.DummyRequest(json_body={'lang': l})
            response = ajax(request)
            self.assertTrue(response['_LOCALE_'] == l)

    def test_switch_language_failure(self):
        from dbas.views import switch_language as ajax
        request = testing.DummyRequest(json_body={'lang': 'sw'})
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_set_user_language(self):
        from dbas.views import set_user_lang as ajax
        request = testing.DummyRequest(json_body={'lang': 'en'})
        response = ajax(request)
        self.assertTrue(400 == response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(json_body={'lang': 'en'})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'en')
        self.assertTrue(response['current_lang'] == 'English')
        request = testing.DummyRequest(json_body={'lang': 'de'})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'de')
        self.assertTrue(response['current_lang'] == 'Deutsch')
        request = testing.DummyRequest(json_body={'lang': 'li'})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['ui_locales'] == 'li')
        self.assertTrue(response['current_lang'] == '')

    def test_set_user_setting_mail(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertTrue(400 == response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(json_body={'service': 'mail', 'settings_value': False})
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
        request = testing.DummyRequest(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertTrue(400 == response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(json_body={'service': 'notification', 'settings_value': True})
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
        request = testing.DummyRequest(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertTrue(400 == response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(json_body={'service': 'public_nick', 'settings_value': False})
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
        request = testing.DummyRequest(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertTrue(400 == response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(json_body={'service': 'oha', 'settings_value': False})
        response = ajax(request)
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_mark_statement_or_argument(self):
        from dbas.views import mark_or_unmark_statement_or_argument as ajax
        request = testing.DummyRequest(json_body={'ui_locales': 'en'})
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        for b1 in [True, False]:
            for b2 in [True, False]:
                for b3 in [True, False]:
                    request = testing.DummyRequest(
                        json_body={'uid': 4, 'is_argument': b1, 'should_mark': b2, 'step': 'reaction/4/undercut/6',
                                   'is_supportive': b3})
                    response = ajax(request)
                    self.assertTrue(len(response['text']) > 0)
