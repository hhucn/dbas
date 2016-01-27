from sqlalchemy import and_
from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, Vote, User
from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015-2016

class VotingHelper(object):

	def add_vote_for_argument(self, argument_uid, user, transaction):
		"""
		Increses the votes of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:return: increased votes of the argument
		"""
		logger('VotingHelper', 'add_vote_for_argument', 'increasing argument ' + str(argument_uid) + ' vote')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_vote, already_voted = self.__check_and_set_vote_uid(db_argument, user)

		# some logical assumptions
		#if db_argument.conclusion_uid == 0:
		#	self.add_vote_for_argument(db_argument.argument_uid, user, transaction)
#
		#	# check for inconsequences
		#	db_relevance_arguments = DBDiscussionSession.query(Argument).filter_by(argument_uid=db_argument.argument_uid).all()
		#	for argument in db_relevance_arguments:
		#		# our argument is supportive, so let's have a look at arguments, which attacks our conclusion argument OR
		#		# our argument is attacking, so let's have a look at arguments, which supports our conclusion argument
		#		if db_argument.isSupportive and not argument.isSupportive \
		#				or not db_argument.isSupportive and not argument.isSupportive:
		#			self.remove_vote_for_argument(argument.uid, user)
#
#
		## let's check, if the user voted for the oposite
		#db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid == db_argument.premisesGroup_uid,
		#                                                              Argument.conclusion_uid == db_argument.conclusion_uid,
		#                                                              Argument.argument_uid == db_argument.argument_uid,
		#                                                              Argument.isSupportive != db_argument.isSupportive)).first()
		#if db_argument:
		#	self.remove_vote_for_argument(db_argument.uid, user)


		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==db_argument.uid, Vote.isValid==True)).all()

		transaction.commit()

		return len(db_votes)

	def remove_vote_for_argument(self, argument_uid, user):
		"""
		Decreses the vote of a given argument
		:param argument_uid: id of the argument
		:param user: self.request.authenticated_userid
		:return: decreased vote of the argument
		"""
		logger('VotingHelper', 'remove_vote_for_argument', 'decreasing argument ' + str(argument_uid) + ' vote')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# remove votes
		DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==db_argument.uid,
		                                            Vote.author_uid==db_user.uid)).first().set_valid(False)

		# return count of votes
		db_votes = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==db_argument.uid, Vote.isValid==True)).all()

		return len(db_votes)

	def __check_and_set_vote_uid(self, db_argument, user):
		"""
		Check if the given argument has a voteing uid
		:param db_argument: Argument
		:param user: self.request.authenticated_userid
		:return: Vote, boolean for already voted
		"""
		
		# get vote
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_vote = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==db_argument.uid,
		                                                      Vote.author_uid==db_user.uid)).first()
		already_voted = False
		# do we have a vote?
		if not db_vote:
			db_vote = Vote(argument_uid=db_argument.uid, author_uid=db_user.uid, isUpVote=True, isValid=True)
			DBDiscussionSession.add(db_vote)
			DBDiscussionSession.flush()
		else:
			db_vote.set_valid(True)
			db_vote.update_timestamp()
			already_voted = True

		return db_vote, already_voted