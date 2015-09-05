import transaction

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid.session import check_csrf_token
from pyramid.renderers import get_renderer
from pyramid.threadlocal import get_current_registry
from pyshorteners.shorteners import Shortener

from .database import DBSession
from .database.model import User, Group, Issue
from .database_helper import DatabaseHelper
from .user_management import PasswordGenerator, PasswordHandler, UserHandler
from .query_helper import QueryHelper
from .email import EmailHelper
from .dictionary_helper import DictionaryHelper
from .logger import logger

name = 'D-BAS'
version = '0.3.1'
header = name + ' ' + version

class Dbas(object):
	def __init__(self, request):
		"""
		Object initialization
		:param request: init http request
		:return:
		"""
		self.request = request


	def base_layout(self):
		renderer = get_renderer('templates/basetemplate.pt')
		layout = renderer.implementation().macros['layout']
		return layout

	# main page
	@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
	def main_page(self):
		"""
		View configuration for the main page
		:return:
		"""
		logger('main_page', 'def', 'main page')
		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Main',
			'project': header,
			'logged_in': self.request.authenticated_userid
		}

	# login page
	@view_config(route_name='main_login', renderer='templates/login.pt', permission='everybody')
	@forbidden_view_config(renderer='templates/login.pt')
	def main_login(self):
		"""
		View-configuration for the login template
		:return:
		"""
		# check for already logged in users
		logger('main_login', 'def', 'login page')

		token = self.request.session.get_csrf_token()
		logger('main_login', 'new token', str(token))

		if self.request.authenticated_userid:
			logger('main_login', 'def', 'user is registered, so redirect to main_discussion_start')
			return HTTPFound(location=self.request.route_url('main_discussion_start'))

		login_url = self.request.route_url('main_login')
		referrer = self.request.url

		if referrer == login_url:
			referrer = self.request.route_url('main_page')  # never use the login form itself as came_from
		came_from = self.request.params.get('came_from', referrer)

		# some variables
		message = ''
		password = ''
		passwordconfirm = ''
		firstname = ''
		surname = ''
		nickname = ''
		email = ''
		reg_failed = False
		log_failed = False
		reg_success = False
		password_handler = PasswordHandler()
		password_generator = PasswordGenerator()

		# case: user login
		if 'form.login.submitted' in self.request.params:
			logger('main_login', 'form.login.submitted', 'requesting params')

			# requesting parameters
			nickname = self.request.params['nickname']
			password = self.request.params['password']
			db_user = DBSession.query(User).filter_by(nickname=nickname).first()

			# check for user and password validations
			if not db_user:
				logger('main_login', 'form.login.submitted', 'user \'' + nickname + '\' does not exists')
				message = 'User does not exists'
			elif not db_user.validate_password(password):  # dbUser.validate_password(password)
				logger('main_login', 'form.login.submitted', 'wrong password')
				message = 'Wrong password'
			else:
				logger('main_login', 'form.login.submitted', 'login successful')
				headers = remember(self.request, nickname)

				# update timestamp
				logger('main_login', 'form.login.submitted', 'update login timestamp')
				db_user.update_last_logged()
				transaction.commit()

				return HTTPFound(
					location=self.request.route_url('main_discussion_start'),
					headers=headers
				)
			log_failed = True

		# case: user registration
		if 'form.registration.submitted' in self.request.params:
			logger('main_login', 'form.registration.submitted', 'Requesting params')

			# getting parameter
			firstname = self.request.params['firstname']
			surname = self.request.params['surname']
			nickname = self.request.params['nickname']
			email = self.request.params['email']
			password = self.request.params['password']
			passwordconfirm = self.request.params['passwordconfirm']
			request_token = self.request.params['csrf_token']
			gender = self.request.params['inlineRadioGenderOptions']

			# database queries mail verification
			db_nick = DBSession.query(User).filter_by(nickname=nickname).first()
			db_mail = DBSession.query(User).filter_by(email=email).first()
			logger('main_login', 'form.registration.submitted', 'Validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# are the password equal?
			if not password == passwordconfirm:
				logger('main_login', 'form.registration.submitted', 'Passwords are not equal')
				message = 'Passwords are not equal'
				password = ''
				passwordconfirm = ''
				reg_failed = True
			# is the nick already taken?
			elif db_nick:
				logger('main_login', 'form.registration.submitted', 'Nickname \'' + nickname + '\' is taken')
				message = 'Nickname is taken'
				nickname = ''
				reg_failed = True
			# is the email already taken?
			elif db_mail:
				logger('main_login', 'form.registration.submitted', 'E-Mail \'' + email + '\' is taken')
				message = 'E-Mail is taken'
				email = ''
				reg_failed = True
			# is the email valid?
			elif not is_mail_valid:
				logger('main_login', 'form.registration.submitted', 'E-Mail \'' + email + '\' is not valid')
				message = 'E-Mail is not valid'
				email = ''
				reg_failed = True
			# is the token valid?
			elif request_token != token :
				logger('main_login', 'form.registration.submitted', 'token is not valid')
				logger('main_login', 'form.registration.submitted', 'request_token: ' + str(request_token))
				logger('main_login', 'form.registration.submitted', 'token: ' + str(token))
				message = 'CSRF-Token is not valid'
				reg_failed = True
			else:
				# getting the editors group
				db_group = DBSession.query(Group).filter_by(name="editors").first()

				# does the group exists?
				if not db_group:
					message = 'An error occured, please try again later or contact the author'
					reg_failed = True
					logger('main_login', 'form.registration.submitted', 'Error occured')
				else:
					# creating a new user with hased password
					logger('main_login', 'form.registration.submitted', 'Adding user')
					hashedPassword = password_handler.get_hashed_password(password)
					newuser = User(firstname=firstname,
					               surname=surname,
					               email=email,
					               nickname=nickname,
					               password=hashedPassword,
					               gender=gender,
					               group=db_group.uid)
					DBSession.add(newuser)
					transaction.commit()

					# sanity check, whether the user exists
					checknewuser = DBSession.query(User).filter_by(nickname=nickname).first()
					if checknewuser:
						logger('main_login', 'form.registration.submitted', 'New data was added with uid ' + str(checknewuser.uid))
						message = 'Your account was added and you are able to login now'
						reg_success = True

						# sending an email
						subject = 'D-BAS Account Registration'
						body = 'Your account was successfully registered for this e-mail.'
						EmailHelper().send_mail(self.request, subject, body, email)

					else:
						logger('main_login', 'form.registration.submitted', 'New data was not added')
						message = 'Your account with the nick could not be added. Please try again or contact the author'
						reg_failed = True

		# case: user password request
		if 'form.passwordrequest.submitted' in self.request.params:
			logger('main_login', 'form.passwordrequest.submitted', 'requesting params')
			email = self.request.params['email']
			logger('main_login', 'form.passwordrequest.submitted', 'email is ' + email)
			db_user = DBSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if db_user:
				# get password and hashed password
				pwd = password_generator.get_rnd_passwd()
				logger('main_login', 'form.passwordrequest.submitted', 'New password is ' + pwd)
				hashedpwd = password_handler.get_hashed_password(pwd)
				logger('main_login', 'form.passwordrequest.submitted', 'New hashed password is ' + hashedpwd)

				# set the hased one
				db_user.password = hashedpwd
				DBSession.add(db_user)
				transaction.commit()

				body = 'Your nickname is: ' + db_user.nickname + '\n'
				body += 'Your new password is: ' + pwd
				subject = 'D-BAS Password Request'
				reg_success, reg_failed, message= EmailHelper().send_mail(self.request, subject, body, email)

				# logger
				if reg_success:
					logger('main_login', 'form.passwordrequest.submitted', 'New password was sent')
				elif reg_failed:
					logger('main_login', 'form.passwordrequest.submitted', 'Error occured')
			else:
				logger('main_login', 'form.passwordrequest.submitted', 'Mail unknown')
				message = 'The given e-mail address is unkown'
				reg_failed = True

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': lang,
			'title': 'Login',
			'project': header,
			'message': message,
			'url': self.request.application_url + '/login',
			'came_from': came_from,
			'password': password,
			'passwordconfirm': passwordconfirm,
			'firstname': firstname,
			'surname': surname,
			'nickname': nickname,
			'email': email,
			'login_failed': log_failed,
			'registration_failed': reg_failed,
			'registration_success': reg_success,
			'logged_in': self.request.authenticated_userid,
			'csrf_token': token
		}

	# logout page
	@view_config(route_name='main_logout', permission='use')
	def main_logout(self):
		"""
		View configuration for the redirect logout view. This method will forget the headers of self.request
		:return: HTTPFound with location for the main page
		"""
		logger('main_logout', 'def', 'headers are now forgotten')
		logger('main_logout', 'def', 'redirecting to the main_page')
		headers = forget(self.request)
		return HTTPFound(
			location=self.request.route_url('main_page'),
			headers=headers
		)

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		"""
		View configuration for the contact view.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_contact', 'def', 'contact page')

		token = self.request.session.new_csrf_token()
		logger('main_contact', 'new token', str(token))

		contact_error = False
		send_message = False
		message = ''
		name = ''
		email = ''
		phone = ''
		content = ''
		spam = ''

		if 'form.contact.submitted' in self.request.params:
			logger('main_contact', 'form.contact.submitted', 'requesting params')
			name = self.request.params['name']
			email = self.request.params['mail']
			phone = self.request.params['phone']
			content = self.request.params['content']
			spam = self.request.params['spam']
			request_token = self.request.params['csrf_token']

			logger('main_contact', 'form.contact.submitted', 'validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			## sanity checks
			# check for empty name
			if not name:
				logger('main_contact', 'form.contact.submitted', 'name empty')
				contact_error = True
				message = "Your name is empty!"

			# check for non valid mail
			elif not is_mail_valid:
				logger('main_contact', 'form.contact.submitted', 'mail is not valid')
				contact_error = True
				message = "Your e-mail is empty!"

			# check for empty content
			elif not content:
				logger('main_contact', 'form.contact.submitted', 'content is empty')
				contact_error = True
				message = "Your content is empty!"

			# check for empty name
			elif (not spam) or (not spam.isdigit()) or (not int(spam) == 4):
				logger('main_contact', 'form.contact.submitted', 'empty or wrong anti-spam answer')
				contact_error = True
				message = "Your anti-spam message is empty or wrong!"

			# is the token valid?
			elif request_token != token :
				logger('main_contact', 'form.contact.submitted', 'token is not valid')
				logger('main_contact', 'form.contact.submitted', 'request_token: ' + str(request_token))
				logger('main_contact', 'form.contact.submitted', 'token: ' + str(token))
				message = 'CSRF-Token is not valid'
				contact_error = True

			else:
				subject = 'Contact D-BAS'
				body = 'Name: ' + name + '\n' + 'Mail: ' + email + '\n' + 'Phone: ' + phone + '\n' + 'Message:\n' + content
				send_message, contact_error, message = EmailHelper().send_mail(self.request, subject, body, email)

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Contact',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'was_message_send': send_message,
			'contact_error': contact_error,
			'message': message,
			'name': name,
			'mail': email,
			'phone': phone,
			'content': content,
			'spam': spam,
			'csrf_token': token
		}

	# content page, after login
	@view_config(route_name='main_discussion', renderer='templates/content.pt', permission='use')
	@view_config(route_name='main_discussion_start', renderer='templates/content.pt', permission='use')
	def main_discussion(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_discussion', 'def', 'main')

		parameters = self.request.matchdict['parameters'] if 'parameters' in self.request.matchdict else '-'
		service = 'ajax_' + self.request.matchdict['service'] if 'service' in self.request.matchdict else '-'
		logger('main_discussion', 'def', 'self.request.matchdict[parameters]: ' + parameters)
		logger('main_discussion', 'def', 'self.request.matchdict[service]: ' + service)


		token = self.request.session.new_csrf_token()
		logger('main_discussion', 'new token', str(token))

		db_issue = DBSession.query(Issue).filter_by(uid=1).first()
		issue = 'none'
		date = 'empty'
		logger('main_discussion', 'def', 'check for an issue')
		msg = ''

		# get the current issue
		if db_issue:
			logger('main_discussion', 'def', 'issue exists: ' + db_issue.text)
			issue = db_issue.text
			date = db_issue.date
		else:
			logger('main_discussion', 'def', 'issue does not exists')

		# checks whether the current user is admin
		is_admin = UserHandler().is_user_admin(self.request.authenticated_userid)

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Content',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'message': msg,
			'issue': issue,
			'date': date,
			'is_admin': is_admin,
			'parameters': parameters,
			'service': service
		}

	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_settings', 'def', 'main')

		token = self.request.session.new_csrf_token()
		logger('main_settings', 'new token', str(token))

		oldpw = ''
		newpw = ''
		confirmpw = ''
		message = ''
		error = False
		success = False

		db_user_firstname = 'unknown'
		db_user_surname = 'unknown'
		db_user_nickname = 'unknown'
		db_user_mail = 'unknown'
		db_user_group = 'unknown'

		db_user = DBSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
		if db_user:
			db_user_firstname = db_user.firstname
			db_user_surname = db_user.surname
			db_user_nickname = db_user.nickname
			db_user_mail = db_user.email
			db_user_group = db_user.groups.name

		if 'form.passwordchange.submitted' in self.request.params:
			logger('main_settings', 'form.changepassword.submitted', 'requesting params')
			old_pw = self.request.params['passwordold']
			new_pw = self.request.params['password']
			confirmpw = self.request.params['passwordconfirm']

			# is the old password given?
			if not old_pw:
				logger('main_settings', 'form.changepassword.submitted', 'old pwd is empty')
				message = 'The old password field is empty.'
				error = True
			# is the new password given?
			elif not new_pw:
				logger('main_settings', 'form.changepassword.submitted', 'new pwd is empty')
				message = 'The new password field is empty.'
				error = True
			# is the cofnrimation password given?
			elif not confirmpw:
				logger('main_settings', 'form.changepassword.submitted', 'confirm pwd is empty')
				message = 'The password confirmation field is empty.'
				error = True
			# is new password equals the confirmation?
			elif not new_pw == confirmpw:
				logger('main_settings', 'form.changepassword.submitted', 'new pwds not equal')
				message = 'The new passwords are not equal'
				error = True
			# is new old password equals the new one?
			elif oldpw == new_pw:
				logger('main_settings', 'form.changepassword.submitted', 'pwds are the same')
				message = 'The new and old password are the same'
				error = True
			else:
				# is the old password valid?
				if not db_user.validate_password(oldpw):
					logger('main_settings', 'form.changepassword.submitted', 'old password is wrong')
					message = 'Your old password is wrong.'
					error = True
				else:
					logger('main_login', 'form.passwordrequest.submitted', 'new password is ' + new_pw)
					password_handler = PasswordHandler()
					hashed_pw = password_handler.get_hashed_password(new_pw)
					logger('main_login', 'form.passwordrequest.submitted', 'New hashed password is ' + hashed_pw)

					# set the hased one
					db_user.password = hashed_pw
					DBSession.add(db_user)
					transaction.commit()

					logger('main_settings', 'form.changepassword.submitted', 'password was changed')
					message = 'Your password was changed'
					success = True

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Settings',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'passwordold': oldpw,
			'password': newpw,
			'passwordconfirm': confirmpw,
			'change_error': error,
			'change_success': success,
			'message': message,
			'db_firstname': db_user_firstname,
			'db_surname': db_user_surname,
			'db_nickname': db_user_nickname,
			'db_mail': db_user_mail,
			'db_group': db_user_group,
			'csrf_token': token
		}

	# news page for everybody
	@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
	def main_news(self):
		"""
		View configuration for the news.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_news', 'def', 'main')
		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'News',
			'project': header,
			'logged_in': self.request.authenticated_userid
		}

	# imprint
	@view_config(route_name='main_imprint', renderer='templates/imprint.pt', permission='everybody')
	def main_imprint(self):
		"""
		View configuration for the imprint.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_imprint', 'def', 'main')
		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Imprint',
			'project': header,
			'logged_in': self.request.authenticated_userid
		}

	# 404 page
	@notfound_view_config(renderer='templates/404.pt')
	def notfound(self):
		"""
		View configuration for the 404 page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('notfound', 'def', 'view \'' + self.request.view_name + '\' not found')
		self.request.response.status = 404
		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Error',
			'project': header,
			'page_notfound_viewname': self.request.view_name,
			'logged_in': self.request.authenticated_userid
		}

	# ajax - getting every user, and returns dicts with name <-> group
	@view_config(route_name='ajax_all_users', renderer='json', check_csrf=True)
	def get_all_users(self):
		"""
		Returns all users as dictionary with name <-> group
		:return: list of all users
		"""
		logger('get_all_users', 'def', 'main')
		logger('get_all_users', 'check_csrf_token', str(check_csrf_token(self.request)))

		return_dict = DatabaseHelper().get_all_users(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - return all start statements in the database
	@view_config(route_name='ajax_get_start_statements', renderer='json', check_csrf=True)
	def get_start_statemens(self):
		"""
		Returns all positions as dictionary with uid <-> value
		:return: list of all positions
		"""
		logger('get_start_statemens', 'def', 'main')

		# update timestamp
		logger('get_start_statemens', 'def',  'update login timestamp')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		return_dict = DatabaseHelper().get_start_statements()
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)


		return return_json

	# ajax - getting all arguments for the island view
	@view_config(route_name='ajax_get_premisses_for_statement', renderer='json', check_csrf=True)
	def get_premisses_for_statement(self):
		"""

		:return:
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_premisses_for_statement', 'def', 'main')

		return_dict = {}
		try:
			logger('get_premisses_for_statement', 'def', 'read params')
			uids = self.request.params['uid'].split('=')
			uid = uids[1]
			return_dict = DatabaseHelper().get_premisses_for_statement(transaction, uid, True, self.request.authenticated_userid)
			return_dict['status'] = '1'
		except KeyError as e:
			logger('get_premisses_for_statement', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - get reply for a premisse group
	@view_config(route_name='ajax_reply_for_premissegroup', renderer='json', check_csrf=True)
	def reply_for_premissegroup(self):
		"""
		Get reply for a premisse
		:return: dictionary with every arguments
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('reply_for_premissegroup', 'def', 'main')

		return_dict = {}
		try:
			ids = self.request.params['ids']
			logger('reply_for_premissegroup', 'def', 'ids ' + ids)
			ids = ids.split('&')
			if ids[0].startswith('pgroup'):
				pgroup_id   = ids[0][ids[0].index('=')+1:]
				statement_id = ids[1][ids[1].index('=')+1:]
			else:
				pgroup_id   = ids[1][ids[1].index('=')+1:]
				statement_id = ids[0][ids[0].index('=')+1:]
			logger('reply_for_premissegroup', 'def', 'premissegroup ' + str(id))
			# track will be saved in the method
			return_dict, status = DatabaseHelper().get_attack_for_premissegroup(transaction, self.request.authenticated_userid,
			                                                                    pgroup_id, statement_id)
			return_dict['status'] = str(status)
		except KeyError as e:
			logger('reply_for_premissegroup', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - get reply for an argument
	@view_config(route_name='ajax_reply_for_argument', renderer='json', check_csrf=True)
	def reply_for_argument(self):
		"""
		Get reply for ana rgument
		:return: dictionary with every arguments
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('reply_for_argument', 'def', 'main')

		return_dict = {}
		try:
			ids = self.request.params['ids']
			logger('reply_for_argument', 'def', 'ids ' + ids)
			ids = ids.split('&')
			if ids[0].startswith('id_text'):
				id_text   = ids[0][ids[0].index('=')+1:]
				pgroup_id = ids[1][ids[1].index('=')+1:]
			else:
				id_text   = ids[1][ids[1].index('=')+1:]
				pgroup_id = ids[0][ids[0].index('=')+1:]
			# track will be saved in the method
			return_dict, status = DatabaseHelper().get_attack_for_argument(transaction, self.request.authenticated_userid, id_text, pgroup_id)
			return_dict['status'] = str(status)
		except KeyError as e:
			logger('reply_for_argument', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - get reply for a confrontation
	@view_config(route_name='ajax_reply_for_response_of_confrontation', renderer='json', check_csrf=True)
	def reply_for_response_of_confrontation(self):
		"""

		:return:
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('reply_for_response_of_confrontation', 'def', 'main')

		return_dict = {}
		try:
			uids = self.request.params['id'].split('=')
			uid = uids[1]
			# track will be saved in get_reply_confrontation_response
			logger('reply_for_response_of_confrontation', 'def', 'id ' + uid)
			return_dict, status = DatabaseHelper().get_reply_confrontations_response(transaction, uid, self.request.authenticated_userid)
			return_dict['status'] = status
		except KeyError as e:
			logger('reply_for_response_of_confrontation', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting complete track of the user
	@view_config(route_name='ajax_manage_user_track', renderer='json', check_csrf=True)
	def manage_user_track(self):
		"""
		Request the complete user track
		:return:
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('manage_user_track', 'def', 'main')

		nickname = 'unknown'
		get_data = ''
		try:
			logger('manage_user_track', 'def', 'read params')
			nickname = str(self.request.authenticated_userid)
			get_data = self.request.params['get_data']
			logger('manage_user_track', 'def', 'nickname ' + nickname + ', get ' + get_data)
		except KeyError as e:
			logger('manage_user_track', 'error', repr(e))

		return_dict = {}
		if get_data == '1':
			logger('manage_user_track', 'def', 'get track data')
			return_dict = QueryHelper().get_track_of_user(nickname)
		else:
			logger('manage_user_track', 'def', 'remove track data')
			return_dict['removed data'] = 'true'
			QueryHelper().del_track_of_user(transaction, nickname)

		dictionary_helper = DictionaryHelper()
		return_json = dictionary_helper.dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - send new start statement
	@view_config(route_name='ajax_set_new_start_statement', renderer='json', check_csrf=True)
	def set_new_start_statement(self):
		"""
		Inserts a new statement into the database
		:return: a status code, if everything was successfull
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_new_start_statement', 'def', 'main')

		return_dict = {}
		try:
			statement = self.request.params['statement']
			logger('set_new_start_statement', 'def', 'request data: statement ' + str(statement))
			return_dict['success'] = '1'
			new_statement = DatabaseHelper().set_statement(transaction, statement, self.request.authenticated_userid, True)
			return_dict['statement'] = DictionaryHelper().save_statement_row_in_dictionary(new_statement)
		except KeyError as e:
			logger('set_new_start_statement', 'error', repr(e))
			return_dict['success'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - send new premisses
	@view_config(route_name='ajax_set_new_premisses', renderer='json', check_csrf=True)
	def set_new_premisses(self):
		"""

		:return:
		"""
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)

		logger('set_new_premisses', 'def', 'main')

		return_dict = {}
		try:
			logger('set_new_premisses', 'def', 'main')
			pro_dict = {}
			con_dict = {}
			conclusion_id = self.request.params['conclusion_id'];
			for key in self.request.params:
				if 'pro' in key:
					logger('set_new_premisses', key, self.request.params[key])
					pro_dict[key] = self.request.params[key]
				if 'con' in key:
					logger('set_new_premisses', key, self.request.params[key])
					con_dict[key] = self.request.params[key]
			dh = DatabaseHelper()
			return_dict = dh.set_premisses_for_tracked_argument(transaction, user_id, pro_dict, 'pro', conclusion_id, True)
			return_dict.update(dh.set_premisses_for_tracked_argument(transaction, user_id, con_dict, 'con', conclusion_id, False))
			return_dict['success'] = '1'

		except KeyError as e:
			logger('set_new_premisses', 'error', repr(e))
			return_dict['success'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting all arguments for the island view
	@view_config(route_name='ajax_get_logfile_for_statement', renderer='json', check_csrf=True)
	def get_logfile_for_statement(self):
		"""

		:return:
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_logfile_for_statement', 'def', 'main')

		uid = ''
		try:
			uid = self.request.params['uid']
			logger('get_logfile_for_statement', 'def', 'params uid: ' + str(uid))
		except KeyError as e:
			logger('get_logfile_for_statement', 'error', repr(e))

		return_dict = DatabaseHelper().get_logfile_for_statement(uid)
		# return_dict = DatabaseHelper().get_logfile_for_premissegroup(uid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting all arguments for the island view
	@view_config(route_name='ajax_set_correcture_of_statement', renderer='json', check_csrf=True)
	def set_correcture_of_statement(self):
		"""

		:return:
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_correcture_of_statement', 'def', 'main')

		uid = ''
		corrected_text = ''
		try:
			uid = self.request.params['uid']
			corrected_text = self.request.params['text']
			logger('set_correcture_of_statement', 'def', 'params uid: ' + str(uid) + ', corrected_text: ' + str(corrected_text))
		except KeyError as e:
			logger('set_correcture_of_statement', 'error', repr(e))

		return_dict = DatabaseHelper().correct_statement(transaction, self.request.authenticated_userid, uid, corrected_text)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for language switch
	@view_config(route_name='ajax_switch_language', renderer='json')
	def switch_language(self):
		"""

		:return:
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('switch_language', 'def', 'main')

		return_dict = {}
		try:
			lang = self.request.params['lang']
			logger('switch_language', 'def', 'params uid: ' + str(lang))
			self.request.response.set_cookie('_LOCALE_', str(lang))
			return_dict['status'] = '1'
		except KeyError as e:
			logger('swich_language', 'error', repr(e))
			return_dict['status'] = '0'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)
		return return_json

	# ajax - for shorten url
	@view_config(route_name='ajax_get_shortened_url', renderer='json')
	def get_shortened_url(self):
		"""
		Shortens url with the help of a python lib
		:return: dictionary with shortend url
		"""
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_shortened_url', 'def', 'main')

		return_dict = {}
		# google_api_key = ' AIzaSyAw0aPsBsAbqEJUP_zJ9Fifbhzs8xkNSw0'
		# bitly_login = 'dbashhu'
		# bitly_token = ''
		# bitly_key = 'R_d8c4acf2fb554494b65529314d1e11d1'

		try:
			url = self.request.params['url']
			# service = 'GoogleShortener'
			# service = 'BitlyShortener'
			service = 'TinyurlShortener'
			# service_url = 'https://goo.gl/'
			# service_url = 'https://bitly.com/'
			service_url = 'http://tinyurl.com/'
			logger('get_shortened_url', 'def', service + ' will shorten ' + str(url))

			# shortener = Shortener(service, api_key=google_api_key) # TODO use google
			# shortener = Shortener(service, bitly_login=bitly_login, bitly_api_key=bitly_key, bitly_token=bitly_token)
			shortener = Shortener(service)

			short_url = format(shortener.short(url))
			return_dict['url'] = short_url
			return_dict['service'] = service
			return_dict['service_url'] = service_url
			logger('get_shortened_url', 'def', 'short url ' + short_url)

			return_dict['status'] = '1'
		except KeyError as e:
			logger('get_shortened_url', 'error', repr(e))
			return_dict['status'] = '0'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)
		return return_json


	# ajax - for attack overview
	@view_config(route_name='ajax_get_attack_overview', renderer='json', check_csrf=True)
	def get_attack_overview(self):
		"""

		:return:
		"""

		logger('get_attack_overview', 'def', 'main')
		logger('get_attack_overview', 'check_csrf_token', str(check_csrf_token(self.request)))
		return_dict = DatabaseHelper().get_attack_overview(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json
