# Common library for Export Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, VoteArgument, Issue
from dbas.query_helper import QueryHelper
from dbas.user_management import UserHandler
from sqlalchemy import and_


def argument_overview(user, lang):
	"""
		Returns a dicitonary with all attacks, done by the users, but only if the user has admin right!
		:param user: current user
		:param issue: current issue
		:param lang: current language
		:return: dict()
		"""
	_qh = QueryHelper()
	is_admin = UserHandler().is_user_in_group(user, 'admins')
	logger('AdminLib', 'get_argument_overview', 'is_admin ' + str(is_admin))
	return_dict = dict()
	if not is_admin:
		return return_dict

	db_issues = DBDiscussionSession.query(Issue).all()
	for issue in db_issues:
		issue_array = []
		db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue.uid).order_by(Argument.uid.asc()).all()
		logger('AdminLib', 'get_argument_overview', 'count: ' + str(len(db_arguments)))

		if len(db_arguments) > 0:
			for argument in db_arguments:
				tmp_dict = dict()
				tmp_dict['uid'] = str(argument.uid)
				tmp_dict['text'] = _qh.get_text_for_argument_uid(argument.uid, lang)
				tmp_dict['text'] = _qh.get_text_for_argument_uid(argument.uid, lang)
				db_votes = DBDiscussionSession.query(VoteArgument).filter_by(argument_uid=argument.uid).all()
				db_valid_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
				                                                                     VoteArgument.is_valid == True)).all()
				db_valid_upvotes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
				                                                                       VoteArgument.is_valid == True,
				                                                                       VoteArgument.is_up_vote)).all()
				tmp_dict['votes'] = len(db_votes)
				tmp_dict['valid_votes'] = len(db_valid_votes)
				tmp_dict['valid_upvotes'] = len(db_valid_upvotes)

				issue_array.append(tmp_dict)
		return_dict[issue.title] = issue_array

	return return_dict
