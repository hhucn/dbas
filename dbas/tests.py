import unittest

from pyramid import testing

def _registerRoutes(config):
    config.add_route('main_page', '/')
    config.add_route('main_login', '/login')
    config.add_route('main_logout', '/logout')
    config.add_route('main_contact', '/contact')
    config.add_route('main_content', '/content')
    config.add_route('main_impressum', '/impressum')

#testing main page
class ViewMainTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from dbas.views import main_page
        return view_page(request)

    def test_main(self):
        from .views import Prototype
        request = testing.DummyRequest()
        inst = Prototype(request)
        response = inst.main_page()
        self.assertEqual('Main', response['title'])

# testing login page
#class ViewLoginTests(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#
#    def tearDown(self):
#        testing.tearDown()
#
#    def _callFUT(self, request):
#        from dbas.views import main_login
#        return view_page(request)
#
#    def test_login(self):
#        from .views import Prototype
#        request = testing.DummyRequest()
#        inst = Prototype(request)
#        response = inst.main_login()
#        self.assertEqual('Login', response['title'])

# testing logout page
#class ViewLogoutTests(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#
#    def tearDown(self):
#        testing.tearDown()
#
#    def _callFUT(self, request):
#        from dbas.views import main_logout
#        return view_page(request)
#
#    def test_logout(self):
#        from .views import Prototype
#        request = testing.DummyRequest()
#        inst = Prototype(request)
#        response = inst.main_logout()
#        self.assertEqual('Logout', response['title'])


# testing logout redirection page
class ViewLogoutRedirectTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from dbas.views import main_logout_redirect
        return view_page(request)

    def test_logout(self):
        from .views import Prototype
        request = testing.DummyRequest()
        inst = Prototype(request)
        response = inst.main_logout_redirect()
        self.assertEqual('Logout', response['title'])

# testing contact page
class ViewContactTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from dbas.views import main_contact
        return view_page(request)

    def test_contact(self):
        from .views import Prototype
        request = testing.DummyRequest()
        inst = Prototype(request)
        response = inst.main_contact()
        self.assertEqual('Contact', response['title'])

# testing content page
class ViewContentTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from dbas.views import main_content
        return view_page(request)

    def test_content(self):
        from .views import Prototype
        request = testing.DummyRequest()
        inst = Prototype(request)
        response = inst.main_content()
        self.assertEqual('Content', response['title'])

# testing impressum page
class ViewImpressumTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from dbas.views import main_impressum
        return view_page(request)

    def test_impressum(self):
        from .views import Prototype
        request = testing.DummyRequest()
        inst = Prototype(request)
        response = inst.main_impressum()
        self.assertEqual('Impressum', response['title'])

# testing a unexisting page
class ViewNotFoundTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from dbas.views import notfound
        return view_page(request)

    def test_main(self):
        from .views import Prototype
        request = testing.DummyRequest()
        inst = Prototype(request)
        response = inst.notfound()
        self.assertEqual('Error', response['title'])

# check, if every site responds with 200 except the error page
class FunctionalTests(unittest.TestCase):

    viewer_login       = '/login?login=viewer&password=viewer&came_from=main_page&form.login.submitted=Login'
    editor_login       = '/login?login=editor&password=editor&came_from=main_page&form.login.submitted=Login'
    user_login         = '/login?login=user&password=user&came_from=main_page&form.login.submitted=Login'
    viewer_wrong_login = '/login?login=viewer&password=incorrect&came_from=main_page&form.login.submitted=Login'

    def setUp(self):
        from dbas import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        testing.tearDown()

    # testing main page
    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h2><span class="font-semi-bold">Welcome', res.body)

    # testing contact page
    def test_contact(self):
        res = self.testapp.get('/contact', status=200)
        self.assertIn(b'<div class="contact">', res.body)

    # testing login page
    def test_login(self):
        res = self.testapp.get('/login', status=200)
        self.assertIn(b'<a href="#signup">Sign Up', res.body)
        self.assertIn(b'<h2>Welcome Back', res.body)

    # testing logout page without login
    def test_logout(self):
        res = self.testapp.get('/logout', status=302)
        self.assertNotIn(b'You will be logged out and redirected', res.body)

    # testing logout page without login
    def test_logout(self):
        res = self.testapp.get('/logout_redirect', status=200)
        self.assertNotIn(b'You will be logged out and redirected', res.body)

# LOGIN FAILES
    # testing content page
    def test_content(self):
        res = self.testapp.get('/content', status=200)
        self.assertNotIn(b'Carousel', res.body) # due to login error

    # testing contact page
    def test_impressum(self):
        res = self.testapp.get('/impressum', status=200)
        self.assertIn(b'Impressum', res.body)

    # testing a unexisting page
    def test_unexisting_page(self):
        res = self.testapp.get('/SomePageYouWontFind', status=404)
        self.assertIn(b'404 Error', res.body)
        self.assertIn(b'SomePageYouWontFind', res.body)

    def test_successful_log_in(self):
        res = self.testapp.get(self.viewer_login, status=302)
        self.assertEqual(res.location, 'http://localhost/content')

    def test_failed_log_in(self):
        res = self.testapp.get(self.viewer_wrong_login, status=200)
        self.assertTrue(b'login' in res.body)

    def test_logout_link_present_when_logged_in(self):
        self.testapp.get(self.viewer_login, status=302)
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Logout' in res.body)

    def test_logout_link_not_present_after_logged_out(self):
        self.testapp.get(self.viewer_login, status=302)
        self.testapp.get('/', status=200)
        res = self.testapp.get('/logout', status=302)
        self.assertTrue(b'Logout' not in res.body)

#    def test_anonymous_user_cannot_edit(self):
#        res = self.testapp.get('/FrontPage/edit_page', status=200)
#        self.assertTrue(b'Login' in res.body)

#    def test_anonymous_user_cannot_add(self):
#        res = self.testapp.get('/add_page/NewPage', status=200)
#        self.assertTrue(b'Login' in res.body)

#    def test_viewer_user_cannot_edit(self):
#        self.testapp.get(self.viewer_login, status=302)
#        res = self.testapp.get('/FrontPage/edit_page', status=200)
#        self.assertTrue(b'Login' in res.body)

#    def test_viewer_user_cannot_add(self):
#        self.testapp.get(self.viewer_login, status=302)
#        res = self.testapp.get('/add_page/NewPage', status=200)
#        self.assertTrue(b'Login' in res.body)

#    def test_editors_member_user_can_edit(self):
#        self.testapp.get(self.editor_login, status=302)
#        res = self.testapp.get('/FrontPage/edit_page', status=200)
#        self.assertTrue(b'Editing' in res.body)

#    def test_editors_member_user_can_add(self):
#        self.testapp.get(self.editor_login, status=302)
#        res = self.testapp.get('/add_page/NewPage', status=200)
#        self.assertTrue(b'Editing' in res.body)

#    def test_editors_member_user_can_view(self):
#        self.testapp.get(self.editor_login, status=302)
#        res = self.testapp.get('/FrontPage', status=200)
#        self.assertTrue(b'FrontPage' in res.body)
