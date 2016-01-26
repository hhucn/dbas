import random

from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Premise, User, Track, Statement
from .logger import logger
#from .tracking_helper import TrackingHelper
from .dictionary_helper import DictionaryHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

# This class handles attacks

class RecommenderHelper(object):

	def get_attack_for_argument(self, argument_uid, issue, queryHelper=None):
		# getting undermines or undercuts or rebuts
		attacks, key = self.__get_attack_for_argument_by_random(argument_uid, issue, queryHelper)

		if not attacks or len(attacks) == 0:
			logger('RecommenderHelper', 'get_attack_for_argument_old', 'there is no attack!')
			return 0, ''
		else:
			attack_no = random.randrange(0, len(attacks)) # Todo fix random

			return attacks[attack_no]['id'], key

	def __get_attack_for_argument_by_random(self, argument_uid, issue, queryHelper=None):
		"""
		Returns a dictionary with attacks. The attack itself is random out of the set of attacks, which were not done yet.
		Additionally returns id's of premises groups with [key + str(index) + 'id']
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
		# all possible attacks

		complete_list_of_attacks = [1,3,5] # todo fix this, when overbid is killed
		attacks = [1,3,5]

		logger('RecommenderHelper', '__get_attack_for_argument_by_random_old', 'attack_list : ' + str(attacks))
		attack_list = complete_list_of_attacks if len(attacks) == 0 else attacks
		return_dict, key = self.__get_attack_for_argument_by_random_in_range(argument_uid, attack_list, issue, complete_list_of_attacks, queryHelper)

		# sanity check if we could not found an attack for a left attack in out set
		if not return_dict and len(attacks) > 0:
			logger('RecommenderHelper', '__get_attack_for_argument_by_random_old', 'no attack found, try to find an attack for any other left attack')
			return_dict, key = self.__get_attack_for_argument_by_random_in_range(argument_uid, [], issue, complete_list_of_attacks, queryHelper)

		return return_dict, key

	def __get_attack_for_argument_by_random_in_range(self, argument_uid, attack_list, issue, complete_list_of_attacks, queryHelper=None):
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
		if not queryHelper:
			from .query_helper import QueryHelper
			queryHelper = QueryHelper()

		logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'attack_list : ' + str(attack_list))
		logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'complete_list_of_attacks : ' + str(complete_list_of_attacks))
		logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'left_attacks : ' + str(left_attacks))

		# randomize at least 1, maximal 3 times for getting an attack
		while len(attack_list) > 0:
			attack = random.choice(attack_list)
			attack_list.remove(attack)
			logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', '\'random\' attack is ' + str(attack))
			if attack == 1:
				return_dict = queryHelper.get_undermines_for_argument_uid(argument_uid)
				key = 'undermine'
			elif attack == 5:
				return_dict = queryHelper.get_rebuts_for_argument_uid(argument_uid)
				key = 'rebut'
			else:
				return_dict = queryHelper.get_undercuts_for_argument_uid(argument_uid)
				key = 'undercut'

			if return_dict and len(return_dict) != 0:
				logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'attack found')
				attack_found = True
				break
			else:
				logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'no attack found')

		if len(left_attacks) > 0 and not attack_found:
			logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'redo algo with left attacks ' + str(left_attacks))
			return_dict, key = self.__get_attack_for_argument_by_random_in_range(argument_uid, left_attacks, issue, left_attacks)
		else:
			logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'no attacks left for redoing')

		return return_dict, key

	def get_premises_for_statement(self, transaction, statement_uid, isSupportive, user, session_id, issue):
		"""
		Returns all premises for the given statement
		:param transaction: current transaction
		:param statement_uid: uid of the statement
		:param isSupportive: boolean
		:param user: self.request.authenticated_userid
		:param session_id: self.request.session.id
		:param issue: current issue
		:return: dictionary
		"""
		#TrackingHelper().save_track_for_user(transaction, user, statement_uid, 0, 0, 0, 0, session_id)

		return_dict = dict()
		premises_dict = dict()
		logger('RecommenderHelper', 'get_premises_for_statement', 'get all premises: conclusion_uid: '+ str(statement_uid)
		       + ', isSupportive: ' + str(isSupportive)
		       + ', issue_uid: ' + str(issue))
		db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==isSupportive,
																Argument.conclusion_uid==statement_uid,
		                                                        Argument.issue_uid==issue)).all()

		for argument in db_arguments:
			logger('RecommenderHelper', 'get_premises_for_statement', 'argument ' + str(argument.uid) + ' ('
			       + str(argument.premisesGroup_uid) + '), issue ' + str(issue))
			db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==argument.premisesGroup_uid,
			                                                             Premise.issue_uid==issue)).all()

			# check out the group
			premisesgroups_dict = dict()
			for premise in db_premises:
				logger('RecommenderHelper', 'get_premises_for_statement', 'premises group ' + str(premise.premisesGroup_uid))
				db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==premise.statement_uid,
				                                                                 Statement.issue_uid==issue)).all()
				for statement in db_statements:
					logger('RecommenderHelper', 'get_premises_for_statement', 'premises group has statement ' + str(statement.uid))
					premisesgroups_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement)

				logger('RecommenderHelper', 'get_premises_for_statement', 'new premises_dict entry with key ' + str(premise.premisesGroup_uid))
				premises_dict[str(premise.premisesGroup_uid)] = premisesgroups_dict # TODO limit the number to 5

		# premises dict has for each group a new dictionary
		return_dict['premises'] = premises_dict
		return_dict['conclusion_id'] = statement_uid
		return_dict['status'] = '1'

		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		return_dict['currentStatement'] = DictionaryHelper().save_statement_row_in_dictionary(db_statement)

		return return_dict

	def get_argument_by_conclusion(self, statement_uid, isSupportive):
		"""

		:param statement_uid:
		:param isSupportive:
		:return:
		"""
		logger('RecommenderHelper', 'get_argument_by_conclusion', 'statement: ' + str(statement_uid) + ', supportive: ' + str(isSupportive))
		db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==isSupportive,
																Argument.conclusion_uid==statement_uid)).all()
		logger('RecommenderHelper', 'get_argument_by_conclusion', 'found ' + str(len(db_arguments)) + ' arguments')
		if db_arguments:
			arguments = []
			for argument in db_arguments:
				arguments.append(argument.uid)
			# get one random premise todo fix random
			rnd = random.randint(0, len(arguments) - 1)
			logger('RecommenderHelper', 'get_argument_by_conclusion', 'rnd ' + str(rnd))
			return arguments[0 if len(arguments) == 1 else rnd]

		else:
			return 0

	def __evaluate_argument(self, argument_uid):
		"""

		:param argument_uid:
		:return:
		"""
		logger('RecommenderHelper', '__evaluate_argument', 'argument ' + str(argument_uid))

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		# db_weight =
		# todo this
