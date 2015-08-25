import logging
import random
from cryptacular.bcrypt import BCRYPTPasswordManager
from .database import DBSession
from .database.model import User, Group, Track, Premisse

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

	def save_track_for_user(self, transaction, user, statement_id, premissesgroup_uid, argument_uid, attacked_by_relation, attacked_with_relation): # TODO
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