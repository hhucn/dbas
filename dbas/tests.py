"""
All kind of tests

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import os
import unittest
import dbas.password_handler as PasswordHandler

from admin.views import main_admin

from webtest import TestApp
from dbas.views import Dbas
from dbas import main
from dbas.database import DBDiscussionSession, initializedb
from dbas.database.discussion_model import Group, User
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
	"""
	Setup testing database
	"""
	# def __init__(self):
	# 	print("Setup __init__")

	def add_testing_db(self, session):
		"""
		Dummy values for testing database

		:param session: current session
		:return: current session inclusive values
		"""
		group1 = session.query(Group).filter_by(name='foo').first()
		group2 = session.query(Group).filter_by(name='bar').first()
		session.add_all([group1, group2])
		session.flush()
		pw1 = PasswordHandler.get_hashed_password('test')
		pw2 = PasswordHandler.get_hashed_password('test')
		user1 = User(firstname='editor', surname='editor', nickname='editor', email='dbas1@hhu.de', password=pw1, gender='m', group=group1)
		user2 = User(firstname='user', surname='user', nickname='user', email='dbas2@hhu.de', password=pw2, gender='m', group=group2)
		user1.group = group1.uid
		user2.group = group2.uid
		session.add_all([user1, user2])
		session.flush()
		initializedb.main_discussion(session)
		return session

	def add_routes(self, config):
		"""
		Routes for testing

		:param config: current config
		:return: current config inclusive routes
		"""
		config.add_route('main_page', '/')
		config.add_route('main_contact', '/contact')
		config.add_route('main_settings', '/settings')
		config.add_route('main_notification', '/notifications')
		config.add_route('main_admin', '/admin/main')
		config.add_route('main_news', '/news')
		config.add_route('main_imprint', '/imprint')
		config.add_route('discussion_reaction', '/discuss/{slug}/reaction/{arg_id_user}/{mode}/{arg_id_sys}')
		config.add_route('discussion_justify', '/discuss/{slug}/justify/{statement_or_arg_id}/{mode}*relation')
		config.add_route('discussion_attitude', '/discuss/{slug}/attitude/*statement_id')
		config.add_route('discussion_choose', '/discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids')
		config.add_route('discussion_finish', '/discuss/finish')
		config.add_route('discussion_init', '/discuss*slug')
		return config


# setup the DBDiscussionSession testing class what will manage our transactions
class DBASTestCase(unittest.TestCase):
	"""
	TODO
	"""

	@classmethod
	def setUpClass(cls):
		"""

		:return:
		"""
		print("DBASTestCase: setUpClass")
		cls.engine = engine_from_config(settings, prefix='sqlalchemy-discussion.')
		cls.Session = sessionmaker()

	def setUp(self):
		"""

		:return:
		"""
		print("DBASTestCase: setUp")
		# self.engine = engine_from_config(settings, prefix='sqlalchemy-discussion.')
		# self.Session = sessionmaker()
		# connection = self.engine.connect()
		# # begin a non-ORM transaction
		# self.trans = connection.begin()
		# # bind an individual Session to the connection
		# # Session.configure(bind=connection)
		# self.session = self.Session(bind=connection)
		# DBDiscussionSession.session = self.session

		self.config = testing.setUp()
		DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

	def tearDown(self):
		"""

		:return:
		"""
		# rollback - everything that happened with the
		# Session above (including calls to commit())
		# is rolled back.
		testing.tearDown()
		# self.trans.rollback()
		# self.session.close()


# skip the routes, templates, etc. So let’s setup our Unit Test DBDiscussionSession class
class UnitTestDBAS(DBASTestCase):
	"""
	TODO
	"""

	def setUp(self):
		"""

		:return:
		"""
		self.config = testing.setUp(request=testing.DummyRequest())
		super(UnitTestDBAS, self).setUp()
		self.config = Setup().add_routes(self.config)

	def tearDown(self):
		"""

		:return:
		"""
		print("UnitTestDBDiscussionSession: tearDown")
		testing.tearDown()

	def get_csrf_request(self, post=None):
		"""

		:return:
		"""
		# print("UnitTestDBDiscussionSession: get_csrf_request")
		csrf = 'abc'
		if 'csrf_token' not in post.keys():
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
class IntegrationTestDBAS(DBASTestCase):
	"""
	TODO
	"""

	@classmethod
	def setUpClass(cls):
		"""

		:return:
		"""
		cls.app = main({}, **settings)
		super(IntegrationTestDBAS, cls).setUpClass()

	def setUp(self):
		"""

		:return:
		"""
		print("IntegrationTestDBAS: setUp")
		self.testapp = TestApp(self.app)
		self.config = testing.setUp()
		super(IntegrationTestDBAS, self).setUp()
		self.config = Setup().add_routes(self.config)
		self.config.include('api', route_prefix='/api')
		self.config.include('export', route_prefix='/export')
		self.config.include('admin', route_prefix='/admin')
		self.config.include('pyramid_chameleon')
		self.config.include('pyramid_mailer')
		self.config.include('pyramid_beaker')


##########################################################################################################
##########################################################################################################
##########################################################################################################

class ViewMainTests(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print("ViewLoginTests: _callFUT")
		return Dbas.main_page(request)

	def test_main(self):
		"""

		:return:
		"""
		print("ViewLoginTests: test_main")
		request = testing.DummyRequest()
		response = Dbas(request).main_page()
		self.assertEqual('Main', response['title'])


class ViewContactTest(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print('ViewTest: _callFUT')
		return Dbas.main_page(request)

	def test_contact(self):
		"""

		:return:
		"""
		print('ViewTest: test_contact')
		request = testing.DummyRequest()
		response = Dbas(request).main_contact()
		self.assertEqual('Contact', response['title'])


class ViewSettingsTests(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print('ViewTest: _callFUT')
		return Dbas.main_settings(request)

	def test_settings(self):
		"""

		:return:
		"""
		print('ViewTest: test_settings')
		request = testing.DummyRequest()
		response = Dbas(request).main_settings()
		self.assertEqual('Settings', response['title'])


class ViewMessagesTests(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print('ViewTest: _callFUT')
		return Dbas.main_notifications(request)

	def test_notification(self):
		"""

		:return:
		"""
		print('ViewTest: test_notification')
		request = testing.DummyRequest()
		response = Dbas(request).main_notifications()
		self.assertEqual('Messages', response['title'])


class ViewNewsTests(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print('ViewTest: _callFUT')
		return Dbas.main_news(request)

	def test_news(self):
		"""

		:return:
		"""
		print('ViewTest: test_news')
		request = testing.DummyRequest()
		response = Dbas(request).main_news()
		self.assertEqual('News', response['title'])


class ViewImprintTests(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print('ViewTest: _callFUT')
		return Dbas.main_imprint(request)

	def test_imprint(self):
		"""

		:return:
		"""
		print('ViewTest: test_imprint')
		request = testing.DummyRequest()
		response = Dbas(request).main_imprint()
		self.assertEqual('Imprint', response['title'])

##########################################################################################################
##########################################################################################################


class ViewAdminTests(IntegrationTestDBAS):
	"""
	TODO
	"""

	def _callFUT(self, request):
		"""

		:return:
		"""
		print('ViewTest: _callFUT')
		return main_admin(request)

	def test_admin(self):
		"""

		:return:
		"""
		print('ViewTest: test_admin')
		request = testing.DummyRequest()
		response = main_admin(request)
		self.assertEqual('Admin', response['title'])

##########################################################################################################
##########################################################################################################


# check, if every site responds with 200 except the error page
class FunctionalViewTests(IntegrationTestDBAS):
	"""
	Todo
	"""

	editor_login       = '/ajax_user_login?user=Pascal&password=iamatestuser2016&keep_login=false&url=http://localhost:4284/discuss'
	viewer_wrong_login = '/ajax_user_login?user=Pascal&password=iamabigfoool2015&keep_login=false&url=http://localhost:4284/discuss'
	logout             = '/ajax_user_logout'

	# testing main page
	def test_home(self):
		"""

		:return:
		"""
		print("FunctionalTests: home")
		res = self.testapp.get('/', status=200)
		self.assertIn(b'<span>This work is part of the graduate school on</span>', res.body)

	# testing contact page
	def test_contact(self):
		"""

		:return:
		"""
		print("FunctionalTests: contact")
		res = self.testapp.get('/contact', status=200)
		self.assertIn(b'<p class="text-center">Feel free to drop us a line a', res.body)

	# testing contact page
	def test_imprint(self):
		"""

		:return:
		"""
		print("FunctionalTests: imprint")
		res = self.testapp.get('/imprint', status=200)
		self.assertIn(b'Imprint', res.body)

	# testing a unexisting page
	def test_unexisting_page(self):
		"""

		:return:
		"""
		print("FunctionalTests: unexisting_page")
		res = self.testapp.get('/SomePageYouWontFind', status=404)
		self.assertIn(b'404 Error', res.body)
		self.assertIn(b'SomePageYouWontFind', res.body)

	# testing successful log in
	def test_successful_log_in(self):
		"""

		:return:
		"""
		print("FunctionalTests: successful_log_in")
		res = self.testapp.get('http://localhost:4284' + self.editor_login, status=302)
		self.assertEqual(res.location, 'http://localhost:4284/discuss')

	# testing failed log in
	def test_failed_log_in(self):
		"""

		:return:
		"""
		print("FunctionalTests: failed_log_in")
		res = self.testapp.get(self.viewer_wrong_login, status=200)
		self.assertTrue(b'User / Password do not match' in res.body)

	# testing wheather the login link is there, when we are logged in
	def test_logout_link_present_when_logged_in(self):
		"""

		:return:
		"""
		print("FunctionalTests: logout_link_present_when_logged_in")
		self.testapp.get(self.editor_login, status=302)
		res = self.testapp.get('/', status=200)
		self.assertIn(b'Logout', res.body)

	# testing wheather the logout link is there, when we are logged out
	def test_logout_link_not_present_after_logged_out(self):
		"""

		:return:
		"""
		print("FunctionalTests: logout_link_not_present_after_logged_out")
		self.testapp.get(self.editor_login, status=302)
		self.testapp.get('/', status=200)
		res = self.testapp.get(self.logout, status=200)
		self.assertTrue(b'Logout' not in res.body)

	# testing to get the settings page when logged out / logged in
	def test_settings_only_when_logged_in(self):
		"""

		:return:
		"""
		print("FunctionalTests: settings_only_when_logged_in")
		res = self.testapp.get('/settings', status=200)
		self.assertNotIn(b'Settings', res.body)  # due to login error
		self.testapp.get(self.editor_login, status=302)
		res = self.testapp.get('/settings', status=200)
		self.assertIn(b'Settings', res.body)

##########################################################################################################
##########################################################################################################


# checks for the email-connection
class FunctionalEMailTests(IntegrationTestDBAS):
	"""
	Todo
	"""

	def test_email_send(self):
		"""

		:return:
		"""
		print("FunctionalTests: email_send")
		self.testapp.get('/contact', status=200)
		mailer = DummyMailer()
		mailer.send(Message(subject='hello world',
							sender='krauthoff@cs.uni-duesseldorf.de',
							recipients=['krauthoff@cs.uni-duesseldorf.de'],
							body='dummybody'))
		self.assertEqual(len(mailer.outbox), 1)
		self.assertEqual(mailer.outbox[0].subject, 'hello world')

	# testing the email - send_immediately
	def test_email_send_immediately(self):
		"""

		:return:
		"""
		print("FunctionalTests: email_send_immediately")
		self.testapp.get('/contact', status=200)
		mailer = DummyMailer()
		mailer.send_immediately(Message(subject='hello world',
										sender='krauthoff@cs.uni-duesseldorf.de',
										recipients=['krauthoff@cs.uni-duesseldorf.de'],
										body='dummybody'))
		self.assertEqual(len(mailer.outbox), 1)
		self.assertEqual(mailer.outbox[0].subject, 'hello world')

	# testing the email - send_immediately_sendmail
	def test_email_send_immediately_sendmail(self):
		"""

		:return:
		"""
		print("FunctionalTests: email_send_immediately_sendmail")
		self.testapp.get('/contact', status=200)
		mailer = DummyMailer()
		mailer.send_immediately_sendmail(Message(subject='hello world',
													sender='krauthoff@cs.uni-duesseldorf.de',
													recipients=['krauthoff@cs.uni-duesseldorf.de'],
													body='dummybody'))
		self.assertEqual(len(mailer.outbox), 1)
		self.assertEqual(mailer.outbox[0].subject, 'hello world')

##########################################################################################################
##########################################################################################################


# checks for the database
#class FunctionalDatabaseTests(IntegrationTestDBDiscussionSession):
#
#	def setUp(self):
#		super(FunctionalDatabaseTests, self).setUp()
#		self.session = Setup().add_testing_db(self.session)
#
#	# testing group content
#	def test_database_group_content(self):
#		print("DatabaseTests: test_database_group_content")
#		group_by_name1 = self.session.query(Group).filter_by(name='foo').first()
#		group_by_name2 = self.session.query(Group).filter_by(name='bar').first()
#		group_by_uid1 = self.session.query(Group).filter_by(uid=1).first()
#		group_by_uid2 = self.session.query(Group).filter_by(uid=2).first()
#		self.assertTrue(group_by_name1.name, group_by_uid1.name)
#		self.assertTrue(group_by_name2.name, group_by_uid2.name)
#		self.assertTrue(group_by_name1.uid, group_by_uid1.uid)
#		self.assertTrue(group_by_name2.uid, group_by_uid2.uid)
