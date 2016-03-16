import transaction
import datetime
import requests

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid.renderers import get_renderer
from pyramid.threadlocal import get_current_registry
from pyshorteners.shorteners import Shortener

from .database import DBDiscussionSession
from .database.discussion_model import User, Group, Issue, Argument, Notification, Settings
from .dictionary_helper import DictionaryHelper
from .email import EmailHelper
from .logger import logger
from .query_helper import QueryHelper
from .strings import Translator
from .string_matcher import FuzzyStringMatcher
from .breadcrumb_helper import BreadcrumbHelper
from .recommender_system import RecommenderHelper
from .user_management import PasswordGenerator, PasswordHandler, UserHandler
from .voting_helper import VotingHelper
from .url_manager import UrlManager
from .notification_helper import NotificationHelper

name = 'D-BAS'
version = '0.5.7a'
header = name + ' ' + version
issue_fallback = 1
mainpage = ''

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class Dbas(object):

	def __init__(self, request):
		"""
		Object initialization
		:param request: init http request
		:return: json-dict()
		"""
		self.request = request
		self.user_login_timeout = '1200'
		global mainpage
		mainpage = request.application_url
		self.issue_fallback = DBDiscussionSession.query(Issue).first().uid

	def escape_string(self, text):
		"""

		:param text:
		:return: json-dict()
		"""
		return text  # todo escaping string correctly
		# return re.escape(text)

	def base_layout(self):
		renderer = get_renderer('templates/basetemplate.pt')
		layout = renderer.implementation().macros['layout']
		return layout

	def get_nickname_and_session(self, for_api, api_data):
		"""
		Given data from api, return nickname and session_id.
		:param for_api:
		:param api_data:
		:return:
		"""
		nickname = api_data["nickname"] if api_data and for_api else self.request.authenticated_userid
		session_id = api_data["session_id"] if api_data and for_api else self.request.session.id
		return nickname, session_id

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
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)
		DictionaryHelper().add_language_options_for_extra_dict(extras_dict, ui_locales)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Main',
			'project': header,
			'extras': extras_dict
		}

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		"""
		View configuration for the contact view.
		:return: dictionary with title and project username as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_contact', 'def', 'main, self.request.params: ' + str(self.request.params))
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		contact_error = False
		send_message = False
		message = ''

		try:
			ui_locales = str(self.request.cookies['_LOCALE_'])
		except KeyError:
			ui_locales = get_current_registry().settings['pyramid.default_locale_name']

		username        = self.request.params['name'] if 'name' in self.request.params else ''
		email           = self.request.params['mail'] if 'mail' in self.request.params else ''
		phone           = self.request.params['phone'] if 'phone' in self.request.params else ''
		content         = self.request.params['content'] if 'content' in self.request.params else ''
		spam            = self.request.params['spam'] if 'spam' in self.request.params else ''
		request_token   = self.request.params['csrf_token'] if 'csrf_token' in self.request.params else ''
		spamquestion    = ''

		if 'form.contact.submitted' not in self.request.params:
			# get anti-spam-question
			spamquestion, answer = UserHandler().get_random_anti_spam_question(ui_locales)
			# save answer in session
			self.request.session['antispamanswer'] = answer
			token = self.request.session.new_csrf_token()

		else:
			_t = Translator(ui_locales)
			token = self.request.session.get_csrf_token()

			logger('main_contact', 'form.contact.submitted', 'validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# sanity checks
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
			elif (not spam) or (not (int(spam) == int(self.request.session['antispamanswer']))):
				logger('main_contact', 'form.contact.submitted', 'empty or wrong anti-spam answer' + ', given answer ' + spam + ', right answer ' + str(self.request.session['antispamanswer']))
				contact_error = True
				message = _t.get(_t.maliciousAntiSpam)

			# is the token valid?
			elif request_token != token:
				logger('main_contact', 'form.contact.submitted', 'token is not valid' + ', request_token: ' + str(request_token) + ', token: ' + str(token))
				message = _t.get(_t.nonValidCSRF)
				contact_error = True

			else:
				subject = 'Contact D-BAS'
				body = _t.get(_t.name) + ': ' + username + '\n'\
				       + _t.get(_t.mail) + ': ' + email + '\n'\
				       + _t.get(_t.phone) + ': ' + phone + '\n'\
				       + _t.get(_t.message) + ':\n' + content
				EmailHelper().send_mail(self.request, subject, body, 'dbas.hhu@gmail.com', ui_locales)
				body = '* THIS IS A COPY OF YOUR MAIL *\n\n' + body
				subject = '[INFO] ' + subject
				send_message, message = EmailHelper().send_mail(self.request, subject, body, email, ui_locales)
				contact_error = not send_message
				if send_message:
					spamquestion, answer = UserHandler().get_random_anti_spam_question(ui_locales)

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)
		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Contact',
			'project': header,
			'extras': extras_dict,
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

	# content page
	@view_config(route_name='discussion_init', renderer='templates/content.pt', permission='everybody')
	def discussion_init(self, for_api=False, api_data=None):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:param api_data: Dictionary, containing data of a user who logged in via API
		:return: dictionary
		"""
		# '/a*slug'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_init', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))

		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		UserHandler().update_last_action(transaction, nickname)

		if for_api and api_data:
			try:
				logged_in = api_data["nickname"]
			except KeyError:
				logged_in = None
		else:
			logged_in = self.request.authenticated_userid

		_qh = QueryHelper()
		_dh = DictionaryHelper()
		if for_api:
			slug = self.request.matchdict['slug'] if 'slug' in self.request.matchdict else ''
		else:
			slug = self.request.matchdict['slug'][0] if 'slug' in self.request.matchdict and len(self.request.matchdict['slug']) > 0 else ''

		issue           = _qh.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else _qh.get_issue_id(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)
		item_dict       = _dh.prepare_item_dict_for_start(issue, logged_in, ui_locales, mainpage, for_api)

		breadcrumbs, has_new_crumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, nickname, session_id, transaction, ui_locales)

		discussion_dict = _dh.prepare_discussion_dict_for_start(ui_locales, breadcrumbs, nickname, session_id)
		extras_dict     = _dh.prepare_extras_dict(slug, True, True, False, True, False, True, ui_locales, nickname,
		                                          application_url=mainpage, for_api=for_api)

		if len(item_dict) == 0:
			_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, ui_locales, at_start=True)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# attitude page
	@view_config(route_name='discussion_attitude', renderer='templates/content.pt', permission='everybody')
	def discussion_attitude(self, for_api=False, api_data=None):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:param api_data:
		:return: dictionary
		"""
		# '/discuss/{slug}/attitude/{statement_id}'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_attitude', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		UserHandler().update_last_action(transaction, nickname)

		_qh = QueryHelper()
		_dh = DictionaryHelper()
		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		statement_id    = matchdict['statement_id'][0] if 'statement_id' in matchdict else ''

		issue           = _qh.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else _qh.get_issue_id(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)
		breadcrumbs, has_new_crumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, nickname, session_id, transaction, ui_locales)

		discussion_dict = _dh.prepare_discussion_dict_for_attitude(statement_id, ui_locales, breadcrumbs, nickname, session_id)
		if not discussion_dict:
			return HTTPFound(location= UrlManager(mainpage, for_api=for_api).get_404([slug, statement_id]))

		item_dict       = _dh.prepare_item_dict_for_attitude(statement_id, issue, ui_locales, mainpage, for_api)
		extras_dict     = _dh.prepare_extras_dict(issue_dict['slug'], False, False, True, True, False, True, ui_locales,
		                                          nickname, application_url=mainpage, for_api=for_api)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# justify page
	@view_config(route_name='discussion_justify', renderer='templates/content.pt', permission='everybody')
	def discussion_justify(self, for_api=False, api_data=None):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:param api_data:
		:return: dictionary
		"""
		# '/discuss/{slug}/justify/{statement_or_arg_id}/{mode}*relation'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		nickname, session_id = self.get_nickname_and_session(for_api, api_data)

		_uh = UserHandler()
		timed_out =_uh.update_last_action(transaction, nickname)
		logged_in = _uh.is_user_logged_in(nickname)

		_qh = QueryHelper()
		_dh = DictionaryHelper()

		slug                = matchdict['slug'] if 'slug' in matchdict else ''
		statement_or_arg_id = matchdict['statement_or_arg_id'] if 'statement_or_arg_id' in matchdict else ''
		mode                = matchdict['mode'] if 'mode' in matchdict else ''
		supportive          = mode == 't' or mode == 'd'  # supportive = t or dont know mode
		relation            = matchdict['relation'][0] if len(matchdict['relation']) > 0 else ''
		# related_arg         = matchdict['relation'][1] if len(matchdict['relation']) > 1 else -1

		issue               = _qh.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else _qh.get_issue_id(self.request)
		ui_locales          = _qh.get_language(self.request, get_current_registry())
		issue_dict          = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)
		breadcrumbs, has_new_crumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, nickname, session_id, transaction, ui_locales)

		if [c for c in ('t', 'f') if c in mode] and relation == '':
			if not QueryHelper().get_text_for_statement_uid(statement_or_arg_id):
				return HTTPFound(location= UrlManager(mainpage, for_api=for_api).get_404([slug, statement_or_arg_id]))

			VotingHelper().add_vote_for_statement(statement_or_arg_id, nickname, supportive, transaction)
			# justifying position
			item_dict       = _dh.prepare_item_dict_for_justify_statement(statement_or_arg_id, nickname, issue,
			                                                              supportive, ui_locales, mainpage, for_api)
			discussion_dict = _dh.prepare_discussion_dict_for_justify_statement(nickname, transaction, statement_or_arg_id,
			                                                                    ui_locales, breadcrumbs, has_new_crumbs,
			                                                                    supportive, nickname, len(item_dict), session_id)
			extras_dict     = _dh.prepare_extras_dict(slug, True, True, False, True, False, True, ui_locales,
			                                          nickname, mode == 't', application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0 or len(item_dict) == 1 and logged_in:
				_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, ui_locales,
				                            at_justify=True, current_premise=_qh.get_text_for_statement_uid(statement_or_arg_id))

		elif 'd' in mode and relation == '':
			# dont know
			argument_uid    = RecommenderHelper().get_argument_by_conclusion(statement_or_arg_id, supportive)
			discussion_dict = _dh.prepare_discussion_dict_for_dont_know_reaction(nickname, transaction, argument_uid,
			                                                                     ui_locales, breadcrumbs, has_new_crumbs, session_id)
			item_dict       = _dh.prepare_item_dict_for_dont_know_reaction(argument_uid, supportive, issue, ui_locales, mainpage, for_api)
			extras_dict     = _dh.prepare_extras_dict(slug, False, False, False, True, True, True, ui_locales, nickname,
			                                          argument_id=argument_uid, application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0:
				_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, ui_locales, at_dont_know=True,
				                            current_premise=_qh.get_text_for_statement_uid(statement_or_arg_id))

		elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
			# justifying argument
			# is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
			item_dict       = _dh.prepare_item_dict_for_justify_argument(statement_or_arg_id, relation, issue, ui_locales,
			                                                             mainpage, for_api, logged_in)

			discussion_dict = _dh.prepare_discussion_dict_for_justify_argument(nickname, statement_or_arg_id, ui_locales,
			                                                                   supportive, relation, nickname, breadcrumbs,
			                                                                   has_new_crumbs, len(item_dict), session_id,
			                                                                   transaction)
			extras_dict     = _dh.prepare_extras_dict(slug, True, True, False, True, True, True, ui_locales, nickname,
			                                          argument_id=statement_or_arg_id, application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if not logged_in and len(item_dict) == 0 or logged_in and len(item_dict) == 1:
				_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, ui_locales, at_justify_argumentation=True)
		else:
			return HTTPFound(location= UrlManager(mainpage, for_api=for_api).get_404([slug, 'justify', statement_or_arg_id, mode, relation]))

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# reaction page
	@view_config(route_name='discussion_reaction', renderer='templates/content.pt', permission='everybody')
	def discussion_reaction(self, for_api=False, api_data=None):
		"""
		View configuration for the content view.
		:param for_api: Boolean
		:param api_data:
		:return: dictionary
		"""
		# '/discuss/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_reaction', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		arg_id_user     = matchdict['arg_id_user'] if 'arg_id_user' in matchdict else ''
		attack          = matchdict['mode'] if 'mode' in matchdict else ''
		arg_id_sys      = matchdict['arg_id_sys'] if 'arg_id_sys' in matchdict else ''
		supportive      = DBDiscussionSession.query(Argument).filter_by(uid=arg_id_user).first().is_supportive
		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		UserHandler().update_last_action(transaction, nickname)

		# set votings
		VotingHelper().add_vote_for_argument(arg_id_user, nickname, transaction)

		_qh = QueryHelper()
		_dh = DictionaryHelper()

		issue           = _qh.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else _qh.get_issue_id(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		breadcrumbs, has_new_crumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, nickname,
		                                                                 session_id, transaction, ui_locales)

		discussion_dict = _dh.prepare_discussion_dict_for_argumentation(nickname, transaction, arg_id_user, ui_locales,
		                                                                breadcrumbs, has_new_crumbs, supportive, arg_id_sys,
		                                                                attack, session_id)
		item_dict       = _dh.prepare_item_dict_for_reaction(arg_id_sys, arg_id_user, supportive, issue, attack, ui_locales,
		                                                     mainpage, for_api)
		extras_dict     = _dh.prepare_extras_dict(slug, False, False, True, True, True, True, ui_locales, nickname,
		                                          argument_id=arg_id_user, application_url=mainpage, for_api=for_api)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# choosing page
	@view_config(route_name='discussion_choose', renderer='templates/content.pt', permission='everybody')
	def discussion_choose(self, for_api=False, api_data=None):
		"""
		View configuration for the choosing view.
		:param for_api: Boolean
		:param api_data:
		:return: dictionary
		"""
		# '/discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids'
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('discussion_reaction', 'def', 'main, self.request.matchdict: ' + str(self.request.matchdict))
		matchdict = self.request.matchdict

		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		is_argument     = matchdict['is_argument'] if 'is_argument' in matchdict else ''
		is_supportive   = matchdict['supportive'] if 'supportive' in matchdict else ''
		uid             = matchdict['id'] if 'id' in matchdict else ''
		pgroup_ids      = matchdict['pgroup_ids'] if 'id' in matchdict else ''
		nickname, session_id = self.get_nickname_and_session(for_api, api_data)

		is_argument = True if is_argument is 't' else False
		is_supportive = True if is_supportive is 't' else False

		_qh = QueryHelper()
		_dh = DictionaryHelper()

		issue           = _qh.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else _qh.get_issue_id(self.request)
		ui_locales      = _qh.get_language(self.request, get_current_registry())
		issue_dict      = _qh.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		UserHandler().update_last_action(transaction, nickname)
		breadcrumbs, has_new_crumbs = BreadcrumbHelper().save_breadcrumb(self.request.path, nickname, session_id, transaction, ui_locales)

		discussion_dict = _dh.prepare_discussion_dict_for_choosing(uid, ui_locales, is_argument, is_supportive, breadcrumbs, nickname, session_id)
		item_dict       = _dh.prepare_item_dict_for_choosing(uid, pgroup_ids, is_argument, is_supportive, ui_locales,
		                                                     mainpage, issue, for_api)
		extras_dict     = _dh.prepare_extras_dict(slug, False, False, False, True, False, True, True, ui_locales, nickname,
		                                          application_url=mainpage, for_api=for_api)

		return_dict = dict()
		return_dict['issues'] = issue_dict
		return_dict['discussion'] = discussion_dict
		return_dict['items'] = item_dict
		return_dict['extras'] = extras_dict

		if for_api:
			return return_dict
		else:
			return_dict['layout'] = self.base_layout()
			return_dict['language'] = str(ui_locales)
			return_dict['title'] = issue_dict['title']
			return_dict['project'] = header
			return return_dict

	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_settings', 'def', 'main, self.request.params: ' + str(self.request.params))
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		_tn = Translator(ui_locales)

		old_pw      = ''
		new_pw      = ''
		confirm_pw  = ''
		message     = ''
		error       = False
		success     = False

		db_user     = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
		db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
		_uh         = UserHandler()
		edits       = _uh.get_count_of_statements_of_user(db_user, True)
		statements  = _uh.get_count_of_statements_of_user(db_user, False)
		arg_vote, stat_vote = _uh.get_count_of_votes_of_user(db_user)

		if db_user and 'form.passwordchange.submitted' in self.request.params:
			old_pw = self.request.params['passwordold']
			new_pw = self.request.params['password']
			confirm_pw = self.request.params['passwordconfirm']

			message, error, success = _uh.change_password(transaction, db_user, old_pw, new_pw, confirm_pw, ui_locales)

		# get gravater profile picture
		gravatar_url = _uh.get_profile_picture(db_user)

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)
		settings_dict = {
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
			'edits_done': edits,
			'statemens_posted': statements,
			'discussion_arg_votes': arg_vote,
			'discussion_stat_votes': stat_vote,
			'send_mails': db_settings.should_send_mails,
			'send_notifications': db_settings.should_send_notifications,
			'title_mails': _tn.get(_tn.mailSettingsTitle),
			'title_notifications': _tn.get(_tn.notificationSettingsTitle)
		}

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Settings',
			'project': header,
			'extras': extras_dict,
			'settings': settings_dict
		}

	# message page, when logged in
	@view_config(route_name='main_notification', renderer='templates/notifications.pt', permission='use')
	def main_notifications(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_notifications', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Messages',
			'project': header,
			'extras': extras_dict
		}

	# admin page, when logged in
	@view_config(route_name='main_admin', renderer='templates/admin.pt', permission='everybody')  # or permission='use'
	def main_admin(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_admin', 'def', 'main')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		_qh = QueryHelper()
		ui_locales = _qh.get_language(self.request, get_current_registry())
		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)
		users = _qh.get_all_users(self.request.authenticated_userid, ui_locales)
		dashboard = _qh.get_dashboard_infos()

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Admin',
			'project': header,
			'extras': extras_dict,
			'users': users,
			'dashboard': dashboard
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
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		is_author = UserHandler().is_user_author(self.request.authenticated_userid)

		# get date
		now = datetime.datetime.now()
		yyyy = str(now.year)
		mm = str(now.month) if now.month > 9 else '0' + str(now.month)
		dd = str(now.day) if now.day > 9 else '0' + str(now.day)
		date = dd + "." + mm + "." + yyyy

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'News',
			'project': header,
			'extras': extras_dict,
			'date': date,
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
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Imprint',
			'project': header,
			'extras': extras_dict
		}

	# 404 page
	@notfound_view_config(renderer='templates/404.pt')
	def notfound(self):
		"""
		View configuration for the 404 page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		logger('notfound', 'def', 'main in ' + str(self.request.method) + '-request')

		logger('notfound', 'def', 'path: ' + self.request.path)
		logger('notfound', 'def', 'view name: ' + self.request.view_name)

		logger('notfound', 'def', 'params:')
		for param in self.request.params:
			logger('notfound', 'def', '    ' + param + ' -> ' + self.request.params[param])

		self.request.response.status = 404
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Error',
			'project': header,
			'page_notfound_viewname': self.request.path,
			'extras': extras_dict
		}


# ####################################
# ADDTIONAL AJAX STUFF # USER THINGS #
# ####################################

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
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		return_dict = BreadcrumbHelper().get_breadcrumbs(self.request.authenticated_userid, self.request.session.id, ui_locales)
		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - getting all text edits
	@view_config(route_name='ajax_get_all_posted_statements', renderer='json', check_csrf=True)
	def get_all_posted_statements(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_posted_statements', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		return_array = UserHandler().get_statements_of_user(self.request.authenticated_userid, ui_locales)
		return DictionaryHelper().data_to_json_array(return_array, True)

	# ajax - getting all text edits
	@view_config(route_name='ajax_get_all_edits', renderer='json', check_csrf=True)
	def get_all_edits(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_edits', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		return_array = UserHandler().get_edits_of_user(self.request.authenticated_userid, ui_locales, QueryHelper())
		return DictionaryHelper().data_to_json_array(return_array, True)

	# ajax - getting all votes for arguments
	@view_config(route_name='ajax_get_all_argument_votes', renderer='json', check_csrf=True)
	def get_all_argument_votes(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_argument_votes', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		return_array = UserHandler().get_votes_of_user(self.request.authenticated_userid, True, ui_locales, QueryHelper())
		return DictionaryHelper().data_to_json_array(return_array, True)

	# ajax - getting all votes for statements
	@view_config(route_name='ajax_get_all_statement_votes', renderer='json', check_csrf=True)
	def get_all_statement_votes(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_statement_votes', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		return_array = UserHandler().get_votes_of_user(self.request.authenticated_userid, False, ui_locales, QueryHelper())
		return DictionaryHelper().data_to_json_array(return_array, True)

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
		BreadcrumbHelper().del_breadcrumbs_of_user(transaction, self.request.authenticated_userid)
		return_dict = dict()
		return_dict['removed_data'] = 'true'  # necessary

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - deleting complete history of the user
	@view_config(route_name='ajax_delete_statistics', renderer='json', check_csrf=True)
	def delete_statistics(self):
		"""
		Request the complete user history
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('delete_statistics', 'def', 'main')

		return_dict = dict()
		return_dict['removed_data'] = 'true' if VotingHelper().clear_votes_of_user(transaction, self.request.authenticated_userid) else 'false'

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - user login
	@view_config(route_name='ajax_user_login', renderer='json')
	def user_login(self, nickname=None, password=None, for_api=False, keep_login=False):
		"""
		Will login the user by his nickname and password
		:param nickname: Manually provide nickname (e.g. from API)
		:param password: Manually provide password (e.g. from API)
		:param for_api: Manually provide boolean (e.g. from API)
		:return: dict() with error
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_login', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()

		_qh = QueryHelper()
		lang = _qh.get_language(self.request, get_current_registry())
		_tn = Translator(lang)

		try:
			if not nickname and not password:
				nickname = self.escape_string(self.request.params['user'])
				password = self.escape_string(self.request.params['password'])
				keep_login = self.escape_string(self.request.params['keep_login'])
				url = self.request.params['url']
			else:
				nickname = self.escape_string(nickname)
				password = self.escape_string(password)
				url = ""

			db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

			# check for user and password validations
			if not db_user:
				logger('user_login', 'no user', 'user \'' + nickname + '\' does not exists')
				error = _tn.get(_tn.userPasswordNotMatch)
			elif not db_user.validate_password(password):
				logger('user_login', 'password not valid', 'wrong password')
				error = _tn.get(_tn.userPasswordNotMatch)
			else:
				logger('user_login', 'login', 'login successful')
				if keep_login:
					headers = remember(self.request, nickname, max_age=self.user_login_timeout)
				else:
					headers = remember(self.request, nickname)

				# update timestamp
				logger('user_login', 'login', 'update login timestamp')
				db_user.update_last_login()
				transaction.commit()

				if for_api:
					return {'status': 'success'}
				else:
					return HTTPFound(
						location=url,
						headers=headers,
					)

		except KeyError as e:
			error = _tn.get(_tn.internalError)
			logger('user_login', 'error', repr(e))

		return_dict['error'] = str(error)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - user logout
	@view_config(route_name='ajax_user_logout', renderer='json')
	def user_logout(self):
		"""
		Will logout the user
		:return: HTTPFound with forgotten headers
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_logout', 'def', 'main')
		self.request.session.invalidate()
		headers = forget(self.request)
		self.request.response.headerlist.extend(headers)
		return self.request.response
		#  return HTTPFound(
		#  	location=mainpage,
		#  	headers=headers,
		#  )

	# ajax - registration of users
	@view_config(route_name='ajax_user_registration', renderer='json')
	def user_registration(self):
		"""
		Registers new user
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_registration', 'def', 'main, self.request.params: ' + str(self.request.params))

		# default values
		success = '0'
		message = ''
		return_dict = dict()

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
			ui_locales      = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = QueryHelper().get_language(self.request, get_current_registry())

			_t = Translator(ui_locales)

			# database queries mail verification
			db_nick = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
			db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
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
			else:
				# getting the authors group
				db_group = DBDiscussionSession.query(Group).filter_by(name="authors").first()

				# does the group exists?
				if not db_group:
					message = _t.get(_t.errorTryLateOrContant)
					logger('user_registration', 'main', 'Error occured')
				else:
					# creating a new user with hashed password
					logger('user_registration', 'main', 'Adding user')
					hashed_password = PasswordHandler().get_hashed_password(password)
					newuser = User(firstname=firstname,
					               surname=lastname,
					               email=email,
					               nickname=nickname,
					               password=hashed_password,
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
						EmailHelper().send_mail(self.request, subject, body, email, ui_locales)
						NotificationHelper().send_welcome_message(transaction, checknewuser.uid)

					else:
						logger('user_registration', 'main', 'New data was not added')
						message = _t.get(_t.accoutErrorTryLateOrContant)

		except KeyError as e:
			logger('user_registration', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - password requests
	@view_config(route_name='ajax_user_password_request', renderer='json')
	def user_password_request(self):
		"""
		Sends an email, when the user requests his password
		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_password_request', 'def', 'main, self.request.params: ' + str(self.request.params))

		success = '0'
		message = ''
		return_dict = dict()

		try:
			email = self.escape_string(self.request.params['email'])
			ui_locales      = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = QueryHelper().get_language(self.request, get_current_registry())

			success = '1'
			_t = Translator(ui_locales)

			db_user = DBDiscussionSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if db_user:
				# get password and hashed password
				pwd = PasswordGenerator().get_rnd_passwd()
				hashedpwd = PasswordHandler().get_hashed_password(pwd)

				# set the hased one
				db_user.password = hashedpwd
				DBDiscussionSession.add(db_user)
				transaction.commit()

				body = _t.get(_t.nicknameIs) + db_user.nickname + '\n'
				body += _t.get(_t.newPwdIs) + pwd
				subject = _t.get(_t.dbasPwdRequest)
				reg_success, message = EmailHelper().send_mail(self.request, subject, body, email, ui_locales)

				if reg_success:
					success = '1'
			else:
				logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
				message = 'emailUnknown'
				success = '0'

		except KeyError as e:
			logger('user_password_request', 'error', repr(e))

		return_dict['success'] = str(success)
		return_dict['message'] = str(message)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - set boolean for receiving information
	@view_config(route_name='ajax_set_user_receive_information', renderer='json')
	def set_user_receive_information_settings(self):
		"""
		Will logout the user
		:return: HTTPFound with forgotten headers
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_user_receive_information_settings', 'def', 'main, self.request.params: ' + str(self.request.params))
		_tn = Translator(QueryHelper().get_language(self.request, get_current_registry()))

		try:
			error = ''
			should_send = True if self.request.params['should_send'] == 'True' else False
			service = self.request.params['service']
			db_user = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
			if db_user:
				db_setting = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
				if service == 'mail':
					db_setting.set_send_mails(should_send)
				elif service == 'notification':
					db_setting.set_send_notifications(should_send)
				else:
					error = _tn.get(_tn.keyword)
				transaction.commit()
			else:
				error = _tn.get(_tn.checkNickname)
		except KeyError as e:
			error = _tn.get(_tn.internalError)
			logger('set_user_receive_information_settings', 'error', repr(e))

		return_dict = {'error': error}
		return DictionaryHelper().data_to_json_array(return_dict, True)


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################

	# ajax - send new start statement
	@view_config(route_name='ajax_set_new_start_statement', renderer='json', check_csrf=True)
	def set_new_start_statement(self, for_api=False, api_data=None):
		"""
		Inserts a new statement into the database, which should be available at the beginning
		:param for_api: boolean
		:param api_data: api_data
		:return: a status code, if everything was successful
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_start_statement', 'def', 'ajax, self.request.params: ' + str(self.request.params))

		logger('set_new_start_statement', 'def', 'main')

		_qh = QueryHelper()
		lang = _qh.get_language(self.request, get_current_registry())
		_tn = Translator(lang)
		return_dict = dict()
		return_dict['error'] = ''
		try:
			if for_api and api_data:
				nickname  = api_data["nickname"]
				statement = api_data["statement"]
				issue     = api_data["issue_id"]
				slug      = api_data["slug"]
			else:
				nickname    = self.request.authenticated_userid
				statement   = self.request.params['statement']
				issue       = _qh.get_issue_id(self.request)
				slug        = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()

			UserHandler().update_last_action(transaction, nickname)
			new_statement = _qh.insert_as_statements(transaction, statement, nickname, issue, is_start=True)
			if new_statement == -1:
				return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseEmpty)
			else:
				url = UrlManager(mainpage, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
				return_dict['url'] = url

		except KeyError as e:
			logger('set_new_start_statement', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - send new start premise
	@view_config(route_name='ajax_set_new_start_premise', renderer='json', check_csrf=True)
	def set_new_start_premise(self, for_api=False, api_data=None):
		"""
		Sets new premise for the start
		:param for_api: boolean
		:param api_data:
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_start_premise', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()
		_qh = QueryHelper()
		_dh = DictionaryHelper()
		lang = _qh.get_language(self.request, get_current_registry())
		_tn = Translator(lang)
		try:
			if for_api and api_data:
				nickname  = api_data["nickname"]
				statement = api_data["statement"]
				issue     = api_data["issue_id"]
				slug      = api_data["slug"]
				# TODO hier weitermachen
			else:
				nickname = self.request.authenticated_userid
				issue    = _qh.get_issue_id(self.request)

			UserHandler().update_last_action(transaction, nickname)
			premisegroups   = _dh.string_to_json(self.request.params['premisegroups'])
			conclusion_id   = self.request.params['conclusion_id']
			supportive      = True if self.request.params['supportive'].lower() == 'true' else False

			url, error = _qh.process_input_of_start_premises_and_receive_url(transaction, premisegroups, conclusion_id,
			                                                                 supportive, issue, nickname, for_api,
			                                                                 mainpage, lang, RecommenderHelper())
			return_dict['error'] = error

			if url == -1:
				return _dh.data_to_json_array(return_dict, True)

			return_dict['url'] = url
		except KeyError as e:
			logger('set_new_start_premise', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return_json = _dh.data_to_json_array(return_dict, True)

		return return_json

	# ajax - send new premises
	@view_config(route_name='ajax_set_new_premises_for_argument', renderer='json', check_csrf=True)
	def set_new_premises_for_argument(self, for_api=False):
		"""
		Sets a new premisse for an argument
		:param for_api: boolean
		:return: json-dict()
		"""
		user_id = self.request.authenticated_userid
		UserHandler().update_last_action(transaction, user_id)
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_premises_for_argument', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()
		_qh = QueryHelper()
		_dh = DictionaryHelper()
		lang = _qh.get_language(self.request, get_current_registry())
		_tn = Translator(lang)

		try:
			arg_uid         = self.request.params['arg_uid']
			attack_type     = self.request.params['attack_type']
			premisegroups   = _dh.string_to_json(self.request.params['premisegroups'])
			issue           = _qh.get_issue_id(self.request)

			url, error = _qh.process_input_of_premises_for_arguments_and_receive_url(transaction, arg_uid, attack_type,
			                                                                         premisegroups, issue, user_id, for_api,
			                                                                         mainpage, lang, RecommenderHelper())
			return_dict['error'] = error

			if url == -1:
				return _dh.data_to_json_array(return_dict, True)

			return_dict['url'] = url

		except KeyError as e:
			logger('set_new_premises_for_argument', 'error', repr(e))
			return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return_json = _dh.data_to_json_array(return_dict, True)

		logger('set_new_premises_for_argument', 'def', 'returning ' + str(return_dict))
		return return_json

	# ajax - set new textvalue for a statement
	@view_config(route_name='ajax_set_correcture_of_statement', renderer='json', check_csrf=True)
	def set_correcture_of_statement(self):
		"""
		Sets a new textvalue for a statement
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_correcture_of_statement', 'def', 'main, self.request.params: ' + str(self.request.params))
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		_qh = QueryHelper()
		_tn = Translator(_qh.get_language(self.request, get_current_registry()))

		try:
			uid = self.request.params['uid']
			corrected_text = self.escape_string(self.request.params['text'])
			ui_locales = _qh.get_language(self.request, get_current_registry())
			return_dict = _qh.correct_statement(transaction, self.request.authenticated_userid, uid, corrected_text, ui_locales)
			if return_dict == -1:
				return_dict = dict()
				return_dict['error'] = _tn.get(_tn.noCorrectionsSet)

			return_dict['error'] = ''
		except KeyError as e:
			return_dict = dict()
			return_dict['error'] = ''
			logger('set_correcture_of_statement', 'error', repr(e))

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - set notification as read
	@view_config(route_name='ajax_notification_read', renderer='json')
	def set_notification_read(self):
		"""
		Set notification as read
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_notification_read', 'def', 'main ' + str(self.request.params))
		return_dict = dict()
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)

		try:
			DBDiscussionSession.query(Notification).filter_by(uid=self.request.params['id']).first().set_read(True)
			transaction.commit()
			return_dict['unread_messages'] = NotificationHelper().count_of_new_notifications(self.request.authenticated_userid)
			return_dict['error'] = ''
		except KeyError as e:
			logger('set_message_read', 'error', repr(e))
			return_dict['error'] = _t.get(_t.internalError)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - deletes a notification
	@view_config(route_name='ajax_notification_delete', renderer='json')
	def set_notification_delete(self):
		"""
		Request the removal of a notification
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		logger('set_notification_delete', 'def', 'main ' + str(self.request.params))
		return_dict = dict()
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)

		try:
			DBDiscussionSession.query(Notification).filter_by(uid=self.request.params['id']).delete()
			transaction.commit()
			_nh = NotificationHelper()
			return_dict['unread_messages'] = _nh.count_of_new_notifications(self.request.authenticated_userid)
			return_dict['total_messages'] = str(len(_nh.get_notification_for(self.request.authenticated_userid)))
			return_dict['error'] = ''
			return_dict['success'] = _t.get(_t.messageDeleted)
		except KeyError as e:
			logger('set_message_read', 'error', repr(e))
			return_dict['error'] = _t.get(_t.internalError)
			return_dict['success'] = ''

		return DictionaryHelper().data_to_json_array(return_dict, True)


# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################

	# ajax - getting changelog of a statement
	@view_config(route_name='ajax_get_logfile_for_statement', renderer='json', check_csrf=False)
	def get_logfile_for_statement(self):
		"""
		Returns the changelog of a statement
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_logfile_for_statement', 'def', 'main, self.request.params: ' + str(self.request.params))
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)

		return_dict = dict()
		try:
			uid = self.request.params['uid']
			return_dict = QueryHelper().get_logfile_for_statement(uid)
			return_dict['error'] = ''
		except KeyError as e:
			logger('get_logfile_for_statement', 'error', repr(e))
			_tn = Translator(QueryHelper().get_language(self.request, get_current_registry()))
			return_dict['error'] = _tn.get(_tn.noCorrections)

		# return_dict = QueryHelper().get_logfile_for_premisegroup(uid)

		return DictionaryHelper().data_to_json_array(return_dict, True)

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

		return_dict = dict()
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

			# shortener = Shortener(service, api_key=google_api_key)
			# shortener = Shortener(service, bitly_login=bitly_login, bitly_api_key=bitly_key, bitly_token=bitly_token)
			shortener = Shortener(service)

			short_url = format(shortener.short(url))
			return_dict['url'] = short_url
			return_dict['service'] = service
			return_dict['service_url'] = service_url

			return_dict['error'] = ''
		except KeyError as e:
			logger('get_shortened_url', 'error', repr(e))
			_tn = Translator(QueryHelper().get_language(self.request, get_current_registry()))
			return_dict['error'] = _tn.get(_tn.internalError)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for attack overview
	@view_config(route_name='ajax_get_argument_overview', renderer='json')
	def get_argument_overview(self):
		"""
		Returns all attacks, done by the users
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_argument_overview', 'def', 'main')
		_qh = QueryHelper()
		ui_locales = _qh.get_language(self.request, get_current_registry())
		return_dict = _qh.get_argument_overview(self.request.authenticated_userid, ui_locales)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for getting all news
	@view_config(route_name='ajax_get_news', renderer='json')
	def get_news(self):
		"""
		ajax interface for getting news
		:return: json-set with all news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_news', 'def', 'main')
		return_dict = QueryHelper().get_news()
		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for getting database
	@view_config(route_name='ajax_get_database_dump', renderer='json')
	def get_database_dump(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_database_dump', 'def', 'main')
		_qh = QueryHelper()
		issue = _qh.get_issue_id(self.request)
		ui_locales = _qh.get_language(self.request, get_current_registry())

		return_dict = _qh.get_dump(issue, ui_locales)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for getting argument infos
	@view_config(route_name='ajax_get_infos_about_argument', renderer='json')
	def get_infos_about_argument(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_infos_about_argument', 'def', 'main, self.request.params: ' + str(self.request.params))
		_qh = QueryHelper()
		ui_locales = _qh.get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)
		return_dict = dict()

		try:
			uid = self.request.params['uid']
			return_dict = _qh.get_infos_about_argument(uid, ui_locales)
			return_dict['error'] = ''
		except KeyError as e:
			logger('get_infos_about_argument', 'error', repr(e))
			return_dict['error'] = _t.get(_t.internalError)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for getting all users
	@view_config(route_name='ajax_all_users', renderer='json')
	def get_all_users(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_all_users', 'def', 'main')
		ui_locales = QueryHelper().get_language(self.request, get_current_registry())

		return_dict = QueryHelper().get_all_users(self.request.authenticated_userid, ui_locales)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for getting all users with the same opinion
	@view_config(route_name='ajax_get_user_with_same_opinion', renderer='json')
	def get_users_with_same_opinion(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_users_with_same_opinion', 'def', 'main')
		_qh = QueryHelper()
		ui_locales = _qh.get_language(self.request, get_current_registry())
		_tn = Translator(ui_locales)

		return_dict = dict()
		try:
			uid = self.request.params['uid']
			is_argument = self.request.params['is_argument']
			if uid == '0':
				issue = _qh.get_issue_id(self.request)
				return_dict = _qh.get_user_with_same_opinion_for_position(issue, ui_locales)
			elif is_argument:
				return_dict = _qh.get_user_with_same_opinion_for_argument(uid, ui_locales)
			else:
				return_dict = _qh.get_user_with_same_opinion_for_statement(uid, ui_locales)
			return_dict['error'] = ''
		except KeyError as e:
			logger('set_new_start_statement', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return DictionaryHelper().data_to_json_array(return_dict, True)


# ########################################
# ADDTIONAL AJAX STUFF # ADDITION THINGS #
# ########################################

	# ajax - for language switch
	@view_config(route_name='ajax_switch_language', renderer='json')
	def switch_language(self):
		"""
		Switches the language
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler().update_last_action(transaction, self.request.authenticated_userid)
		logger('switch_language', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()
		try:
			ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = QueryHelper().get_language(self.request, get_current_registry())
			self.request.response.set_cookie('_LOCALE_', str(ui_locales))
		except KeyError as e:
			logger('swich_language', 'error', repr(e))

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for sending news
	@view_config(route_name='ajax_send_news', renderer='json')
	def send_news(self):
		"""
		ajax interface for settings news
		:return: json-set with new news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('send_news', 'def', 'main, self.request.params: ' + str(self.request.params))

		try:
			title = self.escape_string(self.request.params['title'])
			text = self.escape_string(self.request.params['text'])
			return_dict = QueryHelper().set_news(transaction, title, text, self.request.authenticated_userid)
			return_dict['error'] = ''
		except KeyError as e:
			return_dict = dict()
			logger('send_news', 'error', repr(e))
			_tn = Translator(QueryHelper().get_language(self.request, get_current_registry()))
			return_dict['error'] = _tn.get(_tn.internalError)

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for fuzzy search
	@view_config(route_name='ajax_fuzzy_search', renderer='json')
	def fuzzy_search(self, for_api=False):
		"""
		ajax interface for fuzzy string search
		:param for_api: boolean
		:return: json-set with all matched strings
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('fuzzy_search', 'def', 'main, for_api: ' + str(for_api) + ', self.request.params: ' + str(self.request.params))

		try:
			value = self.request.params['value']
			mode = str(self.request.params['type']) if not for_api else ''
			issue = QueryHelper().get_issue_id(self.request) if not for_api else ''

			return_dict = dict()
			if for_api:
				return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_issues(value)
				return DictionaryHelper().data_to_json_array(return_dict, True)

			if mode == '0':  # start statement
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_start(value, issue, True)
			elif mode == '1':  # edit statement popup
				statement_uid = self.request.params['extra']
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_edits(value, statement_uid, issue)
			elif mode == '2':  # start premise
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_start(value, issue, False)
			elif mode == '3':  # adding reasons
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher().get_fuzzy_string_for_reasons(value, issue)
			else:
				logger('fuzzy_search', 'main', 'unkown mode: ' + str(mode))
		except KeyError as e:
			return_dict = dict()
			logger('fuzzy_search', 'error', repr(e))

		return DictionaryHelper().data_to_json_array(return_dict, True)

	# ajax - for additional service
	@view_config(route_name='ajax_additional_service', renderer='json')
	def additional_service(self):
		"""

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('additional_service', 'def', 'main, self.request.params: ' + str(self.request.params))

		rtype = self.request.params['type']

		if rtype == "chuck":
			data = requests.get('http://api.icndb.com/jokes/random')
		else:
			data = requests.get('http://api.yomomma.info/')

		for a in data.json():
			logger('additional_service', 'main', str(a) + ': ' + str(data.json()[a]))

		return data.json()
