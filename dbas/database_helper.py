import random
import datetime

from sqlalchemy import and_, not_

from .database import DBDiscussionSession, DBNewsSession
from .database.discussion_model import Argument, Statement, User, Group, TextValue, TextVersion, Premisse,  Track, Relation
from .database.news_model import News
from .dictionary_helper import DictionaryHelper
from .query_helper import QueryHelper
from .user_management import UserHandler
from .logger import logger

# TODO: PEP 8

class DatabaseHelper(object):

	def get_news(self):
		"""

		:return:
		"""
		logger('DatabaseHelper', 'get_news', 'main')
		db_news = DBNewsSession.query(News).all()
		logger('DatabaseHelper', 'get_news', 'we have ' + str (len(db_news)) + ' news')
		ret_dict = dict()
		for news in db_news:
			news_dict = {}
			news_dict['title'] = news.title
			news_dict['author'] = news.author
			news_dict['date'] = news.date
			news_dict['news'] = news.news
			ret_dict[str(news.uid)] = news_dict

		return ret_dict

	def set_news(self, transaction, title, text, user):
		"""
		Sets a new news into the news table
		:param title: news title
		:param text: news text
		:param user: self.request.authenticated_userid
		:return: dictionary {title,date,author,news}
		"""
		logger('DatabaseHelper', 'set_news', 'def')
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		author = db_user.firstname if db_user.firstname == "admin" else db_user.firstname + " " + db_user.surname
		now = datetime.datetime.now()
		day = str(now.day) if now.day > 9 else ("0" + str(now.day))
		month = str(now.month) if now.month > 9 else ("0" + str(now.month))
		date = day + '.' + month + '.' + str(now.year)
		news = News(title = title, author = author, date = date, news = text)

		DBNewsSession.add(news)
		DBNewsSession.flush()

		db_news = DBNewsSession.query(News).filter_by(title=title).first()
		return_dict = dict()

		if db_news:
			logger('DatabaseHelper', 'set_news', 'new news is in db')
			return_dict['status'] = '1'
		else:

			logger('DatabaseHelper', 'set_news', 'new news is not in db')
			return_dict['status'] = '-'

		transaction.commit()

		return_dict['title'] = title
		return_dict['date'] = date
		return_dict['author'] = author
		return_dict['news'] = text

		return return_dict

	def correct_statement(self, transaction, user, uid, corrected_text):
		"""
		Corrects a statement
		:param transaction: current transaction
		:param user: requesting user
		:param uid: requested statement uid
		:param corrected_text: new text
		:return: True
		"""
		logger('DatabaseHelper', 'correct_statement', 'def')

		return_dict = dict()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).join(TextValue).first()
		db_textvalue = DBDiscussionSession.query(TextValue).filter_by(uid=db_statement.text_uid)\
			.join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()
		if db_user:
			logger('DatabaseHelper', 'correct_statement', 'given user exists and correction will be set')
			textversion = TextVersion(content=corrected_text, author=db_user.uid, weight=db_textvalue.textversions.weight)
			textversion.set_textvalue(db_textvalue.uid)
			DBDiscussionSession.add(textversion)
			DBDiscussionSession.flush()
			db_textvalue.update_textversion(textversion.uid)
			transaction.commit()
			return_dict['status'] = '1'
		else:
			logger('DatabaseHelper', 'correct_statement', 'user not found')
			return_dict['status'] = '-1'

		return_dict['uid'] = uid
		return_dict['text'] = corrected_text
		return return_dict

	def get_all_users(self, user):
		"""
		Returns all users, if the given user is admin
		:param user: self.request.authenticated_userid
		:return: dictionary
		"""
		is_admin = UserHandler().is_user_admin(user)
		logger('DatabaseHelper', 'get_all_users', 'is_admin ' + str(is_admin))
		if not is_admin:
			return_dict = dict()
		else:
			logger('DatabaseHelper', 'get_all_users', 'get all users')
			db_users = DBDiscussionSession.query(User).join(Group).all()
			logger('DatabaseHelper', 'get_all_users', 'get all groups')

			return_dict = dict()

			if db_users:
				logger('DatabaseHelper', 'get_all_users', 'iterate all users')
				for user in db_users:
					return_user = dict()
					return_user['uid'] = user.uid
					return_user['firstname'] = user.firstname
					return_user['surname'] = user.surname
					return_user['nickname'] = user.nickname
					return_user['email'] = user.email
					return_user['group_uid'] = user.groups.name
					return_user['last_login'] = str(user.last_login)
					return_user['last_action'] = str(user.last_action)
					return_user['registered'] = str(user.registered)
					return_user['gender'] = str(user.gender)
					logger('DatabaseHelper', 'get_all_users ' + str(user.uid) + ' of ' + str(len(db_users)),
						"uid: " + str(user.uid)
						+ ", firstname: " + user.firstname
						+ ", surname: " + user.surname
						+ ", nickname: " + user.nickname
						+ ", email: " + user.email
						+ ", group_uid: " + user.groups.name
						+ ", last_action: " + str(user.last_action)
						+ ", last_logged: " + str(user.last_login)
						+ ", registered: " + str(user.registered)
						+ ", gender: " + str(user.gender)
					)
					return_dict[user.uid] = return_user
		return return_dict

	def get_attack_overview(self, user):
		"""

		:param user:
		:return:
		"""
		is_admin = UserHandler().is_user_admin(user)
		logger('DatabaseHelper', 'get_attack_overview', 'is_admin ' + str(is_admin))
		if not is_admin:
			return_dict = dict()
		else:
			return_dict = {}
			logger('DatabaseHelper', 'get_attack_overview', 'get all attacks for each argument')
			db_arguments = DBDiscussionSession.query(Argument).all()
			db_relations = DBDiscussionSession.query(Relation).all()

			relations_dict = {}
			for relation in db_relations:
				relations_dict[str(relation.uid)] = relation.name
			return_dict['attacks'] = relations_dict

			for argument in db_arguments:
				argument_dict = {}
				argument_dict['id'] = str(argument.uid)
				# try:
				argument_dict['text'] = QueryHelper().get_text_for_argument_uid(argument.uid) # TODO
				# except AttributeError:
				# 	argument_dict['text'] = str(argument.uid) # QueryHelper().get_text_for_argument_uid(argument.uid) # TODO

				for relation in db_relations:
					db_tracks = DBDiscussionSession.query(Track).filter(and_(Track.argument_uid==argument.uid,
					                                               Track.attacked_by_relation==relation.uid)).all()
					argument_dict[relation.name] = str(len(db_tracks)) if len(db_tracks) != 0 else '-'

				return_dict[str(argument.uid)] = argument_dict

		return return_dict

	def get_start_statements(self):
		"""
		Returns start statements
		:return: dictionary
		"""
		return_dict = dict()
		statements_dict = dict()
		db_statements = DBDiscussionSession.query(Statement).filter_by(isStartpoint=True).all()
		logger('DatabaseHelper', 'get_start_statements', 'get all statements')
		if db_statements:
			return_dict['status'] = '1'
			logger('DatabaseHelper', 'get_start_statements', 'there are start statements')
			for stat in db_statements:
				logger('DatabaseHelper', 'get_start_statements', 'stat ' + str(stat.uid) + ': ' + stat.textvalues.textversions.content)
				statements_dict[str(stat.uid)] = DictionaryHelper().save_statement_row_in_dictionary(stat)
		else:
			logger('DatabaseHelper', 'get_start_statements', 'there are no statements')
			return_dict['status'] = '-1'

		return_dict['statements'] = statements_dict
		return return_dict

	def get_premisses_for_statement(self, transaction, statement_uid, issupportive, user, session_id):
		"""

		:param transaction:
		:param statement_uid:
		:param issupportive:
		:param user:
		:param session_id:
		:return:
		"""

		QueryHelper().save_track_for_user(transaction, user, statement_uid, 0, 0, 0, 0, session_id)

		return_dict = dict()
		premisses_dict = dict()
		logger('DatabaseHelper', 'get_premisses_for_statement', 'get all premisses')
		db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==issupportive,
																Argument.conclusion_uid==statement_uid)).all()

		for argument in db_arguments:
			logger('DatabaseHelper', 'get_premisses_for_statement', 'argument ' 
					+ str(argument.uid) + ' (' + str(argument.premissesGroup_uid) + ')')
			db_premisses = DBDiscussionSession.query(Premisse).filter_by(premissesGroup_uid=argument.premissesGroup_uid).all()

			# check out the group
			premissesgroups_dict = dict()
			for premisse in db_premisses:
				logger('DatabaseHelper', 'get_premisses_for_statement', 'premisses group ' + str(premisse.premissesGroup_uid))
				db_statements = DBDiscussionSession.query(Statement).filter_by(uid=premisse.statement_uid).all()
				for statement in db_statements:
					logger('DatabaseHelper', 'get_premisses_for_statement', 'premisses group has statement ' + str(statement.uid))
					premissesgroups_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement)

				premisses_dict[str(premisse.premissesGroup_uid)] = premissesgroups_dict

		# premisses dict has for each group a new dictionary
		return_dict['premisses'] = premisses_dict
		return_dict['conclusion_id'] = statement_uid
		return_dict['status'] = '1'

		db_statements = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		return_dict['currentStatement'] = DictionaryHelper().save_statement_row_in_dictionary(db_statements)

		return return_dict

	def get_attack_for_premissegroup(self, transaction, user, last_premisses_group_uid, last_statement_uid, session_id):
		"""
		Based on the last given premissesgroup and statement, an attack will be choosen and replied.
		:param transaction: current transaction
		:param user: current nick of the user
		:param last_premisses_group_uid:
		:param last_statement_uid:
		:param session_id:
		:return: A random attack (undermine, rebut undercut) based on the last saved premissesgroup and statement as well as many texts
		like the premisse as text, conclusion as text, attack as text, confrontation as text. Everything is in a dict.
		"""
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'main with last_premisses_group_uid ' + str(last_premisses_group_uid))
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'last statement ' + str(last_statement_uid))

		return_dict = {}
		qh = QueryHelper()
		# get premisses and conclusion as text
		return_dict['premisse_text'], premisses_as_statements_uid = qh.get_text_for_premissesGroup_uid(last_premisses_group_uid)
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(last_statement_uid)

		# getting the argument of the premisses and conclusion
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'find argument with group ' + str(last_premisses_group_uid)
				+ ' conclusion statement ' + str(last_statement_uid))
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premissesGroup_uid==last_premisses_group_uid,
				Argument.conclusion_uid==last_statement_uid, Argument.isSupportive==True)).order_by(Argument.uid.desc()).first()

		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'argument uid ' + (str(db_argument.uid) if db_argument else 'none'))
		return_dict['argument_id'] = str(db_argument.uid) if db_argument else '0'

		# getting undermines or undercuts or rebuts
		attacks, key = qh.get_attack_for_argument_by_random(db_argument)
		return_dict['attack'] = key

		status = 1
		if int(attacks[key]) == 0:
			logger('DatabaseHelper', 'get_attack_for_premissegroup', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key])))
			logger('DatabaseHelper', 'get_attack_for_premissegroup', 'attack with ' + attacks[key + str(attack_no)])
			logger('DatabaseHelper', 'get_attack_for_premissegroup', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_id'] = attacks[key + str(attack_no) + 'id']

			# save the attack
			QueryHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                  qh.get_relation_uid_by_name(key), 0, session_id)

		return return_dict, status

	def get_attack_for_argument(self, transaction, user, id_text, pgroup_id, session_id):
		"""

		:param transaction:
		:param user:
		:param id_text:
		:param pgroup_id:
		:param session_id:
		:return:
		"""

		logger('DatabaseHelper', 'get_attack_for_argument', 'main')

		qh = QueryHelper()
		splitted_id = id_text.split('_')
		relation = splitted_id[0]
		premissesgroup_uid = splitted_id[2]

		logger('DatabaseHelper', 'get_attack_for_argument', 'relation: ' + relation + ', premissesgroup_uid: ' + premissesgroup_uid)

		# get last tracked conclusion
		db_last_conclusion = DBDiscussionSession.query(Premisse).filter_by(premissesGroup_uid=pgroup_id).first()

		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==db_last_conclusion.statement_uid,
		                                                    Argument.premissesGroup_uid==int(premissesgroup_uid),
		                                                    Argument.isSupportive==False)).first()
		return_dict = {}
		return_dict['premisse_text'], trash = qh.get_text_for_premissesGroup_uid(int(premissesgroup_uid))
		return_dict['premissesgroup_uid'] = premissesgroup_uid
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_last_conclusion.statement_uid)
		return_dict['argument_uid'] = db_argument.uid
		return_dict['premissegroup_uid'] = db_argument.premissesGroup_uid
		return_dict['relation'] = relation

		# getting undermines or undercuts or rebuts
		attacks, key = qh.get_attack_for_argument_by_random(db_argument)
		return_dict['attack'] = key

		status = 1
		if attacks == None or int(attacks[key]) == 0:
			logger('DatabaseHelper', 'get_attack_for_argument', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key])))
			logger('DatabaseHelper', 'get_attack_for_argument', 'attack with ' + attacks[key + str(attack_no)])
			logger('DatabaseHelper', 'get_attack_for_argument', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_id'] = attacks[key + str(attack_no) + 'id']

			# save the attack
			QueryHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                  qh.get_relation_uid_by_name(key), 0, session_id)

		return return_dict, status

	def get_reply_confrontations_response(self, transaction, uid_text, user, session_id):
		"""

		:param transaction:
		:param uid:
		:param user:
		:param session_id:
		:return:
		"""
		qh = QueryHelper()
		splitted_id = uid_text.split('_')
		relation = splitted_id[0]
		argument_uid = splitted_id[2]

		# get argument
		logger('DatabaseHelper', 'get_reply_confrontations_response', 'get reply confrontations for argument ' + argument_uid)
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=int(argument_uid)).first()

		# get attack
		key = 'reason'

		status = '1'
		if 'undermine' in relation.lower():
			return_dict = qh.get_undermines_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		elif 'support' in relation.lower():
			return_dict = qh.get_supports_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		elif 'undercut' in relation.lower():
			return_dict = qh.get_undercuts_for_argument_uid(key, argument_uid)
			type = 'statement'
		elif 'overbid' in relation.lower():
			return_dict = qh.get_overbids_for_argument_uid(key, argument_uid)
			type = 'statement'
		elif 'rebut' in relation.lower():
			#return_dict = qh.get_rebuts_for_argument_uid(key, argument_uid)
			return_dict = qh.get_supports_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		else:
			return_dict = {}
			type = 'none'
			status = '-1'

		logger('DatabaseHelper', 'get_reply_confrontations_response', 'attack (' + relation + ') was fetched for ' + str(argument_uid))

		# check return value
		if not return_dict:
			return_dict = {}
		if len(return_dict) == 0:
			return_dict[key] = '0'

		return_dict['premissegroup'], uids = qh.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid)
		# Todo: what is with an conclusion as premisse group?
		return_dict['relation'] = splitted_id[0]
		return_dict['argument_uid'] = argument_uid
		return_dict['premissegroup_uid'] = db_argument.premissesGroup_uid
		return_dict['type'] = type

		if db_argument.conclusion_uid is None or db_argument.conclusion_uid == 0:
			return_dict['conclusion_text'] = qh.get_text_for_argument_uid(db_argument.argument_uid)
			logger('DatabaseHelper', 'get_reply_confrontations_response', return_dict['conclusion_text'])
		else:
			return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_argument.conclusion_uid)

		QueryHelper().save_track_for_user(transaction, user, 0, 0, argument_uid, 0, qh.get_relation_uid_by_name(relation.lower()), session_id)

		return return_dict, status

	def get_logfile_for_statement(self, uid):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:return: dictionary with the logfile-rows
		"""
		logger('DatabaseHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(textValue_uid=db_statement.text_uid).join(User).all()

		return_dict = {}
		content_dict = {}
		# add all corrections
		for index, versions in enumerate(db_textversions):
			corr_dict = dict()
			corr_dict['uid'] = str(versions.uid)
			corr_dict['author'] = str(versions.users.nickname)
			corr_dict['date'] = str(versions.timestamp)
			corr_dict['text'] = str(versions.content)
			content_dict[str(index)] = corr_dict
			logger('DatabaseHelper', 'get_logfile_for_statement', 'statement ' + str(index) + ': ' + versions.content)
		return_dict['content'] = content_dict

		return return_dict

	def get_logfile_for_premissegroup(self, uid):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:return: dictionary with the logfile-rows
		"""
		logger('DatabaseHelper', 'get_logfile_for_premissegroup', 'def with uid: ' + str(uid))

		db_premisses = DBDiscussionSession.query(Premisse).filter_by(premissesGroup_uid=uid).first() # todo for premisse groups
		return self.get_logfile_for_statement(db_premisses.statement_uid)

	def set_statement(self, transaction, statement, user, is_start):
		"""
		Saves statement for user
		:param transaction: current transaction
		:param statement: given statement
		:param user: given user
		:param is_start: if it is a start statement
		:return: '1'
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'set_statement', 'user: ' + str(user) + 'user_id: ' + str(db_user.uid) + ', statement: ' + str(statement))

		# check for dot at the end
		if not statement.endswith("."):
			statement += "."
		if statement.lower().startswith('because '):
			statement = statement[8:]

		# check, if the statement already exists
		db_duplicate = DBDiscussionSession.query(TextVersion).filter_by(content=statement).first()

		# add the version
		textversion = db_duplicate if db_duplicate else TextVersion(content=statement, author=db_user.uid, weight=0)
		DBDiscussionSession.add(textversion)
		DBDiscussionSession.flush()

		# add a new cache
		textvalue = TextValue(textversion=textversion.uid)
		DBDiscussionSession.add(textvalue)
		DBDiscussionSession.flush()
		textversion.set_textvalue(textvalue.uid)

		# add the statement
		statement = Statement(text=textvalue.uid, isstartpoint=is_start)
		DBDiscussionSession.add(statement)
		DBDiscussionSession.flush()

		# get the new statement
		new_statement = DBDiscussionSession.query(Statement).filter_by(text_uid=textvalue.uid).order_by(Statement.uid.desc()).first()

		transaction.commit()

		return new_statement

	def set_premisses_for_tracked_argument(self, transaction, user, dict, key, conclusion_id, is_supportive):
		"""
		Inserts the given dictionarie with premisses for an statement or an argument
		:param transaction: current transaction for the database
		:param user_id: current users nickname
		:param dict: dictionary with all statements
		:param key: pro or con
		:param conclusion_id:
		:param is_supportive: for the argument
		:return: dict
		"""

		# user and last given statement is conclusion_id

		# insert the premisses as statements
		return_dict = {}
		qh = QueryHelper()

		logger('DatabaseHelper', 'set_premisses_for_tracked_argument', 'main')
		for index, entry in enumerate(dict):
			# first, save the premisse as statement
			new_statement = self.set_statement(transaction, dict[entry], user, False)

			# second, set the new statement as premisse
			new_premissegroup_uid = qh.set_statement_as_premisse(new_statement, user)
			logger('DatabaseHelper', 'set_premisses', dict[entry] + ' in new_premissegroup_uid ' + str(new_premissegroup_uid)
			       + ' to statement ' + str(conclusion_id) + ', supportive')

			# third, insert the argument
			qh.set_argument(transaction, user, new_premissegroup_uid, conclusion_id, 0, is_supportive)

			return_dict[key + '_' + str(index)] = DictionaryHelper().save_statement_row_in_dictionary(new_statement)

		transaction.commit()

		return return_dict