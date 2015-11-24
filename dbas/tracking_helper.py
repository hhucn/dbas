import collections
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Relation, Track, Issue, \
	History
from .logger import logger
from .strings import Translator
from .query_helper import QueryHelper

class TrackingHelper(object):

	# def __init__ (self):
	# 	self.char_threshold = 30

	def save_track_for_user(self, transaction, user, statement_id, premisesgroup_uid, argument_uid, attacked_by_relation, attacked_with_relation, session_id):
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param statement_id: id of the clicked statement
		:param premisesgroup_uid: id of the clicked premiseGroup
		:param argument_uid:
		:param attacked_by_relation: id of attacked by relation
		:param attacked_with_relation: id of attacked_w th relation
		:return: undefined
		"""
		if user is None:
			user = 'anonymous'

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid) +
														', statememt_id ' + str(statement_id) +
														', premisesgroup_uid ' + str(premisesgroup_uid) +
														', argument_uid ' + str(argument_uid) +
														', attacked_by_relation ' + str(attacked_by_relation) +
														', attacked_with_relation ' + str(attacked_with_relation) +
		                                                ', session_id ' + str(session_id))
		DBDiscussionSession.add(Track(user=db_user.uid, statement=statement_id, premisegroup=premisesgroup_uid, argument = argument_uid,
		                    attacked_by=attacked_by_relation, attacked_with=attacked_with_relation, session_id=session_id))
		transaction.commit()

	def get_track_of_user(self, user, lang):
		"""
		Returns the complete track of given user
		:param user: current user id
		:return: track os the user id as dict
		"""
		logger('QueryHelper', 'get_track_of_user', 'user ' + user)
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			logger('QueryHelper', 'get_track_of_user', 'no user')
			return dict()

		db_tracks = DBDiscussionSession.query(Track).filter_by(author_uid=db_user.uid).all()
		qh = QueryHelper()

		if not db_tracks:
			logger('QueryHelper', 'get_track_of_user', 'no track')
			return dict()

		return_dict = collections.OrderedDict()

		db_issues = DBDiscussionSession.query(Issue).all()

		for issue in db_issues:
			issue_dict = collections.OrderedDict()
			for index, track in enumerate(db_tracks):
				logger('QueryHelper','get_track_of_user','track uid ' + str(track.uid))

				track_dict = dict()

				# get attacks
				attacked_by_relation = DBDiscussionSession.query(Relation).filter_by(uid=track.attacked_by_relation).first()
				attacked_with_relation = DBDiscussionSession.query(Relation).filter_by(uid=track.attacked_with_relation).first()
				attacked_by_relation_id = qh.get_relation_uid_by_name(attacked_by_relation.name) if attacked_by_relation else 'None'
				attacked_with_relation_id = qh.get_relation_uid_by_name(attacked_with_relation.name) if attacked_with_relation else 'None'

				# get text
				attacked_by_relation_str = attacked_by_relation.name if attacked_by_relation else '-'
				attacked_with_relation_str = attacked_with_relation.name if attacked_with_relation else '-'
				track_statement = '-' if track.statement_uid == 0 else qh.get_text_for_statement_uid(track.statement_uid, issue.uid)
				track_argument = '-' if track.argument_uid == 0 else qh.get_text_for_argument_uid(track.argument_uid, issue.uid, lang)
				if track_argument:
					track_argument = track_argument[1:-1]

					if track.premisesGroup_uid == 0:
						track_premisesGroup = '-'
					else:
						track_premisesGroup,tash = qh.get_text_for_premisesGroup_uid(track.premisesGroup_uid, issue.uid)

					if track_statement:

						# text
						track_dict['statement']                  = track_statement
						track_dict['premisesGroup']             = track_premisesGroup
						track_dict['argument']                   = track_argument
						track_dict['attacked_by_relation']       = attacked_by_relation_str
						track_dict['attacked_with_relation']     = attacked_with_relation_str

						# ids
						track_dict['uid']                        = str(track.uid)
						track_dict['statement_uid']              = str(track.statement_uid)
						track_dict['premisesGroup_uid']         = str(track.premisesGroup_uid)
						track_dict['argument_uid']               = str(track.argument_uid)
						track_dict['attacked_by_relation_uid']   = attacked_by_relation_id
						track_dict['attacked_with_relation_uid'] = attacked_with_relation_id
						track_dict['timestamp']                  = str(track.timestamp)

						if not attacked_by_relation_str == '-':
							track_dict['text'] = 'Others say: \'' + track_argument + \
							                     '\' <i>' + attacked_by_relation_str + 's</i> \'' + \
							                     track_premisesGroup + '\''
						if not attacked_with_relation_str == '-':
							if track_premisesGroup == '-':
								track_dict['text'] = 'You will <i>' + attacked_with_relation_str + '</i> \'' + \
							                         track_argument + '\''
							else:
								track_dict['text'] = 'You say: \'' + track_premisesGroup + \
							                         '\' <i>' + attacked_with_relation_str + 's</i> \'' + \
							                         track_argument + '\''

						issue_dict[str(index)] = track_dict
			issue_dict['uid'] = str(issue.uid)
			issue_dict['text'] = str(issue.text)
			issue_dict['date'] = str(issue.date)
			return_dict[str(issue.uid)] = issue_dict

		return return_dict

	def del_track_of_user(self, transaction, user):
		"""
		Deletes the complete track of given user
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'del_track_of_user','user ' + str(db_user.uid))
		DBDiscussionSession.query(Track).filter_by(author_uid=db_user.uid).delete()
		transaction.commit()

	def save_history_for_user_with_statement_uid(self, transaction, user, url, statement_uid, session_id):
		"""
		Saves history for user with statement_uid as keyword. Calls save_history_for_user(self, transaction, user, url, keyword, session_id)
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param statement_uid: uid of the statement
		:param session_id: current session id
		:return: undefined
		"""
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid)).first()
		db_textversion  = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textvalues.textVersion_uid).join(User).first()
		text = db_textversion.content
		# if len(text) > self.char_threshold:
		# 	text = text[0:self.char_threshold] + '...'
		self.save_history_for_user(transaction, user, url, text, session_id)

	def save_history_for_user_with_argument_parts(self, transaction, user, url, premisegroups_uid, conclusion_uid, issue, session_id, lang):
		"""
		Saves history for user with statement_uid as keyword. Calls save_history_for_user(self, transaction, user, url, keyword, session_id)
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param premisegroups_uid: uid of the premisegroup
		:param conclusion_uid: uid of the conclusion
		:param issue: uid of the issue
		:param session_id: current session id
		:param lang: current language
		:return: undefined
		"""
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==conclusion_uid)).first()
		db_textversion  = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textvalues.textVersion_uid).join(User).first()
		text1, tmp = QueryHelper().get_text_for_premisesGroup_uid(premisegroups_uid, issue)
		text2 = db_textversion.content.lower()
		# if len(text1) > self.char_threshold:
		# 	text1 = text1[0:self.char_threshold] + '...'
		# if len(text2) > self.char_threshold:
		# 	text2 = text2[0:self.char_threshold] + '...'
		self.save_history_for_user(transaction, user, url, text1 + ', ' + Translator(lang).get('because') + ' ' + text2,
		                           session_id)

	def save_history_for_user_with_premissegroups_uid(self, transaction, user, url, premisegroup_uid1, premisegroup_uid2, issue,
	                                                 session_id):
		"""
		Saves history for user with statement_uid as keyword. Calls save_history_for_user(self, transaction, user, url, keyword, session_id)
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param premisegroup_uid1: uid of the premisegroup1
		:param premisegroup_uid2: uid of the premisegroup2
		:param issue: uid of the issue
		:param session_id: current session id
		:return: undefined
		"""
		text1, tmp = QueryHelper().get_text_for_premisesGroup_uid(premisegroup_uid1, issue)
		text2, tmp = QueryHelper().get_text_for_premisesGroup_uid(premisegroup_uid2, issue)
		# if len(text1) > self.char_threshold:
		# 	text1 = text1[0:self.char_threshold] + '...'
		# if len(text2) > self.char_threshold:
		# 	text2 = text2[0:self.char_threshold] + '...'
		self.save_history_for_user(transaction, user, url, text1 + ' vs. ' + text2, session_id)

	def save_history_for_user_with_premissegroup_of_arguments_uid(self, transaction, user, url, argument_uid, issue, session_id):
		"""
		Saves history for user with statement_uid as keyword. Calls save_history_for_user(self, transaction, user, url, keyword, session_id)
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param argument_uid: uid of the argument
		:param issue: uid of the issue
		:param session_id: current session id
		:return: undefined
		"""
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==int(argument_uid), Argument.issue_uid==issue)).first()
		text, tmp = QueryHelper().get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid, issue)
		self.save_history_for_user(transaction, user, url, text, session_id)

	def save_history_for_user_with_action(self, transaction, user, url, statement_uid, supportive, session_id, lang):
		"""
		Saves history for user with statement_uid as keyword. Calls save_history_for_user(self, transaction, user, url, keyword, session_id)
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param statement_uid: uid of the statement
		:param supportive: uid of the statement
		:param session_id: current session id
		:param lang: current language
		:return: undefined
		"""
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid)).first()
		db_textversion  = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textvalues.textVersion_uid).join(User).first()
		_t = Translator(lang)
		attribute = _t.get('support') if supportive else _t.get('attack')
		text = db_textversion.content
		# if len(text) > self.char_threshold:
		# 	text = text[0:self.char_threshold] + '...'
		self.save_history_for_user(transaction, user, url, attribute + ' ' + text, session_id)


	def save_history_for_user_with_lang(self, transaction, user, url, keyword, session_id, lang):
		"""
		Saves history for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param keyword: specific additional information
		:param session_id: current session id
		:param lang: current language
		:return: undefined
		"""
		self.save_history_for_user(transaction, user, url, Translator(lang).get(keyword), session_id)


	def save_history_for_user(self, transaction, user, url, keyword, session_id):
		"""
		Saves history for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param url: current url
		:param keyword: specific additional information
		:param session_id: current session id
		:return: undefined
		"""
		if user is None:
			user = 'anonymous'

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_history_for_user', 'user: ' + user +
		                                                ', db_user: ' + str(db_user.uid) +
														', url ' + str(url) +
														', keyword ' + str(keyword) +
		                                                ', session_id ' + str(session_id))

		# check for duplicates
		db_history = DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid, History.url==url)).order_by(History.uid.desc()).first()
		if db_history:
			db_history = DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid, History.uid>db_history.uid)).all()
			for history in db_history:
				DBDiscussionSession.query(History).filter_by(uid=history.uid).delete()
		else:
			DBDiscussionSession.add(History(user=db_user.uid, url=url, keyword=keyword, session_id=session_id))
		transaction.commit()

	def get_history_of_user(self, user):
		"""
		Returns the complete track of given user
		:param user: current user id
		:return: track os the user id as dict
		"""
		logger('QueryHelper', 'get_history_of_user', 'user ' + str(user))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			logger('QueryHelper', 'get_history_of_user', 'no user')
			return dict()

		db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()

		if not db_history:
			logger('QueryHelper', 'get_history_of_user', 'no track')
			return dict()

		return_dict = collections.OrderedDict()

		for index, history in enumerate(db_history):
			hist = dict()
			hist['uid']         = str(history.uid)
			hist['author_uid']  = str(history.author_uid)
			hist['url']         = str(history.url)
			hist['keyword']     = str(history.keyword)
			hist['timestamp']   = str(history.timestamp)
			return_dict[str(index+1)] = hist

		return return_dict