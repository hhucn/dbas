from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class WeightingHelper(object):

	def increase_weight_of_argument(self, argument_uid):
		"""
		Increses the weight of a given argument by 1
		:param argument_uid: id of the argument
		:return: increased weight of the argument
		"""
		return DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first().increase_weight(1)

	def decrease_weight_of_argument(self, argument_uid):
		"""
		Increses the weight of a given argument by 1
		:param argument_uid: id of the argument
		:return: increased weight of the argument
		"""
		return DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first().decrease_weight(1)

	def get_weight_of_argument(self, argument_uid):
		"""
		Returns the weight of an argument
		:param argument_uid: id of the argument
		:return: weight of the argument
		"""
		return DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first().weight

	def increase_weight_of_statement(self, statement_uid):
		"""
		Increses the weight of a given statement by 1
		:param argument_uid: id of the statement
		:return: increased weight of the statement
		"""
		return DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first().increase_weight(1)

	def decrease_weight_of_statement(self, statement_uid):
		"""
		Increses the weight of a given statement by 1
		:param argument_uid: id of the statement
		:return: increased weight of the statement
		"""
		return DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first().decrease_weight(1)

	def get_weight_of_statement(self, statement_uid):
		"""
		Returns the weight of an statement
		:param argument_uid: id of the statement
		:return: weight of the statement
		"""
		return DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first().weight

