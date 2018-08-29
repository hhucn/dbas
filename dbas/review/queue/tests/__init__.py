from dbas.tests.utils import TestCaseWithDatabase


def setup_package():
    TestCaseWithDatabase().setUp()


def teardown_package():
    TestCaseWithDatabase().tearDown()
