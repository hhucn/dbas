"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import collections
import random
from datetime import datetime

from slugify import slugify
from sqlalchemy import and_, func

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, VoteArgument, VoteStatement, Issue
from dbas.database.news_model import News
from dbas.helper.notification_helper import NotificationHelper
from dbas.helper.relation_helper import RelationHelper
from dbas.lib import escape_string, sql_timestamp_pretty_print, get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid
from dbas.logger import logger
from dbas.strings import Translator
from dbas.url_manager import UrlManager
from dbas.user_management import UserHandler


class QueryHelper(object):
	"""
	Todo
	"""

	def __init__(self):
		self.__statement_min_length = 5
		#  self.lang = ''
		#  TODO move lang here and init translator

	# ########################################
	# ARGUMENTS
	# ########################################

	def handle_insert_new_premises_for_argument(self, text, current_attack, arg_uid, issue, user, transaction):
		"""

		:param text: String
		:param current_attack: String
		:param arg_uid: Argument.uid
		:param issue: Issue
		:param user: User.nickname
		:param transaction: transaction
		:return:
		"""
		logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'def')
		_rh = RelationHelper()

		statements = self.insert_as_statements(transaction, text, user, issue)
		if statements == -1:
			return -1

		# set the new statements as premise group and get current user as well as current argument
		new_pgroup_uid = self.__set_statements_as_new_premisegroup(statements, user, issue)
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first()

		new_argument = None
		if current_attack == 'undermine':
			new_argument = _rh.set_new_undermine_or_support(transaction, new_pgroup_uid, current_argument, current_attack, db_user, issue)

		elif current_attack == 'support':
			new_argument, duplicate = _rh.set_new_support(transaction, new_pgroup_uid, current_argument, db_user, issue)

		elif current_attack == 'undercut' or current_attack == 'overbid':
			new_argument, duplicate = _rh.set_new_undercut_or_overbid(transaction, new_pgroup_uid, current_argument, current_attack, db_user, issue)

		elif current_attack == 'rebut':
			new_argument, duplicate = _rh.set_new_rebut(transaction, new_pgroup_uid, current_argument, db_user, issue)

		return new_argument.uid

	@staticmethod
	def __set_argument(transaction, user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
		"""

		:param transaction: transaction
		:param user: User.nickname
		:param premisegroup_uid: PremseGroup.uid
		:param conclusion_uid: Statement.uid
		:param argument_uid: Argument.uid
		:param is_supportive: Boolean
		:param issue: Issue.uid
		:return:
		"""
		logger('QueryHelper', '__set_argument', 'main with user: ' + str(user) +
		       ', premisegroup_uid: ' + str(premisegroup_uid) +
		       ', conclusion_uid: ' + str(conclusion_uid) +
		       ', argument_uid: ' + str(argument_uid) +
		       ', is_supportive: ' + str(is_supportive) +
		       ', issue: ' + str(issue))

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
			logger('QueryHelper', '__set_argument', 'argument was inserted')
			logger('QueryHelper', '__set_argument', 'argument was inserted')
			return new_argument.uid
		else:
			logger('QueryHelper', '__set_argument', 'argument was not inserted')
			logger('QueryHelper', '__set_argument', 'argument was not inserted')
			return None

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
		:param lang: ui_locales ui_locales
		:return: String
		"""
		#  logger('QueryHelper', 'get_date_for_issue_uid', str(uid))
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return sql_timestamp_pretty_print(str(db_issue.date), lang) if db_issue else 'none'

	def prepare_json_of_issue(self, uid, application_url, lang, for_api):
		"""
		Prepares slug, info, argument count and the date of the issue as dict

		:param uid: Issue.uid
		:param application_url:
		:param lang: ui_locales
		:param for_api: Boolean
		:return: Issue-dict()
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
			issue_dict = self.get_issue_dict_for(issue, application_url, for_api, uid, lang)
			all_array.append(issue_dict)

		_t = Translator(lang)
		tooltip = _t.get(_t.discussionInfoTooltip1) + ' ' + date + ' ' +\
		          _t.get(_t.discussionInfoTooltip2) + ' ' + str(arg_count) + ' ' +\
		          (_t.get(_t.discussionInfoTooltip3pl) if arg_count > 1 else _t.get(_t.discussionInfoTooltip3sg))

		return {'slug': slug, 'info': info, 'title': title, 'uid': uid, 'arg_count': arg_count, 'date': date, 'all': all_array, 'tooltip': tooltip}

	def get_number_of_arguments(self, issue):
		"""
		Returns number of arguments for the issue

		:param issue: Issue Issue.uid
		:return: Integer
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
		:param user: User.nickname
		:param issue: Issue
		:return:
		"""
		logger('QueryHelper', '__set_statements_as_new_premisegroup', 'user: ' + str(user) +
		       ', statement: ' + str(statements) + ', issue: ' + str(issue))
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

		:param transaction: transaction current transaction
		:param statement: given statement
		:param user: User.nickname given user
		:param is_start: if it is a start statement
		:param issue: Issue
		:return: Statement, is_duplicate or -1, False on error
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('QueryHelper', 'set_statement', 'user: ' + str(user) + ', user_id: ' + str(db_user.uid) +
		       ', statement: ' + str(statement) + ', issue: ' + str(issue))

		# escaping
		statement = escape_string(statement)

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

	# ########################################
	# OTHER - GETTER
	# ########################################

	def __get_attack_or_support_for_justification_of_argument_uid(self, argument_uid, is_supportive, lang):
		"""

		:param argument_uid: Argument.uid
		:param is_supportive: Boolean
		:param lang: ui_locales
		:return:
		"""
		return_array = []
		logger('QueryHelper', '__get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid==' + str(argument_uid))
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
				tmp_dict['text'], trash = get_text_for_premisesgroup_uid(relation.premisesgroup_uid, lang)
				return_array.append(tmp_dict)
				index += 1
		return return_array

	def get_user_with_same_opinion_for_argument(self, argument_uid, lang, nickname):
		"""

		:param argument_uid: Argument.uid Statement.uid
		:param lang: ui_locales ui_locales
		:param nickname: nickname
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('QueryHelper', 'get_user_with_same_opinion_for_argument', 'Argument ' + str(argument_uid))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		ret_dict = dict()
		all_users = []
		_t = Translator(lang)
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			ret_dict['message'] = _t.get(_t.internalError) + '.'
			ret_dict['users'] = all_users
			return ret_dict

		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == db_argument.uid,
		                                                               VoteArgument.is_up_vote == True,
		                                                               VoteArgument.is_valid == True,
		                                                               VoteArgument.author_uid != db_user_uid)).all()
		uh = UserHandler()
		for vote in db_votes:
			users_dict = dict()
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict[voted_user.nickname] = {'avatar_url': uh.get_profile_picture(voted_user),
			                                   'vote_timestamp': sql_timestamp_pretty_print(str(vote.timestamp), lang)}
			all_users.append(users_dict)
			ret_dict['users'] = all_users

		l = len(db_votes)
		if l == 0:
			ret_dict['message'] = _t.get(_t.voteCountTextFirst) + '.'
		elif l == 1:
			ret_dict['message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			ret_dict['message'] = str(l) + ' ' + _t.get(_t.voteCountTextMore) + '.'

		return ret_dict

	def get_user_with_same_opinion_for_statement(self, statement_uid, lang, nickname):
		"""

		:param statement_uid: Statement.uid
		:param lang: ui_locales ui_locales
		:param nickname: nickname
		:return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
		"""
		logger('QueryHelper', 'get_user_with_same_opinion_for_statement', 'Statement ' + str(statement_uid))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		ret_dict = dict()
		all_users = []
		_t = Translator(lang)
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=statement_uid).first()
		if not db_statement:
			ret_dict['users'] = all_users
			return ret_dict

		db_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == db_statement.uid,
		                                                                VoteStatement.is_up_vote == True,
		                                                                VoteStatement.is_valid == True,
		                                                                VoteStatement.author_uid != db_user_uid)).all()
		uh = UserHandler()
		for vote in db_votes:
			users_dict = dict()
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			users_dict[voted_user.nickname] = {'avatar_url': uh.get_profile_picture(voted_user),
			                                   'vote_timestamp': sql_timestamp_pretty_print(str(vote.timestamp), lang)}
			all_users.append(users_dict)
		ret_dict['users'] = all_users

		if len(db_votes) == 0:
			ret_dict['message'] = _t.get(_t.voteCountTextFirst) + '.'
		elif len(db_votes) == 1:
			ret_dict['message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			ret_dict['message'] = str(db_votes) + ' ' + _t.get(_t.voteCountTextMore) + '.'

		return ret_dict

	def get_user_with_same_opinion_for_position(self, issue_uid, lang, nickname):
		"""

		:param issue_uid:
		:param lang: ui_locales
		:param nickname:
		:return:
		"""
		logger('QueryHelper', 'get_user_with_same_opinion_for_position', 'issue ' + str(issue_uid))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		db_user_uid = db_user.uid if db_user else 0

		ret_dict = dict()
		_t = Translator(lang)
		db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.issue_uid == issue_uid,
		                                                                Statement.is_startpoint == True)).all()
		if not db_statements:
			return ret_dict

		uh = UserHandler()
		votes = []
		for statement in db_statements:
			vote_dict = dict()
			vote_dict['statement_uid'] = str(statement.uid)
			vote_dict['text'] = get_text_for_statement_uid(statement.uid)
			db_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
			                                                                VoteStatement.is_up_vote == True,
			                                                                VoteStatement.is_valid == True,
			                                                                VoteStatement.author_uid != db_user_uid)).all()
			vote_dict['count'] = str(len(db_votes))
			all_users = {}
			for vote in db_votes:
				db_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
				all_users[db_user.nickname] = {'avatar_url': uh.get_profile_picture(db_user),
				                               'vote_timestamp': sql_timestamp_pretty_print(str(vote.timestamp), lang)}
			vote_dict['users'] = all_users
			votes.append(vote_dict)

		ret_dict['votes'] = votes

		ret_dict['message'] = 'TODO'

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

		:param arg_uid: Argument.uid
		:param lang: ui_locales
		:return:
		"""
		logger('QueryHelper', 'get_every_attack_for_island_view', 'def with arg_uid: ' + str(arg_uid))
		return_dict = {}
		_t = Translator(lang)
		_rh = RelationHelper()

		undermine = _rh.get_undermines_for_argument_uid(arg_uid, lang)
		support = _rh.get_supports_for_argument_uid(arg_uid, lang)
		undercut = _rh.get_undercuts_for_argument_uid(arg_uid, lang)
		# overbid = _rh.get_overbids_for_argument_uid(arg_uid, lang)
		rebut = _rh.get_rebuts_for_argument_uid(arg_uid, lang)

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

		# pretty pring
		for dict in return_dict:
			for entry in return_dict[dict]:
				entry['text'] = entry['text'][0:1].upper() + entry['text'][1:]

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
		:return: language abbreviation
		"""
		try:
			lang = str(request.cookies['_LOCALE_'])
		except KeyError:
			lang = str(current_registry.settings['pyramid.default_locale_name'])
		return lang

	def get_news(self):
		"""
		Returns all news in a dictionary, sorted by date
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
			date_object = datetime.strptime(str(news.date), '%d.%m.%Y')
			# add index on the seconds for unique id's
			sec = (date_object - datetime(1970, 1, 1)).total_seconds() + index
			ret_dict[str(sec)] = news_dict

		ret_dict = collections.OrderedDict(sorted(ret_dict.items()))

		return ret_dict

	def get_logfile_for_statement(self, uid, lang):
		"""
		Returns the logfile for the given statement uid

		:param uid: requested statement uid
		:param lang: ui_locales ui_locales
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
			corr_dict['date'] = sql_timestamp_pretty_print(str(versions.timestamp), lang)
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
		db_votes = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == uid,
		                                                               VoteArgument.is_valid == True,
		                                                               VoteStatement.is_up_vote == True)).all()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		db_author = DBDiscussionSession.query(User).filter_by(uid=db_argument.author_uid).first()
		return_dict['vote_count'] = str(len(db_votes))
		return_dict['author']     = db_author.nickname
		return_dict['timestamp']  = sql_timestamp_pretty_print(str(db_argument.timestamp), lang)
		return_dict['text']       = '<strong>' + get_text_for_argument_uid(uid, lang, True, True, first_arg_by_user=True) + '</strong>'

		supporters = []
		gravatars = dict()
		_um = UserHandler()
		for vote in db_votes:
			db_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			supporters.append(db_user.nickname)
			gravatars[db_user.nickname] = _um.get_profile_picture(db_user)

		return_dict['supporter'] = supporters
		return_dict['gravatars'] = gravatars

		return return_dict

	# ########################################
	# OTHER - SETTER
	# ########################################

	def set_news(self, transaction, title, text, user):
		"""
		Sets a new news into the news table

		:param transaction: transaction current transaction
		:param title: news title
		:param text: String news text
		:param user: User.nickname self.request.authenticated_userid
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
		"""
		
		:param transaction: transaction
		:param user: User.nickname
		:param text: String
		:param conclusion_id:
		:param is_supportive: Boolean
		:param issue: Issue
		:return:
		"""
		logger('QueryHelper', 'set_premises_as_group_for_conclusion', 'main with text ' + str(text))
		# current conclusion
		db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                         Statement.issue_uid == issue)).first()
		statements = self.insert_as_statements(transaction, text, user, issue)
		if statements == -1:
			return -1

		statement_uids = [s.uid for s in statements]

		# second, set the new statements as premisegroup
		new_premisegroup_uid = self.__set_statements_as_new_premisegroup(statements, user, issue)

		# third, insert the argument
		new_argument_uid = self.__set_argument(transaction, user, new_premisegroup_uid, db_conclusion.uid, None, is_supportive, issue)

		transaction.commit()
		return new_argument_uid, statement_uids

	def set_issue(self, info, title, nickname, transaction, ui_locales):
		"""

		:param info:
		:param title:
		:param nickname:
		:param transaction: transaction
		:param ui_locales:
		:return:
		"""
		_tn = Translator(ui_locales)

		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		if not UserHandler().is_user_author(nickname):
			return False, _tn.get(_tn.noRights)

		if len(info) < 10:
			return False, _tn.get(_tn.notInsertedErrorBecauseEmpty)

		db_duplicates1 = DBDiscussionSession.query(Issue).filter_by(title=title).all()
		db_duplicates2 = DBDiscussionSession.query(Issue).filter_by(info=info).all()
		if db_duplicates1 or db_duplicates2:
			return False, _tn.get(_tn.duplicate)

		DBDiscussionSession.add(Issue(title=title, info=info, author_uid=db_user.uid))
		DBDiscussionSession.flush()

		transaction.commit()

		return True, ''

	# ########################################
	# OTHER
	# ########################################

	def process_input_of_start_premises_and_receive_url(self, transaction, premisegroups, conclusion_id, supportive,
	                                                    issue, user, for_api, mainpage, lang, recommender_helper):
		"""

		:param transaction: transaction
		:param premisegroups:
		:param conclusion_id:
		:param supportive:
		:param issue: Issue
		:param user: User.nickname
		:param for_api: Boolean
		:param mainpage:
		:param lang: ui_locales
		:param recommender_helper:
		:return:
		"""
		logger('QueryHelper', 'process_input_of_start_premises_and_receive_url', 'count of new pgroups: ' + str(len(premisegroups)))
		_tn = Translator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
		error = ''
		url = ''

		# insert all premise groups into our database
		# all new arguments are collected in a list
		new_argument_uids = []
		new_statement_uids = []  # all statement uids are stored in this list to create the link to a possible reference
		for group in premisegroups:  # premise groups is a list of lists
			new_argument_uid, statement_uids = self.set_premises_as_group_for_conclusion(transaction, user, group, conclusion_id, supportive, issue)
			if new_argument_uid == -1:  # break on error
				error = _tn.get(_tn.notInsertedErrorBecauseEmpty)
				return -1, error

			new_argument_uids.append(new_argument_uid)
			if for_api:
				new_statement_uids.append(statement_uids)

		# #arguments=0: empty input
		# #arguments=1: deliver new url
		# #arguments>1: deliver url where the user has to choose between her inputs
		if len(new_argument_uids) == 0:
			error = _tn.get(_tn.notInsertedErrorBecauseEmpty)

		elif len(new_argument_uids) == 1:
			new_argument_uid    = random.choice(new_argument_uids)
			arg_id_sys, attack  = recommender_helper.get_attack_for_argument(new_argument_uid, issue, lang)
			url = UrlManager(mainpage, slug, for_api).get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)

		else:
			pgroups = []
			for arg_uid in new_argument_uids:
				pgroups.append(DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first().premisesgroup_uid)
			url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, False, supportive, conclusion_id, pgroups)

		return url, new_statement_uids, error

	def process_input_of_premises_for_arguments_and_receive_url(self, transaction, arg_id, attack_type, premisegroups,
	                                                            issue, user, for_api, mainpage, lang, recommender_helper):
		"""

		.. note::

			Optimize the "for_api" part

		:param transaction: transaction
		:param arg_id:
		:param attack_type:
		:param premisegroups:
		:param issue: Issue
		:param user: User.nickname
		:param for_api: Boolean
		:param mainpage:
		:param lang: ui_locales
		:param recommender_helper:
		:return:
		"""
		_tn = Translator(lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()
		error = ''
		url = ''
		supportive = attack_type == 'support' or attack_type == 'overbid'

		# insert all premise groups into our database
		# all new arguments are collected in a list
		new_arguments = []
		for group in premisegroups:  # premise groups is a list of lists
			new_argument_uid = self.handle_insert_new_premises_for_argument(group, attack_type, arg_id, issue, user, transaction)
			if new_argument_uid == -1:  # break on error
				error = _tn.get(_tn.notInsertedErrorBecauseEmpty)
				return -1, error
			new_arguments.append(new_argument_uid)

		statement_uids = []
		if for_api:
			# @OPTIMIZE
			# Query all recently stored premises (internally: statements) and collect their ids
			# This is a bad workaround, let's just think about it in future.
			for argument in new_arguments:
				current_pgroup = DBDiscussionSession.query(Argument).filter_by(uid=argument).first().premisesgroup_uid
				current_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_pgroup).all()
				for premise in current_premises:
					statement_uids.append(premise.statement_uid)

		# #arguments=0: empty input
		# #arguments=1: deliver new url
		# #arguments>1: deliver url where the user has to choose between her inputs
		if len(new_arguments) == 0:
			error = _tn.get(_tn.notInsertedErrorBecauseEmpty)

		elif len(new_arguments) == 1:
			new_argument_uid = random.choice(new_arguments)
			arg_id_sys, attack = recommender_helper.get_attack_for_argument(new_argument_uid, issue, lang)
			if arg_id_sys == 0:
				attack = 'end'

			url = UrlManager(mainpage, slug, for_api).get_url_for_reaction_on_argument(False, new_argument_uid, attack, arg_id_sys)
		else:
			pgroups = []
			for argument in new_arguments:
				pgroups.append(DBDiscussionSession.query(Argument).filter_by(uid=argument).first().premisesgroup_uid)

			current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_id).first()
			# relation to the arguments premise group
			if attack_type == 'undermine' or attack_type == 'support':  # TODO WHAT IS WITH PGROUPS > 1 ? CAN THIS EVEN HAPPEN IN THE WoR?
				db_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).first()
				db_statement = DBDiscussionSession.query(Statement).filter_by(uid=db_premise.statement_uid).first()
				url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, False, supportive, db_statement.uid, pgroups)

			# relation to the arguments relation
			elif attack_type == 'undercut' or attack_type == 'overbid':
				url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, True, supportive, arg_id, pgroups)

			# relation to the arguments conclusion
			elif attack_type == 'rebut':
				# TODO WHAT IS WITH ARGUMENT AS CONCLUSION?
				is_argument = current_argument.conclusion_uid is not None
				uid = current_argument.argument_uid if is_argument else current_argument.conclusion_uid
				url = UrlManager(mainpage, slug, for_api).get_url_for_choosing_premisegroup(False, is_argument, supportive, uid, pgroups)

		return url, statement_uids, error

	def correct_statement(self, transaction, user, uid, corrected_text, lang):
		"""
		Corrects a statement

		:param transaction: transaction current transaction
		:param user: User.nickname requesting user
		:param uid: requested statement uid
		:param corrected_text: new text
		:param lang: ui_locales current ui_locales
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

		:param transaction: transaction
		:param text_list:
		:param user: User.nickname
		:param issue: Issue
		:param is_start: Boolean
		:return:
		"""
		statements = []
		if isinstance(text_list, list):
			for text in text_list:
				if len(text) < self.__statement_min_length:
					return -1
				else:
					new_statement, is_duplicate = self.set_statement(transaction, text, user, is_start, issue)
					statements.append(new_statement)
		else:
			if len(text_list) < self.__statement_min_length:
				return -1
			else:
				new_statement, is_duplicate = self.set_statement(transaction, text_list, user, is_start, issue)
				statements.append(new_statement)
		return statements

	def get_issue_dict_for(self, issue, application_url, for_api, uid, lang):
		"""

		:param issue: Issue
		:param application_url:
		:param for_api: Boolean
		:param uid:
		:param lang: ui_locales
		:return:
		"""
		issue_dict = dict()
		issue_dict['slug']              = issue.get_slug()
		issue_dict['title']             = issue.title
		issue_dict['url']               = UrlManager(application_url, issue.get_slug(), for_api).get_slug_url(False) if str(uid) != str(issue.uid) else ''
		issue_dict['info']              = issue.info
		issue_dict['arg_count']         = self.get_number_of_arguments(issue.uid)
		issue_dict['date']              = sql_timestamp_pretty_print(str(issue.date), lang)
		issue_dict['enabled']           = 'disabled' if str(uid) == str(issue.uid) else 'enabled'
		return issue_dict
