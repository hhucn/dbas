"""
Methods for validating input params given via url or ajax

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, PremiseGroup
from .logger import logger
from sqlalchemy import and_


class Validator:
	"""
	Methods for saving or reading data out of current session. Additionally these values can be aligned.
	"""

	@staticmethod
	def check_reaction(attacked_arg_uid, attacking_arg_uid, relation):
		"""
		Checks whether the attacked argument uid and the attacking argument uid are connected via the given relation

		:param attacking_arg_uid: Argument.uid
		:param relation: String
		:return: Boolean
		"""
		logger('Validator', 'check_reaction', relation + ' from ' + str(attacking_arg_uid) + ' to ' + str(attacked_arg_uid))
		if relation == 'undermine':
			# conclusion of the attacking argument
			db_attacking_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacking_arg_uid).join(Statement).first()
			if not db_attacking_arg:
				return False

			# which pgroups has the conclusion as premise
			db_attacked_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=db_attacking_arg.statements.uid).first()
			if not db_attacked_premise:
				return False

			# and does the attacked argument has this premisegroup as premisegroup
			db_attacked_arg = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == attacked_arg_uid,
			                                                                  Argument.premisesgroup_uid == db_attacked_premise.premisesgroup_uid)).first()
			return True if db_attacked_arg else False

		elif relation == 'undercut':
			db_attacking_arg = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == attacking_arg_uid,
			                                                                   Argument.argument_uid == attacked_arg_uid)).first()
			return True if db_attacking_arg else False

		elif relation == 'rebut':
			db_attacking_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacking_arg_uid).join(Statement).first()
			if not db_attacking_arg:
				return False

			db_attacked_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacked_arg_uid).join(Statement).first()
			if not db_attacked_arg:
				return False

			return True if db_attacking_arg.conclusion_uid == db_attacked_arg.conclusion_uid and db_attacked_arg.conclusion_uid is not None else False
		else:
			return False
