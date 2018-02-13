import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer.mailer import DummyMailer

from dbas.auth.login import login_user, register_user_with_ajax_data, login_user_oauth
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.views import user_login


class AuthLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_login_user(self):
        nickname = 'Bob'
        password = 'iamatestuser2016'
        for_api = False
        keep_login = True

        request = testing.DummyRequest(json_body={
            'user': nickname,
            'password': password,
            'keep_login': keep_login,
            'redirect_url': 'http://some.url'
        }, mailer=DummyMailer)

        _tn = Translator('en')
        response = user_login(request)
        self.assertTrue(type(response) is HTTPFound)

        keep_login = True
        response = login_user(request, nickname, password, for_api=for_api, keep_login=keep_login, lang=_tn)
        self.assertTrue(type(response) is HTTPFound)

        for_api = True
        response = login_user(request, nickname, password, for_api=for_api, keep_login=keep_login, lang=_tn)
        self.assertTrue(type(response) is dict)
        self.assertIn('status', response)

    def test_login_register_with_ajax_data(self):
        _tn = Translator('en')

        request = testing.DummyRequest(params={
            'firstname': '',
            'lastname': '',
            'nickname': '',
            'email': ' ',
            'gender': '',
            'password': '',
            'passwordconfirm': '',
            'g-recaptcha-response': '',
            'mode': '',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.pwdShort), msg)
        self.assertIsNone(db_new_user)

        request = testing.DummyRequest(params={
            'firstname': 'Tobias',
            'lastname': 'Krauthoff',
            'nickname': 'Tobias',
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'g-recaptcha-response': '',
            'mode': 'manually',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.nickIsTaken), msg)
        self.assertIsNone(db_new_user)

        request = testing.DummyRequest(params={
            'firstname': 'Tobiass',
            'lastname': 'Krauthoff',
            'nickname': 'Tobiass',
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'g-recaptcha-response': '',
            'mode': 'manually',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.mailIsTaken), msg)
        self.assertIsNone(db_new_user)

        request = testing.DummyRequest(params={
            'firstname': 'Tobiass',
            'lastname': 'Krauthoff',
            'nickname': 'Tobiass',
            'email': 'bla@blaaa ',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'g-recaptcha-response': '',
            'mode': 'manually',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.mailNotValid), msg)
        self.assertIsNone(db_new_user)

        request = testing.DummyRequest(params={
            'firstname': 'Tobiass',
            'lastname': 'Krauthoff',
            'nickname': 'Tobiass',
            'email': 'dbas@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'g-recaptcha-response': '',
            'mode': 'manually',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.maliciousAntiSpam), msg)
        self.assertIsNone(db_new_user)

        request = testing.DummyRequest(params={
            'firstname': 'Bob',
            'lastname': 'Builder',
            'nickname': 'Builder',
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswdd',
            'g-recaptcha-response': '',
            'mode': 'manually',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.pwdNotEqual), msg)
        self.assertIsNone(db_new_user)

        request = testing.DummyRequest(params={
            'firstname': 'Bob',
            'lastname': 'Builder',
            'nickname': 'Builder',
            'email': 'dbas@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'g-recaptcha-response': '',
            'mode': 'manually',
        }, matchdict={})
        success, msg, db_new_user = register_user_with_ajax_data(request.params, 'en', None)
        self.assertEqual(_tn.get(_.maliciousAntiSpam), msg)
        self.assertIsNone(db_new_user)

    def test_login_user_oauth(self):
        services = ['google', 'github', 'facebook', '']  # 'twitter'
        for service in services:
            redirect_uri = 'http://lvh.me:4284'
            ui_locales = 'en'
            environ = {
                'OAUTH_GOOGLE_CLIENTID': 'OAUTH_GOOGLE_CLIENTID',
                'OAUTH_GOOGLE_CLIENTKEY': 'OAUTH_GOOGLE_CLIENTKEY',
                'OAUTH_GITHUB_CLIENTID': 'OAUTH_GITHUB_CLIENTID',
                'OAUTH_GITHUB_CLIENTKEY': 'OAUTH_GITHUB_CLIENTKEY',
                'OAUTH_FACEBOOK_CLIENTID': 'OAUTH_FACEBOOK_CLIENTID',
                'OAUTH_FACEBOOK_CLIENTKEY': 'OAUTH_FACEBOOK_CLIENTKEY',
                'OAUTH_TWITTER_CLIENTID': 'OAUTH_TWITTER_CLIENTID',
                'OAUTH_TWITTER_CLIENTKEY': 'OAUTH_TWITTER_CLIENTKEY',
            }
            request = testing.DummyRequest(params={'application_url': 'http://lvh.me'}, matchdict={}, environ=environ)
            request.environ = environ
            resp = login_user_oauth(request, service, redirect_uri, redirect_uri, ui_locales)
            if len(service) > 0:
                self.assertIsNotNone(resp)
            else:
                self.assertIsNone(resp)
