import os
import webtest
from nose.tools import assert_is_not_none

import dbas
from api.lib import json_to_dict
from dbas.helper.test import add_settings_to_appconfig

API = "http://localhost:4284/api/v2/"


def get_testapp():
    settings = add_settings_to_appconfig()
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'development.ini'))
    app = dbas.main({'__file__': file}, **settings)
    return webtest.TestApp(app)


def graphql_query(query) -> dict:
    url = '{}query?q={}'.format(API, query)
    response = get_testapp().get(url, status=200)
    ret = json_to_dict(response.body)
    assert_is_not_none(ret)
    return ret
