import collections

from sqlalchemy import and_
from Levenshtein import distance

from .database import DBDiscussionSession
from .database.discussion_model import Statement, User, TextValue, TextVersion
from .logger import logger

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

# This class handles string search requests
class FuzzyStringMatcher(object):

	def __init__(self):
		self.max_count_zeros = 5

	def get_fuzzy_string_for_start(self, value, issue, isStatement):
		"""
		Levenshtein FTW: checks different start-position-strings for a match with given value
		:param value: string
		:param issue: int
		:param isStatement: boolean
		:return: dict()
		"""
		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_start', 'string: ' + value + ', isStatement: ' + str(isStatement))
		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.isStartpoint==isStatement, Statement.issue_uid==issue)).join(TextValue).all()
		tmp_dict = dict()
		for index, statement in enumerate(db_statements):
			db_textvalue = DBDiscussionSession.query(TextValue).filter_by(uid=statement.text_uid).join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()
			if value.lower() in db_textvalue.textversions.content.lower():
				lev = distance(value.lower(), db_textvalue.textversions.content.lower())
				logger('FuzzyStringMatcher', 'get_fuzzy_string_for_start', 'lev: ' + str(lev) + ', value: ' + value.lower() + ' in: ' +  db_textvalue.textversions.content)
				lev  = str(lev).zfill(self.max_count_zeros)
				tmp_dict[str(lev) + '_' + str(index)] = db_textvalue.textversions.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:10]: # TODO RETURN COUNT
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
		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_edits', 'string: ' + value + ', statement uid: ' + str(statement_uid))

		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid, Statement.issue_uid==issue)).first()
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(textValue_uid=db_statement.text_uid).join(User).all()

		tmp_dict = dict()
		for index, textversion in enumerate(db_textversions):
			if value.lower() in textversion.content.lower():
				lev = distance(value.lower(), textversion.content.lower())
				logger('FuzzyStringMatcher', 'get_fuzzy_string_for_edits', 'lev: ' + str(lev) + ', value: ' + value.lower() + ' in: ' + textversion.content.lower())
				lev  = str(lev).zfill(self.max_count_zeros)
				tmp_dict[str(lev) + '_' + str(index)] = textversion.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:10]: # TODO RETURN COUNT
			return_dict[i] = tmp_dict[i]

		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_edits', 'dictionary length: ' + str(len(return_dict.keys())))

		return return_dict

	def get_fuzzy_string_for_reasons(self, value, issue):
		"""
		Levenshtein FTW: checks different textversion-string for a match with given value
		:param value: string
		:param issue: int
		:return: dict()
		"""
		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_reasons', 'string: ' + value + ', issue: ' + str(issue))
		db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).join(TextValue).all()
		tmp_dict = dict()

		for index, statement in enumerate(db_statements):
			db_textvalue = DBDiscussionSession.query(TextValue).filter_by(uid=statement.text_uid).join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()
			if value.lower() in db_textvalue.textversions.content.lower():
				lev = distance(value.lower(), db_textvalue.textversions.content.lower())
				logger('FuzzyStringMatcher', 'get_fuzzy_string_for_start', 'lev: ' + str(lev) + ', value: ' + value.lower() + ' in: ' +  db_textvalue.textversions.content)
				lev  = str(lev).zfill(self.max_count_zeros)
				tmp_dict[str(lev) + '_' + str(index)] = db_textvalue.textversions.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:10]: # TODO RETURN COUNT
			return_dict[i] = tmp_dict[i]

		logger('FuzzyStringMatcher', 'get_fuzzy_string_for_reasons', 'dictionary length: ' + str(len(return_dict.keys())))

		return return_dict