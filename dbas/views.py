"""
Core component of DBAS.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json

import requests
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import remember, forget
from pyramid.threadlocal import get_current_registry
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyshorteners.shorteners import Shortener
from sqlalchemy import and_
from validate_email import validate_email

from .helper.dictionary_helper import DictionaryHelper
from .helper.dictionary_helper_discussion import DiscussionDictHelper
from .helper.dictionary_helper_items import ItemDictHelper
from .helper.issue_helper import IssueHelper
from .helper.history_helper import HistoryHelper
from .helper.notification_helper import NotificationHelper
from .helper.query_helper import QueryHelper
from .helper.voting_helper import VotingHelper
from .database import DBDiscussionSession
from .database.discussion_model import User, Group, Issue, Argument, Notification, Settings
from .email import EmailHelper
from .input_validator import Validator
from .lib import get_language, escape_string, get_text_for_statement_uid
from .logger import logger
from .recommender_system import RecommenderSystem
from .news_handler import NewsHandler
from .opinion_handler import OpinionHandler
from .string_matcher import FuzzyStringMatcher
from .strings import Translator
from .url_manager import UrlManager
from .user_management import PasswordGenerator, PasswordHandler, UserHandler

name = 'D-BAS'
version = '0.5.11'
full_version = version + 'a'
project_name = name + ' ' + full_version
issue_fallback = 1
mainpage = ''


class Dbas(object):
	"""
	Provides every view and ajax-interface.
	"""

	def __init__(self, request):
		"""
		Object initialization

		:param request: init http request
		:return: json-dict()
		"""
		self.request = request
		global mainpage
		mainpage = request.application_url
		self.issue_fallback = DBDiscussionSession.query(Issue).first().uid

	@staticmethod
	def base_layout():
		renderer = get_renderer('templates/basetemplate.pt')
		layout = renderer.implementation().macros['layout']
		return layout

	def get_nickname_and_session(self, for_api=None, api_data=None):
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
		logger('main_page', 'def', 'main, self.request.params: ' + str(self.request.params))
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		session_expired = True if 'session_expired' in self.request.params and self.request.params['session_expired'] == 'true' else False
		ui_locales = get_language(self.request, get_current_registry())
		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)
		DictionaryHelper(ui_locales).add_language_options_for_extra_dict(extras_dict)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Main',
			'project': project_name,
			'extras': extras_dict,
			'session_expired': session_expired
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
		matchdict = self.request.matchdict
		params = self.request.params
		logger('discussion_init', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('discussion_init', 'def', 'main, self.request.params: ' + str(params))

		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		session_expired = UserHandler.update_last_action(transaction, nickname)
		HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
		HistoryHelper.save_history_in_cookie(self.request, self.request.path, '')
		if session_expired:
			return self.user_logout(True)

		if for_api and api_data:
			try:
				logged_in = api_data["nickname"]
			except KeyError:
				logged_in = None
		else:
			logged_in = self.request.authenticated_userid

		ui_locales = get_language(self.request, get_current_registry())
		_dh = DictionaryHelper(ui_locales)
		if for_api:
			slug = matchdict['slug'] if 'slug' in matchdict else ''
		else:
			slug = matchdict['slug'][0] if 'slug' in matchdict and len(matchdict['slug']) > 0 else ''

		issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
		issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)
		item_dict       = ItemDictHelper(ui_locales, issue, mainpage, for_api).prepare_item_dict_for_start(logged_in)

		discussion_dict = DiscussionDictHelper(ui_locales, session_id, nickname, mainpage=mainpage, slug=slug)\
			.prepare_discussion_dict_for_start()
		extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, False, True, nickname,
		                                          application_url=mainpage, for_api=for_api)

		if len(item_dict) == 0:
			_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_start=True)

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
			return_dict['project'] = project_name
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
		matchdict = self.request.matchdict
		params = self.request.params
		logger('discussion_attitude', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('discussion_attitude', 'def', 'main, self.request.params: ' + str(params))

		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		session_expired = UserHandler.update_last_action(transaction, nickname)
		history         = params['history'] if 'history' in params else ''
		HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
		HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)
		if session_expired:
			return self.user_logout(True)

		ui_locales      = get_language(self.request, get_current_registry())
		_dh = DictionaryHelper(ui_locales)
		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		statement_id    = matchdict['statement_id'][0] if 'statement_id' in matchdict else ''

		issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
		issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		discussion_dict = DiscussionDictHelper(ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)\
			.prepare_discussion_dict_for_attitude(statement_id)
		if not discussion_dict:
			return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_id]))

		item_dict       = ItemDictHelper(ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)\
			.prepare_item_dict_for_attitude(statement_id)
		extras_dict     = _dh.prepare_extras_dict(issue_dict['slug'], False, False, True, False, True, nickname,
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
			return_dict['project'] = project_name
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
		matchdict = self.request.matchdict
		params = self.request.params
		logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('discussion_justify', 'def', 'main, self.request.params: ' + str(params))

		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		history              = params['history'] if 'history' in params else ''
		HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
		HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)

		_uh = UserHandler
		session_expired = _uh.update_last_action(transaction, nickname)
		if session_expired:
			return self.user_logout(True)

		logged_in = _uh.is_user_logged_in(nickname)

		ui_locales = get_language(self.request, get_current_registry())
		_dh = DictionaryHelper(ui_locales)

		slug                = matchdict['slug'] if 'slug' in matchdict else ''
		statement_or_arg_id = matchdict['statement_or_arg_id'] if 'statement_or_arg_id' in matchdict else ''
		mode                = matchdict['mode'] if 'mode' in matchdict else ''
		supportive          = mode == 't' or mode == 'd'  # supportive = t or dont know mode
		relation            = matchdict['relation'][0] if len(matchdict['relation']) > 0 else ''

		issue               = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
		issue_dict          = IssueHelper.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)
		_ddh                = DiscussionDictHelper(ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)
		_idh                = ItemDictHelper(ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)

		if [c for c in ('t', 'f') if c in mode] and relation == '':
			logger('discussion_justify', 'def', 'justify statement')
			# justifying statement
			if not get_text_for_statement_uid(statement_or_arg_id):
				return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_or_arg_id]))

			VotingHelper.add_vote_for_statement(statement_or_arg_id, nickname, supportive, transaction)

			item_dict       = _idh.prepare_item_dict_for_justify_statement(statement_or_arg_id, nickname, supportive)
			discussion_dict = _ddh.prepare_discussion_dict_for_justify_statement(statement_or_arg_id, mainpage, slug, supportive, len(item_dict), nickname)
			extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, False, True, nickname, mode == 't',
			                                          application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0 or len(item_dict) == 1 and logged_in:
				_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify=True,
				                            current_premise=get_text_for_statement_uid(statement_or_arg_id),
				                            supportive=supportive)

		elif 'd' in mode and relation == '':
			logger('discussion_justify', 'def', 'dont know statement')
			# dont know
			argument_uid    = RecommenderSystem.get_argument_by_conclusion(statement_or_arg_id, supportive)
			discussion_dict = _ddh.prepare_discussion_dict_for_dont_know_reaction(argument_uid)
			item_dict       = _idh.prepare_item_dict_for_dont_know_reaction(argument_uid, supportive)
			extras_dict     = _dh.prepare_extras_dict(slug, False, False, True, True, True, nickname,
			                                          argument_id=argument_uid, application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if len(item_dict) == 0:
				_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_dont_know=True,
				                            current_premise=get_text_for_statement_uid(statement_or_arg_id))

		elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
			logger('discussion_justify', 'def', 'justify argument')
			# justifying argument
			# is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
			item_dict       = _idh.prepare_item_dict_for_justify_argument(statement_or_arg_id, relation, logged_in)
			discussion_dict = _ddh.prepare_discussion_dict_for_justify_argument(statement_or_arg_id, supportive, relation)
			extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, True, True, nickname,
			                                          argument_id=statement_or_arg_id, application_url=mainpage, for_api=for_api)
			# is the discussion at the end?
			if not logged_in and len(item_dict) == 1 or logged_in and len(item_dict) == 1:
				_dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify_argumentation=True)
		else:
			logger('discussion_justify', 'def', '404')
			return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, 'justify', statement_or_arg_id, mode, relation]))

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
			return_dict['project'] = project_name
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
		matchdict = self.request.matchdict
		params = self.request.params
		logger('discussion_reaction', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('discussion_reaction', 'def', 'main, self.request.params: ' + str(params))

		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		arg_id_user     = matchdict['arg_id_user'] if 'arg_id_user' in matchdict else ''
		attack          = matchdict['mode'] if 'mode' in matchdict else ''
		arg_id_sys      = matchdict['arg_id_sys'] if 'arg_id_sys' in matchdict else ''
		tmp_argument    = DBDiscussionSession.query(Argument).filter_by(uid=arg_id_user).first()
		history         = params['history'] if 'history' in params else ''

		if not tmp_argument or not Validator.check_reaction(arg_id_user, arg_id_sys, attack):
			return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]]))

		supportive           = tmp_argument.is_supportive
		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		session_expired      = UserHandler.update_last_action(transaction, nickname)
		HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
		HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)
		if session_expired:
			return self.user_logout(True)

		# sanity check
		if not [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid', 'end') if c in attack]:
			return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]], True))

		# set votings
		VotingHelper.add_vote_for_argument(arg_id_user, nickname, transaction)

		ui_locales      = get_language(self.request, get_current_registry())
		issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
		issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		_ddh = DiscussionDictHelper(ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)
		discussion_dict = _ddh.prepare_discussion_dict_for_argumentation(arg_id_user, supportive, arg_id_sys, attack, history)
		item_dict       = ItemDictHelper(ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)\
			.prepare_item_dict_for_reaction(arg_id_sys, arg_id_user, supportive, attack)
		extras_dict     = DictionaryHelper(ui_locales).prepare_extras_dict(slug, False, False, True, True, True, nickname,
		                                                                   argument_id=arg_id_user, application_url=mainpage,
		                                                                   for_api=for_api)

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
			return_dict['project'] = project_name
			return return_dict

	# finish page
	@view_config(route_name='discussion_finish', renderer='templates/finish.pt', permission='everybody')
	def discussion_finish(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		matchdict = self.request.matchdict
		params = self.request.params
		logger('discussion_finish', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('discussion_finish', 'def', 'main, self.request.params: ' + str(params))
		ui_locales = get_language(self.request, get_current_registry())
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Finish',
			'project': project_name,
			'extras': extras_dict
		}

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
		matchdict = self.request.matchdict
		params = self.request.params
		logger('discussion_choose', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('discussion_choose', 'def', 'main, self.request.params: ' + str(params))

		slug            = matchdict['slug'] if 'slug' in matchdict else ''
		is_argument     = matchdict['is_argument'] if 'is_argument' in matchdict else ''
		is_supportive   = matchdict['supportive'] if 'supportive' in matchdict else ''
		uid             = matchdict['id'] if 'id' in matchdict else ''
		pgroup_ids      = matchdict['pgroup_ids'] if 'id' in matchdict else ''
		nickname, session_id = self.get_nickname_and_session(for_api, api_data)
		history         = params['history'] if 'history' in params else ''

		is_argument = True if is_argument is 't' else False
		is_supportive = True if is_supportive is 't' else False

		ui_locales      = get_language(self.request, get_current_registry())
		_dh             = DictionaryHelper(ui_locales)
		issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
		issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, ui_locales, for_api)

		session_expired = UserHandler.update_last_action(transaction, nickname)
		HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
		HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)
		if session_expired:
			return self.user_logout(True)

		discussion_dict = DiscussionDictHelper(ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)\
			.prepare_discussion_dict_for_choosing(uid, is_argument, is_supportive)
		item_dict       = ItemDictHelper(ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)\
			.prepare_item_dict_for_choosing(uid, pgroup_ids, is_argument, is_supportive)
		extras_dict     = _dh.prepare_extras_dict(slug, False, False, True, True, True, nickname,
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
			return_dict['project'] = project_name
			return return_dict

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		"""
		View configuration for the contact view.

		:return: dictionary with title and project username as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_contact', 'def', 'main, self.request.params: ' + str(self.request.params))
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		contact_error = False
		send_message = False
		message = ''

		ui_locales = get_language(self.request, get_current_registry())

		username        = escape_string(self.request.params['name'] if 'name' in self.request.params else '')
		email           = escape_string(self.request.params['mail'] if 'mail' in self.request.params else '')
		phone           = escape_string(self.request.params['phone'] if 'phone' in self.request.params else '')
		content         = escape_string(self.request.params['content'] if 'content' in self.request.params else '')
		spam            = escape_string(self.request.params['spam'] if 'spam' in self.request.params else '')
		request_token   = escape_string(self.request.params['csrf_token'] if 'csrf_token' in self.request.params else '')
		spamquestion    = ''

		if 'form.contact.submitted' not in self.request.params:
			# get anti-spam-question
			spamquestion, answer = UserHandler.get_random_anti_spam_question(ui_locales)
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
			elif (not spam) or (not isinstance(spam, int)) or (not (int(spam) == int(self.request.session['antispamanswer']))):
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
				EmailHelper.send_mail(self.request, subject, body, 'dbas.hhu@gmail.com', ui_locales)
				body = '* THIS IS A COPY OF YOUR MAIL *\n\n' + body
				subject = '[INFO] ' + subject
				send_message, message = EmailHelper.send_mail(self.request, subject, body, email, ui_locales)
				contact_error = not send_message
				if send_message:
					spamquestion, answer = UserHandler.get_random_anti_spam_question(ui_locales)

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)
		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Contact',
			'project': project_name,
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

	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.

		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('main_settings', 'def', 'main, self.request.params: ' + str(self.request.params))
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		ui_locales = get_language(self.request, get_current_registry())
		_tn = Translator(ui_locales)

		old_pw      = ''
		new_pw      = ''
		confirm_pw  = ''
		message     = ''
		error       = False
		success     = False

		db_user     = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
		db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first() if db_user else None
		_uh         = UserHandler
		if db_user:
			edits       = _uh.get_count_of_statements_of_user(db_user, True)
			statements  = _uh.get_count_of_statements_of_user(db_user, False)
			arg_vote, stat_vote = _uh.get_count_of_votes_of_user(db_user)
			public_nick = db_user.public_nickname
		else:
			edits       = 0
			statements  = 0
			arg_vote    = 0
			stat_vote   = 0
			public_nick = str(self.request.authenticated_userid)

		if db_user and 'form.passwordchange.submitted' in self.request.params:
			old_pw = escape_string(self.request.params['passwordold'])  # TODO passwords with html strings
			new_pw = escape_string(self.request.params['password'])
			confirm_pw = escape_string(self.request.params['passwordconfirm'])

			message, error, success = _uh.change_password(transaction, db_user, old_pw, new_pw, confirm_pw, ui_locales)

		# get gravater profile picture
		gravatar_url = _uh.get_profile_picture(db_user)

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)
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
			'db_public_nickname': public_nick,
			'db_mail': db_user.email if db_user else 'unknown',
			'db_group': db_user.groups.name if db_user and db_user.groups else 'unknown',
			'avatar_url': gravatar_url,
			'edits_done': edits,
			'statemens_posted': statements,
			'discussion_arg_votes': arg_vote,
			'discussion_stat_votes': stat_vote,
			'send_mails': db_settings.should_send_mails if db_settings else False,
			'send_notifications': db_settings.should_send_notifications if db_settings else False,
			'public_nick': db_settings.should_show_public_nickname if db_settings else True,
			'title_mails': _tn.get(_tn.mailSettingsTitle),
			'title_notifications': _tn.get(_tn.notificationSettingsTitle),
			'title_public_nick': _tn.get(_tn.publicNickTitle),
			'public_page_url': mainpage + '/user/' + public_nick
		}

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Settings',
			'project': project_name,
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
		ui_locales = get_language(self.request, get_current_registry())
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Messages',
			'project': project_name,
			'extras': extras_dict
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
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		ui_locales = get_language(self.request, get_current_registry())
		is_author = UserHandler.is_user_author(self.request.authenticated_userid)

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'News',
			'project': project_name,
			'extras': extras_dict,
			'is_author': is_author
		}

	# public users page for everybody
	@view_config(route_name='main_user', renderer='templates/user.pt', permission='everybody')
	def main_user(self):
		"""
		View configuration for the public users.

		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		matchdict = self.request.matchdict
		params = self.request.params
		logger('main_user', 'def', 'main, self.request.matchdict: ' + str(matchdict))
		logger('main_user', 'def', 'main, self.request.params: ' + str(params))

		nickname = matchdict['nickname'] if 'nickname' in matchdict else ''
		nickname = nickname.replace('%20', ' ')
		logger('main_user', 'def', 'nickname: ' + str(nickname))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_public_user = DBDiscussionSession.query(User).filter_by(public_nickname=nickname).first()

		db_settings = None
		current_user = None

		if db_user:
			db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
		elif db_public_user:
			db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_public_user.uid).first()

		if db_settings:
			if db_settings.should_show_public_nickname and db_user:
				current_user = db_user
			elif not db_settings.should_show_public_nickname and db_public_user:
				current_user = db_public_user

		if current_user is None:
			return HTTPFound(location=UrlManager(mainpage).get_404([self.request.path[1:]]))

		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		ui_locales = get_language(self.request, get_current_registry())
		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)

		user_dict = UserHandler.get_information_of(current_user, ui_locales)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'User ' + nickname,
			'project': project_name,
			'extras': extras_dict,
			'user': user_dict
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
		ui_locales = get_language(self.request, get_current_registry())
		session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
		if session_expired:
			return self.user_logout(True)

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Imprint',
			'project': project_name,
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
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('notfound', 'def', 'main in ' + str(self.request.method) + '-request' +
		       ', path: ' + self.request.path +
		       ', view name: ' + self.request.view_name +
		       ', params: ' + str(self.request.params))
		path = self.request.path
		if path.startswith('/404/'):
			path = path[4:]

		param_error = True if 'param_error' in self.request.params and self.request.params['param_error'] == 'true' else False

		self.request.response.status = 404
		ui_locales = get_language(self.request, get_current_registry())

		extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid)

		# return HTTPFound(location=UrlManager(mainpage, for_api=False).get_404([self.request.path[1:]]))

		return {
			'layout': self.base_layout(),
			'language': str(ui_locales),
			'title': 'Error',
			'project': project_name,
			'page_notfound_viewname': path,
			'extras': extras_dict,
			'param_error': param_error
		}


# ####################################
# ADDTIONAL AJAX STUFF # USER THINGS #
# ####################################

	# ajax - getting complete track of the user
	@view_config(route_name='ajax_get_user_history', renderer='json', check_csrf=True)
	def get_user_history(self):
		"""
		Request the complete user track.

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('get_user_history', 'def', 'main')
		ui_locales = get_language(self.request, get_current_registry())
		return_list = HistoryHelper.get_history_from_database(self.request.authenticated_userid, ui_locales)
		return json.dumps(return_list, True)

	# ajax - getting all text edits
	@view_config(route_name='ajax_get_all_posted_statements', renderer='json', check_csrf=True)
	def get_all_posted_statements(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_posted_statements', 'def', 'main')
		ui_locales = get_language(self.request, get_current_registry())
		return_array = UserHandler.get_statements_of_user(self.request.authenticated_userid, ui_locales)
		return json.dumps(return_array, True)

	# ajax - getting all text edits
	@view_config(route_name='ajax_get_all_edits', renderer='json', check_csrf=True)
	def get_all_edits(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_edits', 'def', 'main')
		ui_locales = get_language(self.request, get_current_registry())
		return_array = UserHandler.get_edits_of_user(self.request.authenticated_userid, ui_locales)
		return json.dumps(return_array, True)

	# ajax - getting all votes for arguments
	@view_config(route_name='ajax_get_all_argument_votes', renderer='json', check_csrf=True)
	def get_all_argument_votes(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_argument_votes', 'def', 'main')
		ui_locales = get_language(self.request, get_current_registry())
		return_array = UserHandler.get_votes_of_user(self.request.authenticated_userid, True, ui_locales, QueryHelper())
		return json.dumps(return_array, True)

	# ajax - getting all votes for statements
	@view_config(route_name='ajax_get_all_statement_votes', renderer='json', check_csrf=True)
	def get_all_statement_votes(self):
		"""

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('get_all_statement_votes', 'def', 'main')
		ui_locales = get_language(self.request, get_current_registry())
		return_array = UserHandler.get_votes_of_user(self.request.authenticated_userid, False, ui_locales, QueryHelper())
		return json.dumps(return_array, True)

	# ajax - deleting complete history of the user
	@view_config(route_name='ajax_delete_user_history', renderer='json', check_csrf=True)
	def delete_user_history(self):
		"""
		Request the complete user history.

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		logger('delete_user_history', 'def', 'main')
		HistoryHelper.delete_history_in_database(self.request.authenticated_userid, transaction)
		return_dict = dict()
		return_dict['removed_data'] = 'true'  # necessary

		return json.dumps(return_dict, True)

	# ajax - deleting complete history of the user
	@view_config(route_name='ajax_delete_statistics', renderer='json', check_csrf=True)
	def delete_statistics(self):
		"""
		Request the complete user history.

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		logger('delete_statistics', 'def', 'main')

		return_dict = dict()
		return_dict['removed_data'] = 'true' if VotingHelper.clear_votes_of_user(transaction, self.request.authenticated_userid) else 'false'

		return json.dumps(return_dict, True)

	# ajax - user login
	@view_config(route_name='ajax_user_login', renderer='json')
	def user_login(self, nickname=None, password=None, for_api=False, keep_login=False):
		"""
		Will login the user by his nickname and password

		:param nickname: Manually provide nickname (e.g. from API)
		:param password: Manually provide password (e.g. from API)
		:param for_api: Manually provide boolean (e.g. from API)
		:param keep_login: Manually provide boolean (e.g. from API)
		:return: dict() with error
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_login', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()

		lang = get_language(self.request, get_current_registry())
		_tn = Translator(lang)

		try:
			if not nickname and not password:
				nickname = escape_string(self.request.params['user'])
				password = escape_string(self.request.params['password'])
				keep_login = escape_string(self.request.params['keep_login'])
				keep_login = True if keep_login == 'true' else False
				url = self.request.params['url']
			else:
				nickname = escape_string(nickname)
				password = escape_string(password)
				url = ''

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
				logger('user_login', 'login', 'keep_login: ' + str(keep_login))
				db_user.should_hold_the_login(keep_login)
				headers = remember(self.request, nickname)

				# update timestamp
				logger('user_login', 'login', 'update login timestamp')
				db_user.update_last_login()
				db_user.update_last_action()
				transaction.commit()
				ending = ['/?session_expired=true', '/?session_expired=falses']
				for e in ending:
					if url.endswith(e):
						url = url[0:-len(e)]

				if for_api:
					logger('user_login', 'return', 'for api: success')
					return {'status': 'success'}
				else:
					logger('user_login', 'return', 'success: ' + url)
					return HTTPFound(
						location=url,
						headers=headers,
					)

		except KeyError as e:
			error = _tn.get(_tn.internalError)
			logger('user_login', 'error', repr(e))

		return_dict['error'] = str(error)

		return json.dumps(return_dict, True)

	# ajax - user logout
	@view_config(route_name='ajax_user_logout', renderer='json')
	def user_logout(self, redirect_to_main=False):
		"""
		Will logout the user

		:param redirect_to_main: Boolean
		:return: HTTPFound with forgotten headers
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_logout', 'def', 'main, user: ' + str(self.request.authenticated_userid) + ', redirect_to_main: ' + str(redirect_to_main))
		self.request.session.invalidate()
		headers = forget(self.request)
		if redirect_to_main:
			return HTTPFound(
				location=mainpage + '?session_expired=true',
				headers=headers,
			)
		else:
			self.request.response.headerlist.extend(headers)
			return self.request.response

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
		success = ''
		error = ''
		info = ''
		return_dict = dict()

		ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
		if not ui_locales:
			ui_locales = get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)

		# getting params
		try:
			params          = self.request.params
			firstname       = escape_string(params['firstname'])
			lastname        = escape_string(params['lastname'])
			nickname        = escape_string(params['nickname'])
			email           = escape_string(params['email'])
			gender          = escape_string(params['gender'])
			password        = escape_string(params['password'])
			passwordconfirm = escape_string(params['passwordconfirm'])

			# database queries mail verification
			db_nick1 = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
			db_nick2 = DBDiscussionSession.query(User).filter_by(public_nickname=nickname).first()
			db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
			is_mail_valid = validate_email(email, check_mx=True)

			# are the password equal?
			if not password == passwordconfirm:
				logger('user_registration', 'main', 'Passwords are not equal')
				info = _t.get(_t.pwdNotEqual)
			# is the nick already taken?
			elif db_nick1 or db_nick2:
				logger('user_registration', 'main', 'Nickname \'' + nickname + '\' is taken')
				info = _t.get(_t.nickIsTaken)
			# is the email already taken?
			elif db_mail:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is taken')
				info = _t.get(_t.mailIsTaken)
			# is the email valid?
			elif not is_mail_valid:
				logger('user_registration', 'main', 'E-Mail \'' + email + '\' is not valid')
				info = _t.get(_t.mailNotValid)
			else:
				# getting the authors group
				db_group = DBDiscussionSession.query(Group).filter_by(name="authors").first()

				# does the group exists?
				if not db_group:
					info = _t.get(_t.errorTryLateOrContant)
					logger('user_registration', 'main', 'Error occured')
				else:
					# creating a new user with hashed password
					logger('user_registration', 'main', 'Adding user')
					hashed_password = PasswordHandler.get_hashed_password(password)
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
						success = _t.get(_t.accountWasAdded)

						# sending an email
						subject = 'D-BAS Account Registration'
						body = _t.get(_t.accountWasRegistered)
						EmailHelper().send_mail(self.request, subject, body, email, ui_locales)
						NotificationHelper.send_welcome_message(transaction, checknewuser.uid)

					else:
						logger('user_registration', 'main', 'New data was not added')
						info = _t.get(_t.accoutErrorTryLateOrContant)

		except KeyError as e:
			logger('user_registration', 'error', repr(e))
			error = _t.get(_t.internalError)

		return_dict['success'] = str(success)
		return_dict['error']   = str(error)
		return_dict['info']    = str(info)

		return json.dumps(return_dict, True)

	# ajax - password requests
	@view_config(route_name='ajax_user_password_request', renderer='json')
	def user_password_request(self):
		"""
		Sends an email, when the user requests his password

		:return: dict() with success and message
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('user_password_request', 'def', 'main, self.request.params: ' + str(self.request.params))

		success = ''
		error = ''
		info = ''
		return_dict = dict()
		ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
		if not ui_locales:
			ui_locales = get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)

		try:
			email = escape_string(self.request.params['email'])
			db_user = DBDiscussionSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if db_user:
				# get password and hashed password
				pwd = PasswordGenerator.get_rnd_passwd()
				hashedpwd = PasswordHandler.get_hashed_password(pwd)

				# set the hashed one
				db_user.password = hashedpwd
				DBDiscussionSession.add(db_user)
				transaction.commit()

				body = _t.get(_t.nicknameIs) + db_user.nickname + '\n'
				body += _t.get(_t.newPwdIs) + pwd
				subject = _t.get(_t.dbasPwdRequest)
				reg_success, message = EmailHelper.send_mail(self.request, subject, body, email, ui_locales)

				if reg_success:
					success = message
				else:
					error = message
			else:
				logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
				info = _t.get(_t.emailUnknown)

		except KeyError as e:
			logger('user_password_request', 'error', repr(e))
			error = _t.get(_t.internalError)

		return_dict['success'] = str(success)
		return_dict['error']   = str(error)
		return_dict['info']    = str(info)

		return json.dumps(return_dict, True)

	# ajax - set boolean for receiving information
	@view_config(route_name='ajax_set_user_setting', renderer='json')
	def set_user_settings(self):
		"""
		Will logout the user

		:return:
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_user_settings', 'def', 'main, self.request.params: ' + str(self.request.params))
		_tn = Translator(get_language(self.request, get_current_registry()))

		try:
			error = ''
			public_nick = ''
			public_page_url = ''
			settings_value = True if self.request.params['settings_value'] == 'True' else False
			service = self.request.params['service']
			db_user = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
			if db_user:
				public_nick = db_user.public_nickname
				db_setting = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()

				if service == 'mail':
					db_setting.set_send_mails(settings_value)

				elif service == 'notification':
					db_setting.set_send_notifications(settings_value)

				elif service == 'public_nick':
					db_setting.set_show_public_nickname(settings_value)
					if settings_value:
						db_user.set_public_nickname(db_user.nickname)
					elif db_user.nickname == db_user.public_nickname:
						# TODO: there are only 52245 different nicks
						UserHandler.refresh_public_nickname(db_user)
					public_nick = db_user.public_nickname
				else:
					error = _tn.get(_tn.keyword)

				transaction.commit()
				public_page_url = mainpage + '/user/' + public_nick
			else:
				error = _tn.get(_tn.checkNickname)
		except KeyError as e:
			error = _tn.get(_tn.internalError)
			public_nick = ''
			public_page_url = ''
			logger('set_user_settings', 'error', repr(e))

		return_dict = {'error': error, 'public_nick': public_nick, 'public_page_url': public_page_url}
		return json.dumps(return_dict, True)


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

		lang = get_language(self.request, get_current_registry())
		_tn = Translator(lang)
		return_dict = dict()
		return_dict['error'] = ''
		return_dict['statement_uids'] = []
		try:
			if for_api and api_data:
				nickname  = api_data["nickname"]
				statement = api_data["statement"]
				issue     = api_data["issue_id"]
				slug      = api_data["slug"]
			else:
				nickname    = self.request.authenticated_userid
				statement   = self.request.params['statement']
				issue       = IssueHelper.get_issue_id(self.request)
				slug        = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()

			# escaping will be done in QueryHelper().set_statement(...)
			UserHandler.update_last_action(transaction, nickname)
			new_statement = QueryHelper.insert_as_statements(transaction, statement, nickname, issue, is_start=True)
			if new_statement == -1:
				return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseEmpty)
			else:
				url = UrlManager(mainpage, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
				return_dict['url'] = url
				return_dict['statement_uids'].append(new_statement[0].uid)
		except KeyError as e:
			logger('set_new_start_statement', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return json.dumps(return_dict, True)

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
		lang = get_language(self.request, get_current_registry())
		_tn = Translator(lang)
		try:
			if for_api and api_data:
				nickname      = api_data['nickname']
				premisegroups = api_data['statement']
				issue         = api_data['issue_id']
				conclusion_id = api_data['conclusion_id']
				supportive    = api_data['supportive']
			else:
				nickname        = self.request.authenticated_userid
				issue           = IssueHelper.get_issue_id(self.request)
				premisegroups   = json.loads(self.request.params['premisegroups'])
				conclusion_id   = self.request.params['conclusion_id']
				supportive      = True if self.request.params['supportive'].lower() == 'true' else False

			# escaping will be done in QueryHelper().set_statement(...)
			UserHandler.update_last_action(transaction, nickname)

			_qh = QueryHelper
			url, statement_uids, error = _qh.process_input_of_start_premises_and_receive_url(self.request, transaction,
			                                                                                 premisegroups, conclusion_id,
			                                                                                 supportive, issue, nickname,
			                                                                                 for_api, mainpage, lang)
			return_dict['error'] = error
			return_dict['statement_uids'] = statement_uids

			if url == -1:
				return json.dumps(return_dict, True)

			return_dict['url'] = url
		except KeyError as e:
			logger('set_new_start_premise', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return json.dumps(return_dict, True)

	# ajax - send new premises
	@view_config(route_name='ajax_set_new_premises_for_argument', renderer='json', check_csrf=True)
	def set_new_premises_for_argument(self, for_api=False, api_data=None):
		"""
		Sets a new premise for an argument

		:param api_data:
		:param for_api: boolean
		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_new_premises_for_argument', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()
		lang = get_language(self.request, get_current_registry())
		_tn = Translator(lang)

		try:
			if for_api and api_data:
				nickname      = api_data['nickname']
				premisegroups = api_data['statement']
				issue         = api_data['issue_id']
				arg_uid       = api_data['arg_uid']
				attack_type   = api_data['attack_type']
			else:
				nickname = self.request.authenticated_userid
				premisegroups = json.loads(self.request.params['premisegroups'])
				issue = IssueHelper.get_issue_id(self.request)
				arg_uid = self.request.params['arg_uid']
				attack_type = self.request.params['attack_type']

			# escaping will be done in QueryHelper().set_statement(...)
			_qh = QueryHelper
			url, statement_uids, error = _qh.process_input_of_premises_for_arguments_and_receive_url(self.request,
			                                                                                         transaction, arg_uid,
			                                                                                         attack_type,
			                                                                                         premisegroups, issue,
			                                                                                         nickname, for_api,
			                                                                                         mainpage, lang)
			UserHandler.update_last_action(transaction, nickname)

			return_dict['error'] = error
			return_dict['statement_uids'] = statement_uids

			if url == -1:
				return json.dumps(return_dict, True)

			return_dict['url'] = url

		except KeyError as e:
			logger('set_new_premises_for_argument', 'error', repr(e))
			return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseInternal)

		logger('set_new_premises_for_argument', 'def', 'returning ' + str(return_dict))
		return json.dumps(return_dict, True)

	# ajax - set new textvalue for a statement
	@view_config(route_name='ajax_set_correcture_of_statement', renderer='json', check_csrf=True)
	def set_correcture_of_statement(self):
		"""
		Sets a new textvalue for a statement

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('set_correcture_of_statement', 'def', 'main, self.request.params: ' + str(self.request.params))
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		_tn = Translator(get_language(self.request, get_current_registry()))

		try:
			uid = self.request.params['uid']
			corrected_text = escape_string(self.request.params['text'])
			ui_locales = get_language(self.request, get_current_registry())
			return_dict = QueryHelper.correct_statement(transaction, self.request.authenticated_userid, uid, corrected_text, ui_locales)
			if return_dict == -1:
				return_dict = dict()
				return_dict['error'] = _tn.get(_tn.noCorrectionsSet)

			return_dict['error'] = ''
		except KeyError as e:
			return_dict = dict()
			return_dict['error'] = ''
			logger('set_correcture_of_statement', 'error', repr(e))

		return json.dumps(return_dict, True)

	# ajax - set notification as read
	@view_config(route_name='ajax_notification_read', renderer='json')
	def set_notification_read(self):
		"""
		Set notification as read

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		logger('set_notification_read', 'def', 'main ' + str(self.request.params))
		return_dict = dict()
		ui_locales = get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)

		try:
			DBDiscussionSession.query(Notification).filter_by(uid=self.request.params['id']).first().set_read(True)
			transaction.commit()
			return_dict['unread_messages'] = NotificationHelper.count_of_new_notifications(self.request.authenticated_userid)
			return_dict['error'] = ''
		except KeyError as e:
			logger('set_message_read', 'error', repr(e))
			return_dict['error'] = _t.get(_t.internalError)

		return json.dumps(return_dict, True)

	# ajax - deletes a notification
	@view_config(route_name='ajax_notification_delete', renderer='json')
	def set_notification_delete(self):
		"""
		Request the removal of a notification

		:return: json-dict()
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		logger('set_notification_delete', 'def', 'main ' + str(self.request.params))
		return_dict = dict()
		ui_locales = get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)

		try:
			DBDiscussionSession.query(Notification).filter_by(uid=self.request.params['id']).delete()
			transaction.commit()
			return_dict['unread_messages'] = NotificationHelper.count_of_new_notifications(self.request.authenticated_userid)
			return_dict['total_messages'] = str(len(NotificationHelper.get_notification_for(self.request.authenticated_userid)))
			return_dict['error'] = ''
			return_dict['success'] = _t.get(_t.messageDeleted)
		except KeyError as e:
			logger('set_message_read', 'error', repr(e))
			return_dict['error'] = _t.get(_t.internalError)
			return_dict['success'] = ''

		return json.dumps(return_dict, True)

	# ajax - set new issue
	@view_config(route_name='ajax_set_new_issue', renderer='json')
	def set_new_issue(self):
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		logger('set_new_issue', 'def', 'main ' + str(self.request.params))
		return_dict = dict()
		ui_locales = get_language(self.request, get_current_registry())
		_tn = Translator(ui_locales)

		try:
			info = escape_string(self.request.params['info'])
			title = escape_string(self.request.params['title'])
			was_set, error = IssueHelper.set_issue(info, title, self.request.authenticated_userid, transaction, ui_locales)
			if was_set:
				db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
				                                                        Issue.info == info)).first()
				return_dict['issue'] = IssueHelper.get_issue_dict_for(db_issue, mainpage, False, 0, ui_locales)
		except KeyError as e:
			logger('set_new_issue', 'error', repr(e))
			error = _tn.get(_tn.notInsertedErrorBecauseInternal)

		return_dict['error'] = error
		return json.dumps(return_dict, True)

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
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		return_dict = dict()
		ui_locales = get_language(self.request, get_current_registry())

		try:
			uid = self.request.params['uid']
			return_dict = QueryHelper.get_logfile_for_statement(uid, ui_locales)
			return_dict['error'] = ''
		except KeyError as e:
			logger('get_logfile_for_statement', 'error', repr(e))
			_tn = Translator(ui_locales)
			return_dict['error'] = _tn.get(_tn.noCorrections)

		# return_dict = QueryHelper().get_logfile_for_premisegroup(uid)

		return json.dumps(return_dict, True)

	# ajax - for shorten url
	@view_config(route_name='ajax_get_shortened_url', renderer='json')
	def get_shortened_url(self):
		"""
		Shortens url with the help of a python lib

		:return: dictionary with shortend url
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)

		logger('get_shortened_url', 'def', 'main')

		return_dict = dict()

		try:
			url = self.request.params['url']
			# google_api_key = 'AIzaSyAw0aPsBsAbqEJUP_zJ9Fifbhzs8xkNSw0' # browser is
			# google_api_key = 'AIzaSyDneaEJN9FNGUpXHDZahe9Rhb21FsFNS14' # server id
			# service = 'GoogleShortener'
			# service_url = 'https://goo.gl/'
			# shortener = Shortener(service, api_key=google_api_key)

			# bitly_login = 'dbashhu'
			# bitly_key = ''
			# bitly_token = 'R_d8c4acf2fb554494b65529314d1e11d1'

			# service = 'BitlyShortener'
			# service_url = 'https://bitly.com/'
			# shortener = Shortener(service, bitly_token=bitly_token)

			service = 'TinyurlShortener'
			service_url = 'http://tinyurl.com/'
			shortener = Shortener(service)

			short_url = format(shortener.short(url))
			return_dict['url'] = short_url
			return_dict['service'] = service
			return_dict['service_url'] = service_url

			return_dict['error'] = ''
		except KeyError as e:
			logger('get_shortened_url', 'error', repr(e))
			_tn = Translator(get_language(self.request, get_current_registry()))
			return_dict['error'] = _tn.get(_tn.internalError)

		return json.dumps(return_dict, True)

	# ajax - for getting all news
	@view_config(route_name='ajax_get_news', renderer='json')
	def get_news(self):
		"""
		ajax interface for getting news

		:return: json-set with all news
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_news', 'def', 'main')
		return_dict = NewsHandler.get_news()
		return json.dumps(return_dict, True)

	# ajax - for getting argument infos
	@view_config(route_name='ajax_get_infos_about_argument', renderer='json')
	def get_infos_about_argument(self):
		"""
		ajax interface for getting a dump

		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_infos_about_argument', 'def', 'main, self.request.params: ' + str(self.request.params))
		ui_locales = get_language(self.request, get_current_registry())
		_t = Translator(ui_locales)
		return_dict = dict()

		try:
			uid = self.request.params['uid']
			return_dict = QueryHelper.get_infos_about_argument(uid, ui_locales, mainpage)
			return_dict['error'] = ''
		except KeyError as e:
			logger('get_infos_about_argument', 'error', repr(e))
			return_dict['error'] = _t.get(_t.internalError)

		return json.dumps(return_dict, True)

	# ajax - for getting all users with the same opinion
	@view_config(route_name='ajax_get_user_with_same_opinion', renderer='json')
	def get_users_with_same_opinion(self):
		"""
		ajax interface for getting a dump
		:return: json-set with everything
		"""
		logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
		logger('get_users_with_same_opinion', 'def', 'main: ' + str(self.request.params))
		ui_locales = get_language(self.request, get_current_registry())
		_tn = Translator(ui_locales)
		nickname = self.request.authenticated_userid

		return_dict = dict()
		try:
			uids = self.request.params['uids']
			is_argument = self.request.params['is_argument'] == 'true' if 'is_argument' in self.request.params else False
			is_attitude = self.request.params['is_attitude'] == 'true' if 'is_attitude' in self.request.params else False
			is_reaction = self.request.params['is_reaction'] == 'true' if 'is_reaction' in self.request.params else False
			if is_argument:
				if not is_reaction:
					return_dict = OpinionHandler.get_user_with_same_opinion_for_argument(uids, ui_locales, nickname, mainpage)
				else:
					return_dict = OpinionHandler.get_user_with_opinions_for_argument(uids, ui_locales, nickname, mainpage)
			else:
				if not is_attitude:
					uids = json.loads(uids)
					return_dict = OpinionHandler.get_user_with_same_opinion_for_statements(uids if isinstance(uids, list) else [uids], ui_locales, nickname, mainpage)
				else:
					return_dict = OpinionHandler.get_user_with_opinions_for_attitude(uids, ui_locales, nickname, mainpage)
			return_dict['error'] = ''
		except KeyError as e:
			logger('get_users_with_same_opinion', 'error', repr(e))
			return_dict['error'] = _tn.get(_tn.internalError)

		return json.dumps(return_dict, True)


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
		UserHandler.update_last_action(transaction, self.request.authenticated_userid)
		logger('switch_language', 'def', 'main, self.request.params: ' + str(self.request.params))

		return_dict = dict()
		try:
			ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
			if not ui_locales:
				ui_locales = get_language(self.request, get_current_registry())
			self.request.response.set_cookie('_LOCALE_', str(ui_locales))
		except KeyError as e:
			logger('swich_language', 'error', repr(e))

		return json.dumps(return_dict, True)

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
			title = escape_string(self.request.params['title'])
			text = escape_string(self.request.params['text'])
			return_dict = NewsHandler.set_news(transaction, title, text, self.request.authenticated_userid)
			return_dict['error'] = ''
		except KeyError as e:
			return_dict = dict()
			logger('send_news', 'error', repr(e))
			_tn = Translator(get_language(self.request, get_current_registry()))
			return_dict['error'] = _tn.get(_tn.internalError)

		return json.dumps(return_dict, True)

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

		_tn = Translator(get_language(self.request, get_current_registry()))

		try:
			value = self.request.params['value']
			mode = str(self.request.params['type']) if not for_api else ''
			issue = IssueHelper.get_issue_id(self.request) if not for_api else ''

			return_dict = dict()
			if for_api and not mode == '4':
				return_dict['values'] = FuzzyStringMatcher.get_strings_for_issues(value)
				return json.dumps(return_dict, True)

			if mode == '0':  # start statement
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_start(value, issue, True)
			elif mode == '1':  # edit statement popup
				statement_uid = self.request.params['extra']
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_edits(value, statement_uid)
			elif mode == '2':  # start premise
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_start(value, issue, False)
			elif mode == '3':  # adding reasons
				return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_reasons(value, issue)
			elif mode == '4':  # getting text
				return_dict = FuzzyStringMatcher.get_strings_for_search(value)
			else:
				logger('fuzzy_search', 'main', 'unkown mode: ' + str(mode))
				return_dict = {'error': _tn.get(_tn.internalError)}

		except KeyError as e:
			return_dict = {'error': _tn.get(_tn.internalError)}
			logger('fuzzy_search', 'error', repr(e))

		return json.dumps(return_dict, True)

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
