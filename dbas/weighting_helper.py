from sqlalchemy import and_
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, Weight, Vote, User
from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015-2016

class WeightingHelper(object):

	def add_vote_for_argument(self, argument_uid, user, transaction):
		"""
		Increses the weight of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'add_vote_for_argument', 'increasing argument ' + str(argument_uid) + ' weight')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_weight, already_voted = self.__check_and_set_vote_uid(db_argument, user)

		if db_argument.conclusion_uid == 0:
			self.add_vote_for_argument(db_argument.argument_uid, user, transaction)

			# check for inconsequences
			db_relevance_arguments = DBDiscussionSession.query(Argument).filter_by(argument_uid=db_argument.argument_uid).all()
			for argument in db_relevance_arguments:
				# our argument is supportive, so let's have a look at arguments, which attacks our conclusion argument OR
				# our argument is attacking, so let's have a look at arguments, which supports our conclusion argument
				if db_argument.isSupportive and not argument.isSupportive \
						or not db_argument.isSupportive and not argument.isSupportive:
					self.remove_vote_for_argument(argument.uid, user)


		# let's check, if the user voted for the oposite
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid == db_argument.premisesGroup_uid,
		                                                              Argument.conclusion_uid == db_argument.conclusion_uid,
		                                                              Argument.argument_uid == db_argument.argument_uid,
		                                                              Argument.isSupportive != db_argument.isSupportive)).first()
		if db_argument:
			self.remove_vote_for_argument(db_argument.uid, user)


		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_weight.uid).all()

		transaction.commit()

		return len(db_votes)

	def remove_vote_for_argument(self, argument_uid, user):
		"""
		Increses the weight of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:return: increased weight of the argument
		"""
		logger('WeightingHelper', 'remove_vote_for_argument', 'decreasing argument ' + str(argument_uid) + ' weight')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# remove votes
		DBDiscussionSession.query(Vote).filter(and_(Vote.weight_uid==db_argument.weight_uid,
		                                            Vote.author_uid==db_user.uid)).first().set_valid(True)

		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_argument.weight_uid).all()
		return len(db_votes)

	def __check_and_set_vote_uid(self, db_argument, user):
		"""
		Check if the given argument has a weighting uid
		:param db_argument: Argument
		:param user: self.request.authenticated_userid
		:return: Weight, boolean for already voted
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		already_voted = False
		# do we have a weight?
		if db_argument.weight_uid == 0:
			# add new weight
			weight = Weight()
			DBDiscussionSession.add(weight)
			DBDiscussionSession.flush()
			# get new weight and create vote with weight uid and user uid; add the vote
			db_weight = DBDiscussionSession.query(Weight).order_by(Weight.uid.desc()).first()
			vote = Vote(weight_uid=db_weight.uid, author_uid=db_user.uid, isValid=True)
			DBDiscussionSession.add(vote)
			DBDiscussionSession.flush()
			# set the weight as arguments weight
			db_argument.set_weight_uid(db_weight.uid)
		else:
			# get weight and vote
			db_weight = DBDiscussionSession.query(Weight).filter_by(uid=db_argument.weight_uid).first()
			db_vote = DBDiscussionSession.query(Vote).filter(and_(Vote.weight_uid==db_weight.uid,
			                                                      Vote.author_uid==db_user.uid)).first()
			# add a vote, if there is no vote
			if not db_vote:
				vote = Vote(weight_uid=db_weight.uid, author_uid=db_user.uid)
				DBDiscussionSession.add(vote)
				DBDiscussionSession.flush()
			else:
				db_vote.set_valid(True)
				db_vote.update_timestamp()
				already_voted = True

		return db_weight, already_voted