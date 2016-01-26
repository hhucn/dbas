import collections
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, History
from .logger import logger
from .strings import Translator
from .query_helper import QueryHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class BreadcrumbHelper(object):

	def save_breadcrumb(self, url, user, session_id):
		"""

		:param url:
		:param user:
		:param session_id:
		:return:
		"""
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'url ' + url + ', user ' + str(user))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		db_already_in = DBDiscussionSession.query(History).filter_by(url=url).first()
		if db_already_in:
			DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid, History.uid>db_already_in.uid)).delete()
		else:
			DBDiscussionSession.add(History(user=db_user.uid, url=url, session_id=session_id))
			transaction.commit()

		return self.get_breadcrumbs(user)

	def get_breadcrumbs(self, user):
		"""

		:param user:
		:return:
		"""
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'user ' + str(user))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			logger('BreadcrumbHelper', 'get_breadcrumbs', 'no user')
			return dict()

		db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()

		if not db_history:
			logger('BreadcrumbHelper', 'get_breadcrumbs', 'no track')
			return dict()

		breadcrumbs = []
		for index, history in enumerate(db_history):
			hist = dict()
			hist['url']     = str(history.url)
			hist['text']    = 'some text'
			breadcrumbs.append(hist)

		return breadcrumbs

	# def save_breadcrumb_for_user_with_statement_uid(self, transaction, user, url, statement_uid, was_action_done, is_supportive,
	#                                                 lang, session_id):
	# 	"""
	# 	Saves history for user with statement_uid as keyword. Calls save_breadcrumb_for_user(self, transaction, user, url, keyword, session_id)
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param statement_uid: uid of the statement
	# 	:param was_action_done: true, if the user has done a decision
	# 	:param is_supportive: true, if the given decision was supportive
	# 	:param lang: current lang
	# 	:param session_id: current session id
	# 	:return: undefined
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_history_for_user_with_statement_uid', 'def')
	# 	db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid)).first()
	# 	db_textversion  = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).first()
	# 	text = db_textversion.content
	#
	# 	returned_in_history = self.save_breadcrumb_for_user(transaction, user, url, text, session_id)
	#
	# 	# manipualte entries only, if we do not stepped back via urls
	# 	if not returned_in_history:
	# 		# was some decision like attack, support, dont know done?
	# 		if was_action_done:
	# 			_t = Translator(lang)
	# 			text = text[0:1].upper() + text[1:]
	# 			if is_supportive is '':
	# 				text = _t.get(_t.moreAbout) + ': ' + text
	# 			else:
	# 				text = (_t.get(_t.support) if is_supportive else _t.get(_t.attack)) + ': ' + text
	# 			self.update_last_record_in_breadcrumbs(transaction, user, text)
	# 		else:
	# 			self.update_last_record_in_breadcrumbs(transaction, user, text)
	#
	#
	# def save_breadcrumb_for_user_with_argument_parts(self, transaction, user, url, premisegroups_uid, conclusion_uid, issue,
	#                                                  is_supportive, session_id, lang, additional_params):
	# 	"""
	# 	Saves history for user with statement_uid as keyword. Calls save_breadcrumb_for_user(self, transaction, user, url, keyword, session_id)
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param premisegroups_uid: uid of the premisegroup
	# 	:param conclusion_uid: uid of the conclusion
	# 	:param issue: uid of the issue
	# 	:param is_supportive: true, if the given decision was supportive
	# 	:param session_id: current session id
	# 	:param lang: current language
	# 	:param additional_params: additional paramseters
	# 	:return: undefined
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_argument_parts', 'def')
	# 	db_statement = DBDiscussionSession.query(Statement).filter_by(uid=conclusion_uid).first()
	# 	db_textversion  = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).first()
	# 	text1, tmp = QueryHelper().get_text_for_premisesGroup_uid(premisegroups_uid)
	# 	text2 = db_textversion.content.lower()
	#
	# 	# change additional information, if they are not present
	# 	if 'attack_arg' not in url:
	# 		confrontation_argument_uid = additional_params['confrontation_argument_uid']
	# 		attack = additional_params['attack']
	# 		pos = url.find('/', url.find('&'))
	# 		logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_argument_parts', url)
	# 		url = url[0:pos] + '&attack_with=' + attack + '&' + 'attack_arg=' + str(confrontation_argument_uid) + url[pos:]
	# 		logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_argument_parts', url)
	#
	# 	_t = Translator(lang)
	# 	arg = text2 + ' ' + _t.get(_t.because).lower() + ' ' + text1
	# 	returned_in_history = self.save_breadcrumb_for_user(transaction, user, url, arg, session_id)
	#
	# 	if not returned_in_history:
	# 		text2 = text2[0:1].upper() + text2[1:]
	# 		if text2.endswith(('.','!','?')):
	# 			text2 = text2[:-1]
	#
	# 		if not text1.endswith(('.','!','?')):
	# 			text1 += '.'
	#
	# 		arg = text2 + ' ' + (_t.get(_t.because).lower() if is_supportive else _t.get(_t.doesNotHoldBecause).lower()) + ' ' + text1
	# 		self.update_last_record_in_breadcrumbs(transaction, user, arg)
	#
	# def save_breadcrumb_for_user_with_premissegroups_uid(self, transaction, user, url, premisegroup_uid1, premisegroup_uid2, issue,
	#                                                      session_id):
	# 	"""
	# 	Saves history for user with statement_uid as keyword. Calls save_breadcrumb_for_user(self, transaction, user, url, keyword, session_id)
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param premisegroup_uid1: uid of the premisegroup1
	# 	:param premisegroup_uid2: uid of the premisegroup2
	# 	:param issue: uid of the issue
	# 	:param session_id: current session id
	# 	:return: undefined
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_premissegroups_uid', 'def')
	# 	text1, tmp = QueryHelper().get_text_for_premisesGroup_uid(premisegroup_uid1)
	# 	text2, tmp = QueryHelper().get_text_for_premisesGroup_uid(premisegroup_uid2)
	#
	# 	text1 = text1[0:1].upper() + text1[1:]
	# 	if text1.endswith(('.','!','?')):
	# 		text1 = text1[:-1]
	#
	# 	text2 = text2[0:1].upper() + text2[1:]
	# 	if text2.endswith(('.','!','?')):
	# 		text2 = text2[:-1]
	# 	returned_in_history = self.save_breadcrumb_for_user(transaction, user, url, text1 + ' vs. ' + text2, session_id)
	# 	if not returned_in_history:
	# 		self.update_last_record_in_breadcrumbs(transaction, user, text1 + ' vs. ' + text2)
	#
	# def save_breadcrumb_for_user_with_premissegroup_of_arguments_uid(self, transaction, user, url, argument_uid, issue, relation,
	#                                                                  session_id, lang):
	# 	"""
	# 	Saves history for user with statement_uid as keyword. Calls save_breadcrumb_for_user(self, transaction, user, url, keyword, session_id)
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param argument_uid: uid of the argument
	# 	:param issue: uid of the issue
	# 	:param relation: relation of the issue
	# 	:param session_id: current session id
	# 	:param lang: current language
	# 	:return: undefined
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_premissegroup_of_arguments_uid', 'def')
	# 	db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==int(argument_uid), Argument.issue_uid==issue)).first()
	# 	text, tmp = QueryHelper().get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
	# 	returned_in_history = self.save_breadcrumb_for_user(transaction, user, url, text, session_id)
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_premissegroup_of_arguments_uid', 'returned user in breadcrumbs: ' + str(returned_in_history))
	# 	if not returned_in_history:
	# 		_t = Translator(lang)
	# 		text1 = _t.get(relation + '1')
	# 		text2 = _t.get(relation + '2')
	# 		who = 'save_breadcrumb_for_user_with_premissegroup_of_arguments_uid'
	# 		when = 'calling update_last_record_in_breadcrumbs with: '
	# 		logger('BreadcrumbHelper', who, when + text1)
	# 		logger('BreadcrumbHelper', who, when + text)
	# 		logger('BreadcrumbHelper', who, when + text2)
	# 		# pretty printing
	# 		if text1 == '':
	# 			text = text[0:1].upper() + text[1:]
	#
	# 		self.update_last_record_in_breadcrumbs(transaction, user, text1 + ' ' + text + ' ' + text2)
	#
	# def save_breadcrumb_for_user_with_action(self, transaction, user, url, statement_uid, supportive, session_id, lang):
	# 	"""
	# 	Saves history for user with statement_uid as keyword. Calls save_breadcrumb_for_user(self, transaction, user, url, keyword, session_id)
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param statement_uid: uid of the statement
	# 	:param supportive: uid of the statement
	# 	:param session_id: current session id
	# 	:param lang: current language
	# 	:return: undefined
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_action', 'def')
	# 	db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid)).first()
	# 	db_textversion  = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).first()
	# 	_t = Translator(lang)
	# 	attribute = _t.get(_t.support) if supportive else _t.get(_t.attack)
	# 	text = db_textversion.content
	# 	self.save_breadcrumb_for_user(transaction, user, url, attribute + ' ' + text, session_id)
	#
	#
	# def save_breadcrumb_for_user_with_lang(self, transaction, user, url, keyword, session_id, lang):
	# 	"""
	# 	Saves history for user
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param keyword: specific additional information
	# 	:param session_id: current session id
	# 	:param lang: current language
	# 	:return: undefined
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user_with_lang', 'def')
	# 	self.save_breadcrumb_for_user(transaction, user, url, Translator(lang).get(keyword), session_id)
	#
	#
	# def save_breadcrumb_for_user(self, transaction, user, url, keyword, session_id):
	# 	"""
	# 	Saves history for user
	# 	:param transaction: current transaction
	# 	:param user: authentication nick id of the user
	# 	:param url: current url
	# 	:param keyword: specific additional information
	# 	:param session_id: current session id
	# 	:return: boolean, if the user took a backstep
	# 	"""
	# 	logger('BreadcrumbHelper', 'save_breadcrumb_for_user', 'def')
	# 	if user is None:
	# 		user = 'anonymous'
	#
	# 	db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
	# 	logger('QueryHelper', 'save_breadcrumb_for_user', 'user: ' + user)
	# 	logger('QueryHelper', 'save_breadcrumb_for_user', 'db_user: ' + str(db_user.uid))
	# 	logger('QueryHelper', 'save_breadcrumb_for_user', 'url ' + str(url))
	# 	logger('QueryHelper', 'save_breadcrumb_for_user', 'keyword ' + str(keyword))
	# 	logger('QueryHelper', 'save_breadcrumb_for_user', 'session_id ' + str(session_id))
	# 	returned_in_history = False
	#
	# 	# check for duplicates
	# 	db_history = DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid, History.url==url)).order_by(History.uid.desc()).first()
	# 	if db_history:
	# 		returned_in_history = True
	# 		db_history = DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid, History.uid>db_history.uid)).all()
	# 		logger('BreadcrumbHelper', 'save_breadcrumb_for_user', 'duplicate check, unnecessary entries: ' + str(len(db_history)))
	# 		for history in db_history:
	# 			logger('BreadcrumbHelper', 'save_breadcrumb_for_user', 'duplicate check, deleting history: ' + str(history.uid))
	# 			DBDiscussionSession.query(History).filter_by(uid=history.uid).delete()
	# 	else:
	# 		logger('BreadcrumbHelper', 'save_breadcrumb_for_user', 'saving url: ' + url)
	# 		DBDiscussionSession.add(History(user=db_user.uid, url=url, keyword_before_decission=keyword, session_id=session_id))
	# 	transaction.commit()
	#
	# 	return returned_in_history
	#
	# def get_breadcrumbs_of_user(self, user):
	# 	"""
	# 	Returns the complete track of given user
	# 	:param user: current user id
	# 	:return: track os the user id as dict
	# 	"""
	# 	logger('QueryHelper', 'get_breadcrumbs_of_user', 'user ' + str(user))
	# 	db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
	#
	# 	if not db_user:
	# 		logger('QueryHelper', 'get_breadcrumbs_of_user', 'no user')
	# 		return dict()
	#
	# 	db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()
	#
	# 	if not db_history:
	# 		logger('QueryHelper', 'get_breadcrumbs_of_user', 'no track')
	# 		return dict()
	#
	# 	return_dict = collections.OrderedDict()
	#
	# 	for index, history in enumerate(db_history):
	# 		hist = dict()
	# 		hist['uid']                         = str(history.uid)
	# 		hist['author_uid']                  = str(history.author_uid)
	# 		hist['url']                         = str(history.url)
	# 		hist['keyword_before_decission']    = str(history.keyword_before_decission)
	# 		hist['keyword_after_decission']     = str(history.keyword_after_decission)
	# 		hist['timestamp']                   = str(history.timestamp)
	# 		return_dict[str(index+1)]           = hist
	#
	# 	return return_dict
	#
	# def update_last_record_in_breadcrumbs(self, transaction, user, keyword_after_decission):
	# 	"""
	# 	Sets the given decision as after keyword for the last record of the user
	# 	:param transaction: current transaction
	# 	:param user: current user
	# 	:param keyword_after_decission: decision done by the user
	# 	:return: None
	# 	"""
	# 	logger('QueryHelper', 'update_last_record_in_breadcrumbs', 'user ' + str(user))
	#
	# 	db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
	# 	if not db_user:
	# 		logger('QueryHelper', 'update_last_record_in_breadcrumbs', 'no user')
	# 		return
	#
	# 	# get last record
	# 	db_history = DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid)).order_by(History.uid.desc()).all()
	#
	# 	logger('QueryHelper', 'update_last_record_in_breadcrumbs', 'len db_history: ' + str(len(db_history)) if db_history else 'null')
	# 	# do we have more than the start statement?
	# 	if len(db_history) > 1:
	# 		db_history[1].set_keyword_after_decission(keyword_after_decission)
	#
	# 	transaction.commit()

	def del_breadcrumbs_of_user(self, transaction, user):
		"""
		Deletes the complete breadcrumbs of given user
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		# maybe we are anonymous
		if user:
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			logger('BreadcrumbHelper', 'del_breadcrumbs_of_user','user ' + str(db_user.uid))
			DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).delete()
			transaction.commit()