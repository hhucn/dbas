import random
import json
import datetime
import locale
import string

from collections import OrderedDict
from sqlalchemy import and_
from slugify import slugify

from .breadcrumb_helper import BreadcrumbHelper
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, Breadcrumb, Issue, History
from .logger import logger
from .recommender_system import RecommenderHelper
from .query_helper import QueryHelper
from .strings import Translator, TextGenerator
from .url_manager import UrlManager
from .user_management import UserHandler
from .notification_helper import NotificationHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class DictionaryHelper(object):

	#  def __init__(self):
	#  self.lang = ''
	#  TODO move lang here and init translator

	def get_random_subdict_out_of_orderer_dict(self, ordered_dict, count):
		"""
		Creates a random subdictionary with given count out of the given ordered_dict.
		With a count of <2 the dictionary itself will be returned.
		:param ordered_dict: dictionary for the function
		:param count: count of entries for the new dictionary
		:return: dictionary
		"""
		return_dict = dict()
		logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'count: ' + str(count))
		items = list(ordered_dict.items())

		if count < 0:
			return ordered_dict
		elif count == 1:
			if len(items) > 1:
				rnd = random.randint(0, len(items) - 1)
				return_dict[items[rnd][0]] = items[rnd][1]
			else:
				return ordered_dict
		else:

			for i in range(0, count):
				rnd = random.randint(0, len(items) - 1)
				return_dict[items[rnd][0]] = items[rnd][1]
				items.pop(rnd)

		return return_dict

	def data_to_json_array(self, raw_dict, ensure_ascii):
		"""
		Dumps given dictionary into json
		:param raw_dict: dictionary for dumping
		:param ensure_ascii: if true, ascii will be checked
		:return: json data
		"""
		return_dict = json.dumps(raw_dict, ensure_ascii)
		return return_dict

	def string_to_json(self, string):
		"""

		:param string:
		:return:
		"""
		return json.loads(string)

	def save_statement_row_in_dictionary(self, statement_row):
		"""
		Saved a row in dictionary
		:param statement_row: for saving
		:return: dictionary
		"""
		logger('DictionaryHelper', 'save_statement_row_in_dictionary', 'statement uid ' + str(statement_row.uid))
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == statement_row.uid,
																		Statement.issue_uid == issue)).first()
		db_premise = DBDiscussionSession.query(Premise).filter(and_(Premise.statement_uid == db_statement.uid,
																	Premise.issue_uid == issue)).first()
		db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).first()

		uid	= str(db_statement.uid)
		text   = db_textversion.content
		date   = str(db_textversion.timestamp)
		author = db_textversion.users.nickname
		pgroup = str(db_premise.premisesgroup_uid) if db_premise else '0'

		while text.endswith('.'):
			text = text[:-1]

		return {'uid': uid, 'text': text, 'date': date, 'author': author, 'premisegroup_uid': pgroup}

	def prepare_discussion_dict(self, user, transaction, uid, lang, breadcrumbs, save_crumb, at_start=False,
	                            at_attitude=False, at_justify=False, is_supportive=False, at_dont_know=False,
	                            at_argumentation=False, at_justify_argumentation=False, at_choosing=False,
	                            additional_id=0, attack='', is_uid_argument=False, logged_in=False):
		"""

		:param user:
		:param transaction:
		:param uid:
		:param lang:
		:param breadcrumbs:
		:param save_crumb:
		:param at_start:
		:param at_attitude:
		:param at_justify:
		:param is_supportive:
		:param at_dont_know:
		:param at_argumentation:
		:param at_justify_argumentation:
		:param at_choosing:
		:param additional_id:
		:param attack:
		:param is_uid_argument:
		:param logged_in:
		:return:
		"""
		_tn			   = Translator(lang)
		_qh			   = QueryHelper()
		h_intro        = ''
		h_bridge       = ''
		h_outro        = ''
		db_user        = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		bubbles_array  = self.__create_speechbubble_history(db_user)
		add_premise_text = ''
		save_statement_url = 'ajax_set_new_start_statement'

		if at_start:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_start')
			h_intro             = _tn.get(_tn.initialPositionInterest)
			save_statement_url  = 'ajax_set_new_start_premise'
			text = 'Welcome to D-BAS<br>If you want to get back in the discussion,<br>please click a bubble. Caution: Your progress will be lost!' # TODO TEXT
			welcome_bubble = self.__create_speechbubble_dict(False, False, True, 'welcome', '', text)
			start_bubble = self.__create_speechbubble_dict(True, False, False, 'start', '', h_intro)
			bubbles_array.append(welcome_bubble)
			bubbles_array.append(start_bubble)

			if save_crumb:
				self.__save_speechbubble(welcome_bubble, db_user, breadcrumbs[-1], transaction)

		elif at_attitude:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_attitude')
			text				= _qh.get_text_for_statement_uid(uid)
			if not text:
				return None
			h_bridge            = _tn.get(_tn.whatDoYouThinkAbout) + ' <strong>' + text[0:1].lower() + text[1:] + '</strong>?'
			select_bubble = self.__create_speechbubble_dict(True, False, False, '', '', 'You have selected: <strong>' + text + '</strong>') # TODO TEXT
			bubble = self.__create_speechbubble_dict(True, False, False, '', '', h_bridge)
			if save_crumb:
				bubbles_array.append(select_bubble)
				self.__save_speechbubble(select_bubble, db_user, breadcrumbs[-1], transaction)
				# self.__save_speechbubble(bubble, db_user, breadcrumbs[-1], transaction)
			bubbles_array.append(bubble)
			for b in breadcrumbs:
				logger('---','---',str(b))

		elif at_justify:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_justify')
			text				= _qh.get_text_for_statement_uid(uid)
			if not text:
				return None
			h_bridge            = _tn.get(_tn.whyDoYouThinkThat) + ' <strong>' + text[0:1].lower() + text[1:] + '</strong> ' \
			                      + _tn.get(_tn.isTrue if is_supportive else _tn.isFalse) + '?'
			because			    = _tn.get(_tn.because)[0:1].upper() + _tn.get(_tn.because)[1:].lower() + '...'
			h_outro             = because
			add_premise_text	+= text[0:1].upper() + text[1:]

			select_bubble = self.__create_speechbubble_dict(True, False, False, '', '', 'You have selected: <strong>' + text + '</strong> ' + ('is true' if is_supportive else 'is false')) # TODO TEXT
			bubble = self.__create_speechbubble_dict(True, False, False, '', '', h_bridge + ' ' + h_outro)
			if save_crumb:
				bubbles_array.append(select_bubble)
				self.__save_speechbubble(select_bubble, db_user, breadcrumbs[-1], transaction)
			bubbles_array.append(self.__create_speechbubble_dict(False, False, True, 'now', '', 'Now'))
			bubbles_array.append(bubble)


		elif at_justify_argumentation:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_justify_argumentation')
			_tg = TextGenerator(lang)
			db_argument		= DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
			confr	        = _qh.get_text_for_argument_uid(uid, lang, True)
			premise, tmp	= _qh.get_text_for_premisesgroup_uid(uid, lang)
			conclusion		= _qh.get_text_for_statement_uid(db_argument.conclusion_uid) if db_argument.conclusion_uid != 0 \
									else _qh.get_text_for_argument_uid(db_argument.argument_uid, lang, True)

			h_intro, h_bridge , h_outro = _tg.get_header_for_users_confrontation_response(confr, premise, attack,
			                                                                              conclusion, False, is_supportive,
			                                                                              logged_in)
			if attack == 'undermine':
				add_premise_text = _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																		  db_argument.is_supportive)
				add_premise_text = add_premise_text[0:1].upper() + add_premise_text[1:]

			elif attack == 'support':
				is_supportive = not is_supportive
				# when the user rebuts a system confrontation, he attacks his own negated premise, therefore he supports
				# is own premise. so his premise is the conclusion and we need new premises ;-)
				add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																		   is_supportive)
			elif attack == 'undercut':
				add_premise_text += _tg.get_text_for_add_premise_container(premise, premise, attack, conclusion,
																		   db_argument.is_supportive)

			else:
				add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																		   db_argument.is_supportive)
			because			 = ' ' + _tn.get(_tn.because)[0:1].upper() + _tn.get(_tn.because)[1:].lower() + '...'
			h_outro      	 = because
			save_statement_url  = 'ajax_set_new_premises_for_argument'


			bubble_intro = self.__create_speechbubble_dict(True, False, False, '', '', h_intro)
			if save_crumb:
				bubbles_array.append(bubble_intro)
			bubble_intro['message'] = bubble_intro['message'] + ' ' + h_outro
			bubbles_array.append(self.__create_speechbubble_dict(False, False, True, 'now', '', 'Now'))
			bubbles_array.append(bubble_intro)

		elif at_dont_know:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_dont_know')
			text				= _qh.get_text_for_argument_uid(uid, lang)
			text				= text.replace(_tn.get(_tn.because).lower(), '</strong>' + _tn.get(_tn.because).lower() + '<strong>')
			if text:
				h_bridge      	= _tn.get(_tn.otherParticipantsThinkThat) + ' <strong>' + text[0:1].lower() + text[1:] \
								 + '</strong>. ' + ''
				h_outro         = _tn.get(_tn.whatDoYouThinkAboutThat) + '?'
			else:  # this will be set in add_discussion_end_text, because if we have no argument, the item_dict will be empty
				h_intro      	= _tn.get(_tn.firstOneText) + ' <strong>' + _qh.get_text_for_statement_uid(additional_id) + '</strong>.'

		elif at_argumentation:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_argumentation')
			_tg					 = TextGenerator(lang)
			db_argument			 = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
			if attack == 'end':
				h_intro          = _tn.get(_tn.sentencesOpenersForArguments[0])\
									  + ': <strong>' + _qh.get_text_for_argument_uid(uid, lang, True) + '</strong>. '
				h_bridge         = _tn.get(_tn.otherParticipantsDontHaveCounterForThat) + '.'
				h_outro          = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)
			else:
				premise, tmp	 = _qh.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
				conclusion       = _qh.get_text_for_conclusion(db_argument, lang)
				db_confrontation = DBDiscussionSession.query(Argument).filter_by(uid=additional_id).first()
				confr, tmp       = _qh.get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid, lang)
				sys_conclusion   = _qh.get_text_for_conclusion(db_confrontation, lang)
				if attack == 'undermine':
					premise = _qh.get_text_for_statement_uid(db_confrontation.conclusion_uid) if db_confrontation.conclusion_uid != 0 \
						else _qh.get_text_for_argument_uid(db_confrontation.argument_uid, lang, True)

				# argumentation is a reply for an argument, if the arguments conclusion of the user is no position
				db_statement		= DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()
				reply_for_argument  = not (db_statement and db_statement.is_startpoint)
				current_argument	= _qh.get_text_for_argument_uid(uid, lang, True, True)
				user_is_attacking   = not db_argument.is_supportive

				# fix
				prefix = '</strong>' + _tn.get(_tn.soYourOpinionIsThat) + ': <strong>'
				if conclusion.startswith(prefix):
					conclusion = conclusion[len(prefix):]

				h_intro, h_bridge , h_outro = _tg.get_text_for_confrontation(premise, conclusion, sys_conclusion, is_supportive,
				                                                             attack, confr, reply_for_argument, user_is_attacking,
				                                                             current_argument, db_argument)
				bubble_intro = self.__create_speechbubble_dict(True, False, False, '', '', h_intro)
				bubble_bridge = self.__create_speechbubble_dict(False, True, False, '', '', h_bridge)
				bubble_outro = self.__create_speechbubble_dict(True, False, False, '', '', h_outro)
				bubbles_array.append(self.__create_speechbubble_dict(False, False, True, 'now', '', 'Now'))
				bubbles_array.append(bubble_intro)
				bubbles_array.append(bubble_bridge)
				bubbles_array.append(bubble_outro)
				if save_crumb:
					self.__save_speechbubble(bubble_intro, db_user, breadcrumbs[-1], transaction)
					self.__save_speechbubble(bubble_bridge, db_user, breadcrumbs[-1], transaction)

		elif at_choosing:
			logger('DictionaryHelper', 'prepare_discussion_dict', 'at_choosing')
			h_intro  = _tn.get(_tn.soYouEnteredMultipleReasons) + '.'
			h_bridge += _tn.get(_tn.whyAreYouAgreeingWithInColor) if is_supportive else _tn.get(_tn.whyAreYouDisagreeingWithInColor)
			h_bridge += ': <strong>'
			h_bridge += _qh.get_text_for_argument_uid(uid, lang, True) if is_uid_argument else _qh.get_text_for_statement_uid(uid)
			h_bridge += '</strong>?'
			h_outro  += _tn.get(_tn.because) + '...'

		heading_dict = {'intro': h_intro, 'bridge': h_bridge, 'outro': h_outro, 'bubbles': bubbles_array}
		return {'heading': heading_dict, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_item_dict_for_start(self, issue_uid, logged_in, lang, application_url, for_api):
		"""

		:param issue_uid:
		:param logged_in:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		db_statements = DBDiscussionSession.query(Statement)\
			.filter(and_(Statement.is_startpoint == True, Statement.issue_uid == issue_uid))\
			.join(TextVersion, TextVersion.uid == Statement.textversion_uid).all()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()

		statements_array = []
		_um = UrlManager(application_url, slug, for_api)
		_qh = QueryHelper()

		if db_statements:
			for statement in db_statements:
				statements_array.append(self.__create_statement_dict(statement.uid,
				                                                     _qh.get_text_for_statement_uid(statement.uid),
				                                                     [{'title': _qh.get_text_for_statement_uid(statement.uid), 'id': statement.uid}],
																  'start',
																     _um.get_url_for_statement_attitude(True, statement.uid)))

			if logged_in:
				_tn = Translator(lang)
				statements_array.append(self.__create_statement_dict('start_statement',
				                                                     _tn.get(_tn.newConclusionRadioButtonText),
				                                                     [{'title': _tn.get(_tn.newConclusionRadioButtonText), 'id': 0}],
																'start',
																'add'))

		return statements_array

	def prepare_item_dict_for_attitude(self, statement_uid, issue_uid, lang, application_url, for_api):
		"""

		:param statement_uid:
		:param issue_uid:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_attitude', 'def')
		_qh = QueryHelper()
		_tn = Translator(lang)

		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		text = _qh.get_text_for_statement_uid(statement_uid)
		statements_array = []

		_um = UrlManager(application_url, slug, for_api)

		statements_array.append(self.__create_statement_dict('agree',
		                                                     _tn.get(_tn.iAgreeWithInColor) + ': ' + text,
		                                                     [{'title': _tn.get(_tn.iAgreeWithInColor) + ': ' + text, 'id': 'agree'}],
														'agree', _um.get_url_for_justifying_statement(True, statement_uid, 't')))
		statements_array.append(self.__create_statement_dict('disagree',
		                                                     _tn.get(_tn.iDisagreeWithInColor) + ': ' + text,
		                                                     [{'title': _tn.get(_tn.iDisagreeWithInColor) + ': ' + text, 'id': 'disagree'}],
														'disagree', _um.get_url_for_justifying_statement(True, statement_uid, 'f')))
		statements_array.append(self.__create_statement_dict('dontknow',
		                                                     _tn.get(_tn.iHaveNoOpinionYetInColor) + ': ' + text,
		                                                     [{'title': _tn.get(_tn.iHaveNoOpinionYetInColor) + ': ' + text, 'id': 'dontknow'}],
														'dontknow', _um.get_url_for_justifying_statement(True, statement_uid, 'd')))

		return statements_array

	def prepare_item_dict_for_justify_statement(self, statement_uid, user, issue_uid, is_supportive, lang, application_url, for_api):
		"""

		:param statement_uid:
		:param user:
		:param issue_uid:
		:param is_supportive:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_justify_statement', 'def')
		statements_array = []
		_tn = Translator(lang)
		_qh = QueryHelper()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		db_arguments = RecommenderHelper().get_arguments_by_conclusion(statement_uid, is_supportive)

		_um = UrlManager(application_url, slug, for_api)

		if db_arguments:
			for argument in db_arguments:
				# get all premises in the premisegroup of this argument
				db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
				premise_array = []
				for premise in db_premises:
					text = _qh.get_text_for_statement_uid(premise.statement_uid)
					premise_array.append({'title': text, 'id': premise.statement_uid})

				text, uid = _qh.get_text_for_premisesgroup_uid(argument.premisesgroup_uid, lang)

				# get attack for each premise, so the urls will be unique
				arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(argument.uid, issue_uid, lang)
				statements_array.append(self.__create_statement_dict(str(argument.uid),
				                                                     text,
				                                                     premise_array,
																  'justify',
																     _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys)))

			if user:
				statements_array.append(self.__create_statement_dict('start_premise',
				                                                     _tn.get(_tn.newPremiseRadioButtonText),
				                                                     [{'title': _tn.get(_tn.newPremiseRadioButtonText), 'id': 0}],
																  'justify',
																  'add'))

		return statements_array

	def prepare_item_dict_for_justify_argument(self, argument_uid, attack_type, issue_uid, lang, application_url, for_api):
		"""

		:param argument_uid:
		:param attack_type:
		:param issue_uid:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_justify_argument', 'def')
		statements_array = []
		_tn = Translator(lang)
		_qh = QueryHelper()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()

		db_arguments = []
		# description in docs: dbas/logic
		if attack_type == 'undermine':
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
			for premise in db_premises:
				arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == premise.statement_uid,
																			Argument.is_supportive == False)).all()
				db_arguments = db_arguments + arguments

		elif attack_type == 'undercut':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.argument_uid == argument_uid,
																		   Argument.is_supportive == False)).all()

		elif attack_type == 'overbid':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.argument_uid == argument_uid,
																		   Argument.is_supportive == True)).all()

		elif attack_type == 'rebut':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == db_argument.conclusion_uid,
																		   Argument.argument_uid == db_argument.argument_uid,
																		   Argument.is_supportive == False)).all()
		elif attack_type == 'support':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == db_argument.conclusion_uid,
																		   Argument.argument_uid == db_argument.argument_uid,
																		   Argument.is_supportive == db_argument.is_supportive)).all()

		_um = UrlManager(application_url, slug, for_api)

		if db_arguments:
			for argument in db_arguments:
				text, tmp = _qh.get_text_for_premisesgroup_uid(argument.premisesgroup_uid, lang)

				# get alles premises in this group
				db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
				premises_array = []
				for premise in db_premises:
					premise_dict = dict()
					premise_dict['id'] = premise.statement_uid
					premise_dict['title'] = _qh.get_text_for_statement_uid(premise.statement_uid)
					premises_array.append(premise_dict)

				# for each justifying premise, we need a new confrontation:
				arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(argument_uid, issue_uid, lang)

				statements_array.append(self.__create_statement_dict(argument.uid,
				                                                     text,
				                                                     premises_array,
																'justify',
																     _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys)))

			statements_array.append(self.__create_statement_dict('justify_premise',
			                                                     _tn.get(_tn.newPremiseRadioButtonText),
			                                                     [{'id': '0', 'title': _tn.get(_tn.newPremiseRadioButtonText)}],
															'null',
															'null'))

		return statements_array

	def prepare_item_dict_for_dont_know_reaction(self, argument_uid, is_supportive, issue_uid, lang, application_url, for_api):
		"""

		:param argument_uid:
		:param is_supportive:
		:param issue_uid:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_dont_know_reaction', 'def')
		_tg = TextGenerator(lang)
		_qh = QueryHelper()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		_um = UrlManager(application_url, slug, for_api)
		statements_array = []

		db_argument  = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		conclusion   = _qh.get_text_for_conclusion(db_argument, lang)
		premise, tmp = _qh.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
		conclusion   = conclusion[0:1].lower() + conclusion[1:]
		premise	     = premise[0:1].lower() + premise[1:]
		ret_dict	 = _tg.get_relation_text_dict(premise, conclusion, False, False, False, is_dont_know=True)
		mode		 = 't' if is_supportive else 't'
		counter_mode = 'f' if is_supportive else 't'

		relations = ['undermine', 'support', 'undercut', 'overbid', 'rebut']
		for relation in relations:
			if relation == 'support':
				arg_id_sys, sys_attack = RecommenderHelper().get_attack_for_argument(argument_uid, issue_uid, lang)
				url = _um.get_url_for_reaction_on_argument(True, argument_uid, sys_attack, arg_id_sys)

			else:
				current_mode = mode if relation == 'overbid' else counter_mode
				url = _um.get_url_for_justifying_argument(True, argument_uid, current_mode, relation)

			statements_array.append(self.__create_statement_dict(relation, ret_dict[relation + '_text'], [{'title': ret_dict[relation + '_text'], 'id':relation}], relation, url))

		return statements_array

	def prepare_item_dict_for_reaction(self, argument_uid_sys, argument_uid_user, is_supportive, issue_uid, attack, lang, application_url, for_api):
		"""

		:param argument_uid_sys:
		:param argument_uid_user:
		:param is_supportive:
		:param issue_uid:
		:param attack:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_reaction', 'def')
		_tg  = TextGenerator(lang)
		_qh = QueryHelper()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()

		db_sys_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid_sys).first()
		db_user_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid_user).first()
		statements_array = []
		if not db_sys_argument or not db_user_argument:
			return statements_array

		conclusion   = _qh.get_text_for_conclusion(db_sys_argument, lang)
		premise, tmp = _qh.get_text_for_premisesgroup_uid(db_sys_argument.premisesgroup_uid, lang)
		conclusion	 = conclusion[0:1].lower() + conclusion[1:]
		premise		 = premise[0:1].lower() + premise[1:]

		ret_dict	 = _tg.get_relation_text_dict(premise, conclusion, False, True, not db_sys_argument.is_supportive)
		mode		 = 't' if is_supportive else 'f'
		_um			 = UrlManager(application_url, slug, for_api)

		# based in the relation, we will fetch different url's for the items
		# relations = ['undermine', 'support', 'undercut', 'overbid', 'rebut'] # TODO 'overbid'
		relations = ['undermine', 'support', 'undercut', 'rebut']
		for relation in relations:
			url = ''

			# special case, when the user selectes the support, because this does not need to be justified!
			if relation == 'support':
				arg_id_sys, sys_attack = RecommenderHelper().get_attack_for_argument(argument_uid_sys, issue_uid, lang)
				url = _um.get_url_for_reaction_on_argument(True, argument_uid_sys, sys_attack, arg_id_sys)

			# easy cases
			elif relation == 'undermine' or relation == 'undercut':

				url = _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)

			elif relation == 'overbid':
				# if overbid is the 'overbid', it's easy
				#  url = _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)
				# otherwise it will be the attack again
				url = _um.get_url_for_justifying_argument(True, argument_uid_user, mode, attack)

			elif relation == 'rebut':  # if we are having an rebut, everything seems different
				if attack == 'undermine':  # rebutting an undermine will be a support for the initial argument
					url = _um.get_url_for_justifying_statement(True, db_sys_argument.conclusion_uid, mode)
				# rebutting an undercut will be a overbid for the initial argument
				elif attack == 'undercut':
					url = _um.get_url_for_justifying_argument(True, argument_uid_user, mode, 'overbid')
				# rebutting an rebut will be a justify for the initial argument
				elif attack == 'rebut':
					url = _um.get_url_for_justifying_statement(True, db_user_argument.conclusion_uid, mode)

			else:
				url = _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)

			statements_array.append(self.__create_statement_dict(relation, ret_dict[relation + '_text'], [{'title': ret_dict[relation + '_text'], 'id':relation}], relation, url))

		# last item is the back button
		relation = 'no_opinion'
		url = 'back' if for_api else 'window.history.go(-1)'
		statements_array.append(self.__create_statement_dict(relation, ret_dict[relation + '_text'], [{'title': ret_dict[relation + '_text'], 'id':relation}], relation, url))

		return statements_array

	def prepare_item_dict_for_choosing(self, argument_or_statement_id, pgroup_ids, is_argument, is_supportive, lang, application_url, issue_uid, for_api):
		"""

		:param argument_or_statement_id:
		:param pgroup_ids:
		:param is_argument:
		:param is_supportive:
		:param lang:
		:param application_url:
		:param issue_uid:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_choosing', 'def')
		statements_array = []
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		_qh = QueryHelper()
		_um = UrlManager(application_url, slug, for_api)
		_t = Translator(lang)
		conclusion = argument_or_statement_id if not is_argument else 0
		argument = argument_or_statement_id if is_argument else 0

		for group_id in pgroup_ids:
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group_id).all()
			premise_array = []
			for premise in db_premises:
				text = _qh.get_text_for_statement_uid(premise.statement_uid)
				premise_array.append({'title': text, 'id': premise.statement_uid})

			text, uid = _qh.get_text_for_premisesgroup_uid(group_id, lang)

			# get attack for each premise, so the urls will be unique
			logger('DictionaryHelper', 'prepare_item_dict_for_choosing', 'premisesgroup_uid: ' + str(group_id)
			       + ', conclusion_uid: ' + str(conclusion)
			       + ', argument_uid: ' + str(argument)
			       + ', is_supportive: ' + str(is_supportive))
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == group_id,
																		  Argument.conclusion_uid == conclusion,
																		  Argument.argument_uid == argument,
																		  Argument.is_supportive == is_supportive)).first()
			arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(db_argument.uid, issue_uid, lang)
			url = _um.get_url_for_reaction_on_argument(True, db_argument.uid, attack, arg_id_sys)

			statements_array.append(self.__create_statement_dict(str(db_argument.uid),
			                                                     text,
			                                                     premise_array,
															  'choose',
															     url))
		url = 'back' if for_api else 'window.history.go(-1)'
		text = _t.get(_t.iHaveNoOpinion) + '. ' + _t.get(_t.goStepBack) + '.'
		statements_array.append(self.__create_statement_dict('no_opinion', text, [{'title': text, 'id': 'no_opinion'}], 'no_opinion', url))
		return statements_array

	def prepare_extras_dict(self, current_slug, is_editable, is_reportable, is_questionable, show_bar_icon,
	                        show_display_styles, lang, authenticated_userid, argument_id=0, application_url='', for_api=False):
		"""

		:param current_slug:
		:param is_editable:
		:param is_reportable:
		:param is_questionable:
		:param show_bar_icon:
		:param show_display_styles:
		:param lang:
		:param authenticated_userid:
		:param argument_id:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_extras_dict', 'def')
		_uh = UserHandler()
		_tn = Translator(lang)
		_qh = QueryHelper()
		_nh = NotificationHelper()
		is_logged_in = _uh.is_user_logged_in(authenticated_userid)

		return_dict = dict()
		return_dict['restart_url']		             = UrlManager(application_url, current_slug, for_api).get_slug_url(True)
		return_dict['logged_in']		             = is_logged_in
		return_dict['users_name']		             = str(authenticated_userid)
		self.add_language_options_for_extra_dict(return_dict, lang)

		if not for_api:
			return_dict['is_editable']                   = is_editable and is_logged_in
			return_dict['is_reportable']	             = is_reportable
			return_dict['is_questionable']                 = is_questionable
			return_dict['is_admin']			             = _uh.is_user_admin(authenticated_userid)
			return_dict['show_bar_icon']	             = show_bar_icon
			return_dict['show_display_style']            = show_display_styles
			return_dict['add_premise_container_style']   = 'display: none'
			return_dict['add_statement_container_style'] = 'display: none'
			return_dict['close_premise_container']	     = True
			return_dict['close_statement_container']	 = True
			return_dict['title']						 = {'barometer': _tn.get(_tn.opinionBarometer),
															'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
															'island_view': _tn.get(_tn.displayControlDialogIslandBody),
															'expert_view': _tn.get(_tn.displayControlDialogExpertBody)}
			return_dict['buttons']					   = {'report': _tn.get(_tn.report),
															'report_title': _tn.get(_tn.reportTitle),
															'question_title': _tn.get(_tn.questionTitle),
															'show_all_arguments': _tn.get(_tn.showAllArguments),
															'show_all_users': _tn.get(_tn.showAllUsers),
															'delete_track': _tn.get(_tn.deleteTrack),
															'request_track': _tn.get(_tn.requestTrack),
															'delete_history': _tn.get(_tn.deleteHistory),
															'request_history': _tn.get(_tn.requestHistory),
															'password_submit': _tn.get(_tn.passwordSubmit),
															'contact_submit': _tn.get(_tn.contactSubmit),
															'lets_go': _tn.get(_tn.letsGo),
															'opinion_barometer': _tn.get(_tn.opinionBarometer),
															'edit_statement': _tn.get(_tn.editTitle),
															'more_title': _tn.get(_tn.more),
															'previous': _tn.get(_tn.previous),
															'next': _tn.get(_tn.next),
															'save_my_statement': _tn.get(_tn.saveMyStatement),
															'add_statement_row_title': _tn.get(_tn.addStatementRow),
															'rem_statement_row_title': _tn.get(_tn.remStatementRow),
															'switch_discussion': _tn.get(_tn.switchDiscussionTitle),
															'clear_statistics': _tn.get(_tn.clearStatistics),
															'user_options': _tn.get(_tn.userOptions),
															'switch_language': _tn.get(_tn.switchLanguage),
															'login': _tn.get(_tn.login),
															'news_about_dbas': _tn.get(_tn.newsAboutDbas),
															'share_url': _tn.get(_tn.shareUrl)}
			# /return_dict['breadcrumbs']   = breadcrumbs
			message_dict = dict()
			message_dict['count']		= _nh.count_of_new_notifications(authenticated_userid)
			message_dict['has_unread']   = (message_dict['count'] > 0)
			message_dict['all']		  = _nh.get_notification_for(authenticated_userid)
			message_dict['total']		= len(message_dict['all'])
			return_dict['notifications'] = message_dict

			# add everything for the island view
			if show_display_styles:
				# does an argumente exists?
				db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()
				if db_argument:
					island_dict = _qh.get_every_attack_for_island_view(argument_id, lang)

					db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()
					premise, tmp = _qh.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
					conclusion = _qh.get_text_for_conclusion(db_argument, lang)
					island_dict['heading'] = _qh.get_text_for_argument_uid(argument_id, lang, True)

					island_dict['premise'] = premise[0:1].lower() + premise[1:]
					island_dict['conclusion'] = conclusion[0:1].lower() + conclusion[1:]
					island_dict.update(TextGenerator(lang).get_relation_text_dict(island_dict['premise'],
																				  island_dict['conclusion'],
																				  False, False, not db_argument.is_supportive))
					return_dict['island'] = island_dict
				else:
					return_dict['is_editable']		  = False
					return_dict['is_reportable']	  = False
					return_dict['show_bar_icon']	  = False
					return_dict['show_display_style'] = False
					return_dict['title']			  = {'barometer': _tn.get(_tn.opinionBarometer),
					                                     'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
					                                     'island_view': _tn.get(_tn.displayControlDialogIslandBody),
					                                     'expert_view': _tn.get(_tn.displayControlDialogExpertBody),
					                                     'edit_statement': _tn.get(_tn.editTitle),
					                                     'report_statement': _tn.get(_tn.reportTitle)}
		return return_dict

	def add_discussion_end_text(self, discussion_dict, extras_dict, logged_in, lang, at_start=False, at_dont_know=False,
								at_justify_argumentation=False, at_justify=False, current_premise=''):
		"""

		:param discussion_dict: dict()
		:param extras_dict: dict()
		:param logged_in: Boolean
		:param lang: String
		:param at_start: Boolean
		:param at_dont_know: Boolean
		:param at_justify_argumentation: Boolean
		:param at_justify: Boolean
		:param current_premise: id
		:return: None
		"""
		logger('QueryHelper', 'add_discussion_end_text', 'main')
		_t = Translator(lang)
		discussion_dict['heading']['outro'] += ''

		if at_start:
			discussion_dict['mode'] = 'start'
			discussion_dict['heading']['intro'] = _t.get(_t.firstPositionText)
			discussion_dict['heading']['bridge'] = ''
			discussion_dict['heading']['outro'] += _t.get(_t.pleaseAddYourSuggestion) if logged_in else (_t.get(_t.discussionEnd) + ' ' + _t.get(_t.feelFreeToLogin))
			if logged_in:
				extras_dict['add_statement_container_style'] = ''  # this will remove the 'display: none;'-style
				extras_dict['close_statement_container'] = False
			extras_dict['show_display_style']	= False
			extras_dict['show_bar_icon']	    = False
			extras_dict['is_editable']		    = False
			extras_dict['is_reportable']		= False

		elif at_justify_argumentation:
			discussion_dict['mode'] = 'justify_argumentation'
			extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
			extras_dict['close_premise_container'] = False
			extras_dict['show_display_style'] = False

		elif at_dont_know:
			discussion_dict['mode'] = 'dont_know'
			discussion_dict['heading']['intro']  = _t.get(_t.firstOneInformationText) + ' <strong>' + current_premise + '</strong>, '
			discussion_dict['heading']['bridge'] = _t.get(_t.butOtherParticipantsDontHaveOpinionRegardingYourOpinion) + ''
			discussion_dict['heading']['outro']  = _t.get(_t.discussionEnd) + ' ' + _t.get(_t.discussionEndLinkText)

		elif at_justify:
			discussion_dict['mode'] = 'justify'
			discussion_dict['heading']['intro']  = _t.get(_t.firstPremiseText1) + ' <strong>' + current_premise + '</strong>.'
			discussion_dict['heading']['bridge'] = ''
			discussion_dict['heading']['outro']  = _t.get(_t.whyDoYouThinkThat) + '?'
			extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
			extras_dict['close_premise_container'] = False
			extras_dict['show_display_style']	   = False
			extras_dict['show_bar_icon']		   = False
			extras_dict['is_editable']			   = False
			extras_dict['is_reportable']		   = False

		else:
			discussion_dict['heading']['outro'] += _t.get(_t.discussionEnd) + ' ' + (_t.get(_t.discussionEndLinkText) if logged_in else _t.get(_t.feelFreeToLogin))

	def add_language_options_for_extra_dict(self, extras_dict, lang):
		"""

		:param extras_dict:
		:param lang:
		:return:
		"""
		logger('DictionaryHelper', 'add_language_options_for_extra_dict', 'def')
		lang_is_en = (lang != 'de')
		lang_is_de = (lang == 'de')
		extras_dict.update({
			'lang_is_de': lang_is_de,
			'lang_is_en': lang_is_en,
			'link_de_class': ('active' if lang_is_de else ''),
			'link_en_class': ('active' if lang_is_en else '')
		})
		
	def __create_statement_dict(self, uid, title, premises, attitude, url):
		"""

		:param uid:
		:param title:
		:param premises:
		:param attitude:
		:param url:
		:return:
		"""
		return {
			'id': 'item_' + str(uid),
			'title': title,
			'premises': premises,
			'attitude': attitude,
			'url': url}

	def __create_speechbubble_dict(self, is_user, is_system, is_status, uid, url, message):
		"""

		:param is_user:
		:param is_system:
		:param is_status:
		:param uid:
		:param url:
		:param message:
		:param should_save:
		:return:
		"""
		speech = dict()
		speech['is_user']   = is_user
		speech['is_system'] = is_system
		speech['is_status'] = is_status
		speech['id']        = uid
		speech['url']       = url + '?breadcrumb=true'
		speech['message']   = message

		return speech

	def __save_speechbubble(self, bubble_dict, db_user, related_breadcrumb, transaction):
		"""

		:param bubble_dict:
		:param transaction:
		:return:
		"""
		DBDiscussionSession.add(History(bubble_id=bubble_dict['id'], user=str(db_user.uid), content=bubble_dict['message'],
		                                is_user=bubble_dict['is_user'], is_system=bubble_dict['is_system'],
		                                is_status=bubble_dict['is_status'], breadcrumb_uid=str(related_breadcrumb['uid'])))
		transaction.commit()

	def __create_speechbubble_history(self, user):
		"""

		:param user:
		:return:
		"""
		if not user:
			return []

		bubble_history = []
		db_history = DBDiscussionSession.query(History).filter_by(author_uid=user.uid).join(Breadcrumb).all()
		for h in db_history:
			bubble_history.append(self.__create_speechbubble_dict(h.is_user, h.is_system, h.is_status, h.bubble_id, h.breadcrumbs.url, h.content))

		return bubble_history