import random
from sqlalchemy import and_, not_

from .database import DBSession
from .database.model import Argument, Statement, Track, User, Group, TextValue, TextVersion, Premisse, PremisseGroup
from .dictionary_helper import DictionaryHelper
from .query_helper import QueryHelper
from .user_management import UserHandler
from .logger import logger

# TODO: PEP 8

class DatabaseHelper(object):

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
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		db_statement = DBSession.query(Statement).filter_by(uid=uid).join(TextValue).first()
		db_textvalue = DBSession.query(TextValue).filter_by(uid=db_statement.text_uid)\
			.join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()
		if db_user:
			logger('DatabaseHelper', 'correct_statement', 'given user exists and correction will be set')
			textversion = TextVersion(content=corrected_text, author=db_user.uid, weight=db_textvalue.textversions.weight)
			textversion.set_textvalue(db_textvalue.uid)
			DBSession.add(textversion)
			DBSession.flush()
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
			db_users = DBSession.query(User).join(Group).all()
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

	def get_start_statements(self):
		"""
		Returns start statements
		:return: dictionary
		"""
		return_dict = dict()
		statements_dict = dict()
		db_statements = DBSession.query(Statement).filter_by(isStartpoint=True).all()
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

	def get_premisses_for_statement(self, transaction, statement_uid, issupportive, user):
		"""

		:param transaction:
		:param statement_uid:
		:param issupportive:
		:param user:
		:return:
		"""

		QueryHelper().save_track_for_user(transaction, user, statement_uid, 0, 0, 0, 0)

		return_dict = dict()
		premisses_dict = dict()
		logger('DatabaseHelper', 'get_premisses_for_statement', 'get all premisses')
		db_arguments = DBSession.query(Argument).filter(and_(Argument.isSupportive==issupportive,
																Argument.conclusion_uid==statement_uid)).all()

		for argument in db_arguments:
			logger('DatabaseHelper', 'get_premisses_for_statement', 'argument ' 
					+ str(argument.uid) + ' (' + str(argument.premissesGroup_uid) + ')')
			db_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid=argument.premissesGroup_uid).all()

			# check out the group
			premissesgroups_dict = dict()
			for premisse in db_premisses:
				logger('DatabaseHelper', 'get_premisses_for_statement', 'premisses group ' + str(premisse.premissesGroup_uid))
				db_statements = DBSession.query(Statement).filter_by(uid=premisse.statement_uid).all()
				for statement in db_statements:
					logger('DatabaseHelper', 'get_premisses_for_statement', 'premisses group has statement ' + str(statement.uid))
					premissesgroups_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement)

				premisses_dict[str(premisse.premissesGroup_uid)] = premissesgroups_dict

		# premisses dict has for each group a new dictionary
		return_dict['premisses'] = premisses_dict
		return_dict['status'] = '1'

		db_statements = DBSession.query(Statement).filter_by(uid=statement_uid).first()
		return_dict['currentStatementText'] = DictionaryHelper().save_statement_row_in_dictionary(db_statements)

		return return_dict

	def get_attack_for_premissegroup(self, transaction, user, last_premisses_group_uid):
		"""
		Based on the last given premissesgroup and statement, an attack will be choosen and replied.
		:param transaction: current transaction
		:param user: current nick of the user
		:param last_premisses_group_uid:
		:return: A random attack (undermine, rebut undercut) based on the last saved premissesgroup and statement as well as many texts
		like the premisse as text, conclusion as text, attack as text, confrontation as text. Everything is in a dict.
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'main')

		# get last statement out of the history
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'last statement with user ' + str(db_user.uid) + ', and statement not zero')
		db_track_last_statement = DBSession.query(Track).filter(and_(Track.author_uid==db_user.uid, not_(Track.statement_uid == 0)))\
			.order_by(Track.uid.desc()).join(Statement).first()
		last_statement_uid = db_track_last_statement.statement_uid
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'last statement ' + str(last_statement_uid))

		return_dict = {}
		qh = QueryHelper()
		# get premisses and conclusion as text
		return_dict['premisse_text'], premisses_as_statements_uid = qh.get_text_for_premissesGroup_uid(last_premisses_group_uid)
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(last_statement_uid)

		# getting the argument of the premisses and conclusion
		logger('DatabaseHelper', 'get_attack_for_premissegroup', 'find argument with group ' + str(last_premisses_group_uid)
				+ ' conclusion statement ' + str(last_statement_uid))
		db_argument = DBSession.query(Argument).filter(and_(Argument.premissesGroup_uid==last_premisses_group_uid,
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
			QueryHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid, qh.get_relation_uid_by_name(key), 0)

		return return_dict, status

	def get_attack_for_argument(self, transaction, user, uid_text):
		"""

		:param transaction:
		:param user:
		:param uid_text:
		:return:
		"""

		logger('DatabaseHelper', 'get_attack_for_argument', 'main')

		qh = QueryHelper()
		splitted_id = uid_text.split('_')
		relation = splitted_id[0]
		premissesgroup_uid = splitted_id[2]

		# get last tracked conclusion
		db_last_tracked_premissegroup = DBSession.query(Track).join(PremisseGroup).order_by(Track.uid.desc()).first()
		db_last_conclusion = DBSession.query(Premisse).filter_by(premissesGroup_uid=db_last_tracked_premissegroup.premissesGroup_uid).first() # todo

		db_argument = DBSession.query(Argument).filter(and_(Argument.conclusion_uid==db_last_conclusion.statement_uid,
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
			QueryHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid, qh.get_relation_uid_by_name(key), 0)

		return return_dict, status

	def get_reply_confrontations_response(self, transaction, uid_text, user):
		"""

		:param transaction:
		:param uid:
		:param user:
		:return:
		"""
		qh = QueryHelper()
		splitted_id = uid_text.split('_')
		relation = splitted_id[0]
		argument_uid = splitted_id[2]

		# get argument
		logger('DatabaseHelper', 'get_reply_confrontations_response', 'get reply confrontations for argument ' + argument_uid)
		db_argument = DBSession.query(Argument).filter_by(uid=int(argument_uid)).first()

		# get attack
		key = 'reason'
		return_dict, type, status = qh.get_attack_for_argument_uid_by_relation(db_argument.uid, relation, key)
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

		QueryHelper().save_track_for_user(transaction, user, 0, 0, argument_uid, 0, qh.get_relation_uid_by_name(relation.lower()))

		return return_dict, status

	def get_logfile_for_statement(self, uid):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:return: dictionary with the logfile-rows
		"""
		logger('DatabaseHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

		db_statement = DBSession.query(Statement).filter_by(uid=uid).first()
		db_textversions = DBSession.query(TextVersion).filter_by(textValue_uid=db_statement.text_uid).join(User).all()

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

		db_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid=uid).first() # todo for premisse groups
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
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'set_statement', 'user: ' + str(user) + 'user_id: ' + str(db_user.uid) + ', statement: ' + str(statement))

		# check for dot at the end
		if not statement.endswith("."):
			statement += "."

		# check, if the statement already exists
		db_duplicate = DBSession.query(TextVersion).filter_by(content=statement).first()

		# add the version
		textversion = db_duplicate if db_duplicate else TextVersion(content=statement, author=db_user.uid, weight=0)
		DBSession.add(textversion)
		DBSession.flush()

		# add a new cache
		textvalue = TextValue(textversion=textversion.uid)
		DBSession.add(textvalue)
		DBSession.flush()
		textversion.set_textvalue(textvalue.uid)

		# add the statement
		statement = Statement(text=textvalue.uid, isstartpoint=is_start)
		DBSession.add(statement)
		DBSession.flush()

		# get the new statement
		new_statement = DBSession.query(Statement).filter_by(text_uid=textvalue.uid).order_by(Statement.uid.desc()).first()
		return_dict = DictionaryHelper().save_statement_row_in_dictionary(new_statement)
		transaction.commit()

		return return_dict

	def set_premisses(self, transaction, pro_dict, con_dict, user, belongsToArgument, relation, related_argument):
		"""
		Inserts the given dictionaries as premisses for an statement or an argument
		:param transaction: current transaction for the database
		:param pro_dict: dictionary with all pro statements
		:param con_dict: dictionaory with all contra statements
		:param user: current users nickname
		:param belongsToArgument: true, whether the dictionaries belong to an argument, false, whether they belong to a premisse
		:return:
		"""

		# user and last given statement
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		db_track = DBSession.query(Track).filter_by(author_uid=db_user.uid).order_by(Track.uid.desc()).first()
		db_track_statement_uid = db_track.statement_uid

		# insert the premisses as statements
		return_dict = {}
		qh = QueryHelper()

		logger('DatabaseHelper', 'set_premisses', 'starts with pro_dict')
		for index, pro in enumerate(pro_dict):
			# first, save the premisse as statement
			statement_dict = self.set_statement(transaction, pro_dict[pro], user, False)
			return_dict['pro_' + str(index)] = statement_dict
			# second, set the new statement as premisse
			new_premissegroup_uid = qh.set_statements_as_premisse(transaction, statement_dict, user)
			logger('DatabaseHelper', 'set_premisses', pro_dict[pro] + ' in new_premissegroup_uid ' + str(new_premissegroup_uid))
			logger('DatabaseHelper', 'set_premisses',
			       'argument from group ' + str(new_premissegroup_uid) + ' to statement ' + str(db_track_statement_uid) + ', supportive')
			# third, insert the argument
			if belongsToArgument:
				logger('DatabaseHelper', 'set_premisses', 'new argument in relation to an ' + relation)
				qh.set_premisses_related_to_argument(new_premissegroup_uid, user, relation, related_argument, True)
			else:
				qh.set_argument(new_premissegroup_uid, True, user, db_track_statement_uid, 0)

		logger('DatabaseHelper', 'set_premisses', 'starts with con_dict')
		for index, con in enumerate(con_dict):
			# first, save the premisse as statement
			statement_dict = self.set_statement(transaction, con_dict[con], user, False)
			return_dict['con_' + str(index)] = statement_dict
			# second, set the new statement as premisse
			new_premissegroup_uid = qh.set_statements_as_premisse(transaction, statement_dict, user)
			logger('DatabaseHelper', 'set_premisses', con_dict[con] + ' in new_premissegroup_uid ' + str(new_premissegroup_uid))
			logger('DatabaseHelper', 'set_premisses', 'argument from group ' + str(new_premissegroup_uid) + ' to statement ' + str(db_track_statement_uid) + ', not supportive')
			# third, insert the argument
			if belongsToArgument:
				logger('DatabaseHelper', 'set_premisses', 'new argument in relation to an ' + relation)
				qh.set_premisses_related_to_argument(new_premissegroup_uid, user, relation, related_argument, False)
				# qh.set_attack_on_argument()
			else:
				qh.set_argument(new_premissegroup_uid, False, user, db_track_statement_uid, 0)
		transaction.commit()

		return return_dict


