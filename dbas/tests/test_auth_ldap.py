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
        import os

        os.environ['DBAS_HHU_LDAP_SERVER'] = 'ldaps://ldaps.ad.hhu.de'
        os.environ['DBAS_HHU_LDAP_BASE'] = 'ou=IDMUsers,DC=AD,DC=hhu,DC=de'
        os.environ['DBAS_HHU_LDAP_ACCOUNT_SCOPE'] = '@ad.hhu.de'
        os.environ['DBAS_HHU_LDAP_ACCOUNT_FILTER'] = 'sAMAccountName'
        os.environ['DBAS_HHU_LDAP_ACCOUNT_FIRSTNAME'] = 'givenName'
        os.environ['DBAS_HHU_LDAP_ACCOUNT_LAST'] = 'sn'
        os.environ['DBAS_HHU_LDAP_ACCOUNT_TITLE'] = 'personalTitle'
        os.environ['DBAS_HHU_LDAP_ACCOUNT_EMAIL'] = 'mail'

        nickname = 'Bob'
        password = 'iamatestuser2016'
        _tn = Translator('en')
        response = verify_ldap_user_data(nickname, password, _tn)
        self.assertTrue(response['error'] in [_tn.get(_.serviceNotAvailable) + '. ' + _tn.get(_.pleaseTryAgainLaterOrContactUs),
                                              _tn.get(_.userPasswordNotMatch)])
