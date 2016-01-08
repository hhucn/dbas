from sqlalchemy import and_
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, Weight, Vote, User
from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015-2016

class WeightingHelper(object):

	def increase_weight_of_argument_by_id(self, argument_uid, user):
		"""
		Increses the weight of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'increase_weight_of_argument_by_id', 'increasing argument ' + str(argument_uid) + ' weight')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_weight = self.__check_weight_and_set_vote_uid(db_argument, user)

		# if we vote for the argument, we have to vote the components to
		self.__increase_weight_of_statements_in_premissegroup(db_argument.premisesGroup_uid, user)
		if db_argument.isSupportive:
			if db_argument.conclusion_uid != 0:
				self.__increase_weight_of_statement(db_argument.conclusion_uid, user)
			else:
				self.increase_weight_of_argument_by_id(db_argument.argument_uid, user)
		else:
			if db_argument.conclusion_uid != 0:
				self.__decrease_weight_of_statement(db_argument.conclusion_uid, user)
			else:
				self.decrease_weight_of_argument_by_id(db_argument.argument_uid, user)


		# let's check, if the user voted for the oposite
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid == db_argument.premisesGroup_uid,
		                                                              Argument.conclusion_uid == db_argument.conclusion_uid,
		                                                              Argument.argument_uid == db_argument.argument_uid,
		                                                              Argument.isSupportive != db_argument.isSupportive)).first()
		if db_argument:
			self.decrease_weight_of_argument_by_id(db_argument.uid, user)


		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_weight.uid).all()
		return len(db_votes)

	def decrease_weight_of_argument_by_id(self, argument_uid, user):
		"""
		Increses the weight of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'decrease_weight_of_argument_by_id', 'decreasing argument ' + str(argument_uid) + ' weight')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# remove votes
		DBDiscussionSession.query(Vote).filter(and_(Vote.weight_uid==db_argument.weight_uid,
		                                            Vote.author_uid==db_user.uid)).delete()
		# remove votes of the components
		self.__decrease_weight_of_statements_in_premissegroup(db_argument.premisesGroup_uid, user)
		if db_argument.conclusion_uid != 0:
			self.__decrease_weight_of_statement(db_argument.conclusion_uid, user)
		else:
			self.decrease_weight_of_argument_by_id(db_argument.argument_uid, user)


		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_argument.weight_uid).all()
		return len(db_votes)

	def __increase_weight_of_statement(self, statement_uid, user):
		"""
		Increses the weight of a given statement
		:param statement_uid: id of the statement
		:param user: self.request.authenticated_userid
		:return: increased weight of the statement
		"""
		logger('WeightingHelper', '__increase_weight_of_statement', 'increasing statement ' + str(statement_uid) + ' weight')
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		db_weight = self.__check_weight_and_set_vote_uid(db_statement, user)

		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_weight.uid).all()
		return len(db_votes)

	def __decrease_weight_of_statement(self, statement_uid, user):
		"""
		Increses the weight of a given statement
		:param statement_uid: id of the statement
		:param user: self.request.authenticated_userid
		:return: increased weight of the statement
		"""
		logger('WeightingHelper', '__decrease_weight_of_statement', 'decreasing statement ' + str(statement_uid) + ' weight')
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# remove vote
		DBDiscussionSession.query(Vote).filter(and_(Vote.weight_uid==db_statement.weight_uid,
		                                            Vote.author_uid==db_user.uid)).delete()

		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_statement.weight_uid).all()
		return len(db_votes)

	def __increase_weight_of_statements_in_premissegroup(self, premissegroup_uid, user):
		"""
		Increses the weight of a given statements in pgroup
		:param premissegroup_uid: id of the premissegroup
		:param user: self.request.authenticated_userid
		:return: None
		"""
		db_group = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=premissegroup_uid).all()
		for premise in db_group:
			db_statement = DBDiscussionSession.query(Statement).filter_by(uid=premise.statement_uid).first()
			self.__check_weight_and_set_vote_uid(db_statement, user)
			logger('WeightingHelper', '__increase_weight_of_statements_in_premissegroup', 'increasing statement ' + str(db_statement.uid) + ' weight')

	def __decrease_weight_of_statements_in_premissegroup(self, premissegroup_uid, user):
		"""
		Increses the weight of a given statements in pgroup
		:param premissegroup_uid: id of the premissegroup
		:param user: self.request.authenticated_userid
		:return: None
		"""
		db_group = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=premissegroup_uid).all()
		for premise in db_group:
			db_statement = DBDiscussionSession.query(Statement).filter_by(uid=premise.statement_uid).first()
			self.__decrease_weight_of_statement(db_statement.uid, user)
			logger('WeightingHelper', 'decrease_weight_of_statement_in_premissegroup', 'decreasing statement ' + str(db_statement.uid) + ' weight')

	def __check_weight_and_set_vote_uid(self, db_argument_or_statement, user):
		"""
		Check if the given argument has a weighting uid
		:param db_argument_or_statement: Argument or Statement
		:param user: self.request.authenticated_userid
		:return: Weight
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		# do we have a weight?
		if db_argument_or_statement.weight_uid == 0:
			# add new weight
			weight = Weight()
			DBDiscussionSession.add(weight)
			DBDiscussionSession.flush()
			# get new weight and create vote with weight uid and user uid; add the vote
			db_weight = DBDiscussionSession.query(Weight).order_by(Weight.uid.desc()).first()
			vote = Vote(weight_uid=db_weight.uid, author_uid=db_user.uid)
			DBDiscussionSession.add(vote)
			DBDiscussionSession.flush()
			# set the weight as arguments weight
			db_argument_or_statement.set_weight_uid(db_weight.uid)
		else:
			# get weight and vote
			db_weight = DBDiscussionSession.query(Weight).filter_by(uid=db_argument_or_statement.weight_uid).first()
			db_vote = DBDiscussionSession.query(Vote).filter(and_(Vote.weight_uid==db_weight.uid,
			                                                      Vote.author_uid==db_user.uid)).all()
			# add a vote, if there is no vote
			if not db_vote:
				vote = Vote(weight_uid=db_weight.uid, author_uid=db_user.uid)
				DBDiscussionSession.add(vote)
				DBDiscussionSession.flush()

		return db_weight