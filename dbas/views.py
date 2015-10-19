import transaction
import datetime

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config#
from pyramid.security import remember, forget
from pyramid.session import check_csrf_token
from pyramid.renderers import get_renderer
from pyramid.threadlocal import get_current_registry
from pyshorteners.shorteners import Shortener

from .database import DBDiscussionSession
from .database.discussion_model import User, Group, Issue
from .database_helper import DatabaseHelper
from .user_management import PasswordGenerator, PasswordHandler, UserHandler
from .query_helper import QueryHelper
from .email import EmailHelper
from .dictionary_helper import DictionaryHelper
from .logger import logger

name = 'D-BAS'
version = '0.3.7'
header = name + ' ' + version
issue_fallback = 1#DBDiscussionSession.query(Issue).first().uid

class Dbas(object):
	def __init__(self, request):
		"""
		Object initialization
		:param request: init http request
		:return:
		"""
		self.request = request
		self.issue_fallback = DBDiscussionSession.query(Issue).first().uid


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
	# @view_config(route_name='user_registration', renderer='templates/login.pt', permission='everybody')
	# @forbidden_view_config(renderer='templates/login.pt')
	# def user_registration(self):

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
		:return: dictionary with title and project username as well as a value, weather the user is logged in
		"""
		logger('main_contact', 'def', 'contact page')

		token = self.request.session.new_csrf_token()
		logger('main_contact', 'new token', str(token))

		contact_error = False
		send_message = False
		message = ''
		username = ''
		email = ''
		phone = ''
		content = ''
		spam = ''

		if 'form.contact.submitted' in self.request.params:
			logger('main_contact', 'form.contact.submitted', 'requesting params')
			username = self.request.params['name']
			email = self.request.params['mail']
			phone = self.request.params['phone']
			content = self.request.params['content']
			spam = self.request.params['spam']
			request_token = self.request.params['csrf_token']

			logger('main_contact', 'form.contact.submitted', 'validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			## sanity checks
			# check for empty username
			if not username:
				logger('main_contact', 'form.contact.submitted', 'username empty')
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

			# check for empty username
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
				body = 'Name: ' + username + '\n' + 'Mail: ' + email + '\n' + 'Phone: ' + phone + '\n' + 'Message:\n' + content
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
			'name': username,
			'mail': email,
			'phone': phone,
			'content': content,
			'spam': spam,
			'csrf_token': token
		}

	# content page, after login
	@view_config(route_name='main_discussion', renderer='templates/content.pt', permission='everybody')
	@view_config(route_name='main_discussion_start', renderer='templates/content.pt', permission='everybody')
	@view_config(route_name='main_discussion_issue', renderer='templates/content.pt', permission='everybody')
	def main_discussion(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_discussion', 'def', 'main')

		parameters = self.request.matchdict['parameters'] if 'parameters' in self.request.matchdict else '-'
		service = 'ajax_' + self.request.matchdict['service'] if 'service' in self.request.matchdict else '-'

		logger('main_discussion', 'def', 'is issue in params ' + str('issue' in self.request.params))
		logger('main_discussion', 'def', 'is issue in session ' + str('issue' in self.request.session))
		logger('main_discussion', 'def', 'is issue in matchdict ' + str('issue' in self.request.matchdict))

		# first matchdict, then params, then session, afterwards fallback
		if 'issue' in self.request.matchdict:
			issue = self.request.matchdict['issue']
			where = 'self.request.matchdict[issue]'
		elif 'issue' in self.request.params:
			issue = self.request.params['issue']
			where = 'self.request.params[issue]'
		elif 'issue' in self.request.session:
			issue = self.request.session['issue']
			where = 'self.request.session[issue]'
		else:
			where = 'fallback'
			issue = issue_fallback

		logger('main_discussion', 'def', 'self.request.matchdict[parameters]: ' + parameters)
		logger('main_discussion', 'def', 'self.request.matchdict[service]: ' + service)
		logger('main_discussion', 'def', where + ': ' + str(issue))

		# save issue in session
		self.request.session['issue'] = issue
		logger('main_discussion', 'def', 'set session[issue] to ' + str(issue))

		token = self.request.session.new_csrf_token()
		logger('main_discussion', 'new token', str(token))

		# checks whether the current user is admin
		is_admin = UserHandler().is_user_admin(self.request.authenticated_userid)

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		logger('main_discussion', 'def', 'return')
		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Content',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'is_admin': is_admin,
			'parameters': parameters,
			'service': service,
			'issue': issue
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

		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
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
					logger('main_settings', 'form.passwordrequest.submitted', 'new password is ' + new_pw)
					password_handler = PasswordHandler()
					hashed_pw = password_handler.get_hashed_password(new_pw)
					logger('main_settings', 'form.passwordrequest.submitted', 'New hashed password is ' + hashed_pw)

					# set the hased one
					db_user.password = hashed_pw
					DBDiscussionSession.add(db_user)
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

		is_author = UserHandler().is_user_author(self.request.authenticated_userid)

		# get date
		now = datetime.datetime.now()
		yyyy = str(now.year)
		mm = str(now.month) if now.month > 9 else '0' + str(now.month)
		dd = str(now.day) if now.day > 9 else '0' + str(now.day)
		date = dd + "." + mm + "." + yyyy

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'News',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'date':date,
			'is_author': is_author
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

		return_dict = dict()
		try:
			logger('get_start_statemens', 'def', 'read params')
			issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			return_dict = DatabaseHelper().get_start_statements(issue)
		except KeyError as e:
			logger('get_start_statemens', 'error', repr(e))

		return_dict['logged_in'] = self.request.authenticated_userid
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
			logger('get_premisses_for_statement', 'def', 'read params: ' + str(self.request.params))
			uids = self.request.params['uid'].split('=')
			uid = uids[1]
			logger('get_premisses_for_statement', 'def', 'issue in params ' + str('issue' in self.request.params))
			logger('get_premisses_for_statement', 'def', 'issue in params ' + str('issue' in self.request.params))
			logger('get_premisses_for_statement', 'def', 'issue in params ' + str('issue' in self.request.params))
			logger('get_premisses_for_statement', 'def', 'issue in params ' + str('issue' in self.request.params))
			logger('get_premisses_for_statement', 'def', 'issue in session ' + str('issue' in self.request.session))
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			logger('get_premisses_for_statement', 'def', 'uid: ' + uid + ', issue ' + str(issue))
			return_dict = DatabaseHelper().get_premisses_for_statement(transaction, uid, True, self.request.authenticated_userid,
			                                                           self.request.session.id, issue)
			return_dict['status'] = '1'
		except KeyError as e:
			logger('get_premisses_for_statement', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
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
			pgroup = self.request.params['pgroup'].split('=')[1]
			conclusion = self.request.params['conclusion'].split('=')[1]
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			logger('reply_for_argument', 'def', 'issue ' + str(issue))
			logger('reply_for_argument', 'def', 'pgroup ' + str(pgroup))
			logger('reply_for_argument', 'def', 'conclusion ' + str(conclusion))
			# track will be saved in the method
			return_dict, status = DatabaseHelper().get_attack_for_premissegroup(transaction, self.request.authenticated_userid, pgroup,
			                                                                    conclusion, self.request.session.id, issue)
			return_dict['status'] = str(status)
		except KeyError as e:
			logger('reply_for_premissegroup', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
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
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			id_text = self.request.params['id_text'].split('=')[1]
			pgroup_id = self.request.params['pgroup'].split('=')[1]
			logger('reply_for_argument', 'def', 'issue ' + str(issue))
			logger('reply_for_argument', 'def', 'id_text ' + str(id_text))
			logger('reply_for_argument', 'def', 'pgroup_id ' + str(pgroup_id))
			# track will be saved in the method
			return_dict, status = DatabaseHelper().get_attack_for_argument(transaction, self.request.authenticated_userid, id_text,
			                                                               pgroup_id, self.request.session.id, issue)
			return_dict['status'] = str(status)
		except KeyError as e:
			logger('reply_for_argument', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
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
			uid_text = self.request.params['id'].split('=')[1]
			relation = self.request.params['relation'].split('=')[1]
			confrontation = self.request.params['confrontation'].split('=')[1]
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback

			# track will be saved in get_reply_confrontation_response
			logger('reply_for_response_of_confrontation', 'def', 'id ' + uid_text + ', last relation ' + relation + ', confrontation ' + confrontation)
			return_dict, status = DatabaseHelper().get_reply_confrontations_response(transaction, uid_text, self.request.authenticated_userid,
			                                                                         self.request.session.id, issue)
			return_dict['status'] = status
			return_dict['last_relation'] = relation
			return_dict['confrontation_uid'] = confrontation
			# return_dict['confrontation_text'] = QueryHelper().get_text_for_arguments_premissesGroup_uid(confrontation, issue)
			return_dict['confrontation_text'], uids = QueryHelper().get_text_for_premissesGroup_uid(confrontation, issue)
		except KeyError as e:
			logger('reply_for_response_of_confrontation', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
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
			issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			logger('set_new_start_statement', 'def', 'request data: statement ' + str(statement))
			new_statement, is_duplicate = DatabaseHelper().set_statement(transaction, statement, self.request.authenticated_userid, True, issue)
			if not new_statement:
				return_dict['status'] = '0'
			else:
				return_dict['status'] = '0' if is_duplicate else '1'
				return_dict['statement'] = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)
		except KeyError as e:
			logger('set_new_start_statement', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - send new premisses
	@view_config(route_name='ajax_set_new_premisses_for_X', renderer='json', check_csrf=True)
	def set_new_premisses_for_X(self):
		"""

		:return:
		"""
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)

		logger('set_new_premisses_for_X', 'def', 'main')

		return_dict = dict()
		try:
			logger('set_new_premisses_for_X', 'def', 'main')
			pro_dict = dict()
			con_dict = dict()
			related_argument  = self.request.params['related_argument'] if 'related_argument' in self.request.params else -1
			premissegroup_id  = self.request.params['premissegroup_id'] if 'premissegroup_id' in self.request.params else -1
			current_attack    = self.request.params['current_attack'] if 'current_attack' in self.request.params else -1
			confrontation_uid = self.request.params['confrontation_uid'] if 'confrontation_uid' in self.request.params else -1
			issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			# confrontation_uid is a premisse group
			# todo kill last_attack !

			# Interpretation of the parameters
			# User says: E => A             | #related_argument
			# System says:
			#   undermine:  F => !E         | #premissegroup_id  =>  !premissegroup of #related_argument
			#   undercut:   D => !(E=>A)    | #premissegroup_id  =>  !#related_argument
			#   rebut:      B => !A         | #premissegroup_id  =>  !conclusion of #related_argument
			# Handle it, based on current and last attack


			# getting all arguments
			for key in self.request.params:
				logger('set_new_premisses_for_X', key, self.request.params[key])
				if 'pro_' in key:
					pro_dict[key] = self.request.params[key]
				if 'con_' in key:
					con_dict[key] = self.request.params[key]

			return_dict['status'] = '1'
			return_dict.update(DatabaseHelper().handle_inserting_new_statements(
				user = user_id,
				pro_dict = pro_dict,
				con_dict = con_dict,
				transaction = transaction,
				argument_id = related_argument,
				premissegroup_id = premissegroup_id,
				confrontation_uid = confrontation_uid,
				current_attack = current_attack,
				issue = issue
			))

		except KeyError as e:
			logger('set_new_premisses_for_X', 'error', repr(e))
			return_dict['status'] = '-1'

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

		return_dict = dict()
		try:
			uid = self.request.params['uid']
			issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			logger('get_logfile_for_statement', 'def', 'params uid: ' + str(uid))
			return_dict = DatabaseHelper().get_logfile_for_statement(uid, issue)
		except KeyError as e:
			logger('get_logfile_for_statement', 'error', repr(e))

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

		try:
			uid = self.request.params['uid']
			corrected_text = self.request.params['text']
			is_final = self.request.params['final']
			issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
			logger('set_correcture_of_statement', 'def', 'params uid: ' + str(uid) + ', corrected_text: ' + str(corrected_text)
			       + ', final ' + str(is_final))
			return_dict = DatabaseHelper().correct_statement(transaction, self.request.authenticated_userid, uid, corrected_text,
			                                                 is_final, issue)
		except KeyError as e:
			return_dict = dict()
			logger('set_correcture_of_statement', 'error', repr(e))

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
		issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
		return_dict = DatabaseHelper().get_attack_overview(self.request.authenticated_userid, issue)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for attack overview
	@view_config(route_name='ajax_get_issue_list', renderer='json')
	def get_issue_list(self):
		"""

		:return:
		"""

		logger('get_issue_list', 'def', 'main')
		return_dict = DatabaseHelper().get_issue_list()
		issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback
		return_dict['current_issue'] = issue
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - user login
	@view_config(route_name='ajax_user_login', renderer='json')
	def user_login(self):
		"""

		:return:
		"""
		logger('user_login', 'def', 'main')

		success = '0'
		message = ''
		return_dict = {}

		try:
			nickname = self.request.params['user']
			password = self.request.params['password']
			url = self.request.params['url']
			logger('user_login', 'def', 'params nickname: ' + str(nickname) + ', password: ' + str(password) + ', url: ' + url)

			db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

			# check for user and password validations
			if not db_user:
				logger('user_login', 'no user', 'user \'' + nickname + '\' does not exists')
				message = 'User does not exists'
			elif not db_user.validate_password(password):
				logger('user_login', 'password not valid', 'wrong password')
				message = 'Wrong password'
			else:
				logger('user_login', 'login', 'login successful')
				headers = remember(self.request, nickname)

				# update timestamp
				logger('user_login', 'login', 'update login timestamp')
				db_user.update_last_logged()
				transaction.commit()

				return HTTPFound(
					location=url,
					headers=headers,
				)

		except KeyError as e:
			logger('user_login', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - registration of users
	@view_config(route_name='ajax_user_registration', renderer='json')
	def user_registration(self):
		"""

		:return:
		"""
		logger('user_registration', 'def', 'main')

		success = '0'
		message = ''
		return_dict = {}

		try:
			firstname = self.request.params['firstname']
			lastname = self.request.params['lastname']
			nickname = self.request.params['nickname']
			email = self.request.params['email']
			gender = self.request.params['gender']
			password = self.request.params['password']
			passwordconfirm = self.request.params['passwordconfirm']
			logger('user_registration', 'def', 'params firstname: ' + str(firstname) + ', lastname: ' + str(lastname) + ', nickname: ' + str(nickname) + ', email: ' + str(email) + ', password: ' + str(password) + ', passwordconfirm: ' + str(passwordconfirm))

			# database queries mail verification
			db_nick = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
			db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
			logger('user_registration', 'main', 'Validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# are the password equal?
			if not password == passwordconfirm:
				logger('user_registration', 'main', 'Passwords are not equal')
				message = 'Passwords are not equal'
			# is the nick already taken?
			elif db_nick:
				logger('user_registration', 'main', 'Nickname \'' + nickname + '\' is taken')
				message = 'Nickname is taken'
			# is the email already taken?
			elif db_mail:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is taken')
				message = 'E-Mail is taken'
			# is the email valid?
			elif not is_mail_valid:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is not valid')
				message = 'E-Mail is not valid'
			# is the token valid?
			# elif request_token != token :
			# 	logger('user_registration', 'main', 'token is not valid')
			# 	logger('user_registration', 'main', 'request_token: ' + str(request_token))
			# 	logger('user_registration', 'main', 'token: ' + str(token))
			# 	message = 'CSRF-Token is not valid'
			else:
				# getting the editors group
				db_group = DBDiscussionSession.query(Group).filter_by(name="editors").first()

				# does the group exists?
				if not db_group:
					message = 'An error occured, please try again later or contact the author'
					logger('user_registration', 'main', 'Error occured')
				else:
					# creating a new user with hased password
					logger('user_registration', 'main', 'Adding user')
					hashedPassword = PasswordHandler().get_hashed_password(password)
					newuser = User(firstname=firstname,
					               surname=lastname,
					               email=email,
					               nickname=nickname,
					               password=hashedPassword,
					               gender=gender,
					               group=db_group.uid)
					DBDiscussionSession.add(newuser)
					transaction.commit()

					# sanity check, whether the user exists
					checknewuser = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
					if checknewuser:
						logger('user_registration', 'main', 'New data was added with uid ' + str(checknewuser.uid))
						message = 'Your account was added and you are now able to login.'
						success = '1'

						# sending an email
						subject = 'D-BAS Account Registration'
						body = 'Your account was successfully registered for this e-mail.'
						EmailHelper().send_mail(self.request, subject, body, email)

					else:
						logger('user_registration', 'main', 'New data was not added')
						message = 'Your account with the nick could not be added. Please try again or contact the author.'

		except KeyError as e:
			logger('user_registration', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - password requests
	@view_config(route_name='ajax_user_password_request', renderer='json')
	def user_password_request(self):
		"""

		:return:
		"""
		logger('user_password_request', 'def', 'main')

		success = '0'
		message = ''
		return_dict = {}

		try:
			email = self.request.params['email']
			logger('user_password_request', 'def', 'params email: ' + str(email))
			success = '1'

			db_user = DBDiscussionSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if db_user:
				# get password and hashed password
				pwd = PasswordGenerator().get_rnd_passwd()
				logger('user_password_request', 'form.passwordrequest.submitted', 'New password is ' + pwd)
				hashedpwd = PasswordHandler().get_hashed_password(pwd)
				logger('user_password_request', 'form.passwordrequest.submitted', 'New hashed password is ' + hashedpwd)

				# set the hased one
				db_user.password = hashedpwd
				DBDiscussionSession.add(db_user)
				transaction.commit()

				body = 'Your nickname is: ' + db_user.nickname + '\n'
				body += 'Your new password is: ' + pwd
				subject = 'D-BAS Password Request'
				reg_success, reg_failed, message= EmailHelper().send_mail(self.request, subject, body, email)

				# logger
				if reg_success:
					logger('user_password_request', 'form.passwordrequest.submitted', 'New password was sent')
					success = '1'
				elif reg_failed:
					logger('user_password_request', 'form.passwordrequest.submitted', 'Error occured')
			else:
				logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
				message = 'The given e-mail address is unkown'


		except KeyError as e:
			logger('user_password_request', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for getting all news
	@view_config(route_name='ajax_get_news', renderer='json')
	def get_news(self):
		"""

		:return:
		"""

		logger('get_news', 'def', 'main')
		return_dict = DatabaseHelper().get_news()
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for sending news
	@view_config(route_name='ajax_send_news', renderer='json')
	def send_news(self):
		"""

		:return:
		"""
		try:
			title = self.request.params['title']
			text = self.request.params['text']
			return_dict = DatabaseHelper().set_news(transaction, title, text, self.request.authenticated_userid)
		except KeyError as e:
			return_dict = dict()
			logger('reply_for_response_of_confrontation', 'error', repr(e))
			return_dict['status'] = '-1'

		logger('send_news', 'def', 'main')
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for fuzzy search
	@view_config(route_name='ajax_fuzzy_search', renderer='json')
	def fuzzy_search(self):
		"""

		:return:
		"""
		logger('fuzzy_search', 'main', 'def')
		try:
			value = self.request.params['value']
			mode = str(self.request.params['type'])
			issue = self.request.params['issue'] if 'issue' in self.request.params else self.request.session['issue'] if 'issue' in self.request.session else issue_fallback

			logger('fuzzy_search', 'main', 'value: ' + str(value) + ', mode: ' + str(mode) + ', issue: ' + str(issue))
			if mode == '0': # start statement
				return_dict = DatabaseHelper().get_fuzzy_string_for_start(value, issue, True)
			elif mode == '1': # edit statememt popup
				statement_uid = self.request.params['extra']
				return_dict = DatabaseHelper().get_fuzzy_string_for_edits(value, statement_uid, issue)
			elif mode == '2':  # start premisse
				return_dict = DatabaseHelper().get_fuzzy_string_for_start(value, issue, False)
			else:
				return_dict = dict()
		except KeyError as e:
			return_dict = dict()
			logger('fuzzy_search', 'error', repr(e))
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json
