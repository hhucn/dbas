import unittest
import transaction

from .views import Dbas
from pyramid import testing
#from pyramid_mailer import get_mailer
from dbas.database.model import DBSession, Group, User, Argument, RelationArgPos, RelationArgArg, Position, Base

def _registerRoutes(config):
	'''
	Registers all views, which are in __init__
	:param config:
	:return:
	'''
	config.add_route('main_page', '/')
	config.add_route('main_login', '/login')
	config.add_route('main_logout', '/logout')
	config.add_route('main_contact', '/contact')
	config.add_route('main_content', '/content')
	config.add_route('main_impressum', '/impressum')

def _initTestingDB():
	from sqlalchemy import create_engine
	#engine = create_engine('sqlite://')
	#Base.metadata.create_all(engine)
	#DBSession.configure(bind=engine)
	with transaction.manager:
		group1 = Group(name='editor')
		group2 = Group(name='user')
		DBSession.add(group1)
		DBSession.add(group2)
		DBSession.flush()

		user1 = User(firstname='editor', surename='editor', nickname='editor', email='nope1@nopeville.com', password='test')
		user2 = User(firstname='user', surename='user', nickname='user', email='nope2@nopeville.com', password='test')
		user1.group = group1.uid
		user2.group = group2.uid
		DBSession.add(user1)

		position1 = Position(text='I like cats.', weight='100')
		position2 = Position(text='I like dogs.', weight='20')
		position1.author = user1.uid
		position2.author = user1.uid
		DBSession.add(position1)
		DBSession.add(position2)
		DBSession.flush()

		argument1 = Argument(text='They are hating all humans!', weight='70')
		argument2 = Argument(text='They are very devoted.', weight='80')
		argument1.author = user1.uid
		argument2.author = user2.uid
		DBSession.add(argument2)
		DBSession.flush()

		relation1 = RelationArgPos(weight='134', is_supportive='1')
		relation2 = RelationArgPos(weight='34', is_supportive='1')
		relation3 = RelationArgArg(weight='14', is_supportive='0')
		relation1.author = user1.uid
		relation2.author = user1.uid
		relation3.author = user2.uid
		relation1.pos_uid = argument1.uid
		relation2.pos_uid = argument2.uid
		relation3.arg_uid1 = argument1.uid
		relation1.arg_uid = argument1.uid
		relation2.arg_uid = argument2.uid
		relation3.arg_uid2 = argument2.uid
		DBSession.add(argument1)
		DBSession.add(relation1)
		DBSession.add(relation2)
		DBSession.add(relation3)
		DBSession.flush()
		transaction.commit
	return DBSession

#testing main page
class ViewMainTests(unittest.TestCase):
	def setUp(self):
		print("ViewMainTests: test_logout")
		self.config = testing.setUp()

	def tearDown(self):
		print("ViewLoginTests: _callFUT")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewLoginTests: tearDown")
		from dbas.views import main_page
		return main_page(request)

	def test_main(self):
		print("ViewLoginTests: setUp")
		request = testing.DummyRequest()
		response = Dbas(request).main_page()
		self.assertEqual('Main', response['title'])

# testing login page
class ViewLoginTests(unittest.TestCase):
	def setUp(self):
		print("ViewLoginTests: test_logout")
		self.config = testing.setUp()
		_registerRoutes(self.config)

	def tearDown(self):
		print("ViewMainTests: _callFUT")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewMainTests: tearDown")
		from dbas.views import main_login
		return main_login(request)

	def test_login(self):
		print("ViewMainTests: setUp")
		request = testing.DummyRequest()
		inst = Dbas(request)
		response = Dbas(request).main_login()
		self.assertEqual('Login', response['title'])

# testing logout page
class ViewLogoutTests(unittest.TestCase):
	def setUp(self):
		print("ViewLogoutTests: setUp")
		self.config = testing.setUp()
		_registerRoutes(self.config)

	def tearDown(self):
		print("ViewLogoutTests: tearDown")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewLogoutTests: _callFUT")
		from dbas.views import main_logout
		return main_logout(request)

	def test_logout(self):
		print("ViewLogoutTests: test_logout")
		request = testing.DummyRequest()
		response = Dbas(request).main_logout()
		self.assertEqual('Logout', response['title'])

# testing logout redirection page
class ViewLogoutRedirectTests(unittest.TestCase):
	def setUp(self):
		print("ViewLogoutRedirectTests: test_logout")
		self.config = testing.setUp()
		_registerRoutes(self.config)

	def tearDown(self):
		print("ViewLogoutRedirectTests: _callFUT")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewLogoutRedirectTests: tearDown")
		from dbas.views import main_logout_redirect
		return main_logout_redirect(request)

	def test_logout_redirect(self):
		print("ViewLogoutRedirectTests: setUp")
		request = testing.DummyRequest()
		inst = Dbas(request)
		response = Dbas(request).main_logout_redirect()
		# do NOT follow HTTPFound with webtest
		# therefore we have function testings
		self.assertEqual(response.status, '302 Found')

# testing contact page
class ViewContactTests(unittest.TestCase):
	def setUp(self):
		print("ViewContactTests: setUp")
		self.config = testing.setUp()

	def tearDown(self):
		print("ViewContactTests: tearDown")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewContactTests: _callFUT")
		from dbas.views import main_contact
		return main_contact(request)

	def test_contact(self):
		print("ViewContactTests: test_logout")
		request = testing.DummyRequest()
		response = Dbas(request).main_contact()
		self.assertEqual('Contact', response['title'])

# testing content page
class ViewContentTests(unittest.TestCase):
	def setUp(self):
		print("ViewContentTests: setUp")
		self.config = testing.setUp()

	def tearDown(self):
		print("ViewContentTests: tearDown")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewContentTests: _callFUT")
		from dbas.views import main_content
		return main_content(request)

	def test_content(self):
		print("ViewContentTests: test_logout")
		request = testing.DummyRequest()
		response = Dbas(request).main_content()
		self.assertEqual('Content', response['title'])

# testing impressum page
class ViewImpressumTests(unittest.TestCase):
	def setUp(self):
		print("ViewImpressumTests: test_logout")
		self.config = testing.setUp()

	def tearDown(self):
		print("ViewImpressumTests: _callFUT")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewImpressumTests: tearDown")
		from dbas.views import main_impressum
		return main_impressum(request)

	def test_impressum(self):
		print("ViewImpressumTests: setUp")
		request = testing.DummyRequest()
		response = Dbas(request).main_impressum()
		self.assertEqual('Impressum', response['title'])

# testing a unexisting page
class ViewNotFoundTests(unittest.TestCase):
	def setUp(self):
		print("ViewNotFoundTests: test_logout")
		self.config = testing.setUp()

	def tearDown(self):
		print("ViewNotFoundTests: _callFUT")
		testing.tearDown()

	def _callFUT(self, request):
		print("ViewNotFoundTests: tearDown")
		from dbas.views import notfound
		return notfound(request)

	def test_main(self):
		print("ViewNotFoundTests: setUp")
		request = testing.DummyRequest()
		response = Dbas(request).notfound()
		self.assertEqual('Error', response['title'])

# check, if every site responds with 200 except the error page
class FunctionalTests(unittest.TestCase):

	editor_login	   = '/login?nickname=editor&password=test&came_from=main_page&form.login.submitted=Login'
	user_login		   = '/login?nickname=user&password=test&came_from=main_page&form.login.submitted=Login'
	viewer_wrong_login = '/login?nickname=viewer&password=incorrect&came_from=main_page&form.login.submitted=Login'

	def setUp(self):
		print("FunctionalTests: setUp")
		from dbas import main
		settings = {'sqlalchemy.url': 'sqlite://', 'pyramid.includes' : 'pyramid_mailer.testing'}
		app = main({}, **settings)
		from webtest import TestApp
		self.testapp = TestApp(app)
		_initTestingDB()

	def tearDown(self):
		print("FunctionalTests: tearDown")
		from dbas.database import DBSession
		DBSession.remove()
		testing.tearDown()

	# testing main page
	def test_home(self):
		print("FunctionalTests: test_home")
		res = self.testapp.get('/', status=200)
		self.assertIn(b'<h2><span class="font-semi-bold">Welcome', res.body)

	# testing contact page
	def test_contact(self):
		print("FunctionalTests: test_contact")
		res = self.testapp.get('/contact', status=200)
		self.assertIn(b'<div class="contact">', res.body)

	# testing login page
	def test_login_when_logged_out(self):
		print("FunctionalTests: test_login_when_logged_out")
		res = self.testapp.get('/login', status=200)
		self.assertIn(b'<a href="#signup">Sign Up', res.body)
		self.assertIn(b'<h2>Welcome Back', res.body)

	# testing logout page without login
	def test_logout_when_logged_out(self):
		print("FunctionalTests: test_logout_when_logged_out")
		res = self.testapp.get('/logout', status=200)
		self.assertNotIn(b'You will be logged out and redirected', res.body)

	# testing logout page without login
	def logout_redirect_when_logged_out(self):
		print("FunctionalTests: logout_redirect_when_logged_out")
		res = self.testapp.get('/logout_redirect', status=302)
		self.assertIn(b'You will be logged out and redirected', res.body)

	# testing content page
	def test_content(self):
		print("FunctionalTests: test_content")
		res = self.testapp.get('/content', status=200)
		self.assertNotIn(b'Carousel', res.body) # due to login error

	# testing contact page
	def test_impressum(self):
		print("FunctionalTests: test_impressum")
		res = self.testapp.get('/impressum', status=200)
		self.assertIn(b'Impressum', res.body)

	# testing a unexisting page
	def test_unexisting_page(self):
		print("FunctionalTests: test_unexisting_page")
		res = self.testapp.get('/SomePageYouWontFind', status=404)
		self.assertIn(b'404 Error', res.body)
		self.assertIn(b'SomePageYouWontFind', res.body)

	# testing successful log in
	def test_successful_log_in(self):
		print("FunctionalTests: test_successful_log_in")
		res = self.testapp.get(self.editor_login, status=302)
		self.assertEqual(res.location, 'http://localhost/content')
		self.testapp.get('/', status=200)

	# testing failed log in
	def test_failed_log_in(self):
		print("FunctionalTests: test_failed_log_in")
		res = self.testapp.get(self.viewer_wrong_login, status=200)
		self.assertTrue(b'User does not exists' in res.body)

	# testing successful log in
	def test_redirection_when_logged_in(self):
		print("FunctionalTests: test_redirection_when_logged_in")
		res = self.testapp.get(self.editor_login, status=302)
		self.assertEqual(res.location, 'http://localhost/content')
		res = self.testapp.get('/login', status=302)

	# testing wheather the login link is there, when we are logged in
	def test_logout_link_present_when_logged_in(self):
		print("FunctionalTests: test_logout_link_present_when_logged_in")
		self.testapp.get(self.editor_login, status=302)
		res = self.testapp.get('/', status=200)
		self.assertTrue(b'Logout' in res.body)

	# testing wheather the logout link is there, when we are logged out
	def test_logout_link_not_present_after_logged_out(self):
		print("FunctionalTests: test_logout_link_not_present_after_logged_out")
		self.testapp.get(self.editor_login, status=302)
		self.testapp.get('/', status=200)
		res = self.testapp.get('/logout_redirect', status=302)
		self.assertTrue(b'Logout' not in res.body)

	# testing the email
	def test_email(self):
		print("FunctionalTests: test_email")
		self.res = self.testapp.get('/contact', status=200)
		self.registry = self.testapp.app.registry
#		self.mailer = get_mailer(self.registry)
#		self.assertEqual(len(self.mailer.outbox), 1)
#		self.assertEqual(self.mailer.outbox[0].subject, "hello world")
#		self.assertEqual(len(self.mailer.queue), 1)
#		self.assertEqual(self.mailer.queue[0].subject, "hello world")


class DatabaseTests(unittest.TestCase):

	def setUp(self):
		print("DatabaseTests: setUp")
		from dbas import main
		settings = {'sqlalchemy.url': 'sqlite://', 'pyramid.includes' : 'pyramid_mailer.testing'}
		app = main({}, **settings)
		from webtest import TestApp
		self.testapp = TestApp(app)
		_initTestingDB()

	def tearDown(self):
		print("DatabaseTests: tearDown")
		from dbas.database import DBSession
		DBSession.remove()
		testing.tearDown()

	def test_database_content(self):
		print("DatabaseTests: test_database_content")
		#group1 = DBSession.query(Group).filter_by(uid=1)
		#group2 = DBSession.query(Group).filter_by(uid=2)
		#self.assertTrue(b'editor' in group1.name)
		#self.assertTrue(b'user' in group2.name)



#	def test_anonymous_user_cannot_edit(self):
#		res = self.testapp.get('/FrontPage/edit_page', status=200)
#		self.assertTrue(b'Login' in res.body)

#	def test_anonymous_user_cannot_add(self):
#		res = self.testapp.get('/add_page/NewPage', status=200)
#		self.assertTrue(b'Login' in res.body)

#	def test_viewer_user_cannot_edit(self):
#		self.testapp.get(self.editor_login, status=302)
#		res = self.testapp.get('/FrontPage/edit_page', status=200)
#		self.assertTrue(b'Login' in res.body)

#	def test_viewer_user_cannot_add(self):
#		self.testapp.get(self.editor_login, status=302)
#		res = self.testapp.get('/add_page/NewPage', status=200)
#		self.assertTrue(b'Login' in res.body)

#	def test_editors_member_user_can_edit(self):
#		self.testapp.get(self.editor_login, status=302)
#		res = self.testapp.get('/FrontPage/edit_page', status=200)
#		self.assertTrue(b'Editing' in res.body)

#	def test_editors_member_user_can_add(self):
#		self.testapp.get(self.editor_login, status=302)
#		res = self.testapp.get('/add_page/NewPage', status=200)
#		self.assertTrue(b'Editing' in res.body)

#	def test_editors_member_user_can_view(self):
#		self.testapp.get(self.editor_login, status=302)
#		res = self.testapp.get('/FrontPage', status=200)
#		self.assertTrue(b'FrontPage' in res.body)
