from sqlalchemy import and_
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, VoteArgument, VoteStatement, User
from .logger import logger
from .user_management import UserHandler

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class VotingHelper(object):

	def add_vote_for_argument(self, argument_uid, user, transaction):
		"""
		Increses the votes of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:param transaction: transaction
		:return: increased votes of the argument
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not UserHandler().is_user_logged_in(user) or not db_user:
			return None

		logger('VotingHelper', 'add_vote_for_argument', 'increasing argument ' + str(argument_uid) + ' vote')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()

		# set vote for the argument (relation), its premisegroup and conclusion
		self.__vote_argument(db_argument, db_user, True)
		self.__vote_premisesgroup(db_argument.premisesgroup_uid, db_user, True)

		if db_argument.argument_uid == 0:
			db_conclusion = DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()
			self.__vote_statement(db_conclusion, db_user, True)
		else:
			# check for inconsequences
			db_conclusion_argument = DBDiscussionSession.query(Argument).filter_by(argument_uid=db_argument.argument_uid).first()
			db_conclusion_conclusion = DBDiscussionSession.query(Statement).filter_by(uid=db_conclusion_argument.conclusion_uid).first()
			if db_argument.is_supportive:
				if db_conclusion_argument.is_supportive:
					# argument supportive -> conclusion supportive
					self.__vote_argument(db_conclusion_argument, db_user, True)
					self.__vote_premisesgroup(db_conclusion_argument.premisesgroup_uid, db_user, True)
					self.__vote_statement(db_conclusion_conclusion, db_user, True)
				else:
					# argument supportive -> conclusion attacking
					self.__vote_argument(db_conclusion_argument, db_user, True)
					self.__vote_premisesgroup(db_conclusion_argument.premisesgroup_uid, db_user, True)
					self.__vote_statement(db_conclusion_conclusion, db_user, False)
			else:
				if db_conclusion_argument.is_supportive:
					# argument attacking -> conclusion supportive
					self.__vote_argument(db_conclusion_argument, db_user, False)
					self.__vote_premisesgroup(db_conclusion_argument.premisesgroup_uid, db_user, True)
					self.__vote_statement(db_conclusion_conclusion, db_user, False)
				else:
					# argument attacking -> conclusion attacking
					self.__vote_argument(db_conclusion_argument, db_user, False)
					self.__vote_premisesgroup(db_conclusion_argument.premisesgroup_uid, db_user, True)
					self.__vote_statement(db_conclusion_conclusion, db_user, True)

		# votes redundance will be handled in the accept and decline methods!

		# return count of votes for this argument
		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == db_argument.uid,
		                                                               VoteArgument.is_valid == True)).all()

		transaction.commit()

		return len(db_votes)

	def add_vote_for_statement(self, statement_uid, user, supportive, transaction):
		"""

		:param statement_uid:
		:param user:
		:param supportive:
		:param transaction:
		:return:
		"""
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if db_user:
			self.__vote_statement(db_statement, db_user, supportive)
			transaction.commit()

	def clear_votes_of_user(self, transaction, user):
		"""

		:param transaction:
		:param user:
		:return:
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return False

		DBDiscussionSession.query(VoteArgument).filter_by(author_uid=db_user.uid).delete()
		DBDiscussionSession.query(VoteStatement).filter_by(author_uid=db_user.uid).delete()
		DBDiscussionSession.flush()
		transaction.commit()
		return True

	def __vote_argument(self, argument, user, is_accept):
		"""
		Check if there is a vote for the argument. If not, we will create a new one, otherwise the current one will be
		invalid an we will create a new entry.
		:param argument: Argument
		:param user: User
		:param is_accept: Boolean
		:return: None
		"""
		if argument is None:
			logger('VotingHelper', '__vote_argument', 'argument is None')
			return

		logger('VotingHelper', '__vote_argument', 'argument ' + str(argument.uid) + ', user ' + user.nickname)

		db_vote = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
		                                                              VoteArgument.author_uid == user.uid,
		                                                              VoteArgument.is_up_vote == is_accept,
		                                                              VoteArgument.is_valid == True)).first()

		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
		                                                              VoteArgument.author_uid == user.uid,
		                                                              VoteArgument.is_up_vote == is_accept)).all()
		for d in db_votes:
			logger('--',str(d.uid), str(d.is_valid))

		# old one will be invalid
		db_old_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
		                                                                   VoteArgument.author_uid == user.uid,
		                                                                   VoteArgument.is_valid == True)).all()
		if db_vote in db_old_votes:
			db_old_votes.remove(db_vote)

		for old_vote in db_old_votes:
			old_vote.set_valid(False)
			old_vote.update_timestamp()
		DBDiscussionSession.flush()

		if not db_vote:
			db_new_vote = VoteArgument(argument_uid=argument.uid, author_uid=user.uid, is_up_vote=is_accept, is_valid=True)
			DBDiscussionSession.add(db_new_vote)
			DBDiscussionSession.flush()

	def __vote_statement(self, statement, user, is_accept):
		"""
		Check if there is a vote for the statement. If not, we will create a new one, otherwise the current one will be
		invalid an we will create a new entry.
		:param argument: Statement
		:param user: User
		:param is_accept: Boolean
		:return: None
		"""
		if statement is None:
			logger('VotingHelper', '__vote_statement', 'statement is None')
			return

		logger('VotingHelper', '__vote_statement', 'statement ' + str(statement.uid) + ', user ' + user.nickname)

		# check for duplicate
		db_vote = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
		                                                               VoteStatement.author_uid == user.uid,
		                                                               VoteStatement.is_up_vote == is_accept,
		                                                               VoteStatement.is_valid == True)).first()

		# old one will be invalid
		db_old_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
		                                                                    VoteStatement.author_uid == user.uid,
		                                                                    VoteStatement.is_valid == True)).all()
		if db_vote in db_old_votes:
			db_old_votes.remove(db_vote)

		for old_vote in db_old_votes:
			old_vote.set_valid(False)
			old_vote.update_timestamp()
		DBDiscussionSession.flush()

		if not db_vote:
			db_new_vote = VoteStatement(statement_uid=statement.uid, author_uid=user.uid, is_up_vote=is_accept, is_valid=True)
			DBDiscussionSession.add(db_new_vote)
			DBDiscussionSession.flush()

	def __vote_premisesgroup(self, premisesgroup_uid, user, is_accept):
		"""
		Calls statemens-methods for every premise
		:param premisegroup_uid: PremiseGroup.uid
		:param user: User
		:param is_accept: Boolean
		:return:
		"""
		if premisesgroup_uid is None or premisesgroup_uid == 0:
			logger('VotingHelper', '__vote_premisesgroup', 'premisegroup_uid is None')
			return

		logger('VotingHelper', '__vote_premisesgroup', 'premisegroup_uid ' + str(premisesgroup_uid) + ', user ' + user.nickname)

		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisesgroup_uid).all()
		for premise in db_premises:
			db_statement = DBDiscussionSession.query(Statement).filter_by(uid=premise.statement_uid).first()
			self.__vote_statement(db_statement, user, is_accept)
