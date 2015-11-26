import random
import collections

from sqlalchemy import and_
from Levenshtein import distance
from datetime import datetime

from .database import DBDiscussionSession, DBNewsSession
from .database.discussion_model import Argument, Statement, User, Group, TextValue, TextVersion, Premise, PremiseGroup,  Track, \
	Relation, Issue
from .database.news_model import News
from .dictionary_helper import DictionaryHelper
from .query_helper import QueryHelper
from .user_management import UserHandler
from .logger import logger
from .strings import Translator
from .tracking_helper import TrackingHelper
from .user_management import PasswordHandler

# TODO: PEP 8

class DatabaseHelper(object):

	def get_news(self):
		"""

		:return:
		"""
		logger('DatabaseHelper', 'get_news', 'main')
		db_news = DBNewsSession.query(News).all()
		logger('DatabaseHelper', 'get_news', 'we have ' + str(len(db_news)) + ' news')
		ret_dict = dict()
		for index, news in enumerate(db_news):
			news_dict = {}
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
		:param title: news title
		:param text: news text
		:param user: self.request.authenticated_userid
		:return: dictionary {title,date,author,news}
		"""
		logger('DatabaseHelper', 'set_news', 'def')
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		author = db_user.firstname if db_user.firstname == "admin" else db_user.firstname + " " + db_user.surname
		now = datetime.datetime.now()
		day = str(now.day) if now.day > 9 else ("0" + str(now.day))
		month = str(now.month) if now.month > 9 else ("0" + str(now.month))
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

	def correct_statement(self, transaction, user, uid, corrected_text, is_final, issue):
		"""
		Corrects a statement
		:param transaction: current transaction
		:param user: requesting user
		:param uid: requested statement uid
		:param corrected_text: new text
		:param is_final:
		:param issue:
		:return: True
		"""
		logger('DatabaseHelper', 'correct_statement', 'def')
		is_final = is_final == 'true'

		return_dict = dict()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==uid, Statement.issue_uid==issue)).join(TextValue).first()
		db_textvalue = DBDiscussionSession.query(TextValue).filter_by(uid=db_statement.text_uid).join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()

		# duplicate check
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).all()
		if len(db_textversions)>0 and (not is_final):
			logger('DatabaseHelper', 'correct_statement', 'duplicate')
			return_dict['status'] = '0'
			return return_dict

		if db_user:
			logger('DatabaseHelper', 'correct_statement', 'given user exists and correction will be set')
			# duplicate or not?
			if (len(db_textversions)>0):
				textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=db_textversions[-1].uid)
			else:
				textversion = TextVersion(content=corrected_text, author=db_user.uid, weight=db_textvalue.textversions.weight)
				textversion.set_textvalue(db_textvalue.uid)
				DBDiscussionSession.add(textversion)
				DBDiscussionSession.flush()

			db_textvalue.update_textversion(textversion.uid)
			transaction.commit()
			return_dict['status'] = '1'
		else:
			logger('DatabaseHelper', 'correct_statement', 'user not found')
			return_dict['status'] = '-1'

		return_dict['uid'] = uid
		return_dict['text'] = corrected_text
		return return_dict

	def change_password(self, transaction, user, old_pw, new_pw, confirm_pw, lang):
		"""

		:param transaction: current database transaction
		:param user: current database user
		:param old_pw: old received password
		:param new_pw: new received password
		:param confirm_pw: confirmation of the password
		:param lang: current language
		:return: an message and boolean for error and success
		"""
		logger('DatabaseHelper', 'change_password', 'def')
		t = Translator(lang)

		error = False
		success = False

		# is the old password given?
		if not old_pw:
			logger('DatabaseHelper', 'change_password', 'old pwd is empty')
			message = t.get('oldPwdEmpty') # 'The old password field is empty.'
			error = True
		# is the new password given?
		elif not new_pw:
			logger('DatabaseHelper', 'change_password', 'new pwd is empty')
			message = t.get('newPwdEmtpy') # 'The new password field is empty.'
			error = True
		# is the cofnrimation password given?
		elif not confirm_pw:
			logger('DatabaseHelper', 'change_password', 'confirm pwd is empty')
			message = t.get('confPwdEmpty') # 'The password confirmation field is empty.'
			error = True
		# is new password equals the confirmation?
		elif not new_pw == confirm_pw:
			logger('DatabaseHelper', 'change_password', 'new pwds not equal')
			message = t.get('newPwdNotEqual') # 'The new passwords are not equal'
			error = True
		# is new old password equals the new one?
		elif old_pw == new_pw:
			logger('DatabaseHelper', 'change_password', 'pwds are the same')
			message = t.get('pwdsSame') # 'The new and old password are the same'
			error = True
		else:
			# is the old password valid?
			if not user.validate_password(old_pw):
				logger('DatabaseHelper', 'change_password', 'old password is wrong')
				logger('DatabaseHelper', 'old', old_pw + " " + PasswordHandler().get_hashed_password(old_pw))
				logger('DatabaseHelper', 'new', new_pw + " " + PasswordHandler().get_hashed_password(new_pw))
				logger('DatabaseHelper', 'current', user.password)
				message = t.get('oldPwdWrong') # 'Your old password is wrong.'
				error = True
			else:
				logger('DatabaseHelper', 'form.passwordrequest.submitted', 'new password is ' + new_pw)
				password_handler = PasswordHandler()
				hashed_pw = password_handler.get_hashed_password(new_pw)
				logger('DatabaseHelper', 'form.passwordrequest.submitted', 'New hashed password is ' + hashed_pw)

				# set the hased one
				user.password = hashed_pw
				DBDiscussionSession.add(user)
				transaction.commit()

				logger('DatabaseHelper', 'change_password', 'password was changed')
				message = t.get('pwdChanged') # 'Your password was changed'
				success = True

		return message, error, success

	def get_all_users(self, user):
		"""
		Returns all users, if the given user is admin
		:param user: self.request.authenticated_userid
		:return: dictionary
		"""
		is_admin = UserHandler().is_user_admin(user)
		logger('DatabaseHelper', 'get_all_users', 'is_admin ' + str(is_admin))
		if not is_admin:
			return_dict = dict()
		else:
			logger('DatabaseHelper', 'get_all_users', 'get all users')
			db_users = DBDiscussionSession.query(User).join(Group).all()
			logger('DatabaseHelper', 'get_all_users', 'get all groups')

			return_dict = dict()

			if db_users:
				logger('DatabaseHelper', 'get_all_users', 'iterate all users')
				for user in db_users:
					return_user = dict()
					return_user['uid'] = user.uid
					return_user['firstname'] = user.firstname
					return_user['surname'] = user.surname
					return_user['nickname'] = user.nickname
					return_user['email'] = user.email
					return_user['group_uid'] = user.groups.name
					return_user['last_login'] = str(user.last_login)
					return_user['last_action'] = str(user.last_action)
					return_user['registered'] = str(user.registered)
					return_user['gender'] = str(user.gender)
					logger('DatabaseHelper', 'get_all_users ' + str(user.uid) + ' of ' + str(len(db_users)),
						"uid: " + str(user.uid)
						+ ", firstname: " + user.firstname
						+ ", surname: " + user.surname
						+ ", nickname: " + user.nickname
						+ ", email: " + user.email
						+ ", group_uid: " + user.groups.name
						+ ", last_action: " + str(user.last_action)
						+ ", last_logged: " + str(user.last_login)
						+ ", registered: " + str(user.registered)
						+ ", gender: " + str(user.gender)
					)
					return_dict[user.uid] = return_user
		return return_dict

	def get_issue_list(self, lang):
		"""

		:param lang:
		:return:
		"""
		logger('DatabaseHelper', 'get_issue_list', 'main')
		db_issues = DBDiscussionSession.query(Issue).all()
		return_dict = dict()
		for issue in db_issues:
			logger('DatabaseHelper', 'get_issue_list', 'issue no ' + str(issue.uid) + ': ' + issue.text)
			return_dict[str(issue.uid)] = {'uid': str(issue.uid), 'text': issue.text, 'date': QueryHelper().sql_timestamp_pretty_print(
				str(issue.date), lang)}

		if not db_issues:
			logger('DatabaseHelper', 'get_issue_list', 'no issues')

		return_dict = collections.OrderedDict(sorted(return_dict.items()))
		return return_dict

	def get_attack_overview(self, user, issue, lang):
		"""

		"""
		is_admin = UserHandler().is_user_admin(user)
		logger('DatabaseHelper', 'get_attack_overview', 'is_admin ' + str(is_admin) + ', issue ' + str(issue))
		if not is_admin:
			return_dict = dict()
		else:
			return_dict = {}
			logger('DatabaseHelper', 'get_attack_overview', 'get all attacks for each argument')
			db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()
			db_relations = DBDiscussionSession.query(Relation).all()

			relations_dict = {}
			for relation in db_relations:
				relations_dict[str(relation.uid)] = relation.name
			return_dict['attacks'] = relations_dict

			for argument in db_arguments:
				logger('DatabaseHelper', 'get_attack_overview', 'argument with uid ' + str(argument.uid) + ', issue ' + str(issue))
				text = QueryHelper().get_text_for_argument_uid(argument.uid, issue, lang)
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
		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.isStartpoint==True, Statement.issue_uid==issue)).all()
		logger('DatabaseHelper', 'get_start_statements', 'get all statements for issue ' + str(issue))
		if db_statements:
			return_dict['status'] = '1'
			logger('DatabaseHelper', 'get_start_statements', 'there are start statements')
			for statement in db_statements:
				logger('DatabaseHelper', 'get_start_statements', 'statement ' + str(statement.uid) + ': ' + statement.textvalues.textversions.content)
				statements_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement, issue)
		else:
			logger('DatabaseHelper', 'get_start_statements', 'there are no statements')
			return_dict['status'] = '0'

		return_dict['statements'] = statements_dict
		return return_dict

	def get_text_for_statement(self, transaction, statement_uid, user, issue):
		"""

		:param transaction:
		:param statement_uid:
		:param user:
		:param issue:
		:return:
		"""

		logger('DatabaseHelper', 'get_text_for_statement', 'get all premises: conclusion_uid: ' + str(statement_uid) + ', issue_uid: ' + str(issue))

		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid,Statement.issue_uid==issue)).first()
		return_dict = DictionaryHelper().save_statement_row_in_dictionary(db_statement, issue)

		return return_dict

	def get_premises_for_statement(self, transaction, statement_uid, isSupportive, user, session_id, issue):
		"""
		Rerturns all premises for the given statement
		:param transaction: current transaction
		:param statement_uid: uid of the statement
		:param isSupportive: boolean
		:param user: self.request.authenticated_userid
		:param session_id: self.request.session.id
		:param issue: current issue
		:return: dictionary
		"""

		TrackingHelper().save_track_for_user(transaction, user, statement_uid, 0, 0, 0, 0, session_id)

		return_dict = dict()
		premises_dict = dict()
		logger('DatabaseHelper', 'get_premises_for_statement', 'get all premises: conclusion_uid: ' + str(isSupportive)
		       + ', isSupportive: ' + str(issue)
		       + ', issue_uid: ' + str(issue))
		db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.isSupportive==isSupportive,
																Argument.conclusion_uid==statement_uid,
		                                                        Argument.issue_uid==issue)).all()

		for argument in db_arguments:
			logger('DatabaseHelper', 'get_premises_for_statement', 'argument ' + str(argument.uid) + ' (' + str(argument.premisesGroup_uid)
			       + '), issue ' + str(issue))
			db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==argument.premisesGroup_uid, 
			                                                               Premise.issue_uid==issue)).all()

			# check out the group
			premisesgroups_dict = dict()
			for premise in db_premises:
				logger('DatabaseHelper', 'get_premises_for_statement', 'premises group ' + str(premise.premisesGroup_uid))
				db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==premise.statement_uid,
				                                                                 Statement.issue_uid==issue)).all()
				for statement in db_statements:
					logger('DatabaseHelper', 'get_premises_for_statement', 'premises group has statement ' + str(statement.uid))
					premisesgroups_dict[str(statement.uid)] = DictionaryHelper().save_statement_row_in_dictionary(statement, issue)

				logger('DatabaseHelper', 'get_premises_for_statement', 'new premises_dict entry with key ' + str(premise.premisesGroup_uid))
				premises_dict[str(premise.premisesGroup_uid)] = premisesgroups_dict

		# premises dict has for each group a new dictionary
		return_dict['premises'] = premises_dict
		return_dict['conclusion_id'] = statement_uid
		return_dict['status'] = '1'

		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid, Statement.issue_uid==issue)).first()
		return_dict['currentStatement'] = DictionaryHelper().save_statement_row_in_dictionary(db_statements, issue)

		return return_dict

	def get_premise_for_statement(self, transaction, statement_uid, isSupportive, user, session_id, issue):
		"""

		:param transaction:
		:param statement_uid:
		:param isSupportive:
		:param user:
		:param session_id:
		:param issue:
		:return:
		"""
		logger('DatabaseHelper', 'get_premise_for_statement', 'get all premisses: conclusion_uid: ' + str(statement_uid) + ', issue_uid: ' +
		       str(issue))

		return_dict = self.get_premises_for_statement(transaction, statement_uid, isSupportive, user, session_id, issue)

		# get one random premise todo fix random

		premises_dict = return_dict['premises']
		if len(premises_dict) == 0:
			logger('DatabaseHelper', 'get_premise_for_statement', 'no premisses')
			return_dict['premises'] = '0'
		else:
			logger('DatabaseHelper', 'get_premise_for_statement', 'found ' + str(len(premises_dict)) + ' premises')
			rnd_element = random.choice(list(premises_dict.keys()))
			logger('DatabaseHelper', 'get_premise_for_statement', 'rnd_element out of premise keys[' + str(list(premises_dict.keys())) + '] is ' + str(rnd_element))

			return_dict['premises'] = premises_dict[rnd_element]
			logger('DatabaseHelper', 'get_premise_for_statement', 'return random premise: ' + str(return_dict['premises']))

			# current argument
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==rnd_element,
		                                                              Argument.conclusion_uid==statement_uid)).first()
			return_dict['argument_uid'] = db_argument.uid

		logger('DatabaseHelper', 'get_premise_for_statement', 'return')
		return return_dict

	def get_attack_or_support_for_premisegroup(self, transaction, user, last_premises_group_uid, last_statement_uid, session_id,
	                                           supportive, issue):
		"""
		Based on the last given premisesgroup and statement, an attack will be choosen and replied.
		:param transaction: current transaction
		:param user: current nick of the user
		:param last_premises_group_uid:
		:param last_statement_uid:
		:param session_id:
		:param supportive:
		:param issue:
		:return: A random attack (undermine, rebut undercut) based on the last saved premisesgroup and statement as well as many texts
		like the premise as text, conclusion as text, attack as text, confrontation as text. Everything is in a dict.
		"""

		logger('DatabaseHelper', 'get_attack_for_premisegroup', 'def')

		return_dict = {}
		qh = QueryHelper()
		# get premises and conclusion as text
		return_dict['premise_text'], premises_as_statements_uid = qh.get_text_for_premisesGroup_uid(last_premises_group_uid, issue)
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(last_statement_uid, issue)

		# getting the argument of the premises and conclusion
		logger('DatabaseHelper', 'get_attack_for_premisegroup', 'find argument with group ' + str(last_premises_group_uid)
				+ ' conclusion statement ' + str(last_statement_uid)
		       + ', support ' + str(supportive))

		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesGroup_uid==last_premises_group_uid,
		                                                              Argument.conclusion_uid==last_statement_uid,
		                                                              Argument.isSupportive==supportive,
		                                                              Argument.issue_uid==issue)).order_by(Argument.uid.desc()).first()

		# logging and ...
		logger('DatabaseHelper', 'get_attack_for_premisegroup', 'argument uid ' + (str(db_argument.uid) if db_argument else 'none'))
		return_dict['argument_id'] = str(db_argument.uid) if db_argument else '0'

		# getting undermines or undercuts or rebuts
		if not db_argument:
			attacks = None
			key = ''
		else:
			attacks, key = qh.get_attack_for_argument_by_random(db_argument, user, issue)
			return_dict['attack'] = key

		status = 1
		if not attacks or int(attacks[key]) == 0:
			logger('DatabaseHelper', 'get_attack_for_premisegroup', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key])))
			logger('DatabaseHelper', 'get_attack_for_premisegroup', 'attack with ' + attacks[key + str(attack_no)])
			logger('DatabaseHelper', 'get_attack_for_premisegroup', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_uid'] = attacks[key + str(attack_no) + 'id']
			return_dict['confrontation_argument_id'] = attacks[key + str(attack_no) + '_argument_id']

			# save the attack
			TrackingHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                  qh.get_relation_uid_by_name(key), 0, session_id)

		return return_dict, status

	def get_attack_for_argument(self, transaction, user, id_text, pgroup_id, session_id, issue):
		"""

		:param transaction:
		:param user:
		:param id_text:
		:param pgroup_id:
		:param session_id:
		:param issue:
		:return:
		"""

		logger('DatabaseHelper', 'get_attack_for_argument', 'main')

		qh = QueryHelper()
		splitted_id = id_text.split('_')
		relation = splitted_id[0]
		premisesgroup_uid = splitted_id[2]
		no_attacked_argument = False

		logger('DatabaseHelper', 'get_attack_for_argument', 'relation: ' + relation
		       + ', premisesgroup_uid: ' + premisesgroup_uid
		       + ', issue: ' + issue)

		# get latest conclusion
		logger('DatabaseHelper', 'get_attack_for_argument', 'get last conclusion: ' + str(pgroup_id) + ', issue: ' + str(issue))
		db_last_conclusion = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==pgroup_id,
		                                                                     Premise.issue_uid==issue)).first()

		# get the non supportive argument
		logger('DatabaseHelper', 'get_attack_for_argument', 'get the non supportive argument: conclusion_uid=' +
		       str(db_last_conclusion.statement_uid) + ', premisesGroup_uid=' + premisesgroup_uid + ', isSupportive==False')
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==db_last_conclusion.statement_uid,
		                                                    Argument.premisesGroup_uid==int(premisesgroup_uid),
		                                                    Argument.isSupportive==False,
		                                                    Argument.issue_uid==issue)).first()

		# maybe there is no argument, whoch is not-supportive
		if not db_argument:
			logger('DatabaseHelper', 'get_attack_for_argument', 'no suitable non supportive argument')
			logger('DatabaseHelper', 'get_attack_for_argument', 'new try: conclusion_uid: ' +  str(db_last_conclusion.statement_uid)
			       + ', premisesGroup_uid: ' +  str(premisesgroup_uid) + ', issue_uid: ' +  str(issue))
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid==db_last_conclusion.statement_uid,
		                                                    Argument.premisesGroup_uid==int(premisesgroup_uid),
		                                                    Argument.issue_uid==issue)).first()
			no_attacked_argument = True


		return_dict = {}
		return_dict['premise_text'], trash = qh.get_text_for_premisesGroup_uid(int(premisesgroup_uid), issue)
		return_dict['premisesgroup_uid'] = premisesgroup_uid
		return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_last_conclusion.statement_uid, issue)
		return_dict['conclusion_uid'] = db_last_conclusion.statement_uid
		return_dict['relation'] = relation

		# if there as no non-supportive argument, let's get back
		if no_attacked_argument:
			logger('DatabaseHelper', 'get_attack_for_argument', 'no_attacked_argument, so return')
			return return_dict, 0
		else:
			return_dict['argument_uid'] = db_argument.uid


		# getting undermines or undercuts or rebuts
		attacks, key = qh.get_attack_for_argument_by_random(db_argument, user, issue)
		return_dict['attack'] = key

		status = 1
		if not attacks or int(attacks[key]) == 0:
			logger('DatabaseHelper', 'get_attack_for_argument', 'there is no attack!')
			status = 0
		else:
			attack_no = str(random.randrange(0, int(attacks[key]))) # Todo fix random
			logger('DatabaseHelper', 'get_attack_for_argument', 'attack with ' + attacks[key + str(attack_no)])
			logger('DatabaseHelper', 'get_attack_for_argument', 'attack with pgroup ' + str(attacks[key + str(attack_no) + 'id']))
			return_dict['confrontation'] = attacks[key + str(attack_no)]
			return_dict['confrontation_id'] = attacks[key + str(attack_no) + 'id']
			return_dict['confrontation_argument_id'] = attacks[key + str(attack_no) + '_argument_id']

			# save the attack
			TrackingHelper().save_track_for_user(transaction, user, 0, attacks[key + str(attack_no) + 'id'], db_argument.uid,
			                                  qh.get_relation_uid_by_name(key), 0, session_id)

		return return_dict, status

	def get_reply_confrontations_response(self, transaction, uid_text, user, session_id, exception_rebut, issue, lang):
		"""

		:param transaction:
		:param uid_text:
		:param user:
		:param session_id:
		:param exception_rebut:
		:param issue:
		:param lang:
		:return:
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
			identifier = 'premisesgroup'
		elif 'support' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'support')
			return_dict = qh.get_supports_for_argument_uid(key, argument_uid, issue)
			identifier = 'premisesgroup'
		elif 'undercut' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'undercut')
			return_dict = qh.get_undercuts_for_argument_uid(key, argument_uid, issue)
			identifier = 'statement'
		elif 'overbid' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'overbid')
			return_dict = qh.get_overbids_for_argument_uid(key, argument_uid, issue)
			identifier = 'statement'
		elif 'rebut' in relation.lower():
			logger('DatabaseHelper', 'get_reply_confrontations_response', 'rebut')
			#return_dict = qh.get_rebuts_for_argument_uid(key, argument_uid)
			if exception_rebut:
				return_dict = qh.get_rebuts_for_argument_uid(key, argument_uid, issue)
			else:
				return_dict = qh.get_supports_for_argument_uid(key, argument_uid, issue)
			identifier = 'premisesgroup'
		else:
			return_dict = {}
			identifier = 'none'
			status = '-1'

		logger('DatabaseHelper', 'get_reply_confrontations_response', 'attack (' + relation + ') was fetched for ' + str(argument_uid))

		# check return value
		if not return_dict:
			return_dict = {}
		if len(return_dict) == 0:
			return_dict[key] = '0'

		return_dict['premisegroup'], uids = qh.get_text_for_premisesGroup_uid(db_argument.premisesGroup_uid, issue)
		# Todo: what is with an conclusion as premise group?
		return_dict['relation'] = splitted_id[0]
		return_dict['argument_uid'] = argument_uid
		return_dict['premisegroup_uid'] = db_argument.premisesGroup_uid
		return_dict['type'] = identifier

		if db_argument.conclusion_uid is None or db_argument.conclusion_uid == 0:
			return_dict['conclusion_text'] = qh.get_text_for_argument_uid(db_argument.argument_uid, issue, lang)
			logger('DatabaseHelper', 'get_reply_confrontations_response', return_dict['conclusion_text'])
		else:
			return_dict['conclusion_text'] = qh.get_text_for_statement_uid(db_argument.conclusion_uid, issue)
			logger('DatabaseHelper', 'get_reply_confrontations_response', return_dict['conclusion_text'])

		TrackingHelper().save_track_for_user(transaction, user, 0, 0, argument_uid, 0, qh.get_relation_uid_by_name(relation.lower()), session_id)

		return return_dict, status

	def get_logfile_for_statement(self, uid, issue):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:param issue:
		:return: dictionary with the logfile-rows
		"""
		logger('DatabaseHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==uid, Statement.issue_uid==issue)).first()
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(textValue_uid=db_statement.text_uid).join(User).all()

		return_dict = {}
		content_dict = {}
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
			statement += "."
		if statement.lower().startswith('because '):
			statement = statement[8:]

		# check, if the statement already exists
		logger('DatabaseHelper', 'set_statement', 'check for duplicate with: ' + statement)
		db_duplicate = DBDiscussionSession.query(TextVersion).filter_by(content=statement).first()
		if db_duplicate:
			db_textvalue = DBDiscussionSession.query(TextValue).filter_by(textVersion_uid=db_duplicate.uid).first()
			db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.text_uid==db_textvalue.uid,
			                                                                Statement.issue_uid==issue)).first()
			logger('DatabaseHelper', 'set_statement', 'duplicate, returning old statement with uid ' + str(db_statement.uid))
			return db_statement, True

		# add the version
		textversion = TextVersion(content=statement, author=db_user.uid, weight=0)
		DBDiscussionSession.add(textversion)
		DBDiscussionSession.flush()

		# add a new cache
		textvalue = TextValue(textversion=textversion.uid)
		DBDiscussionSession.add(textvalue)
		DBDiscussionSession.flush()
		textversion.set_textvalue(textvalue.uid)

		# add the statement
		statement = Statement(text=textvalue.uid, isstartpoint=is_start, issue=issue)
		DBDiscussionSession.add(statement)
		DBDiscussionSession.flush()

		# get the new statement
		new_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.text_uid==textvalue.uid,
		                                                                 Statement.issue_uid==issue)).order_by(Statement.uid.desc()).first()

		transaction.commit()

		logger('DatabaseHelper', 'set_statement', 'returning new statement with uid ' + str(new_statement.uid))
		return new_statement, False

	def set_argument(self, transaction, text, user_id, is_supportive, related_to_arg_uid, issue):
		"""

		:param transaction:
		:param text:
		:param user_id:
		:param is_supportive:
		:param related_to_arg_uid:
		:param issue:
		:return:
		"""
		new_statement, is_duplicate = self.set_statement(transaction, text, user_id, False, issue)

		new_premisegroup = PremiseGroup(author=user_id)
		DBDiscussionSession.add(new_premisegroup)
		DBDiscussionSession.flush()

		new_premise = Premise(premisesgroup=new_premisegroup.uid, statement=new_premisegroup.uid, isnegated=False, author=user_id,
		                        issue=issue)
		DBDiscussionSession.add(new_premise)
		DBDiscussionSession.flush()

		new_argument = Argument(premisegroup=new_premisegroup.uid, issupportive=is_supportive, author=user_id, weight=0,
		                        conclusion=new_statement.uid, issue=issue)
		new_argument.conclusions_argument(related_to_arg_uid)
		DBDiscussionSession.add(new_argument)
		DBDiscussionSession.flush()

		transaction.commit()
		return new_argument

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
		return_dict = dict()
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

#	def set_premises_for_premisegroups(self, transaction, user, pdict, key, premisegroup_id, is_supportive, issue):
#		"""
#		Inserts the given dictionary with premises for an statement or an argument
#		:param transaction: current transaction for the database
#		:param user: current users nickname
#		:param pdict: dictionary with all statements
#		:param key: pro or con
#		:param premisegroup_id:
#		:param is_supportive: for the argument
#		:param issue:
#		:return: dict
#		"""
#
#		# insert the premises as statements
#		return_dict = dict()
#
#		db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.premisesGroup_uid==premisegroup_id,
#		                                                               Premise.issue_uid==issue)).all()
#
#		logger('DatabaseHelper', 'set_premises_for_premisegroups', 'main')
#		for premise in db_premises:
#			logger('DatabaseHelper', 'set_premises_for_premisegroups', 'calling set_premises_for_conclusion with ' + str(
# premise.statement_uid))
#			return_dict.update(self.set_premises_for_conclusion(transaction, user, pdict, key, premise.statement_uid, is_supportive,
#			                                                     issue))
#
#		return return_dict

	def handle_inserting_new_statements(self, user, pro_dict, con_dict, transaction, argument_id, premisegroup_id,
	                                    current_attack, last_attack, premisegroup_con, premisegroup_pro, exception_rebut, issue):
		"""

		:param user:
		:param pro_dict:
		:param con_dict:
		:param transaction:
		:param argument_id:
		:param premisegroup_id:
		:param current_attack:
		:param last_attack:
		:param premisegroup_con:
		:param premisegroup_pro:
		:param exception_rebut:
		:param issue:
		:return:
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

	def get_fuzzy_string_for_start(self, value, issue, isStatement):
		"""
		Levenshtein FTW
		:param value:
		:param issue:
		:param isStatement:
		:return:
		"""
		logger('DatabaseHelper', 'get_fuzzy_string_for_start', 'string: ' + value + ', isStatement: ' + str(isStatement))
		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.isStartpoint==isStatement, Statement.issue_uid==issue)).join(TextValue).all()
		tmp_dict = dict()
		for index, statement in enumerate(db_statements):
			db_textvalue = DBDiscussionSession.query(TextValue).filter_by(uid=statement.text_uid).join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()
			# logger('DatabaseHelper', 'get_fuzzy_string_for_start', 'current db_textvalue ' + db_textvalue.textversions.content.lower())
			if value.lower() in db_textvalue.textversions.content.lower():
				lev = distance(value.lower(), db_textvalue.textversions.content.lower())
				logger('DatabaseHelper', 'get_fuzzy_string_for_start', 'lev: ' + str(lev) + ', value: ' + value.lower() + ' in: ' +  db_textvalue.textversions.content)
				if lev < 10:		lev = '0000' + str(lev)
				elif lev < 100:		lev = '000' + str(lev)
				elif lev < 1000:	lev = '00' + str(lev)
				elif lev < 10000:	lev = '0' + str(lev)
				tmp_dict[str(lev) + '_' + str(index)] = db_textvalue.textversions.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:10]: # TODO RETURN COUNT
			return_dict[i] = tmp_dict[i]

		logger('DatabaseHelper', 'get_fuzzy_string_for_start', 'dictionary length: ' + str(len(return_dict.keys())))

		return return_dict

	def get_fuzzy_string_for_edits(self, value, statement_uid, issue):
		"""
		Levenshtein FTW
		:param value:
		:param issue:
		:return:
		"""
		logger('DatabaseHelper', 'get_fuzzy_string_for_edits', 'string: ' + value + ', statement uid: ' + str(statement_uid))

		db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid==statement_uid, Statement.issue_uid==issue)).first()
		db_textversions = DBDiscussionSession.query(TextVersion).filter_by(textValue_uid=db_statement.text_uid).join(User).all()

		tmp_dict = dict()
		for index, textversion in enumerate(db_textversions):
			if value.lower() in textversion.content.lower():
				lev = distance(value.lower(), textversion.content.lower())
				logger('DatabaseHelper', 'get_fuzzy_string_for_edits', 'lev: ' + str(lev) + ', value: ' + value.lower() + ' in: ' + textversion.content.lower())
				if lev < 10:
					lev = '0000' + str(lev)
				elif lev < 100:
					lev = '000' + str(lev)
				elif lev < 1000:
					lev = '00' + str(lev)
				elif lev < 10000:
					lev = '0' + str(lev)
				tmp_dict[str(lev) + '_' + str(index)] = textversion.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:10]: # TODO RETURN COUNT
			return_dict[i] = tmp_dict[i]

		logger('DatabaseHelper', 'get_fuzzy_string_for_edits', 'dictionary length: ' + str(len(return_dict.keys())))

		return return_dict

	def get_fuzzy_string_for_reasons(self, value, issue):
		"""

		:param value:
		:param issue:
		:return:
		"""
		logger('DatabaseHelper', 'get_fuzzy_string_for_reasons', 'string: ' + value + ', issue: ' + str(issue))
		db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).join(TextValue).all()
		tmp_dict = dict()

		for index, statement in enumerate(db_statements):
			db_textvalue = DBDiscussionSession.query(TextValue).filter_by(uid=statement.text_uid).join(TextVersion, TextVersion.uid==TextValue.textVersion_uid).first()
			if value.lower() in db_textvalue.textversions.content.lower():
				lev = distance(value.lower(), db_textvalue.textversions.content.lower())
				logger('DatabaseHelper', 'get_fuzzy_string_for_start', 'lev: ' + str(lev) + ', value: ' + value.lower() + ' in: ' +  db_textvalue.textversions.content)
				if lev < 10:		lev = '0000' + str(lev)
				elif lev < 100:		lev = '000' + str(lev)
				elif lev < 1000:	lev = '00' + str(lev)
				elif lev < 10000:	lev = '0' + str(lev)
				tmp_dict[str(lev) + '_' + str(index)] = db_textvalue.textversions.content

		tmp_dict = collections.OrderedDict(sorted(tmp_dict.items()))

		return_dict = collections.OrderedDict()
		for i in list(tmp_dict.keys())[0:10]: # TODO RETURN COUNT
			return_dict[i] = tmp_dict[i]

		logger('DatabaseHelper', 'get_fuzzy_string_for_reasons', 'dictionary length: ' + str(len(return_dict.keys())))

		return return_dict
