"""
Provides helping function for getting some opinions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import re
from sqlalchemy import and_
import dbas.user_management as UserHandler

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, VoteArgument, VoteStatement, Premise
from dbas.helper.relation_helper import RelationHelper
from dbas.lib import sql_timestamp_pretty_print, get_text_for_statement_uid, get_text_for_argument_uid,\
	get_text_for_premisesgroup_uid, get_text_for_conclusion
from dbas.logger import logger
from dbas.strings import Translator, TextGenerator


class OpinionHandler:
	"""
	Provides function for getting users with the same opinons as the user
	"""
	
	def __init__(self, lang, nickname, mainpage):
		"""
		
		:param self.lang: ui_locales ui_locales
		:param self.nickname: self.nickname
		:param self.mainpage: URL
		:return: 
		"""
		self.lang = lang
		self.nickname = nickname
		self.mainpage = mainpage

	def get_user_and_opinions_for_argument(self, argument_uids):
		"""
		Returns nested dictionary with all kinds of attacks for the argument as well as the users who are supporting
		these attacks.

		:param argument_uids: Argument.uid
		:return: { 'attack_type': { 'message': 'string', 'users': [{'self.nickname': 'string', 'avatar_url': 'url' 'vote_timestamp': 'string' ], ... }],...}
		"""

		logger('OpinionHandler', 'get_user_with_same_opinion_for_argument', 'Arguments ' + str(argument_uids))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		# preperation
		ret_dict = dict()
		all_users = []
		regex = re.compile('</?(strong|em)>')  # replacing html tags
		_t = Translator(self.lang)
		_tg = TextGenerator(self.lang)
		db_user_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[0]).first()
		db_syst_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uids[1]).first()

		# sanity check
		if not db_user_argument or not db_syst_argument:
			ret_dict['message'] = _t.get(_t.internalError) + '.'
			ret_dict['users'] = all_users
			return {'opinions': ret_dict, 'title': _t.get(_t.internalError)}

		title = _t.get(_t.reactionFor) + ': ' + get_text_for_argument_uid(argument_uids[0], self.lang)

		# getting uids of all reactions
		_rh = RelationHelper(argument_uids[0], self.lang)
		undermines_uids  = _rh.get_undermines_for_argument_uid()
		supports_uids    = _rh.get_supports_for_argument_uid()
		undercuts_uids   = _rh.get_undercuts_for_argument_uid()
		rebuts_uids      = _rh.get_rebuts_for_argument_uid()

		tmp_dict = {
			'undermine': undermines_uids,
			'support': supports_uids,
			'undercut': undercuts_uids,
			'rebut': rebuts_uids
		}

		# getting the text of all reactions
		conclusion      = get_text_for_conclusion(db_syst_argument, self.lang)
		premise, tmp    = get_text_for_premisesgroup_uid(db_syst_argument.premisesgroup_uid, self.lang)
		db_tmp_argument = db_syst_argument
		while db_tmp_argument.argument_uid and not db_tmp_argument.conclusion_uid:
			db_tmp_argument = DBDiscussionSession.query(Argument).filter_by(uid=db_tmp_argument.argument_uid).first()
		first_conclusion = get_text_for_statement_uid(db_tmp_argument.conclusion_uid)
		first_conclusion = first_conclusion[0:1].lower() + first_conclusion[1:]
		conclusion	     = conclusion[0:1].lower() + conclusion[1:]
		premise		     = premise[0:1].lower() + premise[1:]
		relation_text    = _tg.get_relation_text_dict(premise, conclusion, False, True, db_user_argument.is_supportive,
		                                              first_conclusion=first_conclusion)

		# getting votes for every reaction
		for relation in tmp_dict:
			relation_dict   = dict()
			all_users       = []
			message         = ''

			for uid in tmp_dict[relation]:
				db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == uid['id'],
				                                                               VoteArgument.is_up_vote == True,
				                                                               VoteArgument.is_valid == True,
				                                                               VoteArgument.author_uid != db_user_uid)).all()
				for vote in db_votes:
					voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
					users_dict = self.create_users_dict(voted_user, vote.timestamp)
					all_users.append(users_dict)
				relation_dict['users'] = all_users

				if len(db_votes) == 0:
					message = _t.get(_t.voteCountTextMayBeFirst) + '.'
				elif len(db_votes) == 1:
					message = _t.get(_t.voteCountTextOneOther) + '.'
				else:
					message = str(len(db_votes)) + ' ' + _t.get(_t.voteCountTextMore) + '.'

			ret_dict[relation] = {'users': all_users, 'message': message, 'text': regex.sub('', relation_text[relation + '_text'].replace('<strong>', ''))}

		return {'opinions': ret_dict, 'title': title[0:1].upper() + title[1:]}

	def get_user_with_same_opinion_for_statements(self, statement_uids, is_supportive):
		"""
		Returns nested dictionary with all kinds of information about the votes of the statements.

		:param statement_uids: Statement.uid
		:param is_supportive: Boolean
		:return: {'users':[{self.nickname1.avatar_url, self.nickname1.vote_timestamp}*]}
		"""
		logger('OpinionHandler', 'get_user_with_same_opinion_for_statements', 'Statement ' + str(statement_uids))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		opinions = []
		_t = Translator(self.lang)
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
			text = get_text_for_statement_uid(uid)
			statement_dict['text'] = text[0:1].upper() + text[1:]

			logger('--', str(is_supportive), str(str(is_supportive) == 'True'))
			logger('--', str(is_supportive), str(str(is_supportive) == 'True'))
			logger('--', str(is_supportive), str(str(is_supportive) == 'True'))
			if is_supportive is not None:
				is_supportive = True if str(is_supportive) == 'True' else False
			else:
				is_supportive = False

			db_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == uid,
		                                                                    VoteStatement.is_up_vote == is_supportive,
		                                                                    VoteStatement.is_valid == True,
		                                                                    VoteStatement.author_uid != db_user_uid)).all()

			for vote in db_votes:
				voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
				users_dict = self.create_users_dict(voted_user, vote.timestamp)
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

	def get_user_with_same_opinion_for_premisegroups(self, argument_uids):
		"""
		Returns nested dictionary with all kinds of information about the votes of the premisegroups.

		:param argument_uids: Argument.uid
		:return: {'users':[{self.nickname1.avatar_url, self.nickname1.vote_timestamp}*]}
		"""
		logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'Arguments ' + str(argument_uids))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		opinions = []
		_t = Translator(self.lang)
		title = _t.get(_t.informationForStatements)

		for uid in argument_uids:
			logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'argument ' + str(uid))
			statement_dict = dict()
			all_users = []
			db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
			if not db_premises:
				statement_dict['uid']       = None
				statement_dict['text']      = None
				statement_dict['message']   = None
				statement_dict['users']     = None

			statement_dict['uid'] = str(uid)
			text, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
			statement_dict['text'] = text[0:1].upper() + text[1:]

			db_votes = []
			for premise in db_premises:
				logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'group ' + str(uid) +
				       ' premises statement ' + str(premise.statement_uid))
				db_votes += DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == premise.statement_uid,
				                                                                 VoteStatement.is_up_vote == True,
				                                                                 VoteStatement.is_valid == True,
				                                                                 VoteStatement.author_uid != db_user_uid)).all()

			for vote in db_votes:
				voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
				users_dict = self.create_users_dict(voted_user, vote.timestamp)
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

	def get_user_with_same_opinion_for_argument(self, argument_uid):
		"""
		Returns nested dictionary with all kinds of information about the votes of the argument.

		:param argument_uid: Argument.uid
		:return: {'users':[{self.nickname1.avatar_url, self.nickname1.vote_timestamp}*]}
		"""
		logger('OpinionHandler', 'get_user_with_same_opinion_for_argument', 'Argument ' + str(argument_uid) + ' ' + get_text_for_argument_uid(argument_uid, 'de'))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		opinions = dict()
		all_users = []
		_t = Translator(self.lang)
		text = get_text_for_argument_uid(argument_uid, self.lang)
		title = _t.get(_t.reactionFor) + ': ' + text[0:1].upper() + text[1:]

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			opinions['uid']       = None
			opinions['text']      = None
			opinions['message']   = None
			opinions['users']     = None

		opinions['uid'] = str(argument_uid)
		text = get_text_for_argument_uid(argument_uid, self.lang)
		opinions['text'] = text[0:1].upper() + text[1:]

		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
		                                                               VoteArgument.is_up_vote == True,
		                                                               VoteArgument.is_valid == True,
		                                                               VoteArgument.author_uid != db_user_uid)).all()

		for vote in db_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict = self.create_users_dict(voted_user, vote.timestamp)
			all_users.append(users_dict)
		opinions['users'] = all_users

		if len(db_votes) == 0:
			opinions['message'] = _t.get(_t.voteCountTextMayBeFirst) + '.'
		elif len(db_votes) == 1:
			opinions['message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			opinions['message'] = str(len(db_votes)) + ' ' + _t.get(_t.voteCountTextMore) + '.'

		return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}

	def get_user_with_opinions_for_attitude(self, statement_uid):
		"""
		Returns dictionary with agree- and disagree-votes

		:param statement_uid: Statement.uid
		:return:
		"""
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		_t = Translator(self.lang)
		text = get_text_for_statement_uid(statement_uid)
		title = _t.get(_t.attitudeFor) + ': ' + text[0:1].upper() + text[1:]
		ret_dict = dict()

		if not db_statement:
			ret_dict['text'] = None
			ret_dict['agree'] = None
			ret_dict['disagree'] = None
			ret_dict['agree_users'] = []
			ret_dict['disagree_users'] = []
			ret_dict['title'] = title[0:1].upper() + title[1:]

		text = get_text_for_statement_uid(statement_uid)
		ret_dict['text'] = text[0:1].upper() + text[1:]
		ret_dict['agree'] = None
		ret_dict['disagree'] = None

		db_user = DBDiscussionSession.query(User).filter_by(nickname=self.nickname).first()
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
			users_dict = self.create_users_dict(voted_user, vote.timestamp)
			pro_array.append(users_dict)
		ret_dict['agree_users'] = pro_array
		ret_dict['agree_text'] = _t.get(_t.iAgreeWith)

		con_array = []
		for vote in db_con_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict = self.create_users_dict(voted_user, vote.timestamp)
			con_array.append(users_dict)
		ret_dict['disagree_users'] = con_array
		ret_dict['disagree_text'] = _t.get(_t.iDisagreeWith)

		ret_dict['title'] = title[0:1].upper() + title[1:]

		return ret_dict

	def create_users_dict(self, db_user, timestamp):
		"""
		Creates dictionary with self.nickname, url and timestamp

		:param db_user: User
		:param timestamp: SQL Timestamp
		:param self.lang: ui_locales
		:param self.mainpage: Url
		:return: dict()
		"""
		return {'nickname': db_user.public_nickname,
		        'public_profile_url': self.mainpage + '/user/' + db_user.public_nickname,
		        'avatar_url': UserHandler.get_public_profile_picture(db_user),
		        'vote_timestamp': sql_timestamp_pretty_print(timestamp, self.lang)}
