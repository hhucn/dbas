import datetime
import locale
import collections
from sqlalchemy import and_
from slugify import slugify

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, Relation, History, Vote, Issue
from .logger import logger
from .recommender_system import RecommenderHelper
from .strings import Translator, TextGenerator
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
			       + ', weight_uid: ' + str(argument.weight_uid)
			       + ', conclusion_uid: ' + str(argument.conclusion_uid)
			       + ', issue_uid: ' + str(argument.issue_uid)
			       + ', argument_uid: ' + str(argument.argument_uid))
			db_duplicate = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid == argument.premisesGroup_uid,
			                                                               Argument.isSupportive == argument.isSupportive,
			                                                               Argument.author_uid == argument.author_uid,
			                                                               Argument.weight_uid == argument.weight_uid,
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
		new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premisegroup_uid,
		                                                               Argument.isSupportive==is_supportive,
		                                                               Argument.conclusion_uid==conclusion_uid,
		                                                               Argument.issue_uid==issue)).first()
		if not new_argument:
			new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid, weight=0,
			                        conclusion=conclusion_uid, issue=issue)
			new_argument.conclusions_argument(argument_uid)

			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()

			new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premisegroup_uid,
			                                                               Argument.isSupportive==is_supportive,
			                                                               Argument.author_uid==db_user.uid,
			                                                               Argument.weight_uid==0,
			                                                               Argument.conclusion_uid==conclusion_uid,
			                                                               Argument.argument_uid==argument_uid,
			                                                               Argument.issue_uid==issue)).first()
		transaction.commit()
		if new_argument:
			logger('QueryHelper', 'set_argument', 'new argument has uid ' + str(new_argument.uid))
			return new_argument.uid
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

	def get_text_for_statement_uid(self, uid):
		"""

		:param uid: id of a statement
		:return: text of the mapped textvalue for this statement
		"""
		logger('QueryHelper', 'get_text_for_statement_uid', 'uid ' + str(uid))
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
		if not db_statement:
			return None

		db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
			uid=db_statement.textversion_uid).first()
		logger('QueryHelper', 'get_text_for_statement_uid', 'text ' + db_textversion.content)
		tmp = db_textversion.content

		if tmp.endswith(('.','?','!')):
			tmp = tmp[:-1]

		return tmp

	def get_text_for_argument_uid(self, id, lang):
		"""
		Returns current argument as string like conclusion, because premise1 and premise2
		:param id: int
		:param lang: str
		:return: str
		"""
		logger('QueryHelper', 'get_text_for_argument_uid', 'uid ' + str(id) )
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=id).first()
		retValue = ''
		_t = Translator(lang)

		# catch error
		if not db_argument:
			logger('QueryHelper', 'get_text_for_argument_uid', 'Error: no argument for id: ' + str(id))
			return None

		# basecase
		if db_argument.argument_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'basecase with argument_uid: ' + str(db_argument.argument_uid)
			       + ', in argument: ' + str(db_argument.uid))
			premises, uids = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid)
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
			argument = self.get_text_for_argument_uid(db_argument.argument_uid, lang)
			premises, uids = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
			if not premises:
				return None
			if db_argument.isSupportive:
				retValue = argument + ', ' + _t.get(_t.because).lower() + ' ' + premises
			else:
				retValue = argument + ' ' + _t.get(_t.doesNotHoldBecause).lower() + ' ' + premises
			#retValue = premises + (' supports ' if db_argument.isSupportive else ' attacks ') + argument

		return retValue

	def get_text_for_premisesGroup_uid(self, uid):
		"""

		:param uid: id of a premise group
		:return: text of all premises in this group and the uids as list
		"""
		logger('QueryHelper', 'get_text_for_premisesGroup_uid', 'main group ' + str(uid) )
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=uid).join(Statement).all()
		text = ''
		uids = []
		for premise in db_premises:
			logger('QueryHelper', 'get_text_for_premisesGroup_uid', 'premise ' + str(premise.premisesGroup_uid) + ' . statement'
					+ str(premise.statement_uid) + ', premise.statement ' + str(premise.statements.uid))
			tmp = self.get_text_for_statement_uid(premise.statements.uid)
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
		text, uids = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
		return text, uids

	def get_undermines_for_premises(self, premises_as_statements_uid):
		"""

		:param premises_as_statements_uid:
		:param issue:
		:param key:
		:return:
		"""
		logger('QueryHelper', 'get_undermines_for_premises', 'main')
		return_array = []
		index = 0
		given_undermines = set()
		for s_uid in premises_as_statements_uid:
			logger('QueryHelper', 'get_undermines_for_premises', 'db_undermine against Argument.conclusion_uid=='+str(s_uid))
			db_undermine = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==False, Argument.conclusion_uid==s_uid)).all()
			for undermine in db_undermine:
				if undermine.premisesGroup_uid not in given_undermines:
					given_undermines.add(undermine.premisesGroup_uid)
					logger('QueryHelper', 'get_undermines_for_premises', 'found db_undermine ' + str(undermine.uid))
					tmp_dict = dict()
					tmp_dict['id'] = undermine.uid
					tmp_dict['text'], uids = QueryHelper().get_text_for_premisesGroup_uid(undermine.premisesGroup_uid)
					return_array.append(tmp_dict)
					index += 1
		return return_array

	def get_undermines_for_argument_uid(self, argument_uid):
		"""
		Calls get_undermines_for_premises('reason', premises_as_statements_uid)
		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(argument_uid))
		db_attacked_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_attacked_premises = DBDiscussionSession.query(Premise).filter_by(
				premisesGroup_uid=db_attacked_argument.premisesGroup_uid).order_by(
				Premise.premisesGroup_uid.desc()).all()

		premises_as_statements_uid = set()
		for premise in db_attacked_premises:
			premises_as_statements_uid.add(premise.statement_uid)
			logger('QueryHelper', 'get_undermines_for_argument_uid', 'db_attacked_argument has pgroup with pgroup ' +
		           str(premise.premisesGroup_uid) + ', statement ' + str(premise.statement_uid))

		if len(premises_as_statements_uid) == 0:
			return None

		return self.get_undermines_for_premises(premises_as_statements_uid)

	def get_overbids_for_argument_uid(self, argument_uid):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, True)
		:param argument_uid: uid of the specified argument
		:param issue:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_overbids_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(argument_uid, True)

	def get_undercuts_for_argument_uid(self, argument_uid):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, False)
		:param argument_uid:
		:param key:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'get_undercuts_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(argument_uid, False)

	def get_rebuts_for_arguments_conclusion_uid(self, conclusion_statements_uid, is_current_argument_supportive):
		"""

		:param conclusion_statements_uid:
		:param is_current_argument_supportive:
		:param issue:
		:return:
		"""
		return_array = []
		given_rebuts = set()
		index = 0
		logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'conclusion_statements_uid ' + str(conclusion_statements_uid)
		       + ', is_current_argument_supportive ' + str(is_current_argument_supportive) + ' (searching for the opposite)')
		db_rebut = DBDiscussionSession.query(Argument).filter(Argument.isSupportive==(not is_current_argument_supportive),
		                                                      Argument.conclusion_uid==conclusion_statements_uid).all()
		for rebut in db_rebut:
			if rebut.premisesGroup_uid not in given_rebuts:
				given_rebuts.add(rebut.premisesGroup_uid)
				logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'found db_rebut ' + str(rebut.uid))
				tmp_dict = dict()
				tmp_dict['id'] = rebut.uid
				tmp_dict['text'], trash = self.get_text_for_premisesGroup_uid(rebut.premisesGroup_uid)
				return_array.append(tmp_dict)
				index += 1

		return return_array

	def get_rebuts_for_argument_uid(self, argument_uid):
		"""
		Calls self.get_rebuts_for_arguments_conclusion_uid('reason', Argument.conclusion_uid)
		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_rebuts_for_argument_uid', 'main')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=int(argument_uid)).first()
		if not db_argument:
			return None
		return self.get_rebuts_for_arguments_conclusion_uid(db_argument.conclusion_uid, db_argument.isSupportive)

	def get_supports_for_argument_uid(self, argument_uid):
		"""

		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_supporRects_for_argument_uid', 'main')

		return_array = []
		given_supports = set()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).join(
			PremiseGroup).first()
		db_arguments_premises = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=db_argument.premisesGroup_uid).all()
		index = 0

		for arguments_premises in db_arguments_premises:
			db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==arguments_premises.statement_uid,
			                                                              Argument.isSupportive==True)).join(PremiseGroup).all()
			if not db_supports:
				continue

			for support in db_supports:
				if support.premisesGroup_uid not in given_supports:
					tmp_dict = dict()
					tmp_dict['id'] = support.uid
					tmp_dict['text'], trash = self.get_text_for_premisesGroup_uid(support.premisesGroup_uid)
					return_array.append(tmp_dict)
					index += 1
					given_supports.add(support.premisesGroup_uid)

		return None if len(return_array) == 0 else return_array

	def get_attack_or_support_for_justification_of_argument_uid(self, argument_uid, is_supportive):
		"""

		:param key:
		:param argument_uid:
		:param is_supportive:
		:param issue:
		:return:
		"""
		return_array = []
		logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid=='+str(argument_uid))
		db_relation = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==is_supportive,
		                                                              Argument.argument_uid==argument_uid)).all()
		given_relations = set()
		index = 0

		if not db_relation:
			return None

		for relation in db_relation:
			if relation.premisesGroup_uid not in given_relations:
				given_relations.add(relation.premisesGroup_uid)
				logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
						'found relation, argument uid ' + str(relation.uid))
				tmp_dict = dict()
				tmp_dict['id'] = relation.uid
				tmp_dict['text'], trash = self.get_text_for_premisesGroup_uid(relation.premisesGroup_uid)
				return_array.append(tmp_dict)
				index += 1
		return return_array

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

	# new part

	def get_id_of_slug(self, slug, request):
		"""
		Returns the uid
		:param slug: slug
		:param request: self.request for a fallback
		:return: uid
		"""
		db_issues = DBDiscussionSession.query(Issue).all()
		for issue in db_issues:
			if str(slugify(issue.title)) == str(slug):
				return issue.uid
		return self.get_issue(request)

	def get_title_for_issue_uid(self, id):
		"""
		Returns the title or none for the issue id
		:param id: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=id).first()
		return db_issue.title if db_issue else 'none'

	def get_slug_for_issue_uid(self, id):
		"""
		Returns the slug of the title or none for the issue id
		:param id: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=id).first()
		return slugify(db_issue.title) if db_issue else 'none'

	def get_info_for_issue_uid(self, id):
		"""
		Returns the slug or none for the issue id
		:param id: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=id).first()
		return db_issue.info if db_issue else 'none'

	def get_date_for_issue_uid(self, id, lang):
		"""
		Returns the date or none for the issue id
		:param id: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=id).first()
		return self.sql_timestamp_pretty_print(str(db_issue.date), lang) if db_issue else 'none'

	def prepare_json_of_issue(self, id, lang):
		"""
		Prepares slug, info, argument count and the date of the issue as dict
		:param id: Issue.uid
		:param lang: String
		:return: dict()
		"""
		slug = self.get_slug_for_issue_uid(id)
		title = self.get_title_for_issue_uid(id)
		info = self.get_info_for_issue_uid(id)
		arg_count = self.get_number_of_arguments(id)
		date = self.get_date_for_issue_uid(id, lang)

		db_issues = DBDiscussionSession.query(Issue).all()
		all_array = []
		for issue in db_issues:
			issue_dict = dict()
			issue_dict['slug']      = issue.get_slug()
			issue_dict['title']     = issue.title
			issue_dict['url']       = UrlManager(issue.get_slug()).get_slug_url(True)
			issue_dict['info']      = issue.info
			issue_dict['arg_count'] = self.get_number_of_arguments(issue.uid)
			issue_dict['date']      = self.sql_timestamp_pretty_print(str(issue.date), lang)
			issue_dict['enabled']   = 'disabled' if str(id) == str(issue.uid) else 'enabled'
			all_array.append(issue_dict)

		return {'slug': slug, 'info': info, 'title': title, 'id': id, 'arg_count': arg_count, 'date': date, 'all': all_array}

	def prepare_discussion_dict(self, uid, lang, at_start=False, at_attitude=False, at_justify=False,
	                            is_supportive=False, at_dont_know=False, at_argumentation=False,
	                            at_justify_argumentation=False, additional_id=0, attack='', logged_in=False):
		"""

		:param uid:
		:param lang:
		:param at_start:
		:param at_attitude:
		:param at_justify:
		:param is_supportive:
		:param at_dont_know:
		:param at_argumentation:
		:param additional_id:
		:param attack:
		:return:
		"""
		_tn              = Translator(lang)
		heading          = ''
		add_premise_text = ''
		if at_start:
			logger('QueryHelper', 'prepare_discussion_dict', 'at_start')
			heading             = _tn.get(_tn.initialPositionInterest)

		elif at_attitude:
			logger('QueryHelper', 'prepare_discussion_dict', 'at_attitude')
			text                = self.get_text_for_statement_uid(uid)
			if not text:
				return None
			heading             = _tn.get(_tn.whatDoYouThinkAbout) + ' <strong>' + text[0:1].lower() + text[1:] + '</strong>?'

		elif at_justify:
			logger('QueryHelper', 'prepare_discussion_dict', 'at_justify')
			text                = self.get_text_for_statement_uid(uid)
			if not text:
				return None
			heading             = _tn.get(_tn.whyDoYouThinkThat) + ' <strong>' + text[0:1].lower() + text[1:] + '</strong> ' \
			                        + _tn.get(_tn.isTrue if is_supportive else _tn.isFalse) + '?'
			add_premise_text    = text

		elif at_justify_argumentation:
			logger('QueryHelper', 'prepare_discussion_dict', 'at_justify_argumentation')
			_tg = TextGenerator(lang)
			db_argument         = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
			confrontation       = self.get_text_for_argument_uid(uid, lang)
			premise, tmp        = self.get_text_for_premisesGroup_uid(uid)
			conclusion          = self.get_text_for_statement_uid(db_argument.conclusion_uid) if db_argument.conclusion_uid != 0 \
				else self.get_text_for_argument_uid(db_argument.argument_uid, lang)
			heading             = _tg.get_header_for_confrontation_response(confrontation, premise, attack, conclusion, False, is_supportive, logged_in)
			add_premise_text    = _tg.get_text_for_add_premise_container(confrontation, premise, attack, conclusion, is_supportive)

		elif at_dont_know:
			logger('QueryHelper', 'prepare_discussion_dict', 'at_dont_know')
			text                = self.get_text_for_argument_uid(uid, lang)
			if text:
				heading         = _tn.get(_tn.otherParticipantsThinkThat) + ' <strong>' + text[0:1].lower() + text[1:] \
			                     + '</strong>. ' + '<br><br>' + _tn.get(_tn.whatDoYouThinkAboutThat) + '?'
			else:
				heading         = _tn.get(_tn.firstOneText) + ' <strong>' + self.get_text_for_statement_uid(additional_id) + '</strong>.'

		elif at_argumentation:
			logger('QueryHelper', 'prepare_discussion_dict', 'at_argumentation')
			_tg                 = TextGenerator(lang)
			db_argument         = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
			if attack == 'end':
				heading             = _tn.get(_tn.sentencesOpenersForArguments[0])\
				                      + ': <strong>' + self.get_text_for_argument_uid(uid, lang) + '</strong>.'\
				                      + '<br><br>' + _tn.get(_tn.otherParticipantsDontHaveCounterForThat)\
				                      + '.<br><br>' + _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndText)
			else:
				premise, tmp        = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
				conclusion          = self.get_text_for_statement_uid(db_argument.conclusion_uid) if db_argument.conclusion_uid != 0 \
					else self.get_text_for_argument_uid(db_argument.argument_uid)
				confrontation       = self.get_text_for_argument_uid(additional_id, lang)
				logger('QueryHelper', 'prepare_discussion_dict', 'additional_id ' + str(additional_id) + ', confrontation '
				       + str(confrontation) + ', attack ' + str(attack))

				reply_for_argument  = True
				current_argument    = self.get_text_for_argument_uid(uid, lang)
				heading             = _tg.get_text_for_confrontation(premise, conclusion, is_supportive, attack,
			                                                     confrontation, reply_for_argument, current_argument)

		return {'heading': heading, 'add_premise_text': add_premise_text}

	def prepare_item_dict_for_start(self, issue_uid, logged_in, lang):
		"""

		:param issue_uid:
		:param logged_in:
		:param lang:
		:return:
		"""
		db_statements = DBDiscussionSession.query(Statement)\
			.filter(and_(Statement.isStartpoint==True, Statement.issue_uid==issue_uid))\
			.join(TextVersion, TextVersion.uid==Statement.textversion_uid).all()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()

		statements_array = []
		_um = UrlManager(slug)

		if db_statements:
			for statement in db_statements:
				statements_array.append(self.get_statement_dict(statement.uid,
				                                                self.get_text_for_statement_uid(statement.uid),
				                                                [{'title': self.get_text_for_statement_uid(statement.uid), 'id': statement.uid}],
				                                                '',
				                                                _um.get_url_for_statement_attitude(True, statement.uid),
				                                                False))

			if logged_in:
				_tn = Translator(lang)
				statements_array.append(self.get_statement_dict('start_statement',
				                                                _tn.get(_tn.newConclusionRadioButtonText),
				                                                [{'title': _tn.get(_tn.newConclusionRadioButtonText), 'id': 0}],
				                                                'null',
				                                                'null',
				                                                False))

		return statements_array

	def prepare_item_dict_for_attitude(self, statement_uid, issue_uid, lang):
		"""

		:param statement_uid:
		:param issue_uid:
		:param url:
		:param lang:
		:return:
		"""
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		text = self.get_text_for_statement_uid(statement_uid)
		statements_array = []
		_um = UrlManager(slug)

		_tn = Translator(lang)

		statements_array.append(self.get_statement_dict('agree',
		                                                _tn.get(_tn.iAgreeWithInColor) + ': ' + text,
		                                                [{'title': _tn.get(_tn.iAgreeWithInColor) + ' ' + text, 'id': 'agree'}],
		                                                'agree', _um.get_url_for_justifying_statement(True, statement_uid, 't'),
		                                                False))
		statements_array.append(self.get_statement_dict('disagree',
		                                                _tn.get(_tn.iDisagreeWithInColor) + ': ' + text,
		                                                [{'title': _tn.get(_tn.iDisagreeWithInColor) + ' ' + text, 'id': 'disagree'}],
		                                                'disagree', _um.get_url_for_justifying_statement(True, statement_uid, 'f'),
		                                                False))
		statements_array.append(self.get_statement_dict('dontknow',
		                                                _tn.get(_tn.iDoNotKnowInColor) + ': ' + text,
		                                                [{'title': _tn.get(_tn.iDoNotKnowInColor) + ' ' + text, 'id': 'dontknow'}],
		                                                'dontknow', _um.get_url_for_justifying_statement(True, statement_uid, 'd'),
		                                                False))

		return statements_array

	def prepare_item_dict_for_justify_statement(self, statement_uid, issue_uid, isSupportive, lang):
		"""

		:param statement_uid:
		:param issue_uid:
		:param isSupportive:
		:param lang:
		:return:
		"""
		statements_array = []
		_tn = Translator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==isSupportive,
		                                                               Argument.conclusion_uid==statement_uid)).all()

		_um = UrlManager(slug)

		if db_arguments:
			for argument in db_arguments:
				# get all premises in the premisegroup of this argument
				db_premises = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=argument.premisesGroup_uid).all()
				premise_array = []
				for premise in db_premises:
					text = self.get_text_for_statement_uid(premise.statement_uid)
					premise_array.append({'title': text, 'id': premise.statement_uid})

				text, uid = self.get_text_for_premisesGroup_uid(argument.premisesGroup_uid)

				# get attack for each premise, so the urls will be unique
				arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(argument.uid, issue_uid, self)
				statements_array.append(self.get_statement_dict(str(argument.uid),
				                                                text,
				                                                premise_array, 'justify',
				                                                _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys),
				                                                True))

			statements_array.append(self.get_statement_dict('start_premise',
			                                                _tn.get(_tn.newPremiseRadioButtonText),
			                                                [{'title': _tn.get(_tn.newPremiseRadioButtonText), 'id':0}],
			                                                'null',
			                                                'null',
			                                                False))

		return statements_array

	def prepare_item_dict_for_justify_argument(self, argument_uid, attack_type, issue_uid, isSupportive, lang):
		"""

		:param argument_uid:
		:param attack_type:
		:param issue_uid:
		:param lang:
		:return:
		"""
		statements_array = []
		_tn = Translator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()

		db_arguments = []
		if attack_type == 'undermine':
			db_premisses = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=db_argument.premisesGroup_uid).all()
			for premise in db_premisses:
				arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==premise.statement_uid, Argument.isSupportive==False)).all()
				db_arguments = db_arguments + arguments

		elif attack_type == 'undercut':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.argument_uid==argument_uid, Argument.isSupportive==False)).all()

		elif attack_type == 'overbid':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.argument_uid==argument_uid, Argument.isSupportive==True)).all()

		elif attack_type == 'rebut':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==db_argument.conclusion_uid, Argument.isSupportive==False)).all()

		_um = UrlManager(slug)

		if db_arguments:
			for argument in db_arguments:
				text, tmp = self.get_text_for_premisesGroup_uid(argument.premisesGroup_uid)

				# get alles premises in this group
				db_premises = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=argument.premisesGroup_uid).all()
				premises_array = []
				for premise in db_premises:
					premise_dict = dict()
					premise_dict['id'] = premise.statement_uid
					premise_dict['title'] = self.get_text_for_statement_uid(premise.statement_uid)
					premises_array.append(premise_dict)

				# for each justifying premise, we need a new confrontation:
				arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(argument_uid, issue_uid, self)

				statements_array.append(self.get_statement_dict(argument.uid,
				                                                text,
				                                                premises_array,
				                                                'justify',
				                                                _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys),
				                                                True))

			statements_array.append(self.get_statement_dict('justify_premise',
			                                                _tn.get(_tn.newPremiseRadioButtonText),
			                                                [{'id': '0', 'title': _tn.get(_tn.newPremiseRadioButtonText)}],
			                                                'null',
			                                                'null',
			                                                False))


		return statements_array

	def prepare_item_dict_for_reaction(self, argument_uid, isSupportive, issue_uid, lang):
		"""

		:param argument_uid:
		:param isSupportive:
		:param issue_uid:
		:param lang:
		:return:
		"""
		_tg  = TextGenerator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		statements_array = []

		if db_argument:
			if db_argument.argument_uid == 0:
				conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid)
			else:
				conclusion = self.get_text_for_argument_uid(db_argument.argument_uid, lang)

			premise, tmp     = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
			conclusion       = conclusion[0:1].lower() + conclusion[1:]
			premise          = premise[0:1].lower() + premise[1:]
			ret_dict         = _tg.get_relation_text_dict_without_confrontation(conclusion, premise, False, True)
			mode             = 't' if isSupportive else 't'
			_um              = UrlManager(slug)

			types = ['undermine', 'support', 'undercut', 'overbid', 'rebut', 'no_opinion']
			for t in types:
				# special case, when the user selectes the support, because this does not need to be justified!
				if t == 'support':
					arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(argument_uid, issue_uid, self)
					url = _um.get_url_for_reaction_on_argument(True, argument_uid, attack, arg_id_sys)
				else:
					url = _um.get_url_for_justifying_argument(True, argument_uid, mode, t) if t != 'no_opinion' else 'window.history.go(-1)'
				statements_array.append(self.get_statement_dict(t, ret_dict[t + '_text'], [{'title': ret_dict[t + '_text'], 'id':t}], t, url, False))

		return statements_array

	def add_discussion_end_text(self, discussion_dict, extras_dict, logged_in, lang, at_dont_know=False, at_justify_argumentation=False, at_justify=False):
		"""

		:param discussion_dict:
		:param logged_in:
		:param lang:
		:return:
		"""
		_t = Translator(lang)
		discussion_dict['heading'] += '<br><br>'
		if at_justify_argumentation:
			extras_dict['add_premise_container_style'] = '' # this will remove the 'display: none;'-style
			extras_dict['show_display_style'] = False
		elif at_dont_know:
			discussion_dict['heading'] += _t.get(_t.otherParticipantsDontHaveOpinion) + '<br><br>' + (_t.get(_t.discussionEnd) + ' ' + _t.get(_t.discussionEndText))
		elif at_justify:
			discussion_dict['heading'] += '?????'
		else:
			discussion_dict['heading'] += (_t.get(_t.discussionEnd) + ' ' + _t.get(_t.discussionEndText)) if logged_in else _t.get(_t.discussionEndFeelFreeToLogin)

	def prepare_extras_dict(self, current_slug, is_editable, is_reportable, show_bar_icon, show_display_styles, lang, authenticated_userid, add_premise_supportive=False, argument_id=0):
		"""

		:param current_slug:
		:param is_editable:
		:param is_reportable:
		:param show_bar_icon:
		:param show_display_styles:
		:param add_premise_supportive:
		:param authenticated_userid:
		:return:
		"""
		_uh = UserHandler()
		_tn = Translator(lang)
		return_dict = dict()
		return_dict['restart_url']                   =  UrlManager(current_slug).get_slug_url(True)
		return_dict['is_editable']                   =  is_editable and _uh.is_user_logged_in(authenticated_userid)
		return_dict['is_reportable']                 =  is_reportable
		return_dict['is_admin']                      =  _uh.is_user_admin(authenticated_userid)
		return_dict['logged_in']                     =  authenticated_userid
		return_dict['show_bar_icon']                 =  show_bar_icon
		return_dict['show_display_style']            =  show_display_styles
		return_dict['add_premise_supportive']        =  add_premise_supportive
		return_dict['add_premise_container_style']   = 'display: none'
		return_dict['add_statement_container_style'] = 'display: none'
		return_dict['title']                         = {'barometer': _tn.get(_tn.opinionBarometer),
													 	 'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
													 	 'island_view': _tn.get(_tn.displayControlDialogIslandBody),
													 	 'expert_view': _tn.get(_tn.displayControlDialogExpertBody),
		                                                 'edit_statement': _tn.get(_tn.editTitle),
		                                                 'report_statement': _tn.get(_tn.reportTitle)}


		# add everything for the island view
		if show_display_styles:
			# does an argumente exists?
			if (DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()):
				island_dict = self.get_everything_for_island_view(argument_id, lang)
				island_dict['premise'] = island_dict['premise'][0:1].lower() + island_dict['premise'][1:]
				island_dict['conclusion'] = island_dict['conclusion'][0:1].lower() + island_dict['conclusion'][1:]
				island_dict.update(TextGenerator(lang).get_relation_text_dict_without_confrontation(island_dict['premise'],
				                                                                                    island_dict['conclusion'],
				                                                                                    False, False))
				return_dict['island'] = island_dict
			else:
				return_dict['is_editable']            =  False
				return_dict['is_reportable']          =  False
				return_dict['show_bar_icon']          =  False
				return_dict['show_display_style']     =  False
				return_dict['title']                  = {'barometer': _tn.get(_tn.opinionBarometer),
												        'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
												        'island_view': _tn.get(_tn.displayControlDialogIslandBody),
												        'expert_view': _tn.get(_tn.displayControlDialogExpertBody),
		                                                'edit_statement': _tn.get(_tn.editTitle),
		                                                'report_statement': _tn.get(_tn.reportTitle)}


		return return_dict

	def get_everything_for_island_view(self, arg_uid, lang):
		"""

		:param arg_uid:
		:param lang:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'get_everything_for_island_view', 'def with arg_uid: ' + str(arg_uid))
		return_dict = {}
		_t = Translator(lang)

		undermine   = self.get_undermines_for_argument_uid(arg_uid)
		support     = self.get_supports_for_argument_uid(arg_uid)
		undercut    = self.get_undercuts_for_argument_uid(arg_uid)
		overbid     = self.get_overbids_for_argument_uid(arg_uid)
		rebut       = self.get_rebuts_for_argument_uid(arg_uid)

		undermine   = undermine if undermine else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		support     = support   if support   else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		undercut    = undercut  if undercut  else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		overbid     = overbid   if overbid   else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		rebut       = rebut     if rebut     else [{'id': 0, 'text': _t.get(_t.no_entry)}]

		return_dict.update({'undermine': undermine})
		return_dict.update({'support':   support})
		return_dict.update({'undercut':  undercut})
		return_dict.update({'overbid':   overbid})
		return_dict.update({'rebut':     rebut})

		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(undermine)) + ' undermines')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(support)) + ' supports')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(undercut)) + ' undercuts')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(overbid)) + ' overbids')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(rebut)) + ' rebuts')

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first()
		return_dict['premise'], tmp = self.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
		return_dict['conclusion'] = self.get_text_for_statement_uid(db_argument.conclusion_uid,) \
			if db_argument.conclusion_uid != 0 else \
			self.get_text_for_argument_uid(db_argument.argument_uid, lang)
		return_dict['heading'] = self.get_text_for_argument_uid(arg_uid, lang)

		return return_dict

	def get_language(self, request, current_registry):
		"""

		:param request: self.request
		:param current_registry: get_current_registry()
		:return: language abr
		"""
		try:
			lang = str(request.cookies['_LOCALE_'])
		except KeyError:
			lang = current_registry().settings['pyramid.default_locale_name']
		return lang

	def get_issue(self, request):
		"""
		Returns issue uid
		:param request: self.request
		:return: uid
		"""

		# first matchdict, then params, then session, afterwards fallback
		issue = request.matchdict['issue'] if 'issue' in request.matchdict \
			else request.params['issue'].split('=')[1] if 'issue' in request.params \
			else request.session['issue'] if 'issue' in request.session \
			else DBDiscussionSession.query(Issue).first().uid

		if str(issue) is 'undefined':
			self.issue_fallback = 1

		# save issue in session
		request.session['issue'] = issue
		logger('discussion_init', 'def', 'set session[issue] to ' + str(issue))

		return issue

	def get_statement_dict(self, id, title, premises, attitude, url, leading_because):
		if leading_because:
			title = title[0:1].lower() + title[1:]

		return {'id': id,
		        'title': title,
		        'premises': premises,
		        'attitude': attitude,
		        'url': url,
		        'leading_because': leading_because}

	def sql_timestamp_pretty_print(self, ts, lang):
		"""

		:param ts: timestamp as string
		:param lang: language
		:return:
		"""

		format = '%-I:%M %p, %d. %b. %Y'
		if lang == 'de':
			try:
				locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
				format = '%-H:%M Uhr, %d. %b. %Y'
			except:
				locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

		time = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

		return time.strftime(format)


class UrlManager(object):

	def __init__(self, slug=''):
		self.url = 'http://localhost:4284/'
		self.discussion_url = self.url + 'd/'
		self.slug = slug

	def get_404(self, params):
		"""

		:param params:
		:return:
		"""
		url = self.url + '404'
		for p in params:
			if p != '':
				url += '/' + p
		return url

	def get_slug_url(self, as_location_href):
		"""

		:param as_location_href:
		:return:
		"""
		url = self.discussion_url + (self.slug if self.slug != '' else '')
		return 'location.href="' + url + '"' if as_location_href else url

	def get_url_for_statement_attitude(self, as_location_href, statement_uid):
		"""

		:param as_location_href:
		:return: discussion_url/slug/a/statement_uid
		"""
		url = self.discussion_url +  self.slug + '/a/' + str(statement_uid)
		return 'location.href="' + url + '"' if as_location_href else url

	def get_url_for_justifying_statement(self, as_location_href, statement_uid, mode):
		"""

		:param as_location_href:
		:param statement_uid:
		:param mode:
		:return:
		"""
		url = self.discussion_url +  self.slug + '/j/' + str(statement_uid) + '/' + mode
		return 'location.href="' + url + '"' if as_location_href else url

	def get_url_for_justifying_argument(self, as_location_href, argument_uid, mode, attitude):
		"""

		:param as_location_href:
		:param argument_uid:
		:param mode:
		:param attitude:
		:return:
		"""
		url = self.discussion_url +  self.slug + '/j/' + str(argument_uid) + '/' + mode + '/' + attitude
		return 'location.href="' + url + '"' if as_location_href else url

	def get_url_for_reaction_on_argument(self, as_location_href, argument_uid, mode, confrontation_argument):
		"""

		:param as_location_href:
		:param argument_uid:
		:param mode: 't' on supportive, 'f' otherwise
		:param confrontation_argument:
		:return:
		"""
		url = self.discussion_url + self.slug + '/r/' + str(argument_uid) + '/' + mode + '/' + str(confrontation_argument)
		return 'location.href="' + url + '"' if as_location_href else url

