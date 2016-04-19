"""
Provides helping function for dictionaries, which are used in discussions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import re

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, Bubble, VoteArgument, VoteStatement
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion
from dbas.logger import logger
from dbas.strings import Translator, TextGenerator
from dbas.url_manager import UrlManager


class DiscussionDictHelper(object):
	"""
	Provides all functions for creating the discussion dictionaries with all bubbles.
	"""

	def __init__(self, lang, session_id, breadcrumbs, nickname=None):
		"""
		Initialize default values

		:param lang: ui_locales
		:param session_id: request.session_id
		:param breadcrumbs: breadcrumbs-dict()
		:return:
		"""
		self.lang = lang
		self.session_id = session_id
		self.breadcrumbs = breadcrumbs
		self.nickname = nickname

	def prepare_discussion_dict_for_start(self):
		"""
		Prepares the discussion dict with all bubbles for the first step in discussion, where the user chooses a position.
		
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_start', 'at_start')
		_tn			        = Translator(self.lang)
		bubbles_array       = self.__create_speechbubble_history()
		add_premise_text    = ''
		intro               = _tn.get(_tn.initialPositionInterest)
		save_statement_url  = 'ajax_set_new_start_premise'

		start_bubble = self.create_speechbubble_dict(is_system=True, uid='start', message=intro, omit_url=True)
		self.__append_bubble(bubbles_array, start_bubble)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_attitude(self, uid):
		"""
		Prepares the discussion dict with all bubbles for the second step in discussion, where the user chooses her attitude.
		
		:param uid: Argument.uid
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_attitude', 'at_attitude')
		_tn			        = Translator(self.lang)
		bubbles_array       = self.__create_speechbubble_history()
		add_premise_text    = ''
		save_statement_url  = 'ajax_set_new_start_statement'
		statement_text      = get_text_for_statement_uid(uid)
		if not statement_text:
			return None
		text                = _tn.get(_tn.whatDoYouThinkAbout) + ' <strong>' + statement_text[0:1].lower() + statement_text[1:] + '</strong>?'
		# select_bubble = self.create_speechbubble_dict(is_user=True, '', '', _tn.get(_tn.youAreInterestedIn) + ': <strong>' + statement_text + '</strong>')
		bubble = self.create_speechbubble_dict(is_system=True, message=text, omit_url=True)

		# if save_crumb:
		# 	self.__append_bubble(bubbles_array, select_bubble)
		# 	self.__save_speechbubble(select_bubble, db_user, self.session_id, self.breadcrumbs[-1], transaction, statement_uid=uid)
		self.__append_bubble(bubbles_array, bubble)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_justify_statement(self, transaction, uid, save_crumb, application_url,
	                                                  slug, is_supportive, count_of_items):
		"""
		Prepares the discussion dict with all bubbles for the third step in discussion, where the user justifies his position.
		
		:param transaction: transaction
		:param uid: Argument.uid
		:param save_crumb: Boolean
		:param application_url: URL
		:param slug: Issue.info as Slug
		:param is_supportive: Boolean
		:param count_of_items: Integer
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_justify_statement', 'at_justify')
		_tn			        = Translator(self.lang)
		tmp_nick = self.nickname
		if not tmp_nick:
			tmp_nick = 'anonymous'
		db_user             = DBDiscussionSession.query(User).filter_by(nickname=tmp_nick).first()
		bubbles_array       = self.__create_speechbubble_history()
		add_premise_text    = ''
		save_statement_url  = 'ajax_set_new_start_statement'
		text				= get_text_for_statement_uid(uid)
		text                = text[0:1].upper() + text[1:]
		if not text:
			return None
		question            = _tn.get(_tn.whatIsYourMostImportantReasonWhy) + ' <strong>' + text[0:1].lower() + text[1:] + '</strong> '
		question            += _tn.get(_tn.holds if is_supportive else _tn.isNotAGoodIdea) + '?'
		because			    = _tn.get(_tn.because)[0:1].upper() + _tn.get(_tn.because)[1:].lower() + '...'
		add_premise_text	+= text + ' ' + (_tn.get(_tn.holds) if is_supportive else _tn.get(_tn.isNotAGoodIdea))

		# intro = _tn.get(_tn.youAgreeWith) if is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
		intro = '' if is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
		url = UrlManager(application_url, slug).get_slug_url(False)
		question_bubble = self.create_speechbubble_dict(is_system=True, message=question + ' <br>' + because, omit_url=True)
		if not text.endswith(('.', '?', '!')):
			text += '.'
		select_bubble = self.create_speechbubble_dict(is_user=True, url=url, message=intro + '<strong>' + text + '</strong>', omit_url=False, statement_uid=uid, is_up_vote=is_supportive)

		if save_crumb:
			self.__save_speechbubble(select_bubble, db_user, self.session_id, self.breadcrumbs[-1], transaction, statement_uid=uid)

		# check for double bubbles
		should_append = True

		if not last_relation:
			intro_rev = '' if not is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
			if len(bubbles_array) > 0:
				should_append = bubbles_array[-1]['message'] != select_bubble['message']
				if bubbles_array[-1]['message'] == intro_rev + '<strong>' + text + '</strong>':
					bubbles_array.remove(bubbles_array[-1])
			if len(bubbles_array) > 1:
				if bubbles_array[-2]['message'] == intro_rev + '<strong>' + text + '</strong>':
					bubbles_array.remove(bubbles_array[-2])

		if should_append:
			self.__append_bubble(bubbles_array, select_bubble)

		self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_status=True, uid='now', message=_tn.get(_tn.now), omit_url=True))
		self.__append_bubble(bubbles_array, question_bubble)

		if not self.nickname and count_of_items == 1:
			self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_info=True, uid='now', message=_tn.get(_tn.voteCountTextFirst) + '. ' + _tn.get(_tn.onlyOneItemWithLink), omit_url=True))

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'is_supportive': is_supportive}

	def prepare_discussion_dict_for_justify_argument(self, uid, is_supportive, attack):
		"""
		Prepares the discussion dict with all bubbles for a step in discussion, where the user justifies his attack she has done.
		
		:param uid: Argument.uid
		:param is_supportive: Boolean
		:param attack: String (undermine, support, undercut, rebut, ...)
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict', 'prepare_discussion_dict_for_justify_argument')
		_tn			       = Translator(self.lang)
		_tg                = TextGenerator(self.lang)
		bubbles_array      = self.__create_speechbubble_history()
		add_premise_text   = ''
		save_statement_url = 'ajax_set_new_premises_for_argument'

		db_argument		= DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		if not db_argument:
			return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

		confr	       = get_text_for_argument_uid(uid, self.lang, True)
		premise, tmp   = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
		conclusion     = get_text_for_conclusion(db_argument, self.lang)

		user_msg, sys_msg = _tg.get_header_for_users_confrontation_response(premise, attack, conclusion, False, is_supportive, self.nickname)

		if attack == 'undermine':
			add_premise_text = _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																	  db_argument.is_supportive)
			add_premise_text = add_premise_text[0:1].upper() + add_premise_text[1:]

		elif attack == 'support':
			is_supportive = not is_supportive
			# when the user rebuts a system confrontation, he attacks his own negated premise, therefore he supports
			# is own premise. so his premise is the conclusion and we need new premises ;-)
			add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion, is_supportive)
		elif attack == 'undercut':
			add_premise_text += _tg.get_text_for_add_premise_container(premise, premise, attack, conclusion,
																	   db_argument.is_supportive)
		else:
			add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																	   db_argument.is_supportive)

		sys_msg  = _tn.get(_tn.whatIsYourMostImportantReasonFor) + ': ' + user_msg[:-1] + '?<br>' + _tn.get(_tn.because) + '...'
		# bubble_user = self.create_speechbubble_dict(is_user=True, message=user_msg[0:1].upper() + user_msg[1:], omit_url=True)
		bubble_question = self.create_speechbubble_dict(is_system=True, message=sys_msg, omit_url=True)

		self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_status=True, uid='now', message=_tn.get(_tn.now), omit_url=True))
		# self.__append_bubble(bubbles_array, bubble_user)
		self.__append_bubble(bubbles_array, bubble_question)

		# if save_crumb:
		# 	db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		# 	self.__save_speechbubble(bubble_user, db_user, self.session_id, self.breadcrumbs[-1], transaction, argument_uid=uid)
		# 	self.__save_speechbubble(bubble_question, db_user, self.session_id, self.breadcrumbs[-1], transaction)

		# if not self.nickname and count_of_items == 1:
		# 	self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_status=True, 'now', '', _tn.get(_tn.onlyOneItemWithLink), True))

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'attack_type': attack, 'arg_uid': uid}

	def prepare_discussion_dict_for_dont_know_reaction(self, transaction, uid, save_crumb):
		"""
		Prepares the discussion dict with all bubbles for the third step, where an suppotive argument will be presented.

		:param transaction: transaction
		:param uid: Argument.uid
		:param save_crumb: Boolean
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_dont_know_reaction', 'at_dont_know')
		_tn			   = Translator(self.lang)
		db_user        = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
		bubbles_array  = self.__create_speechbubble_history()
		add_premise_text = ''
		save_statement_url = 'ajax_set_new_start_statement'

		if uid != 0:
			text			= get_text_for_argument_uid(uid, self.lang)
			text			= text.replace(_tn.get(_tn.because).lower(), '</strong>' + _tn.get(_tn.because).lower() + '<strong>')
			sys_text    	= _tn.get(_tn.otherParticipantsThinkThat) + ' <strong>' + text[0:1].lower() + text[1:]  + '</strong>. '

			bubble_sys_save = self.create_speechbubble_dict(is_system=True, message=sys_text)
			bubble_sys = self.create_speechbubble_dict(is_system=True, message=sys_text + '<br><br>' + _tn.get(_tn.whatDoYouThinkAboutThat) + '?')
			self.__append_bubble(bubbles_array, bubble_sys)

			if save_crumb:
				self.__save_speechbubble(bubble_sys_save, db_user, self.session_id, self.breadcrumbs[-1], transaction, argument_uid=uid)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_argumentation(self, transaction, uid, save_crumb, is_supportive, additional_id, attack, last_relation):
		"""
		Prepares the discussion dict with all bubbles for the argumentation window.
		
		:param transaction: transaction
		:param uid: Argument.uid
		:param save_crumb: Boolean
		:param is_supportive: Boolean
		:param additional_id: Argument.uid
		:param attack: String (undermine, support, undercut, rebut, ...)
		:param last_relation: String (undermine, support, undercut, rebut, ...)
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_argumentation', 'at_argumentation')
		_tn			        = Translator(self.lang)
		db_user             = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
		bubbles_array       = self.__create_speechbubble_history()
		add_premise_text    = ''
		save_statement_url  = 'ajax_set_new_start_statement'
		mid_text            = ''
		bubble_mid          = ''

		_tg					 = TextGenerator(self.lang)
		db_argument			 = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		if attack == 'end':
			#  user_text        = _tn.get(_tn.soYourOpinionIsThat) + ': '
			text             = get_text_for_argument_uid(uid, self.lang, True, user_changed_opinion=last_relation == 'support')
			user_text        = '<strong>' + text[0:1].upper() + text[1:] + '</strong>.'
			sys_text         = _tn.get(_tn.otherParticipantsDontHaveCounterForThat) + '.'
			mid_text         = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)
		else:
			premise, tmp	 = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
			conclusion       = get_text_for_conclusion(db_argument, self.lang)
			db_confrontation = DBDiscussionSession.query(Argument).filter_by(uid=additional_id).first()
			confr, tmp       = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid, self.lang)
			sys_conclusion   = get_text_for_conclusion(db_confrontation, self.lang)
			if attack == 'undermine':
				premise = get_text_for_statement_uid(db_confrontation.conclusion_uid) if db_confrontation.conclusion_uid != 0 \
					else get_text_for_argument_uid(db_confrontation.argument_uid, self.lang, True)

			# did the user changed his opinion?
			user_changed_opinion = len(self.breadcrumbs) > 1 and '/undercut/' in self.breadcrumbs[-2]['url']

			# argumentation is a reply for an argument, if the arguments conclusion of the user is no position
			db_statement		= DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()
			reply_for_argument  = not (db_statement and db_statement.is_startpoint)
			current_argument	= get_text_for_argument_uid(uid, self.lang, with_strong_html_tag=True,
			                                                    start_with_intro=True, user_changed_opinion=user_changed_opinion)
			user_is_attacking   = not db_argument.is_supportive

			# fix
			prefix = '</strong>' + _tn.get(_tn.soYourOpinionIsThat) + ': <strong>'
			if conclusion.startswith(prefix):
				conclusion = conclusion[len(prefix):]

			if current_argument.startswith(prefix):
				current_argument = current_argument[len(prefix):]

			current_argument = current_argument[0:1].upper() + current_argument[1:]
			premise = premise[0:1].lower() + premise[1:]

			user_text = (_tn.get(tn.otherParticipantsConvincedYouThat) + ': ') if last_relation == 'support' else ''
			user_text += '<strong>'
			user_text += current_argument if current_argument != '' else premise
			user_text += '</strong>.'

			sys_text = _tg.get_text_for_confrontation(premise, conclusion, sys_conclusion, is_supportive, attack, confr,
			                                          reply_for_argument, user_is_attacking, db_argument)

		bubble_user = self.create_speechbubble_dict(is_user=True, message=user_text, omit_url=True, argument_uid=uid, is_up_vote=is_supportive)
		if attack == 'end':
			bubble_sys  = self.create_speechbubble_dict(is_system=True, message=sys_text, omit_url=True)
			bubble_mid  = self.create_speechbubble_dict(is_info=True, message=mid_text, omit_url=True)
		else:
			bubble_sys  = self.create_speechbubble_dict(is_system=True, uid='question-bubble', message=sys_text, omit_url=True)

		# dirty fixes
		if len(bubbles_array) > 0 and bubbles_array[-1]['message'] == bubble_user['message']:
			bubbles_array.remove(bubbles_array[-1])

		self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_status=True, uid='now', message=_tn.get(_tn.now)))
		self.__append_bubble(bubbles_array, bubble_user)
		self.__append_bubble(bubbles_array, bubble_sys)

		if attack == 'end':
			self.__append_bubble(bubbles_array, bubble_mid)

		if save_crumb:
			self.__save_speechbubble(bubble_user, db_user, self.session_id, self.breadcrumbs[-1], transaction, argument_uid=uid)
			self.__save_speechbubble(bubble_sys, db_user, self.session_id, self.breadcrumbs[-1], transaction)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_choosing(self, uid, is_uid_argument, is_supportive):
		"""
		Prepares the discussion dict with all bubbles for the choosing an premise, when the user inserted more than one new premise.

		:param uid: Argument.uid
		:param is_uid_argument: Boolean
		:param is_supportive: Boolean
		:return:
		"""
		_tn			   = Translator(self.lang)
		bubbles_array  = self.__create_speechbubble_history()
		add_premise_text = ''
		save_statement_url = 'ajax_set_new_start_statement'

		logger('DictionaryHelper', 'prepare_discussion_dict', 'at_choosing')
		text = _tn.get(_tn.soYouEnteredMultipleReasons) + '.'
		text += _tn.get(_tn.whyAreYouAgreeingWith) if is_supportive else _tn.get(_tn.whyAreYouDisagreeingWith)
		text += ':<br><strong>'
		text += get_text_for_argument_uid(uid, self.lang, True) if is_uid_argument else get_text_for_statement_uid(uid)
		text += '</strong>?<br>' + _tn.get(_tn.because) + '...'

		self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_status=True, uid='now', message='Now', omit_url=True))
		self.__append_bubble(bubbles_array, self.create_speechbubble_dict(is_user=True, uid='question-bubble', message=text, omit_url=True))

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}
	
	def create_speechbubble_dict(self, is_user=False, is_system=False, is_status=False, is_info=False, uid='', url='',
	                             message='', omit_url=False, argument_uid=None, statement_uid=None, is_up_vote=True,
	                             add_del_history=False):
		"""
		Creates an dictionary with every information needed for a bubble.

		:param is_user: Boolean
		:param is_system: Boolean
		:param is_status: Boolean
		:param is_info: Boolean
		:param uid: Argument.uid
		:param url: URL
		:param message: String
		:param omit_url: Boolean
		:param argument_uid: Argument.uid
		:param statement_uid: Statement.uid
		:param is_up_vote: Boolean
		:return: dict()
		"""
		speech = dict()
		speech['is_user']            = is_user
		speech['is_system']          = is_system
		speech['is_status']          = is_status
		speech['is_info']            = is_info
		speech['id']                 = uid if len(str(uid)) > 0 else 'None'
		speech['url']                = url if len(str(url)) > 0 else 'None'
		speech['url']                = (url + ('&' if '?' in url else '?') + 'del_history=true') if len(str(url)) > 0 else 'None'
		speech['message']            = message
		speech['omit_url']           = omit_url
		speech['data_type']          = 'argument' if argument_uid else 'statement' if statement_uid else 'None'
		speech['data_argument_uid']  = str(argument_uid)
		speech['data_statement_uid'] = str(statement_uid)
		db_votecounts                = None

		if argument_uid:
			db_votecounts = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
			                                                                    VoteArgument.is_up_vote == is_up_vote,
			                                                                    VoteArgument.is_valid == True)).all()
		elif statement_uid:
			db_votecounts = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement_uid,
			                                                                     VoteStatement.is_up_vote == is_up_vote,
			                                                                     VoteStatement.is_valid == True)).all()
		_t = Translator(self.lang)
		diff = 0
		tmp_nick = self.nickname
		if tmp_nick:
			diff = 1 if tmp_nick != 'anonymous' else 0
		votecounts = len(db_votecounts) - diff if db_votecounts else 0

		if votecounts == 0:
			speech['votecounts_message'] = _t.get(_t.voteCountTextFirst) + '.'
		elif votecounts == 1:
			speech['votecounts_message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			speech['votecounts_message'] = str(votecounts) + ' ' + _t.get(_t.voteCountTextMore) + '.'
		speech['votecounts'] = votecounts

		return speech

	@staticmethod
	def __append_bubble(bubbles_array, bubble):
		"""
		Reeturn current bubbles_array with bubble appended.

		:param bubbles_array: Bubbles[]
		:param bubble: Bubble
		:return: []
		"""
		# sanity check
		if len(bubbles_array) > 2:
			for i in range(-3, 0):
				if bubbles_array[i]['message'] == bubble['message']:
					bubbles_array.remove(bubbles_array[i])

		bubbles_array.append(bubble)

	@staticmethod
	def __save_speechbubble(bubble_dict, db_user, session_id, related_breadcrumb, transaction, argument_uid=None, statement_uid=None):
		"""
		Saves given bubble with additional information into database.

		:param bubble_dict: dict()
		:param db_user: User
		:param session_id: request.session_id
		:param related_breadcrumb: Breadcrumb
		:param transaction: transaction
		:param argument_uid: Argument.uid
		:param statement_uid: Statement.uid
		:return: True if Bubble was saved
		"""
		if not db_user:
			user = 'anonymous'
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if not db_user:
				return False

		is_user   = bubble_dict['is_user']
		is_system = bubble_dict['is_system']
		is_status = bubble_dict['is_status']
		latest_bubble = DBDiscussionSession.query(Bubble).filter(and_(Bubble.breadcrumb_uid == related_breadcrumb['uid'],
		                                                              Bubble.author_uid == db_user.uid)).order_by(Bubble.uid.desc()).first()
		latest_specific_bubble = DBDiscussionSession.query(Bubble).filter(and_(Bubble.author_uid == db_user.uid,
		                                                                       Bubble.is_user == is_user,
																			   Bubble.is_system == is_system,
																			   Bubble.is_status == is_status)).order_by(Bubble.uid.desc()).first()
		if latest_bubble and latest_bubble.content == bubble_dict['message'] or \
						latest_specific_bubble and latest_specific_bubble.content == bubble_dict['message']:
				return False

		logger('DictionaryHelper', '__save_speechbubble', 'bubble_id = ' + str(bubble_dict['id']) +
		       ', user=' + str(db_user.uid) +
		       ', content=' + str(bubble_dict['message']) +
		       ', is_user=' + str(bubble_dict['is_user']) +
		       ', is_system=' + str(bubble_dict['is_system']) +
		       ', is_status=' + str(bubble_dict['is_status']) +
		       ', session_id=' + str(session_id) +
		       ', breadcrumb_uid=' + str(related_breadcrumb['uid']) +
		       ', argument_uid=' + str(argument_uid) +
		       ', statement_uid=' + str(statement_uid))
		DBDiscussionSession.add(Bubble(bubble_id=bubble_dict['id'],
		                               user=str(db_user.uid),
		                               content=bubble_dict['message'],
		                               is_user=bubble_dict['is_user'],
		                               is_system=bubble_dict['is_system'],
		                               is_status=bubble_dict['is_status'],
		                               is_info=bubble_dict['is_info'],
		                               session_id=session_id,
		                               breadcrumb_uid=str(related_breadcrumb['uid']),
		                               related_argument_uid=argument_uid,
									   related_statement_uid=statement_uid))
		transaction.commit()
		return True

	def __create_speechbubble_history(self):
		"""
		Creates the history of speech bubbles.

		:return: []
		"""
		logger('DictionaryHelper', '__create_speechbubble_history', 'main')
		bubble_history = []
		is_user_anonym = not self.nickname
		tmp_nick = 'anonymous' if is_user_anonym else self.nickname
		db_user = DBDiscussionSession.query(User).filter_by(nickname=tmp_nick).first()
		for crumb in self.breadcrumbs:
			if is_user_anonym:
				history = DBDiscussionSession.query(Bubble).filter(and_(Bubble.breadcrumb_uid == crumb['uid'],
				                                                        Bubble.author_uid == db_user.uid,
				                                                        Bubble.session_id == self.session_id)).all()
			else:
				history = DBDiscussionSession.query(Bubble).filter(and_(Bubble.breadcrumb_uid == crumb['uid'],
				                                                        Bubble.author_uid == db_user.uid)).all()
			for h in history:
				is_user   = h.is_user
				is_system = h.is_system
				is_status = h.is_status
				is_info   = h.is_info
				uid       = crumb['uid']
				url       = crumb['url']
				content   = h.content
				rel_arg   = h.related_argument_uid
				rel_stat  = h.related_statement_uid
				if h.related_argument_uid:
					is_supp = DBDiscussionSession.query(Argument).filter_by(uid=h.related_argument_uid).first().is_supportive
				else:
					expr0     = re.search(re.compile(r"/t/"), url)
					expr1     = re.search(re.compile(r"/t$"), url)
					group0    = expr0.group(0) if expr0 else None
					group1    = expr1.group(0) if expr1 else None
					is_supp   = True if group0 or group1 else False
				bubble_history.append(self.create_speechbubble_dict(is_user=is_user, is_system=is_system, is_status=is_status, is_info=is_info,
				                                                    uid=uid, url=url, message=content, omit_url=False,
				                                                    argument_uid=rel_arg, statement_uid=rel_stat, is_up_vote=is_supp))

		return bubble_history
