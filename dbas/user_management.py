import random
import hashlib
import urllib

from cryptacular.bcrypt import BCRYPTPasswordManager
from .database import DBDiscussionSession
from .database.discussion_model import User, Group
from .logger import logger
from .strings import Translator

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

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
		if nick is not None: # todo: catch none user
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

	def get_profile_picture(self, user):
		"""
		Returns the url to a https://secure.gravatar.com picture, with the option wavatar and size of 80px
		:param user: User
		:return:
		"""
		email = user.email.encode('utf-8') if user else 'unknown@dbas.cs.uni-duesseldorf.de'.encode('utf-8')
		gravatar_url = 'https://secure.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + "?"
		gravatar_url += urllib.parse.urlencode({'d':'wavatar', 's':str(80)})
		logger('UserHandler', 'get_profile_picture', 'url: ' + gravatar_url)
		return gravatar_url

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

	def is_user_logged_in(self, user):
		"""
		Checks if the user is logged in
		:param user: current user name
		:return: user or None
		"""
		return DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()


	def get_random_anti_spam_question(self, lang):
		"""
		Returns a random math question
		:param lang: string
		:return: question, answer
		"""
		_t = Translator(lang)

		int1 = random.randint(0,9)
		int2 = random.randint(0,9)
		answer = 0
		question = _t.get(_t.antispamquestion) + ' '
		sign = _t.get(_t.signs)[random.randint(0,3)]

		if sign is '+':
			sign = _t.get(sign)
			answer = int1 + int2

		elif sign is '-':
			sign = _t.get(sign)
			answer = int2 - int1 if int2 > int1 else int1 - int2

		elif sign is '*':
			sign = _t.get(sign)
			answer = int1 * int2

		elif sign is '/':
			sign = _t.get(sign)
			while int1 == 0 or int2 == 0 or int1 % int2 != 0:
				int1 = random.randint(1,9)
				int2 = random.randint(1,9)
			answer = int1 / int2

		question += _t.get(str(int1)) + ' ' + sign + ' '+ _t.get(str(int2)) + '?'
		logger('UserHandler', 'get_random_anti_spam_question', 'question: ' + question)
		logger('UserHandler', 'get_random_anti_spam_question', 'answer: ' + str(answer))

		return question, answer

	def change_password(self, transaction, user, old_pw, new_pw, confirm_pw, lang):
		"""

		:param transaction: current database transaction
		:param user: current database user
		:param old_pw: old received password
		:param new_pw: new received password
		:param confirm_pw: confirmation of the password
		:param lang: current language
		:return: an message and boolean for error and success
		"""
		logger('DatabaseHelper', 'change_password', 'def')
		_t = Translator(lang)

		error = False
		success = False

		# is the old password given?
		if not old_pw:
			logger('DatabaseHelper', 'change_password', 'old pwd is empty')
			message = _t.get(_t.oldPwdEmpty) # 'The old password field is empty.'
			error = True
		# is the new password given?
		elif not new_pw:
			logger('DatabaseHelper', 'change_password', 'new pwd is empty')
			message = _t.get(_t.newPwdEmtpy) # 'The new password field is empty.'
			error = True
		# is the cofnrimation password given?
		elif not confirm_pw:
			logger('DatabaseHelper', 'change_password', 'confirm pwd is empty')
			message = _t.get(_t.confPwdEmpty) # 'The password confirmation field is empty.'
			error = True
		# is new password equals the confirmation?
		elif not new_pw == confirm_pw:
			logger('DatabaseHelper', 'change_password', 'new pwds not equal')
			message = _t.get(_t.newPwdNotEqual) # 'The new passwords are not equal'
			error = True
		# is new old password equals the new one?
		elif old_pw == new_pw:
			logger('DatabaseHelper', 'change_password', 'pwds are the same')
			message = _t.get(_t.pwdsSame) # 'The new and old password are the same'
			error = True
		else:
			# is the old password valid?
			if not user.validate_password(old_pw):
				logger('DatabaseHelper', 'change_password', 'old password is wrong')
				logger('DatabaseHelper', 'old', old_pw + " " + PasswordHandler().get_hashed_password(old_pw))
				logger('DatabaseHelper', 'new', new_pw + " " + PasswordHandler().get_hashed_password(new_pw))
				logger('DatabaseHelper', 'current', user.password)
				message = _t.get(_t.oldPwdWrong) # 'Your old password is wrong.'
				error = True
			else:
				logger('DatabaseHelper', 'form.passwordrequest.submitted', 'new password is ' + new_pw)
				password_handler = PasswordHandler()
				hashed_pw = password_handler.get_hashed_password(new_pw)
				logger('DatabaseHelper', 'form.passwordrequest.submitted', 'New hashed password is ' + hashed_pw)

				# set the hased one
				user.password = hashed_pw
				DBDiscussionSession.add(user)
				transaction.commit()

				logger('DatabaseHelper', 'change_password', 'password was changed')
				message = _t.get(_t.pwdChanged) # 'Your password was changed'
				success = True

		return message, error, success

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