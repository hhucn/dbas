from sqlalchemy import and_
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise
from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class WeightingHelper(object):
	# TODO improve manipulation

	def increase_weight_of_argument_by_id(self, argument_uid):
		"""
		Increses the weight of a given argument by 1
		:param argument_uid: id of the argument
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'increase_weight_of_argument_by_id', 'increasing argument ' + str(argument_uid) + ' weight by 1')
		return DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first().increase_weight(1)

	def decrease_weight_of_argument_by_id(self, argument_uid):
		"""
		Increses the weight of a given argument by 1
		:param argument_uid: id of the argument
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'decrease_weight_of_argument_by_id', 'decreasing argument ' + str(argument_uid) + ' weight by 1')
		return DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first().decrease_weight(1)

	def get_weight_of_argument_by_id(self, argument_uid):
		"""
		Returns the weight of an argument
		:param argument_uid: id of the argument
		:return: weight of the argument
		"""
		return DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first().weight

	def increase_weight_of_argument_by_components(self, premissegroup_uid, conclusion_uid, is_supportive):
		"""
		Increses the weight of a given argument by 1
		:param premissegroup_uid: id of the premisegroup
		:param conclusion_uid: id of the conclusion
		:param is_supportive: boolean
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'increase_weight_of_argument_by_components', 'increasing argument pgroup' + str(premissegroup_uid)
		       + ' conclusion' + str(conclusion_uid) + ' supportive' + str(is_supportive) + ' weight by 1')
		return DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premissegroup_uid,
		                                                       Argument.conclusion_uid==conclusion_uid,
		                                                       Argument.isSupportive==is_supportive)).first().increase_weight(1)

	def decrease_weight_of_argument_by_components(self, premissegroup_uid, conclusion_uid, is_supportive):
		"""
		Increses the weight of a given argument by 1
		:param premissegroup_uid: id of the premisegroup
		:param conclusion_uid: id of the conclusion
		:param is_supportive: boolean
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'decrease_weight_of_argument_by_components', 'decreasing argument pgroup' + str(premissegroup_uid)
		       + ' conclusion' + str(conclusion_uid) + ' supportive' + str(is_supportive) + ' weight by 1')
		return DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premissegroup_uid,
		                                                       Argument.conclusion_uid==conclusion_uid,
		                                                       Argument.isSupportive==is_supportive)).first().decrease_weight(1)

	def get_weight_of_argument_by_components(self, premissegroup_uid, conclusion_uid, is_supportive):
		"""
		Returns the weight of a given argument by 1
		:param premissegroup_uid: id of the premisegroup
		:param conclusion_uid: id of the conclusion
		:param is_supportive: boolean
		:return: increased weight of the argument
		"""
		return DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premissegroup_uid,
		                                                       Argument.conclusion_uid==conclusion_uid,
		                                                       Argument.isSupportive==is_supportive)).first().weight

	def increase_weight_of_statement(self, statement_uid):
		"""
		Increses the weight of a given statement by 1
		:param statement_uid: id of the statement
		:return: increased weight of the statement
		"""
		logger('WeightingHelper', 'increase_weight_of_statement', 'increasing statement ' + str(statement_uid) + ' weight by 1')
		return DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first().increase_weight(1)

	def decrease_weight_of_statement(self, statement_uid):
		"""
		Increses the weight of a given statement by 1
		:param statement_uid: id of the statement
		:return: increased weight of the statement
		"""
		logger('WeightingHelper', 'decrease_weight_of_statement', 'decreasing statement ' + str(statement_uid) + ' weight by 1')
		return DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first().decrease_weight(1)

	def get_weight_of_statement(self, statement_uid):
		"""
		Returns the weight of an statement
		:param statement_uid: id of the statement
		:return: weight of the statement
		"""
		return DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first().weight

	def increase_weight_of_statements_in_premissegroup(self, premissegroup_uid):
		"""
		Increses the weight of a given statements in pgroup by 1
		:param premissegroup_uid: id of the premissegroup
		:return: None
		"""
		db_group = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=premissegroup_uid).all()
		for premise in db_group:
			db_statement = DBDiscussionSession.query(Statement).filter_by(uid=premise.statement_uid).first()
			db_statement.increase_weight(1)
			logger('WeightingHelper', 'increase_weight_of_statements_in_premissegroup', 'increasing statement ' + str(db_statement.uid) + ' weight by 1')

	def decrease_weight_of_statements_in_premissegroup(self, premissegroup_uid):
		"""
		Increses the weight of a given statements in pgroup by 1
		:param premissegroup_uid: id of the premissegroup
		:return: None
		"""
		db_group = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=premissegroup_uid).all()
		for premise in db_group:
			db_statement = DBDiscussionSession.query(Statement).filter_by(uid=premise.statement_uid).first()
			db_statement.decrease_weight(1)
			logger('WeightingHelper', 'decrease_weight_of_statement_in_premissegroup', 'decreasing statement ' + str(db_statement.uid) + ' weight by 1')

