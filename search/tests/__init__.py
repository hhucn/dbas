from dbas.tests.utils import TestCaseWithDatabase


def setup_package():
    TestCaseWithDatabase().setUpDb()


def teardown_package():
    TestCaseWithDatabase().tearDownTest()
