# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer.mailer import DummyMailer
from uuid import uuid4

from dbas.auth.login import login_local_user, register_user_with_json_data
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request
from dbas.views import user_login


class AuthLoginTest(TestCaseWithConfig):
    @staticmethod
    def uustring():
        """
        Create instance-unique strings to avoid clashes with pre-seeded database.

        :return: Stringified uuid
        :rtype: str
        """
        return str(uuid4())

    def setUp(self):
        super().setUp()
        self._tn = Translator('en')

    def test_login_user(self):
        nickname = 'Bob'
        password = 'iamatestuser2016'
        keep_login = True

        request = construct_dummy_request(json_body={
            'user': nickname,
            'password': password,
            'keep_login': keep_login,
            'redirect_url': 'http://some.url'
        })

        _tn = Translator('en')
        response = user_login(request)
        self.assertTrue(type(response) is HTTPFound)

        response = login_local_user(nickname, password, DummyMailer, lang=_tn)
        self.assertTrue(isinstance(response, dict))
        self.assertNotIn('error', response)
        self.assertIn('user', response)

        response = login_local_user('definitelynotauser', r'¯\_(ツ)_/¯', DummyMailer, lang=_tn)
        self.assertTrue(isinstance(response, dict))
        self.assertIn('error', response)
        self.assertNotIn('user', response)

    def test_login_register_with_json_data(self):
        request = construct_dummy_request(validated={
            'firstname': '',
            'lastname': '',
            'nickname': '',
            'email': ' ',
            'gender': '',
            'password': '',
            'passwordconfirm': '',
            'mode': '',
        })
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.checkFirstname), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_nickname_is_taken(self):
        request = construct_dummy_request(validated={
            'firstname': self.uustring(),
            'lastname': self.uustring(),
            'nickname': 'Tobias',
            'email': self.uustring() + '@hhu.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'mode': 'manually',
        })
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.nickIsTaken), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_mail_is_taken(self):
        request = construct_dummy_request(validated={
            'firstname': self.uustring(),
            'lastname': self.uustring(),
            'nickname': self.uustring(),
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'mode': 'manually',
        })
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)

        self.assertEqual(self._tn.get(_.mailIsTaken), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_mail_invalid(self):
        request = construct_dummy_request(validated={
            'firstname': self.uustring(),
            'lastname': self.uustring(),
            'nickname': self.uustring(),
            'email': 'nota@validhost',
            'gender': 'm',
            'password': 'somepasswd',
            'passwordconfirm': 'somepasswd',
            'mode': 'manually',
        })
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.mailNotValid), msg)
        self.assertIsNone(db_new_user)

    def test_register_user_passwords_not_equal(self):
        request = construct_dummy_request(validated={
            'firstname': 'Bob',
            'lastname': 'Builder',
            'nickname': 'Builder',
            'email': 'krauthoff@cs.uni-duesseldorf.de',
            'gender': 'm',
            'password': self.uustring(),
            'passwordconfirm': self.uustring(),
            'mode': 'manually',
        })
        success, msg, db_new_user = register_user_with_json_data(request.validated, 'en', request.mailer)
        self.assertEqual(self._tn.get(_.pwdNotEqual), msg)
        self.assertIsNone(db_new_user)
