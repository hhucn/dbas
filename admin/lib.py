# Common library for Admin Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

import dbas.user_management as UserHandler

from dbas.lib import sql_timestamp_pretty_print, get_text_for_argument_uid
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, VoteArgument, Issue, User, Group, Statement, VoteStatement
from sqlalchemy import and_


def get_overview_of_arguments(user='', lang=''):
	"""
	Returns a dicitonary with all attacks, done by the users, but only if the user has admin right!

	:param user: current user
	:param lang: current language
	:return: dict()
	"""
	is_admin = UserHandler.is_user_in_group(user, 'admins')
	logger('AdminLib', 'get_overview_of_arguments', 'is_admin ' + str(is_admin))
	return_dict = dict()
	if not is_admin:
		return return_dict

	db_issues = DBDiscussionSession.query(Issue).all()
	for issue in db_issues:
		issue_array = []
		db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue.uid).order_by(Argument.uid.asc()).all()
		logger('AdminLib', 'get_overview_of_arguments', 'count: ' + str(len(db_arguments)))

		if len(db_arguments) > 0:
			for argument in db_arguments:
				text = get_text_for_argument_uid(argument.uid, lang)
				tmp_dict = dict()
				tmp_dict['uid'] = str(argument.uid)
				tmp_dict['text'] = text[0:1].upper() + text[1:]
				db_votes         = DBDiscussionSession.query(VoteArgument).filter_by(argument_uid=argument.uid).all()
				db_valid_votes   = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
				                                                                       VoteArgument.is_valid == True)).all()
				db_valid_upvotes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument.uid,
				                                                                       VoteArgument.is_valid == True,
				                                                                       VoteArgument.is_up_vote == True)).all()
				tmp_dict['votes'] = len(db_votes)
				tmp_dict['valid_votes'] = len(db_valid_votes)
				tmp_dict['valid_upvotes'] = len(db_valid_upvotes)

				issue_array.append(tmp_dict)
		return_dict[issue.title] = issue_array

	return return_dict


def get_all_users(user, lang, mainpage):
	"""
	Bla

	:param user:
	:param lang:
	:return:
	"""
	is_admin = UserHandler.is_user_in_group(user, 'admins')
	logger('AdminLib', 'get_all_users', 'is_admin ' + str(is_admin))
	return_array = []
	if not is_admin:
		return return_array

	_uh = UserHandler
	db_users = DBDiscussionSession.query(User).order_by(User.uid.asc()).all()
	for user in db_users:
		tmp_dict = dict()
		tmp_dict['uid']             = str(user.uid)
		tmp_dict['firstname']       = str(user.firstname)
		tmp_dict['surname']         = str(user.surname)
		tmp_dict['nickname']        = str(user.nickname)
		tmp_dict['public_nickname'] = str(user.public_nickname)
		tmp_dict['email']           = str(user.email)
		tmp_dict['gender']          = str(user.gender)
		tmp_dict['group_uid']       = DBDiscussionSession.query(Group).filter_by(uid=user.group_uid).first().name
		tmp_dict['last_login']      = sql_timestamp_pretty_print(user.last_login, lang)
		tmp_dict['registered']      = sql_timestamp_pretty_print(user.registered, lang)
		tmp_dict['avatar']          = _uh.get_profile_picture(user, 40)
		tmp_dict['public_avatar']   = _uh.get_public_profile_picture(user, 40)
		tmp_dict['last_action']     = sql_timestamp_pretty_print(user.last_action, lang)
		tmp_dict['public_url']      = mainpage + '/user/' + str(user.public_nickname)
		return_array.append(tmp_dict)

	return return_array


def get_dashboard_infos():
	"""
	Bla

	:return:
	"""
	logger('AdminLib', 'get_dashboard_infos', 'main')
	return_dict = dict()
	return_dict['user_count'] = str(len(DBDiscussionSession.query(User).all()))
	return_dict['vote_count'] = str(len(DBDiscussionSession.query(VoteArgument).all()) + len(DBDiscussionSession.query(VoteStatement).all()))
	return_dict['argument_count'] = str(len(DBDiscussionSession.query(Argument).all()))
	return_dict['statement_count'] = str(len(DBDiscussionSession.query(Statement).all()))
	return return_dict
