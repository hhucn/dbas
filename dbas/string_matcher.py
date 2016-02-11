import collections
import difflib

from sqlalchemy import and_
from Levenshtein import distance

from .database import DBDiscussionSession
from .database.discussion_model import Statement, User, TextVersion
from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class FuzzyStringMatcher(object):

	def __init__(self):
		self.max_count_zeros = 5
		self.return_count = 10  # same number as in googles suggest list (16.12.2015)

	def get_fuzzy_string_for_start(self, value, issue, is_startpoint):
		"""
		Levenshtein FTW: checks different start-position-strings for a match with given value
		:param value: string
		:param issue: int
		:param is_startpoint: boolean
		:return: dict()
		"""
		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.is_startpoint == is_startpoint, Statement.issue_uid == issue)).all()
		tmp_dict = dict()
		for index, statement in enumerate(db_statements):
			db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=statement.textversion_uid).first()
			if value.lower() in db_textversion.content.lower():
				dist = self.__get_distance__(value, db_textversion.content)
				tmp_dict[str(dist) + '_' + str(index)] = db_textversion.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:self.return_count]:
			return_dict[i] = tmp_dict[i]

		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_start', 'dictionary length: ' + str(len(return_dict.keys())))

		return return_dict

	def get_fuzzy_string_for_edits(self, value, statement_uid, issue):
		"""
		Levenshtein FTW: checks different textversion-strings for a match with given value
		:param value: string
		:param statement_uid:
		:param issue: int
		:return: dict()
		"""

		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == statement_uid,
		                                                                Statement.issue_uid == issue)).first()
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).all()

		tmp_dict = dict()
		for index, textversion in enumerate(db_textversions):
			if value.lower() in textversion.content.lower():
				dist = self.__get_distance__(value, textversion.content)
				tmp_dict[str(dist) + '_' + str(index)] = textversion.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:self.return_count]:
			return_dict[i] = tmp_dict[i]

		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_edits', 'string: ' + value + ', is_startpoint: ' +
		       str(is_startpoint) + ', string: ' + value + ', statement uid: ' + str(statement_uid) +
		       ', dictionary length: ' + str(len(return_dict.keys())))

		return return_dict

	def get_fuzzy_string_for_reasons(self, value, issue):
		"""
		Levenshtein FTW: checks different textversion-string for a match with given value
		:param value: string
		:param issue: int
		:return: dict()
		"""
		db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
		tmp_dict = dict()

		for index, statement in enumerate(db_statements):
			db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=statement.textversion_uid).first()
			if value.lower() in db_textversion.content.lower():
				dist = self.__get_distance__(value, db_textversion.content)
				tmp_dict[str(dist) + '_' + str(index)] = db_textversion.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:self.return_count]:
			return_dict[i] = tmp_dict[i]

		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_reasons', 'string: ' + value + ', issue: ' + str(issue) +
		       ', dictionary length: ' + str(len(return_dict.keys())))

		return return_dict

	def __get_distance__(self, string_a, string_b):
		"""

		:param string_a:
		:param string_b:
		:return:
		"""
		dist = distance(string_a.lower(), string_b.lower())
		#  logger('FuzzyStringMatcher', '__get_distance__', 'levensthein: ' + str(dist) + ', value: ' + string_a.lower() + ' in: ' + string_b.lower())

		# matcher = difflib.SequenceMatcher(lambda x: x == " ", string_a.lower(), string_b.lower())
		# dist = round(matcher.ratio()*100,1)
		# logger('FuzzyStringMatcher', '__get_distance__', 'SequenceMatcher: ' + str(matcher.ratio()) + ', value: ' + string_a.lower() + ' in: ' +  string_b.lower())

		return str(dist).zfill(self.max_count_zeros)
