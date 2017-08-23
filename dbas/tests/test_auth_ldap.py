import unittest

from pyramid import testing
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

from dbas.auth.ldap import verify_ldap_user_data


class AuthLdapTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_verify_ldap_user_data(self):
        registry_settings = {
            'settings:ldap:server': 'ldaps://ldaps.ad.hhu.de',
            'settings:ldap:base': 'ou=IDMUsers,DC=AD,DC=hhu,DC=de',
            'settings:ldap:account.scope': '@ad.hhu.de',
            'settings:ldap:account.filter': 'sAMAccountName',
            'settings:ldap:account.firstname': 'givenName',
            'settings:ldap:account.lastname': 'sn',
            'settings:ldap:account.title': 'personalTitle',
            'settings:ldap:account.email': 'mail'
        }
        nickname = 'Bob'
        password = 'iamatestuser2016'
        _tn = Translator('en')
        response = verify_ldap_user_data(registry_settings, nickname, password, _tn)
        self.assertTrue(response['error'] in [_tn.get(_.serviceNotAvailable) + '. ' + _tn.get(_.pleaseTryAgainLaterOrContactUs),
                                              _tn.get(_.userPasswordNotMatch)])
