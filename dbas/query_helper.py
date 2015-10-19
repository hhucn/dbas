import random
import collections
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextValue, TextVersion, Premisse, PremisseGroup, Relation, Track, Issue
from .logger import logger

class QueryHelper(object):
	"""

	"""

	def set_statement_as_premisse(self, statement, user, issue):
		"""

		:param statement:
		:param user:
		:param issue:
		:return: uid of the PremisseGroup
		"""
		logger('DatabaseHelper', 'set_statement_as_premisse', 'statement: ' + str(statement) + ', user: ' + str(user))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		premisse_group = PremisseGroup(author=db_user.uid)
		DBDiscussionSession.add(premisse_group)
		DBDiscussionSession.flush()

		premisse_list = []
		logger('DatabaseHelper', 'set_statement_as_premisse', 'premissesgroup: ' + str(premisse_group.uid) + ', statement: '
				+ str(statement.uid) + ', isnegated: ' + ('0' if False else '1') + ', author: ' + str(db_user.uid))
		premisse = Premisse(premissesgroup=premisse_group.uid, statement=statement.uid, isnegated=False, author=db_user.uid, issue=issue)
		premisse_list.append(premisse)

		DBDiscussionSession.add_all(premisse_list)
		DBDiscussionSession.flush()

		db_premissegroup = DBDiscussionSession.query(PremisseGroup).filter_by(author_uid=db_user.uid).order_by(PremisseGroup.uid.desc()).first()

		return db_premissegroup.uid

	def set_argument(self, transaction, user, premissegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
		"""

		:param premissegroup_uid:
		:param is_supportive:
		:param user:
		:param conclusion_uid:
		:param argument_uid:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_argument', 'main')
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		new_argument = Argument(premissegroup=premissegroup_uid, issupportive=is_supportive, author=db_user.uid, weight=0,
							conclusion=conclusion_uid, issue=issue)
		new_argument.conclusions_argument(argument_uid)

		DBDiscussionSession.add(new_argument)
		DBDiscussionSession.flush()

		new_inserted_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premissesGroup_uid==premissegroup_uid,
		                                                              Argument.isSupportive==is_supportive,
		                                                              Argument.author_uid==db_user.uid,
		                                                              Argument.weight==0,
		                                                              Argument.conclusion_uid==conclusion_uid,
		                                                              Argument.argument_uid==argument_uid,
		                                                              Argument.issue_uid==issue)).first()
		transaction.commit()
		if new_inserted_argument:
			logger('QueryHelper', 'set_argument', 'new argument has uid ' + str(new_inserted_argument.uid))
			return new_inserted_argument.uid
		else:
			logger('QueryHelper', 'set_argument', 'new argument is not in the database')
			return 0

	def set_premisses_related_to_argument(self, premissegroup_uid, user, relation, related_argument_uid, is_supportive, issue):
		"""

		:param premissegroup_uid:
		:param user:
		:param relation:
		:param related_argument_uid:
		:param is_supportive:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_premisses_related_to_argument', 'main, ' + ('supports' if is_supportive else 'attacks') + ' related argument ' + str(related_argument_uid))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_related_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==related_argument_uid,
		                                                                      Argument.issue_uid==issue)).first()

		# todo: is this right?

		lo = 'set_premisses_related_to_argument'
		pg = str(premissegroup_uid)
		if 'undermine' in relation.lower() or 'support' in relation.lower():
			logger('QueryHelper', lo, relation + ' from group ' + pg + ' to statement ' + str(db_related_argument.premissesGroup_uid))
			db_premisses = DBDiscussionSession.query(Premisse).filter_by(premissesGroup_uid=db_related_argument.premissesGroup_uid).all()
			arguments = []
			for premisse in db_premisses:
				argument = Argument(premissegroup=premissegroup_uid,
									issupportive=is_supportive,
									author=db_user.uid,
									weight=0,
									conclusion=premisse.statement_uid,
									issue=issue)
				arguments.append(argument)

		elif 'undercut' in relation.lower() or 'overbid' in relation.lower():
			logger('QueryHelper', lo, relation + ' from group ' + pg + ' to argument ' + str(db_related_argument.uid))
			argument = Argument(premissegroup=premissegroup_uid,
								issupportive=is_supportive,
								author=db_user.uid,
								weight=0,
								issue=issue)
			argument.conclusions_argument(db_related_argument.uid)
			arguments = []
			arguments.append(argument)

		elif 'rebut' in relation.lower():
			logger('QueryHelper', lo, 'rebut from group ' + pg + ' to conclusiongroup ' + str(db_related_argument.conclusion_uid))
			argument = Argument(premissegroup=premissegroup_uid,
								issupportive=is_supportive,
								author=db_user.uid,
								weight=0,
								conclusion=db_related_argument.conclusion_uid,
								issue=issue)
			arguments = []
			arguments.append(argument)

		else:
			logger('QueryHelper', 'set_premisses_related_to_argument', 'error')
			return '-1'

		DBDiscussionSession.add_all(arguments)
		DBDiscussionSession.flush()

	def get_relation_uid_by_name(self, relation_name):
		"""

		:param relation_name:
		:param issue:
		:return:
		"""
		db_relation = DBDiscussionSession.query(Relation).filter_by(name=relation_name).first()
		logger('DatabaseHelper', 'get_relation_uid_by_name', 'return ' + str(db_relation.name if db_relation else -1))
		return db_relation.uid if db_relation else -1

	def get_text_for_statement_uid(self, uid, issue):
		"""

		:param uid: id of a statement
		:return: text of the mapped textvalue for this statement
		"""
		logger('QueryHelper', 'get_text_for_statement_uid', 'uid ' + str(uid) + ', issue ' + str(issue))
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==uid, Statement.issue_uid==issue)).join(
			TextValue).first()
		if not db_statement:
			return None
		db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
			textValue_uid=db_statement.textvalues.uid).first()
		logger('QueryHelper', 'get_text_for_statement_uid', 'text ' + db_textversion.content)
		tmp = db_textversion.content
		if tmp.endswith('.'):
			tmp = tmp[:-1]
		return tmp

	def get_text_for_argument_uid(self, id, issue):
		"""

		:param id:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'get_text_for_argument_uid', 'uid ' + str(id) + ', issue ' + str(issue))
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==id, Argument.issue_uid==issue)).first()
		retValue = ''

		# catch error
		if not db_argument:
			logger('QueryHelper', 'get_text_for_argument_uid', 'Error: no argument for id: ' + str(id) + ', issue: ' + str(issue))
			return None

		# basecase
		if db_argument.argument_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'basecase with argument_uid: ' + str(db_argument.argument_uid)
			       + ', in argument: ' + str(db_argument.uid))
			premisses, uids = self.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid, issue)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid, issue)
			premisses = premisses[:-1] if premisses.endswith('.') else premisses # pretty print
			conclusion = conclusion[0:1].lower() + conclusion[1:] # pretty print
			argument = '\'' + premisses + ('\' supports \'' if db_argument.isSupportive else '\' attacks \'') + conclusion + '\''
			return argument

		# recursion
		if db_argument.conclusion_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'recursion with conclusion_uid: ' + str(db_argument.conclusion_uid)
			       + ', in argument: ' + str(db_argument.uid))
			argument = self.get_text_for_argument_uid(db_argument.argument_uid, issue)
			premisses, uids = self.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid, issue)
			retValue = premisses + (' supports ' if db_argument.isSupportive else ' attacks ') + argument

		return retValue

	def get_text_for_premissesGroup_uid(self, uid, issue):
		"""

		:param uid: id of a premisse group
		:param issue:
		:return: text of all premisses in this group and the uids as list
		"""
		logger('QueryHelper', 'get_text_for_premissesGroup_uid', 'main group ' + str(uid))
		db_premisses = DBDiscussionSession.query(Premisse).filter(and_(Premisse.premissesGroup_uid==uid, 
		                                                               Premisse.issue_uid==issue)).join(Statement).all()
		text = ''
		uids = []
		for premisse in db_premisses:
			logger('QueryHelper', 'get_text_for_premissesGroup_uid', 'premisse ' + str(premisse.premissesGroup_uid) + ' . statement'
					+ str(premisse.statement_uid) + ', premisse.statement ' + str(premisse.statements.uid))
			tmp = self.get_text_for_statement_uid(premisse.statements.uid, issue)
			if tmp.endswith('.'):
				tmp = tmp[:-1]
			uids.append(str(premisse.statements.uid))
			text += ' and ' + tmp[:1].lower() + tmp[1:]

		return text[5:], uids

	def get_text_for_arguments_premissesGroup_uid(self, uid, issue):
		"""

		:param uid:
		:param issue:
		:return:
		"""
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==uid, Argument.issue_uid==issue)).first()
		text, tmp = self.get_text_for_premissesGroup_uid(db_argument.premissesGroup_uid, issue)
		return text

	def get_undermines_for_premisses(self, key, premisses_as_statements_uid, issue):
		"""

		:param premisses_as_statements_uid:
		:param issue:
		:param key:
		:return:
		"""
		logger('QueryHelper', 'get_undermines_for_premisses', 'main')
		return_dict = {}
		index = 0
		for s_uid in premisses_as_statements_uid:
			logger('QueryHelper', 'get_undermines_for_premisses', 'db_undermine against Argument.conclusion_uid=='+str(s_uid))
			db_undermine = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==False, Argument.conclusion_uid==s_uid, Argument.issue_uid==issue
			                                                               )).all()
			for undermine in db_undermine:
				db_undermine_premisses = DBDiscussionSession.query(Premisse).filter(
					and_(Premisse.premissesGroup_uid==undermine.premissesGroup_uid, Premisse.issue_uid==issue)).first()
				logger('QueryHelper', 'get_undermines_for_premisses', 'found db_undermine ' + str(undermine.uid))
				return_dict[key + str(index)], uids = QueryHelper().get_text_for_premissesGroup_uid(undermine.premissesGroup_uid, issue)
				return_dict[key + str(index) + 'id'] = undermine.premissesGroup_uid
				return_dict[key + str(index) + '_statement_id'] = db_undermine_premisses.statement_uid
				return_dict[key + str(index) + '_argument_id'] = undermine.uid
				index += 1
		return_dict[key] = str(index)
		return return_dict

	def get_undermines_for_argument_uid(self, key, argument_uid, issue):
		"""
		Calls get_undermines_for_premisses('reason', premisses_as_statements_uid)
		:param argument_uid: uid of the specified argument
		:param issue:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(argument_uid))
		db_attacked_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==argument_uid,
		                                                                       Argument.issue_uid==issue)).first()
		db_attacked_premisses = DBDiscussionSession.query(Premisse).filter(and_(
			Premisse.premissesGroup_uid==db_attacked_argument.premissesGroup_uid, Premisse.issue_uid==issue)).order_by(
			Premisse.premissesGroup_uid.desc()).all()

		premisses_as_statements_uid = set()
		for premisse in db_attacked_premisses:
			premisses_as_statements_uid.add(premisse.statement_uid)
			logger('QueryHelper', 'get_undermines_for_argument_uid', 'db_attacked_argument has pgroup with pgroup ' +
		           str(premisse.premissesGroup_uid) + ', statement ' + str(premisse.statement_uid))

		if len(premisses_as_statements_uid) == 0:
			return None

		return self.get_undermines_for_premisses(key, premisses_as_statements_uid, issue)

	def get_overbids_for_argument_uid(self, key, argument_uid, issue):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, True)
		:param argument_uid: uid of the specified argument
		:param issue:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_overbids_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, True, issue)

	def get_undercuts_for_argument_uid(self, key, argument_uid, issue):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, False)
		:param argument_uid:
		:param key:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'get_undercuts_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, False, issue)

	def get_rebuts_for_arguments_conclusion_uid(self, key, conclusion_statements_uid, is_current_argument_supportive, issue):
		"""

		:param key:
		:param conclusion_statements_uid:
		:param is_current_argument_supportive:
		:param issue:
		:return:
		"""
		return_dict = {}
		logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid',
		       'db_rebut against Argument.conclusion_uid=='+str(conclusion_statements_uid))
		db_rebut = DBDiscussionSession.query(Argument).filter(Argument.isSupportive==(not is_current_argument_supportive),
		                                            Argument.conclusion_uid==conclusion_statements_uid, Argument.issue_uid==issue).all()
		for index, rebut in enumerate(db_rebut):
			db_rebut_premisses = DBDiscussionSession.query(Premisse).filter(and_(
				Premisse.premissesGroup_uid==rebut.premissesGroup_uid, Premisse.issue_uid==issue)).first()
			logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'found db_rebut ' + str(rebut.uid))
			return_dict[key + str(index)], uids = QueryHelper().get_text_for_premissesGroup_uid(rebut.premissesGroup_uid, issue)
			return_dict[key + str(index) + 'id'] = rebut.premissesGroup_uid
			return_dict[key + str(index) + '_statement_id'] = db_rebut_premisses.statement_uid
			return_dict[key + str(index) + '_argument_id'] = rebut.uid
		return_dict[key] = str(len(db_rebut))
		return return_dict

	def get_rebuts_for_argument_uid(self, key, argument_uid, issue):
		"""
		Calls self.get_rebuts_for_arguments_conclusion_uid('reason', Argument.conclusion_uid)
		:param argument_uid: uid of the specified argument
		:param issue:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_rebuts_for_argument_uid', 'main')
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==int(argument_uid), Argument.issue_uid==issue)).first()
		if not db_argument:
			return None
		return self.get_rebuts_for_arguments_conclusion_uid(key, db_argument.conclusion_uid, db_argument.isSupportive, issue)

	def get_supports_for_argument_uid(self, key, argument_uid, issue):
		"""

		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_supports_for_argument_uid', 'main')

		return_dict = {}
		index = 0
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==argument_uid, Argument.issue_uid==issue)).join(
			PremisseGroup).first()
		db_arguments_premisses = DBDiscussionSession.query(Premisse).filter(and_(
			Premisse.premissesGroup_uid==db_argument.premissesGroup_uid, Premisse.issue_uid==issue)).all()

		for arguments_premisses in db_arguments_premisses:
			db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==arguments_premisses.statement_uid, Argument.isSupportive==True, Argument.issue_uid==issue)).join(
				PremisseGroup).all()
			if not db_supports:
				continue

			for support in db_supports:
				db_support_premisses = DBDiscussionSession.query(Premisse).filter(and_(
					Premisse.premissesGroup_uid==support.premissesGroup_uid, Premisse.issue_uid==issue)).first()
				return_dict[key + str(index)], trash = self.get_text_for_premissesGroup_uid(support.premissesGroup_uid, issue)
				return_dict[key + str(index) + 'id'] = support.premissesGroup_uid
				return_dict[key + str(index) + '_statement_id'] = db_support_premisses.statement_uid
				index += 1

		return_dict[key] = str(index)

		return None if len(return_dict) == 0 else return_dict

	def get_attack_or_support_for_justification_of_argument_uid(self, key, argument_uid, is_supportive, issue):
		"""

		:param key:
		:param argument_uid:
		:param is_supportive:
		:param issue:
		:return:
		"""
		return_dict = {}
		logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid=='+str(argument_uid))
		db_relation = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==is_supportive,
		                                                         Argument.argument_uid==argument_uid, Argument.issue_uid==issue)).all()
		if not db_relation:
			return None
		for index, relation in enumerate(db_relation):
			db_relation_premisses = DBDiscussionSession.query(Premisse).filter(and_(
				Premisse.premissesGroup_uid==relation.premissesGroup_uid, Premisse.issue_uid==issue)).first()
			logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
					'found relation, argument uid ' + str(relation.uid))
			return_dict[key + str(index)], uids = QueryHelper().get_text_for_premissesGroup_uid(relation.premissesGroup_uid, issue)
			return_dict[key + str(index) + 'id'] = relation.premissesGroup_uid
			return_dict[key + str(index) + '_statement_id'] = db_relation_premisses.statement_uid
			return_dict[key + str(index) + '_argument_id'] = relation.uid
			#return_dict[key + str(index) + 'id'] = ','.join(uids)
		return_dict[key] = str(len(db_relation))
		return return_dict

	def get_attack_for_argument_by_random(self, db_argument, user, issue):
		"""
		Returns a dictionary with attacks. The attack itself is random out of the set of attacks, which were not done yet.
		Additionally returns id's of premisses groups with [key + str(index) + 'id']
		:param db_argument:
		:param user:
		:param issue:
		:return: dict, key
		"""

		# 1 = undermine
		# 2 = support
		# 3 = undercut
		# 4 = overbid
		# 5 = rebut

		logger('QueryHelper', 'get_attack_for_argument_by_random', 'user ' + (user if user else 'anonymous') + ', arg.uid ' + str(
			db_argument.uid))

		# all possible attacks
		complete_list_of_attacks = [1,3,5]
		attacks = [1,3,5]
		# maybe we are anonymous
		if user:
			# history of selected attacks
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if db_user.uid != 1: # not equal anonymous
				db_track = DBDiscussionSession.query(Track).filter(and_(Track.author_uid==db_user.uid, Track.argument_uid==db_argument.uid)).all()
				for track in db_track:
					if track.attacked_by_relation in attacks:
						attacks.remove(track.attacked_by_relation)
				# now attacks contains all attacks, which were not be done
				logger('QueryHelper', 'get_attack_for_argument_by_random', 'attacks, which were not done yet ' + str(attacks))

		attack_list = complete_list_of_attacks if len(attacks) == 0 else attacks
		dict, key = self.get_attack_for_argument_by_random_in_range(db_argument.uid, attack_list, issue, complete_list_of_attacks)
		# sanity check if we could not found an attack for a left attack in out set
		if not dict and len(attacks) > 0:
			dict, key = self.get_attack_for_argument_by_random_in_range(db_argument.uid, complete_list_of_attacks, issue, complete_list_of_attacks)

		return dict, key

	def get_attack_for_argument_by_random_in_range(self, argument_uid, attack_list, issue, complete_list_of_attacks):
		"""

		:param argument_uid:
		:param attack_list:
		:param issue:
		:param complete_list_of_attacks:
		:return:
		"""
		return_dict = None
		key = ''
		left_attacks = list(set(complete_list_of_attacks) - set(attack_list))
		attack_found = False

		logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'attack_list : ' + str(attack_list))
		logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'complete_list_of_attacks : ' + str(complete_list_of_attacks))
		logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'left_attacks : ' + str(left_attacks))

		# randomize at least 1, maximal 3 times for getting an attack
		while len(attack_list) > 0:
			attack = random.choice(attack_list)
			attack_list.remove(attack)
			logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', '\'random\' attack is ' + str(attack))
			if attack == 1:
				return_dict = self.get_undermines_for_argument_uid('undermine', argument_uid, issue)
				key = 'undermine'
			elif attack == 5:
				return_dict = self.get_rebuts_for_argument_uid('rebut', argument_uid, issue)
				key = 'rebut'
			else:
				return_dict = self.get_undercuts_for_argument_uid('undercut', argument_uid, issue)
				key = 'undercut'

			if return_dict and int(return_dict[key]) != 0:
				logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'attack found')
				attack_found = True
				break
			else:
				logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'no attack found')

		if len(left_attacks) > 0 and not attack_found:
			logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'redo algo with left attacks ' + str(left_attacks))
			return_dict, key = self.get_attack_for_argument_by_random_in_range(argument_uid, left_attacks, issue, left_attacks)
		else:
			logger('QueryHelper', 'get_attack_for_argument_by_random_in_range', 'no attacks left for redoing')


		return return_dict, key

	def save_track_for_user(self, transaction, user, statement_id, premissesgroup_uid, argument_uid, attacked_by_relation, attacked_with_relation, session_id):
		"""
		Saves track for user
		:param transaction: current transaction
		:param user: authentication nick id of the user
		:param statement_id: id of the clicked statement
		:param premissesgroup_uid: id of the clicked premisseGroup
		:param attacked_by_relation: id of attacked by relation
		:param attacked_with_relation: id of attacked_w th relation
		:param issue:
		:return: undefined
		"""
		if user == None:
			user = 'anonymous'

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'save_track_for_user', 'user: ' + user + ', db_user: ' + str(db_user.uid) +
														', statememt_id ' + str(statement_id) +
														', premissesgroup_uid ' + str(premissesgroup_uid) +
														', argument_uid ' + str(argument_uid) +
														', attacked_by_relation ' + str(attacked_by_relation) +
														', attacked_with_relation ' + str(attacked_with_relation) +
		                                                ', sesseion_id ' + str(session_id))
		DBDiscussionSession.add(Track(user=db_user.uid, statement=statement_id, premissegroup=premissesgroup_uid, argument = argument_uid,
		                    attacked_by=attacked_by_relation, attacked_with=attacked_with_relation, session_id=session_id))
		transaction.commit()

	def get_track_of_user(self, user):
		"""
		Returns the complete track of given user
		:param user: current user id
		:param issue:
		:return: track os the user id as dict
		"""
		logger('QueryHelper', 'get_track_of_user', 'user ' + user)
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			logger('QueryHelper', 'get_track_of_user', 'no user')
			return dict()

		db_tracks = DBDiscussionSession.query(Track).filter_by(author_uid=db_user.uid).all()
		qh = QueryHelper()

		if not db_tracks:
			logger('QueryHelper', 'get_track_of_user', 'no track')
			return dict()

		return_dict = collections.OrderedDict()

		db_issues = DBDiscussionSession.query(Issue).all()

		for issue in db_issues:
			issue_dict = collections.OrderedDict()
			for index, track in enumerate(db_tracks):
				logger('QueryHelper','get_track_of_user','track uid ' + str(track.uid))

				track_dict = dict()

				# get attacks
				attacked_by_relation = DBDiscussionSession.query(Relation).filter_by(uid=track.attacked_by_relation).first()
				attacked_with_relation = DBDiscussionSession.query(Relation).filter_by(uid=track.attacked_with_relation).first()
				attacked_by_relation_id = qh.get_relation_uid_by_name(attacked_by_relation.name) if attacked_by_relation else 'None'
				attacked_with_relation_id = qh.get_relation_uid_by_name(attacked_with_relation.name) if attacked_with_relation else 'None'

				# get text
				attacked_by_relation_str = attacked_by_relation.name if attacked_by_relation else '-'
				attacked_with_relation_str = attacked_with_relation.name if attacked_with_relation else '-'
				track_statement = '-' if track.statement_uid == 0 else qh.get_text_for_statement_uid(track.statement_uid, issue.uid)
				track_argument = '-' if track.argument_uid == 0 else qh.get_text_for_argument_uid(track.argument_uid, issue.uid)[1:-1]
				if track.premissesGroup_uid == 0:
					track_premissesGroup = '-'
				else:
					track_premissesGroup,tash = qh.get_text_for_premissesGroup_uid(track.premissesGroup_uid, issue.uid)

				if track_statement:

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

					issue_dict[str(index)] = track_dict
			issue_dict['uid'] = str(issue.uid)
			issue_dict['text'] = str(issue.text)
			issue_dict['date'] = str(issue.date)
			return_dict[str(issue.uid)] = issue_dict

		return return_dict

	def del_track_of_user(self, transaction, user):
		"""
		Returns the complete track of given user
		:param transaction: current transaction
		:param user: current user
		:param issue:
		:return: undefined
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'del_track_of_user','user ' + str(db_user.uid))
		DBDiscussionSession.query(Track).filter_by(author_uid=db_user.uid).delete()
		transaction.commit()
