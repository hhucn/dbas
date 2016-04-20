"""
Provides helping function for creating the history as bubbles.

.. codeauthor: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from sqlalchemy import and_

from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import VoteArgument, VoteStatement, Argument, Statement
from dbas.strings import Translator, TextGenerator
from dbas.url_manager import UrlManager


class HistoryHelper:
	"""
	Helper class for parsing and consuming the history
	"""

	@staticmethod
	def create_bubbles_from_history(history, nickname='', lang='', application_url=''):
		"""
		Creates the bubbles for every history step
		
		:param history: String 
		:param nickname: User.nickname
		:param lang: ui_locales
		:param application_url: String
		:return: Array
		"""
		if len(history) == 0:
			return

		logger('HistoryHelper', 'create_bubbles_from_history', 'history: ' + history)
		splitted_history = history.split('-')

		logger('HistoryHelper', 'create_bubbles_from_history', 'steps: ' + str(len(splitted_history)))
		bubble_array = []

		nickname = nickname if nickname else 'anonymous'

		for index, step in enumerate(splitted_history):
			logger('HistoryHelper', 'create_bubbles_from_history', 'step: ' + step[1:])

			if '/justify/' in step:
				logger('HistoryHelper', 'create_bubbles_from_history', str(index) + ': ' + step[1:])
				steps    = step.split('/')
				mode     = steps[2]  # Todo: mode in 'justify' branch of create_bubbles_from_history
				relation = steps[3]  # Todo: relaton in 'justify' branch of create_bubbles_from_history

				if [c for c in ('t', 'f') if c in mode] and relation == '':
					bubble_array.append(HistoryHelper.__justify_statement_step(step[1:], nickname, lang))

				#  elif 'd' in mode and relation == '':

				elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
					bubble_array.append(HistoryHelper.__dont_know_step(step[1:], nickname, lang))

			elif '/reaction/' in step:
				logger('HistoryHelper', 'create_bubbles_from_history', str(index) + ': ' + step[1:])
				bubble_user, bubble_syst = HistoryHelper.__reaction_step(step[1:], nickname, lang, splitted_history)
				bubble_array.append(bubble_user)
				bubble_array.append(bubble_syst)

			#  elif '/choose/' in step:
			#  logger('HistoryHelper', 'create_bubbles_from_history', str(index) + ': ' + step[1:])

			else:
				logger('HistoryHelper', 'create_bubbles_from_history', 'UNUSED ' + str(index) + ': ' + step[1:])
				logger('HistoryHelper', 'create_bubbles_from_history', 'UNUSED ' + str(index) + ': ' + step[1:])
				logger('HistoryHelper', 'create_bubbles_from_history', 'UNUSED ' + str(index) + ': ' + step[1:])

		logger('HistoryHelper', '- - - - - - - - - -', ' - - - - - BUBBLE HISTORY BELOW')
		for index, bubble in enumerate(bubble_array):
			logger('HistoryHelper', 'create_bubbles_from_history', 'bubble ' + str(index) + ': ' + str(bubble))
		logger('HistoryHelper', '- - - - - - - - - -', ' - - - - - BUBBLE HISTORY ABOVE')

		return bubble_array

	@staticmethod
	def __justify_statement_step(step, nickname, lang):
		"""
		Creates bubbles for the justify-keyword for an statement.

		:param step: String
		:param nickname: User.nickname
		:param lang: ui_locales
		:return: dict()
		"""
		steps   = step.split('/')
		uid     = int(steps[1])
		#  slug    = ''
		is_supportive = steps[2] == 't' or steps[2] == 'd'  # supportive = t(rue) or d(ont know) mode

		_tn		 = Translator(lang)
		#  url     = UrlManager(application_url, slug).get_slug_url(False)
		intro   = '' if is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
		text	= get_text_for_statement_uid(uid)
		text    = text[0:1].upper() + text[1:]
		return HistoryHelper.__create_speechbubble_dict(is_user=True, message=intro + '<strong>' + text + '</strong>',
		                                                omit_url=False, statement_uid=uid, is_up_vote=is_supportive,
		                                                nickname=nickname, lang=lang)

	@staticmethod
	def __dont_know_step(step, nickname, lang):
		"""
		Creates bubbles for the dont-know-reaction for a statement.

		:param step: String
		:param nickname: User.nickname
		:param lang: ui_locales
		:return: dict()
		"""
		steps    = step.split('/')
		uid      = int(steps[1])

		_tn		 = Translator(lang)
		text	 = get_text_for_argument_uid(uid, lang)
		text	 = text.replace(_tn.get(_tn.because).lower(), '</strong>' + _tn.get(_tn.because).lower() + '<strong>')
		sys_text = _tn.get(_tn.otherParticipantsThinkThat) + ' <strong>' + text[0:1].lower() + text[1:]  + '</strong>. '
		return HistoryHelper.__create_speechbubble_dict(is_system=True, message=sys_text, nickname=nickname, lang=lang)

	@staticmethod
	def __reaction_step(step, nickname, lang, splitted_history):
		"""
		Creates bubbles for the reaction-keyword.

		:param step: String
		:param nickname: User.nickname
		:param lang: ui_locales
		:param splitted_history: [String].uid
		:return: dict(), dict()
		"""
		steps           = step.split('/')
		uid             = int(steps[1])
		additional_uid  = int(steps[3])
		attack          = steps[2]

		is_supportive   = DBDiscussionSession.query(Argument).filter_by(uid=uid).first().is_supportive
		last_relation   = splitted_history[-1].split('/')[2]  # Todo: last_relation in __reaction_step

		user_changed_opinion = len(splitted_history) > 1 and '/undercut/' in splitted_history[-2]
		current_argument     = get_text_for_argument_uid(uid, lang, with_strong_html_tag=True, start_with_intro=True, user_changed_opinion=user_changed_opinion)
		db_argument			 = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		db_confrontation     = DBDiscussionSession.query(Argument).filter_by(uid=additional_uid).first()
		db_statement		 = DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()

		premise, tmp         = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
		conclusion           = get_text_for_conclusion(db_argument, lang)
		sys_conclusion       = get_text_for_conclusion(db_confrontation, lang)
		confr, tmp           = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid, lang)
		reply_for_argument   = not (db_statement and db_statement.is_startpoint)
		user_is_attacking    = not db_argument.is_supportive

		_tn = Translator(lang)
		user_text = (_tn.get(_tn.otherParticipantsConvincedYouThat) + ': ') if last_relation == 'support' else ''
		user_text += '<strong>'
		user_text += current_argument if current_argument != '' else premise
		user_text += '</strong>.'
		sys_text = TextGenerator(lang).get_text_for_confrontation(premise, conclusion, sys_conclusion, is_supportive,
		                                                          attack, confr, reply_for_argument, user_is_attacking,
		                                                          db_argument)

		bubble_user = HistoryHelper.__create_speechbubble_dict(is_user=True, message=user_text, omit_url=True, argument_uid=uid, is_up_vote=is_supportive, nickname=nickname, lang=lang)
		if attack == 'end':
			bubble_syst  = HistoryHelper.__create_speechbubble_dict(is_system=True, message=sys_text, omit_url=True, nickname=nickname, lang=lang)
		else:
			bubble_syst  = HistoryHelper.__create_speechbubble_dict(is_system=True, uid='question-bubble', message=sys_text, omit_url=True, nickname=nickname, lang=lang)
		return bubble_user, bubble_syst

	@staticmethod
	def __create_speechbubble_dict(is_user=False, is_system=False, is_status=False, is_info=False, uid='', url='',
	                               message='', omit_url=False, argument_uid=None, statement_uid=None, is_up_vote=True,
	                               nickname='anonymous', lang='en'):
		"""
		Creates an dictionary which includes every information needed for a bubble.

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
		:param nickname: String
		:param lang: String
		:return: dict()
		"""
		speech = dict()
		speech['is_user']            = is_user
		speech['is_system']          = is_system
		speech['is_status']          = is_status
		speech['is_info']            = is_info
		speech['id']                 = uid if len(str(uid)) > 0 else 'None'
		# speech['url']                = url if len(str(url)) > 0 else 'None'
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
		_t = Translator(lang)
		diff = 1 if nickname != 'anonymous' else 0  # Todo: Check difference of vote count
		votecounts = len(db_votecounts) - diff if db_votecounts else 0

		if votecounts == 0:
			speech['votecounts_message'] = _t.get(_t.voteCountTextFirst) + '.'
		elif votecounts == 1:
			speech['votecounts_message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			speech['votecounts_message'] = str(votecounts) + ' ' + _t.get(_t.voteCountTextMore) + '.'
		speech['votecounts'] = votecounts

		return speech
