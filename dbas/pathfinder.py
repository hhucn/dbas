from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise

# TODO: PathFinder ... BUT WHY?

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class PathFinder(object):

	def get_shortest_path_from_argument_to_argument(self, start_argument_uid, end_argument_uid, lang):
		"""
		Returns shortest path between two arguments
		:param start_argument_uid: uid of the database entry
		:param end_argument_uid: uid of the database entry
		:param lang: string
		:return: []
		"""

		start = DBDiscussionSession.query(Argument).filter_by(uid=start_argument_uid)
		end = DBDiscussionSession.query(Argument).filter_by(uid=end_argument_uid)
		if start.issue_uid != end.issue_uid:
			return None

		return self.do_dijkstra(DBDiscussionSession.query(Argument).filter_by(issue_uid=start.issue_uid).all(), start, end)

	def get_non_visited_neighbours_of_argument(self, argument, already_visited):
		"""
		Returns a list with all connected, non-visted arguments.
		Looks for relations regarding the premise, conclusion and the argument itself.
		:param argument:
		:param already_visited:
		:return:
		"""
		l = self.get_neighbours_of_argument(argument)
		return list(set(l) - already_visited)

	def get_neighbours_of_argument(self, argument):
		"""
		Returns a list with all connected arguments.
		Looks for relations regarding the premise, conclusion and the argument itself.
		:param argument: Argument
		:return: []
		"""
		l = []

		db_args_premise = DBDiscussionSession.query(Premise).filter_by(premisesGroup_uid=argument.premisesGroup_uid).all()
		for premise in db_args_premise:
			db_statement = DBDiscussionSession.query(Statement).filter_by(premise.statement_uid).first()
			db_next_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_statement.uid).all()
			for arg in db_next_arguments:
				l.append(arg.uid)

		# all relations to the current relation (undercuts and overbids)
		db_args_relation = DBDiscussionSession.query(Argument).filter_by(argument_uid=argument.uid).all()
		for arg in db_args_relation:
			l.append(arg.uid)

		# all relations to the conclusion (rebuts)
		if argument.conclusion_uid != 0:
			db_args_conclusion = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=argument.conclusion_uid).all()
			for arg in db_args_conclusion:
				l.append(arg.uid)
		if argument.argument_uid != 0:
			db_next_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument.argument_uid).all()
			for arg in db_next_argument:
				l.append(arg)

		return list


	def do_dijkstra(self, all_arguments, start_argument, end_argument):
		"""
		Simply Dijkstra!
		:param all_arguments: Argument
		:param start_argument: Argument
		:return: []
		"""
		# init graph
		distance = {}
		predecessor = []
		for argument in all_arguments:
			distance[str(argument.uid)] = 0
		distance[str(start_argument.uid)] = 0

		# while there are still arguments left
		while len(all_arguments)>0:
			# get current argument with smallest distance and his neighbours
			current, all_arguments = self.get_argument_with_smallest_distance_out_of_set(all_arguments, distance)
			neighbours = self.get_neighbours_of_argument(current)

			# break, if we are there
			if current == end_argument:
				return predecessor.reverse

			# for all non visited neigbours
			for neighbour in set(neighbours):
				if neighbour in all_arguments:
					# update distances
					alternativ = distance[str(current.uid)] + self.distance_between(current.uid, neighbour.uid)
					if alternativ < distance[str(neighbour.uid)]:
						distance[str(neighbour.uid)] = alternativ
						predecessor.append(current.uid)

		return predecessor.reverse

	def get_argument_with_smallest_distance_out_of_set(self, all_arguments, distance):
		"""
		Returns the first argument in the set of all arguments
		:param all_arguments: {}
		:param distance: {}
		:return: Argument, {Arguments}
		"""
		# todo: what is distance ?
		elem = all_arguments.pop(0)
		return elem, all_arguments

	def distance_between(self, arg1_uid, arg2_uid):
		"""
		Returns the distance between two connected arguments. Currently this is just one
		:param arg1_uid: int
		:param arg2_uid: int
		:return: int
		"""
		# todo: what is distance ?
		return 1