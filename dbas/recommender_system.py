import random

from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Premise, User, Statement
from .logger import logger
from .query_helper import QueryHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

# This class handles attacks

class RecommenderHelper(object):

	def get_attack_for_argument(self, argument_uid, issue):
		# getting undermines or undercuts or rebuts
		attacks, key = self.__get_attack_for_argument_by_random(argument_uid, issue)

		if not attacks or len(attacks) == 0:
			logger('RecommenderHelper', 'get_attack_for_argument_old', 'there is no attack!')
			return 0, ''
		else:
			attack_no = random.randrange(0, len(attacks)) # Todo fix random

			return attacks[attack_no]['id'], key

	def get_argument_by_conclusion(self, statement_uid, isSupportive):
		"""

		:param statement_uid:
		:param isSupportive:
		:return:
		"""
		logger('RecommenderHelper', 'get_argument_by_conclusion', 'statement: ' + str(statement_uid) + ', supportive: ' + str(isSupportive))
		db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == isSupportive,
		                                                               Argument.conclusion_uid == statement_uid)).all()
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

	def __get_attack_for_argument_by_random(self, argument_uid, issue):
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
		return_dict, key = self.__get_attack_for_argument_by_random_in_range(argument_uid, attack_list, issue, complete_list_of_attacks)

		# sanity check if we could not found an attack for a left attack in out set
		if not return_dict and len(attacks) > 0:
			logger('RecommenderHelper', '__get_attack_for_argument_by_random_old', 'no attack found, try to find an attack for any other left attack')
			return_dict, key = self.__get_attack_for_argument_by_random_in_range(argument_uid, [], issue, complete_list_of_attacks)

		return return_dict, key

	def __get_attack_for_argument_by_random_in_range(self, argument_uid, attack_list, issue, complete_list_of_attacks):
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
		_qh = QueryHelper

		logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'attack_list : ' + str(attack_list))
		logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'complete_list_of_attacks : ' + str(complete_list_of_attacks))
		logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', 'left_attacks : ' + str(left_attacks))

		# randomize at least 1, maximal 3 times for getting an attack
		while len(attack_list) > 0:
			attack = random.choice(attack_list)
			attack_list.remove(attack)
			logger('RecommenderHelper', '__get_attack_for_argument_by_random_in_range', '\'random\' attack is ' + str(attack))

			return_dict = _qh.get_undermines_for_argument_uid(argument_uid) if attack == 1 \
				else (_qh.get_rebuts_for_argument_uid(argument_uid)  if attack == 5
				      else _qh.get_undercuts_for_argument_uid(argument_uid))
			key = 'undermine' if attack == 1 \
				else ('rebut' if attack == 5
				      else 'undercut')

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

	def __get_best_argument(self, argument_list):
		"""

		:param argument_list: Argument[]
		:return: Argument
		"""
		logger('RecommenderHelper', '__get_best_argument', 'main')
		evaluations = []
		for argument in argument_list:
			evaluations.append(self.__evaluate_argument(argument.uid))

		best = max(evaluations)
		index = [i for i, j in enumerate(evaluations) if j == best]
		logger('RecommenderHelper', '__get_best_argument', 'index ' + str(index))
		return index[0]

	def __evaluate_argument(self, argument_uid):
		"""

		:param argument_uid: Argument.uid
		:return:
		"""
		logger('RecommenderHelper', '__evaluate_argument', 'argument ' + str(argument_uid))

		db_votes = DBDiscussionSession.query(Vote).filter_by(argument_uid=argument_uid).all()
		db_valid_votes   = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==argument_uid,
		                                                               Vote.isValid==true)).all()
		db_valid_upvotes = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==argument_uid,
		                                                               Vote.isValid==True,
		                                                               Vote.isUpVote==True)).all()
		index_up_vs_down = len(db_valid_upvotes) / len(db_valid_votes)
		index_participation = len(db_votes) / len(DBDiscussionSession.query(User).all())

		return index_participation, index_up_vs_down