import os

import webtest

import dbas
from dbas.helper.test import add_settings_to_appconfig
from dbas.tests.utils import TestCaseWithDatabase

settings = add_settings_to_appconfig()
file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'development.ini'))
app = webtest.TestApp(dbas.main({'__file__': file}, **settings))


def setup_package():
    TestCaseWithDatabase().setUp()


def teardown_package():
    TestCaseWithDatabase().tearDown()
