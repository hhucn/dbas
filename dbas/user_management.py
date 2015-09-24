import random
from cryptacular.bcrypt import BCRYPTPasswordManager
from .database import DBSession
from .database.model import User, Group
from .logger import logger

class PasswordGenerator(object):

	# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
	def get_rnd_passwd(self):
		"""
		Generates a password with the length of 10 out of ([a-z][A-Z][+-*/#!*?])+
		:return: new secure password
		"""
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		upperalphabet = alphabet.upper()
		symbols = '+-*/#!*?'
		pw_len = 10
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
		"""

		:param password:
		:return:
		"""
		manager = BCRYPTPasswordManager()
		return manager.encode(password)


class UserHandler(object):

	def update_last_action(self, transaction, nick):
		"""

		:param transaction:
		:param nick:
		:return:
		"""
		if nick != None: # todo: catch none user
			db_user = DBSession.query(User).filter_by(nickname=str(nick)).first()
			db_user.update_last_action()
			transaction.commit()

	def is_user_admin(self, user):
		"""
		Check, if the given uid has admin rights or is admin
		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBSession.query(User).filter_by(nickname=str(user)).first()
		db_group = DBSession.query(Group).filter_by(name='admins').first()
		logger('UserHandler', 'is_user_admin', 'check for current user')
		if db_user:
			logger('UserHandler', 'is_user_admin', 'user exists; check for admin')
			if db_user.nickname == 'admin' or db_user.group_uid == db_group.uid:
				logger('UserHandler', 'is_user_admin', 'user is admin')
				return True

		return False