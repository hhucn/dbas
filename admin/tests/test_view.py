import unittest

from pyramid import testing


class AdminViewTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_main_admin_no_author(self):
        from admin.views import main_admin
        request = testing.DummyRequest()
        response = main_admin(request)
        self.assertEqual(400, response.status_code)

    def test_main_admin(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from admin.views import main_admin
        request = testing.DummyRequest()
        response = main_admin(request)
        self.assertIn('layout', response)
        self.assertIn('language', response)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('dashboard', response)

    def test_main_table_no_author(self):
        from admin.views import main_table
        request = testing.DummyRequest()
        response = main_table(request)
        self.assertEqual(400, response.status_code)

    def test_main_table_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from admin.views import main_table
        request = testing.DummyRequest(matchdict={'table': 'fu'})
        response = main_table(request)
        self.assertEqual(400, response.status_code)

    def test_main_table(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from admin.views import main_table
        request = testing.DummyRequest(matchdict={'table': 'User'})
        response = main_table(request)
        self.assertIn('layout', response)
        self.assertIn('language', response)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
