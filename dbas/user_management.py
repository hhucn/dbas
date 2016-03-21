import random
import hashlib
import urllib

from datetime import datetime
from cryptacular.bcrypt import BCRYPTPasswordManager
from .database import DBDiscussionSession
from .database.discussion_model import User, Group, VoteStatement, VoteArgument, TextVersion
from .logger import logger

from .strings import Translator

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


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

		for i in range(pw_len // 3):
			pwlist.append(alphabet[random.randrange(len(alphabet))])
			pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
			pwlist.append(str(random.randrange(10)))
		for i in range(pw_len - len(pwlist)):
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

	def __init__(self):
		self.timeout = 1800

	def update_last_action(self, transaction, nick):
		"""

		:param nick:
		:return:
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nick)).first()
		if db_user:
			last_action_object = datetime.strptime(str(db_user.last_action), '%Y-%m-%d %H:%M:%S')
			diff = (datetime.now() - last_action_object).seconds - 3600  # TODO dirty fix
			log_out = diff > self.timeout
			logger('UserHandler', 'update_last_action', 'session run out: ' + str(log_out) + ', ' + str(diff) + 's')
			db_user.update_last_action()
			db_user.should_hold_the_login(not log_out)
			transaction.commit()
			return log_out
		return False

	def is_user_admin(self, user):
		"""
		Check, if the given uid has admin rights or is admin
		:param user: current user name
		:return: true, if user is admin, false otherwise
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
		db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
		logger('UserHandler', 'is_user_admin', 'main')
		if db_user:
			if db_user.group_uid == db_admin_group.uid:
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
		gravatar_url += urllib.parse.urlencode({'d': 'wavatar', 's': str(80)})
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
		logger('UserHandler', 'is_user_author', 'main')
		if db_user:
			if db_author_group.uid == db_admin_group.uid or db_user.group_uid == db_admin_group.uid:
				return True

		return False

	def is_user_logged_in(self, user):
		"""
		Checks if the user is logged in
		:param user: current user name
		:return: user or None
		"""
		return True if DBDiscussionSession.query(User).filter_by(nickname=str(user)).first() else False

	def get_random_anti_spam_question(self, lang):
		"""
		Returns a random math question
		:param lang: string
		:return: question, answer
		"""
		_t = Translator(lang)

		int1 = random.randint(0, 9)
		int2 = random.randint(0, 9)
		answer = 0
		question = _t.get(_t.antispamquestion) + ' '
		sign = _t.get(_t.signs)[random.randint(0, 3)]

		if sign is '+':
			sign = _t.get(sign)
			answer = int1 + int2

		elif sign is '-':
			sign = _t.get(sign)
			if int2 > int1:
				tmp = int1
				int1 = int2
				int2 = tmp
			answer = int1 - int2

		elif sign is '*':
			sign = _t.get(sign)
			answer = int1 * int2

		elif sign is '/':
			sign = _t.get(sign)
			while int1 == 0 or int2 == 0 or int1 % int2 != 0:
				int1 = random.randint(1, 9)
				int2 = random.randint(1, 9)
			answer = int1 / int2

		question += _t.get(str(int1)) + ' ' + sign + ' ' + _t.get(str(int2)) + '?'
		logger('UserHandler', 'get_random_anti_spam_question', 'question: ' + question + ', answer: ' + str(answer))

		return question, str(answer)

	def get_count_of_statements_of_user(self, user, only_edits):
		"""

		:param user:
		:param only_edits:
		:return:
		"""
		if not user:
			return 0

		edit_count = 0
		statement_count = 0
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(author_uid=user.uid).all()

		for tv in db_textversions:
			db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=tv.statement_uid).first()
			if db_root_version.uid < tv.uid:
				edit_count += 1
			else:
				statement_count +=1

		return edit_count if only_edits else statement_count

	def get_count_of_votes_of_user(self, user):
		"""

		:param user:
		:return:
		"""
		if not user:
			return 0
		arg_votes = len(DBDiscussionSession.query(VoteArgument).filter_by(author_uid=user.uid).all())
		stat_votes = len(DBDiscussionSession.query(VoteStatement).filter_by(author_uid=user.uid).all())
		return arg_votes, stat_votes

	def get_statements_of_user(self, user, lang):
		"""

		:param user:
		:param lang:
		:return:
		"""
		return_array = []

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return return_array

		db_edits = DBDiscussionSession.query(TextVersion).filter_by(author_uid=db_user.uid).all()

		for edit in db_edits:
			db_root_version = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=edit.statement_uid).first()
			if db_root_version.uid == edit.uid:
				edit_dict = dict()
				edit_dict['uid'] = str(edit.uid)
				edit_dict['statement_uid'] = str(edit.statement_uid)
				edit_dict['content'] = str(edit.content)
				edit_dict['timestamp'] = str(edit.timestamp)
				return_array.append(edit_dict)

		return return_array

	def get_edits_of_user(self, user, lang, query_helper):
		"""

		:param user:
		:param lang:
		:param query_helper:
		:return:
		"""
		return_array = []

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return return_array

		db_edits = DBDiscussionSession.query(TextVersion).filter_by(author_uid=db_user.uid).all()

		for edit in db_edits:
			edit_dict = dict()
			edit_dict['uid'] = str(edit.uid)
			edit_dict['statement_uid'] = str(edit.statement_uid)
			edit_dict['content'] = str(edit.content)
			edit_dict['timestamp'] = query_helper.sql_timestamp_pretty_print(str(edit.timestamp), lang)
			return_array.append(edit_dict)

		return return_array

	def get_votes_of_user(self, user, is_argument, lang, query_helper):
		"""

		:param user:
		:param is_argument:
		:param lang:
		:param query_helper:
		:return:
		"""
		return_array = []

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return return_array

		_qh = query_helper

		if is_argument:
			db_votes = DBDiscussionSession.query(VoteArgument).filter_by(author_uid=db_user.uid).all()
		else:
			db_votes = DBDiscussionSession.query(VoteStatement).filter_by(author_uid=db_user.uid).all()

		for vote in db_votes:
			vote_dict = dict()
			vote_dict['uid'] = str(vote.uid)
			vote_dict['timestamp'] = _qh.sql_timestamp_pretty_print(str(vote.timestamp), lang)
			vote_dict['is_up_vote'] = str(vote.is_up_vote)
			vote_dict['is_valid'] = str(vote.is_valid)
			if is_argument:
				vote_dict['argument_uid'] = str(vote.argument_uid)
				vote_dict['text'] = _qh.get_text_for_argument_uid(vote.argument_uid, lang)
			else:
				vote_dict['statement_uid'] = str(vote.statement_uid)
				vote_dict['text'] = _qh.get_text_for_statement_uid(vote.statement_uid)
			return_array.append(vote_dict)

		return return_array

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
		logger('UserHandler', 'change_password', 'def')
		_t = Translator(lang)

		error = False
		success = False

		# is the old password given?
		if not old_pw:
			logger('UserHandler', 'change_password', 'old pwd is empty')
			message = _t.get(_t.oldPwdEmpty) # 'The old password field is empty.'
			error = True
		# is the new password given?
		elif not new_pw:
			logger('UserHandler', 'change_password', 'new pwd is empty')
			message = _t.get(_t.newPwdEmtpy) # 'The new password field is empty.'
			error = True
		# is the confirmation password given?
		elif not confirm_pw:
			logger('UserHandler', 'change_password', 'confirm pwd is empty')
			message = _t.get(_t.confPwdEmpty) # 'The password confirmation field is empty.'
			error = True
		# is new password equals the confirmation?
		elif not new_pw == confirm_pw:
			logger('UserHandler', 'change_password', 'new pwds not equal')
			message = _t.get(_t.newPwdNotEqual) # 'The new passwords are not equal'
			error = True
		# is new old password equals the new one?
		elif old_pw == new_pw:
			logger('UserHandler', 'change_password', 'pwds are the same')
			message = _t.get(_t.pwdsSame) # 'The new and old password are the same'
			error = True
		else:
			# is the old password valid?
			if not user.validate_password(old_pw):
				logger('UserHandler', 'change_password', 'old password is wrong')
				message = _t.get(_t.oldPwdWrong) # 'Your old password is wrong.'
				error = True
			else:
				password_handler = PasswordHandler()
				hashed_pw = password_handler.get_hashed_password(new_pw)

				# set the hased one
				user.password = hashed_pw
				DBDiscussionSession.add(user)
				transaction.commit()

				logger('UserHandler', 'change_password', 'password was changed')
				message = _t.get(_t.pwdChanged)  # 'Your password was changed'
				success = True

		return message, error, success

	def get_all_users(self, user):
		"""
		Returns all users, if the given user is admin
		:param user: self.request.authenticated_userid
		:return: dictionary
		"""
		is_admin = UserHandler().is_user_admin(user)
		if not is_admin:
			return_dict = dict()
		else:
			logger('UserHandler', 'get_all_users', 'get all users')
			db_users = DBDiscussionSession.query(User).join(Group).all()

			return_dict = dict()

			if db_users:
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
					return_dict[user.uid] = return_user
		return return_dict
