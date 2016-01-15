import random

from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Premise, User, Track, Statement
from .query_helper import QueryHelper
from .logger import logger
from .tracking_helper import TrackingHelper
from .dictionary_helper import DictionaryHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

# This class handles attacks

class RecommenderHelper(object):

	def get_attack_or_support_for_premisegroup(self, transaction, user, last_premises_group_uid, last_statement_uid,
	                                           session_id, supportive, issue):
		"""
		Based on the last given premisesgroup and statement, an attack will be choosen and replied.
		:param transaction: current transaction
		:param user: current nick of the user
		:param last_premises_group_uid:
		:param last_statement_uid:
		:param session_id:
		:param supportive:
		:param issue:
		:return: A random attack (undermine, rebut undercut) based on the last saved premisesgroup and statement as well as many texts
		like the premise as text, conclusion as text, attack as text, confrontation as text. Everything is in a dict.
		"""

		logger('RecommenderHelper', 'get_attack_for_premisegroup', 'def')

		return_dict = dict()
		qh = QueryHelper()
		# get premises and conclusion as text
		return_dict['premise_text'], premises_as_statements_uid = qh.get_text_for_premisesGroup_uid(last_premises_group_uid, issue)
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(last_statement_uid, issue)

		# getting the argument of the premises and conclusion
		logger('RecommenderHelper', 'get_attack_for_premisegroup', 'find argument with group ' + str(last_premises_group_uid)
				+ ' conclusion statement ' + str(last_statement_uid)
		       + ', support ' + str(supportive))

		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==last_premises_group_uid,
		                                                              Argument.conclusion_uid==last_statement_uid,
		                                                              Argument.isSupportive==supportive,
		                                                              Argument.issue_uid==issue)).order_by(Argument.uid.desc()).first()

		# logging and ...
		logger('RecommenderHelper', 'get_attack_for_premisegroup', 'argument uid ' + (str(db_argument.uid) if db_argument else 'none'))
		return_dict['argument_id'] = str(db_argument.uid) if db_argument else '0'

		# getting undermines or undercuts or rebuts
		if not db_argument:
			attacks = None
			key = ''
		else:
			attacks, key = self.__get_attack_for_argument_by_random(db_argument, user, issue)
			return_dict['attack'] = key

		status = 1
		if not attacks or int(attacks[key]) == 0:
			logger('RecommenderHelper', 'get_attack_for_premisegroup', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key])))
			logger('RecommenderHelper', 'get_attack_for_premisegroup', 'attack with ' + attacks[key + str(attack_no)])
			logger('RecommenderHelper', 'get_attack_for_premisegroup', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_uid'] = attacks[key + str(attack_no) + 'id']
			return_dict['confrontation_argument_id'] = attacks[key + str(attack_no) + '_argument_id']
			return_dict['argument_uid'] = str(db_argument.uid)

			# save the attack
			TrackingHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                     qh.get_relation_uid_by_name(key), 0, session_id)

		return return_dict, status

	def get_attack_or_support_for_premisegroup_by_args(self, attack_with, attack_arg, pgroup, conclusion, issue):
		"""
		Same as get_attack_or_support_for_premisegroup, but more manually, without saving this attack
		:param attack_with:
		:param attack_arg:
		:param pgroup:
		:param conclusion:
		:param issue:
		:return:
		"""

		logger('RecommenderHelper', 'get_attack_for_premisegroup', 'attack_with: ' + attack_with
		       + ', attack_arg:' + attack_arg
		       + ', pgroup:' + pgroup
		       + ', conclusion:' + conclusion)
		return_dict = dict()
		status = '1'

		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==int(pgroup),
		                                                              Argument.conclusion_uid==int(conclusion))).first()

		#{'attack': 'undercut',
		##'argument_id': '1',
		##'conclusion_text': 'We should get a cat',
		##'premise_text': 'cats are very independent',
		##'confrontation': 'the purpose of a pet is to have something to take care of',
		# 'confrontation_uid': 17,
		##'confrontation_argument_id': 17}>

		return_dict['attack'] = attack_with
		return_dict['argument_id'] = str(db_argument.uid)
		return_dict['conclusion_text'] = QueryHelper().get_text_for_statement_uid(int(db_argument.conclusion_uid), issue)
		return_dict['premise_text'], tmp = QueryHelper().get_text_for_arguments_premisesGroup_uid(db_argument.uid, issue)
		return_dict['confrontation'], tmp = QueryHelper().get_text_for_arguments_premisesGroup_uid(int(attack_arg), issue)
		return_dict['confrontation_uid'] = attack_arg
		return_dict['confrontation_argument_id'] = attack_arg

		return return_dict, status

	def get_attack_for_argument_if_support(self, transaction, user, id_text, session_id, issue, lang):
		"""
		Returns an attack, if the id_text should refer to an argument and skips the justification part
		:param transaction: current transaction
		:param user: recent user
		:param id_text: text of the browser
		:param session_id: recent session id
		:param issue: current issue
		:param lang: given language
		:return: dict()
		"""
		logger('RecommenderHelper', 'get_attack_for_argument_if_support', 'extracting argument')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=int(id_text.split('_')[2])).first()
		return_dict = dict()
		qh = QueryHelper()

		return_dict['premise_text'], trash = qh.get_text_for_premisesGroup_uid(int(db_argument.premisesGroup_uid), issue)
		return_dict['premisesgroup_uid'] = db_argument.premisesGroup_uid
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_argument.conclusion_uid, issue) \
			if db_argument.conclusion_uid != 0 else qh.get_text_for_argument_uid(db_argument.argument_uid, issue, lang)
		return_dict['conclusion_uid'] = db_argument.conclusion_uid
		return_dict['relation'] = id_text.split('_')[0]

		# getting undermines or undercuts or rebuts
		attacks, key = self.__get_attack_for_argument_by_random(db_argument, user, issue)
		return_dict['attack'] = key

		status = 1
		if not attacks or int(attacks[key]) == 0:
			logger('RecommenderHelper', 'get_attack_for_argument_if_support', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key]))) # Todo fix random
			logger('RecommenderHelper', 'get_attack_for_argument_if_support', 'attack with ' + attacks[key + str(attack_no)])
			logger('RecommenderHelper', 'get_attack_for_argument_if_support', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_id'] = attacks[key + str(attack_no) + 'id']
			return_dict['confrontation_argument_id'] = attacks[key + str(attack_no) + '_argument_id']

			# save the attack
			TrackingHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                     qh.get_relation_uid_by_name(key), 0, session_id)

		logger('RecommenderHelper', 'get_attack_for_argument_by_ids_argument', str(return_dict))
		return return_dict, status

	def get_attack_for_argument(self, transaction, user, id_text, pgroup_id, session_id, issue):
		"""
		Returns an attack, if the id_text should refer to an argument and not skips the justification part
		:param transaction: current transaction
		:param user: recent user
		:param id_text: text of the browser
		:param pgroup_id: recent premisse group id
		:param session_id: recent session id
		:param issue: current issue
		:return: dict()
		"""

		logger('RecommenderHelper', 'get_attack_for_argument', 'main')

		qh = QueryHelper()
		splitted_id = id_text.split('_')
		relation = splitted_id[0]
		premisesgroup_uid = splitted_id[2]
		no_attacked_argument = False

		logger('RecommenderHelper', 'get_attack_for_argument', 'relation: ' + relation
		       + ', premisesgroup_uid: ' + premisesgroup_uid
		       + ', issue: ' + str(issue))

		# get latest conclusion
		logger('RecommenderHelper', 'get_attack_for_argument', 'get last premisesGroup_uid: ' + str(pgroup_id) + ', issue: ' + str(issue))
		db_last_conclusion = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==pgroup_id,
		                                                                    Premise.issue_uid==issue)).first()

		# get the non supportive argument
		logger('RecommenderHelper', 'get_attack_for_argument', 'get the non supportive argument: conclusion_uid=' +
		       str(db_last_conclusion.statement_uid) + ', premisesGroup_uid=' + premisesgroup_uid + ', isSupportive==False')
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==db_last_conclusion.statement_uid,
		                                                              Argument.premisesGroup_uid==int(premisesgroup_uid),
		                                                              Argument.issue_uid==issue)).first()

		# maybe there is no argument, whoch is not-supportive
		if not db_argument:
			logger('RecommenderHelper', 'get_attack_for_argument', 'no suitable non supportive argument')
			logger('RecommenderHelper', 'get_attack_for_argument', 'new try: conclusion_uid: ' +  str(db_last_conclusion.statement_uid)
			       + ', premisesGroup_uid: ' +  str(premisesgroup_uid) + ', issue_uid: ' +  str(issue))
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==db_last_conclusion.statement_uid,
			                                                              Argument.premisesGroup_uid==int(premisesgroup_uid),
			                                                              Argument.issue_uid==issue)).first()
			no_attacked_argument = True


		return_dict = dict()
		return_dict['premise_text'], trash = qh.get_text_for_premisesGroup_uid(int(premisesgroup_uid), issue)
		return_dict['premisesgroup_uid'] = premisesgroup_uid
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_last_conclusion.statement_uid, issue)
		return_dict['conclusion_uid'] = db_last_conclusion.statement_uid
		return_dict['relation'] = relation

		# if there as no non-supportive argument, let's get back
		if no_attacked_argument:
			logger('RecommenderHelper', 'get_attack_for_argument', 'no_attacked_argument, so return')
			return return_dict, 0
		else:
			return_dict['argument_uid'] = db_argument.uid


		# getting undermines or undercuts or rebuts
		attacks, key = self.__get_attack_for_argument_by_random(db_argument, user, issue)
		return_dict['attack'] = key

		status = 1
		if not attacks or int(attacks[key]) == 0:
			logger('RecommenderHelper', 'get_attack_for_argument', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key]))) # Todo fix random
			logger('RecommenderHelper', 'get_attack_for_argument', 'attack with ' + attacks[key + str(attack_no)])
			logger('RecommenderHelper', 'get_attack_for_argument', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_id'] = attacks[key + str(attack_no) + 'id']
			return_dict['confrontation_argument_id'] = attacks[key + str(attack_no) + '_argument_id']

			# save the attack
			TrackingHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                     qh.get_relation_uid_by_name(key), 0, session_id)

		return return_dict, status

	def __get_attack_for_argument_by_random(self, db_argument, user, issue):
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

		logger('QueryHelper', '__get_attack_for_argument_by_random', 'user ' + (user if user else 'anonymous') + ', arg.uid ' + str(db_argument.uid))

		# all possible attacks
		complete_list_of_attacks = [1,3,5] # todo fix this, when overbid is killed
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
				logger('QueryHelper', '__get_attack_for_argument_by_random', 'attacks, which were not done yet ' + str(attacks))

		logger('QueryHelper', '__get_attack_for_argument_by_random', 'attack_list : ' + str(attacks))
		attack_list = complete_list_of_attacks if len(attacks) == 0 else attacks
		return_dict, key = self.__get_attack_for_argument_by_random_in_range(db_argument.uid, attack_list, issue, complete_list_of_attacks)
		# sanity check if we could not found an attack for a left attack in out set
		if not return_dict and len(attacks) > 0:
			logger('QueryHelper', '__get_attack_for_argument_by_random', 'no attack found, try to find an attack for any other left attack')
			return_dict, key = self.__get_attack_for_argument_by_random_in_range(db_argument.uid, [], issue, complete_list_of_attacks)

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
		qh = QueryHelper()

		logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'attack_list : ' + str(attack_list))
		logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'complete_list_of_attacks : ' + str(complete_list_of_attacks))
		logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'left_attacks : ' + str(left_attacks))

		# randomize at least 1, maximal 3 times for getting an attack
		while len(attack_list) > 0:
			attack = random.choice(attack_list)
			attack_list.remove(attack)
			logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', '\'random\' attack is ' + str(attack))
			if attack == 1:
				return_dict = qh.get_undermines_for_argument_uid('undermine', argument_uid, issue)
				key = 'undermine'
			elif attack == 5:
				return_dict = qh.get_rebuts_for_argument_uid('rebut', argument_uid, issue)
				key = 'rebut'
			else:
				return_dict = qh.get_undercuts_for_argument_uid('undercut', argument_uid, issue)
				key = 'undercut'

			if return_dict and int(return_dict[key]) != 0:
				logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'attack found')
				attack_found = True
				break
			else:
				logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'no attack found')

		if len(left_attacks) > 0 and not attack_found:
			logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'redo algo with left attacks ' + str(left_attacks))
			return_dict, key = self.__get_attack_for_argument_by_random_in_range(argument_uid, left_attacks, issue, left_attacks)
		else:
			logger('QueryHelper', '__get_attack_for_argument_by_random_in_range', 'no attacks left for redoing')

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
		TrackingHelper().save_track_for_user(transaction, user, statement_uid, 0, 0, 0, 0, session_id)

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
					premisesgroups_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement, issue)

				logger('RecommenderHelper', 'get_premises_for_statement', 'new premises_dict entry with key ' + str(premise.premisesGroup_uid))
				premises_dict[str(premise.premisesGroup_uid)] = premisesgroups_dict # TODO limit the number to 5

		# premises dict has for each group a new dictionary
		return_dict['premises'] = premises_dict
		return_dict['conclusion_id'] = statement_uid
		return_dict['status'] = '1'

		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		return_dict['currentStatement'] = DictionaryHelper().save_statement_row_in_dictionary(db_statement, issue)

		return return_dict

	def get_premise_for_statement(self, transaction, statement_uid, isSupportive, user, session_id, issue):
		"""
		Returns one random premisses, which have a relation to this statement in the form of an argument
		:param transaction: transaction
		:param statement_uid: int
		:param isSupportive: boolean
		:param user: string
		:param session_id: id
		:param issue: int
		:return: dict()
		"""
		logger('RecommenderHelper', 'get_premise_for_statement', 'get all premisses: conclusion_uid: ' + str(statement_uid) + ', issue_uid: ' +
		       str(issue))

		return_dict = self.get_premises_for_statement(transaction, statement_uid, isSupportive, user, session_id, issue)

		# get one random premise todo fix random

		premises_dict = return_dict['premises']
		if len(premises_dict) == 0:
			logger('RecommenderHelper', 'get_premise_for_statement', 'no premisses')
			return_dict['premises'] = '0'
		else:
			logger('RecommenderHelper', 'get_premise_for_statement', 'found ' + str(len(premises_dict)) + ' premises')
			rnd_element = random.choice(list(premises_dict.keys()))
			logger('RecommenderHelper', 'get_premise_for_statement', 'rnd_element out of premise keys[' + str(list(premises_dict.keys())) + '] is ' + str(rnd_element))

			return_dict['premises'] = premises_dict[rnd_element]
			logger('RecommenderHelper', 'get_premise_for_statement', 'return random premise: ' + str(return_dict['premises']))

			# current argument
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==rnd_element,
		                                                              Argument.conclusion_uid==statement_uid)).first()
			return_dict['argument_uid'] = db_argument.uid

		logger('RecommenderHelper', 'get_premise_for_statement', 'return')
		return return_dict

	def __evaluate_argument(self, argument_uid):
		"""

		:param argument_uid:
		:return:
		"""
		logger('RecommenderHelper', '__evaluate_argument', 'argument ' + str(argument_uid))

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		# db_weight =
		# todo this
