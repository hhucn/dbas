"""
Provides helping function for dictionaries.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
from datetime import datetime

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User
from dbas.helper.dictionary_helper_discussion import DiscussionDictHelper
from dbas.helper.notification_helper import NotificationHelper
from dbas.helper.query_helper import QueryHelper
from dbas.lib import get_text_for_argument_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion
from dbas.logger import logger
from dbas.strings import Translator, TextGenerator
from dbas.url_manager import UrlManager
from dbas.user_management import UserHandler


class DictionaryHelper(object):
	"""
	General function for dictionaries as well as the extras-dict()
	"""

	def __init__(self, lang=''):
		"""
		Initialize default values

		:param lang: ui_locales
		:return:
		"""
		self.lang = lang

	@staticmethod
	def get_random_subdict_out_of_orderer_dict(ordered_dict, count):
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

	def prepare_extras_dict_for_normal_page(self, nickname):
		"""
		Calls self.prepare_extras_dict('', False, False, False, False, False, nickname)
		:param nickname: Users.nickname
		:return: dict()
		"""
		return self.prepare_extras_dict('', False, False, False, False, False, nickname)

	def prepare_extras_dict(self, current_slug, is_editable, is_reportable, show_bar_icon,
	                        show_display_styles, show_expert_icon, authenticated_userid, argument_id=0,
	                        application_url='', for_api=False,):
		"""
		Creates the extras.dict() with many options!

		:param current_slug:
		:param is_editable: Boolean
		:param is_reportable: Boolean
		:param show_bar_icon: Boolean
		:param show_display_styles: Boolean
		:param show_expert_icon: Boolean
		:param authenticated_userid: User.nickname
		:param argument_id: Argument.uid
		:param application_url: String
		:param for_api: Boolean
		:return: dict()
		"""
		logger('DictionaryHelper', 'prepare_extras_dict', 'def')
		_uh = UserHandler
		_tn = Translator(self.lang)
		is_logged_in = _uh.is_user_logged_in(authenticated_userid)
		nickname = authenticated_userid if authenticated_userid else 'anonymous'
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

		return_dict = dict()
		return_dict['restart_url']		             = UrlManager(application_url, current_slug, for_api).get_slug_url(True)
		return_dict['logged_in']		             = is_logged_in
		return_dict['nickname']		                 = nickname
		return_dict['users_name']		             = str(authenticated_userid)
		return_dict['add_premise_container_style']   = 'display: none'
		return_dict['add_statement_container_style'] = 'display: none'
		return_dict['users_avatar']                  = _uh.get_profile_picture(db_user)
		return_dict['is_user_male']                  = db_user.gender == 'm' if db_user else False
		return_dict['is_user_female']                = db_user.gender == 'f' if db_user else False
		return_dict['is_user_neutral']               = not return_dict['is_user_male'] and not return_dict['is_user_female']
		self.add_language_options_for_extra_dict(return_dict)

		if not for_api:
			return_dict['is_editable']                   = is_editable and is_logged_in
			return_dict['is_reportable']	             = is_reportable
			return_dict['is_admin']			             = _uh.is_user_in_group(authenticated_userid, 'admins')
			return_dict['is_author']			         = _uh.is_user_in_group(authenticated_userid, 'authors')
			return_dict['show_bar_icon']	             = show_bar_icon and False
			return_dict['show_display_style']            = show_display_styles and False
			return_dict['show_expert_icon']              = show_expert_icon and False
			return_dict['close_premise_container']	     = True
			return_dict['close_statement_container']	 = True
			return_dict['date']	                         = datetime.strftime(datetime.now(), '%d.%m.%Y')
			return_dict['title']						 = {'barometer': _tn.get(_tn.opinionBarometer),
															'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
															'island_view': _tn.get(_tn.displayControlDialogIslandBody),
															'expert_view': _tn.get(_tn.displayControlDialogExpertBody)}
			return_dict['buttons']					     = {'report': _tn.get(_tn.report),
															'report_title': _tn.get(_tn.reportTitle),
															'finish_title': _tn.get(_tn.finishTitle),
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
															'clear_statistics': _tn.get(_tn.clearStatistics),
															'user_options': _tn.get(_tn.userOptions),
															'switch_language': _tn.get(_tn.switchLanguage),
															'login': _tn.get(_tn.login),
															'news_about_dbas': _tn.get(_tn.newsAboutDbas),
															'share_url': _tn.get(_tn.shareUrl),
			                                                'go_back': _tn.get(_tn.letsGoBack),
			                                                'go_home': _tn.get(_tn.letsGoHome),
			                                                'count_of_posts': _tn.get(_tn.countOfPosts),
			                                                'default_view': _tn.get(_tn.defaultView),
			                                                'wide_node_view': _tn.get(_tn.wideView),
			                                                'tight_node_view': _tn.get(_tn.tightView),
			                                                'show_content': _tn.get(_tn.showContent),
			                                                'hide_content': _tn.get(_tn.hideContent)}
			# /return_dict['breadcrumbs']   = breadcrumbs
			message_dict = dict()
			message_dict['new_count']    = NotificationHelper.count_of_new_notifications(authenticated_userid)
			message_dict['has_unread']   = (message_dict['new_count'] > 0)
			message_dict['all']		     = NotificationHelper.get_notification_for(authenticated_userid)
			message_dict['total']		 = len(message_dict['all'])
			return_dict['notifications'] = message_dict

			# add everything for the island view
			if return_dict['show_display_style']:
				# does an argumente exists?
				db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()
				if db_argument:
					island_dict = QueryHelper.get_every_attack_for_island_view(argument_id, self.lang)

					db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()
					premise, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
					conclusion = get_text_for_conclusion(db_argument, self.lang)
					island_dict['heading'] = get_text_for_argument_uid(argument_id, self.lang, True)

					island_dict['premise'] = premise[0:1].lower() + premise[1:]
					island_dict['conclusion'] = conclusion[0:1].lower() + conclusion[1:]
					island_dict.update(TextGenerator(self.lang).get_relation_text_dict(island_dict['premise'],
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

	def add_discussion_end_text(self, discussion_dict, extras_dict, logged_in, at_start=False, at_dont_know=False,
								at_justify_argumentation=False, at_justify=False, current_premise='', supportive=False):
		"""
		Adds a speicif text when the discussion is at the end

		:param discussion_dict: dict()
		:param extras_dict: dict()
		:param logged_in: Boolean
		:param at_start: Boolean
		:param at_dont_know: Boolean
		:param at_justify_argumentation: Boolean
		:param at_justify: Boolean
		:param current_premise: id
		:param supportive: supportive
		:return: None
		"""
		logger('DictionaryHelper', 'add_discussion_end_text', 'main')
		_tn = Translator(self.lang)
		current_premise = current_premise[0:1].lower() + current_premise[1:]
		_ddh = DiscussionDictHelper(self.lang, '', '', None)

		if at_start:
			discussion_dict['mode'] = 'start'
			user_text = _tn.get(_tn.firstPositionText) + '<br>'
			user_text += _tn.get(_tn.pleaseAddYourSuggestion) if logged_in else (_tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.feelFreeToLogin))
			discussion_dict['bubbles'].append(_ddh.create_speechbubble_dict(is_status=True, uid='end', message=user_text))
			if logged_in:
				extras_dict['add_statement_container_style'] = ''  # this will remove the 'display: none;'-style
				extras_dict['close_statement_container'] = False
			extras_dict['show_display_style']	= False
			extras_dict['show_bar_icon']	    = False
			extras_dict['is_editable']		    = False
			extras_dict['is_reportable']		= False

		elif at_justify_argumentation:
			discussion_dict['mode'] = 'justify_argumentation'
			if logged_in:
				extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
			extras_dict['close_premise_container'] = False
			extras_dict['show_display_style'] = False
			if logged_in:
				mid_text = _tn.get(_tn.firstOneReason)
				discussion_dict['bubbles'].append(_ddh.create_speechbubble_dict(is_info=True, uid='end', message=mid_text))
			# else:
			# 	mid_text = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.feelFreeToLogin)

		elif at_dont_know:
			discussion_dict['mode'] = 'dont_know'
			sys_text  = _tn.get(_tn.firstOneInformationText) + ' <strong>' + current_premise + '</strong>, '
			sys_text += _tn.get(_tn.soThatOtherParticipantsDontHaveOpinionRegardingYourOpinion) + '.'
			mid_text  = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)
			discussion_dict['bubbles'].append(_ddh.create_speechbubble_dict(is_system=True, uid='end', message=sys_text))
			discussion_dict['bubbles'].append(_ddh.create_speechbubble_dict(is_info=True, uid='end', message=mid_text))

		elif at_justify:
			discussion_dict['mode'] = 'justify'
			mid_text = _tn.get(_tn.firstPremiseText1) + ' <strong>' + current_premise + '</strong>'
			if not supportive:
				mid_text += ' ' + _tn.get(_tn.doesNotHold)
			mid_text += '.<br>'
			# pretty prints
			#if discussion_dict['bubbles'][-1]['is_system'] and discussion_dict['bubbles'][-2]['message'] == _tn.get(_tn.now):
			#	discussion_dict['bubbles'].remove(discussion_dict['bubbles'][-1])
			#	discussion_dict['bubbles'].remove(discussion_dict['bubbles'][-1])
			if logged_in:
				extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
				mid_text += _tn.get(_tn.firstPremiseText2)
			else:
				mid_text += _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)

			discussion_dict['bubbles'].append(_ddh.create_speechbubble_dict(is_info=True, uid='end', message=mid_text))
			extras_dict['close_premise_container'] = False
			extras_dict['show_display_style']	   = False
			extras_dict['show_bar_icon']		   = False
			extras_dict['is_editable']			   = False
			extras_dict['is_reportable']		   = False

		else:
			mid_text = _tn.get(_tn.discussionEnd) + ' ' + (_tn.get(_tn.discussionEndLinkText) if logged_in else _tn.get(_tn.feelFreeToLogin))
			discussion_dict['bubbles'].append(_ddh.create_speechbubble_dict(is_info=True, message=mid_text))

	def add_language_options_for_extra_dict(self, extras_dict):
		"""
		Adds language options to the extra-dictionary

		:param extras_dict: current dict()
		:return: dict()
		"""
		logger('DictionaryHelper', 'add_language_options_for_extra_dict', 'def')
		lang_is_en = (self.lang != 'de')
		lang_is_de = (self.lang == 'de')
		extras_dict.update({
			'lang_is_de': lang_is_de,
			'lang_is_en': lang_is_en,
			'link_de_class': ('active' if lang_is_de else ''),
			'link_en_class': ('active' if lang_is_en else '')
		})
