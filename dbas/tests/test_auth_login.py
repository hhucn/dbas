import unittest

from pyramid.httpexceptions import HTTPFound
from pyramid import testing
from dbas.auth.login import login_user, register_with_ajax_data
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _


class AuthLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_login_user(self):
        nickname = 'Bob'
        password = 'iamatestuser2016'
        for_api = False
        keep_login = 'true'

        request = testing.DummyRequest(params={
            'user': nickname,
            'password': password,
            'keep_login': keep_login,
            'url': 'http://some.url'
        }, matchdict={})
        _tn = Translator('en')
        response = login_user(request, '', '', for_api, '', _tn)
        self.assertTrue(type(response) is HTTPFound)

        response = login_user(request, nickname, password, for_api, keep_login, _tn)
        self.assertTrue(type(response) is HTTPFound)

        for_api = True
        response = login_user(request, nickname, password, for_api, keep_login, _tn)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
        self.assertEqual(_tn.get(_.mailNotValid), msg)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
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
        }, matchdict={})
        success, msg, db_new_user = register_with_ajax_data(request)
        self.assertEqual(_tn.get(_.maliciousAntiSpam), msg)
        self.assertIsNone(db_new_user)
