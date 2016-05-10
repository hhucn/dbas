"""
Provides methods for comparing strings.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import difflib

from collections import OrderedDict
from sqlalchemy import and_
from Levenshtein import distance

from .database import DBDiscussionSession
from .database.discussion_model import Statement, User, TextVersion, Issue, Premise, Argument
from .logger import logger

max_count_zeros = 5
index_zeros = 3
return_count = 10  # same number as in googles suggest list (16.12.2015)
mechanism = 'Levensthein'
# mechanism = 'SequenceMatcher'


class FuzzyStringMatcher:
	"""
	Compares given string with values in the database and returns set of similar string.
	"""

	def get_strings_for_start(value, issue, is_startpoint):
		"""
		Checks different position-strings for a match with given value

		:param value: string
		:param issue: int
		:param is_startpoint: boolean
		:return: dict()
		"""
		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.is_startpoint == is_startpoint, Statement.issue_uid == issue)).all()
		tmp_dict = dict()
		index = 1
		for statement in db_statements:
			db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=statement.textversion_uid).first()
			if value.lower() in db_textversion.content.lower():
				dist = FuzzyStringMatcher.__get_distance__(value, db_textversion.content)
				tmp_dict[str(dist) + '_' + str(index).zfill(index_zeros)] = db_textversion.content
				index += 1

		return_dict = FuzzyStringMatcher.__sort_dict(tmp_dict)

		logger('FuzzyStringMatcher', 'get_strings_for_start', 'dictionary length: ' + str(len(return_dict.keys())), debug=True)

		return mechanism, return_dict

	def get_strings_for_edits(value, statement_uid):
		"""
		Checks different textversion-strings for a match with given value

		:param value: string
		:param statement_uid:
		:return: dict()
		"""

		# db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == statement_uid,
		#                                                                Statement.issue_uid == issue)).first()
		# db_textversions = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).all()
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).join(User).all()

		tmp_dict = dict()
		index = 1
		for textversion in db_textversions:
			if value.lower() in textversion.content.lower():
				dist = FuzzyStringMatcher.__get_distance__(value, textversion.content)
				tmp_dict[str(dist) + '_' + str(index).zfill(index_zeros)] = textversion.content
				index += 1

		return_dict = FuzzyStringMatcher.__sort_dict(tmp_dict)

		logger('FuzzyStringMatcher', 'get_strings_for_edits', 'string: ' + value + ', string: ' + value +
		       ', statement uid: ' + str(statement_uid) + ', dictionary length: ' + str(len(return_dict.keys())), debug=True)

		return mechanism, return_dict

	def get_strings_for_reasons(value, issue):
		"""
		Checks different textversion-strings for a match with given value

		:param value: string
		:param issue: int
		:return: dict()
		"""
		db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
		tmp_dict = dict()

		index = 1
		for statement in db_statements:
			db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=statement.textversion_uid).first()
			if value.lower() in db_textversion.content.lower():
				dist = FuzzyStringMatcher.__get_distance__(value, db_textversion.content)
				tmp_dict[str(dist) + '_' + str(index).zfill(index_zeros)] = db_textversion.content
				index += 1

		return_dict = FuzzyStringMatcher.__sort_dict(tmp_dict)

		logger('FuzzyStringMatcher', 'get_strings_for_reasons', 'string: ' + value + ', issue: ' + str(issue) +
		       ', dictionary length: ' + str(len(return_dict.keys())), debug=True)

		return mechanism, return_dict

	def get_strings_for_issues(value):
		"""
		Checks different issue-strings for a match with given value

		:param value:
		:return:
		"""
		db_issues = DBDiscussionSession.query(Issue).all()
		tmp_dict = dict()

		for index, issue in enumerate(db_issues):
			dist = FuzzyStringMatcher.__get_distance__(value, issue.title)
			tmp_dict[str(dist) + '_' + str(index).zfill(index_zeros)] = issue.title

		return_dict = FuzzyStringMatcher.__sort_dict(tmp_dict)

		logger('FuzzyStringMatcher', 'get_strings_for_issues', 'string: ' + value +
		       ', dictionary length: ' + str(len(return_dict.keys())), debug=True)

		return mechanism, return_dict

	def get_strings_for_search(value):
		"""
		Returns all statements which have a substring of the given value as well as the arguments, where the statements are used

		:param value: String
		:return: dict() with Statements.uid as key and 'text', 'distance' as well as 'arguments' as values
		"""
		tmp_dict = dict()
		db_statements = DBDiscussionSession.query(Statement).join(TextVersion, Statement.textversion_uid==TextVersion.uid).all()
		for statement in db_statements:
			arg_set = []
			dist = -1
			if value.lower() in statement.textversions.content.lower():
				# get distance between input value and saved value
				dist = FuzzyStringMatcher.__get_distance__(value, statement.textversions.content.lower())
				# get all premise groups with this statement
				group_set = []
				db_premises = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).all()
				for premise in db_premises:
					if premise.premisesgroup_uid not in group_set:
						group_set.append(premise.premisesgroup_uid)
						# get all arguments with this premisegroup
						db_arguments = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=premise.premisesgroup_uid).all()
						for argument in db_arguments:
							arg_set.append(argument.uid)
			tmp_dict[str(statement.uid)] = {'text': statement.textversions.content,
			                                'distance': dist,
			                                'arguments': arg_set}

		return_dict = FuzzyStringMatcher.__sort_dict(tmp_dict)

		logger('FuzzyStringMatcher', 'get_strings_for_search', 'string: ' + value +
		       ', dictionary length: ' + str(len(return_dict.keys())), debug=True)
		return return_dict

	def __sort_dict(dictionary):
		"""

		:return:
		"""
		dictionary = OrderedDict(sorted(dictionary.items()))

		return_dict = OrderedDict()
		for i in list(dictionary.keys())[0:return_count]:
			return_dict[i] = dictionary[i]

		if mechanism == 'SequenceMatcher':  # sort descending
			return_dict = OrderedDict(sorted(dictionary.items(), key=lambda kv: kv[0], reverse=True))
		else:  # sort ascending
			return_dict = OrderedDict()
			for i in list(dictionary.keys())[0:return_count]:
				return_dict[i] = dictionary[i]

		return return_dict

	def __get_distance__(string_a, string_b):
		"""

		:param string_a:
		:param string_b:
		:return:
		"""
		logger('FuzzyStringMatcher', '__get_distance__', string_a + ' - ' + string_b)
		if mechanism == 'Levensthein':
			dist = distance(string_a.lower(), string_b.lower())
			#  logger('FuzzyStringMatcher', '__get_distance__', 'levensthein: ' + str(dist) + ', value: ' + string_a.lower() + ' in: ' + string_b.lower())
		else:
			matcher = difflib.SequenceMatcher(lambda x: x == " ", string_a.lower(), string_b.lower())
			dist = str(round(matcher.ratio() * 100, 1))[:-2]
			# logger('FuzzyStringMatcher', '__get_distance__', 'SequenceMatcher: ' + str(matcher.ratio()) + ', value: ' + string_a.lower() + ' in: ' +  string_b.lower())

		return str(dist).zfill(max_count_zeros)
