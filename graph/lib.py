# Common library for Graph Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, TextVersion, Premise, Issue


grey = '#9E9E9E'
red = '#F44336'
green = '#8BC34A'
blue = '#2196F3'
dark_grey = '#616161'
dark_red = '#D32F2F'
dark_green = '#689F38'
dark_blue = '#1976D2'


def get_sigma_data(issue):
	"""

	:param issue:
	:return:
	"""
	logger('GraphLib', 'get_sigma_data', 'main')
	x = 0
	y = 0
	node_size = 6
	position_size = 6
	issue_size = 8
	edge_size = 2
	edge_type = 'arrow'

	nodes_array = []
	edges_array = []
	db_issue = DBDiscussionSession.query(Issue).filter_by(uid=issue).first()
	db_textversions = DBDiscussionSession.query(TextVersion).all()
	db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
	db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()

	# issue
	node_dict = __get_node_dict('issue',
	                            db_issue.info,
	                            blue,
	                            issue_size,
	                            x,
	                            y)
	x = (x + 1) % 10
	y += (1 if x == 0 else 0)
	nodes_array.append(node_dict)

	# for each statement a node will be added
	for statement in db_statements:
		text = next((tv for tv in db_textversions if tv.uid == statement.textversion_uid), None)
		text = text.content if text else 'None'
		node_dict = __get_node_dict('statement_' + str(statement.uid),
		                            text,
		                            blue if statement.is_startpoint else grey,
		                            position_size if statement.is_startpoint else node_size,
		                            x,
		                            y)
		x = (x + 1) % 10
		y += (1 if x == 0 else 0)
		nodes_array.append(node_dict)
		if statement.is_startpoint:
			edge_dict = __get_edge_dict('edge_' + str(statement.uid) + '_issue',
			                            'statement_' + str(statement.uid),
			                            'issue',
			                            grey,
			                            edge_size,
			                            edge_type)
			edges_array.append(edge_dict)

	# for each argument edges will be added as well as the premises
	for argument in db_arguments:
		counter = 0
		# add invisible point in the middle of the edge (to enable pgroups and undercuts)
		node_dict = __get_node_dict('argument_' + str(argument.uid),
		                            '',
		                            green if argument.is_supportive else red,
		                            0.5,
		                            x,
		                            y)
		x = (x + 1) % 10
		y += (1 if x == 0 else 0)
		nodes_array.append(node_dict)

		# edge from premisegroup to the middle point
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
		for premise in db_premises:
			edge_dict = __get_edge_dict('edge_' + str(argument.uid) + '_' + str(counter),
			                            'statement_' + str(premise.statement_uid),
			                            'argument_' + str(argument.uid),
			                            green if argument.is_supportive else red,
			                            edge_size,
			                            '')
			edges_array.append(edge_dict)
			counter += 1

		# edge from the middle point to the conclusion/argument
		target = 'statement_' + str(argument.conclusion_uid) if argument.conclusion_uid is not None else 'argument_' + str(argument.argument_uid)
		edge_dict = __get_edge_dict('edge_' + str(argument.uid) + '_' + str(counter),
		                            'argument_' + str(argument.uid),
		                            target,
		                            green if argument.is_supportive else red,
		                            edge_size,
		                            edge_type)
		edges_array.append(edge_dict)

	sigma_dict = {'nodes': nodes_array, 'edges': edges_array}
	return sigma_dict


def __get_node_dict(uid, label, color, size, x, y, borderSize=0):
	"""

	:param uid:
	:param label:
	:param color:
	:param size:
	:param x:
	:param y:
	:param borderSize:
	:return:
	"""
	return {'id': uid,
	        'label': label,
	        'color': color,
	        'hover_color': dark_grey if color == green else dark_blue,
	        'borderColor': color,
	        'borderSize': borderSize,
	        'size': size,
	        'x': x,
	        'y': y}


def __get_edge_dict(uid, source, target, color, size, edge_type):
	"""

	:param uid:
	:param source:
	:param target:
	:param color:
	:param size:
	:param edge_type:
	:return:
	"""
	return {'id': uid,
	        'source': source,
	        'target': target,
	        'color': color,
	        'hover_color': dark_green if color == green else dark_red,
	        'size': size,
	        'type': edge_type}
