import logging
import random
import smtplib
import collections
import json

from random import randint

from socket import error as socket_error

from cryptacular.bcrypt import BCRYPTPasswordManager
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from sqlalchemy import and_

from .database import DBSession
from .database.model import Argument, Statement, Track, User, Group, TextValue, TextVersion, Premisse


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


class QueryHelper(object):

	def is_user_admin(self, user):
		"""
		Check, if the given uid has admin rights or is admin
		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBSession.query(User).filter_by(nickname=str(user)).first()
		db_group = DBSession.query(Group).filter_by(name='admins').first()
		logger('QueryHelper', 'is_user_admin', 'check for current user')
		if db_user:
			logger('QueryHelper', 'is_user_admin', 'user exists; check for admin')
			if db_user.nickname == 'admin' or db_user.group == db_group.uid:
				logger('QueryHelper', 'is_user_admin', 'user is admin')
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
		logger('QueryHelper', 'correct_statement', 'def')

		return_dict = dict()
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		db_statement = DBSession.query(Statement).filter_by(uid=uid).join(TextValue).first()
		db_textvalue = DBSession.query(TextValue).filter_by(uid=db_statement.text_uid).join(TextVersion,
		                                                                                    TextVersion.uid==TextValue.textVersion_uid).first()
		if db_user:
			logger('QueryHelper', 'correct_statement', 'given user exists and correction will be set')
			textversion = TextVersion(content=corrected_text, author=db_user.uid, weight=db_textvalue.textversions.weight)
			textversion.set_textvalue(db_textvalue.uid)
			DBSession.add(textversion)
			DBSession.flush()
			db_textvalue.update_textversion(textversion.uid)
			transaction.commit()
			return_dict['status'] = '1'
		else:
			logger('QueryHelper', 'correct_statement', 'user not found')
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
		logger('QueryHelper', 'get_all_users', 'is_admin ' + str(is_admin))
		if not is_admin:
			return_dict = dict()
		else:
			logger('QueryHelper', 'get_all_users', 'get all users')
			db_users = DBSession.query(User).join(Group).all()
			logger('QueryHelper', 'get_all_users', 'get all groups')

			return_dict = dict()

			if db_users:
				logger('QueryHelper', 'get_all_users', 'iterate all users')
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
					logger('QueryHelper', 'get_all_users ' + str(user.uid) + ' of ' + str(len(db_users)),
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

	# def get_all_arguments_by_arg_uid(self, uid, is_supportive):
	# 	"""
	# 	Getting every pro/con arument, which is for/against the same position as the given argument uid
	# 	:param uid: uid of the argument
	# 	:param is_supportive: true, if all supportive arguments should be fetched
	# 	:return: ordered dictionary
	# 	"""
	#
	# 	# # raw query
	# 	# select * from arguments where uid in (
	# 	# select arg_uid from relation_argpos where pos_uid in (
	# 	# select pos_uid from relation_argpos where arg_uid = 3 and is_supportive = 1
	# 	# ) and is_supportive = 0
	# 	# );
	#
	# 	return_dict = collections.OrderedDict()
	# 	logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'check for uid')
	# 	support = 1 if is_supportive else 0
	# 	was_suportive = 0 if is_supportive else 1
	#
	# 	if uid:
	# 		logger('QueryHelper', 'get_all_arguments_by_arg_uid ', 'get connected position for argument uid ' + str(uid))
	# 		db_posuid = DBSession.query(RelationArgPos).filter(
	# 			and_(RelationArgPos.arg_uid == uid, RelationArgPos.is_supportive == was_suportive)).first()
	#
	# 		if db_posuid:
	# 			logger('QueryHelper', 'get_all_arguments_by_arg_uid',  'get all arguments from the opposite for position uid ' + str(
	# 				db_posuid.pos_uid))
	# 			db_arguids = DBSession.query(RelationArgPos).filter(
	# 				and_(RelationArgPos.pos_uid == db_posuid.pos_uid, RelationArgPos.is_supportive == support)).all()
	#
	# 			logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'iterate all arguments for that uid')
	# 			for argid in db_arguids:
	# 				logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'get argument with' + str(argid.arg_uid))
	# 				db_argument = DBSession.query(Argument).filter_by(uid=argid.arg_uid).first()
	# 				db_correction = DBSession.query(Correction).filter_by(arg_uid=argid.arg_uid).order_by(Correction.uid.desc()).first()
	#
	# 				logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'checks whether argument exists, uid ' + str(argid.uid))
	# 				if db_argument:
	# 					logger('QueryHelper' , 'get_all_arguments_by_arg_uid' , 'add argument in dict' + \
	# 						'uid:' + str(db_argument.uid) + ', val: ' + (db_correction.text if db_correction else db_argument.text))
	# 					return_dict[str(db_argument.uid)] = db_correction.text if db_correction else db_argument.text
	# 				else:
	# 					logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'no argument exists, uid ' + str(argid.uid))
	# 		else:
	# 			logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'no argument exists, uid ' + str(uid))
	#
	# 	else:
	# 		logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'ERROR: uid not found')
	#
	# 	return return_dict

	def get_start_statements(self):
		"""
		Returns start statements
		:return: dictionary
		"""
		return_dict = dict()
		statements_dict = dict()
		db_statements = DBSession.query(Statement).filter_by(isStartpoint=True).all()
		logger('QueryHelper', 'get_start_statements', 'get all statements')
		if db_statements:
			return_dict['status'] = '1'
			logger('QueryHelper', 'get_start_statements', 'there are start statements')
			for stat in db_statements:
				logger('QueryHelper', 'get_start_statements', 'stat ' + str(stat.uid) + ': ' + stat.textvalues.textversions.content)
				statements_dict[str(stat.uid)] = DictionaryHelper().save_statement_row_in_dictionary(stat)
		else:
			logger('QueryHelper', 'get_start_statements', 'there are no statements')
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
		premissesgroups_dict = dict()
		logger('QueryHelper', 'get_premisses_for_statement', 'get all premisses')
		db_arguments = DBSession.query(Argument).filter(and_(Argument.isSupportive==issupportive, Argument.conclusion_uid==statement_uid)).all()

		logger('QueryHelper', 'get_premisses_for_statement', '------------')
		for argument in db_arguments:
			logger('QueryHelper', 'get_premisses_for_statement', 'argument ' + str(argument.uid) + ' (' + str(argument.premissesGroup_uid) + ')')
			db_premisses = DBSession.query(Premisse).filter_by(premissesGroup_uid=argument.premissesGroup_uid).all()

			# check out the group
			premissesgroups_dict = dict()
			for premisse in db_premisses:
				logger('QueryHelper', 'get_premisses_for_statement', 'premisses group ' + str(premisse.premissesGroup_uid))
				db_statements = DBSession.query(Statement).filter_by(uid=premisse.statement_uid).all()
				for statement in db_statements:
					logger('QueryHelper', 'get_premisses_for_statement', 'premisses group has statement ' + str(statement.uid))
					premissesgroups_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement)

			premisses_dict[str(premisse.premissesGroup_uid)] = premissesgroups_dict
		logger('QueryHelper', 'get_premisses_for_statement', '------------')

		# premisses dict has for each group a new dictionary
		return_dict['premisses'] = premisses_dict
		return_dict['status'] = '1'

		db_statements = DBSession.query(Statement).filter_by(uid=statement_uid).first()
		return_dict['currentStatementText'] = DictionaryHelper().save_statement_row_in_dictionary(db_statements)

		return return_dict

	# def get_args_for_justifications(self, uid):
	# 	"""
	# 	Retruns all arguments for justification for the given id
	# 	:param uid:
	# 	:return:
	# 	"""
	# 	return_list = QueryHelper().get_args_list_in_relation_to_statement(uid, True, True)
	# 	justification_dict = dict()
	# 	return_dict = dict()
	# 	if return_list == []:
	# 		return_dict['status'] = '-1'
	# 	else:
	# 		return_dict['status'] = '1'
	# 		for entry in return_list:
	# 			justification_dict[entry['uid']] = entry
	#
	# 		return_dict['justification'] = justification_dict
	#
	# 	return return_dict

	# def get_args_for_new_round(self, user, statement_id):
	# 	"""
	# 	Returns the next argument for a confrontation. This is based on the last given id.
	# 	:param user: current user id, as given in the request params
	# 	:param statement_id: current statement id
	# 	:return: dictionary with 'status' <-> {0 (no contra), 1 (everything is fine), -1 (no justification)},
	# 	the 'currentStatementText' <-> argument of the user and a justification dictionary with mapping uid <-> argument dictionary
	# 	"""
	# 	logger('QueryHelper', 'get_args_for_new_round', 'user ' + str(user) + ', statement id ' + str(statement_id))
	# 	return_dict = collections.OrderedDict()
	#
	# 	# get the last used statement
	# 	db_last_statement = DBSession.query(Argument).filter_by(uid=statement_id).first()
	# 	db_correction = DBSession.query(Correction).filter_by(arg_uid=statement_id).order_by(Correction.uid.desc()).first()
	#
	# 	# save the last statement text in the return dictionary
	# 	text = db_correction.text if db_correction else db_last_statement.text
	# 	logger('QueryHelper', 'get_args_for_new_round', 'last statement is an argument: ' + text)
	# 	return_dict['currentStatementText'] = text
	#
	# 	# get all statements against our statement
	# 	contra_argument_rows = self.get_args_list_in_relation_to_statement(statement_id, False, False)
	# 	if contra_argument_rows:
	# 		# fetch a random contra argument
	# 		contra_argument = self.get_confrontation_argument(contra_argument_rows)
	#
	# 		# pick a random contra argument and get all arguments against the confrontation argument
	# 		return_dict['confrontation'] = contra_argument['text']
	#
	# 		# get all arguments against the confrontation argument
	# 		logger('QueryHelper', 'get_args_for_new_round', 'get args against nth argument as contra ' + str(contra_argument['uid']))
	# 		justifications_dict = collections.OrderedDict()
	# 		justificiation_argument_list = self.get_args_list_in_relation_to_statement(contra_argument['uid'], False, False)
	#
	# 		# get all justifications
	# 		if justificiation_argument_list:
	# 			logger('QueryHelper', 'get_justification_against_statement_uid_as_dict', 'There are arguments against the contra argument')
	# 			for justification in justificiation_argument_list:
	# 				justifications_dict[str(justification['uid'])] = justification
	# 			return_dict['justifications'] = justifications_dict
	# 			return_dict['status_con'] = '1'
	# 		else:
	# 			logger('QueryHelper', 'get_justification_against_statement_uid_as_dict', 'No arguments against the contra argument')
	# 			return_dict['status_con'] = '-1'
	#
	# 	else:
	# 		logger('QueryHelper', 'get_args_for_new_round', 'No arguments for confrontation')
	# 		return_dict['status_con'] = '0'
	#
	# 	# get all statements against for statement
	# 	pro_argument_rows = self.get_args_list_in_relation_to_statement(statement_id, True, False)
	# 	if pro_argument_rows:
	# 		logger('QueryHelper', 'get_args_for_new_round', 'got new pro arguments')
	# 		pro_arguments = collections.OrderedDict()
	# 		for pro in pro_argument_rows:
	# 			logger('QueryHelper', 'get_args_for_new_round', 'got new pro argument with uid ' + str (pro['uid']))
	# 			pro_arguments[str(pro['uid'])] = pro
	# 		return_dict['new_pros'] = pro_arguments
	# 		return_dict['status_pro'] = '1'
	# 	else:
	# 		logger('QueryHelper', 'get_args_for_new_round', 'No arguments for new pros')
	# 		return_dict['status_pro'] = '0'
	#
	# 	return return_dict

	# def get_args_by_pos(self, uid):
	# 	"""
	# 	Returns all arguments, which are connected to the position
	# 	:param uid: position uid
	# 	:return: dictioanry
	# 	"""
	# 	return_dict = self.get_args_for_justifications(uid)
	#
	#
	# 	# get last statement
	# 	db_last_statement = DBSession.query(Position).filter_by(uid=uid).first()
	# 	# check for correction
	# 	db_correction = DBSession.query(Correction).filter_by(pos_uid=uid).order_by(Correction.uid.desc()).first()
	# 	return_dict['currentStatementText'] = db_correction.text if db_correction else db_last_statement.text
	#
	# 	return return_dict

	# def get_args_list_in_relation_to_statement(self, uid, is_supportive, is_position):
	# 	"""
	# 	Returns every statement with a (non-)supportive connection to the given statement uid
	# 	:param uid: uid of the position
	# 	:param is_supportive: 1 if it is supportive, 0 otherwise
	# 	:param is_position: true, if it is a position
	# 	:return: list with arguments
	# 	"""
	#
	# 	if is_position:
	# 		# # raw query
	# 		# select * from arguments where uid in (
	# 		# select arg_uid from relation_argpos where pos_uid = 1 and is_supportive = 1
	# 		# )
	# 		logger('QueryHelper', 'get_arguments_in_relation_to_statement', 'pos_uid ' + str(uid) + ' support ' + str(is_supportive))
	# 		db_arg_uids = DBSession.query(RelationArgPos).filter(and_(RelationArgPos.pos_uid == uid,
	# 	                                                            RelationArgPos.is_supportive == is_supportive)).all()
	# 	else:
	# 		# # raw query
	# 		# select * from arguments where uid in (
	# 		# select arg_uid1 from relation_argarg where arg_uid2 = 7 and is_supportive = 0
	# 		# )
	# 		logger('QueryHelper', 'get_arguments_in_relation_to_statement', 'arg_uid2 ' + str(uid) + ' support ' + str(is_supportive))
	# 		db_arg_uids = DBSession.query(RelationArgArg).filter(and_(RelationArgArg.arg_uid2 == uid,
	# 	                                                            RelationArgArg.is_supportive == is_supportive)).all()
	#
	# 	return_list = []
	# 	for arg in db_arg_uids:
	#
	# 		if is_position:
	# 			logger('QueryHelper', 'get_arguments_against_position', 'connected ' + ('pro' if is_supportive else 'contra')
	# 				+ ' argument ' + str(arg.arg_uid))
	# 			db_arg = DBSession.query(Argument).filter_by(uid=arg.arg_uid).first()
	# 		else:
	# 			logger('QueryHelper', 'get_arguments_against_argument', 'connected ' + ('pro' if is_supportive else 'contra')
	# 				+ ' argument ' + str(arg.arg_uid1))
	# 			db_arg = DBSession.query(Argument).filter_by(uid=arg.arg_uid1).first()
	#
	# 		argument_dict = DictionaryHelper().save_corrected_statement_row_in_dictionary(db_arg, True)
	# 		return_list.append(argument_dict)
	#
	# 	return return_list

	# def get_args_for_island(self, user):
	# 	"""
	# 	Returns every argument for and against the last tracked argument as json dict with {pro_i: {...}, con_i {...}}
	# 	:param user: requesting user
	# 	:return: dict
	# 	"""
	# 	logger('QueryHelper', 'get_arguments_for_island', 'def')
	# 	return_dict = collections.OrderedDict()
	# 	db_user = DBSession.query(User).filter_by(nickname=user).first()
	# 	db_track = DBSession.query(Track).filter_by(user_uid=db_user.uid).order_by(Track.uid.desc()).first()
	# 	logger('QueryHelper', 'get_arguments_for_island', 'get island view for last selected statement (track:' + str(db_track.arg_uid) + ') '
	# 	                                                                                                                           'from user ' + user)
	#
	# 	if db_track:
	# 		if db_track.is_argument:
	# 			arg_dict = dict()
	# 			dict_pro = self.get_args_list_in_relation_to_statement(db_track.arg_uid, True, False)
	# 			dict_con = self.get_args_list_in_relation_to_statement(db_track.arg_uid, False, False)
	#
	# 			counter = 0
	# 			logger('QueryHelper', 'get_arguments_for_island', 'pro arguments: ' + str(len(dict_pro)))
	# 			for pro_arg in dict_pro:
	# 				arg_dict['pro_' + str(counter)] = pro_arg
	# 				counter += 1
	#
	# 			logger('QueryHelper', 'get_arguments_for_island', 'con arguments: ' + str(len(dict_con)))
	# 			counter = 0
	# 			for con_arg in dict_con:
	# 				arg_dict['con_' + str(counter)] = con_arg
	# 				counter += 1
	#
	# 			return_dict['status'] = '1'
	# 			return_dict['arguments'] = arg_dict
	# 		else:
	# 			logger('QueryHelper', 'get_arguments_for_island', 'no saved argument')
	# 			return_dict['status'] = '-1'
	# 	else:
	# 		logger('QueryHelper', 'get_arguments_for_island', 'no saved track')
	# 		return_dict['status'] = '-1'
	#
	# 	return return_dict

	# def get_confrontation_argument(self, contra_argument_rows):
	# 	"""
	# 	Returns a argument for confrontation
	# 	:param contra_argument_rows: rows of contra arguments
	# 	:return: argument row
	# 	"""
	# 	# fetch a random contra argument
	# 	rnd = randint(0, len(contra_argument_rows)-1)
	# 	logger('QueryHelper', 'get_confrontation_argument', 'get the nth argument as contra ' + str(rnd))
	# 	return contra_argument_rows[rnd]

	def get_logfile_for_statement(self, uid):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:return: dictionary with the logfile-rows
		"""
		logger('QueryHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

		db_statement = DBSession.query(Statement).filter_by(uid=uid).first()
		db_textversions = DBSession.query(TextVersion).filter_by(textValue_uid=db_statement.text_uid).join(User).all()

		index = 0
		return_dict = {}
		content_dict = {}
		# add all corrections
		for versions in db_textversions:
			corr_dict = dict()
			corr_dict['uid'] = str(versions.uid)
			corr_dict['author'] = str(versions.users.nickname)
			corr_dict['date'] = str(versions.timestamp)
			corr_dict['text'] = str(versions.content)
			content_dict[str(index)] = corr_dict
			logger('QueryHelper', 'get_logfile_for_statement', 'statement ' + str(index) + ': ' + versions.content)
			index += 1
		return_dict['content'] = content_dict

		return return_dict

	# def get_data_for_one_step_back(self, user):
	# 	"""
	# 	Gets data to get one step back
	# 	:param user: current user
	# 	:return: dictionary with necessary data
	# 	"""
	# 	db_user = DBSession.query(User).filter_by(nickname=str(user)).first()
	# 	logger('QueryHelper', 'get_data_for_one_step_back', 'user id ' + str(db_user.uid))
	#
	# 	# get the track of arguments for this user
	# 	db_track = DBSession.query(Track).filter_by(user_uid=db_user.uid).order_by(Track.uid.desc()).all()
	#
	# 	return_dict = dict()
	# 	# check for history
	# 	if not db_track:
	# 		logger('QueryHelper', 'get_data_for_one_step_back', 'user has no argument trace')
	# 		return_dict['status'] = '-1'
	# 	else:
	# 		logger('QueryHelper', 'get_data_for_one_step_back', 'user has a trace')
	# 		row = True
	# 		# get second entry, because this is the decision made one step back
	# 		for track in db_track:
	# 			if row:
	# 				logger('QueryHelper', 'get_data_for_one_step_back', 'passed first row')
	# 				row = False
	# 			else:
	# 				row = track
	# 				logger('QueryHelper', 'get_data_for_one_step_back', 'get second row with arg_uid ' + str(track.arg_uid)
	# 				       + ', pos_uid ' + str(track.pos_uid) + ', is_argument ' + str(track.is_argument))
	# 				break
	#
	# 		# do we have a position or an argument?
	# 		if row.arg_uid == -1:
	# 			logger('QueryHelper', 'get_data_for_one_step_back', 'last statement was a position with uid : ' + str(row.pos_uid))
	# 			return_dict = self.get_args_for_justifications(row.pos_uid)
	# 			db_last_position = DBSession.query(Position).filter_by(uid=row.pos_uid).first()
	# 			db_correction = DBSession.query(Correction).filter_by(pos_uid=row.pos_uid).order_by(Correction.uid.desc()).first()
	# 			return_dict['currentStatementText'] = db_correction.text if db_correction else db_last_position.text
	# 			return_dict['status'] = '0'
	# 		else:
	# 			logger('QueryHelper', 'get_data_for_one_step_back', 'last statement was an argument with uid : ' + str(row.arg_uid))
	# 			return_dict = self.get_args_for_new_round(user, row.arg_uid)
	# 			return_dict['status'] = '1'
	#
	# 	logger('QueryHelper', 'get_data_for_one_step_back', 'finished')
	# 	return return_dict

	def get_track_for_user(self, user):
		"""
		Returns the complete track of given user
		:param user: current user id
		:return: track os the user id as dict
		ödictionary
		"""
		logger('QueryHelper', 'get_track_for_user', 'user ' + user)
		db_user = DBSession.query(User).filter_by(nickname=user).first()

		if db_user:
			db_track = DBSession.query(Track).filter_by(author_uid=db_user.uid).all()
			return_dict = collections.OrderedDict()
			for track in db_track:
				logger('QueryHelper','get_track_for_user','track uid ' + str(track.uid))

				try:
					# Todo this can be optimized with joins ?
					db_statement = DBSession.query(Statement).filter_by(uid=track.statement_uid).first()
					tmp_dict = DictionaryHelper().save_statement_row_in_dictionary(db_statement)
					track_dict = dict()
					track_dict['uid'] = str(track.uid)
					track_dict['statement_uid'] = str(track.statement_uid)
					track_dict['timestamp'] = str(track.timestamp)
					track_dict['text'] = str(tmp_dict['text'])
					return_dict[track.uid] = track_dict
				except AttributeError as ae:
					logger('>>> QueryHelper <<<', 'get_track_for_user', 'ATTRIBUTE ERROR uid ' + str(ae))

			else:
				logger('QueryHelper', 'get_track_for_user', 'no track')
		else:
			return_dict = dict()
			logger('QueryHelper', 'get_track_for_user', 'no user')

		return return_dict

	def del_track_for_user(self, transaction, user):
		"""
		Returns the complete track of given user
		:param DBSession: current session
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'del_track_for_user','user ' + str(db_user.uid))
		DBSession.query(Track).filter_by(author_uid=db_user.uid).delete()
		transaction.commit()


	def set_statement(self, transaction, statement, user, isStart):
		"""
		Saves position for user
		:param transaction: current transaction
		:param statement: given statement
		:param user: given user
		:param isStart: if it is a start statement
		:return: '1'
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_argument_for_user', 'user: ' + str(user) + 'user_id: ' + str(db_user.uid) + ', statement: ' + str(statement))

		# add the version
		textversion = TextVersion(content=statement, author=db_user.uid, weight=0)
		DBSession.add(textversion)
		DBSession.flush()

		# add a new cache
		textvalue = TextValue(textversion=textversion.uid)
		DBSession.add(textvalue)
		DBSession.flush()
		textversion.set_textvalue(textvalue.uid)

		# add the statement
		statement = Statement(text=textvalue.uid, isstartpoint=isStart)
		DBSession.add(statement)
		DBSession.flush()

		# get the new statement
		new_statement = DBSession.query(Statement).filter_by(text_uid=textvalue.uid).order_by(Statement.uid.desc()).first()

		transaction.commit()
		return DictionaryHelper().save_statement_row_in_dictionary(new_statement)

	# def set_new_arguments(self, transaction, params, user):
	# 	"""
	# 	Saves arguments for user
	# 	:param transaction: current transaction
	# 	:param params: self.request.params with pro and con keys as well as values
	# 	:param user: given user
	# 	:return: dictionary of the new arguments
	# 	"""
	#
	# 	# get author and last selected statement
	# 	db_user = DBSession.query(User).filter_by(nickname=user).first()
	# 	db_user_uid = db_user.uid
	# 	db_last_statement = DBSession.query(Track).filter_by(user_uid=db_user.uid).order_by(Track.uid.desc()).first()
	# 	is_argument = db_last_statement.is_argument
	# 	last_statement_uid = db_last_statement.arg_uid if is_argument else db_last_statement.pos_uid
	#
	# 	text = 'last tracked statement of user ' + user + '(uid ' + str(db_user_uid) + ') is '
	# 	if db_last_statement:
	# 		text += 'argument' if is_argument else 'position' + ', uid ' + str(last_statement_uid)
	# 	else:
	# 		text += 'empty'
	# 		return_dict = dict()
	# 		return_dict['status'] = '-1'
	# 		return return_dict
	#
	# 	logger('QueryHelper', 'set_new_arguments', text)
	#
	# 	return_dict = dict()
	# 	all_arguments_dict = dict()
	# 	for key in params:
	# 		value = str(params[key])
	# 		logger('QueryHelper', 'set_new_arguments', '====================================')
	# 		logger('QueryHelper', 'set_new_arguments', 'argument will be added: (' + str(key) + ') ' + value)
	# 		# set argument
	# 		new_argument = Argument(text=value, weight=0)
	# 		new_argument.author = db_user_uid
	# 		DBSession.add(new_argument)
	# 		transaction.commit()
	#
	# 		# check if it was added
	# 		is_supportive = key.startswith('pro')
	# 		db_new_argument = DBSession.query(Argument).filter_by(text=value).order_by(Argument.uid.desc()).first()
	# 		uid = db_new_argument.uid
	# 		text = 'did db request whether the new argument was added: uid ' + str(uid) + ', support ' + str(is_supportive)
	# 		logger('QueryHelper', 'set_new_arguments', text)
	#
	# 		# save the argument
	# 		additional_key = 'is_supportive'
	# 		additional_value = '1' if is_supportive else '0'
	# 		argument_dict = DictionaryHelper().save_corrected_statement_row_in_dictionary(db_new_argument, True, additional_key, additional_value)
	# 		all_arguments_dict[str(argument_dict['uid'])] = argument_dict
	#
	# 		# set relation to the last selected statement
	# 		# case 1. last statement is argument + support relation
	# 		# case 2. last statement is argument +  attack relation
	# 		# case 3. last statement is position + support relation
	# 		# case 4. last statement is position +  attack relation
	#
	# 		if is_argument:
	# 			text = 'set relation: last statement is argument, ' + ('support' if is_supportive else 'attack') + ' relation'
	# 			new_relation = RelationArgArg(weight=0, is_supportive=is_supportive)
	# 			new_relation.arg_uid1 = uid
	# 			new_relation.arg_uid2 = last_statement_uid
	# 			DBSession.add(new_relation)
	# 			new_relation.author = db_user_uid
	# 			transaction.commit()
	#
	# 		elif not is_argument:
	# 			text = 'set relation: last statement is position, ' + ('support' if is_supportive else 'attack')  + ' relation'
	# 			new_relation = RelationArgPos(weight=0, is_supportive=is_supportive)
	# 			new_relation.arg_uid = uid
	# 			new_relation.pos_uid = last_statement_uid
	# 			new_relation.author = db_user_uid
	# 			DBSession.add(new_relation)
	# 			transaction.commit()
	#
	# 		else:
	# 			text = 'relation is unknown'
	#
	# 		logger('QueryHelper', 'set_new_arguments', text)
	#
	# 		return_dict['status'] = '1'
	#
	# 	return_dict['arguments'] = all_arguments_dict
	#
	# 	return return_dict

	# def is_statement_already_in_database(self, statement_text, is_position):
	# 	"""
	# 	Checks whether the given statement is already inserted
	# 	:param statement_text: text for the check
	# 	:param is_position: true, if it is a position
	# 	:return: >0, if it was already inserted, -1 otherwise
	# 	"""
	# 	if is_position:
	# 		db_statement = DBSession.query(Position).filter_by(text=statement_text).order_by(Position.uid.desc()).first()
	# 	else:
	# 		db_statement = DBSession.query(Argument).filter_by(text=statement_text).order_by(Argument.uid.desc()).first()
	#
	# 	if not db_statement:
	# 		db_statement = DBSession.query(Correction).filter_by(text=statement_text).order_by(Correction.uid.desc()).first()
	#
	# 	logger('QueryHelper', 'is_statement_already_in_database', 'new statement is already' if db_statement else 'not in the db')
	# 	return db_statement.uid if db_statement else -1

	def save_track_for_user(self, transaction, user, statememt_id):
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param statememt_id: id of the clicked statement
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid)+ ', statememt_uid: ' + str(
			statememt_id))
		new_track = Track(user=db_user.uid, statement=statememt_id)
		DBSession.add(new_track)
		transaction.commit()


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
