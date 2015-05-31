import logging
import random
import smtplib
import collections
import json

from socket import error as socket_error

from cryptacular.bcrypt import BCRYPTPasswordManager
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from sqlalchemy import and_

from .database import DBSession
from .database.model import Argument, RelationArgPos


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
		message = Message( subject=subject, sender=systemmail, recipients =[email], body=body)
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

	def get_all_arguments_for_by_pos_uid(self, uid, is_supportive):
		"""
		Getting every pro/con argument, which is connected to the given position uid
		:param uid: uid of the argument
		:param is_supportive: true, if all supportive arguments should be fetched
		:return: ordered dictionary
		"""

		## raw query
		# select * from arguments where uid in (
		# 	select arg_uid from relation_argpos where pos_uid=UID and is_supportive = 1
		# );
		## tried sql query
		# db_arguments = DBSession.query(Argument).filter_by(Argument.uid.in_(
		# 	DBSession.query(RelationArgPos).options(load_only("arg_uid")).filter(
		# 	and_(RelationArgPos.pos_uid == uid, RelationArgPos.is_supportive == 1)).all()
		# ))

		return_dict = collections.OrderedDict()
		logger('QueryHelper', 'get_all_arguments_for_uid', 'check for uid')
		support = 1 if is_supportive else 0

		if uid:
			logger('QueryHelper', 'get_all_arguments_for_uid ', 'send uid ' + str(uid))
			db_arguid = DBSession.query(RelationArgPos).filter(
				and_(RelationArgPos.pos_uid == uid, RelationArgPos.is_supportive == support)).all()

			all_uids = ' '
			for arg in db_arguid:
				all_uids += str(arg.arg_uid) + ' '
			logger('QueryHelper','get_all_arguments_for_uid',  'arg_uids' + all_uids)

			logger('QueryHelper', 'get_all_arguments_for_uid', 'iterate all arguments for that uid')
			for arg in db_arguid:
				logger('QueryHelper', 'get_all_arguments_for_uid' , 'get argument with' + str(arg.arg_uid))
				db_argument = DBSession.query(Argument).filter_by(uid = arg.arg_uid).first()

				logger('QueryHelper', 'get_all_arguments_for_uid', 'checks whether argument exists, uid ' + str(arg.uid))
				if db_argument:
					logger('QueryHelper', 'get_all_arguments_for_uid' , 'add argument in dict' +
						'uid:' + str(db_argument.uid) + '	val: ' + db_argument.text)
					return_dict[str(db_argument.uid)] = db_argument.text
				else :
					logger('QueryHelper', 'get_all_arguments_for_uid', 'no argument exists, uid ' + str(uid))
		else:
			logger('QueryHelper', 'get_all_arguments_for_uid', 'ERROR: uid not found')

		return return_dict

	def get_all_arguments_for_by_arg_uid(self, uid, is_supportive):
		"""
		Getting every pro/con arument, which is for/against the same position as the given argument uid
		:param uid: uid of the argument
		:param isSupportive: true, if all supportive arguments should be fetched
		:return: ordered dictionary
		"""

		# # raw query
		# select * from arguments where uid in (
		#	select arg_uid from relation_argpos where pos_uid in (
		#	  select pos_uid from relation_argpos where arg_uid = 3 and is_supportive = 1
		#	) and is_supportive = 0
		# );

		return_dict = collections.OrderedDict()
		logger('QueryHelper', 'get_all_arguments_for_by_arg_uid', 'check for uid')
		support = 1 if is_supportive else 0
		was_suportive = 0 if is_supportive else 1

		if uid:
			logger('QueryHelper', 'get_all_arguments_for_by_arg_uid ', 'get connected position for argument uid ' + str(uid))
			db_posuid = DBSession.query(RelationArgPos).filter(
				and_(RelationArgPos.arg_uid == uid, RelationArgPos.is_supportive == was_suportive)).first()

			if db_posuid:
				logger('QueryHelper', 'get_all_arguments_for_by_arg_uid',  'get all arguments from the opposite for position uid ' + str(
					db_posuid.pos_uid))
				db_arguids = DBSession.query(RelationArgPos).filter(
					and_(RelationArgPos.pos_uid == db_posuid.pos_uid, RelationArgPos.is_supportive == support)).all()

				logger('QueryHelper', 'get_all_arguments_for_by_arg_uid', 'iterate all arguments for that uid')
				for argid in db_arguids:
					logger('QueryHelper', 'get_all_arguments_for_by_arg_uid' , 'get argument with' + str(argid.arg_uid))
					db_argument = DBSession.query(Argument).filter_by(uid = argid.arg_uid).first()

					logger('QueryHelper', 'get_all_arguments_for_by_arg_uid', 'checks whether argument exists, uid ' + str(argid.uid))
					if db_argument:
						logger('QueryHelper', 'get_all_arguments_for_by_arg_uid' , 'add argument in dict' +
							'uid:' + str(db_argument.uid) + '	val: ' + db_argument.text)
						return_dict[str(db_argument.uid)] = db_argument.text
					else:
						logger('QueryHelper', 'get_all_arguments_for_by_arg_uid', 'no argument exists, uid ' + str(argid.uid))
			else:
				logger('QueryHelper', 'get_all_arguments_for_by_arg_uid', 'no argument exists, uid ' + str(uid))

		else:
			logger('QueryHelper', 'get_all_arguments_for_by_arg_uid', 'ERROR: uid not found')

		return return_dict

	def get_next_arg_for_confrontation(self, uid):
		"""

		:param uid:
		:return:
		"""
		return_dict = collections.OrderedDict()

		if uid:
			logger('QueryHelper', 'get_next_arg_for_confrontation', 'uid ' + str(uid))
			# todo: get_next_arg_for_confrontation

		else:
			logger('QueryHelper', 'get_next_arg_for_confrontation', 'ERROR: uid not found')

		return return_dict

	def get_next_args_for_justification(self, uid):
		"""

		:param uid:
		:return:
		"""
		return_dict = collections.OrderedDict()

		if uid:
			logger('QueryHelper', 'get_next_args_for_justification', 'uid ' + str(uid))
			# todo: get_next_args_for_justification

		else:
			logger('QueryHelper', 'get_next_args_for_justification', 'ERROR: uid not found')

		return return_dict

	def save_track_for_user(self, arg_uid, user):
		"""

		:param arg_uid:
		:param user:
		:return:
		"""
		logger('QueryHelper', 'save_track_for_user', 'arg_uid ' + str(arg_uid) + ', user' + str(user))


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
