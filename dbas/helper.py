import logging
import random
import smtplib
import collections
import json

from socket import error as socket_error

from cryptacular.bcrypt import BCRYPTPasswordManager
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from sqlalchemy import and_, not_

from .database import DBSession
from .database.model import Argument, Statement, Track, User, Group, TextValue, TextVersion, Premisse, PremisseGroup, Relation

# TODO: PEP 8

log = logging.getLogger(__name__)


def logger(who, when, what):
	log.debug(who.upper() + ' ' + when + ' <' + what + '>')


class PasswordGenerator(object):

	# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
	def get_rnd_passwd(self):
		"""
		Generates a password with the length of 8 out of [a-z][A-Z][+-*/#!*?]
		:return: new secure password
		"""
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		upperalphabet = alphabet.upper()
		symbols = '+-*/#!*?'
		pw_len = 8
		pwlist = []

		for i in range(pw_len//3):
			pwlist.append(alphabet[random.randrange(len(alphabet))])
			pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
			pwlist.append(str(random.randrange(10)))
		for i in range(pw_len-len(pwlist)):
			pwlist.append(alphabet[random.randrange(len(alphabet))])

		pwlist.append(symbols[random.randrange(len(symbols))])
		pwlist.append(symbols[random.randrange(len(symbols))])

		random.shuffle(pwlist)
		pwstring = ''.join(pwlist)

		return pwstring


class PasswordHandler(object):

	def get_hashed_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.encode(password)


class UserHandler(object):

	def update_last_action(self, transaction, nick):
		db_user = DBSession.query(User).filter_by(nickname=str(nick)).first()
		db_user.update_last_action()
		transaction.commit()


class DatabaseHelper(object):

	def is_user_admin(self, user):
		"""
		Check, if the given uid has admin rights or is admin
		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBSession.query(User).filter_by(nickname=str(user)).first()
		db_group = DBSession.query(Group).filter_by(name='admins').first()
		logger('DatabaseHelper', 'is_user_admin', 'check for current user')
		if db_user:
			logger('DatabaseHelper', 'is_user_admin', 'user exists; check for admin')
			if db_user.nickname == 'admin' or db_user.group_uid == db_group.uid:
				logger('DatabaseHelper', 'is_user_admin', 'user is admin')
				return True

		return False

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
		is_admin = self.is_user_admin(user)
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

	def get_premisses_for_statement(self, statement_uid, issupportive):
		"""
		Returns premisses for statements
		:return: dictionary
		"""
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

	def get_reply_for_premissegroup(self, transaction, user):
		"""
		Based on the last given premissesgroup and statement, an attack will be choosen and replied.
		:param transaction: current transaction
		:param user: current nick of the user
		:return: A random attack (undermine, rebut undercut) based on the last saved premissesgroup and statement as well as many texts
		like the premisse as text, conclusion as text, attack as text, confrontation as text. Everything is in a dict.
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'main')

		# get last statement out of the history
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'last statement with user ' + str(db_user.uid) + ', and statement not zero')
		db_track_last_statement = DBSession.query(Track).filter(and_(Track.author_uid==db_user.uid, not_(Track.statement_uid == 0)))\
			.order_by(Track.uid.desc()).join(Statement).first()
		last_statement_uid = db_track_last_statement.statement_uid
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'last statement ' + str(last_statement_uid))

		# get last premisses out of the history
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'last pgroup with user ' + str(db_user.uid) + ', and pgroup not zero')
		db_track_last_pgroup = DBSession.query(Track).filter(and_(Track.author_uid==db_user.uid, not_(Track.premissesGroup_uid == 0)))\
			.order_by(Track.uid.desc()).join(PremisseGroup).first()
		last_premisses_group_uid = db_track_last_pgroup.premissesGroup_uid
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'last premissesgroup ' + str(last_premisses_group_uid))

		return_dict = {}
		qh = QueryHelper()
		# get premisses and conclusion as text
		return_dict['premisse_text'], premisses_as_statements_uid = qh.get_text_for_premissesGroup_uid(last_premisses_group_uid)
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(last_statement_uid)

		# getting the argument of the premisses and conclusion
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'find argument with group ' + str(last_premisses_group_uid)
				+ ' conclusion statement ' + str(last_statement_uid))
		db_argument = DBSession.query(Argument).filter(and_(Argument.premissesGroup_uid==last_premisses_group_uid,
				Argument.conclusion_uid==last_statement_uid, Argument.isSupportive==True)).order_by(Argument.uid.desc()).first()

		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'argument uid ' + str(db_argument.uid) if db_argument else 'none')
		return_dict['argument_id'] = str(db_argument.uid) if db_argument else '0'

		# getting undermines or undercuts or rebuts
		rnd = random.randrange(0, 3 if db_argument else 2)
		logger('DatabaseHelper', 'get_reply_for_premissegroup', 'random attack is ' + str(rnd))
		#rnd = 1
		if rnd == 0:
			key = 'undermine'
			attacks = qh.get_undermines_for_premisses(key, premisses_as_statements_uid)
		elif rnd == 1:
			key = 'rebut'
			attacks = qh.get_rebuts_for_arguments_conclusion_uid(key, last_statement_uid, True)
		else:
			key = 'undercut'
			attacks = qh.get_undercuts_for_argument_uid(key, db_argument.uid)
		return_dict['attack'] = key

		status = 1
		if int(attacks[key]) == 0:
			logger('DatabaseHelper', 'get_reply_for_premissegroup', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key])))
			logger('DatabaseHelper', 'get_reply_for_premissegroup', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_id'] = attacks[key + str(attack_no) + 'id']

			# save one random attack
			self.save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
		                             qh.get_relation_uid_by_name(key), 0)

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

		key = 'reason'
		type = ''
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
			return_dict = qh.get_rebuts_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		else:
			return_dict = {}
			type = 'none'
			status = '-1'
		logger('DatabaseHelper', 'get_reply_confrontations_response', 'attack (' + relation + ') was fetched for ' + str(argument_uid))

		# check return value
		if not return_dict:
			return_dict = {}
			return return_dict, '0'
		if len(return_dict) == 0:
			return_dict[key] = '0'
			return return_dict, '0'

		return_dict['premissegroup'], uids = qh.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid)
		return_dict['previous_argument'] = qh.get_text_for_argument_uid(argument_uid)
		# Get right response with premisse, conclusion, attack and so on
		# Todo: what is with an conclusion as premisse group?
		return_dict['relation'] = splitted_id[0]
		return_dict['argument_uid'] = argument_uid
		return_dict['type'] = type

		if db_argument.conclusion_uid is None or db_argument.conclusion_uid == 0:
			return_dict['conclusion_text'] = qh.get_text_for_argument_uid(db_argument.argument_uid)
			logger('DatabaseHelper', 'get_reply_confrontations_response', return_dict['conclusion_text'])
		else:
			return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_argument.conclusion_uid)

		# save track
		relation_uid = qh.get_relation_uid_by_name(relation.lower())
		self.save_track_for_user(transaction, user, 0, db_argument.premissesGroup_uid, argument_uid, 0, relation_uid)

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

	def get_track_for_user(self, user):
		"""
		Returns the complete track of given user
		:param user: current user id
		:return: track os the user id as dict
		ödictionary
		"""
		logger('DatabaseHelper', 'get_track_for_user', 'user ' + user)
		db_user = DBSession.query(User).filter_by(nickname=user).first()

		if db_user:
			db_track = DBSession.query(Track).filter_by(author_uid=db_user.uid).all()
			return_dict = collections.OrderedDict()
			qh = QueryHelper()
			for track in db_track:
				logger('DatabaseHelper','get_track_for_user','track uid ' + str(track.uid))

				# TODO GET TEXT
				db_statement = DBSession.query(Statement).filter_by(uid=track.statement_uid).first()
				# tmp_dict = DictionaryHelper().save_statement_row_in_dictionary(db_statement)
				track_dict = dict()

				attacked_by_relation = DBSession.query(Relation).filter_by(uid=track.attacked_by_relation).first()
				attacked_with_relation = DBSession.query(Relation).filter_by(uid=track.attacked_with_relation).first()
				attacked_by_relation = qh.get_relation_uid_by_name(attacked_by_relation.name) if attacked_by_relation else 'None'
				attacked_with_relation = qh.get_relation_uid_by_name(attacked_with_relation.name) if attacked_with_relation else 'None'

				if not attacked_by_relation == 'None':
					# db_argument = DBSession.query(Argument).filter_by(uid=track.argument_uid).first()
					# relation = ' supports ' if db_argument.isSupportive else ' attacks '
					# text = qh.get_text_for_statement_uid(track.statement_uid)\
					#       + relation\
					#       + qh.get_text_for_premissesGroup_uid(track.premissesGroup_uid)
					text = '2'
				elif not attacked_with_relation == 'None':
					# db_argument = DBSession.query(Argument).filter_by(uid=track.argument_uid).first()
					# relation = ' supports ' if db_argument.isSupportive else ' attacks '
					# text = qh.get_text_for_argument_uid(track.argument_uid)\
					#       + relation\
					#       + qh.get_text_for_statement_uid(track.statement_uid)
					text = '2'
				elif not track.statement_uid == 0:
					text = '4'
				elif not track.premissesGroup_uid == 0:
					text = '4'
				else:
					text = '5'

				track_dict['author_uid'] = str(track.author_uid)
				track_dict['statement_uid'] = str(track.statement_uid)
				track_dict['premissesGroup_uid'] = str(track.premissesGroup_uid)
				track_dict['argument_uid'] = str(track.argument_uid)
				track_dict['attacked_by_relation'] = attacked_by_relation
				track_dict['attacked_with_relation'] = attacked_with_relation
				track_dict['timestamp'] = str(track.timestamp)
				track_dict['text'] = '? Todo: ' + text + ' ?'#str(tmp_dict['text'])
				return_dict[track.uid] = track_dict

			else:
				logger('DatabaseHelper', 'get_track_for_user', 'no track')
		else:
			return_dict = dict()
			logger('DatabaseHelper', 'get_track_for_user', 'no user')

		return return_dict

	def del_track_for_user(self, transaction, user):
		"""
		Returns the complete track of given user
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'del_track_for_user','user ' + str(db_user.uid))
		DBSession.query(Track).filter_by(author_uid=db_user.uid).delete()
		transaction.commit()

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
		success = True

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

	def save_track_for_user(self, transaction, user, statement_id, premissesgroup_uid, argument_uid, attacked_by_relation, \
	                                                                                        attacked_with_relation): # TODO
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param statememt_id: id of the clicked statement
		:param premissesgroup_uid: id of the clicked premisseGroup
		:param attacked_by_relation: id of attacked by relation
		:param attacked_with_relation: id of attacked_w th relation
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid) +
														', statememt_id ' + str(statement_id) +
														', premissesgroup_uid ' + str(premissesgroup_uid) +
														', argument_uid ' + str(argument_uid) +
														', attacked_by_relation ' + str(attacked_by_relation) +
														', attacked_with_relation ' + str(attacked_with_relation))
		DBSession.add(Track(user=db_user.uid, statement=statement_id, premissegroup=premissesgroup_uid, argument = argument_uid,
		                    attacked_by=attacked_by_relation, attacked_with=attacked_with_relation))
		transaction.commit()

	def save_premissegroup_for_user(self, transaction, user, premissesgroup_uid):
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param premissesgroup_uid: id of the clicked premisseGroup
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_premissegroup_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid)+ ', premissesGroup_uid: '
				+ str(premissesgroup_uid))
		db_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid = premissesgroup_uid).all()
		for premisse in db_premisses:
			logger('QueryHelper', 'save_premissegroup_for_user', str(premissesgroup_uid) + " " + str(premisse.statement_uid))
			new_track = Track(user=db_user.uid, statement=premisse.statement_uid, premissegroup=premissesgroup_uid)
			DBSession.add(new_track)
		transaction.commit()


class QueryHelper(object):

	def get_relation_uid_by_name(self, relation_name):
		"""

		:param relation_name:
		:return:
		"""
		db_relation = DBSession.query(Relation).filter_by(name=relation_name).first()
		logger('DatabaseHelper', 'set_statements_as_premisse', 'return ' + str(db_relation.name if db_relation else -1))
		return db_relation.uid if db_relation else -1

	def set_statements_as_premisse(self, transaction, statement, user):
		"""

		:param transaction:
		:param statement:
		:param user:
		:return: uid of the PremisseGroup
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		premisse_group = PremisseGroup(author=db_user.uid)
		DBSession.add(premisse_group)
		DBSession.flush()

		premisse_list = []
		logger('DatabaseHelper', 'set_statements_as_premisse', 'premissesgroup=' + str(premisse_group.uid) + ', statement='
				+ statement['uid'] + ', isnegated=' + ('0' if False else '1') + ', author=' + str(db_user.uid))
		premisse = Premisse(premissesgroup=premisse_group.uid, statement=int(statement['uid']), isnegated=False, author=db_user.uid)
		premisse_list.append(premisse)

		DBSession.add_all(premisse_list)
		DBSession.flush()

		db_premissegroup = DBSession.query(PremisseGroup).filter_by(author_uid=db_user.uid).order_by(PremisseGroup.uid.desc()).first()
		return db_premissegroup.uid

	def set_argument(self, premissegroup_uid, is_supportive, user, conclusion_uid, argument_uid):
		"""

		:param premissegroup_uid:
		:param is_supportive:
		:param user:
		:param conclusion_uid:
		:param argument_uid:
		:return:
		"""
		logger('QueryHelper', 'set_argument_with_premissegroup', 'main')
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		argument = Argument(premissegroup=premissegroup_uid, issupportive=is_supportive, author=db_user.uid, weight=0,
							conclusion=conclusion_uid)
		argument.conclusions_argument(argument_uid)

		DBSession.add(argument)
		DBSession.flush()

		return '1'

	def set_premisses_related_to_argument(self, premissegroup_uid, user, relation, related_argument_uid, is_supportive):
		"""

		:param premissegroup_uid:
		:param user:
		:param relation:
		:param related_argument_uid:
		:param is_supportive:
		:return:
		"""
		logger('QueryHelper', 'set_premisses_related_to_argument', 'main, ' + ('supports' if is_supportive else 'attacks') + ' related argument ' + str(related_argument_uid))

		db_user = DBSession.query(User).filter_by(nickname=user).first()
		db_related_argument = DBSession.query(Argument).filter_by(uid=related_argument_uid).first()

		# todo: is this right?

		lo = 'set_premisses_related_to_argument'
		pg = str(premissegroup_uid)
		if 'undermine' in relation.lower() or 'support' in relation.lower():
			logger('QueryHelper', lo, relation + ' from group ' + pg + ' to statement ' + str(db_related_argument.premissesGroup_uid))
			db_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid=db_related_argument.premissesGroup_uid).all()
			arguments = []
			for premisse in db_premisses:
				argument = Argument(premissegroup=premissegroup_uid,
									issupportive=is_supportive,
									author=db_user.uid,
									weight=0,
									conclusion=premisse.statement_uid)
				arguments.append(argument)

		elif 'undercut' in relation.lower() or 'overbid' in relation.lower():
			logger('QueryHelper', lo, relation + ' from group ' + pg + ' to argument ' + str(db_related_argument.uid))
			argument = Argument(premissegroup=premissegroup_uid,
								issupportive=is_supportive,
								author=db_user.uid,
								weight=0)
			argument.conclusions_argument(db_related_argument.uid)
			arguments = []
			arguments.append(argument)

		elif 'rebut' in relation.lower():
			logger('QueryHelper', lo, 'rebut from group ' + pg + ' to conclusiongroup ' + str(db_related_argument.conclusion_uid))
			argument = Argument(premissegroup=premissegroup_uid,
								issupportive=is_supportive,
								author=db_user.uid,
								weight=0,
								conclusion=db_related_argument.conclusion_uid)
			arguments = []
			arguments.append(argument)
		else:
			logger('QueryHelper', 'set_premisses_related_to_argument', 'error')
			return '-1'

		DBSession.add_all(arguments)
		DBSession.flush()

	def get_text_for_statement_uid(self, uid):
		"""

		:param uid: id of a statement
		:return: text of the mapped textvalue for this statement
		"""
		logger('QueryHelper', 'get_text_for_statement_uid', 'uid ' + str(uid))
		db_statement = DBSession.query(Statement).filter_by(uid=uid).join(TextValue).first()
		db_textversion = DBSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
			textValue_uid=db_statement.textvalues.uid).first()
		logger('QueryHelper', 'get_text_for_statement_uid', 'text ' + db_textversion.content)
		tmp = db_textversion.content
		if tmp.endswith('.'):
			tmp = tmp[:-1]
		return tmp

	def get_text_for_argument_uid(self, uid):
		"""

		:param uid:
		:return:
		"""
		db_argument = DBSession.query(Argument).filter_by(uid=uid).join(Statement).first()
		logger('QueryHelper', 'get_text_for_argument_uid', 'uid ' + str(uid) +
		       ', pgroup ' + str(db_argument.premissesGroup_uid) +
		       ', concl ' + str(db_argument.conclusion_uid) +
		       ', arg ' + str(db_argument.argument_uid))
		retValue = ''

		# basecase
		if db_argument.argument_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'basecase')
			premisses, uids = self.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid)
			premisses = premisses[:-1] if premisses.endswith('.') else premisses # pretty print
			conclusion = conclusion[0:1].lower() + conclusion[1:] # pretty print
			argument = '\'' + premisses + (' supports ' if db_argument.isSupportive else ' attacks ') + conclusion + '\''
			return argument

		# recursion
		if db_argument.conclusion_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'recursion')
			argument = self.get_text_for_argument_uid(db_argument.argument_uid)
			premisses, uids = self.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid)
			retValue = premisses + (' supports ' if db_argument.isSupportive else ' attacks ') + argument

		return retValue

	def get_text_for_premissesGroup_uid(self, uid):
		"""

		:param uid: id of a premisse group
		:return: text of all premisses in this group and the uids as list
		"""
		logger('QueryHelper', 'get_text_for_premissesGroup_uid', 'main group ' + str(uid))
		db_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid=uid).join(Statement).all()
		text = ''
		uids = []
		for premisse in db_premisses:
			logger('QueryHelper', 'get_text_for_premissesGroup_uid', 'premisse ' + str(premisse.premissesGroup_uid) + ' . statement'
					+ str(premisse.statement_uid) + ', premisse.statement ' + str(premisse.statements.uid))
			tmp = self.get_text_for_statement_uid(premisse.statements.uid)
			if tmp.endswith('.'):
				tmp = tmp[:-1]
			uids.append(str(premisse.statements.uid))
			text += ' and ' + tmp[:1].lower() + tmp[1:]

		return text[5:], uids

	def get_undermines_for_premisses(self, key, premisses_as_statements_uid):
		"""

		:param premisses_as_statements_uid:
		:param key:
		:return:
		"""
		logger('QueryHelper', 'get_undermines_for_premisses', 'main')
		return_dict = {}
		index = 0
		for s_uid in premisses_as_statements_uid:
			logger('QueryHelper', 'get_undermines_for_premisses', 'db_undermine against Argument.conclusion_uid=='+str(s_uid))
			db_undermine = DBSession.query(Argument).filter(and_(Argument.isSupportive==False, Argument.conclusion_uid==s_uid)).all()
			for undermine in db_undermine:
				logger('QueryHelper', 'get_undermines_for_premisses', 'found db_undermine ' + str(undermine.uid))
				return_dict[key + str(index)], uids = QueryHelper().get_text_for_premissesGroup_uid(undermine.premissesGroup_uid)
				return_dict[key + str(index) + 'id'] = undermine.premissesGroup_uid
				index += 1
		return_dict[key] = str(index)
		return return_dict

	def get_undermines_for_argument_uid(self, key, argument_uid):
		"""
		Calls get_undermines_for_premisses('reason', premisses_as_statements_uid)
		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(argument_uid))
		db_attacked_argument = DBSession.query(Argument).filter_by(uid=argument_uid).first()
		db_attacked_premisses = DBSession.query(Premisse).filter_by(
			premissesGroup_uid=db_attacked_argument.premissesGroup_uid).order_by(Premisse.premissesGroup_uid.desc()).all()

		premisses_as_statements_uid = set()
		for premisse in db_attacked_premisses:
			premisses_as_statements_uid.add(premisse.statement_uid)
			logger('QueryHelper', 'get_undermines_for_argument_uid', 'db_attacked_argument has pgroup with pgroup ' +
		           str(premisse.premissesGroup_uid) + ', statement ' + str(premisse.statement_uid))

		if len(premisses_as_statements_uid) == 0:
			return None

		return self.get_undermines_for_premisses(key, premisses_as_statements_uid)

	def get_overbids_for_argument_uid(self, key, argument_uid):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, True)
		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_overbids_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, True)

	def get_undercuts_for_argument_uid(self, key, argument_uid):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, False)
		:param argument_uid:
		:param key:
		:return:
		"""
		logger('QueryHelper', 'get_undercuts_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, False)

	def get_rebuts_for_arguments_conclusion_uid(self, key, conclusion_statements_uid, is_current_argument_supportive):
		"""

		:param key:
		:param conclusion_statements_uid:
		:param is_current_argument_supportive:
		:return:
		"""
		return_dict = {}
		logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid',
		       'db_rebut against Argument.conclusion_uid=='+str(conclusion_statements_uid))
		db_rebut = DBSession.query(Argument).filter(Argument.isSupportive==(not is_current_argument_supportive),
		                                            Argument.conclusion_uid==conclusion_statements_uid).all()
		for index, rebut in enumerate(db_rebut):
			logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'found db_rebut ' + str(rebut.uid))
			return_dict[key + str(index)], uids = QueryHelper().get_text_for_premissesGroup_uid(rebut.premissesGroup_uid)
			return_dict[key + str(index) + 'id'] = rebut.premissesGroup_uid
		return_dict[key] = str(len(db_rebut))
		return return_dict

	def get_rebuts_for_argument_uid(self, key, argument_uid):
		"""
		Calls self.get_rebuts_for_arguments_conclusion_uid('reason', Argument.conclusion_uid)
		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_rebuts_for_argument_uid', 'main')
		db_argument = DBSession.query(Argument).filter_by(uid=int(argument_uid)).first()
		if not db_argument:
			return None
		return self.get_rebuts_for_arguments_conclusion_uid(key, db_argument.conclusion_uid, db_argument.isSupportive)

	def get_supports_for_argument_uid(self, key, argument_uid):
		"""

		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_supports_for_argument_uid', 'main')

		return_dict = {}
		index = 0
		db_argument = DBSession.query(Argument).filter_by(uid=argument_uid).join(PremisseGroup).first()
		db_arguments_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid=db_argument.premissesGroup_uid).all()

		for arguments_premisses in db_arguments_premisses:
			db_supports = DBSession.query(Argument).filter(and_(Argument.conclusion_uid==arguments_premisses.statement_uid,
			                                                    Argument.isSupportive==True)).join(PremisseGroup).all()
			if not db_supports:
				continue

			for support in db_supports:
				return_dict[key + str(index)], trash = self.get_text_for_premissesGroup_uid(support.premissesGroup_uid)
				return_dict[key + str(index) + 'id'] = support.premissesGroup_uid
				index += 1

		return_dict[key] = str(index)

		return None if len(return_dict) == 0 else return_dict

	def get_attack_or_support_for_justification_of_argument_uid(self, key, argument_uid, is_supportive):
		"""

		:param key:
		:param argument_uid:
		:param is_supportive:
		:return:
		"""
		return_dict = {}
		logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid=='+str(argument_uid))
		db_relation = DBSession.query(Argument).filter(Argument.isSupportive==is_supportive, Argument.argument_uid==argument_uid).all()
		if not db_relation:
			return None
		for index, relation in enumerate(db_relation):
			logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
					'found relation, argument uid ' + str(relation.uid))
			return_dict[key + str(index)], uids = QueryHelper().get_text_for_premissesGroup_uid(relation.premissesGroup_uid)
			return_dict[key + str(index) + 'groupid'] = relation.premissesGroup_uid
			return_dict[key + str(index) + 'id'] = ','.join(uids)
		return_dict[key] = str(len(db_relation))
		return return_dict


class DictionaryHelper(object):

	def get_subdictionary_out_of_orderer_dict(self, ordered_dict, count):
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
		for item in items:
			logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'all items: ' + ''.join(str(item)))
		if count < 0:
			return ordered_dict
		elif count == 1:
			if len(items) > 1:
				rnd = random.randint(0, len(items)-1)
				logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'return item at ' + str(rnd))
				return_dict[items[rnd][0]] = items[rnd][1]
			else:
				return ordered_dict
		else:

			for i in range(0, count):
				rnd = random.randint(0, len(items)-1)
				logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'for loop ' + str(i) + '. add element at ' + str(rnd))
				return_dict[items[rnd][0]] = items[rnd][1]
				items.pop(rnd)

		return return_dict

	def dictionarty_to_json_array(self, raw_dict, ensure_ascii):
		"""
		Dumps given dictionary into json
		:param raw_dict: dictionary for dumping
		:param ensure_ascii: if true, ascii will be checked
		:return: json data
		"""
		return_dict = json.dumps(raw_dict, ensure_ascii)
		return return_dict

	def save_statement_row_in_dictionary(self, statement_row):
		"""
		Saved a row in dictionary
		:param statement_row: for saving
		:return: dictionary
		"""
		db_statement = DBSession.query(Statement).filter_by(uid=statement_row.uid).join(TextValue).first()
		db_textversion = DBSession.query(TextVersion).filter_by(uid=db_statement.textvalues.textVersion_uid).join(User).first()
		logger('DictionaryHelper', 'save_statement_row_in_dictionary',
				'db_statement.uid ' + str(db_statement.uid) + ', ' +
				'db_statement.textvalues.textVersion_uid ' + str(db_statement.textvalues.textVersion_uid) + ', ' +
				'db_textversion.uid ' + str(db_textversion.uid))
		uid = str(db_statement.uid)
		text = db_textversion.content
		date = str(db_textversion.timestamp)
		weight = str(db_textversion.weight)
		author = db_textversion.users.nickname
		if text.endswith('.'):
			text = text[:-1]
		logger('DictionaryHelper', 'save_statement_row_in_dictionary', uid + ', ' + text + ', ' + date + ', ' + weight + ', ' + author)
		dic = dict()
		dic['uid'] = uid
		dic['text'] = text
		dic['date'] = date
		dic['weight'] = weight
		dic['author'] = author
		return dic


class EmailHelper(object):

	def send_mail(self, request, subject, body, recipient):
		"""
		Try except block for sending an email
		:param request: current request
		:param subject: subject text of the mail
		:param body: body text of the mail
		:param recipient: recipient of the mail
		:return: boolean if message was sent, boolean an error occured, message if an error occured
		"""
		logger('EmailHelper', 'send_mail', 'sending mail with subject \'' + subject + '\' to ' + recipient)
		send_message = False
		contact_error = False
		mailer = get_mailer(request)
		body = body +"\n\n---\n" + \
				"This is an automatically generated mail by the D-BAS System.\n" + \
				"For contact please write an mail to krauthoff@cs.uni-duesseldorf.de\n" + \
				"This system is part of a doctoral thesis and currently in an alpha-phase."
		message = Message(subject=subject, sender='dbas.hhu@gmail.com', recipients=[recipient], body=body)
		# try sending an catching errors
		try:
			mailer.send_immediately(message, fail_silently=False)
			send_message = True
			message = 'An E-Mail was sent to the given address.'
		except smtplib.SMTPConnectError as exception:
			logger('EmailHelper', 'send_mail', 'error while sending')
			code = str(exception.smtp_code)
			error = str(exception.smtp_error)
			logger('EmailHelper', 'send_mail', 'exception smtplib.SMTPConnectError smtp_code ' + code)
			logger('EmailHelper', 'send_mail', 'exception smtplib.SMTPConnectError smtp_error ' + error)
			contact_error = True
			message = 'Your message could not be send due to a system error! (' + 'smtp_code ' + code + ' || smtp_error ' + error + ')'
		except socket_error as serr:
			logger('EmailHelper', 'send_mail', 'error while sending')
			logger('EmailHelper', 'send_mail', 'socket_error ' + str(serr))
			contact_error = True
			message = 'Your message could not be send due to a system error! (' + 'socket_error ' + str(serr) + ')'

		return send_message, contact_error, message
