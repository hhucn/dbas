import datetime
import locale
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, Relation, History, Vote
from .logger import logger
from .strings import Translator
from .user_management import UserHandler

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class QueryHelper(object):
	"""

	"""

	def add_arguments(self, transaction, argument_list):
		"""
		Ass all arguments in argument_list only if they are not duplicates
		:param transaction:
		:param argument_list:
		:return:
		"""
		logger('QueryHelper', 'add_arguments', 'main')
		duplicate_free_list = []
		duplicate_dict = {}
		for argument in argument_list:
			logger('QueryHelper', 'add_arguments', 'check for duplicate of argument with '
			       + ', premisesGroup_uid: ' + str(argument.premisesGroup_uid)
			       + ', isSupportive: ' + str(argument.isSupportive)
			       + ', author_uid: ' + str(argument.author_uid)
			       + ', weight_uid: ' + str(argument.weight)
			       + ', conclusion_uid: ' + str(argument.conclusion_uid)
			       + ', issue_uid: ' + str(argument.issue_uid)
			       + ', argument_uid: ' + str(argument.argument_uid))
			db_duplicate = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid == argument.premisesGroup_uid,
			                                                               Argument.isSupportive == argument.isSupportive,
			                                                               Argument.author_uid == argument.author_uid,
			                                                               Argument.weight == argument.weight,
			                                                               Argument.conclusion_uid == argument.conclusion_uid,
			                                                               Argument.issue_uid == argument.issue_uid,
			                                                               Argument.argument_uid == 0)).first()


			if db_duplicate:
				logger('QueryHelper', 'add_arguments', 'argument is a duplicate')
				duplicate_dict['arg_' + str(argument.premisesGroup_uid)] = 'true'
			else:
				logger('QueryHelper', 'add_arguments', 'argument is no duplicate')
				duplicate_free_list.append(argument)
				duplicate_dict['arg_' + str(argument.premisesGroup_uid)] = 'false'

		DBDiscussionSession.add_all(duplicate_free_list)
		DBDiscussionSession.flush()
		transaction.commit()

		return duplicate_dict

	def get_number_of_arguments(self, issue):
		"""

		:param issue:
		:return:
		"""
		return len(DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all())

	def set_statement_as_new_premise(self, statement, user, issue):
		"""

		:param statement:
		:param user:
		:param issue:
		:return: uid of the PremiseGroup
		"""
		logger('QueryHelper', 'set_statement_as_new_premise', 'statement: ' + str(statement) + ', user: ' + str(user))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# check for duplicate
		db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
		if db_premise:
			logger('QueryHelper', 'set_statement_as_new_premise', 'statement is already given as premise')
			db_premisegroup = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=db_premise.premisesGroup_uid).all()

			if len(db_premisegroup) == 1:
				logger('QueryHelper', 'set_statement_as_new_premise', 'statement is already given as premise and the only one in its group')
				return db_premisegroup[0].premisesGroup_uid

		premise_group = PremiseGroup(author=db_user.uid)
		DBDiscussionSession.add(premise_group)
		DBDiscussionSession.flush()

		premise_list = []
		logger('QueryHelper', 'set_statement_as_new_premise', 'premisesgroup: ' + str(premise_group.uid) + ', statement: '
				+ str(statement.uid) + ', isnegated: ' + ('0' if False else '1') + ', author: ' + str(db_user.uid))
		premise = Premise(premisesgroup=premise_group.uid, statement=statement.uid, isnegated=False, author=db_user.uid, issue=issue)
		premise_list.append(premise)

		DBDiscussionSession.add_all(premise_list)
		DBDiscussionSession.flush()

		db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

		return db_premisegroup.uid

	def set_statement_as_premise(self, statement, user, premise_group_uid, issue):
		"""

		:param statement:
		:param user:
		:param premise_group_uid:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_statement_as_premise', 'statement: ' + str(statement) + ', user: ' + str(user))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		premise_list = []
		logger('QueryHelper', 'set_statement_as_premise', 'premisesgroup: ' + str(premise_group_uid) + ', statement: '
				+ str(statement.uid) + ', isnegated: ' + ('0' if False else '1') + ', author: ' + str(db_user.uid))
		premise = Premise(premisesgroup=premise_group_uid, statement=statement.uid, isnegated=False, author=db_user.uid, issue=issue)
		premise_list.append(premise)

		DBDiscussionSession.add_all(premise_list)
		DBDiscussionSession.flush()

		db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

		return db_premisegroup.uid

	def set_argument(self, transaction, user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
		"""

		:param premisegroup_uid:
		:param is_supportive:
		:param user:
		:param conclusion_uid:
		:param argument_uid:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_argument', 'main with user: ' + str(user)
		       + ', premisegroup_uid: ' + str(premisegroup_uid)
		       + ', conclusion_uid: ' + str(conclusion_uid)
		       + ', argument_uid: ' + str(argument_uid)
		       + ', is_supportive: ' + str(is_supportive)
		       + ', issue: ' + str(issue))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid, weight=0,
							conclusion=conclusion_uid, issue=issue)
		new_argument.conclusions_argument(argument_uid)

		DBDiscussionSession.add(new_argument)
		DBDiscussionSession.flush()

		new_inserted_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premisegroup_uid,
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

	def set_premises_related_to_argument(self, premisegroup_uid, user, relation, related_argument_uid, is_supportive, issue):
		"""

		:param premisegroup_uid:
		:param user:
		:param relation:
		:param related_argument_uid:
		:param is_supportive:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_premises_related_to_argument', 'main, ' + ('supports' if is_supportive else 'attacks') + ' related argument ' + str(related_argument_uid))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_related_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==related_argument_uid,
		                                                                      Argument.issue_uid==issue)).first()

		lo = 'set_premises_related_to_argument'
		pg = str(premisegroup_uid)
		if 'undermine' in relation.lower() or 'support' in relation.lower():
			logger('QueryHelper', lo, relation + ' from group ' + pg + ' to statement ' + str(db_related_argument.premisesGroup_uid))
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=db_related_argument.premisesGroup_uid).all()
			arguments = []
			for premise in db_premises:
				argument = Argument(premisegroup=premisegroup_uid,
									issupportive=is_supportive,
									author=db_user.uid,
									weight=0,
									conclusion=premise.statement_uid,
									issue=issue)
				arguments.append(argument)

		elif 'undercut' in relation.lower() or 'overbid' in relation.lower():
			logger('QueryHelper', lo, relation + ' from group ' + pg + ' to argument ' + str(db_related_argument.uid))
			argument = Argument(premisegroup=premisegroup_uid,
								issupportive=is_supportive,
								author=db_user.uid,
								weight=0,
								issue=issue)
			argument.conclusions_argument(db_related_argument.uid)
			arguments = []
			arguments.append(argument)

		elif 'rebut' in relation.lower():
			logger('QueryHelper', lo, 'rebut from group ' + pg + ' to conclusiongroup ' + str(db_related_argument.conclusion_uid))
			argument = Argument(premisegroup=premisegroup_uid,
								issupportive=is_supportive,
								author=db_user.uid,
								weight=0,
								conclusion=db_related_argument.conclusion_uid,
								issue=issue)
			arguments = []
			arguments.append(argument)

		else:
			logger('QueryHelper', 'set_premises_related_to_argument', 'error')
			return '-1'

		DBDiscussionSession.add_all(arguments)
		DBDiscussionSession.flush()

	def get_relation_uid_by_name(self, relation_name):
		"""

		:param relation_name:
		:return:
		"""
		db_relation = DBDiscussionSession.query(Relation).filter_by(name=relation_name).first()
		logger('QueryHelper', 'get_relation_uid_by_name', 'return ' + str(db_relation.name if db_relation else -1))
		return db_relation.uid if db_relation else -1

	def get_text_for_statement_uid(self, uid, issue):
		"""

		:param uid: id of a statement
		:param issue:
		:return: text of the mapped textvalue for this statement
		"""
		logger('QueryHelper', 'get_text_for_statement_uid', 'uid ' + str(uid) + ', issue ' + str(issue))
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==uid,
		                                                                Statement.issue_uid==issue)).first()
		if not db_statement:
			return None

		db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
			uid=db_statement.textversion_uid).first()
		logger('QueryHelper', 'get_text_for_statement_uid', 'text ' + db_textversion.content)
		tmp = db_textversion.content

		if tmp.endswith('.'):
			tmp = tmp[:-1]

		return tmp

	def get_text_for_argument_uid(self, id, issue, lang):
		"""
		Returns current argument as string like conclusion, because premise1 and premise2
		:param id: int
		:param issue: int
		:param lang: str
		:return: str
		"""
		logger('QueryHelper', 'get_text_for_argument_uid', 'uid ' + str(id) + ', issue ' + str(issue))
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=id).first()
		retValue = ''
		_t = Translator(lang)

		# catch error
		if not db_argument:
			logger('QueryHelper', 'get_text_for_argument_uid', 'Error: no argument for id: ' + str(id) + ', issue: ' + str(issue))
			return None

		# basecase
		if db_argument.argument_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'basecase with argument_uid: ' + str(db_argument.argument_uid)
			       + ', in argument: ' + str(db_argument.uid))
			premises, uids = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid, issue)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid, issue)
			premises = premises[:-1] if premises.endswith('.') else premises # pretty print
			if not conclusion:
				return None
			conclusion = conclusion[0:1].lower() + conclusion[1:] # pretty print
			if db_argument.isSupportive:
				argument = conclusion + ' ' + _t.get(_t.because).lower() + ' ' + premises
			else:
				argument = conclusion + ' ' + _t.get(_t.doesNotHoldBecause).lower() + ' ' + premises
			#argument = premises + (' supports ' if db_argument.isSupportive else ' attacks ') + conclusion
			return argument

		# recursion
		if db_argument.conclusion_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'recursion with conclusion_uid: ' + str(db_argument.conclusion_uid)
			       + ', in argument: ' + str(db_argument.uid))
			argument = self.get_text_for_argument_uid(db_argument.argument_uid, issue, lang)
			premises, uids = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid, issue)
			if not premises:
				return None
			if db_argument.isSupportive:
				retValue = argument + ', ' + _t.get(_t.because).lower() + ' ' + premises
			else:
				retValue = argument + ' ' + _t.get(_t.doesNotHoldBecause).lower() + ' ' + premises
			#retValue = premises + (' supports ' if db_argument.isSupportive else ' attacks ') + argument

		return retValue

	def get_text_for_premisesGroup_uid(self, uid, issue):
		"""

		:param uid: id of a premise group
		:param issue:
		:return: text of all premises in this group and the uids as list
		"""
		logger('QueryHelper', 'get_text_for_premisesGroup_uid', 'main group ' + str(uid) + ', issue ' + str(issue))
		db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==uid,
		                                                             Premise.issue_uid==issue)).join(Statement).all()
		text = ''
		uids = []
		for premise in db_premises:
			logger('QueryHelper', 'get_text_for_premisesGroup_uid', 'premise ' + str(premise.premisesGroup_uid) + ' . statement'
					+ str(premise.statement_uid) + ', premise.statement ' + str(premise.statements.uid))
			tmp = self.get_text_for_statement_uid(premise.statements.uid, issue)
			if tmp.endswith('.'):
				tmp = tmp[:-1]
			uids.append(str(premise.statements.uid))
			text += ' and ' + tmp[:1].lower() + tmp[1:]

		return text[5:], uids

	def get_text_for_arguments_premisesGroup_uid(self, uid, issue):
		"""

		:param uid:
		:param issue:
		:return:
		"""
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==uid, Argument.issue_uid==issue)).first()
		text, uids = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid, issue)
		return text, uids

	def get_undermines_for_premises(self, key, premises_as_statements_uid, issue):
		"""

		:param premises_as_statements_uid:
		:param issue:
		:param key:
		:return:
		"""
		logger('QueryHelper', 'get_undermines_for_premises', 'main')
		return_dict = {}
		index = 0
		given_undermines = set()
		for s_uid in premises_as_statements_uid:
			logger('QueryHelper', 'get_undermines_for_premises', 'db_undermine against Argument.conclusion_uid=='+str(s_uid))
			db_undermine = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==False, Argument.conclusion_uid==s_uid, Argument.issue_uid==issue
			                                                               )).all()
			for undermine in db_undermine:
				if undermine.premisesGroup_uid not in given_undermines:
					given_undermines.add(undermine.premisesGroup_uid)
					db_undermine_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==undermine.premisesGroup_uid,
				                                                                       Premise.issue_uid==issue)).first()
					logger('QueryHelper', 'get_undermines_for_premises', 'found db_undermine ' + str(undermine.uid))
					return_dict[key + str(index)], uids = QueryHelper().get_text_for_premisesGroup_uid(undermine.premisesGroup_uid, issue)
					return_dict[key + str(index) + 'id'] = undermine.premisesGroup_uid
					return_dict[key + str(index) + '_statement_id'] = db_undermine_premises.statement_uid
					return_dict[key + str(index) + '_argument_id'] = undermine.uid
					index += 1
		return_dict[key] = str(index)
		return return_dict

	def get_undermines_for_argument_uid(self, key, argument_uid, issue):
		"""
		Calls get_undermines_for_premises('reason', premises_as_statements_uid)
		:param argument_uid: uid of the specified argument
		:param issue:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(argument_uid))
		db_attacked_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==argument_uid,
		                                                                       Argument.issue_uid==issue)).first()
		db_attacked_premises = DBDiscussionSession.query(Premise).filter(and_(
			Premise.premisesGroup_uid==db_attacked_argument.premisesGroup_uid, Premise.issue_uid==issue)).order_by(
			Premise.premisesGroup_uid.desc()).all()

		premises_as_statements_uid = set()
		for premise in db_attacked_premises:
			premises_as_statements_uid.add(premise.statement_uid)
			logger('QueryHelper', 'get_undermines_for_argument_uid', 'db_attacked_argument has pgroup with pgroup ' +
		           str(premise.premisesGroup_uid) + ', statement ' + str(premise.statement_uid))

		if len(premises_as_statements_uid) == 0:
			return None

		return self.get_undermines_for_premises(key, premises_as_statements_uid, issue)

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
		index = 0
		given_rebuts = set()
		logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'conclusion_statements_uid ' + str(conclusion_statements_uid)
		       + ', is_current_argument_supportive ' + str(is_current_argument_supportive) + ' (searching for the opposite)')
		db_rebut = DBDiscussionSession.query(Argument).filter(Argument.isSupportive==(not is_current_argument_supportive),
		                                                      Argument.conclusion_uid==conclusion_statements_uid,
		                                                      Argument.issue_uid==issue).all()
		for rebut in db_rebut:
			if rebut.premisesGroup_uid not in given_rebuts:
				given_rebuts.add(rebut.premisesGroup_uid)
				db_rebut_premises = DBDiscussionSession.query(Premise).filter(and_(
					Premise.premisesGroup_uid==rebut.premisesGroup_uid, Premise.issue_uid==issue)).first()
				logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'found db_rebut ' + str(rebut.uid))
				return_dict[key + str(index)], uids = QueryHelper().get_text_for_premisesGroup_uid(rebut.premisesGroup_uid, issue)
				return_dict[key + str(index) + 'id'] = rebut.premisesGroup_uid
				return_dict[key + str(index) + '_statement_id'] = db_rebut_premises.statement_uid
				return_dict[key + str(index) + '_argument_id'] = rebut.uid
				index += 1
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
		given_supports = set()
		index = 0
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==argument_uid, Argument.issue_uid==issue)).join(
			PremiseGroup).first()
		db_arguments_premises = DBDiscussionSession.query(Premise).filter(and_(
			Premise.premisesGroup_uid==db_argument.premisesGroup_uid, Premise.issue_uid==issue)).all()

		for arguments_premises in db_arguments_premises:
			db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==arguments_premises.statement_uid,
			                                                              Argument.isSupportive==True,
			                                                              Argument.issue_uid==issue)).join(PremiseGroup).all()
			if not db_supports:
				continue

			for support in db_supports:
				if support.premisesGroup_uid not in given_supports:
					db_support_premises = DBDiscussionSession.query(Premise).filter(and_(
						Premise.premisesGroup_uid==support.premisesGroup_uid,
						Premise.issue_uid==issue)).first()
					return_dict[key + str(index)], trash = self.get_text_for_premisesGroup_uid(support.premisesGroup_uid, issue)
					return_dict[key + str(index) + 'id'] = support.premisesGroup_uid
					return_dict[key + str(index) + '_statement_id'] = db_support_premises.statement_uid
					index += 1
					given_supports.add(support.premisesGroup_uid)

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
		index = 0
		logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid=='+str(argument_uid))
		db_relation = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==is_supportive,
		                                                         Argument.argument_uid==argument_uid, Argument.issue_uid==issue)).all()#
		given_relations = set()

		if not db_relation:
			return None

		for relation in db_relation:
			if relation.premisesGroup_uid not in given_relations:
				given_relations.add(relation.premisesGroup_uid)
				db_relation_premises = DBDiscussionSession.query(Premise).filter(and_(
					Premise.premisesGroup_uid==relation.premisesGroup_uid, Premise.issue_uid==issue)).first()
				logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
						'found relation, argument uid ' + str(relation.uid))
				return_dict[key + str(index)], uids = QueryHelper().get_text_for_premisesGroup_uid(relation.premisesGroup_uid, issue)
				return_dict[key + str(index) + 'id'] = relation.premisesGroup_uid
				return_dict[key + str(index) + '_statement_id'] = db_relation_premises.statement_uid
				return_dict[key + str(index) + '_argument_id'] = relation.uid
				index += 1
				#return_dict[key + str(index) + 'id'] = ','.join(uids)
		return_dict[key] = str(len(db_relation))
		return return_dict

	def get_user_with_same_opinion(self, argument_uid, lang):
		"""

		:param argument_uid:
		:param lang:
		:return:
		"""
		logger('QueryHelper', 'get_user_with_same_opinion', 'Argument ' + str(argument_uid))

		ret_dict = dict()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			return ret_dict

		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_argument.weight_uid).all()
		uh = UserHandler()
		for vote in db_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			logger('QueryHelper', 'get_user_with_same_opinion', 'User ' + str(voted_user.nickname)
			       + ', avatar ' + uh.get_profile_picture(voted_user))
			ret_dict[voted_user.nickname] = {'avatar_url': uh.get_profile_picture(voted_user),
			                                 'vote_timestamp': self.sql_timestamp_pretty_print(str(vote.timestamp), lang)}
		return ret_dict

	def sql_timestamp_pretty_print(self, ts, lang):
		"""

		:param ts: timestamp as string
		:param lang: language
		:return:
		"""

		logger('QueryHelper', 'sql_timestamp_pretty_print', 'with locale ' + str(lang))
		format = '%-I:%M %p, %d. %b. %Y'

		if lang == 'de':
			try:
				locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
				format = '%-H:%M Uhr, %d. %b. %Y'
			except:
				logger('QueryHelper', 'sql_timestamp_pretty_print', 'locale ' + str(lang) + ' is not supported')
				locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

		time = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

		return time.strftime(format)