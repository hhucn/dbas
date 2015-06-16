import os
import unittest

# done with the help of: https://gist.github.com/sontek/1420255

from webtest import TestApp
from dbas.views import Dbas
from dbas import main
from dbas.helper import PasswordHandler
from dbas.database import Base as Entity
from dbas.database.model import Group, User, Argument, RelationArgPos, RelationArgArg, RelationPosPos, RelationPosArg, Position
from mock import Mock
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from pyramid_mailer.mailer import DummyMailer
from pyramid_mailer.message import Message
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../', 'development.ini'))


class Setup:
	def __init__(self):
		print("Setup __init__")

	def add_testing_db(self, session):
		group1 = session.query(Group).filter_by(name='editors').first()
		group2 = session.query(Group).filter_by(name='users').first()

		pw1 = PasswordHandler.get_hashed_password(None, 'test')
		pw2 = PasswordHandler.get_hashed_password(None, 'test')
		user1 = User(firstname='editor', surname='editor', nickname='test_editor', email='dbas1@cs.uni-duesseldorf.de', password=pw1)
		user2 = User(firstname='user', surname='user', nickname='test_user', email='dbas2@cs.uni-duesseldorf.de', password=pw2)
		user1.group = group1.uid
		user2.group = group2.uid
		session.add_all([user1, user2])
		session.flush()
		position1 = Position(text='I like cats.', weight=1)
		position2 = Position(text='I like dogs.', weight=2)
		position1.author = user2.uid
		position2.author = user1.uid
		session.add_all([position1, position2])
		session.flush()
		argument1 = Argument(text='They are hating all humans!', weight=1)
		argument2 = Argument(text='They are very devoted.', weight=2)
		argument1.author = user1.uid
		argument2.author = user2.uid
		session.add_all([argument1, argument2])
		session.flush()
		relation1 = RelationArgPos(weight=1, is_supportive=True)
		relation2 = RelationArgPos(weight=2, is_supportive=True)
		relation3 = RelationArgArg(weight=3, is_supportive=False)
		relation4 = RelationPosPos(weight=4, is_supportive=False)
		relation5 = RelationArgArg(weight=5, is_supportive=False)
		relation6 = RelationPosArg(weight=6, is_supportive=False)
		relation1.author = user1.uid
		relation1.arg_uid = argument1.uid
		relation1.pos_uid = position1.uid
		relation2.author = user1.uid
		relation2.arg_uid = argument2.uid
		relation2.pos_uid = position2.uid
		relation3.author = user2.uid
		relation3.arg_uid1 = argument1.uid
		relation3.arg_uid2 = argument2.uid
		relation4.author = user2.uid
		relation4.pos_uid1 = position1.uid
		relation4.pos_uid2 = position2.uid
		relation5.author = user2.uid
		relation5.arg_uid = argument1.uid
		relation5.arg_uid = argument2.uid
		relation6.author = user1.uid
		relation6.pos_uid = position2.uid
		relation6.arg_uid = argument1.uid
		session.add_all([relation1, relation2, relation3, relation4, relation5, relation6])
		session.flush()

		return session

	def add_routes(self, config):
		config.add_route('main_page', '/')
		config.add_route('main_login', '/login')
		config.add_route('main_logout', '/logout')
		config.add_route('main_contact', '/contact')
		config.add_route('main_content', '/content')
		config.add_route('main_news', '/news')
		config.add_route('main_settings', '/settings')
		config.add_route('main_impressum', '/impressum')
		config.add_route('404', '/404')
		return config


# setup the Base testing class what will manage our transactions
class BaseTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
		cls.Session = sessionmaker()

	def setUp(self):
		connection = self.engine.connect()
		# begin a non-ORM transaction
		self.trans = connection.begin()
		# bind an individual Session to the connection
		# Session.configure(bind=connection)
		self.session = self.Session(bind=connection)
		Entity.session = self.session

	def tearDown(self):
		# rollback - everything that happened with the
		#  Session above (including calls to commit())
		#  is rolled back.
		testing.tearDown()
		self.trans.rollback()
		self.session.close()


# skip the routes, templates, etc. So let’s setup our Unit Test Base class
class UnitTestBase(BaseTestCase):
	def setUp(self):
		print("UnitTestBase: setUp")
		self.config = testing.setUp(request=testing.DummyRequest())
		super(UnitTestBase, self).setUp()
		self.config = Setup().add_routes(self.config)

	def tearDown(self):
		print("UnitTestBase: tearDown")
		testing.tearDown()

	def get_csrf_request(self, post=None):
		print("UnitTestBase: get_csrf_request")
		csrf = 'abc'
		if u'csrf_token' not in post.keys():
			post.update({
				'csrf_token': csrf
			})
		request = testing.DummyRequest(post)
		request.session = Mock()
		csrf_token = Mock()
		csrf_token.return_value = csrf
		request.session.get_csrf_token = csrf_token
		return request

# integrate with the whole web framework and actually hit the define routes, render the templates,
# and actually test the full stack of your application


class IntegrationTestBase(BaseTestCase):
	@classmethod
	def setUpClass(cls):
		cls.app = main({}, **settings)
		super(IntegrationTestBase, cls).setUpClass()

	def setUp(self):
		self.testapp = TestApp(self.app)
		self.config = testing.setUp()
		super(IntegrationTestBase, self).setUp()
		self.config = Setup().add_routes(self.config)


##########################################################################################################
##########################################################################################################
##########################################################################################################

# testing main page
class ViewMainTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewLoginTests: _callFUT")
		return Dbas.main_page(request)

	def test_main(self):
		print("ViewLoginTests: test_main")
		request = testing.DummyRequest()
		response = Dbas(request).main_page()
		self.assertEqual('Main', response['title'])


# testing login page
class ViewLoginTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewMainTests: _callFUT")
		return Dbas.main_login(request)

	def test_login(self):
		print("ViewLoginTests: test_login")
		request = testing.DummyRequest()
		response = Dbas(request).main_login()
		self.assertEqual('Login', response['title'])


# testing logout page
class ViewLogoutTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewLogoutTests: _callFUT")
		return Dbas.main_logout(request)

	# logout has no niew
	# def test_logout(self):
		# print("ViewLogoutTests: test_logout")
		# request = testing.DummyRequest()
		# response = Dbas(request).main_logout()
		# self.assertEqual('Logout', response['title'])


# testing logout redirection page
# class ViewLogoutRedirectTests(UnitTestBase):
	# def _callFUT(self, request):
		# print("ViewLogoutRedirectTests: tearDown")
		# return Dbas.main_logout_redirect(request)

	# def test_logout_redirect(self):
		# print("ViewLogoutRedirectTests: setUp")
		# request = testing.DummyRequest()
		# response = Dbas(request).main_logout_redirect()
		# # do NOT follow HTTPFound with webtest
		# # therefore we have function testings
		# self.assertEqual(response.status, '302 Found')


# testing contact page
class ViewContactTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewContactTests: _callFUT")
		return Dbas.main_contact(request)

	def test_contact(self):
		print("ViewContactTests: test_contact")
		request = testing.DummyRequest()
		response = Dbas(request).main_contact()
		self.assertEqual('Contact', response['title'])


# testing content page
class ViewContentTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewContentTests: _callFUT")
		return Dbas.main_content(request)

	def test_content(self):
		print("ViewContentTests: test_logout")
		request = testing.DummyRequest()
		response = Dbas(request).main_content()
		self.assertEqual('Content', response['title'])


# settings content page
class ViewSettingsTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewSettingsTests: _callFUT")
		return Dbas.main_settings(request)

	def test_content(self):
		print("ViewSettingsTests: test_logout")
		request = testing.DummyRequest()
		response = Dbas(request).main_settings()
		self.assertEqual('Settings', response['title'])


# testing content page
class ViewNewsTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewNewsTests: _callFUT")
		return Dbas.main_content(request)

	def test_news(self):
		print("ViewNewsTests: test_news")
		request = testing.DummyRequest()
		response = Dbas(request).main_news()
		self.assertEqual('News', response['title'])


# testing impressum page
class ViewImpressumTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewImpressumTests: tearDown")
		return Dbas.main_impressum(request)

	def test_impressum(self):
		print("ViewImpressumTests: setUp")
		request = testing.DummyRequest()
		response = Dbas(request).main_impressum()
		self.assertEqual('Impressum', response['title'])


# testing a unexisting page
class ViewNotFoundTests(UnitTestBase):
	def _callFUT(self, request):
		print("ViewNotFoundTests: tearDown")
		return Dbas.notfound(request)

	def test_main(self):
		print("ViewNotFoundTests: setUp")
		request = testing.DummyRequest()
		response = Dbas(request).notfound()
		self.assertEqual('Error', response['title'])

##########################################################################################################
##########################################################################################################
##########################################################################################################


# check, if every site responds with 200 except the error page
class FunctionalViewTests(IntegrationTestBase):
	editor_login = '/login?nickname=editor&password=test&came_from=main_page&form.login.submitted=Login'
	viewer_wrong_login = '/login?nickname=randomguest&password=incorrect&came_from=main_page&form.login.submitted=Login'

	# testing main page
	def test_home(self):
		print("FunctionalTests: test_home")
		res = self.testapp.get('/', status=200)
		self.assertIn(b'<h2><span class="font-semi-bold">Welcome', res.body)

	# testing contact page
	def test_contact(self):
		print("FunctionalTests: test_contact")
		res = self.testapp.get('/contact', status=200)
		self.assertIn(b'<div class="contact', res.body)

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
	# def logout_redirect_when_logged_out(self):
		# print("FunctionalTests: logout_redirect_when_logged_out")
		# res = self.testapp.get('/logout_redirect', status=302)
		# self.assertIn(b'You will be logged out and redirected', res.body)

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
		self.testapp.get('/login', status=302)

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
		res = self.testapp.get('/logout', status=302)
		self.assertTrue(b'Logout' not in res.body)

	# testing to get the content page when logged out / logged in
	def test_content_only_when_logged_in(self):
		print("FunctionalTests: test_content_only_when_logged_in")
		res = self.testapp.get('/content', status=200)
		self.assertNotIn(b'The current discussion is about', res.body)  # due to login error
		self.testapp.get(self.editor_login, status=302)
		res = self.testapp.get('/content', status=200)
		self.assertIn(b'The current discussion is about', res.body)

	# testing to get the settings page when logged out / logged in
	def test_settings_only_when_logged_in(self):
		print("FunctionalTests: test_settings_only_when_logged_in")
		res = self.testapp.get('/settings', status=200)
		self.assertNotIn(b'Settings', res.body)  # due to login error
		self.testapp.get(self.editor_login, status=302)
		res = self.testapp.get('/settings', status=200)
		self.assertIn(b'Settings', res.body)

##########################################################################################################
##########################################################################################################
##########################################################################################################

# checks for the email-connection
class FunctionalEMailTests(IntegrationTestBase):
	# testing the email - send
	def test_email_send(self):
		print("FunctionalTests: test_email_send")
		self.testapp.get('/contact', status=200)
		mailer = DummyMailer()
		mailer.send(Message(subject='hello world',
							sender='krauthoff@cs.uni-duesseldorf.de',
							recipients =['krauthoff@cs.uni-duesseldorf.de'],
							body='dummybody'))
		self.assertEqual(len(mailer.outbox), 1)
		self.assertEqual(mailer.outbox[0].subject, 'hello world')

	# testing the email - send_immediately
	def test_email_send_immediately(self):
		print("FunctionalTests: test_email_send_immediately")
		self.testapp.get('/contact', status=200)
		mailer = DummyMailer()
		mailer.send_immediately(Message(subject='hello world',
										sender='krauthoff@cs.uni-duesseldorf.de',
										recipients =['krauthoff@cs.uni-duesseldorf.de'],
										body='dummybody'))
		self.assertEqual(len(mailer.outbox), 1)
		self.assertEqual(mailer.outbox[0].subject, 'hello world')

	# testing the email - send_immediately_sendmail
	def test_email_send_immediately_sendmail(self):
		print("FunctionalTests: test_email_send_immediately_sendmail")
		self.testapp.get('/contact', status=200)
		mailer = DummyMailer()
		mailer.send_immediately_sendmail(Message(subject='hello world',
													sender='krauthoff@cs.uni-duesseldorf.de',
													recipients =['krauthoff@cs.uni-duesseldorf.de'],
													body='dummybody'))
		self.assertEqual(len(mailer.outbox), 1)
		self.assertEqual(mailer.outbox[0].subject, 'hello world')

##########################################################################################################
##########################################################################################################
##########################################################################################################


# checks for the database
class FunctionalDatabaseTests(IntegrationTestBase):

	def setUp(self):
		super(FunctionalDatabaseTests, self).setUp()
		self.session = Setup().add_testing_db(self.session)

	# testing group content
	def test_database_group_content(self):
		print("DatabaseTests: test_database_group_content")
		group_by_name1 = self.session.query(Group).filter_by(name='editors').first()
		group_by_name2 = self.session.query(Group).filter_by(name='users').first()
		group_by_uid1 = self.session.query(Group).filter_by(uid=1).first()
		group_by_uid2 = self.session.query(Group).filter_by(uid=2).first()
		self.assertTrue(group_by_name1.name, group_by_uid1.name)
		self.assertTrue(group_by_name2.name, group_by_uid2.name)
		self.assertTrue(group_by_name1.uid, group_by_uid1.uid)
		self.assertTrue(group_by_name2.uid, group_by_uid2.uid)

	# testing content
	def test_database_content(self):
		user1 = self.session.query(User).filter_by(nickname='test_user').first()
		user2 = self.session.query(User).filter_by(nickname='test_editor').first()
		position1 = self.session.query(Position).filter_by(text='I like cats.').first()  #, weight='100')
		position2 = self.session.query(Position).filter_by(text='I like dogs.').first()  #, weight='20')
		self.assertTrue(user1.firstname, 'user')
		self.assertTrue(user2.firstname, 'editor')
		self.assertEqual(position1.weight, 1)
		self.assertEqual(position2.weight, 2)

	# testing group content
	def test_database_user_content(self):
		print("DatabaseTests: test_database_user_content")
		user = self.session.query(User).filter_by(nickname='test_user').first()
		self.assertTrue(user.firstname, 'user')
		self.assertTrue(user.surname, 'user')
		self.assertTrue(user.nickname, 'user')
		self.assertTrue(user.email, 'dbas1@cs.uni-duesseldorf.de')
		self.assertTrue(user.password, PasswordHandler.get_hashed_password(None,'test'))

	# testing position content
	def test_database_position_content(self):
		print("DatabaseTests: test_database_position_content")
		position = self.session.query(Position).filter_by(uid=1).first()
		self.assertTrue(position.text, 'I like cats.')
		self.assertEqual(position.weight, 0)
		self.assertTrue(position.author, self.session.query(User).filter_by(uid=1).first().uid)

	# testing argument content
	def test_database_argument_content(self):
		print("DatabaseTests: test_database_argument_content")
		argument = self.session.query(Argument).filter_by(uid=1).first()
		self.assertTrue(argument.text, 'They are hating all humans!')
		self.assertEqual(argument.weight, 0)
		self.assertTrue(argument.author, self.session.query(User).filter_by(uid=1).first().uid)

	# testing relation arg pos content
	def test_database_RelationArgPos(self):
		print("DatabaseTests: test_database_RelationArgPos")
		relation = self.session.query(RelationArgPos).filter_by(uid=1).first()
		self.assertEqual(relation.weight, 0)
		self.assertTrue(relation.is_supportive, True)
		self.assertTrue(relation.author, self.session.query(User).filter_by(uid=1).first().uid)
		self.assertTrue(relation.pos_uid, self.session.query(Position).filter_by(uid=1).first().uid)
		self.assertTrue(relation.arg_uid, self.session.query(Argument).filter_by(uid=1).first().uid)

	# testing relation arg pos content
	def test_database_RelationPosArg(self):
		print("DatabaseTests: test_database_RelationPosArg")
		relation = self.session.query(RelationPosArg).filter_by(uid=1).first()
		self.assertEqual(relation.weight, 6)
		self.assertFalse(relation.is_supportive, False)
		self.assertTrue(relation.author, self.session.query(User).filter_by(uid=1).first().uid)
		self.assertTrue(relation.pos_uid, self.session.query(Position).filter_by(uid=2).first().uid)
		self.assertTrue(relation.arg_uid, self.session.query(Argument).filter_by(uid=1).first().uid)

	# testing relation arg arg content
	def test_database_RelationArgArg(self):
		print("DatabaseTests: test_database_RelationArgArg")
		relation = self.session.query(RelationArgArg).filter_by(uid=1).first()
		self.assertEqual(relation.weight, 0)
		self.assertFalse(relation.is_supportive, True)
		self.assertTrue(relation.author, self.session.query(User).filter_by(uid=1).first().uid)
		self.assertTrue(relation.arg_uid1, self.session.query(Argument).filter_by(uid=1).first().uid)
		self.assertTrue(relation.arg_uid2, self.session.query(Argument).filter_by(uid=2).first().uid)

	# testing relation pos pos content
	def test_database_RelationPosPos(self):
		print("DatabaseTests: test_database_RelationPosPos")
		relation = self.session.query(RelationPosPos).filter_by(uid=1).first()
		self.assertEqual(relation.weight, 4)
		self.assertFalse(relation.is_supportive, True)
		self.assertTrue(relation.author, self.session.query(User).filter_by(uid=2).first().uid)
		self.assertTrue(relation.pos_uid1, self.session.query(Position).filter_by(uid=1).first().uid)
		self.assertTrue(relation.pos_uid2, self.session.query(Position).filter_by(uid=2).first().uid)
