import collections
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Relation, Track, Issue, \
	History
from .logger import logger
from .strings import Translator
from .query_helper import QueryHelper

# todo pathfinder

class PathFinder(object):

	def get_path_from_statement_to_statement(self, start_statement_uid, end_statement_uid, get_all_path, restriction_dict):
		"""

		:param start_statement_uid: uid of the database entry
		:param end_statement_uid: uid of the database entry
		:param get_all_path: boolean
		:param restriction_dict: dict with restrictions: valid entries are {'issue': uid, 'author':uid}
		:return:
		"""
		start = DBDiscussionSession.query(Statement).filter_by(uid=start_statement_uid)
		end = DBDiscussionSession.query(Statement).filter_by(uid=end_statement_uid)
		# link to get_path_from_argument_to_argument
		return None

	def get_path_from_argument_to_argument(self, start_argument_uid, end_argument_uid, get_all_path, restriction_dict):
		"""

		:param start_statement_uid: uid of the database entry
		:param end_statement_uid: uid of the database entry
		:param get_all_path: boolean
		:param restriction_dict: dict with restrictions: valid entries are {'issue': uid, 'author':uid}
		:return:
		"""

		return_dict = collections.OrderedDict()

		start = DBDiscussionSession.query(Argument).filter_by(uid=start_argument_uid)
		end = DBDiscussionSession.query(Argument).filter_by(uid=end_argument_uid)

		if start.uid == end.uid:
			return_dict = True
		else:
			return_dict = True


		return return_dict