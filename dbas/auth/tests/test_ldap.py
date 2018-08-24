import os

from dbas.auth.ldap import verify_ldap_user_data
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class AuthLdapTest(TestCaseWithConfig):
    def test_verify_ldap_user_data(self):
        os.environ['HHU_LDAP_SERVER'] = 'ldaps://ldaps.ad.hhu.de'
        os.environ['HHU_LDAP_BASE'] = 'ou=IDMUsers,DC=AD,DC=hhu,DC=de'
        os.environ['HHU_LDAP_ACCOUNT_SCOPE'] = '@ad.hhu.de'
        os.environ['HHU_LDAP_ACCOUNT_FILTER'] = 'sAMAccountName'
        os.environ['HHU_LDAP_ACCOUNT_FIRSTNAME'] = 'givenName'
        os.environ['HHU_LDAP_ACCOUNT_LAST'] = 'sn'
        os.environ['HHU_LDAP_ACCOUNT_TITLE'] = 'personalTitle'
        os.environ['HHU_LDAP_ACCOUNT_EMAIL'] = 'mail'

        nickname = 'Bob'
        password = 'iamatestuser2016'
        _tn = Translator('en')
        response = verify_ldap_user_data(nickname, password, _tn)
        self.assertTrue(
            response['error'] in [_tn.get(_.serviceNotAvailable) + '. ' + _tn.get(_.pleaseTryAgainLaterOrContactUs),
                                  _tn.get(_.userPasswordNotMatch)])
