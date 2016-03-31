# Common library for Export Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, VoteArgument, VoteStatement, Issue
from dbas.query_helper import QueryHelper


def get_dump(issue, lang):
	"""

	:param issue: current issue
	:param lang: current lang
	:return: dictionary labeled with enumerated integeres, whereby these dicts are named by their table
	"""
	ret_dict = dict()
	logger('ExportLib', 'get_dump', 'main')
	_qh = QueryHelper()

	db_issue = DBDiscussionSession.query(Issue).filter_by(uid=issue).first()
	if not db_issue:
		return ret_dict

	ret_dict['issue'] = {'title': db_issue.title, 'info': db_issue.info}

	# getting all users
	db_users = DBDiscussionSession.query(User).all()
	user_dict = dict()
	for index, user in enumerate(db_users):
		tmp_dict = dict()
		tmp_dict['uid']         = user.uid
		tmp_dict['nickname']    = user.nickname
		user_dict[str(index)]   = tmp_dict
	ret_dict['user'] = user_dict

	# getting all statements
	db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
	statement_uid_set = set()
	statement_dict = dict()
	for index, statement in enumerate(db_statements):
		tmp_dict = dict()
		statement_uid_set.add(statement.uid)
		tmp_dict['uid']             = statement.uid
		tmp_dict['textversion_uid'] = statement.textversion_uid
		tmp_dict['is_startpoint']   = statement.is_startpoint
		statement_dict[str(index)]  = tmp_dict
	ret_dict['statement'] = statement_dict

	# getting all textversions
	db_textversions = DBDiscussionSession.query(TextVersion).all()
	textversion_dict = dict()
	for index, textversion in enumerate(db_textversions):
		if textversion.uid in statement_uid_set:
			tmp_dict = dict()
			tmp_dict['uid']              = textversion.uid
			tmp_dict['statement_uid']    = textversion.statement_uid
			tmp_dict['content']          = textversion.content
			tmp_dict['author_uid']       = textversion.author_uid
			tmp_dict['timestamp']        = _qh.sql_timestamp_pretty_print(str(textversion.timestamp), lang)
			textversion_dict[str(index)] = tmp_dict
	ret_dict['textversion'] = textversion_dict

	# getting all arguments
	db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()
	argument_dict = dict()
	argument_uid_set = set()
	argument_prgoup_set = set()
	for index, argument in enumerate(db_arguments):
		tmp_dict = dict()
		argument_uid_set.add(argument.uid)
		argument_prgoup_set.add(argument.premisesgroup_uid)
		tmp_dict['uid']                 = argument.uid
		tmp_dict['premisesgroup_uid']   = argument.premisesgroup_uid
		tmp_dict['conclusion_uid']      = argument.conclusion_uid if argument.conclusion_uid else 0
		tmp_dict['argument_uid']        = argument.argument_uid if argument.argument_uid else 0
		tmp_dict['is_supportive']       = argument.is_supportive
		tmp_dict['author_uid']          = argument.author_uid
		tmp_dict['timestamp']           = _qh.sql_timestamp_pretty_print(str(argument.timestamp), lang)
		argument_dict[str(index)]       = tmp_dict
	ret_dict['argument'] = argument_dict

	# getting all premisegroups
	db_premisegroups = DBDiscussionSession.query(PremiseGroup).all()
	premisegroup_dict = dict()
	premisegroup_uid_set = set()
	for index, premisegroup in enumerate(db_premisegroups):
		if premisegroup.uid in argument_prgoup_set:
			tmp_dict = dict()
			premisegroup_uid_set.add(premisegroup.uid)
			tmp_dict['uid']                 = premisegroup.uid
			tmp_dict['author_uid']          = premisegroup.author_uid
			premisegroup_dict[str(index)]   = tmp_dict
	ret_dict['premisegroup'] = premisegroup_dict

	# getting all premises
	db_premises = DBDiscussionSession.query(Premise).filter_by(issue_uid=issue).all()
	premise_dict = dict()
	for index, premise in enumerate(db_premises):
		if premise.premisesgroup_uid in premisegroup_uid_set:
			tmp_dict = dict()
			tmp_dict['premisesgroup_uid'] = premise.premisesgroup_uid
			tmp_dict['statement_uid']     = premise.statement_uid
			tmp_dict['is_negated']        = premise.is_negated
			tmp_dict['author_uid']        = premise.author_uid
			tmp_dict['timestamp']         = _qh.sql_timestamp_pretty_print(str(premise.timestamp), lang)
			premise_dict[str(index)]      = tmp_dict
	ret_dict['premise'] = premise_dict

	# getting all votes
	db_votes = DBDiscussionSession.query(VoteArgument).all()
	vote_dict = dict()
	for index, vote in enumerate(db_votes):
		if vote.argument_uid in argument_uid_set:
			tmp_dict = dict()
			tmp_dict['uid']          = vote.uid
			tmp_dict['argument_uid'] = vote.argument_uid
			tmp_dict['author_uid']   = vote.author_uid
			tmp_dict['is_up_vote']   = vote.is_up_vote
			tmp_dict['is_valid']     = vote.is_valid
			vote_dict[str(index)]    = tmp_dict
	ret_dict['vote_argument'] = vote_dict

	# getting all votes
	db_votes = DBDiscussionSession.query(VoteStatement).all()
	vote_dict = dict()
	for index, vote in enumerate(db_votes):
		if vote.statement_uid in statement_uid_set:
			tmp_dict = dict()
			tmp_dict['uid']           = vote.uid
			tmp_dict['statement_uid'] = vote.statement_uid
			tmp_dict['author_uid']    = vote.author_uid
			tmp_dict['is_up_vote']    = vote.is_up_vote
			tmp_dict['is_valid']      = vote.is_valid
			vote_dict[str(index)]     = tmp_dict
	ret_dict['vote_statement'] = vote_dict

	return ret_dict


def get_sigma_export(issue, lang):
	"""

	:param issue:
	:param lang:
	:return:
	"""
	logger('ExportLib', 'get_sigma_export', 'main')
	nodes_array = []
	edges_array = []
	db_textversions = DBDiscussionSession.query(TextVersion).all()
	db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
	for statement in db_statements:
		node_dict = dict()
		node_dict['id'] = 'statement_' + str(statement.uid)
		text = next((tv for tv in db_textversions if tv.uid == statement.textversion_uid), None)
		# text = [tv for tv in db_textversions if tv.uid == statement.textversion_uid]
		node_dict['label'] = text.content if text else 'None'
		nodes_array.append(node_dict)

	db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()
	for argument in db_arguments:
		counter = 0
		# add point in the middle of the edge
		node_dict = dict()
		node_dict['id'] = 'argument_' + str(argument.uid)
		node_dict['label'] = ''
		node_dict['size'] = 0
		nodes_array.append(node_dict)

		# edge from premisegroup to the middle point
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
		for premise in db_premises:
			edge_dict = dict()
			edge_dict['id'] = 'edge_' + str(argument.uid) + '_' + str(counter)
			edge_dict['source'] = 'statement_' + str(premise.statement_uid)
			edge_dict['target'] = 'argument_' + str(argument.uid)
			edges_array.append(edge_dict)
			counter += 1

		# edge from the middle point to the conclusion/argument
		edge_dict = dict()
		edge_dict['id'] = 'edge_' + str(argument.uid) + '_' + str(counter)
		edge_dict['source'] = 'argument_' + str(argument.uid)
		if argument.conclusion_uid is not None:
			edge_dict['target'] = 'statement_' + str(argument.conclusion_uid)
		else:
			edge_dict['target'] = 'argument_' + str(argument.argument_uid)
		edges_array.append(edge_dict)

	sigma_dict = {'nodes': nodes_array, 'edges': edges_array}
	return sigma_dict
