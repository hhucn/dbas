import webtest
import dbas
import os

from nose.tools import assert_is_not_none

from api.lib import json_to_dict
from dbas.helper.tests import add_settings_to_appconfig

API = "http://localhost:4284/api/v2/"


def get_testapp():
    settings = add_settings_to_appconfig()
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'development.ini'))
    app = dbas.main({'__file__': file}, **settings)
    return webtest.TestApp(app)


def graphql_query(query) -> dict:
    url = '{}query?q={}'.format(API, query)
    response = get_testapp().get(url, status=200, extra_environ=dict(DBAS_HHU_LDAP_SERVER='ldaps://ldaps.ad.hhu.de',
                                                                     DBAS_HHU_LDAP_BASE='ou=IDMUsers,DC=AD,DC=hhu,DC=de',
                                                                     DBAS_HHU_LDAP_ACCOUNT_SCOPE='@ad.hhu.de',
                                                                     DBAS_HHU_LDAP_ACCOUNT_FILTER='sAMAccountName',
                                                                     DBAS_HHU_LDAP_ACCOUNT_FIRSTNAME='givenName',
                                                                     DBAS_HHU_LDAP_ACCOUNT_LAST='sn',
                                                                     DBAS_HHU_LDAP_ACCOUNT_TITLE='personalTitle',
                                                                     DBAS_HHU_LDAP_ACCOUNT_EMAIL='mail'))
    ret = json_to_dict(response.body)
    assert_is_not_none(ret)
    return ret
