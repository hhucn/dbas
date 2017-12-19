import unittest

from pyramid import testing

from graph.views import get_d3_complete_dump, get_d3_partial_dump

# copy/paste from https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/tests.html


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_get_d3_complete_dump(self):
        request = testing.DummyRequest()
        ret_dict = get_d3_partial_dump(request)
        self.assertIsNotNone(ret_dict)

    def test_get_d3_partial_dump(self):
        request = testing.DummyRequest()
        ret_dict = get_d3_complete_dump(request)
        self.assertIsNotNone(ret_dict)
