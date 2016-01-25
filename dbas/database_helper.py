import random
import collections

from sqlalchemy import and_
from datetime import datetime

from .database import DBDiscussionSession, DBNewsSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup,  Track, \
	Relation, Issue
from .database.news_model import News
from .dictionary_helper import DictionaryHelper
from .query_helper import QueryHelper
from .user_management import UserHandler
from .logger import logger
from .strings import Translator
from .tracking_helper import TrackingHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class DatabaseHelper(object):

	def get_news(self):
		"""
		Returns all news in a dicitionary, sorted by date
		:return: dict()
		"""
		logger('DatabaseHelper', 'get_news', 'main')
		db_news = DBNewsSession.query(News).all()
		logger('DatabaseHelper', 'get_news', 'we have ' + str(len(db_news)) + ' news')
		ret_dict = dict()
		for index, news in enumerate(db_news):
			news_dict = dict()
			news_dict['title'] = news.title
			news_dict['author'] = news.author
			news_dict['date'] = news.date
			news_dict['news'] = news.news
			news_dict['uid'] = str(news.uid)
			# string date into date
			date_object = datetime.strptime(str(news.date), '%d.%m.%Y')
			# add index on the seconds for unique id's
			sec = (date_object - datetime(1970,1,1)).total_seconds() + index
			logger('DatabaseHelper', 'get_news', 'news from  ' + str(news.date) + ', ' + str(sec))
			ret_dict[str(sec)] = news_dict

		ret_dict = collections.OrderedDict(sorted(ret_dict.items()))

		return ret_dict

	def set_news(self, transaction, title, text, user):
		"""
		Sets a new news into the news table
		:param transaction: current transaction
		:param title: news title
		:param text: news text
		:param user: self.request.authenticated_userid
		:return: dictionary {title,date,author,news}
		"""
		logger('DatabaseHelper', 'set_news', 'def')
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		author = db_user.firstname if db_user.firstname == 'admin' else db_user.firstname + ' ' + db_user.surname
		now = datetime.now()
		day = str(now.day) if now.day > 9 else ('0' + str(now.day))
		month = str(now.month) if now.month > 9 else ('0' + str(now.month))
		date = day + '.' + month + '.' + str(now.year)
		news = News(title = title, author = author, date = date, news = text)

		DBNewsSession.add(news)
		DBNewsSession.flush()

		db_news = DBNewsSession.query(News).filter_by(title=title).first()
		return_dict = dict()

		if db_news:
			logger('DatabaseHelper', 'set_news', 'new news is in db')
			return_dict['status'] = '1'
		else:

			logger('DatabaseHelper', 'set_news', 'new news is not in db')
			return_dict['status'] = '-'

		transaction.commit()

		return_dict['title'] = title
		return_dict['date'] = date
		return_dict['author'] = author
		return_dict['news'] = text

		return return_dict

	def correct_statement(self, transaction, user, uid, corrected_text):
		"""
		Corrects a statement
		:param transaction: current transaction
		:param user: requesting user
		:param uid: requested statement uid
		:param corrected_text: new text
		:return: True
		"""
		logger('DatabaseHelper', 'correct_statement', 'def ' + str(uid))

		return_dict = dict()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()

		if corrected_text.endswith(('.','?','!')):
			corrected_text = corrected_text[:-1]

		# duplicate check
		db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(TextVersion.uid.desc()).first()

		if db_user:
			logger('DatabaseHelper', 'correct_statement', 'given user exists and correction will be set')
			# duplicate or not?
			if db_textversion:
				textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=db_textversion.uid).first()
			else:
				textversion = TextVersion(content=corrected_text, author=db_user.uid)
				textversion.set_statement(db_statement.uid)
				DBDiscussionSession.add(textversion)
				DBDiscussionSession.flush()

			db_statement.set_textversion(textversion.uid)
			transaction.commit()
			return_dict['status'] = '1'
		else:
			logger('DatabaseHelper', 'correct_statement', 'user not found')
			return_dict['status'] = '-1'

		return_dict['uid'] = uid
		return_dict['text'] = corrected_text
		return return_dict

	def get_issue_list(self, lang):
		"""
		Returns all isuees as dictionary
		:param lang: dict() with {uid, text, date}
		:return:
		"""
		logger('DatabaseHelper', 'get_issue_list', 'main')
		db_issues = DBDiscussionSession.query(Issue).all()
		return_dict = dict()
		for issue in db_issues:
			logger('DatabaseHelper', 'get_issue_list', 'issue no ' + str(issue.uid) + ': ' + issue.title)
			db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue.uid).all()
			return_dict[str(issue.uid)] = {'uid': str(issue.uid),
										   'title': issue.title,
										   'info': issue.info,
										   'date': QueryHelper().sql_timestamp_pretty_print(str(issue.date), lang),
										   'arguments': str(len(db_arguments))}

		if not db_issues:
			logger('DatabaseHelper', 'get_issue_list', 'no issues')

		return_dict = collections.OrderedDict(sorted(return_dict.items()))
		return return_dict

	def get_attack_overview(self, user, issue, lang):
		"""
		Returns a dicitonary with all attacks, done by the users, but only if the user has admin right!
		:param user: current user
		:param issue: current issue
		:param lang: current language
		:return: dict()
		"""
		is_admin = UserHandler().is_user_admin(user)
		logger('DatabaseHelper', 'get_attack_overview', 'is_admin ' + str(is_admin) + ', issue ' + str(issue))
		return_dict = dict()
		if is_admin:
			return_dict = dict()
			logger('DatabaseHelper', 'get_attack_overview', 'get all attacks for each argument')
			db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()
			db_relations = DBDiscussionSession.query(Relation).all()

			relations_dict = dict()
			for relation in db_relations:
				relations_dict[str(relation.uid)] = relation.name
			return_dict['attacks'] = relations_dict

			for argument in db_arguments:
				logger('DatabaseHelper', 'get_attack_overview', 'argument with uid ' + str(argument.uid) + ', issue ' + str(issue))
				text = QueryHelper().get_text_for_argument_uid(argument.uid, lang)
				if text:
					argument_dict = {'id': str(argument.uid), 'text': text}

				for relation in db_relations:
					db_tracks = DBDiscussionSession.query(Track).filter(and_(Track.argument_uid==argument.uid,
					                                               Track.attacked_by_relation==relation.uid)).all()
					argument_dict[relation.name] = str(len(db_tracks)) if len(db_tracks) != 0 else '-'

				return_dict[str(argument.uid)] = argument_dict

		return return_dict

	def get_start_statements(self, issue):
		"""
		Returns start statements
		:param issue:
		:return:
		"""
		return_dict = dict()
		statements_dict = dict()
		db_statements = DBDiscussionSession.query(Statement)\
			.filter(and_(Statement.isStartpoint==True, Statement.issue_uid==issue))\
			.join(TextVersion, TextVersion.uid==Statement.textversion_uid).all()
		logger('DatabaseHelper', 'get_start_statements', 'get all statements for issue ' + str(issue))
		if db_statements:
			return_dict['status'] = '1'
			logger('DatabaseHelper', 'get_start_statements', 'there are start statements')
			for statement in db_statements:
				logger('DatabaseHelper', 'get_start_statements', 'statement ' + str(statement.uid) + ': ' + statement.textversions.content)
				statements_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement, issue)
		else:
			logger('DatabaseHelper', 'get_start_statements', 'there are no statements')
			return_dict['status'] = '0'

		return_dict['statements'] = statements_dict
		return return_dict

	def get_text_for_statement(self, statement_uid, issue):
		"""
		Returns dictionary with all information about the given statement ui
		:param statement_uid: recent uid of the statement
		:param issue: current issue
		:return: dict()
		"""
		logger('DatabaseHelper', 'get_text_for_statement', 'get all premises: conclusion_uid: ' + str(statement_uid) + ', issue_uid: ' + str(issue))

		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid,Statement.issue_uid==issue)).first()
		return_dict = DictionaryHelper().save_statement_row_in_dictionary(db_statement, issue)

		return return_dict

	def get_reply_confrontations_response(self, transaction, user, uid_text, session_id, exception_rebut, issue, lang):
		"""
		Returns the answer for a confrontation by the user. We will differentiate between {undermine, support, undercut, overbid, rebut}
		:param transaction: transaction
		:param user: string
		:param uid_text: int
		:param session_id: id
		:param exception_rebut: boolean
		:param issue: int
		:param lang: string
		:return: dict()
		"""
		qh = QueryHelper()
		splitted_id = uid_text.split('_')
		relation = splitted_id[0]
		argument_uid = splitted_id[2]

		# get argument
		logger('DatabaseHelper', 'get_reply_confrontations_response', 'get reply confrontations for argument ' + argument_uid + ', issue ' + str(issue))
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==int(argument_uid), Argument.issue_uid==issue)).first()

		# get attack
		key = 'reason'

		status = '1'
		if 'undermine' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'undermine')
			return_dict = qh.get_undermines_for_argument_uid(key, argument_uid, issue)
			return_dict['attack'] = 'undermine'
			identifier = 'premisesgroup'
		elif 'support' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'support')
			return_dict = qh.get_supports_for_argument_uid(key, argument_uid, issue)
			return_dict['attack'] = 'support'
			identifier = 'premisesgroup'
		elif 'undercut' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'undercut')
			return_dict = qh.get_undercuts_for_argument_uid(key, argument_uid, issue)
			return_dict['attack'] = 'undercut'
			identifier = 'statement'
		elif 'overbid' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'overbid')
			return_dict = qh.get_overbids_for_argument_uid(key, argument_uid, issue)
			return_dict['attack'] = 'overbid'
			identifier = 'statement'
		elif 'rebut' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'rebut')
			#return_dict = qh.get_rebuts_for_argument_uid(key, argument_uid)
			if exception_rebut:
				return_dict = qh.get_rebuts_for_argument_uid(key, argument_uid, issue)
			else:
				return_dict = qh.get_supports_for_argument_uid(key, argument_uid, issue)
			identifier = 'premisesgroup'
			return_dict['attack'] = 'rebut'
		else:
			return_dict = dict()
			identifier = 'none'
			status = '-1'

		logger('DatabaseHelper', 'get_reply_confrontations_response', 'attack (' + relation + ') was fetched for ' + str(argument_uid))

		# check return value
		if not return_dict:
			return_dict = dict()
		if len(return_dict) == 0:
			return_dict[key] = '0'

		return_dict['premisegroup'], uids = qh.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid)
		# Todo: what is with an conclusion as premise group?
		return_dict['relation'] = splitted_id[0]
		return_dict['argument_uid'] = argument_uid
		return_dict['premisegroup_uid'] = db_argument.premisesGroup_uid
		return_dict['type'] = identifier

		if db_argument.conclusion_uid is None or db_argument.conclusion_uid == 0:
			return_dict['conclusion_text'] = qh.get_text_for_argument_uid(db_argument.argument_uid, lang)
			logger('DatabaseHelper', 'get_reply_confrontations_response', return_dict['conclusion_text'])
		else:
			return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_argument.conclusion_uid)
			logger('DatabaseHelper', 'get_reply_confrontations_response', return_dict['conclusion_text'])

		TrackingHelper().save_track_for_user(transaction, user, 0, 0, argument_uid, 0, qh.get_relation_uid_by_name(relation.lower()), session_id)

		return return_dict, status

	def get_logfile_for_statement(self, uid):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:return: dictionary with the logfile-rows
		"""
		logger('DatabaseHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).join(User).all()

		return_dict = dict()
		content_dict = dict()
		# add all corrections
		for index, versions in enumerate(db_textversions):
			corr_dict = dict()
			corr_dict['uid'] = str(versions.uid)
			corr_dict['author'] = str(versions.users.nickname)
			corr_dict['date'] = str(versions.timestamp)
			corr_dict['text'] = str(versions.content)
			content_dict[str(index)] = corr_dict
			logger('DatabaseHelper', 'get_logfile_for_statement', 'statement ' + str(index) + ': ' + versions.content)
		return_dict['content'] = content_dict

		return return_dict

	def get_logfile_for_premisegroup(self, uid, issue):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:param issue:
		:return: dictionary with the logfile-rows
		"""
		logger('DatabaseHelper', 'get_logfile_for_premisegroup', 'def with uid: ' + str(uid))

		db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==uid,
		                                                              Premise.issue_uid==issue)).first()
		# todo for  premise groups
		return self.get_logfile_for_statement(db_premises.statement_uid, issue)

	def set_statement(self, transaction, statement, user, is_start, issue):
		"""
		Saves statement for user
		:param transaction: current transaction
		:param statement: given statement
		:param user: given user
		:param is_start: if it is a start statement
		:param issue:
		:return: '1'
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'set_statement', 'user: ' + str(user) + ', user_id: ' + str(db_user.uid) + ', statement: ' + str(
			statement) + ', issue: ' + str(issue))

		# check for dot at the end
		if not statement.endswith(('.','?','!')):
			statement += '.'
		if statement.lower().startswith('because '):
			statement = statement[8:]

		# check, if the statement already exists
		logger('DatabaseHelper', 'set_statement', 'check for duplicate with: ' + statement)
		db_duplicate = DBDiscussionSession.query(TextVersion).filter_by(content=statement).first()
		if db_duplicate:
			db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid==db_duplicate.uid,
			                                                                Statement.issue_uid==issue)).first()
			logger('DatabaseHelper', 'set_statement', 'duplicate, returning old statement with uid ' + str(db_statement.uid))
			return db_statement, True

		# add the version
		textversion = TextVersion(content=statement, author=db_user.uid)
		DBDiscussionSession.add(textversion)
		DBDiscussionSession.flush()

		# add the statement
		statement = Statement(textversion=textversion.uid, isstartpoint=is_start, issue=issue)
		DBDiscussionSession.add(statement)
		DBDiscussionSession.flush()

		# get the new statement
		new_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid==textversion.uid,
		                                                                 Statement.issue_uid==issue)).order_by(Statement.uid.desc()).first()
		textversion.set_statement(new_statement.uid)

		transaction.commit()

		logger('DatabaseHelper', 'set_statement', 'returning new statement with uid ' + str(new_statement.uid))
		return new_statement, False

	def set_premises_for_conclusion(self, transaction, user, text, conclusion_id, is_supportive, issue):
		"""
		Inserts the given dictionary with premises for an statement or an argument
		:param transaction: current transaction for the database
		:param user: current users nickname
		:param text: text
		:param conclusion_id:
		:param is_supportive: for the argument
		:return: dict
		"""
		logger('DatabaseHelper', 'set_premises_for_conclusion', 'main')

		# insert the premises as statements
		qh = QueryHelper()

		# current conclusion
		db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==conclusion_id, Statement.issue_uid==issue)).first()

		# first, save the premise as statement
		new_statement, is_duplicate = self.set_statement(transaction, text, user, False, issue)
		# duplicates do not count, because they will be fetched in set_statement_as_new_premise

		# second, set the new statement as premise
		new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
		logger('DatabaseHelper', 'set_premises_for_conclusion', text + ' in new_premisegroup_uid ' + str(new_premisegroup_uid)
		       + ' to statement ' + str(db_conclusion.uid) + ', ' + ('' if is_supportive else '' ) + 'supportive')

		# third, insert the argument
		qh.set_argument(transaction, user, new_premisegroup_uid, db_conclusion.uid, 0, is_supportive, issue)

		# we need the 'pro'-key cause the callback uses a method, where we differentiate between several prefixes
		return_dict = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)

		transaction.commit()
		return return_dict, is_duplicate

	def handle_inserting_new_statements(self, user, pro_dict, con_dict, transaction, argument_id, premisegroup_id,
	                                    current_attack, last_attack, premisegroup_con, premisegroup_pro, exception_rebut, issue):
		"""
		Highly complex stuff! Please ask the author!
		:param user: string
		:param pro_dict: dict()
		:param con_dict: dict()
		:param transaction: transactiom
		:param argument_id: int
		:param premisegroup_id: int
		:param current_attack: string
		:param last_attack: string
		:param premisegroup_con: boolean
		:param premisegroup_pro: boolean
		:param exception_rebut: boolean
		:param issue: int
		:return: dict()
		"""
		# Interpretation of the parameters
		# User says: E => A             | #argument_id
		# System says:
		#   undermine:  F => !E         | #premisegroup_id => (part of argument_id)
		#   undercut:   D => !(E=>A)    | #premisegroup_id => (part of argument_id)
		#   rebut:      B => !A         | #premisegroup_id => (part of argument_id)
		# Handle it, based on current and last attack

		return_dict = dict()
		logger('DatabaseHelper', 'handle_inserting_new_statements', 'length of pro dict: ' + str(len(pro_dict)))
		logger('DatabaseHelper', 'handle_inserting_new_statements', 'length of con dict: ' + str(len(con_dict)))

		# id of user
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('DatabaseHelper', 'handle_inserting_new_statements', 'users nick: ' + user + ', id ' + str(db_user.uid))

		logger('DatabaseHelper', 'handle_inserting_new_statements', 'db_premises_of_current_attack premisesGroup_uid=' + str(premisegroup_id))
		db_premises_of_current_attack = DBDiscussionSession.query(Premise).filter(and_(
			Premise.premisesGroup_uid==premisegroup_id, Premise.issue_uid==issue)).all()

		for premise in db_premises_of_current_attack:
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'db_premises_of_current_attack premise.statement_uid ' + str(premise.statement_uid))

		logger('DatabaseHelper', 'handle_inserting_new_statements', 'db_argument_of_current_attack: '
		       + ' premisesGroup_uid=' + str(premisegroup_id)
		       + ', argument_id=' + str(argument_id))
		db_argument_of_current_attack = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==premisegroup_id,
		                                                                                Argument.uid==argument_id,
		                                                                                Argument.issue_uid==issue)).first()
		new_premisegroup_uid = None
		is_inserted = False
		qh = QueryHelper()

		#############
		# UNDERMINE #
		#############
		if current_attack == 'undermine':
			return_dict['same_group'] = '1' if premisegroup_con else '0'
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undermine')
			argument_list = []
			# for every statement in current dictionary
			for index, con in enumerate(con_dict):
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undermine: ' + con_dict[con] + ', with same pgroup: ' + str(premisegroup_con))
				# every entry of the dict will be a new statement with a new premisegroup
				new_statement, is_duplicate = self.set_statement(transaction, con_dict[con], user, False, issue)
				if premisegroup_con:
					# Todo handle duplicats in pgroups
					if new_premisegroup_uid is None:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undermine: new pgroup, but this one will be for all')
						new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
					else:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undermine: old pgroup')
						qh.set_statement_as_premise(new_statement, user, new_premisegroup_uid, issue)
				else:
					logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undermine: every round, new pgroup')
					new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undermine: new_premisegroup_uid is ' + str(new_premisegroup_uid))
				# now, every new statement will attack the attack of the system, which is as confrontation_uid
				for premise in db_premises_of_current_attack:
					# now, every new statement will be inserted, because groups will be added once only
					if (premisegroup_con):
						if (not is_inserted):
							new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=False, author=db_user.uid, weight=0, conclusion=premise.statement_uid, issue=issue)
							argument_list.append(new_argument)
							is_inserted = True
					else:
						new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=False, author=db_user.uid, weight=0, conclusion=premise.statement_uid, issue=issue)
						argument_list.append(new_argument)
				key = 'con_' + current_attack + '_premisegroup_' + str(new_premisegroup_uid) + '_index_' + str(index)
				return_dict[key] = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)
				return_dict[key]['duplicate'] = str(is_duplicate)
			return_dict['duplicates'] = qh.add_arguments(transaction, argument_list)

		###########
		# SUPPORT #
		###########
		elif current_attack == 'support':
			return_dict['same_group'] = '1' if premisegroup_pro else '0'
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch support')
			argument_list = []
			# for every statement in current dictionary
			for index, pro in enumerate(pro_dict):
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch support: ' + pro_dict[pro] + ', with same pgroup: ' + str(premisegroup_pro))
				# every entry of the dict will be a new statement with a new premisegroup
				new_statement, is_duplicate = self.set_statement(transaction, pro_dict[pro], user, False, issue)
				# new pgroup only if they should be new
				if premisegroup_pro:
					# Todo handle duplicats in pgroups
					if new_premisegroup_uid is None:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch support: new pgroup, but this one will be for all')
						new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
					else:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch support: old pgroup')
						qh.set_statement_as_premise(new_statement, user, new_premisegroup_uid, issue)
				else:
					logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch support: every round, new pgroup')
					new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch support: new_premisegroup_uid is ' + str(new_premisegroup_uid))
				# now, every new statement will attack the attack of the system, which is as confrontation_uid
				for premise in db_premises_of_current_attack:
					# now, every new statement will be inserted, because groups will be added once only
					if (premisegroup_pro):
						if (not is_inserted):
							new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=True, author=db_user.uid, weight=0, conclusion=premise.statement_uid, issue=issue)
							argument_list.append(new_argument)
							is_inserted = True
					else:
						new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=True, author=db_user.uid, weight=0, conclusion=premise.statement_uid, issue=issue)
						argument_list.append(new_argument)
				key = 'pro_' + current_attack + '_premisegroup_' + str(new_premisegroup_uid) + '_index_' + str(index)
				return_dict[key] = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)
				return_dict[key]['duplicate'] = str(is_duplicate)
			return_dict['duplicates'] = qh.add_arguments(transaction, argument_list)

		############
		# UNDERCUT #
		############
		elif current_attack == 'undercut':
			return_dict['same_group'] = '1' if premisegroup_con else '0'
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undercut')
			argument_list = []
			# for every statement in current dictionary
			for index, con in enumerate(con_dict):
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undercut: ' + con_dict[con] + ', with same pgroup: ' + str(premisegroup_con))
				new_statement, is_duplicate = self.set_statement(transaction, con_dict[con], user, False, issue)
				if premisegroup_con:
					# Todo handle duplicats in pgroups
					if new_premisegroup_uid is None:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undercut: new pgroup, but this one will be for all')
						new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
					else:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undercut: old pgroup')
						qh.set_statement_as_premise(new_statement, user, new_premisegroup_uid, issue)
				else:
					logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undercut: every round, new pgroup')
					new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch undercut: new_premisegroup_uid is ' + str(new_premisegroup_uid))
				# now, every new statement will be inserted, because groups will be added once only
				if (premisegroup_con):
					if (not is_inserted):
						new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=False, author=db_user.uid, weight=0, conclusion=0, issue=issue)
						new_argument.conclusions_argument(db_argument_of_current_attack.uid)
						argument_list.append(new_argument)
						is_inserted = True
				else:
					new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=False, author=db_user.uid, weight=0, conclusion=0, issue=issue)
					new_argument.conclusions_argument(db_argument_of_current_attack.uid)
					argument_list.append(new_argument)
				key = 'con_' + current_attack + '_premisegroup_' + str(new_premisegroup_uid) + '_index_' + str(index)
				return_dict[key] = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)
				return_dict[key]['duplicate'] = str(is_duplicate)
			return_dict['duplicates'] = qh.add_arguments(transaction, argument_list)

		###########
		# OVERBID #
		###########
		elif current_attack == 'overbid':
			return_dict['same_group'] = '1' if premisegroup_pro else '0'
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch overbid')
			argument_list = []
			# for every statement in current dictionary
			for index, pro in enumerate(pro_dict):
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch overbid: ' + pro_dict[pro] + ', with same pgroup: ' + str(premisegroup_pro))
				new_statement, is_duplicate = self.set_statement(transaction, pro_dict[pro], user, False, issue)
				if premisegroup_pro:
					# Todo handle duplicats in pgroups
					if new_premisegroup_uid is None:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch overbid: new pgroup, but this one will be for all')
						new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
					else:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch overbid: old pgroup')
						qh.set_statement_as_premise(new_statement, user, new_premisegroup_uid, issue)
				else:
					logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch overbid: every round, new pgroup')
					new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch overbid: new_premisegroup_uid is ' + str(new_premisegroup_uid))
				# now, every new statement will be inserted, because groups will be added once only
				if (premisegroup_pro):
					if (not is_inserted):
						new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=True, author=db_user.uid, weight=0, conclusion=0, issue=issue)
						new_argument.conclusions_argument(db_argument_of_current_attack.uid)
						argument_list.append(new_argument)
						is_inserted = True
				else:
					new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=True, author=db_user.uid, weight=0, conclusion=0, issue=issue)
					new_argument.conclusions_argument(db_argument_of_current_attack.uid)
					argument_list.append(new_argument)
				key = 'pro_' + current_attack + '_premisegroup_' + str(new_premisegroup_uid) + '_index_' + str(index)
				return_dict[key] = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)
				return_dict[key]['duplicate'] = str(is_duplicate)
			return_dict['duplicates'] = qh.add_arguments(transaction, argument_list)

		#########
		# REBUT #
		#########
		elif current_attack == 'rebut':
			return_dict['same_group'] = '1' if premisegroup_pro else '0'
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut')
			# getting premise of users argument
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid==argument_id,
			                                                              Argument.issue_uid==issue)).first()
			db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==db_argument.premisesGroup_uid,
			                                                             Premise.issue_uid==issue)).all()
			db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==db_argument.conclusion_uid,
			                                                                 Statement.issue_uid==issue)).first()
			argument_list = []
			# for every statement in current dictionary
			used_dict = con_dict if exception_rebut else pro_dict
			supportive = False if exception_rebut else True
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut: using ' + ('con' if exception_rebut else 'pro') + '_dict because ' + str(exception_rebut))

			for index, pro in enumerate(used_dict):
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut: ' + used_dict[pro] + ', with same pgroup: ' + str(premisegroup_pro))
				# every entry of the dict will be a new statement with a new premisegroup
				new_statement, is_duplicate = self.set_statement(transaction, used_dict[pro], user, False, issue)
				if premisegroup_pro:
					# Todo handle duplicats in pgroups
					if new_premisegroup_uid is None:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut: new pgroup, but this one will be for all')
						new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
					else:
						logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut: old pgroup')
						qh.set_statement_as_premise(new_statement, user, new_premisegroup_uid, issue)
				else:
					logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut: every round, new pgroup')
					new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
				logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch rebut: new_premisegroup_uid is ' + str(new_premisegroup_uid))
				# now, every new statement will ...
				###
				###
				#for premise in db_premises:
				# now, every new statement will be inserted, because groups will be added once only
				if (premisegroup_pro):
					if (not is_inserted):
						new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=supportive, author=db_user.uid, weight=0, conclusion=db_conclusion.uid, issue=issue)
							# differentiate between the attacks
						if last_attack == 'undermine':
							new_argument.conclusion = db_conclusion.uid
						elif last_attack == 'undercut':
							new_argument.conclusion = 0
							new_argument.conclusions_argument(argument_id)
						elif last_attack == 'rebut':
							new_argument.conclusion = db_argument.conclusion_uid

						argument_list.append(new_argument)
						is_inserted = True
				else:
					new_argument = Argument(premisegroup=new_premisegroup_uid, issupportive=supportive, author=db_user.uid, weight=0, conclusion=db_conclusion.uid, issue=issue)
					# if last_attack == 'undermine':
					# elif last_attack == 'undercut':
					# elif last_attack == 'rebut':
					argument_list.append(new_argument)
				###
				###
				key = 'pro_' + current_attack + '_premisegroup_' + str(new_premisegroup_uid) + '_index_' + str(index)
				return_dict[key] = DictionaryHelper().save_statement_row_in_dictionary(new_statement, issue)
				return_dict[key]['duplicate'] = str(is_duplicate)
			return_dict['duplicates'] = qh.add_arguments(transaction, argument_list)

		else:
			logger('DatabaseHelper', 'handle_inserting_new_statements', 'branch error')
			return_dict['status'] = '-1'
			return return_dict


		return return_dict

	def get_dump(self, issue):
		"""

		:param issue: current issue
		:return: dictionary labeled with enumerated integeres, whereby these dicts are named by their table
		"""
		ret_dict = dict()

		# getting all users
		db_users = DBDiscussionSession.query(User).all()
		user_dict = dict()
		for index, user in enumerate(db_users):
			tmp_dict = dict()
			tmp_dict['uid'] = user.uid
			tmp_dict['nickname'] = user.nickname
			user_dict[str(index)] = tmp_dict
		ret_dict['user'] = user_dict

		# getting all statements
		db_statements = DBDiscussionSession.query(Statement).all()
		statement_dict = dict()
		for index, statement in enumerate(db_statements):
			tmp_dict = dict()
			tmp_dict['uid'] = statement.uid
			tmp_dict['textversion_uid'] = statement.textversion_uid
			tmp_dict['isStartpoint'] = statement.isStartpoint
			tmp_dict['weight_uid'] = statement.weight_uid
			statement_dict[str(index)] = tmp_dict
		ret_dict['statement'] = statement_dict

		# getting all textversions
		db_textversions = DBDiscussionSession.query(TextVersion).all()
		textversion_dict = dict()
		for index, textversion in enumerate(db_textversions):
			tmp_dict = dict()
			tmp_dict['uid'] = textversion.uid
			tmp_dict['statement_uid'] = textversion.statement_uid
			tmp_dict['content'] = textversion.content
			tmp_dict['author_uid'] = textversion.author_uid
			tmp_dict['timestamp'] = textversion.timestamp
			textversion_dict[str(index)] = tmp_dict
		ret_dict['textversion'] = textversion_dict

		# getting all premisegroups
		db_premisegroups = DBDiscussionSession.query(PremiseGroup).all()
		premisegroup_dict = dict()
		for index, premisegroup in enumerate(db_premisegroups):
			tmp_dict = dict()
			tmp_dict['uid'] = premisegroup.uid
			tmp_dict['author_uid'] = premise.author_uid
			premisegroup_dict[str(index)] = tmp_dict
		ret_dict['premisegroup'] = premisegroup_dict

		# getting all premises
		db_premises = DBDiscussionSession.query(Premise).all()
		premise_dict = dict()
		for index, premise in enumerate(db_premises):
			tmp_dict = dict()
			tmp_dict['premisesGroup_uid'] = premise.premisesGroup_uid
			tmp_dict['statement_uid'] = premise.statement_uid
			tmp_dict['isNegated'] = premise.isNegated
			tmp_dict['author_uid'] = premise.author_uid
			tmp_dict['timestamp'] = premise.timestamp
			premise_dict[str(index)] = tmp_dict
		ret_dict['premise'] = premise_dict

		# getting all arguments
		db_arguments = DBDiscussionSession.query(Argument).all()
		argument_dict = dict()
		for index, argument in enumerate(db_arguments):
			tmp_dict = dict()
			tmp_dict['uid'] = argument.uid
			tmp_dict['premisesGroup_uid'] = argument.premisesGroup_uid
			tmp_dict['conclusion_uid'] = argument.conclusion_uid
			tmp_dict['argument_uid'] = argument.argument_uid
			tmp_dict['isSupportive'] = argument.isSupportive
			tmp_dict['author_uid'] = argument.author_uid
			tmp_dict['timestamp'] = argument.timestamp
			tmp_dict['weight_uid'] = argument.weight_uid
			argument_dict[str(index)] = tmp_dict
		ret_dict['argument'] = argument_dict

		# getting all weights
		db_weights = DBDiscussionSession.query(Weight).all()
		weight_dict = dict()
		for index, weight in enumerate(db_weights):
			tmp_dict = dict()
			tmp_dict['uid'] = weight.uid
			weight_dict[str(index)] = tmp_dict
		ret_dict['weight'] = weight_dict

		# getting all votes
		db_votes = DBDiscussionSession.query(Vote).all()
		vote_dict = dict()
		for index, vote in enumerate(db_votes):
			tmp_dict = dict()
			tmp_dict['weight_uid'] = vote.weight_uid
			tmp_dict['author_uid'] = vote.author_uid
			vote_dict[str(index)] = tmp_dict
		ret_dict['vote'] = vote_dict

		return ret_dict


