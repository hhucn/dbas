"""
Class for handling relations of arguments

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Premise, PremiseGroup, User
from dbas.lib import get_text_for_premisesgroup_uid
from dbas.logger import logger


class RelationHelper(object):
	"""
	Helper for returning all kind of relatins for an argument
	"""

	def __init__(self, argument_uid=None, lang=None):
		"""
		Initialie default values.

		:param argument_uid: Argument.uid
		:param lang: ui_locales
		:return:
		"""
		self.argument_uid = argument_uid
		self.lang = lang

	def get_undermines_for_argument_uid(self, is_supportive=False):
		"""
		Returns all uid's of undermines for the argument.

		:return is_supportive: Boolean
		:return: array with dict() with id (of argumet) and text.
		"""
		# logger('RelationHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(self.argument_uid))
		db_attacked_argument = DBDiscussionSession.query(Argument).filter_by(uid=self.argument_uid).first()
		db_attacked_premises = DBDiscussionSession.query(Premise).filter_by(
				premisesgroup_uid=db_attacked_argument.premisesgroup_uid).order_by(
				Premise.premisesgroup_uid.desc()).all()

		premises_as_statements_uid = set()
		for premise in db_attacked_premises:
			premises_as_statements_uid.add(premise.statement_uid)

		if len(premises_as_statements_uid) == 0:
			return []

		return self.__get_undermines_for_premises(premises_as_statements_uid, self.lang, is_supportive)

	def get_overbids_for_argument_uid(self):
		"""
		Returns all uid's of overbids for the argument.

		:return: array with dict() with id (of argumet) and text.
		"""
		# logger('RelationHelper', 'get_overbids_for_argument_uid', 'main')
		return self.__get_attack_or_support_for_justification_of_argument_uid(self.argument_uid, True, self.lang)

	def get_undercuts_for_argument_uid(self):
		"""
		Calls self.__get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, False)

		:return: array with dict() with id (of argumet) and text.
		"""
		# logger('RelationHelper', 'get_undercuts_for_argument_uid', 'main ' + str(self.argument_uid))
		return self.__get_attack_or_support_for_justification_of_argument_uid(self.argument_uid, False, self.lang)

	def get_rebuts_for_argument_uid(self):
		"""
		Returns all uid's of rebuts for the argument.

		:return: array with dict() with id (of argumet) and text.
		"""
		# logger('RelationHelper', 'get_rebuts_for_argument_uid', 'main ' + str(self.argument_uid))
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=int(self.argument_uid)).first()
		if not db_argument:
			return None
		if db_argument.conclusion_uid is not None:
			return self.__get_rebuts_for_arguments_conclusion_uid(db_argument, self.lang)
		else:
			return self.get_undercuts_for_argument_uid()

	@staticmethod
	def __get_rebuts_for_arguments_conclusion_uid(db_argument, lang):
		"""

		:param db_argument:
		:param lang: ui_locales
		:return:
		"""
		return_array = []
		given_rebuts = set()
		index = 0
		#  logger('RelationHelper', 'get_rebuts_for_arguments_conclusion_uid', 'conclusion_statements_uid ' +
		#         str(db_argument.conclusion_uid) + ', is_current_argument_supportive ' + str(db_argument.is_supportive) +
		#         ' (searching for the opposite)')
		db_rebut = DBDiscussionSession.query(Argument).filter(Argument.is_supportive == (not db_argument.is_supportive),
                                                              Argument.conclusion_uid == db_argument.conclusion_uid).all()
		for rebut in db_rebut:
			logger('--- RelationHelper', 'get_rebuts_for_arguments_conclusion_uid', str(rebut.uid))
			logger('--- RelationHelper', 'get_rebuts_for_arguments_conclusion_uid', str(rebut.uid))

			if rebut.premisesgroup_uid not in given_rebuts:
				given_rebuts.add(rebut.premisesgroup_uid)
				tmp_dict = dict()
				tmp_dict['id'] = rebut.uid
				text, trash = get_text_for_premisesgroup_uid(rebut.premisesgroup_uid, lang)
				tmp_dict['text'] = text[0:1].upper() + text[1:]
				return_array.append(tmp_dict)
				index += 1
		return return_array

	def get_supports_for_argument_uid(self):
		"""
		Returns all uid's of supports for the argument.

		:return: array with dict() with id (of argumet) and text
		"""
		# logger('RelationHelper', 'get_supports_for_argument_uid', 'main')

		return_array = []
		given_supports = set()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=self.argument_uid).join(
			PremiseGroup).first()
		db_arguments_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
		index = 0

		for arguments_premises in db_arguments_premises:
			db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == arguments_premises.statement_uid,
                                                                          Argument.is_supportive == True)).join(PremiseGroup).all()
			if not db_supports:
				continue

			for support in db_supports:
				if support.premisesgroup_uid not in given_supports:
					tmp_dict = dict()
					tmp_dict['id'] = support.uid
					tmp_dict['text'], trash = get_text_for_premisesgroup_uid(support.premisesgroup_uid, self.lang)
					return_array.append(tmp_dict)
					index += 1
					given_supports.add(support.premisesgroup_uid)

		return [] if len(return_array) == 0 else return_array

	@staticmethod
	def set_new_undermine_or_support(transaction, premisegroup_uid, current_argument, current_attack, db_user, issue):
		"""
		Inserts a new undermine or support with the given parameters.

		:param transaction: transaction
		:param premisegroup_uid: premisesgroup_uid
		:param current_argument: Argument
		:param current_attack: String
		:param db_user: User
		:param issue: Issue.uid
		:return: Argument, Boolean if the argument is a duplicate
		"""
		new_arguments = []
		already_in = []
		# all premises out of current pgroup
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).all()
		for premise in db_premises:
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
			                                                              Argument.is_supportive == True,
			                                                              Argument.conclusion_uid == current_argument.conclusion_uid,
			                                                              Argument.argument_uid == None)).first()
			if db_argument:
				return db_argument, True
			else:
				new_argument = Argument(premisegroup=premisegroup_uid,
			                            issupportive=current_attack == 'support',
			                            author=db_user.uid,
			                            conclusion=premise.statement_uid,
			                            issue=issue)
				new_arguments.append(new_argument)

			if len(new_arguments) > 0:
				DBDiscussionSession.add_all(new_arguments)
				DBDiscussionSession.flush()
				transaction.commit()

				for argument in new_arguments:
					already_in.append(argument)

		rnd = random.randint(0, len(already_in) - 1)
		return already_in[rnd]

	@staticmethod
	def set_new_undercut_or_overbid(transaction, premisegroup_uid, current_argument, current_attack, db_user, issue):
		"""
		Inserts a new undercut or overbid with the given parameters.

		:param transaction: transaction
		:param premisegroup_uid: premisesgroup_uid
		:param current_argument: Argument
		:param current_attack: String
		:param db_user: User
		:param issue: Issue.uid
		:return: Argument, Boolean if the argument is a duplicate
		"""
		# duplicate?
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
		                                                              Argument.is_supportive == True,
		                                                              Argument.conclusion_uid == current_argument.conclusion_uid,
		                                                              Argument.argument_uid == 0)).first()
		if db_argument:
			return db_argument, True
		else:
			new_argument = Argument(premisegroup=premisegroup_uid,
			                        issupportive=current_attack == 'overbid',
			                        author=db_user.uid,
			                        issue=issue)
			new_argument.conclusions_argument(current_argument.uid)
			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()
			transaction.commit()
			return new_argument, False

	@staticmethod
	def set_new_rebut(transaction, premisegroup_uid, current_argument
	                  , db_user, issue):
		"""
		Inserts a new rebut with the given parameters.

		:param transaction: transaction
		:param premisegroup_uid: premisesgroup_uid
		:param current_argument: Argument
		:param db_user: User
		:return: Argument, Boolean if the argument is a duplicate
		"""
		# duplicate?
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
		                                                              Argument.is_supportive == True,
		                                                              Argument.conclusion_uid == current_argument.conclusion_uid,
		                                                              Argument.argument_uid == None)).first()
		if db_argument:
			return db_argument, True
		else:
			new_argument = Argument(premisegroup=premisegroup_uid,
			                        issupportive=False,
			                        author=db_user.uid,
			                        conclusion=current_argument.conclusion_uid,
			                        issue=issue)
			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()
			transaction.commit()
			return new_argument, False

	@staticmethod
	def set_new_support(transaction, premisegroup_uid, current_argument, db_user, issue):
		"""
		Inserts a new support with the given parameters.

		:param transaction: transaction
		:param premisegroup_uid: premisesgroup_uid
		:param current_argument: Argument
		:param db_user: User
		:return: Argument, Boolean if the argument is a duplicate
		"""
		# duplicate?
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
		                                                              Argument.is_supportive == True,
		                                                              Argument.conclusion_uid == current_argument.conclusion_uid,
		                                                              Argument.argument_uid == 0)).first()
		if db_argument:
			return db_argument, True
		else:
			new_argument = Argument(premisegroup=premisegroup_uid,
			                        issupportive=True,
			                        author=db_user.uid,
			                        conclusion=current_argument.conclusion_uid,
			                        issue=issue)
			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()
			transaction.commit()
			return new_argument, False

	@staticmethod
	def __set_argument(transaction, user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
		"""
		Set an Argument with given values into database

		:param transaction: transaction
		:param user: User.nickname
		:param premisegroup_uid: premisesgroup_uid
		:param conclusion_uid: Statement.uid
		:param argument_uid: Argument.uid
		:param is_supportive: Boolean
		:param issue: Issue.uid
		:return: Argument.uid or None
		"""
		# logger('RelationHelper', '__create_argument_by_uids', 'main with user: ' + str(user) +
		#        ', premisegroup_uid: ' + str(premisegroup_uid) +
		#        ', conclusion_uid: ' + str(conclusion_uid) +
		#        ', argument_uid: ' + str(argument_uid) +
		#        ', is_supportive: ' + str(is_supportive) +
		#        ', issue: ' + str(issue))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.issue_uid == issue)).first()
		if not new_argument:
			new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid,
			                        conclusion=conclusion_uid, issue=issue)
			new_argument.conclusions_argument(argument_uid)

			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()

			new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                           Argument.is_supportive == is_supportive,
                                                                           Argument.author_uid == db_user.uid,
                                                                           Argument.conclusion_uid == conclusion_uid,
                                                                           Argument.argument_uid == argument_uid,
                                                                           Argument.issue_uid == issue)).first()
		transaction.commit()
		if new_argument:
			# logger('RelationHelper', '__create_argument_by_uids', 'argument was inserted')
			return new_argument.uid
		else:
			# logger('RelationHelper', '__create_argument_by_uids', 'argument was not inserted')
			return None

	@staticmethod
	def __get_attack_or_support_for_justification_of_argument_uid(argument_uid, is_supportive, lang):
		"""
		Querys all

		:param argument_uid: Argument.uid
		:param is_supportive: Boolean
		:param lang: ui_locales
		:return: [{id, text}] or 0
		"""
		return_array = []
		# logger('RelationHelper', '__get_attack_or_support_for_justification_of_argument_uid',
		#        'db_undercut against Argument.argument_uid==' + str(argument_uid))
		db_related_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
		                                                                       Argument.argument_uid == argument_uid)).all()
		given_relations = set()
		index = 0

		if not db_related_arguments:
			return None

		for relation in db_related_arguments:
			if relation.premisesgroup_uid not in given_relations:
				given_relations.add(relation.premisesgroup_uid)
				tmp_dict = dict()
				tmp_dict['id'] = relation.uid
				tmp_dict['text'], trash = get_text_for_premisesgroup_uid(relation.premisesgroup_uid, lang)
				return_array.append(tmp_dict)
				index += 1
		return return_array

	@staticmethod
	def __get_undermines_for_premises(premises_as_statements_uid, lang, is_supportive=False):
		"""
		Querys all undermines for the given statements

		:param premises_as_statements_uid:
		:param lang: ui_locales
		:param is_supportive
		:return: [{id, text}]
		"""
		# logger('RelationHelper', '__get_undermines_for_premises', 'main')
		return_array = []
		index = 0
		given_undermines = set()
		for s_uid in premises_as_statements_uid:
			db_undermine = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
			                                                               Argument.conclusion_uid == s_uid)).all()
			for undermine in db_undermine:
				if undermine.premisesgroup_uid not in given_undermines:
					given_undermines.add(undermine.premisesgroup_uid)
					tmp_dict = dict()
					tmp_dict['id'] = undermine.uid
					tmp_dict['text'], uids = get_text_for_premisesgroup_uid(undermine.premisesgroup_uid, lang)
					return_array.append(tmp_dict)
					index += 1
		return return_array
