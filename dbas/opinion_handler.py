"""
Provides helping function for getting some opinions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, VoteArgument, VoteStatement, Premise
from dbas.helper.relation_helper import RelationHelper
from dbas.lib import sql_timestamp_pretty_print, get_text_for_statement_uid, get_text_for_argument_uid, get_text_for_premisesgroup_uid
from dbas.logger import logger
from dbas.strings import Translator
from dbas.user_management import UserHandler


class OpinionHandler:
	"""
	Provides function for getting users with the same opinons as the user
	"""

	@staticmethod
	def get_user_with_opinions_for_argument(argument_uid, lang, nickname, mainpage):
		"""
		Returns nested dictionary with all kinds of attacks for the argument as well as the users who are supporting
		these attacks.

		:param argument_uid: Argument.uid
		:param lang: ui_locales ui_locales
		:param nickname: nickname
		:param mainpage: URL
		:return: { 'attack_type': { 'message': 'string', 'users': [{'nickname': 'string', 'avatar_url': 'url' 'vote_timestamp': 'string' ], ... }],...}
		"""

		logger('OpinionHandler', 'get_user_with_same_opinion_for_argument', 'Argument ' + str(argument_uid))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		ret_dict = dict()
		all_users = []
		_t = Translator(lang)
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		title = _t.get(_t.reactionFor) + ': ' + get_text_for_argument_uid(argument_uid, lang)

		if not db_argument:
			ret_dict['message'] = _t.get(_t.internalError) + '.'
			ret_dict['users'] = all_users
			return {'opinions': ret_dict, 'title': title}

		_rh = RelationHelper(argument_uid, lang)
		undermines_uids  = _rh.get_undermines_for_argument_uid()
		supports_uids    = _rh.get_supports_for_argument_uid()
		undercuts_uids   = _rh.get_undercuts_for_argument_uid()
		rebuts_uids      = _rh.get_rebuts_for_argument_uid()

		tmp_dict = {
			'undermines': undermines_uids,
			'supports': supports_uids,
			'undercuts': undercuts_uids,
			'rebuts': rebuts_uids
		}

		for relation in tmp_dict:
			relation_dict = dict()
			all_users = []
			text = ''
			message = ''
			logger('--', '--', str(relation) + ' # ' + str(tmp_dict[relation]))
			for uid in tmp_dict[relation]:
				logger('--', '--', '-->' + str(uid['id']))
				db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == uid['id'],
				                                                               VoteArgument.is_up_vote == True,
				                                                               VoteArgument.is_valid == True,
				                                                               VoteArgument.author_uid != db_user_uid)).all()
				for vote in db_votes:
					voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
					users_dict = OpinionHandler.create_users_dict(voted_user, vote.timestamp, lang, mainpage)
					all_users.append(users_dict)
				relation_dict['users'] = all_users
				text = get_text_for_argument_uid(uid['id'], lang)

				if len(db_votes) == 0:
					message = _t.get(_t.voteCountTextMayBeFirst) + '.'
				elif len(db_votes) == 1:
					message = _t.get(_t.voteCountTextOneOther) + '.'
				else:
					message = str(len(db_votes)) + ' ' + _t.get(_t.voteCountTextMore) + '.'

			ret_dict[relation] = {'users': all_users, 'message': message, 'text': text}

		return {'opinions': ret_dict, 'title': title[0:1].upper() + title[1:]}

	@staticmethod
	def get_user_with_same_opinion_for_statements(statement_uids, lang, nickname, mainpage):
		"""
		Returns nested dictionary with all kinds of information about the votes of the statements.

		:param statement_uids: Statement.uid
		:param lang: ui_locales ui_locales
		:param nickname: User.nickname
		:param mainpage: URL
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('OpinionHandler', 'get_user_with_same_opinion_for_statement', 'Statement ' + str(statement_uids))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		opinions = []
		_t = Translator(lang)
		title = _t.get(_t.informationForStatements)

		for uid in statement_uids:
			statement_dict = dict()
			all_users = []
			db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
			if not db_statement:
				statement_dict['uid']       = None
				statement_dict['text']      = None
				statement_dict['message']   = None
				statement_dict['users']     = None

			statement_dict['uid'] = str(uid)
			statement_dict['text'] = get_text_for_statement_uid(uid)

			db_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == uid,
		                                                                    VoteStatement.is_up_vote == True,
		                                                                    VoteStatement.is_valid == True,
		                                                                    VoteStatement.author_uid != db_user_uid)).all()

			for vote in db_votes:
				voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
				users_dict = OpinionHandler.create_users_dict(voted_user, vote.timestamp, lang, mainpage)
				all_users.append(users_dict)
			statement_dict['users'] = all_users

			if len(db_votes) == 0:
				statement_dict['message'] = _t.get(_t.voteCountTextMayBeFirst) + '.'
			elif len(db_votes) == 1:
				statement_dict['message'] = _t.get(_t.voteCountTextOneOther) + '.'
			else:
				statement_dict['message'] = str(len(db_votes)) + ' ' + _t.get(_t.voteCountTextMore) + '.'

			opinions.append(statement_dict)

		return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

	@staticmethod
	def get_user_with_same_opinion_for_premisegroups(pgroup_uids, lang, nickname, mainpage):
		"""
		Returns nested dictionary with all kinds of information about the votes of the premisegroups.

		:param pgroup_uids: PremiseGroups.uid
		:param lang: ui_locales ui_locales
		:param nickname: User.nickname
		:param mainpage: URL
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'PGroups ' + str(pgroup_uids))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		opinions = []
		_t = Translator(lang)
		title = _t.get(_t.informationForStatements)

		for uid in pgroup_uids:
			statement_dict = dict()
			all_users = []
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=uid).all()
			if not db_premises:
				statement_dict['uid']       = None
				statement_dict['text']      = None
				statement_dict['message']   = None
				statement_dict['users']     = None

			statement_dict['uid'] = str(uid)
			statement_dict['text'], tmp = get_text_for_premisesgroup_uid(uid, lang)

			db_votes = []
			for premise in db_premises:
				db_votes += DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == premise.statement_uid,
				                                                                 VoteStatement.is_up_vote == True,
				                                                                 VoteStatement.is_valid == True,
				                                                                 VoteStatement.author_uid != db_user_uid)).all()

			for vote in db_votes:
				voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
				users_dict = OpinionHandler.create_users_dict(voted_user, vote.timestamp, lang, mainpage)
				all_users.append(users_dict)
			statement_dict['users'] = all_users

			if len(db_votes) == 0:
				statement_dict['message'] = _t.get(_t.voteCountTextMayBeFirst) + '.'
			elif len(db_votes) == 1:
				statement_dict['message'] = _t.get(_t.voteCountTextOneOther) + '.'
			else:
				statement_dict['message'] = str(len(db_votes)) + ' ' + _t.get(_t.voteCountTextMore) + '.'

			opinions.append(statement_dict)

		return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

	@staticmethod
	def get_user_with_same_opinion_for_argument(argument_uid, lang, nickname, mainpage):
		"""
		Returns nested dictionary with all kinds of information about the votes of the argument.

		:param argument_uid: Argument.uid
		:param lang: ui_locales ui_locales
		:param nickname: User.nickname
		:param mainpage: URL
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('OpinionHandler', 'get_user_with_same_opinion_for_argument', 'Argument ' + str(argument_uid))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		opinions = dict()
		all_users = []
		_t = Translator(lang)
		text = get_text_for_argument_uid(argument_uid, lang)
		title = _t.get(_t.reactionFor) + ': ' + text[0:1].upper() + text[1:]

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			opinions['uid']       = None
			opinions['text']      = None
			opinions['message']   = None
			opinions['users']     = None

		opinions['uid'] = str(argument_uid)
		opinions['text'] = get_text_for_argument_uid(argument_uid, lang)

		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
		                                                               VoteArgument.is_up_vote == True,
		                                                               VoteArgument.is_valid == True,
		                                                               VoteArgument.author_uid != db_user_uid)).all()

		for vote in db_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict = OpinionHandler.create_users_dict(voted_user, vote.timestamp, lang, mainpage)
			all_users.append(users_dict)
		opinions['users'] = all_users

		if len(db_votes) == 0:
			opinions['message'] = _t.get(_t.voteCountTextMayBeFirst) + '.'
		elif len(db_votes) == 1:
			opinions['message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			opinions['message'] = str(len(db_votes)) + ' ' + _t.get(_t.voteCountTextMore) + '.'

		return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

	@staticmethod
	def get_user_with_opinions_for_attitude(statement_uid, lang, nickname, mainpage):
		"""
		Returns dictionary with agree- and disagree-votes

		:param statement_uid: Statement.uid
		:param lang: ui_locales ui_locales
		:param nickname: User.nickname
		:param mainpage: URL
		:return:
		"""
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		_t = Translator(lang)
		text = get_text_for_statement_uid(statement_uid)
		title = _t.get(_t.attitudeFor) + ': ' + text[0:1].upper() + text[1:]
		ret_dict = dict()

		if not db_statement:
			ret_dict['text'] = None
			ret_dict['agree'] = None
			ret_dict['disagree'] = None

		ret_dict['text'] = get_text_for_statement_uid(statement_uid)
		ret_dict['agree'] = None
		ret_dict['disagree'] = None

		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		db_pro_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement_uid,
		                                                                    VoteStatement.is_up_vote == True,
		                                                                    VoteStatement.is_valid == True,
		                                                                    VoteStatement.author_uid != db_user_uid)).all()

		db_con_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement_uid,
		                                                                    VoteStatement.is_up_vote == False,
		                                                                    VoteStatement.is_valid == True,
		                                                                    VoteStatement.author_uid != db_user_uid)).all()
		pro_array = []
		for vote in db_pro_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict = OpinionHandler.create_users_dict(voted_user, vote.timestamp, lang, mainpage)
			pro_array.append(users_dict)
		ret_dict['agree_users'] = pro_array

		con_array = []
		for vote in db_con_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict = OpinionHandler.create_users_dict(voted_user, vote.timestamp, lang, mainpage)
			con_array.append(users_dict)
		ret_dict['disagree_users'] = con_array

		ret_dict['title'] = title[0:1].upper() + title[1:]

		return ret_dict

	@staticmethod
	def create_users_dict(db_user, timestamp, lang, mainpage):
		"""
		Creates dictionary with nickname, url and timestamp

		:param db_user: User
		:param timestamp: SQL Timestamp
		:param lang: ui_locales
		:param mainpage: Url
		:return: dict()
		"""
		return {'nickname': db_user.public_nickname,
		        'public_profile_url': mainpage + '/user/' + db_user.public_nickname,
		        'avatar_url': UserHandler.get_public_profile_picture(db_user),
		        'vote_timestamp': sql_timestamp_pretty_print(str(timestamp), lang)}
