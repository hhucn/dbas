import unittest

from pyramid import testing

from dbas.helper.tests import verify_dictionary_of_view


class MainMyDiscussionViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_mydiscussions as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        self.assertIn('layout', response)
        self.assertIn('language', response)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('issues', response)


class MainMyDiscussionViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_mydiscussions as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(self, response)

        self.assertIn('layout', response)
        self.assertIn('language', response)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('issues', response)
