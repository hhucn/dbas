import transaction
import datetime
import requests
import urllib
import hashlib

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid.session import check_csrf_token
from pyramid.renderers import get_renderer
from pyramid.threadlocal import get_current_registry
from pyshorteners.shorteners import Shortener

from .database import DBDiscussionSession
from .database.discussion_model import User, Group, Issue, Argument
from .database_helper import DatabaseHelper
from .dictionary_helper import DictionaryHelper
from .email import EmailHelper
from .logger import logger
from .query_helper import QueryHelper
from .strings import Translator, TextGenerator
from .string_matcher import FuzzyStringMatcher
from .breadcrumb_helper import BreadcrumbHelper
from .tracking_helper import TrackingHelper
from .recommender_system import RecommenderHelper, RecommenderHelper
from .user_management import PasswordGenerator, PasswordHandler, UserHandler
from .weighting_helper import WeightingHelper

name = 'D-BAS'
version = '0.5.0'
header = name + ' ' + version
issue_fallback = 1

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class Dbas(object):
	def __init__(self, request):
		"""
		Object initialization
		:param request: init http request
		:return: json-dict()
		"""
		self.request = request
		self.issue_fallback = DBDiscussionSession.query(Issue).first().uid
		logger('DBAS', 'MAIN', 'issue_fallback ' + str(issue_fallback))

	def escape_string(self, text):
		"""

		:param text:
		:return: json-dict()
		"""
		return text # todo escaping string correctly
		#return re.escape(text)

	def base_layout(self):
		renderer = get_renderer('templates/basetemplate.pt')
		layout = renderer.implementation().macros['layout']
		return layout

	# main page
	@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
	@forbidden_view_config(renderer='templates/index.pt')
	def main_page(self):
		"""
		View configuration for the main page
		:return: HTTP 200 with several information
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
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

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		"""
		View configuration for the contact view.
		:return: dictionary with title and project username as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_contact', 'def', 'contact page')

		token = self.request.session.new_csrf_token()
		logger('main_contact', 'new token', str(token))

		contact_error = False
		send_message = False
		message = ''

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		logger('main_contact', 'form.contact.submitted', 'requesting params')
		username        = self.request.params['name'] if 'name' in self.request.params else ''
		email           = self.request.params['mail'] if 'mail' in self.request.params else ''
		phone           = self.request.params['phone'] if 'phone' in self.request.params else ''
		content         = self.request.params['content'] if 'content' in self.request.params else ''
		spam            = self.request.params['spam'] if 'spam' in self.request.params else ''
		request_token   = self.request.params['csrf_token'] if 'csrf_token' in self.request.params else ''
		logger('main_contact', 'form.contact.submitted', 'name: ' + name + ', mail: ' + email + ', phone: ' + phone + ', content: ' + content + ', spam: ' + spam + ', csrf_token: ' + request_token)

		# get anti-spam-question
		spamquestion, answer = UserHandler().get_random_anti_spam_question(lang)
		# save answer in session
		self.request.session['antispamanswer'] = answer

		if 'form.contact.submitted' in self.request.params:
			_t = Translator(lang)

			logger('main_contact', 'form.contact.submitted', 'validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			## sanity checks
			# check for empty username
			if not username:
				logger('main_contact', 'form.contact.submitted', 'username empty')
				contact_error = True
				message = _t.get(_t.emptyName)

			# check for non valid mail
			elif not is_mail_valid:
				logger('main_contact', 'form.contact.submitted', 'mail is not valid')
				contact_error = True
				message = _t.get(_t.emptyEmail)

			# check for empty content
			elif not content:
				logger('main_contact', 'form.contact.submitted', 'content is empty')
				contact_error = True
				message = _t.get(_t.emtpyContent)

			# check for empty username
			elif (not spam) or (not spam.isdigit()) or (not int(spam) == self.request.session['antispamanswer']):
				logger('main_contact', 'form.contact.submitted', 'empty or wrong anti-spam answer' + ', given answer ' + spam + ', right answer ' + str(self.request.session['antispamanswer']))
				contact_error = True
				message = _t.get(_t.maliciousAntiSpam)

			# is the token valid?
			elif request_token != token:
				logger('main_contact', 'form.contact.submitted', 'token is not valid' + ', request_token: ' + str(request_token) + ', token: ' + str(token))
				message = _t.get(_t.nonValidCSRF)
				contact_error = True

			else:
				subject = 'contactDBAS''Contact D-BAS'
				body = _t.get(_t.name) + ': ' + username + '\n'\
				       + _t.get(_t.mail) + ': ' + email + '\n'\
				       + _t.get(_t.phone) + ': ' + phone + '\n'\
				       + _t.get(_t.message) + ':\n' + content
				send_message, message = EmailHelper().send_mail(self.request, subject, body, email, lang)
				contact_error = not send_message

		logger('main_contact', 'form.contact.submitted', 'content: ' + content)
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
			'spam': '',
			'spamquestion': spamquestion,
			'csrf_token': token
		}

	# content page, after login
	@view_config(route_name='main_discussion', renderer='templates/content_old.pt', permission='everybody')
	@view_config(route_name='main_discussion_start', renderer='templates/content_old.pt', permission='everybody')
	@view_config(route_name='main_discussion_issue', renderer='templates/content_old.pt', permission='everybody')
	def main_discussion(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_discussion', 'def', 'main')

		parameters = self.request.matchdict['parameters'] if 'parameters' in self.request.matchdict else '-'

		logger('main_discussion', 'def', 'is issue in params ' + str('issue' in self.request.params))
		logger('main_discussion', 'def', 'is issue in session ' + str('issue' in self.request.session))
		logger('main_discussion', 'def', 'is issue in matchdict ' + str('issue' in self.request.matchdict))

		# first matchdict, then params, then session, afterwards fallback
		issue = self.request.matchdict['issue'] if 'issue' in self.request.matchdict \
			else self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
			else self.request.session['issue'] if 'issue' in self.request.session \
			else issue_fallback

		# save issue in session
		self.request.session['issue'] = issue
		logger('main_discussion', 'def', 'set session[issue] to ' + str(issue))

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
			'issue': issue
		}



	# content page
	@view_config(route_name='discussion_init', renderer='templates/content.pt', permission='everybody')
	def discussion_init(self):
		"""
		View configuration for the content view.
		:return: dictionary
		"""
		#'/a*slug'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_init', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))

		# update timestamp
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		_qh = QueryHelper()
		slug = self.request.matchdict['slug'][0] if len(self.request.matchdict['slug'])>0 else ''

		issue           = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		lang            = _qh.get_language(self.request, get_current_registry)
		issue_dict      = _qh.prepare_json_of_issue(issue, lang)

		discussion_dict = _qh.prepare_discussion_dict(issue, lang, at_start=True)
		item_dict       = _qh.prepare_item_dict_for_start(issue, self.request.authenticated_userid, lang)
		extras_dict     = _qh.prepare_extras_dict(slug, True, True, True, False, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': issue_dict['title'],
			'project': header,

			'issue': issue_dict,
			'discussion': discussion_dict,
			'item': item_dict,
			'extras': extras_dict
		}

	# attitude page
	@view_config(route_name='discussion_attitude', renderer='templates/content.pt', permission='everybody')
	def discussion_attitude(self):
		"""
		View configuration for the content view.
		:return: dictionary
		"""
		# '/a/{slug}/a/{statement_id}'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_attitude', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		# update timestamp
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		_qh = QueryHelper()
		_uh = UserHandler()
		slug            = matchdict['slug'] if 'slug' in matchdict['slug'] else ''
		statement_id    = matchdict['statement_id'][0] if 'statement_id' in matchdict else ''

		issue           = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		lang            = _qh.get_language(self.request, get_current_registry)
		issue_dict      = _qh.prepare_json_of_issue(issue, lang)

		discussion_dict = _qh.prepare_discussion_dict(statement_id, lang, at_attitude=True)
		item_dict       = _qh.prepare_item_dict_for_attitude(statement_id, issue, lang)
		extras_dict     = _qh.prepare_extras_dict(issue_dict['slug'], False, False, True, False, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': issue_dict['title'],
			'project': header,

			'issue': issue_dict,
			'discussion': discussion_dict,
			'item': item_dict,
			'extras': extras_dict
		}

	# justify page
	@view_config(route_name='discussion_justify', renderer='templates/content.pt', permission='everybody')
	def discussion_justify(self):
		"""
		View configuration for the content view.
		:return: dictionary
		"""
		# '/a/{slug}/j/{statement_or_arg_id}/{mode}*relation'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		# update timestamp
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		_qh = QueryHelper()

		slug                = matchdict['slug'] if 'slug' in matchdict else ''
		statement_or_arg_id = matchdict['statement_or_arg_id'] if 'statement_or_arg_id' in matchdict else ''
		mode                = matchdict['mode'] if 'mode' in matchdict else ''
		supportive          = mode == 't' or mode == 'd'  # supportive = t or dont know mode
		relation            = matchdict['relation'][0] if len(matchdict['relation'])>0 else ''

		issue               = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		lang                = _qh.get_language(self.request, get_current_registry)
		issue_dict          = _qh.prepare_json_of_issue(issue, lang)

		if [c for c in ('t','f') if c in mode] and relation == '':
			# justifying position
			logger('discussion_justify', 'def', 'justifying position')
			discussion_dict = _qh.prepare_discussion_dict(statement_or_arg_id, lang, at_justify=True, is_supportive=supportive)
			item_dict       = _qh.prepare_item_dict_for_justify_statement(statement_or_arg_id, issue, supportive, lang)
			extras_dict     = _qh.prepare_extras_dict(slug, True, True, True, False, self.request.authenticated_userid, True)

			# is the discussion at the end?
			if len(item_dict) == 0:
				# TODO HANDLE DISCUSSION END ; NO PREMISE
				_qh.add_discussion_end_text(discussion_dict, self.request.authenticated_userid, lang, at_justify=True)


		elif 'd' in mode and relation == '':
			# dont know
			logger('discussion_justify', 'def', 'dont know position')
			argument_uid    = RecommenderHelper().get_argument_by_conclusion(statement_or_arg_id, supportive) # todo empty uid
			discussion_dict = _qh.prepare_discussion_dict(argument_uid, lang, at_dont_know=True, is_supportive=supportive)
			item_dict       = _qh.prepare_item_dict_for_reaction(argument_uid, supportive, issue, lang)
			extras_dict     = _qh.prepare_extras_dict(slug, False, False, True, True, self.request.authenticated_userid)

			# is the discussion at the end?
			if len(item_dict) == 0:
				_qh.add_discussion_end_text(discussion_dict, self.request.authenticated_userid, lang, at_dont_know=True)


		else:
			# justifying argument
			logger('discussion_justify', 'def', 'argument stuff')
			is_attack = True if [c for c in ('undermine','rebut','undercut') if c in relation] else False
			discussion_dict = _qh.prepare_discussion_dict(statement_or_arg_id, lang, at_justify_argumentation=True,
			                                              is_supportive=supportive, attack=relation,
			                                              logged_in=self.request.authenticated_userid)
			item_dict       = _qh.prepare_item_dict_for_justify_argument(statement_or_arg_id, relation, issue, supportive, lang)
			extras_dict     = _qh.prepare_extras_dict(slug, False, False, True, True, self.request.authenticated_userid, is_attack)

			# is the discussion at the end?
			if len(item_dict) == 0:
				_qh.add_discussion_end_text(discussion_dict, self.request.authenticated_userid, lang, at_justify_argumentation=True)

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': issue_dict['title'],
			'project': header,

			'issue': issue_dict,
			'discussion': discussion_dict,
			'item': item_dict,
			'extras': extras_dict
		}

	# reaction page
	@view_config(route_name='discussion_reaction', renderer='templates/content.pt', permission='everybody')
	def discussion_reaction(self):
		"""
		View configuration for the content view.
		:return: dictionary
		"""
		# '/a/{slug}/r/{arg_id_user}/{mode}*arg_id_sys'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		# update timestamp
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		arg_id_user     = matchdict['arg_id_user'] if 'arg_id_user' in matchdict else ''
		attack          = matchdict['mode'] if 'mode' in matchdict else ''
		arg_id_sys      = matchdict['arg_id_sys'][0] if len(matchdict['arg_id_sys'])>0 else ''
		supportive      = DBDiscussionSession.query(Argument).filter_by(uid=arg_id_user).first().isSupportive

		_qh = QueryHelper()

		issue           = _qh.get_id_of_slug(slug, self.request) if len(slug) > 0 else _qh.get_issue(self.request)
		lang            = _qh.get_language(self.request, get_current_registry)
		issue_dict      = _qh.prepare_json_of_issue(issue, lang)

		discussion_dict = _qh.prepare_discussion_dict(arg_id_user, lang, at_argumentation=True, is_supportive=supportive,
		                                              additional_id=arg_id_sys, attack=attack)
		item_dict       = _qh.prepare_item_dict_for_reaction(arg_id_sys, supportive, issue, lang)
		extras_dict     = _qh.prepare_extras_dict(slug, False, False, True, True, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': issue_dict['title'],
			'project': header,

			'issue': issue_dict,
			'discussion': discussion_dict,
			'item': item_dict,
			'extras': extras_dict
		}



	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_settings', 'def', 'main')

		token = self.request.session.get_csrf_token()
		logger('main_settings', 'new token', str(token))

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']
		logger('main_settings', 'language', lang)

		old_pw = ''
		new_pw = ''
		confirm_pw = ''
		message = ''
		error = False
		success = False

		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
		logger('main_settings', 'db_user', db_user.nickname + ' ' + str(db_user.groups.uid) + ' ' + str(db_user.groups.name))
		uh = UserHandler()
		if db_user and 'form.passwordchange.submitted' in self.request.params:
			logger('main_settings', 'form.changepassword.submitted', 'requesting params')
			old_pw = self.request.params['passwordold']
			new_pw = self.request.params['password']
			confirm_pw = self.request.params['passwordconfirm']

			message, error, success = uh.change_password(transaction, db_user, old_pw, new_pw, confirm_pw, lang)

		# get gravater profile picture
		gravatar_url = uh.get_profile_picture(db_user)

		logger('main_settings', 'return change_error', str(error) + ', change_success' + str(success) + ', message' + str(message))
		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Settings',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'passwordold': '' if success else old_pw,
			'password': '' if success else new_pw,
			'passwordconfirm': '' if success else confirm_pw,
			'change_error': error,
			'change_success': success,
			'message': message,
			'db_firstname': db_user.firstname if db_user else 'unknown',
			'db_surname': db_user.surname if db_user else 'unknown',
			'db_nickname': db_user.nickname if db_user else 'unknown',
			'db_mail': db_user.email if db_user else 'unknown',
			'db_group': db_user.groups.name if db_user and db_user.groups else 'unknown',
			'avatar_url': gravatar_url,
			'csrf_token': token
		}

	# admin page, when logged in
	@view_config(route_name='main_admin', renderer='templates/admin.pt', permission='use')
	def main_admin(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_admin', 'def', 'main')

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		# checks whether the current user is admin
		is_admin = UserHandler().is_user_admin(self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(lang),
			'title': 'Settings',
			'project': header,
			'logged_in': self.request.authenticated_userid,
			'is_admin': is_admin,
		}

	# news page for everybody
	@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
	def main_news(self):
		"""
		View configuration for the news.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
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
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
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
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('notfound', 'def', 'main in ' + str(self.request.method) + '-request')

		logger('notfound', 'def', 'path: ' + self.request.path)
		logger('notfound', 'def', 'view name: ' + self.request.view_name)

		logger('notfound', 'def', 'params:')
		for param in self.request.params:
			logger('notfound', 'def', '    ' + param + ' -> ' + self.request.params[param])

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

	#########################################
	## DISCUSSION VIEWS ## TODO KILL THESE! #
	#########################################

	# ajax - return all start statements in the database
	@view_config(route_name='ajax_get_start_statements', renderer='json', check_csrf=False)
	def get_start_statements(self):
		"""
		Returns all positions as dictionary with uid <-> value
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: list of all positions
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_start_statements', 'def', 'main')

		# update timestamp
		logger('get_start_statements', 'def',  'update login timestamp')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		return_dict = dict()
		try:
			logger('get_start_statements', 'def', 'read params')
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback

			# reset and save url for breadcrumbs
			url = self.request.params['url']
			BreadcrumbHelper().del_breadcrumbs_of_user(transaction, self.request.authenticated_userid)
			BreadcrumbHelper().save_breadcrumb_for_user(transaction, self.request.authenticated_userid, url, 'Start',
			                                            self.request.session.id)

			if issue == 'undefined':
				logger('get_start_statements', 'def', 'issue is undefined -> fallback')
				issue = issue_fallback
				return_dict['reset_url'] = 'true'
				return_dict['reset_issue'] = issue
			else:
				logger('get_start_statements', 'def', 'issue found')

			return_dict.update(DatabaseHelper().get_start_statements(issue))
		except KeyError as e:
			logger('get_start_statements', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting text for a statement
	@view_config(route_name='ajax_get_text_for_statement', renderer='json', check_csrf=False)
	def get_text_for_statement(self):
		"""
		Returns text of a statement
		:needed param self.request.params['uid']: id of the statement
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_text_for_statement', 'def', 'main')

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = {}
		try:
			logger('get_text_for_statement', 'def', 'read params: ' + str(self.request.params))
			uid = self.request.params['uid'].split('=')[1]
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback

			# reset and save url for breadcrumbs
			url = self.request.params['url']
			BreadcrumbHelper().save_breadcrumb_for_user_with_statement_uid(transaction, self.request.authenticated_userid,
			                                                               url, uid, False, '', lang, self.request.session.id)
			logger('get_text_for_statement', 'def', 'uid: ' + uid)
			logger('get_text_for_statement', 'def', 'issue ' + str(issue))
			return_dict = DatabaseHelper().get_text_for_statement(uid, issue)
			_t = Translator(lang)
			text = ' <b>' + return_dict['text'][0:1].lower() + return_dict['text'][1:] + '</b>'
			return_dict['discussion_description'] = _t.get(_t.whatDoYouThinkAbout) + text + '?'
			return_dict['agree'] = _t.get(_t.iAgreeWithInColor) + text
			return_dict['disagree'] = _t.get(_t.iDisagreeWithInColor) + text
			return_dict['dont_know'] = _t.get(_t.iDoNotKnowInColor) + ', ' + _t.get(_t.showMeAnArgumentFor)[0:1].lower() + _t.get(_t.showMeAnArgumentFor)[1:] + text

			return_dict['status'] = '1'
		except KeyError as e:
			logger('get_text_for_statement', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting text for a statement
	@view_config(route_name='ajax_get_premise_for_statement', renderer='json', check_csrf=False)
	def get_premise_for_statement(self):
		"""
		Returns random premisses for a statement
		:needed param self.request.params['uid']: id of the statement
		:needed param self.request.params['supportive']: does the user agrees or disagrees?
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('ajax_get_premise_for_statement', 'def', 'main')

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = {}
		try:
			logger('ajax_get_premise_for_statement', 'def', 'read params: ' + str(self.request.params))
			uid = self.request.params['uid'].split('=')[1]
			supportive = True if self.request.params['supportive'].split('=')[1].lower() == 'true' else False
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback

			# reset and save url for breadcrumbs
			url = self.request.params['url']
			BreadcrumbHelper().save_breadcrumb_for_user_with_statement_uid(transaction, self.request.authenticated_userid, url,
			                                                               uid, True, '', lang, self.request.session.id)
			# DO NOT increase weight of statement, because this is the "do not know"-trace

			logger('ajax_get_premise_for_statement', 'def', 'uid: ' + uid + ', supportive:' + str(supportive) + ', issue: ' + str(issue))

			return_dict = RecommenderHelper().get_premise_for_statement_old(transaction, uid, supportive, self.request.authenticated_userid,
			                                                                self.request.session.id, issue)

			conclusion = return_dict['currentStatement']['text'][0:1].lower() + return_dict['currentStatement']['text'][1:]
			return_dict.update(TextGenerator(lang).get_text_for_premise_for_statement(conclusion,
			                                                                          return_dict['premises'],
			                                                                          supportive,
			                                                                          UserHandler().is_user_logged_in(self.request.authenticated_userid)))


			return_dict['status'] = '1'
		except KeyError as e:
			logger('ajax_get_premise_for_statement', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting all premisses for a statement
	@view_config(route_name='ajax_get_premises_for_statement', renderer='json', check_csrf=False)
	def get_premises_for_statement(self):
		"""
		Returns all premisses for a statement
		:needed param self.request.params['uid']: id of the statement
		:needed param self.request.params['supportive']: does the user agrees or disagrees?
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_premises_for_statement', 'def', 'main')

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = {}
		try:
			logger('get_premises_for_statement', 'def', 'read params: ' + str(self.request.params))
			uid = self.request.params['uid'].split('=')[1]
			supportive = True if self.request.params['supportive'].split('=')[1].lower() == 'true' else False

			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback

			# reset and save url for breadcrumbs
			url = self.request.params['url']
			BreadcrumbHelper().save_breadcrumb_for_user_with_statement_uid(transaction, self.request.authenticated_userid, url,
			                                                               uid, True, supportive, lang, self.request.session.id)

			logger('get_premises_for_statement', 'def', 'uid: ' + uid + ', supportive ' + str(supportive) + ', issue ' + str(issue))

			return_dict = RecommenderHelper().get_premises_for_statement(transaction, uid, supportive, self.request.authenticated_userid,
			                                                             self.request.session.id, issue)
			_t = Translator(lang)
			text = return_dict['currentStatement']['text'][0:1].lower() + return_dict['currentStatement']['text'][1:]
			if len(return_dict['premises']) == 0:
				return_dict['discussion_description'] = _t.get(_t.firstPremiseText1) + ' <b>' + text + '</b>' + (' ' + _t.get(_t.doesNotHold) if not supportive else '') + '.<br><br>' + _t.get(_t.firstPremiseText2)
			else:
				return_dict['discussion_description'] = _t.get(_t.sentencesOpenersRequesting[0]) + ' <b>' + text + '</b> ' + (_t.get(_t.isTrue) if supportive else _t.get(_t.isFalse))

			return_dict['status'] = '1'
		except KeyError as e:
			logger('get_premises_for_statement', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - get reply for a premise group
	@view_config(route_name='ajax_reply_for_premisegroup', renderer='json', check_csrf=False)
	def reply_for_premisegroup(self):
		"""
		Get reply for a premise
		:needed param self.request.params['pgroup']: id of current premisegroup | combined this is an argument
		:needed param self.request.params['conclusion']: id of current conclusion | combined this is an argument
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: dictionary with every arguments
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('reply_for_premisegroup', 'def', 'main')

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = {}
		try:
			logger('reply_for_premisegroup', 'def', 'read params: ' + str(self.request.params))
			pgroup = self.request.params['pgroup'].split('=')[1]
			conclusion = self.request.params['conclusion'].split('=')[1]
			supportive = True if self.request.params['supportive'].split('=')[1].lower() == 'true' else False
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback

			logger('reply_for_premisegroup', 'def', 'issue ' + str(issue) + ', pgroup ' + str(pgroup) + ', conclusion ' + str(conclusion))

			# check for additional params, maybe they were set by breadcrumbs
			url = self.request.matchdict['url'] if 'url' in self.request.matchdict else '-'
			attack_with = ''
			attack_arg = ''
			if 'attack_with=' in url and 'attack_arg=' in url:
				pos1 = url.find('attack_with=') + len('attack_with=')
				pos2 = url.find('&', pos1)
				attack_with = url[pos1:pos2]
				pos1 = url.find('attack_arg=') + len('attack_arg=')
				pos2 = url.find('/', pos1)
				attack_arg = url[pos1:pos2]

			# get argument by system or with params, when we are navigating with breadcrumbs
			#return_dict, status = RecommenderHelper().get_attack_or_support_for_premisegroup(transaction,
			#                                                                                 self.request.authenticated_userid,
			#                                                                                 pgroup, conclusion,
			#                                                                                 self.request.session.id,
			#                                                                                 supportive, issue)

			# Track will be saved in the method, whereby we differentiate between an 'normal' request and one,
			# which was saved in the breadcrumbs to prevent the random attack
			if attack_arg is '' or attack_with is '':
				return_dict, status = RecommenderHelper().get_attack_or_support_for_premisegroup(transaction,
				                                                                                 self.request.authenticated_userid,
				                                                                                 pgroup, conclusion,
				                                                                                 self.request.session.id,
				                                                                                 supportive, issue)
				logger('reply_for_premisegroup', 'def', 'status I ' + str(status))
			else:
				return_dict, status = RecommenderHelper().get_attack_or_support_for_premisegroup_by_args(attack_with,
				                                                                                         attack_arg,
				                                                                                         pgroup,
				                                                                                         conclusion,
				                                                                                         issue)
				logger('reply_for_premisegroup', 'def', 'status II ' + str(status))

			_tg = TextGenerator(lang)
			conclusion_text = return_dict['conclusion_text'][0:1].lower() + return_dict['conclusion_text'][1:]
			relation = return_dict['relation'] if 'relation' in return_dict else None
			if status != 0:
			# rate premise, because here we have the first argument ever!
			# votes for the oposite will decreased in the WeightingHelper
				WeightingHelper().add_vote_for_argument(return_dict['argument_uid'], self.request.authenticated_userid, transaction)
				url = self.request.params['url'] # TODO better url for noticing attacking arguments
				additional_params = dict()
				additional_params['confrontation_argument_uid'] = return_dict['confrontation_argument_id']
				additional_params['attack'] = return_dict['attack']
				BreadcrumbHelper().save_breadcrumb_for_user_with_argument_parts(transaction,
				                                                                self.request.authenticated_userid,
				                                                                url,
				                                                                pgroup,
				                                                                conclusion,
				                                                                issue,
				                                                                supportive,
				                                                                self.request.session.id,
				                                                                lang,
				                                                                additional_params)
				return_dict['argument'] = QueryHelper().get_text_for_argument_uid(return_dict['argument_uid'], lang)

				return_dict['discussion_description'] = _tg.get_text_for_status_one_in_confrontation(return_dict['premise_text'],
				                                                                                     conclusion_text,
				                                                                                     relation,
				                                                                                     supportive,
				                                                                                     return_dict['attack'],
				                                                                                     url,
				                                                                                     return_dict['confrontation'],
				                                                                                     False)
				return_dict.update(_tg.get_confrontation_relation_text_dict(return_dict['confrontation'],
			                                                                conclusion_text,
			                                                                return_dict['premise_text'],
			                                                                False,
			                                                                supportive))
			else:
				return_dict['discussion_description'] = _tg.get_text_for_status_zero_in_confrontation(return_dict['premise_text'],
				                                                                                      conclusion_text,
				                                                                                      relation)

			return_dict['supportive'] = str(supportive)
			return_dict['status'] = str(status)
			return_dict['same_opinion'] = QueryHelper().get_user_with_same_opinion(return_dict['argument_uid'] if 'argument_uid' in return_dict else 0, lang) # todo use this

			transaction.commit()
		except KeyError as e:
			logger('reply_for_premisegroup', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - get reply for an argument
	@view_config(route_name='ajax_reply_for_argument', renderer='json', check_csrf=False)
	def reply_for_argument(self):
		"""
		Get reply for an argument
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['id_text']: ....
		:needed param self.request.params['pgroup']: ....
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: dictionary with every arguments
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('reply_for_argument', 'def', 'main')

		# get language
		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = {}
		try:
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			issue = issue_fallback if issue == 'undefined' else issue
			id_text = self.request.params['id_text'].split('=')[1]
			pgroup_id = self.request.params['pgroup'].split('=')[1]
			supportive = True if self.request.params['supportive'].split('=')[1].lower() == 'true' else False

			# reset and save url for breadcrumbs
			url = self.request.params['url']
			BreadcrumbHelper().save_breadcrumb_for_user_with_premissegroups_uid(transaction,
			                                                                    self.request.authenticated_userid, url,
			                                                                    id_text.split('_')[2], pgroup_id, issue,
			                                                                    self.request.session.id)

			logger('reply_for_argument', 'def', 'issue ' + str(issue) + ', id_text ' + str(id_text) + ', pgroup_id ' + str(pgroup_id) + ', supportive ' + str(supportive))
			# track will be saved in the method
			return_dict, status = RecommenderHelper().get_attack_for_argument_old(transaction,
			                                                                      self.request.authenticated_userid,
			                                                                      id_text, pgroup_id,
			                                                                      self.request.session.id, issue)

			_tg = TextGenerator(lang)
			return_dict.update(_tg.get_confrontation_relation_text_dict(return_dict['confrontation'],
			                                                            return_dict['conclusion_text'][0:1].lower() + return_dict['conclusion_text'][1],
			                                                            return_dict['premise_text'],
			                                                            False,
			                                                            supportive))

			premise = return_dict['premise_text']
			conclusion = return_dict['conclusion_text'][0:1].lower() + return_dict['conclusion_text'][1:]
			relation = return_dict['relation'] if 'relation' in return_dict else None
			if int(status) == 0:
				return_dict['discussion_description'] = _tg.get_text_for_status_zero_in_confrontation(premise, conclusion, relation)
			else:
				return_dict['discussion_description'] = _tg.get_text_for_status_one_in_confrontation(premise,
				                                                                                     conclusion,
				                                                                                     relation,
				                                                                                     supportive,
				                                                                                     return_dict['attack'],
				                                                                                     url,
				                                                                                     return_dict['confrontation'],
				                                                                                     True)

			# rate argument, cause this is between confrontations
			WeightingHelper().add_vote_for_argument(int(id_text.split('_')[2]), self.request.authenticated_userid, transaction)

			return_dict['status'] = str(status)
			return_dict['argument_uid'] = str(id_text.split('_')[2])
		except KeyError as e:
			logger('reply_for_argument', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_dict['same_opinion'] = QueryHelper().get_user_with_same_opinion(return_dict['argument_uid'] if 'argument_uid' in return_dict else 0, lang) # todo use this
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - get reply for a confrontation
	@view_config(route_name='ajax_reply_for_response_of_confrontation', renderer='json', check_csrf=False)
	def reply_for_response_of_confrontation(self):
		"""
		:needed param self.request.params['id']: x1_argument_x2, where x1 is the name of dbas confrontation and x2 the argument, which gets attacked
		:needed param self.request.params['relation']: name of the current relation. this is the attack of the user
		:needed param self.request.params['issue']: id of the issue
		:needed param self.request.params['url']: current url for the breadcrumbs
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('reply_for_response_of_confrontation', 'def', 'main')

		# get language
		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = {}
		try:
			# IMPORTANT: Supports are a special case !
			uid_text = self.request.params['id'].split('=')[1]
			relation = self.request.params['relation'].split('=')[1]
			confrontation = uid_text.split('_')[2]
			exception_rebut = True if uid_text.split('_')[1] == 'attacking' else False
			issue = self.request.params['issue'].split('=')[1] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			issue = issue_fallback if issue == 'undefined' else issue
			supportive = True if self.request.params['supportive'].split('=')[1].lower() == 'true' else False
			supportive_argument = True if 'support' in uid_text else False

			# reset and save url for breadcrumbs
			url = self.request.params['url']
			BreadcrumbHelper().save_breadcrumb_for_user_with_premissegroup_of_arguments_uid(transaction, self.request.authenticated_userid, url,
			                                                                                confrontation, issue, uid_text.split('_')[0],
			                                                                                self.request.session.id, lang)

			# track will be saved in get_reply_confrontation_response
			logger('reply_for_response_of_confrontation', 'def', 'id ' + uid_text + ', last relation ' + relation + ', confrontation ' +  confrontation + ', issue ' + str(issue) + ', exception_rebut ' + str(exception_rebut))

			# IMPORTANT: Supports are a special case !
			if 'support' in uid_text:
				logger('reply_for_response_of_confrontation', 'def', 'path a1')
				return_dict, status = RecommenderHelper().get_attack_for_argument_if_support(transaction, self.request.authenticated_userid,
				                                                                             uid_text, self.request.session.id, issue, lang)
				# rate argument, cause supports are special cases
				WeightingHelper().add_vote_for_argument(int(uid_text.split('_')[2]), self.request.authenticated_userid, transaction)

			else:
				logger('reply_for_response_of_confrontation', 'def', 'path a2')
				return_dict, status = DatabaseHelper().get_reply_confrontations_response(transaction, self.request.authenticated_userid,
				                                                                         uid_text, self.request.session.id,
				                                                                         exception_rebut, issue, lang)

			return_dict['status'] = status
			return_dict['last_relation'] = relation
			return_dict['confrontation_uid'] = confrontation
			transaction.commit()
			confrontation_text, uids = QueryHelper().get_text_for_arguments_premisesGroup_uid(confrontation, issue)

			logger('reply_for_response_of_confrontation', 'def', 'adding confrontation_text: ' + confrontation_text)
			return_dict['confrontation_text'] = confrontation_text

			# IMPORTANT: Supports are a special case !
			_tg = TextGenerator(lang)
			conclusion = return_dict['conclusion_text'][0:1].lower() + return_dict['conclusion_text'][1:]
			relation = return_dict['relation'] if 'relation' in return_dict else None
			premise = return_dict['premise_text'] if 'premise_text' in return_dict else return_dict['premisegroup']
			attack = return_dict['attack']
			attack_or_confrontation = return_dict['confrontation'] if 'confrontation' in return_dict else confrontation_text
			argument = QueryHelper().get_text_for_argument_uid((int(confrontation)), lang)

			return_dict.update(_tg.get_text_for_response_of_confrontation(argument,
			                                                              conclusion,
			                                                              relation,
			                                                              premise,
			                                                              attack,
			                                                              attack_or_confrontation,
			                                                              supportive,
			                                                              'support' in uid_text,
			                                                              supportive_argument,
			                                                              self.request.authenticated_userid,
			                                                              url,
			                                                              status))
			return_dict['same_opinion'] = QueryHelper().get_user_with_same_opinion(int(uid_text.split('_')[2]), lang) # todo use this


		except KeyError as e:
			logger('reply_for_response_of_confrontation', 'error', repr(e))
			return_dict['status'] = '-1'

		return_dict['logged_in'] = self.request.authenticated_userid
		return_dict['history'] = BreadcrumbHelper().get_breadcrumbs_of_user(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	#######################################
	## ADDTIONAL AJAX STUFF # USER THINGS #
	#######################################

	# ajax - getting every user, and returns dicts with name <-> group
	@view_config(route_name='ajax_all_users', renderer='json', check_csrf=False)
	def get_all_users(self):
		"""
		Returns all users as dictionary with name <-> group
		:return: json-dict() of all users
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_all_users', 'def', 'main')

		return_dict = UserHandler().get_all_users(self.request.authenticated_userid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting complete track of the user
	@view_config(route_name='ajax_get_user_track', renderer='json', check_csrf=True)
	def get_user_track(self):
		"""
		Request the complete user track
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		logger('get_user_track', 'def', 'main')

		nickname = 'unknown'
		try:
			logger('get_user_track', 'def', 'read params')
			nickname = str(self.request.authenticated_userid)
			logger('get_user_track', 'def', 'nickname ' + nickname)
		except KeyError as e:
			logger('get_user_track', 'error', repr(e))

		logger('manage_user_track', 'def', 'get track data')
		return_dict = TrackingHelper().get_track_of_user(nickname, lang)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - deleting complete track of the user
	@view_config(route_name='ajax_delete_user_track', renderer='json', check_csrf=True)
	def delete_user_track(self):
		"""
		Request the complete user track
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('delete_user_track', 'def', 'main')

		nickname = 'unknown'
		try:
			logger('delete_user_track', 'def', 'read params')
			nickname = str(self.request.authenticated_userid)
			logger('delete_user_track', 'def', 'nickname ' + nickname)
		except KeyError as e:
			logger('delete_user_track', 'error', repr(e))

		logger('delete_user_track', 'def', 'remove track data')
		TrackingHelper().del_track_of_user(transaction, nickname)
		return_dict = dict()
		return_dict['removed_data'] = 'true' # necessary
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - getting complete track of the user
	@view_config(route_name='ajax_get_user_history', renderer='json', check_csrf=True)
	def get_user_history(self):
		"""
		Request the complete user track
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_user_history', 'def', 'main')

		nickname = 'unknown'
		try:
			logger('get_user_history', 'def', 'read params')
			nickname = str(self.request.authenticated_userid)
			logger('get_user_history', 'def', 'nickname ' + nickname)
		except KeyError as e:
			logger('get_user_history', 'error', repr(e))

		logger('get_user_history', 'def', 'get history data')
		return_dict = BreadcrumbHelper().get_breadcrumbs_of_user(nickname)
		logger('get_user_history', 'def', str(return_dict))
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - deleting complete history of the user
	@view_config(route_name='ajax_delete_user_history', renderer='json', check_csrf=True)
	def delete_user_history(self):
		"""
		Request the complete user history
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('delete_user_history', 'def', 'main')

		nickname = 'unknown'
		try:
			logger('delete_user_history', 'def', 'read params')
			nickname = str(self.request.authenticated_userid)
			logger('delete_user_history', 'def', 'nickname ' + nickname)
		except KeyError as e:
			logger('delete_user_history', 'error', repr(e))

		logger('delete_user_history', 'def', 'remove history data')
		BreadcrumbHelper().del_breadcrumbs_of_user(transaction, nickname)
		return_dict = dict()
		return_dict['removed_data'] = 'true' # necessary
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - user login
	@view_config(route_name='ajax_user_login', renderer='json')
	def user_login(self):
		"""
		Will login the user by his nickname and password
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_login', 'def', 'main')

		success = '0'
		message = ''
		return_dict = {}

		try:
			nickname = self.escape_string(self.request.params['user'])
			password = self.escape_string(self.request.params['password'])
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

	# ajax - user login
	@view_config(route_name='ajax_user_logout', renderer='json')
	def user_logout(self):
		"""
		Will logout the user
		:return: HTTPFound with forgotten headers
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_logout', 'def', 'main')

		url = self.request.params['url']
		logger('user_logout', 'def', 'url: ' + url)

		if 'setting' in url:
			url = self.request.application_url
			logger('user_logout', 'def', 'redirect: ' + url)

		headers = forget(self.request)
		return HTTPFound(
			location=url,
			headers=headers,
		)

	# ajax - registration of users
	@view_config(route_name='ajax_user_registration', renderer='json')
	def user_registration(self):
		"""
		Registers new user
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_registration', 'def', 'main')

		# default values
		success = '0'
		message = ''
		return_dict = {}

		# getting params
		try:
			params          = self.request.params
			firstname       = self.escape_string(params['firstname'])
			lastname        = self.escape_string(params['lastname'])
			nickname        = self.escape_string(params['nickname'])
			email           = self.escape_string(params['email'])
			gender          = self.escape_string(params['gender'])
			password        = self.escape_string(params['password'])
			passwordconfirm = self.escape_string(params['passwordconfirm'])
			lang            = self.request.params['lang']
			logger('user_registration', 'def', 'params firstname: ' + str(firstname)
			       + ', lastname: ' + str(lastname)
			       + ', nickname: ' + str(nickname)
			       + ', email: ' + str(email)
			       + ', password: ' + str(password)
			       + ', passwordconfirm: ' + str(passwordconfirm)
			       + ', lang: ' + lang)

			_t = Translator(lang)

			# database queries mail verification
			db_nick = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
			db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
			logger('user_registration', 'main', 'Validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# are the password equal?
			if not password == passwordconfirm:
				logger('user_registration', 'main', 'Passwords are not equal')
				message = _t.get(_t.pwdNotEqual)
			# is the nick already taken?
			elif db_nick:
				logger('user_registration', 'main', 'Nickname \'' + nickname + '\' is taken')
				message = _t.get(_t.nickIsTaken)
			# is the email already taken?
			elif db_mail:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is taken')
				message = _t.get(_t.mailIsTaken)
			# is the email valid?
			elif not is_mail_valid:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is not valid')
				message = _t.get(_t.mailNotValid)
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
					message = _t.get(_t.errorTryLateOrContant)
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
						message = _t.get(_t.accountWasAdded)
						success = '1'

						# sending an email
						subject = 'D-BAS Account Registration'
						body = _t.get(_t.accountWasRegistered)
						EmailHelper().send_mail(self.request, subject, body, email, lang)

					else:
						logger('user_registration', 'main', 'New data was not added')
						message = _t.get(_t.accoutErrorTryLateOrContant)

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
		Sends an email, when the user requests his password
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_password_request', 'def', 'main')

		success = '0'
		message = ''
		return_dict = {}

		try:
			email = self.escape_string(self.request.params['email'])
			lang = self.request.params['lang']
			logger('user_password_request', 'def', 'params email: ' + str(email) + ', lang ' + lang)
			success = '1'
			_t = Translator(lang)

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

				body = _t.get(_t.nicknameIs) + db_user.nickname + '\n'
				body += _t.get(_t.newPwdIs) + pwd
				subject = _t.get(_t.dbasPwdRequest)
				reg_success, message= EmailHelper().send_mail(self.request, subject, body, email, lang)

				# logger
				if reg_success:
					logger('user_password_request', 'form.passwordrequest.submitted', 'New password was sent')
					success = '1'
				else:
					logger('user_password_request', 'form.passwordrequest.submitted', 'Error occured')
			else:
				logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
				message = 'emailUnknown'


		except KeyError as e:
			logger('user_password_request', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	##########################################
	## ADDTIONAL AJAX STUFF # SET NEW THINGS #
	##########################################

	# ajax - send new start statement
	@view_config(route_name='ajax_set_new_start_statement', renderer='json', check_csrf=True)
	def set_new_start_statement(self):
		"""
		Inserts a new statement into the database, which should be available at the beginning
		:return: a status code, if everything was successfull
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_new_start_statement', 'def', 'main')

		return_dict = {}
		try:
			statement = self.request.params['statement']
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			issue = issue_fallback if issue == 'undefined' else issue
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

	# ajax - send new start premise
	@view_config(route_name='ajax_set_new_start_premise', renderer='json', check_csrf=True)
	def set_new_start_premise(self):
		"""
		Sets new premise for the start
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)

		logger('set_new_start_premise', 'def', 'main')

		return_dict = dict()
		try:
			logger('set_new_start_premise', 'def', 'getting params')
			text = self.escape_string(self.request.params['text'])
			conclusion_id = self.request.params['conclusion_id']
			support = True if self.request.params['support'].lower() == 'true' else False
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			issue = issue_fallback if issue == 'undefined' else issue
			logger('set_new_start_premise', 'def', 'conclusion_id: ' + str(conclusion_id) + ', text: ' + text + ', supportive: ' +
			       str(support) + ', issue: ' + str(issue))

			tmp_dict, is_duplicate = DatabaseHelper().set_premises_for_conclusion(transaction, user_id, text, conclusion_id, support, issue)

			return_dict['pro_0'] = tmp_dict
			if is_duplicate:
				return_dict['premisegroup_uid'] = tmp_dict['premisegroup_uid']
			return_dict['status'] = '0' if is_duplicate else '1'
		except KeyError as e:
			logger('set_new_start_premise', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - send new premises
	@view_config(route_name='ajax_set_new_premises_for_x', renderer='json', check_csrf=True)
	def set_new_premises_for_x(self):
		"""
		Sets a new premisse for statement, argument, ? Everything is possible
		:return: json-dict()
		"""
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')

		logger('set_new_premises_for_x', 'def', 'main')

		return_dict = dict()
		try:
			logger('set_new_premises_for_x', 'def', 'getting params')
			pro_dict = dict()
			con_dict = dict()

			related_argument  = self.request.params['related_argument'] if 'related_argument' in self.request.params else -1
			premisegroup_id   = self.request.params['premisegroup_id'] if 'premisegroup_id' in self.request.params else -1
			current_attack    = self.request.params['current_attack'] if 'current_attack' in self.request.params else -1
			last_attack       = self.request.params['last_attack'] if 'last_attack' in self.request.params else -1
			confrontation_uid = self.request.params['confrontation_uid'] if 'confrontation_uid' in self.request.params else -1
			premisegroup_con  = self.request.params['premisegroup_con'] if 'premisegroup_con' in self.request.params else '0'
			premisegroup_pro  = self.request.params['premisegroup_pro'] if 'premisegroup_pro' in self.request.params else '0'
			exception_rebut   = self.request.params['exceptionForRebut'] if 'exceptionForRebut' in self.request.params else '0'
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			issue = issue_fallback if issue == 'undefined' else issue

			premisegroup_con = True if premisegroup_con.lower() == 'true' else False
			premisegroup_pro = True if premisegroup_pro.lower() == 'true' else False
			exception_rebut  = True if exception_rebut.lower() == 'true' else False

			logger('set_new_premises_for_x', 'def', 'param related_argument: ' + str(related_argument)
			       + ', param premisegroup_id: ' + str(premisegroup_id)
			       + ', param current_attack: ' + str(current_attack)
			       + ', param last_attack: ' + str(last_attack)
			       + ', param confrontation_uid: ' + str(confrontation_uid)
			       + ', param premisegroup_con: ' + str(premisegroup_con)
			       + ', param premisegroup_pro: ' + str(premisegroup_pro)
			       + ', param issue: ' + str(issue)
			       + ', param exception_rebut: ' + str(exception_rebut))

			# confrontation_uid is a premise group

			# Interpretation of the parameters
			# User says: E => A             | #related_argument
			# System says:
			#   undermine:  F => !E         | #premisegroup_id  =>  !premisegroup of #related_argument
			#   undercut:   D => !(E=>A)    | #premisegroup_id  =>  !#related_argument
			#   rebut:      B => !A         | #premisegroup_id  =>  !conclusion of #related_argument
			# Handle it, based on current and last attack

			# getting all arguments
			for key in self.request.params:
				logger('set_new_premises_for_x', key, self.request.params[key])
				if 'pro_' in key:
					pro_dict[key] = self.escape_string(self.request.params[key])
				if 'con_' in key:
					con_dict[key] = self.escape_string(self.request.params[key])

			return_dict['status'] = '1'
			return_dict.update(DatabaseHelper().handle_inserting_new_statements(
				user = user_id,
				pro_dict = pro_dict,
				con_dict = con_dict,
				transaction = transaction,
				argument_id = related_argument,
				premisegroup_id = premisegroup_id,
				current_attack = current_attack,
				last_attack = last_attack,
				premisegroup_con = premisegroup_con,
				premisegroup_pro = premisegroup_pro,
				issue = issue,
				exception_rebut = exception_rebut
			))

		except KeyError as e:
			logger('set_new_premises_for_x', 'error', repr(e))
			return_dict['status'] = '-1'

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		logger('set_new_premises_for_x', 'def', 'returning')
		return return_json

	# ajax - set new textvalue for a statement
	@view_config(route_name='ajax_set_correcture_of_statement', renderer='json', check_csrf=True)
	def set_correcture_of_statement(self):
		"""
		Sets a new textvalue for a statement
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_correcture_of_statement', 'def', 'main')

		try:
			uid = self.request.params['uid']
			corrected_text = self.escape_string(self.request.params['text'])
			is_final = self.request.params['final']
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			logger('set_correcture_of_statement', 'def', 'params uid: ' + str(uid) + ', corrected_text: ' + str(corrected_text)
			       + ', final ' + str(is_final))
			return_dict = DatabaseHelper().correct_statement(transaction, self.request.authenticated_userid, uid, corrected_text,
			                                                 is_final, issue)
		except KeyError as e:
			return_dict = dict()
			logger('set_correcture_of_statement', 'error', repr(e))

		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	######################################
	## ADDTIONAL AJAX STUFF # GET THINGS #
	######################################

	# ajax - getting changelog of a statement
	@view_config(route_name='ajax_get_logfile_for_statement', renderer='json', check_csrf=False)
	def get_logfile_for_statement(self):
		"""
		Returns the changelog of a statement
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_logfile_for_statement', 'def', 'main')

		return_dict = dict()
		try:
			uid = self.request.params['uid']
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback
			logger('get_logfile_for_statement', 'def', 'params uid: ' + str(uid))
			return_dict = DatabaseHelper().get_logfile_for_statement(uid, issue)
		except KeyError as e:
			logger('get_logfile_for_statement', 'error', repr(e))

		# return_dict = DatabaseHelper().get_logfile_for_premisegroup(uid)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for shorten url
	@view_config(route_name='ajax_get_everything_for_island_view', renderer='json')
	def get_everything_for_island_view(self):
		"""
		Everthing for the island view
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_everything_for_island_view', 'def', 'main')

		return_dict = {}
		try:
			arg_uid = self.request.params['arg_uid']
			lang = self.request.params['lang']
			logger('get_everything_for_island_view', 'def', 'params arg_uid ' + str(arg_uid))

			return_dict = DatabaseHelper().get_everything_for_island_view(arg_uid, lang)
			return_dict.update(TextGenerator(lang).get_relation_text_dict_without_confrontation(return_dict['premise'],
			                                                                                    return_dict['conclusion'],
			                                                                                    False))

			return_dict['status'] = '1'
			logger('get_everything_for_island_view', 'return', str(return_dict))

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
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('get_shortened_url', 'def', 'main')

		return_dict = {}
		# google_api_key = 'AIzaSyAw0aPsBsAbqEJUP_zJ9Fifbhzs8xkNSw0' # browser is
		# google_api_key = 'AIzaSyDneaEJN9FNGUpXHDZahe9Rhb21FsFNS14' # server id
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

			# shortener = Shortener(service, api_key=google_api_key)
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
		Returns all attacks, done by the users
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')

		logger('get_attack_overview', 'def', 'main')
		lang = self.request.params['lang']
		issue = self.request.params['issue'] if 'issue' in self.request.params \
			else self.request.session['issue'] if 'issue' in self.request.session \
			else issue_fallback
		return_dict = DatabaseHelper().get_attack_overview(self.request.authenticated_userid, issue, lang)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for attack overview
	@view_config(route_name='ajax_get_issue_list', renderer='json')
	def get_issue_list(self):
		"""
		Returns all issues
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')

		logger('get_issue_list', 'def', 'main')

		try:
			lang = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			lang = get_current_registry().settings['pyramid.default_locale_name']

		return_dict = DatabaseHelper().get_issue_list(lang)
		issue = self.request.params['issue'] if 'issue' in self.request.params \
			else self.request.session['issue'] if 'issue' in self.request.session \
			else issue_fallback
		return_dict['current_issue'] = issue
		return_dict['current_issue_arg_count'] = QueryHelper().get_number_of_arguments(issue)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for getting all news
	@view_config(route_name='ajax_get_news', renderer='json')
	def get_news(self):
		"""
		ajax interface for getting news
		:return: json-set with all news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_news', 'def', 'main')
		return_dict = DatabaseHelper().get_news()
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for getting database
	@view_config(route_name='ajax_get_database_dump', renderer='json')
	def get_database_dump(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_database_dump', 'def', 'main')
		issue = self.request.params['issue'] if 'issue' in self.request.params \
			else self.request.session['issue'] if 'issue' in self.request.session \
			else issue_fallback
		return_dict = DatabaseHelper().get_dump(issue)
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json


	###########################################
	## ADDTIONAL AJAX STUFF # ADDITION THINGS #
	###########################################

	# ajax - for language switch
	@view_config(route_name='ajax_switch_language', renderer='json')
	def switch_language(self):
		"""
		Switches the language
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
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

	# ajax - for sending news
	@view_config(route_name='ajax_send_news', renderer='json')
	def send_news(self):
		"""
		ajax interface for settings news
		:return: json-set with new news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')

		try:
			title = self.escape_string(self.request.params['title'])
			text = self.escape_string(self.request.params['text'])
			return_dict = DatabaseHelper().set_news(transaction, title, text, self.request.authenticated_userid)
		except KeyError as e:
			return_dict = dict()
			logger('ajax_send_news', 'error', repr(e))
			return_dict['status'] = '-1'

		logger('send_news', 'def', 'main')
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for fuzzy search
	@view_config(route_name='ajax_fuzzy_search', renderer='json')
	def fuzzy_search(self):
		"""
		ajax interface for fuzzy string search
		:return: json-set with all matched strings
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('fuzzy_search', 'main', 'def')
		try:
			value = self.request.params['value']
			mode = str(self.request.params['type'])
			issue = self.request.params['issue'] if 'issue' in self.request.params \
				else self.request.session['issue'] if 'issue' in self.request.session \
				else issue_fallback

			logger('fuzzy_search', 'main', 'value: ' + str(value) + ', mode: ' + str(mode) + ', issue: ' + str(issue))
			if mode == '0': # start statement
				return_dict = FuzzyStringMatcher().get_fuzzy_string_for_start(value, issue, True)
			elif mode == '1': # edit statement popup
				statement_uid = self.request.params['extra']
				return_dict = FuzzyStringMatcher().get_fuzzy_string_for_edits(value, statement_uid, issue)
			elif mode == '2':  # start premise
				return_dict = FuzzyStringMatcher().get_fuzzy_string_for_start(value, issue, False)
			elif mode == '3':  # adding reasons
				return_dict = FuzzyStringMatcher().get_fuzzy_string_for_reasons(value, issue)
			else:
				logger('fuzzy_search', 'main', 'unkown mode: ' + str(mode))
				return_dict = dict()
		except KeyError as e:
			return_dict = dict()
			logger('fuzzy_search', 'error', repr(e))
		return_json = DictionaryHelper().dictionary_to_json_array(return_dict, True)

		return return_json

	# ajax - for additional service
	@view_config(route_name='ajax_additional_service', renderer='json')
	def additional_service(self):
		"""

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('additional_service', 'main', 'def')
		rtype = self.request.params['type']

		if rtype == "chuck":
			data = requests.get('http://api.icndb.com/jokes/random')
		else:
			data = requests.get('http://api.yomomma.info/')

		for a in data.json():
			logger('additional_service', 'main', str(a) + ': ' + str(data.json()[a]))

		return data.json()