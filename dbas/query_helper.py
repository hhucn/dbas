import datetime
import locale
import collections
import random
from sqlalchemy import and_, func
from slugify import slugify

from .database import DBDiscussionSession, DBNewsSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, History, VoteArgument, VoteStatement, Issue, Group
from .database.news_model import News
from .logger import logger
from .notification_helper import NotificationHelper
from .strings import Translator, TextGenerator
from .user_management import UserHandler
from .url_manager import UrlManager

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

class QueryHelper(object):
	"""

	"""

	def __init__(self):
		self.__statement_min_length = 5
		#  TODO move lang here and init translator

	# ########################################
	# ARGUMENTS
	# ########################################
	def get_text_for_argument_uid(self, uid, lang, with_strong_html_tag = False, start_with_intro=False):
		"""
		Returns current argument as string like conclusion, because premise1 and premise2
		:param uid: int
		:param lang: str
		:param with_strong_html_tag: Boolean
		:param start_with_intro: Boolean
		:return: str
		"""
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		# catch error
		if not db_argument:
			return None

		_t = Translator(lang)
		sb = '<strong>' if with_strong_html_tag else ''
		se = '</strong>' if with_strong_html_tag else ''
		because = ' ' + se + _t.get(_t.because).lower() + ' ' + sb
		doesnt_hold_because = ' ' + se + _t.get(_t.doesNotHoldBecause).lower() + ' ' + sb

		# getting all argument id
		arg_array = [db_argument.uid]
		while db_argument.argument_uid != 0:
			db_argument = DBDiscussionSession.query(Argument).filter_by(uid=db_argument.argument_uid).first()
			arg_array.append(db_argument.uid)

		if len(arg_array) == 1:
			# build one and only argument
			db_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_array[0]).first()
			premises, uids = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid)
			conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
			ret_value = (se + _t.get(_t.soYourOpinionIsThat) + ': ' + sb) if start_with_intro else ''
			ret_value += conclusion + (because if db_argument.is_supportive else doesnt_hold_because) + premises

			return ret_value

		else:
			# get all pgroups and at last, the conclusion
			pgroups = []
			supportive = []
			arg_array = arg_array[::-1]
			for uid in arg_array:
				db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
				text, tmp = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
				pgroups.append(text[0:1].lower() + text[1:])
				supportive.append(db_argument.is_supportive)
			conclusion = self.get_text_for_statement_uid(DBDiscussionSession.query(Argument).filter_by(uid=arg_array[0]).first().conclusion_uid)

			if len(arg_array) % 2 is 0: # system starts
				ret_value = se + _t.get(_t.otherUsersSaidThat) + sb + ' '
				users_opinion = True # user after system
				conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
			else: # user starts
				ret_value = (se + _t.get(_t.sentencesOpenersForArguments[0]) + ': ' + sb) if start_with_intro else ''
				users_opinion = False # system after user
				conclusion = conclusion[0:1].upper() + conclusion[1:]  # pretty print

			ret_value += conclusion + (because if supportive[0] else doesnt_hold_because) + pgroups[0] + '.'
			for i in range(1, len(pgroups)):
				ret_value += ' ' + se + (_t.get(_t.butYouCounteredWith) if users_opinion else _t.get(_t.otherUsersHaveCounterArgument)) + sb + ' ' + pgroups[i] + '.'
				users_opinion = not users_opinion
			return ret_value[:-1] # cut off punctuation

	# DEPRECATED
	def __get_text_for_argument_uid(self, uid, lang, with_strong_html_tag = False, start_with_intro=False):
		"""
		DEPRECATED Returns current argument as string like conclusion, because premise1 and premise2
		:param uid: int
		:param lang: str
		:param with_strong_html_tag: Boolean
		:return: str
		"""
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		ret_value = ''
		_t = Translator(lang)
		because = (' </strong>' if with_strong_html_tag else ' ')\
		          + _t.get(_t.because).lower()\
		          + (' <strong>' if with_strong_html_tag else ' ')
		doesnt_hold_because = (' </strong>' if with_strong_html_tag else ' ')\
		                     + _t.get(_t.doesNotHoldBecause).lower()\
		                     + (' <strong>' if with_strong_html_tag else ' ')

		# catch error
		if not db_argument:
			return None

		# basecase
		if db_argument.argument_uid == 0:
			premises, uids = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid)
			premises = premises[:-1] if premises.endswith('.') else premises  # pretty print
			if not conclusion:
				return None
			conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
			argument = conclusion + (because if db_argument.is_supportive else doesnt_hold_because) + premises
			return argument

		# recursion
		if db_argument.conclusion_uid == 0:
			argument = self.get_text_for_argument_uid(db_argument.argument_uid, lang, with_strong_html_tag)
			premises, uids = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
			if not premises:
				return None
			if db_argument.is_supportive:
				ret_value = argument + ',' + because + premises
			else:
				ret_value = argument + doesnt_hold_because + premises
		return ret_value

	def get_undermines_for_argument_uid(self, argument_uid, lang):
		"""
		Calls __get_undermines_for_premises('reason', premises_as_statements_uid)
		:param argument_uid: uid of the specified argument
		:param lang: ui_locales
		:return: dictionary
		"""
		logger('QueryHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(argument_uid))
		db_attacked_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		db_attacked_premises = DBDiscussionSession.query(Premise).filter_by(
				premisesgroup_uid=db_attacked_argument.premisesgroup_uid).order_by(
				Premise.premisesgroup_uid.desc()).all()

		premises_as_statements_uid = set()
		for premise in db_attacked_premises:
			premises_as_statements_uid.add(premise.statement_uid)

		if len(premises_as_statements_uid) == 0:
			return None

		return self.__get_undermines_for_premises(premises_as_statements_uid, lang)

	def get_overbids_for_argument_uid(self, argument_uid, lang):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, True)
		:param argument_uid: uid of the specified argument
		:param lang:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_overbids_for_argument_uid', 'main')
		return self.__get_attack_or_support_for_justification_of_argument_uid(argument_uid, True, lang)

	def get_undercuts_for_argument_uid(self, argument_uid, lang):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, False)
		:param argument_uid:
		:param lang:

		:return:
		"""
		logger('QueryHelper', 'get_undercuts_for_argument_uid', 'main')
		return self.__get_attack_or_support_for_justification_of_argument_uid(argument_uid, False, lang)

	def get_rebuts_for_argument_uid(self, argument_uid, lang):
		"""
		Calls self.get_rebuts_for_arguments_conclusion_uid('reason', Argument.conclusion_uid)
		:param argument_uid: uid of the specified argument
		:param lang:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_rebuts_for_argument_uid', 'main')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=int(argument_uid)).first()
		if not db_argument:
			return None
		return self.get_rebuts_for_arguments_conclusion_uid(db_argument, lang)

	def get_rebuts_for_arguments_conclusion_uid(self, db_argument, lang):
		"""

		:param db_argument:
		:param lang:
		:return:
		"""
		return_array = []
		given_rebuts = set()
		index = 0
		logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'conclusion_statements_uid ' +
		       str(db_argument.conclusion_uid) + ', is_current_argument_supportive ' + str(db_argument.is_supportive) +
		       ' (searching for the opposite)')
		db_rebut = DBDiscussionSession.query(Argument).filter(Argument.is_supportive == (not db_argument.is_supportive),
                                                              Argument.conclusion_uid == db_argument.conclusion_uid).all()
		for rebut in db_rebut:
			if rebut.premisesgroup_uid not in given_rebuts:
				given_rebuts.add(rebut.premisesgroup_uid)
				tmp_dict = dict()
				tmp_dict['id'] = rebut.uid
				text, trash = self.get_text_for_premisesgroup_uid(rebut.premisesgroup_uid, lang)
				tmp_dict['text'] = text[0:1].upper() + text[1:]
				return_array.append(tmp_dict)
				index += 1

		return return_array

	def get_supports_for_argument_uid(self, argument_uid, lang):
		"""

		:param argument_uid: uid of the specified argument
		:param lang:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_supporRects_for_argument_uid', 'main')

		return_array = []
		given_supports = set()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).join(
			PremiseGroup).first()
		db_arguments_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
		index = 0

		for arguments_premises in db_arguments_premises:
			db_supports = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == arguments_premises.statement_uid,
                                                                          Argument.is_supportive == True)).join(PremiseGroup).all()
			if not db_supports:
				continue

			for support in db_supports:
				if support.premisesgroup_uid not in given_supports:
					tmp_dict = dict()
					tmp_dict['id'] = support.uid
					tmp_dict['text'], trash = self.get_text_for_premisesgroup_uid(support.premisesgroup_uid, lang)
					return_array.append(tmp_dict)
					index += 1
					given_supports.add(support.premisesgroup_uid)

		return None if len(return_array) == 0 else return_array

	def handle_insert_new_premises_for_argument(self, text, current_attack, arg_uid, issue, user, transaction):
		"""

		:param text:
		:param current_attack:
		:param arg_uid:
		:param issue:
		:param user:
		:param transaction:
		:return:
		"""
		logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'def')

		statements = self.insert_as_statements(transaction, text, user, issue)
		if statements == -1:
			return -1

		# set the new statements as premisegroup and get current user as well as current argument
		new_pgroup_uid = self.__set_statements_as_new_premisegroup(statements, user, issue)
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first()

		new_argument = None
		if current_attack == 'undermine':
			new_argument = self.__set_new_undermine_or_support(transaction, new_pgroup_uid, current_argument, current_attack, db_user, issue)

		elif current_attack == 'support':
			new_argument, duplicate = self.__set_new_support(transaction, new_pgroup_uid, current_argument, db_user, issue)

		elif current_attack == 'undercut' or current_attack == 'overbid':
			new_argument, duplicate = self.__set_new_undercut_or_overbid(transaction, new_pgroup_uid, current_argument, current_attack, db_user, issue)

		elif current_attack == 'rebut':
			new_argument, duplicate = self.__set_new_rebut(transaction, new_pgroup_uid, current_argument, db_user, issue)

		return new_argument.uid

	def __set_new_undermine_or_support(self, transaction, premisegroup_uid, current_argument, current_attack, db_user, issue):
		"""

		:param transaction:
		:param premisegroup_uid:
		:param current_argument:
		:param current_attack:
		:param db_user:
		:param issue:
		:return:
		"""
		new_arguments = []
		already_in = []
		# all premises out of current pgroup
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).all()
		for premise in db_premises:
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                          Argument.is_supportive == (current_attack == 'support'),
                                                                          Argument.conclusion_uid == premise.statement_uid,
                                                                          Argument.argument_uid == 0)).first()
			# duplicate?
			if db_argument:
				already_in.append(db_argument)
			else:
				new_argument = Argument(premisegroup=premisegroup_uid,
			                            issupportive=current_attack == 'support',
			                            author=db_user.uid,
			                            conclusion=premise.statement_uid,
			                            issue=issue)
				new_arguments.append(new_argument)

			if len(new_arguments) > 0:
				DBDiscussionSession.add_all(new_arguments)
				DBDiscussionSession.flush()
				transaction.commit()

				for argument in new_arguments:
					already_in.append(argument)

			rnd = random.randint(0, len(already_in) - 1)
			return already_in[rnd]

	def __set_new_undercut_or_overbid(self, transaction, premisegroup_uid, current_argument, current_attack, db_user, issue):
		"""

		:param transaction:
		:param premisegroup_uid:
		:param current_argument:
		:param current_attack:
		:param db_user:
		:param issue:
		:return:
		"""
		# duplicate?
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
		                                                              Argument.is_supportive == (current_attack == 'overbid'),
		                                                              Argument.conclusion_uid == 0,
		                                                              Argument.argument_uid == current_argument.uid)).first()
		if db_argument:
			return db_argument, True
		else:
			new_argument = Argument(premisegroup=premisegroup_uid,
			                        issupportive=current_attack == 'overbid',
			                        author=db_user.uid,
			                        issue=issue)
			new_argument.conclusions_argument(current_argument.uid)
			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()
			transaction.commit()
			return new_argument, False

	def __set_new_rebut(self, transaction, premisegroup_uid, current_argument, db_user, issue):
		"""

		:param transaction:
		:param premisegroup_uid:
		:param current_argument:
		:param db_user:
		:return:
		"""
		# duplicate?
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
		                                                              Argument.is_supportive == False,
		                                                              Argument.conclusion_uid == current_argument.conclusion_uid,
		                                                              Argument.argument_uid == 0)).first()
		if db_argument:
			return db_argument, True
		else:
			new_argument = Argument(premisegroup=premisegroup_uid,
			                        issupportive=False,
			                        author=db_user.uid,
			                        conclusion=current_argument.conclusion_uid,
			                        issue=issue)
			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()
			transaction.commit()
			return new_argument, False

	def __set_new_support(self, transaction, premisegroup_uid, current_argument, db_user, issue):
		"""

		:param transaction:
		:param premisegroup_uid:
		:param current_argument:
		:param db_user:
		:return:
		"""
		# duplicate?
		db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
		                                                              Argument.is_supportive == True,
		                                                              Argument.conclusion_uid == current_argument.conclusion_uid,
		                                                              Argument.argument_uid == 0)).first()
		if db_argument:
			return db_argument, True
		else:
			new_argument = Argument(premisegroup=premisegroup_uid,
			                        issupportive=True,
			                        author=db_user.uid,
			                        conclusion=current_argument.conclusion_uid,
			                        issue=issue)
			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()
			transaction.commit()
			return new_argument, False

	def __set_argument(self, transaction, user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
		"""

		:param transaction:
		:param user:
		:param premisegroup_uid:
		:param conclusion_uid:
		:param argument_uid:
		:param is_supportive:
		:param issue:
		:return:
		"""
		logger('QueryHelper', '__set_argument', 'main with user: ' + str(user) +
		       ', premisegroup_uid: ' + str(premisegroup_uid) +
		       ', conclusion_uid: ' + str(conclusion_uid) +
		       ', argument_uid: ' + str(argument_uid) +
		       ', is_supportive: ' + str(is_supportive) +
		       ', issue: ' + str(issue), debug=True)

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.issue_uid == issue)).first()
		if not new_argument:
			new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid,
			                        conclusion=conclusion_uid, issue=issue)
			new_argument.conclusions_argument(argument_uid)

			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()

			new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                           Argument.is_supportive == is_supportive,
                                                                           Argument.author_uid == db_user.uid,
                                                                           Argument.conclusion_uid == conclusion_uid,
                                                                           Argument.argument_uid == argument_uid,
                                                                           Argument.issue_uid == issue)).first()
		transaction.commit()
		if new_argument:
			return new_argument.uid
		else:
			return 0

	# ########################################
	# ISSUE
	# ########################################

	def get_title_for_issue_uid(self, uid):
		"""
		Returns the title or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
		#  logger('QueryHelper', 'get_title_for_issue_uid', str(uid))
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return db_issue.title if db_issue else 'none'

	def get_slug_for_issue_uid(self, uid):
		"""
		Returns the slug of the title or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
		#  logger('QueryHelper', 'get_slug_for_issue_uid', str(uid))
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return slugify(db_issue.title) if db_issue else 'none'

	def get_info_for_issue_uid(self, uid):
		"""
		Returns the slug or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
		#  logger('QueryHelper', 'get_info_for_issue_uid', str(uid))
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return db_issue.info if db_issue else 'none'

	def get_date_for_issue_uid(self, uid, lang):
		"""
		Returns the date or none for the issue uid
		:param uid: Issue.uid
		:param lang: ui_locales
		:return: String
		"""
		#  logger('QueryHelper', 'get_date_for_issue_uid', str(uid))
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return self.sql_timestamp_pretty_print(str(db_issue.date), lang) if db_issue else 'none'

	def prepare_json_of_issue(self, uid, application_url, lang, for_api):
		"""
		Prepares slug, info, argument count and the date of the issue as dict
		:param uid: Issue.uid
		:param application_url:
		:param lang: String
		:param for_api: boolean
		:return: dict()
		"""
		logger('QueryHelper', 'prepare_json_of_issue', 'main')
		slug = self.get_slug_for_issue_uid(uid)
		title = self.get_title_for_issue_uid(uid)
		info = self.get_info_for_issue_uid(uid)
		arg_count = self.get_number_of_arguments(uid)
		date = self.get_date_for_issue_uid(uid, lang)

		db_issues = DBDiscussionSession.query(Issue).all()
		all_array = []
		for issue in db_issues:
			issue_dict = dict()
			issue_dict['slug']              = issue.get_slug()
			issue_dict['title']             = issue.title
			issue_dict['url']               = UrlManager(application_url, issue.get_slug(), for_api).get_slug_url(False) if str(uid) != str(issue.uid) else ''
			issue_dict['info']              = issue.info
			issue_dict['arg_count']         = self.get_number_of_arguments(issue.uid)
			issue_dict['date']              = self.sql_timestamp_pretty_print(str(issue.date), lang)
			issue_dict['enabled']           = 'disabled' if str(uid) == str(issue.uid) else 'enabled'
			all_array.append(issue_dict)

		return {'slug': slug, 'info': info, 'title': title, 'uid': uid, 'arg_count': arg_count, 'date': date, 'all': all_array}

	def get_number_of_arguments(self, issue):
		"""

		:param issue:
		:return:
		"""
		return len(DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all())

	def get_issue_id(self, request):
		"""
		Returns issue uid
		:param request: self.request
		:return: uid
		"""

		# first matchdict, then params, then session, afterwards fallback
		issue = request.matchdict['issue'] if 'issue' in request.matchdict \
			else request.params['issue'] if 'issue' in request.params \
			else request.session['issue'] if 'issue' in request.session \
			else DBDiscussionSession.query(Issue).first().uid

		if str(issue) is 'undefined':
			self.issue_fallback = 1

		# save issue in session
		request.session['issue'] = issue

		return issue

	# ########################################
	# STATEMENTS
	# ########################################

	def __set_statements_as_new_premisegroup(self, statements, user, issue):
		"""

		:param statements:
		:param user:
		:param issue:
		:return:
		"""
		logger('QueryHelper', '__set_statements_as_new_premisegroup', 'user: ' + str(user) +
		       ', statement: ' + str(statements) + ', issue: ' + str(issue), debug=True)
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# check for duplicate
		all_groups = []
		for statement in statements:
			# get the premise
			db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
			if db_premise:
				# getting all groups, where the premise is member
				db_premisegroup = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_premise.premisesgroup_uid).all()
				groups = set()
				for group in db_premisegroup:
					groups.add(group.premisesgroup_uid)
				all_groups.append(groups)
		# if every set in this array has one common member, they are all in the same group
		if len(all_groups) > 0:
			intersec = set.intersection(*all_groups)
			for group in intersec:
				db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group).all()
				if len(db_premise) == len(statements):
					return group

		premise_group = PremiseGroup(author=db_user.uid)
		DBDiscussionSession.add(premise_group)
		DBDiscussionSession.flush()

		premise_list = []
		for statement in statements:
			premise = Premise(premisesgroup=premise_group.uid, statement=statement.uid, is_negated=False, author=db_user.uid, issue=issue)
			premise_list.append(premise)

		DBDiscussionSession.add_all(premise_list)
		DBDiscussionSession.flush()

		db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

		return db_premisegroup.uid

	def set_statement(self, transaction, statement, user, is_start, issue):
		"""
		Saves statement for user
		:param transaction: current transaction
		:param statement: given statement
		:param user: given user
		:param is_start: if it is a start statement
		:param issue:
		:return: Statement, is_duplicate or -1, False on error
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'set_statement', 'user: ' + str(user) + ', user_id: ' + str(db_user.uid) +
		       ', statement: ' + str(statement) + ', issue: ' + str(issue))

		# check for dot at the end
		if not statement.endswith(('.', '?', '!')):
			statement += '.'
		if statement.lower().startswith('because '):
			statement = statement[8:]

		# check, if the statement already exists
		db_duplicate = DBDiscussionSession.query(TextVersion).filter(func.lower(TextVersion.content) == func.lower(statement)).first()
		if db_duplicate:
			db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid == db_duplicate.uid,
			                                                                Statement.issue_uid == issue)).first()
			return db_statement, True

		# add the version
		textversion = TextVersion(content=statement, author=db_user.uid)
		DBDiscussionSession.add(textversion)
		DBDiscussionSession.flush()

		# add the statement
		statement = Statement(textversion=textversion.uid, is_startpoint=is_start, issue=issue)
		DBDiscussionSession.add(statement)
		DBDiscussionSession.flush()

		# get the new statement
		new_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid == textversion.uid,
		                                                                 Statement.issue_uid == issue)).order_by(Statement.uid.desc()).first()
		textversion.set_statement(new_statement.uid)

		transaction.commit()

		return new_statement, False

	def get_text_for_conclusion(self, argument, lang):
		"""

		:param argument:
		:param lang:
		:return:
		"""
		if argument.argument_uid == 0:
			return self.get_text_for_statement_uid(argument.conclusion_uid)
		else:
			return self.get_text_for_argument_uid(argument.argument_uid, lang)

	def get_text_for_statement_uid(self, uid):
		"""

		:param uid: id of a statement
		:return: text of the mapped textvalue for this statement
		"""
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
		if not db_statement:
			return None

		db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
			uid=db_statement.textversion_uid).first()
		tmp = db_textversion.content

		if tmp.endswith(('.', '?', '!')):
			tmp = tmp[:-1]

		return tmp

	# ########################################
	# OTHER - GETTER
	# ########################################

	def get_text_for_premisesgroup_uid(self, uid, lang):
		"""

		:param uid: id of a premise group
		:param lang: ui_locales
		:return: text of all premises in this group and the uids as list
		"""
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=uid).join(Statement).all()
		text = ''
		uids = []
		_t = Translator(lang)
		for premise in db_premises:
			tmp = self.get_text_for_statement_uid(premise.statements.uid)
			if tmp.endswith('.'):
				tmp = tmp[:-1]
			uids.append(str(premise.statements.uid))
			text += ' ' + _t.get(_t.aand) + ' ' + tmp[0:1].lower() + tmp[1:]

		return text[5:], uids

	def __get_undermines_for_premises(self, premises_as_statements_uid, lang):
		"""

		:param premises_as_statements_uid:
		:param lang: ui_locales
		:return:
		"""
		logger('QueryHelper', '__get_undermines_for_premises', 'main', debug=True)
		return_array = []
		index = 0
		given_undermines = set()
		for s_uid in premises_as_statements_uid:
			db_undermine = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == False, Argument.conclusion_uid == s_uid)).all()
			for undermine in db_undermine:
				if undermine.premisesgroup_uid not in given_undermines:
					given_undermines.add(undermine.premisesgroup_uid)
					tmp_dict = dict()
					tmp_dict['id'] = undermine.uid
					tmp_dict['text'], uids = self.get_text_for_premisesgroup_uid(undermine.premisesgroup_uid, lang)
					return_array.append(tmp_dict)
					index += 1
		return return_array

	def __get_attack_or_support_for_justification_of_argument_uid(self, argument_uid, is_supportive, lang):
		"""

		:param argument_uid:
		:param is_supportive:
		:param lang:
		:return:
		"""
		return_array = []
		logger('QueryHelper', '__get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid==' + str(argument_uid), debug=True)
		db_related_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
		                                                                       Argument.argument_uid == argument_uid)).all()
		given_relations = set()
		index = 0

		if not db_related_arguments:
			return None

		for relation in db_related_arguments:
			if relation.premisesgroup_uid not in given_relations:
				given_relations.add(relation.premisesgroup_uid)
				tmp_dict = dict()
				tmp_dict['id'] = relation.uid
				tmp_dict['text'], trash = self.get_text_for_premisesgroup_uid(relation.premisesgroup_uid, lang)
				return_array.append(tmp_dict)
				index += 1
		return return_array

	def get_user_with_same_opinion_for_argument(self, argument_uid, lang):  # TODO TERESA
		"""

		:param argument_uid: Statement.uid
		:param lang: ui_locales
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('QueryHelper', 'get_user_with_same_opinion', 'Argument ' + str(argument_uid))

		ret_dict = dict()
		all_users = []
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			ret_dict['users'] = all_users
			return ret_dict

		db_votes = DBDiscussionSession.query(VoteArgument).filter_by(argument_uid=db_argument.uid).all()
		uh = UserHandler()
		for vote in db_votes:
			users_dict = dict()
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict[voted_user.nickname] = {'avatar_url': uh.get_profile_picture(voted_user),
			                                   'vote_timestamp': self.sql_timestamp_pretty_print(str(vote.timestamp), lang)}
			all_users.append(users_dict)
			ret_dict['users'] = all_users
		return ret_dict

	def get_user_with_same_opinion_for_statement(self, statement_uid, lang):  # TODO TERESA
		"""

		:param statement_uid: Statement.uid
		:param lang: ui_locales
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('QueryHelper', 'get_user_with_same_opinion_for_statement', 'Statement ' + str(statement_uid))

		ret_dict = dict()
		all_users = []
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		if not db_argument:
			ret_dict['users'] = all_users
			return ret_dict

		db_votes = DBDiscussionSession.query(VoteStatement).filter_by(statement_uid=db_statement.uid).all()
		uh = UserHandler()
		for vote in db_votes:
			users_dict = dict()
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict[voted_user.nickname] = {'avatar_url': uh.get_profile_picture(voted_user),
			                                   'vote_timestamp': self.sql_timestamp_pretty_print(str(vote.timestamp), lang)}
			all_users.append(users_dict)
		ret_dict['users'] = all_users
		return ret_dict

	def get_id_of_slug(self, slug, request, save_id_in_session):
		"""
		Returns the uid
		:param slug: slug
		:param request: self.request for a fallback
		:param save_id_in_session:
		:return: uid
		"""
		db_issues = DBDiscussionSession.query(Issue).all()
		for issue in db_issues:
			if str(slugify(issue.title)) == str(slug):
				if save_id_in_session:
					request.session['issue'] = issue.uid
				return issue.uid
		return self.get_issue_id(request)

	def get_every_attack_for_island_view(self, arg_uid, lang):
		"""

		:param arg_uid:
		:param lang:
		:return:
		"""
		logger('QueryHelper', 'get_every_attack_for_island_view', 'def with arg_uid: ' + str(arg_uid))
		return_dict = {}
		_t = Translator(lang)

		undermine = self.get_undermines_for_argument_uid(arg_uid, lang)
		support = self.get_supports_for_argument_uid(arg_uid, lang)
		undercut = self.get_undercuts_for_argument_uid(arg_uid, lang)
		# overbid = self.get_overbids_for_argument_uid(arg_uid, lang)
		rebut = self.get_rebuts_for_argument_uid(arg_uid, lang)

		undermine = undermine if undermine else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		support = support if support else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		undercut = undercut if undercut else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		# overbid = overbid if overbid else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		rebut = rebut if rebut else [{'id': 0, 'text': _t.get(_t.no_entry)}]

		return_dict.update({'undermine': undermine})
		return_dict.update({'support': support})
		return_dict.update({'undercut': undercut})
		# return_dict.update({'overbid': overbid})
		return_dict.update({'rebut': rebut})

		logger('QueryHelper', 'get_every_attack_for_island_view', 'summary: ' +
		       str(len(undermine)) + ' undermines, ' +
		       str(len(support)) + ' supports, ' +
		       str(len(undercut)) + ' undercuts, ' +
		       # str(len(overbid)) + ' overbids, ' +
		       str(len(rebut)) + ' rebuts')

		return return_dict

	def get_language(self, request, current_registry):
		"""
		Returns current ui locales code which is saved in current cookie or the registry
		:param request: self.request
		:param current_registry: get_current_registry()
		:return: language abrreviation
		"""
		try:
			lang = str(request.cookies['_LOCALE_'])
		except KeyError:
			lang = current_registry.settings['pyramid.default_locale_name']
		return lang

	def get_news(self):
		"""
		Returns all news in a dicitionary, sorted by date
		:return: dict()
		"""
		logger('QueryHelper', 'get_news', 'main')
		db_news = DBNewsSession.query(News).all()
		ret_dict = dict()
		for index, news in enumerate(db_news):
			news_dict = dict()
			news_dict['title'] = news.title
			news_dict['author'] = news.author
			news_dict['date'] = news.date
			news_dict['news'] = news.news
			news_dict['uid'] = str(news.uid)
			# string date into date
			date_object = datetime.datetime.strptime(str(news.date), '%d.%m.%Y')
			# add index on the seconds for unique id's
			sec = (date_object - datetime.datetime(1970, 1, 1)).total_seconds() + index
			ret_dict[str(sec)] = news_dict

		ret_dict = collections.OrderedDict(sorted(ret_dict.items()))

		return ret_dict

	def get_dump(self, issue, lang):
		"""

		:param issue: current issue
		:param lang: current lang
		:return: dictionary labeled with enumerated integeres, whereby these dicts are named by their table
		"""
		ret_dict = dict()
		logger('QueryHelper', 'get_dump', 'main')

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
				tmp_dict['timestamp']        = self.sql_timestamp_pretty_print(str(textversion.timestamp), lang)
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
			tmp_dict['conclusion_uid']      = argument.conclusion_uid
			tmp_dict['argument_uid']        = argument.argument_uid
			tmp_dict['is_supportive']       = argument.is_supportive
			tmp_dict['author_uid']          = argument.author_uid
			tmp_dict['timestamp']           = self.sql_timestamp_pretty_print(str(argument.timestamp), lang)
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
				tmp_dict['timestamp']         = self.sql_timestamp_pretty_print(str(premise.timestamp), lang)
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

	def get_all_users(self, user, lang):
		"""

		:param user:
		:param lang:
		:return:
		"""
		is_admin = UserHandler().is_user_admin(user)
		logger('QueryHelper', 'get_all_users', 'is_admin ' + str(is_admin))
		return_dict = dict()
		if not is_admin:
			return return_dict

		db_users = DBDiscussionSession.query(User).all()
		for index, user in enumerate(db_users):
			tmp_dict = dict()
			tmp_dict['uid']         = str(user.uid)
			tmp_dict['firstname']   = str(user.firstname)
			tmp_dict['surname']     = str(user.surname)
			tmp_dict['nickname']    = str(user.nickname)
			tmp_dict['email']       = str(user.email)
			tmp_dict['gender']      = str(user.gender)
			tmp_dict['group_uid']   = DBDiscussionSession.query(Group).filter_by(uid=user.group_uid).first().name
			tmp_dict['last_action'] = self.sql_timestamp_pretty_print(str(user.last_action), lang)
			tmp_dict['last_login']  = self.sql_timestamp_pretty_print(str(user.last_login), lang)
			tmp_dict['registered']  = self.sql_timestamp_pretty_print(str(user.registered), lang)
			return_dict[str(index)] = tmp_dict

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
		logger('QueryHelper', 'get_attack_overview', 'is_admin ' + str(is_admin) + ', issue ' + str(issue))
		return_dict = dict()
		if not is_admin:
			return return_dict

		db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()

		for index, argument in enumerate(db_arguments):
			tmp_dict = dict()
			tmp_dict['uid'] = str(argument.uid)
			tmp_dict['text'] = self.get_text_for_argument_uid(argument.uid, lang)
			db_votes = DBDiscussionSession.query(VoteArgument).filter_by(argument_uid=argument.uid).all()
			db_valid_votes = DBDiscussionSession.query(Vote).filter(and_(VoteArgument.argument_uid == argument.uid,
			                                                             VoteArgument.is_valid == True)).all()
			db_valid_upvotes = DBDiscussionSession.query(Vote).filter(and_(VoteArgument.argument_uid == argument.uid,
			                                                               VoteArgument.is_valid == True,
			                                                               VoteArgument.is_up_vote)).all()
			tmp_dict['votes'] = len(db_votes)
			tmp_dict['valid_votes'] = len(db_valid_votes)
			tmp_dict['valid_upvotes'] = len(db_valid_upvotes)

			return_dict[str(index)] = tmp_dict

		return return_dict

	def get_logfile_for_statement(self, uid):
		"""
		Returns the logfile for the given statement uid
		:param uid: requested statement uid
		:return: dictionary with the logfile-rows
		"""
		logger('QueryHelper', 'get_logfile_for_statement', 'def with uid: ' + str(uid))

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
		return_dict['content'] = content_dict

		return return_dict

	def get_infos_about_argument(self, uid, lang):
		"""

		:param uid:
		:return:
		"""
		return_dict = dict()
		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.uid == uid,
		                                                               VoteArgument.is_valid == True,
		                                                               VoteStatement.is_up_vote == True)).all()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		db_author = DBDiscussionSession.query(User).filter_by(uid=db_argument.author_uid).first()
		return_dict['vote_count'] = str(len(db_votes))
		return_dict['author']     = db_author.nickname
		return_dict['timestamp']  = self.sql_timestamp_pretty_print(str(db_argument.timestamp), lang)

		supporter = []
		for vote in db_votes:
			supporter.append(DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first().nickname)

		return_dict['supporter'] = supporter

		return return_dict

	# ########################################
	# OTHER - SETTER
	# ########################################

	def set_news(self, transaction, title, text, user):
		"""
		Sets a new news into the news table
		:param transaction: current transaction
		:param title: news title
		:param text: news text
		:param user: self.request.authenticated_userid
		:return: dictionary {title,date,author,news}
		"""
		logger('QueryHelper', 'set_news', 'def')
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		author = db_user.firstname if db_user.firstname == 'admin' else db_user.firstname + ' ' + db_user.surname
		now = datetime.now()
		day = str(now.day) if now.day > 9 else ('0' + str(now.day))
		month = str(now.month) if now.month > 9 else ('0' + str(now.month))
		date = day + '.' + month + '.' + str(now.year)
		news = News(title=title, author=author, date=date, news=text)

		DBNewsSession.add(news)
		DBNewsSession.flush()

		db_news = DBNewsSession.query(News).filter_by(title=title).first()
		return_dict = dict()

		if db_news:
			return_dict['status'] = '1'
		else:

			return_dict['status'] = '-'

		transaction.commit()

		return_dict['title'] = title
		return_dict['date'] = date
		return_dict['author'] = author
		return_dict['news'] = text

		return return_dict

	def set_premises_as_group_for_conclusion(self, transaction, user, text, conclusion_id, is_supportive, issue):
		logger('QueryHelper', 'set_premises_as_group_for_conclusion', 'main with text ' + str(text))
		# current conclusion
		db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                         Statement.issue_uid == issue)).first()
		statements = self.insert_as_statements(transaction, text, user, issue)

		# second, set the new statements as premisegroup
		new_premisegroup_uid = self.__set_statements_as_new_premisegroup(statements, user, issue)

		# third, insert the argument
		new_argument_uid = self.__set_argument(transaction, user, new_premisegroup_uid, db_conclusion.uid, 0, is_supportive, issue)

		transaction.commit()
		return new_argument_uid

	# ########################################
	# OTHER
	# ########################################

	def process_input_of_start_premises_and_receive_url(self, transaction, premisegroups, conclusion_id, supportive, issue, user, for_api, mainpage, lang, recommender_helper):
		"""

		:param transaction:
		:param premisegroups:
		:param conclusion_id:
		:param supportive:
		:param issue:
		:param user:
		:param for_api:
		:param mainpage:
		:param lang:
		:param recommender_helper:
		:return:
		"""
		_tn = Translator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
		error = ''
		url = ''

		# insert all premisegroups into our databse
		# all new arguments are collected in a list
		new_arguments = []
		for group in premisegroups:  # premisegroups is a list of lists
			new_argument_uid = self.set_premises_as_group_for_conclusion(transaction, user, group, conclusion_id, supportive, issue)

			if new_argument_uid == -1:  # break on error
				error = _tn.get(_tn.notInsertedErrorBecauseEmpty)
				return -1, error

			new_arguments.append(new_argument_uid)

		# #arguments=0: empty input
		# #arguments=1: deliever new url
		# #arguments>1: deliever url where the user has to choose between her inputs
		if len(new_arguments) == 0:
			error = _tn.get(_tn.notInsertedErrorBecauseEmpty)

		elif len(new_arguments) == 1:
			new_argument_uid    = random.choice(new_arguments)
			arg_id_sys, attack  = recommender_helper.get_attack_for_argument(new_argument_uid, issue)
			url = UrlManager(mainpage, slug, for_api).get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)

		else:
			pgroups = []
			for argument in new_arguments:
				pgroups.append(DBDiscussionSession.query(Argument).filter_by(uid=argument).first().premisesgroup_uid)
			url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, False, supportive, conclusion_id, pgroups)

		return url, error

	def process_input_of_premises_for_arguments_and_receive_url(self, transaction, arg_id, attack_type, premisegroups,
	                                                            issue, user, for_api, mainpage, lang, recommender_helper):
		"""

		:param transaction:
		:param arg_id:
		:param attack_type:
		:param premisegroups:
		:param issue:
		:param user:
		:param for_api:
		:param mainpage:
		:param lang:
		:param recommender_helper:
		:return:
		"""
		_tn = Translator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
		error = ''
		url = ''
		supportive = attack_type == 'support' or attack_type == 'overbid'

		# insert all premisegroups into our databse
		# all new arguments are collected in a list
		new_arguments = []
		for group in premisegroups:  # premisegroups is a list of lists
			new_argument_uid = self.handle_insert_new_premises_for_argument(group, attack_type, arg_id, issue,
			                                                                         user, transaction)
			if new_argument_uid == -1:  # break on error
				error = _tn.get(_tn.notInsertedErrorBecauseEmpty)
				return -1, error
			new_arguments.append(new_argument_uid)

		# #arguments=0: empty input
		# #arguments=1: deliever new url
		# #arguments>1: deliever url where the user has to choose between her inputs
		if len(new_arguments) == 0:
			error  = _tn.get(_tn.notInsertedErrorBecauseEmpty)

		elif len(new_arguments) == 1:
			new_argument_uid = random.choice(new_arguments)
			arg_id_sys, attack = recommender_helper.get_attack_for_argument(new_argument_uid, issue)
			if arg_id_sys == 0:
				attack = 'end'

			url = UrlManager(mainpage, slug, for_api).get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
		else:
			pgroups = []
			for argument in new_arguments:
				pgroups.append(DBDiscussionSession.query(Argument).filter_by(uid=argument).first().premisesgroup_uid)

			current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_id).first()
			# relation to the arguments premisegroup
			if attack_type == 'undermine' or attack_type == 'support':
				 # TODO WHAT IS WITH PGROUPS > 1 ? CAN THIS EVEN HAPPEN IN THE WoR?
				db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).first()
				db_statement = DBDiscussionSession.query(Statement).filter_by(uid=db_premise.statement_uid).first()
				url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, False, supportive, db_statement.uid, pgroups)

			# relation to the arguments relation
			elif attack_type == 'undercut' or attack_type == 'overbid':
				url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, True, supportive, arg_id, pgroups)

			# relation to the arguments conclusion
			elif attack_type == 'rebut':
				# TODO WHAT IS WITH ARGUMENT AS CONCLUSION?
				is_argument = current_argument.conclusion_uid == 0
				uid = current_argument.argument_uid if is_argument else current_argument.conclusion_uid
				url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, is_argument, supportive, uid, pgroups)

		return url, error

	def sql_timestamp_pretty_print(self, ts, lang):
		"""

		:param ts: timestamp as string
		:param lang: language
		:return:
		"""

		formatter = '%-I:%M %p, %d. %b. %Y'
		if lang == 'de':
			try:
				locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
				formatter = '%-H:%M Uhr, %d. %b. %Y'
			except locale.Error:
				locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

		time = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

		return time.strftime(formatter)

	def correct_statement(self, transaction, user, uid, corrected_text, lang):
		"""
		Corrects a statement
		:param transaction: current transaction
		:param user: requesting user
		:param uid: requested statement uid
		:param corrected_text: new text
		:param lang: current ui_locales
		:return: True
		"""
		logger('QueryHelper', 'correct_statement', 'def ' + str(uid))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			return -1

		if corrected_text.endswith(('.', '?', '!')):
			corrected_text = corrected_text[:-1]

		# duplicate check
		return_dict = dict()
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
		db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(TextVersion.uid.desc()).all()

		# duplicate or not?
		if db_textversion:
			textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=db_textversion[0].uid).first()
		else:
			textversion = TextVersion(content=corrected_text, author=db_user.uid)
			textversion.set_statement(db_statement.uid)
			DBDiscussionSession.add(textversion)
			DBDiscussionSession.flush()

			NotificationHelper().send_edit_text_notification(textversion, lang)

		db_statement.set_textversion(textversion.uid)
		transaction.commit()

		return_dict['uid'] = uid
		return_dict['text'] = corrected_text
		return return_dict

	def insert_as_statements(self, transaction, text_list, user, issue, is_start=False):
		"""

		:param transaction:
		:param text_list:
		:param user:
		:param issue:
		:param is_start:
		:return:
		"""
		statements = []
		if isinstance(text_list, list):
			for text in text_list:
				if len(text) < self.__statement_min_length:  # TODO LENGTH
					return -1
				else:
					new_statement, is_duplicate = self.set_statement(transaction, text, user, is_start, issue)
					statements.append(new_statement)
		else:
			if len(text_list) < self.__statement_min_length:  # TODO LENGTH
				return -1
			else:
				new_statement, is_duplicate = self.set_statement(transaction, text_list, user, is_start, issue)
				statements.append(new_statement)
		return statements
