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
from .database.model import Argument, RelationArgPos, RelationArgArg, Track, User, Group, Position


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

	def send_password_to_email(self, request, password):
		"""
		Checks, for a valid email in the request, generats, sends and updates a new password
		:param request: current request
		:params password: the new password
		:return: message
		"""
		email = request.params['email']

		subject = 'D-BAS Password Request'
		systemmail = 'krauthoff@cs.uni-duesseldorf.de'
		body = 'Your new password is: ' + password
		logger('main_contact', 'form.contact.submitted', 'sending mail')
		mailer = get_mailer(request)
		message = Message(subject=subject, sender=systemmail, recipients =[email], body=body)
		send_error = False
		send_message = False
		# try sending an catching errors
		try:
			mailer.send_immediately(message, fail_silently=False)
			send_message = True
			message = 'A new password was send to ' + email
		except smtplib.SMTPConnectError as exception:
			logger('helper', 'send_password_to_email', 'error while sending')
			logger('helper', 'send_password_to_email', str(exception.smtp_code))
			logger('helper', 'send_password_to_email', str(exception.smtp_error))
			send_error = True
			message = 'A message could not be send due to a system error! (' \
						+ 'smtp_code ' + str(exception.smtp_code) + ' || smtp_error ' + str(exception.smtp_error) + ')'
		except socket_error as serr:
			logger('helper', 'send_password_to_email', 'error while sending')
			logger('helper', 'send_password_to_email', 'socket_error ' + str(serr))
			send_error = True
			message = 'A message could not be send due to a system error! (' + 'socket_error ' + str(serr) + ')'
		return message, send_message, send_error


class QueryHelper(object):

	def is_user_admin(self, uid):
		"""
		Check, if the given uid has admin rights or is admin
		:param uid:
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBSession.query(User).filter_by(nickname=str(uid)).first()
		db_group = DBSession.query(Group).filter_by(name='admins').first()
		logger('QueryHelper', 'is_user_admin', 'check for current user')
		if db_user:
			logger('QueryHelper', 'is_user_admin', 'user exists; check for admin')
			if db_user.nickname == 'admin' or db_user.group == db_group.uid:
				logger('QueryHelper', 'is_user_admin', 'user is admin')
				return True

		return False

	def get_all_arguments_by_arg_uid(self, uid, is_supportive):
		"""
		Getting every pro/con arument, which is for/against the same position as the given argument uid
		:param uid: uid of the argument
		:param is_supportive: true, if all supportive arguments should be fetched
		:return: ordered dictionary
		"""

		# # raw query
		# select * from arguments where uid in (
		# select arg_uid from relation_argpos where pos_uid in (
		# select pos_uid from relation_argpos where arg_uid = 3 and is_supportive = 1
		# ) and is_supportive = 0
		# );

		return_dict = collections.OrderedDict()
		logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'check for uid')
		support = 1 if is_supportive else 0
		was_suportive = 0 if is_supportive else 1

		if uid:
			logger('QueryHelper', 'get_all_arguments_by_arg_uid ', 'get connected position for argument uid ' + str(uid))
			db_posuid = DBSession.query(RelationArgPos).filter(
				and_(RelationArgPos.arg_uid == uid, RelationArgPos.is_supportive == was_suportive)).first()

			if db_posuid:
				logger('QueryHelper', 'get_all_arguments_by_arg_uid',  'get all arguments from the opposite for position uid ' + str(
					db_posuid.pos_uid))
				db_arguids = DBSession.query(RelationArgPos).filter(
					and_(RelationArgPos.pos_uid == db_posuid.pos_uid, RelationArgPos.is_supportive == support)).all()

				logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'iterate all arguments for that uid')
				for argid in db_arguids:
					logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'get argument with' + str(argid.arg_uid))
					db_argument = DBSession.query(Argument).filter_by(uid = argid.arg_uid).first()

					logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'checks whether argument exists, uid ' + str(argid.uid))
					if db_argument:
						logger('QueryHelper', 'get_all_arguments_by_arg_uid' , 'add argument in dict' +
							'uid:' + str(db_argument.uid) + ', val: ' + db_argument.text)
						return_dict[str(db_argument.uid)] = db_argument.text
					else:
						logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'no argument exists, uid ' + str(argid.uid))
			else:
				logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'no argument exists, uid ' + str(uid))

		else:
			logger('QueryHelper', 'get_all_arguments_by_arg_uid', 'ERROR: uid not found')

		return return_dict

	def get_args_for_new_round(self, user_id, statement_id, is_argument):
		"""
		Returns the next argument for a confrontation. This is based on the last given id.
		:param user_id: current user id, as given in the request params
		:param statement_id: current statement id
		:param is_argument: true, when the id is for an argument
		:return: dictionary with 'confrontation' <-> argument , the 'currentStatementText' <-> argument of the user and a justification
		dictionary with mapping uid <-> argument dictionary
		"""
		logger('QueryHelper', 'get_args_for_new_round', 'user ' + str(user_id)  + ', is_argument ' + str(is_argument) + ', statement id ' + str(statement_id))
		return_dict = collections.OrderedDict()
		justifications_dict = collections.OrderedDict()

		# get the last used statement
		if is_argument:
			db_last_statement = DBSession.query(Argument).filter_by(uid=statement_id).first()
		else:
			db_last_statement = DBSession.query(Position).filter_by(uid=statement_id).first()

		# save the last statement text in the return dictionary
		statement = 'argument' if is_argument else 'position'
		logger('QueryHelper', 'get_args_for_new_round', 'last statement is ' + statement + ': ' + db_last_statement.text)
		return_dict['currentStatementText'] = db_last_statement.text

		# get all statements against our statement
		if is_argument:
			contra_argument_rows = self.get_argument_list_in_relation_to_statement(statement_id, False, False)
			# pro_argument_rows = self.get_argument_list_in_relation_to_statement(statement_id, True, False)
		else:
			contra_argument_rows = self.get_argument_list_in_relation_to_statement(statement_id, False, True)
			# pro_argument_rows = self.get_argument_list_in_relation_to_statement(statement_id, True, True)

		# todo: what to do, when there is no argument for an confrontation?

		# pick a random contra argument and get all arguments against the confrontation argument
		if len(contra_argument_rows) > 0:
			rnd = randint(0,len(contra_argument_rows)-1)
			logger('QueryHelper', 'get_args_for_new_round', 'get the nth argument ' + str(rnd))
			return_dict['confrontation'] = contra_argument_rows[rnd]['text']
			confrontation_uid = contra_argument_rows[rnd]['uid']

			# get all arguments against the confrontation argument
			contra_argument_rows = self.get_argument_list_in_relation_to_statement(confrontation_uid, False, False)
		else :
			return_dict['confrontation'] = 'There is no contra argument!'


		# get all justifications
		for justification in contra_argument_rows:
			argument_dict = {}
			argument_dict['uid'] = justification['uid']
			argument_dict['text'] = justification['text']
			argument_dict['date'] = str(justification['date'])
			argument_dict['weight'] = str(justification['weight'])
			argument_dict['author'] = justification['author']
			justifications_dict[str(justification['uid'])] = argument_dict

		return_dict['justifications'] = justifications_dict
		return return_dict

	def is_statement_already_in_database(self, statement_text, is_position):
		"""
		Checks whether the given statement is already inserted
		:param statement_text: text for the check
		:param is_position: true, if it is a position
		:return: true, if it was already inserted
		"""
		if is_position:
			db_statement = DBSession.query(Position).filter_by(text=statement_text).first()
		else:
			db_statement = DBSession.query(Argument).filter_by(text=statement_text).first()

		if db_statement:
			logger('QueryHelper', 'is_statement_already_in_database', 'new statement is already in the db')
			return True
		else:
			logger('QueryHelper', 'is_statement_already_in_database', 'new statement is not in the db')
			return False

	def get_argument_list_in_relation_to_statement(self, uid, is_supportive, is_position):
		"""
		Returns every argument with a non-supportive connection to the given position
		:param pos_uid: uid of the position
		:param is_supportive: 1 if it is supportive, 0 otherwise
		:param is_position: true, if it is a position
		:return: list with arguments
		"""

		if is_position:
			# # raw query
			# select * from arguments where uid in (
			# select arg_uid from relation_argpos where pos_uid = 1 and is_supportive = 1
			# )
			logger('QueryHelper', 'get_arguments_in_relation_to_statement', 'pos_uid ' + str(uid) + ' support ' + str(is_supportive))
			db_arg_uids = DBSession.query(RelationArgPos).filter(and_(RelationArgPos.pos_uid == uid,
		                                                            RelationArgPos.is_supportive == is_supportive)).all()
		else:
			# # raw query
			# select * from arguments where uid in (
			# select arg_uid1 from relation_argarg where arg_uid2 = 7 and is_supportive = 0
			# )
			logger('QueryHelper', 'get_arguments_in_relation_to_statement', 'arg_uid2 ' + str(uid) + ' support ' + str(is_supportive))
			db_arg_uids = DBSession.query(RelationArgArg).filter(and_(RelationArgArg.arg_uid2 == uid,
		                                                            RelationArgArg.is_supportive == is_supportive)).all()

		return_list = []
		for arg in db_arg_uids:

			if is_position:
				logger('QueryHelper', 'get_arguments_against_position', 'connected ' + ('pro' if is_supportive else 'contra')
					+ ' argument ' + str(arg.arg_uid))
				db_arg = DBSession.query(Argument).filter_by(uid=arg.arg_uid).first()
			else:
				logger('QueryHelper', 'get_arguments_against_argument', 'connected ' + ('pro' if is_supportive else 'contra')
					+ ' argument ' + str(arg.arg_uid1))
				db_arg = DBSession.query(Argument).filter_by(uid=arg.arg_uid1).first()

			argument_dict = {}
			argument_dict['uid'] = db_arg.uid
			argument_dict['text'] = db_arg.text
			argument_dict['date'] = str(db_arg.date)
			argument_dict['weight'] = str(db_arg.weight)
			author = DBSession.query(User).filter_by(uid=db_arg.author).first()
			argument_dict['author'] = author.nickname
			return_list.append(argument_dict)

		return return_list

	def save_track_position_for_user(self, db_session, transaction, user, pos_id):
		"""

		:param db_session: current session
		:param transaction: current transaction
		:param user_id: authentication id of the user
		:param pos_id: id of the clicked position
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_position_for_user', 'user: ' + str(user) + ', user_uid: ' + str(db_user.uid)+ ', pos_uid: ' + str(
			pos_id))
		new_track = Track(user_uid=db_user.uid, pos_uid=pos_id, arg_uid=-1, is_argument=False)
		db_session.add(new_track)
		transaction.commit()

	def save_track_argument_for_user(self, db_session, transaction, user, arg_id):
		"""
		Saves track for user
		:param db_session: current session
		:param transaction: current transaction
		:param user_id: authentication id of the user
		:param arg_id: id of the clicked argument
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_argument_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid)+ ', arg_uid: ' + str(
			arg_id))
		new_track = Track(user_uid=db_user.uid, pos_uid=-1, arg_uid=arg_id, is_argument=True)
		db_session.add(new_track)
		transaction.commit()

	def get_track_for_user(self, db_session, user):
		"""
		Returns the complete track of given user
		:param db_session: current session
		:param user: current user id
		:return: track os the user id as dictionary
		"""
		logger('QueryHelper','get_track_for_user','user ' + user)
		db_user = DBSession.query(User).filter_by(nickname=user).first()

		db_track = db_session.query(Track).filter_by(user_uid=db_user.uid).all()
		return_dict = collections.OrderedDict()
		for track in db_track:
			logger('QueryHelper','get_track_for_user','track uid ' + str(track.uid) + ', user ' + str(track.user) + ', date ' + str(
				track.date) + ', pos_uid ' + str(track.pos_uid) + ', arg_uid ' + str(track.arg_uid) + ', is_arg ' + str(track.is_argument))

			track_dict = {}
			track_dict['date'] = str(track.date)
			track_dict['pos_uid'] = track.pos_uid
			track_dict['arg_uid'] = track.arg_uid
			if track.is_argument:
				db_row = db_session.query(Argument).filter_by(uid=track.arg_uid).first()
			else:
				db_row = db_session.query(Position).filter_by(uid=track.pos_uid).first()
			track_dict['text'] = db_row.text
			track_dict['is_argument'] = track.is_argument
			return_dict[track.uid] = track_dict
		else:
			logger('QueryHelper','get_track_for_user','no track')

		return return_dict

	def del_track_for_user(self, DBSession, transaction, user):
		"""
		Returns the complete track of given user
		:param DBSession: current session
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'del_track_for_user','user ' + db_user.uid)
		DBSession.query(Track).filter_by(user_uid=db_user.uid).delete()
		transaction.commit()

	def set_new_position(self, db_session, transaction, position, user):
		"""
		Saves position for user
		:param db_session: current session
		:param transaction: current transaction
		:param position: given position
		:param user: given user
		:return: dictionary of the new position
		"""
		return_dict = collections.OrderedDict()
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_argument_for_user', 'user: ' + str(user) + 'user_id: ' + str(db_user.uid)
		       + ', position: ' + str(position))

		# save position
		new_position = Position(text=position, weight=0)
		new_position.author = db_user.uid
		db_session.add(new_position)
		transaction.commit()

		# check out, if it is there
		db_position = DBSession.query(Position).filter_by(text=position).order_by(Position.uid.desc()).first()
		return_dict = {}
		if db_position:
			logger('QueryHelper', 'save_track_argument_for_user', 'position was inserted with uid ' + str(db_position.uid))
			return_dict['uid'] = db_position.uid
			return_dict['text'] = db_position.text
			return_dict['date'] = str(db_position.date)
			return_dict['weight'] = str(db_position.weight)
			return_dict['author'] = user
		else:
			logger('QueryHelper', 'save_track_argument_for_user', 'cannot get uid of position')

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
		return_dict = {}
		logger('helper', 'get_subdictionary_out_of_orderer_dict', 'count: ' + str(count))
		items = list(ordered_dict.items())
		for item in items:
			logger('helper', 'get_subdictionary_out_of_orderer_dict', 'all items: ' + ''.join(str(item)))
		if count < 0:
			return ordered_dict
		elif count == 1:
			if len(items) > 1:
				rnd = random.randint(0, len(items)-1)
				logger('helper', 'get_subdictionary_out_of_orderer_dict', 'return item at ' + str(rnd))
				return_dict[items[rnd][0]] = items[rnd][1]
			else:
				return ordered_dict
		else:

			for i in range(0, count):
				rnd = random.randint(0, len(items)-1)
				logger('helper', 'get_subdictionary_out_of_orderer_dict', 'for loop ' + str(i) + '. add element at ' + str(rnd))
				return_dict[items[rnd][0]] = items[rnd][1]
				items.pop(rnd)

		return return_dict

	def dictionarty_to_json_array(self, dict, ensure_ascii):
		"""
		Dumps given dictionary into json
		:param dict: dictionary for dumping
		:param ensure_ascii: if true, ascii will be checked
		:return: json data
		"""
		return_dict = json.dumps(dict, ensure_ascii)
		return return_dict
