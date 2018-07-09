# -*- coding: utf-8 -*-
import unittest
from uuid import uuid4

from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer.mailer import DummyMailer

from dbas.auth.login import login_local_user, register_user_with_json_data
from dbas.auth.oauth.main import login_oauth_user
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.views import user_login


class AuthLoginTest(unittest.TestCase):
    @staticmethod
    def uustring():
        """
        Create instance-unique strings to avoid clashes with pre-seeded database.

        :return: Stringified uuid
        :rtype: str
        """
        return str(uuid4())

    def setUp(self):
        self.config = testing.setUp()
        self._tn = Translator('en')

    def tearDown(self):
        testing.tearDown()

    def test_login_user(self):
        nickname = 'Bob'
        password = 'iamatestuser2016'
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

        response = login_local_user(nickname, password, DummyMailer, lang=_tn)
        self.assertTrue(isinstance(response, dict))
        self.assertNotIn('error', response)
        self.assertIn('user', response)

        response = login_local_user('definitelynotauser', '¯\_(ツ)_/¯', DummyMailer, lang=_tn)
        self.assertTrue(isinstance(response, dict))
        self.assertIn('error', response)
        self.assertNotIn('user', response)

    def test_login_register_with_json_data(self):
        request = testing.DummyRequest(validated={
            'firstname': '',
            'lastname': '',
            'nickname': '',
            'email': ' ',
            'gender': '',
            'password': '',
            'passwordconfirm': '',
            'mode': '',
        }, mailer=DummyMailer)
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.pwdShort), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_nickname_is_taken(self):
        request = testing.DummyRequest(validated={
            'firstname': self.uustring(),
            'lastname': self.uustring(),
            'nickname': 'Tobias',
            'email': self.uustring() + '@hhu.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'mode': 'manually',
        }, mailer=DummyMailer)
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.nickIsTaken), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_mail_is_taken(self):
        request = testing.DummyRequest(validated={
            'firstname': self.uustring(),
            'lastname': self.uustring(),
            'nickname': self.uustring(),
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'mode': 'manually',
        }, mailer=DummyMailer)
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)

        self.assertEqual(self._tn.get(_.mailIsTaken), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_mail_invalid(self):
        request = testing.DummyRequest(validated={
            'firstname': self.uustring(),
            'lastname': self.uustring(),
            'nickname': self.uustring(),
            'email': 'nota@validhost',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'mode': 'manually',
        }, mailer=DummyMailer)
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.mailNotValid), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_passwords_not_equal(self):
        request = testing.DummyRequest(validated={
            'firstname': 'Bob',
            'lastname': 'Builder',
            'nickname': 'Builder',
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': self.uustring(),
            'passwordconfirm': self.uustring(),
            'mode': 'manually',
        }, mailer=DummyMailer)
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.pwdNotEqual), msg)
        self.assertIsNone(db_new_user)

    def test_login_oauth_user(self):
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
            request = testing.DummyRequest(params={'application_url': 'http://lvh.me'}, environ=environ)
            request.environ = environ
            resp = login_oauth_user(request, service, redirect_uri, redirect_uri, ui_locales)
            if len(service) > 0:
                self.assertIsNotNone(resp)
            else:
                self.assertIsNone(resp)
