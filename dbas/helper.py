import logging
import random
import smtplib
from socket import error as socket_error

from cryptacular.bcrypt import BCRYPTPasswordManager
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from sqlalchemy import and_

from .database import DBSession
from .database.model import User, Group, Issue, Position, Argument, RelationArgPos


systemmail = 'dbas@cs.uni-duesseldorf.de'
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
		message = Message(subject=subject,
		                  sender=systemmail,
		                  recipients =[email],
		                  body=body
		                  )
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

	def get_all_arguments_for_uid(self, uid, isSupportive):
		"""
		todo
		:param uid: uid of the argument
		:param isSupportive: true, if all supportive arguments should be fetched
		:return:
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

		return_dict = {}
		logger('QueryHelper', 'get_all_arguments_for_uid', 'check for uid')
		support = 1 if isSupportive else 0
		if (uid):
			logger('QueryHelper', 'get_all_arguments_for_uid ', 'send uid ' + str(uid))
			db_arguid = DBSession.query(RelationArgPos).filter(
				and_(RelationArgPos.pos_uid == uid, RelationArgPos.is_supportive == support)).all()
			list_arg_ids = []

			all_uids = ' '
			for arg in db_arguid:
				all_uids += str(arg.arg_uid) + ' '
			logger('QueryHelper','get_all_arguments_for_uid',  'arg_uids' + all_uids)
			i = 0

			logger('QueryHelper', 'get_all_arguments_for_uid', 'iterate all arguemnts for that uid')
			for arg in db_arguid:
				logger('QueryHelper','get_all_arguments_for_uid', 'current arg_uids' + str(arg.arg_uid))
				if arg.uid not in list_arg_ids:
					logger('QueryHelper', 'get_all_arguments_for_uid' , 'get argument with' + str(arg.arg_uid))
					list_arg_ids.append(arg.arg_uid)
					db_argument = DBSession.query(Argument).filter_by(uid = arg.arg_uid).first()

					logger('QueryHelper', 'get_all_arguments_for_uid', 'checks whether argument exists, uid ' + str(arg.uid))
					if (db_argument):
						logger('QueryHelper', 'get_all_arguments_for_uid' , 'add argument in dict' +
					       'uid:' + str(db_argument.uid) + '   val: ' + db_argument.text)
						return_dict[str(db_argument.uid)] = db_argument.text
						i += 1
					else :
						logger('QueryHelper', 'get_all_arguments_for_uid', 'no argument exists, uid ' + str(arg.uid))
		else:
			logger('QueryHelper', 'get_all_arguments_for_uid', 'ERROR: uid not found')

		return return_dict