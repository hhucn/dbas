import random
from sqlalchemy import and_
import collections

from .database import DBSession
from .database.model import Argument, Statement, Track, User, TextValue, TextVersion, Premisse, PremisseGroup, Relation
from .logger import logger

class QueryHelper(object):
	"""

	"""

	def set_statements_as_premisse(self, statement, user):
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

	def get_relation_uid_by_name(self, relation_name):
		"""

		:param relation_name:
		:return:
		"""
		db_relation = DBSession.query(Relation).filter_by(name=relation_name).first()
		logger('DatabaseHelper', 'get_relation_uid_by_name', 'return ' + str(db_relation.name if db_relation else -1))
		return db_relation.uid if db_relation else -1

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
		logger('QueryHelper', 'get_text_for_argument_uid', 'uid ' + str(uid))
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
			return_dict[key + str(index) + 'id'] = relation.premissesGroup_uid
			#return_dict[key + str(index) + 'id'] = ','.join(uids)
		return_dict[key] = str(len(db_relation))
		return return_dict

	def get_attack_for_argument_uid_by_relation(self, argument_uid, relation, key):
		"""

		:param argument_uid:
		:param relation:
		:param key:
		:return:
		"""
		status = '1'
		if 'undermine' in relation.lower():
			return_dict = self.get_undermines_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		elif 'support' in relation.lower():
			return_dict = self.get_supports_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		elif 'undercut' in relation.lower():
			return_dict = self.get_undercuts_for_argument_uid(key, argument_uid)
			type = 'statement'
		elif 'overbid' in relation.lower():
			return_dict = self.get_overbids_for_argument_uid(key, argument_uid)
			type = 'statement'
		elif 'rebut' in relation.lower():
			return_dict = self.get_rebuts_for_argument_uid(key, argument_uid)
			type = 'premissesgroup'
		else:
			return_dict = {}
			type = 'none'
			status = '-1'
		return return_dict, type, status

	def get_attack_for_argument_by_random(self, db_argument):
		"""
		Returns a dictionary with attacks. The attack itself is random.
		if rnd is equal 0, get_undermines_for_argument_uid(...) is called
		if rnd is equal 1, get_rebuts_for_argument_uid(...) is called
		if rnd is equal 2, get_undercuts_for_argument_uid(...) is called
		Additionally returns id's of premisses groups with [key + str(index) + 'id']
		:param argument_uid:
		:param key:
		:return: dict, key
		"""
		rnd = random.randrange(0, 3 if db_argument else 2)
		startrnd = rnd
		dict = None
		key = ''

		# randomize at least 1, maximal 3 times for getting an attack
		while True:
			logger('QueryHelper', 'get_attack_for_argument_by_random', 'random attack is ' + str(rnd))
			if rnd == 0:
				dict = self.get_undermines_for_argument_uid('undermine', db_argument.uid)
				key = 'undermine'
			elif rnd == 1:
				dict = self.get_rebuts_for_argument_uid('rebut', db_argument.uid)
				key = 'rebut'
			else:
				dict = self.get_undercuts_for_argument_uid('undercut', db_argument.uid)
				key = 'undercut'

			rnd = (rnd+1)%3
			if int(dict[key]) != 0 or startrnd == rnd:
				break


		return dict, key

	def save_track_for_user(self, transaction, user, statement_id, premissesgroup_uid, argument_uid, attacked_by_relation, attacked_with_relation): # TODO
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param statement_id: id of the clicked statement
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

	def get_track_of_user(self, user):
		"""
		Returns the complete track of given user
		:param user: current user id
		:return: track os the user id as dict
		ödictionary
		"""
		logger('QueryHelper', 'get_track_of_user', 'user ' + user)
		db_user = DBSession.query(User).filter_by(nickname=user).first()

		if db_user:
			db_track = DBSession.query(Track).filter_by(author_uid=db_user.uid).all()
			return_dict = collections.OrderedDict()
			qh = QueryHelper()
			for index, track in enumerate(db_track):
				logger('QueryHelper','get_track_of_user','track uid ' + str(track.uid))

				track_dict = dict()

				# get attacks
				attacked_by_relation = DBSession.query(Relation).filter_by(uid=track.attacked_by_relation).first()
				attacked_with_relation = DBSession.query(Relation).filter_by(uid=track.attacked_with_relation).first()
				attacked_by_relation_id = qh.get_relation_uid_by_name(attacked_by_relation.name) if attacked_by_relation else 'None'
				attacked_with_relation_id = qh.get_relation_uid_by_name(attacked_with_relation.name) if attacked_with_relation else 'None'

				# get text
				attacked_by_relation_str = attacked_by_relation.name if attacked_by_relation else '-'
				attacked_with_relation_str = attacked_with_relation.name if attacked_with_relation else '-'
				track_statement = '-' if track.statement_uid == 0 else qh.get_text_for_statement_uid(track.statement_uid)
				track_argument = '-' if track.argument_uid == 0 else qh.get_text_for_argument_uid(track.argument_uid)[1:-1]
				if track.premissesGroup_uid == 0:
					track_premissesGroup = '-'
				else:
					track_premissesGroup,tash = qh.get_text_for_premissesGroup_uid(track.premissesGroup_uid)

				# text
				track_dict['statement']                  = track_statement
				track_dict['premissesGroup']             = track_premissesGroup
				track_dict['argument']                   = track_argument
				track_dict['attacked_by_relation']       = attacked_by_relation_str
				track_dict['attacked_with_relation']     = attacked_with_relation_str

				# ids
				track_dict['uid']                        = str(track.uid)
				track_dict['statement_uid']              = str(track.statement_uid)
				track_dict['premissesGroup_uid']         = str(track.premissesGroup_uid)
				track_dict['argument_uid']               = str(track.argument_uid)
				track_dict['attacked_by_relation_uid']   = attacked_by_relation_id
				track_dict['attacked_with_relation_uid'] = attacked_with_relation_id
				track_dict['timestamp']                  = str(track.timestamp)

				if not attacked_by_relation_str == '-':
					track_dict['text'] = 'Others say: \'' + track_argument + \
					                     '\' <i>' + attacked_by_relation_str + 's</i> \'' + \
					                     track_premissesGroup + '\''
				if not attacked_with_relation_str == '-':
					if track_premissesGroup == '-':
						track_dict['text'] = 'You will <i>' + attacked_with_relation_str + '</i> \'' + \
					                         track_argument + '\''
					else:
						track_dict['text'] = 'You say: \'' + track_premissesGroup + \
					                         '\' <i>' + attacked_with_relation_str + 's</i> \'' + \
					                         track_argument + '\''

				return_dict[track.uid] = str(index)

			else:
				logger('QueryHelper', 'get_track_of_user', 'no track')
		else:
			return_dict = dict()
			logger('QueryHelper', 'get_track_of_user', 'no user')

		return return_dict

	def del_track_of_user(self, transaction, user):
		"""
		Returns the complete track of given user
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		db_user = DBSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'del_track_of_user','user ' + str(db_user.uid))
		DBSession.query(Track).filter_by(author_uid=db_user.uid).delete()
		transaction.commit()
