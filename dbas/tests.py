import unittest

from pyramid import testing


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


class ViewLoginTests(unittest.TestCase):
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


class ViewContactTests(unittest.TestCase):
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


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from dbas import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h2><span class="font-semi-bold">Welcome', res.body)

    def test_contact(self):
        res = self.testapp.get('/contact', status=200)
        self.assertIn(b'<div class="contact">', res.body)

    def test_login(self):
        res = self.testapp.get('/login', status=200)
        self.assertIn(b'<a href="#signup">Sign Up', res.body)
        self.assertIn(b'<h2>Welcome Back', res.body)

    def test_unexisting_page(self):
        res = self.testapp.get('/SomePage', status=404)
        self.assertIn(b'The page you are looking for could not be found.', res.body)

#
# WIKI2
#
#class FunctionalTests(unittest.TestCase):
#
#    viewer_login = '/login?login=viewer&password=viewer' \
#                   '&came_from=FrontPage&form.submitted=Login'
#    viewer_wrong_login = '/login?login=viewer&password=incorrect' \
#                   '&came_from=FrontPage&form.submitted=Login'
#    editor_login = '/login?login=editor&password=editor' \
#                   '&came_from=FrontPage&form.submitted=Login'
#
#    def setUp(self):
#        from tutorial import main
#        settings = { 'sqlalchemy.url': 'sqlite://'}
#        app = main({}, **settings)
#        from webtest import TestApp
#        self.testapp = TestApp(app)
#        _initTestingDB()
#
#    def tearDown(self):
#        del self.testapp
#        from tutorial.models import DBSession
#        DBSession.remove()
#
#    def test_root(self):
#        res = self.testapp.get('/', status=302)
#        self.assertEqual(res.location, 'http://localhost/FrontPage')
#
#    def test_FrontPage(self):
#        res = self.testapp.get('/FrontPage', status=200)
#        self.assertTrue(b'FrontPage' in res.body)
#
#    def test_unexisting_page(self):
#        self.testapp.get('/SomePage', status=404)
#
#    def test_successful_log_in(self):
#        res = self.testapp.get(self.viewer_login, status=302)
#        self.assertEqual(res.location, 'http://localhost/FrontPage')
#
#    def test_failed_log_in(self):
#        res = self.testapp.get(self.viewer_wrong_login, status=200)
#        self.assertTrue(b'login' in res.body)
#
#    def test_logout_link_present_when_logged_in(self):
#        self.testapp.get(self.viewer_login, status=302)
#        res = self.testapp.get('/FrontPage', status=200)
#        self.assertTrue(b'Logout' in res.body)
#
#    def test_logout_link_not_present_after_logged_out(self):
#        self.testapp.get(self.viewer_login, status=302)
#        self.testapp.get('/FrontPage', status=200)
#        res = self.testapp.get('/logout', status=302)
#        self.assertTrue(b'Logout' not in res.body)
#
#    def test_anonymous_user_cannot_edit(self):
#        res = self.testapp.get('/FrontPage/edit_page', status=200)
#        self.assertTrue(b'Login' in res.body)
#
#    def test_anonymous_user_cannot_add(self):
#        res = self.testapp.get('/add_page/NewPage', status=200)
#        self.assertTrue(b'Login' in res.body)
#
#    def test_viewer_user_cannot_edit(self):
#        self.testapp.get(self.viewer_login, status=302)
#        res = self.testapp.get('/FrontPage/edit_page', status=200)
#        self.assertTrue(b'Login' in res.body)
#
#    def test_viewer_user_cannot_add(self):
#        self.testapp.get(self.viewer_login, status=302)
#        res = self.testapp.get('/add_page/NewPage', status=200)
#        self.assertTrue(b'Login' in res.body)
#
#    def test_editors_member_user_can_edit(self):
#        self.testapp.get(self.editor_login, status=302)
#        res = self.testapp.get('/FrontPage/edit_page', status=200)
#        self.assertTrue(b'Editing' in res.body)
#
#    def test_editors_member_user_can_add(self):
#        self.testapp.get(self.editor_login, status=302)
#        res = self.testapp.get('/add_page/NewPage', status=200)
#        self.assertTrue(b'Editing' in res.body)
#
#    def test_editors_member_user_can_view(self):
#        self.testapp.get(self.editor_login, status=302)
#        res = self.testapp.get('/FrontPage', status=200)
#        self.assertTrue(b'FrontPage' in res.body)
