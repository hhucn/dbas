import random
import json
from .database import DBSession
from .database.model import Statement, User, TextValue, TextVersion, Premisse
from .logger import logger

class DictionaryHelper(object):

	def get_random_subdict_out_of_orderer_dict(self, ordered_dict, count):
		"""
		Creates a random subdictionary with given count out of the given ordered_dict.
		With a count of <2 the dictionary itself will be returned.
		:param ordered_dict: dictionary for the function
		:param count: count of entries for the new dictionary
		:return: dictionary
		"""
		return_dict = dict()
		logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'count: ' + str(count))
		items = list(ordered_dict.items())
		for item in items:
			logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'all items: ' + ''.join(str(item)))
		if count < 0:
			return ordered_dict
		elif count == 1:
			if len(items) > 1:
				rnd = random.randint(0, len(items)-1)
				logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'return item at ' + str(rnd))
				return_dict[items[rnd][0]] = items[rnd][1]
			else:
				return ordered_dict
		else:

			for i in range(0, count):
				rnd = random.randint(0, len(items)-1)
				logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'for loop ' + str(i) + '. add element at ' + str(rnd))
				return_dict[items[rnd][0]] = items[rnd][1]
				items.pop(rnd)

		return return_dict

	def dictionarty_to_json_array(self, raw_dict, ensure_ascii):
		"""
		Dumps given dictionary into json
		:param raw_dict: dictionary for dumping
		:param ensure_ascii: if true, ascii will be checked
		:return: json data
		"""
		return_dict = json.dumps(raw_dict, ensure_ascii)
		return return_dict

	def save_statement_row_in_dictionary(self, statement_row):
		"""
		Saved a row in dictionary
		:param statement_row: for saving
		:return: dictionary
		"""
		db_statement    = DBSession.query(Statement).filter_by(uid=statement_row.uid).join(TextValue).first()
		db_premisse     = DBSession.query(Premisse).filter_by(statement_uid=db_statement.uid).first()
		db_textversion  = DBSession.query(TextVersion).filter_by(uid=db_statement.textvalues.textVersion_uid).join(User).first()

		uid    = str(db_statement.uid)
		text   = db_textversion.content
		date   = str(db_textversion.timestamp)
		weight = str(db_textversion.weight)
		author = db_textversion.users.nickname
		pgroup = str( db_premisse.premissesGroup_uid) if db_premisse else '0'

		while text.endswith('.'):
			text = text[:-1]

		logger('DictionaryHelper', 'save_statement_row_in_dictionary', uid + ', ' + text + ', ' + date + ', ' + weight + ', ' + author +
		       ', ' + pgroup)
		return {'uid':uid, 'text':text, 'date':date, 'weight':weight, 'author':author, 'premissegroup_uid':pgroup}