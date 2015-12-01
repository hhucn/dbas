import random

from cryptacular.bcrypt import BCRYPTPasswordManager
from .database import DBDiscussionSession
from .database.discussion_model import User, Group
from .logger import logger
from .strings import Translator

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
			db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nick)).first()
			db_user.update_last_action()
			transaction.commit()

	def is_user_admin(self, user):
		"""
		Check, if the given uid has admin rights or is admin
		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
		logger('UserHandler', 'is_user_admin', 'check for current user')
		if db_user:
			logger('UserHandler', 'is_user_admin', 'user exists; check for admin')
			if db_user.group_uid == db_admin_group.uid:
				logger('UserHandler', 'is_user_admin', 'user is admin')
				return True

		return False

	def is_user_author(self, user):
		"""
		Check, if the given uid has admin rights or is admin
		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
		db_author_group = DBDiscussionSession.query(Group).filter_by(name='authors').first()
		logger('UserHandler', 'is_user_author', 'check for current user')
		if db_user:
			logger('UserHandler', 'is_user_author', 'user exists; check for author (or admin)')
			if db_author_group.uid == db_admin_group.uid or db_user.group_uid == db_admin_group.uid:
				logger('UserHandler', 'is_user_author', 'user is author (or admin)')
				return True

		return False

	def get_random_anti_spam_question(self, lang):
		"""

		:return:
		"""
		_t = Translator(lang)

		int1 = random.randint(0,9)
		int2 = random.randint(0,9)
		answer = 0
		question = _t.get('antispamquestion') + ' '
		sign = _t.get('signs')[random.randint(0,3)]


		if sign is '+':
			sign = _t.get(sign)
			answer = int1 + int2

		elif sign is '-':
			sign = _t.get(sign)
			if int2 > int1:
				tmp = int2
				int2 = int1
				int1 = tmp
			answer = int1 - int2

		elif sign is '*':
			sign = _t.get(sign)
			answer = int1 * int2

		elif sign is '/':
			sign = _t.get(sign)
			answer = int1 / int2
			while int1 % int2 != 0 or int1 == 0 or int2 == 0:
				int1 = random.randint(1,9)
				int2 = random.randint(1,9)


		question += _t.get(str(int1)) + ' ' + sign + ' '+ _t.get(str(int2)) + '?'
		logger('UserHandler', 'get_random_anti_spam_question', 'question: ' + question)
		logger('UserHandler', 'get_random_anti_spam_question', 'answer: ' + str(answer))

		return question, answer