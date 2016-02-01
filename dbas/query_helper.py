import datetime
import locale
import collections
from sqlalchemy import and_, func
from slugify import slugify

from .database import DBDiscussionSession, DBNewsSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, History, Vote, Issue, Group
from .database.news_model import News
from .logger import logger
from .strings import Translator, TextGenerator
from .user_management import UserHandler
from .url_manager import UrlManager

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015


class QueryHelper(object):
	"""

	"""

	def set_statement_as_new_premise(self, statement, user, issue):
		"""

		:param statement:
		:param user:
		:param issue:
		:return: uid of the PremiseGroup
		"""
		logger('QueryHelper', 'set_statement_as_new_premise', 'statement: ' + str(statement) + ', user: ' + str(user))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# check for duplicate
		db_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement.uid).first()
		if db_premise:
			logger('QueryHelper', 'set_statement_as_new_premise', 'statement is already given as premise')
			db_premisegroup = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_premise.premisesgroup_uid).all()

			if len(db_premisegroup) == 1:
				logger('QueryHelper', 'set_statement_as_new_premise', 'statement is already given as premise and the only one in its group')
				return db_premisegroup[0].premisesgroup_uid

		premise_group = PremiseGroup(author=db_user.uid)
		DBDiscussionSession.add(premise_group)
		DBDiscussionSession.flush()

		premise_list = []
		logger('QueryHelper', 'set_statement_as_new_premise', 'premisesgroup: ' + str(premise_group.uid) + ', statement: '
				+ str(statement.uid) + ', isnegated: ' + ('0' if False else '1') + ', author: ' + str(db_user.uid))
		premise = Premise(premisesgroup=premise_group.uid, statement=statement.uid, isnegated=False, author=db_user.uid, issue=issue)
		premise_list.append(premise)

		DBDiscussionSession.add_all(premise_list)
		DBDiscussionSession.flush()

		db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

		return db_premisegroup.uid

	def set_statement_as_premise(self, statement, user, premise_group_uid, issue):
		"""

		:param statement:
		:param user:
		:param premise_group_uid:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_statement_as_premise', 'statement: ' + str(statement) + ', user: ' + str(user))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		premise_list = []
		logger('QueryHelper', 'set_statement_as_premise', 'premisesgroup: ' + str(premise_group_uid) + ', statement: '
				+ str(statement.uid) + ', isnegated: ' + ('0' if False else '1') + ', author: ' + str(db_user.uid))
		premise = Premise(premisesgroup=premise_group_uid, statement=statement.uid, isnegated=False, author=db_user.uid, issue=issue)
		premise_list.append(premise)

		DBDiscussionSession.add_all(premise_list)
		DBDiscussionSession.flush()

		db_premisegroup = DBDiscussionSession.query(PremiseGroup).filter_by(author_uid=db_user.uid).order_by(PremiseGroup.uid.desc()).first()

		return db_premisegroup.uid

	def set_argument(self, transaction, user, premisegroup_uid, conclusion_uid, argument_uid, is_supportive, issue):
		"""

		:param premisegroup_uid:
		:param is_supportive:
		:param user:
		:param conclusion_uid:
		:param argument_uid:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'set_argument', 'main with user: ' + str(user)
		       + ', premisegroup_uid: ' + str(premisegroup_uid)
		       + ', conclusion_uid: ' + str(conclusion_uid)
		       + ', argument_uid: ' + str(argument_uid)
		       + ', is_supportive: ' + str(is_supportive)
		       + ', issue: ' + str(issue))

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                       Argument.is_supportive == is_supportive,
                                                                       Argument.conclusion_uid == conclusion_uid,
                                                                       Argument.issue_uid == issue)).first()
		if not new_argument:
			new_argument = Argument(premisegroup=premisegroup_uid, issupportive=is_supportive, author=db_user.uid, weight=0,
			                        conclusion=conclusion_uid, issue=issue)
			new_argument.conclusions_argument(argument_uid)

			DBDiscussionSession.add(new_argument)
			DBDiscussionSession.flush()

			new_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == premisegroup_uid,
                                                                           Argument.is_supportive == is_supportive,
                                                                           Argument.author_uid == db_user.uid,
                                                                           Argument.weight_uid == 0,
                                                                           Argument.conclusion_uid == conclusion_uid,
                                                                           Argument.argument_uid == argument_uid,
                                                                           Argument.issue_uid == issue)).first()
		transaction.commit()
		if new_argument:
			logger('QueryHelper', 'set_argument', 'new argument has uid ' + str(new_argument.uid))
			return new_argument.uid
		else:
			logger('QueryHelper', 'set_argument', 'new argument is not in the database')
			return 0

	def get_number_of_arguments(self, issue):
		"""

		:param issue:
		:return:
		"""
		return len(DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all())

	def get_text_for_statement_uid(self, uid):
		"""

		:param uid: id of a statement
		:return: text of the mapped textvalue for this statement
		"""
		logger('QueryHelper', 'get_text_for_statement_uid', 'uid ' + str(uid))
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
		if not db_statement:
			return None

		db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
			uid=db_statement.textversion_uid).first()
		logger('QueryHelper', 'get_text_for_statement_uid', 'text ' + db_textversion.content)
		tmp = db_textversion.content

		if tmp.endswith(('.','?','!')):
			tmp = tmp[:-1]

		return tmp

	def get_text_for_argument_uid(self, uid, lang):
		"""
		Returns current argument as string like conclusion, because premise1 and premise2
		:param uid: int
		:param lang: str
		:return: str
		"""
		logger('QueryHelper', 'get_text_for_argument_uid', 'uid ' + str(uid))
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		retValue = ''
		_t = Translator(lang)

		# catch error
		if not db_argument:
			logger('QueryHelper', 'get_text_for_argument_uid', 'Error: no argument for uid: ' + str(uid))
			return None

		# basecase
		if db_argument.argument_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'basecase with argument_uid: ' + str(db_argument.argument_uid)
			       + ', in argument: ' + str(db_argument.uid))
			premises, uids = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
			conclusion = self.get_text_for_statement_uid(db_argument.conclusion_uid)
			premises = premises[:-1] if premises.endswith('.') else premises  # pretty print
			if not conclusion:
				return None
			conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
			if db_argument.is_supportive:
				argument = conclusion + ' ' + _t.get(_t.because).lower() + ' ' + premises
			else:
				argument = conclusion + ' ' + _t.get(_t.doesNotHoldBecause).lower() + ' ' + premises
			# argument = premises + (' supports ' if db_argument.is_supportive else ' attacks ') + conclusion
			return argument

		# recursion
		if db_argument.conclusion_uid == 0:
			logger('QueryHelper', 'get_text_for_argument_uid', 'recursion with conclusion_uid: ' + str(db_argument.conclusion_uid)
			       + ', in argument: ' + str(db_argument.uid))
			argument = self.get_text_for_argument_uid(db_argument.argument_uid, lang)
			premises, uids = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
			if not premises:
				return None
			if db_argument.is_supportive:
				retValue = argument + ', ' + _t.get(_t.because).lower() + ' ' + premises
			else:
				retValue = argument + ' ' + _t.get(_t.doesNotHoldBecause).lower() + ' ' + premises
			# retValue = premises + (' supports ' if db_argument.is_supportive else ' attacks ') + argument

		return retValue

	def get_text_for_premisesgroup_uid(self, uid):
		"""

		:param uid: id of a premise group
		:return: text of all premises in this group and the uids as list
		"""
		logger('QueryHelper', 'get_text_for_premisesgroup_uid', 'main group ' + str(uid) )
		db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=uid).join(Statement).all()
		text = ''
		uids = []
		for premise in db_premises:
			logger('QueryHelper', 'get_text_for_premisesgroup_uid', 'premise ' + str(premise.premisesgroup_uid) + ' . statement'
					+ str(premise.statement_uid) + ', premise.statement ' + str(premise.statements.uid))
			tmp = self.get_text_for_statement_uid(premise.statements.uid)
			if tmp.endswith('.'):
				tmp = tmp[:-1]
			uids.append(str(premise.statements.uid))
			text += ' and ' + tmp[:1].lower() + tmp[1:]

		return text[5:], uids

	def get_undermines_for_premises(self, premises_as_statements_uid):
		"""

		:param premises_as_statements_uid:
		:param issue:
		:param key:
		:return:
		"""
		logger('QueryHelper', 'get_undermines_for_premises', 'main')
		return_array = []
		index = 0
		given_undermines = set()
		for s_uid in premises_as_statements_uid:
			logger('QueryHelper', 'get_undermines_for_premises', 'db_undermine against Argument.conclusion_uid=='+str(s_uid))
			db_undermine = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == False, Argument.conclusion_uid == s_uid)).all()
			for undermine in db_undermine:
				if undermine.premisesgroup_uid not in given_undermines:
					given_undermines.add(undermine.premisesgroup_uid)
					logger('QueryHelper', 'get_undermines_for_premises', 'found db_undermine ' + str(undermine.uid))
					tmp_dict = dict()
					tmp_dict['id'] = undermine.uid
					tmp_dict['text'], uids = self.get_text_for_premisesgroup_uid(undermine.premisesgroup_uid)
					return_array.append(tmp_dict)
					index += 1
		return return_array

	def get_undermines_for_argument_uid(self, argument_uid):
		"""
		Calls get_undermines_for_premises('reason', premises_as_statements_uid)
		:param argument_uid: uid of the specified argument
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
			logger('QueryHelper', 'get_undermines_for_argument_uid', 'db_attacked_argument has pgroup with pgroup ' +
		           str(premise.premisesgroup_uid) + ', statement ' + str(premise.statement_uid))

		if len(premises_as_statements_uid) == 0:
			return None

		return self.get_undermines_for_premises(premises_as_statements_uid)

	def get_overbids_for_argument_uid(self, argument_uid):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, True)
		:param argument_uid: uid of the specified argument
		:param issue:
		:return: dictionary
		"""
		logger('QueryHelper', 'get_overbids_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(argument_uid, True)

	def get_undercuts_for_argument_uid(self, argument_uid):
		"""
		Calls self.get_attack_for_justification_of_argument_uid(key, argument_uid, False)
		:param argument_uid:
		:param key:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'get_undercuts_for_argument_uid', 'main')
		return self.get_attack_or_support_for_justification_of_argument_uid(argument_uid, False)

	def get_rebuts_for_argument_uid(self, argument_uid):
		"""
		Calls self.get_rebuts_for_arguments_conclusion_uid('reason', Argument.conclusion_uid)
		:param argument_uid: uid of the specified argument
		:return: dictionary
		"""
		logger('QueryHelper', 'get_rebuts_for_argument_uid', 'main')
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=int(argument_uid)).first()
		if not db_argument:
			return None
		return self.get_rebuts_for_arguments_conclusion_uid(db_argument)

	def get_rebuts_for_arguments_conclusion_uid(self, db_argument):
		"""

		:param db_argument:
		:return:
		"""
		return_array = []
		given_rebuts = set()
		index = 0
		logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'conclusion_statements_uid ' + str(db_argument.conclusion_uid)
		       + ', is_current_argument_supportive ' + str(db_argument.is_supportive) + ' (searching for the opposite)')
		db_rebut = DBDiscussionSession.query(Argument).filter(Argument.is_supportive == (not db_argument.is_supportive),
                                                              Argument.conclusion_uid == db_argument.conclusion_uid).all()
		for rebut in db_rebut:
			if rebut.premisesgroup_uid not in given_rebuts:
				given_rebuts.add(rebut.premisesgroup_uid)
				logger('QueryHelper', 'get_rebuts_for_arguments_conclusion_uid', 'found db_rebut ' + str(rebut.uid))
				tmp_dict = dict()
				tmp_dict['id'] = rebut.uid
				text, trash = self.get_text_for_premisesgroup_uid(rebut.premisesgroup_uid)
				tmp_dict['text'] = text[0:1].upper() + text[1:]
				return_array.append(tmp_dict)
				index += 1

		return return_array

	def get_supports_for_argument_uid(self, argument_uid):
		"""

		:param argument_uid: uid of the specified argument
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
					tmp_dict['text'], trash = self.get_text_for_premisesgroup_uid(support.premisesgroup_uid)
					return_array.append(tmp_dict)
					index += 1
					given_supports.add(support.premisesgroup_uid)

		return None if len(return_array) == 0 else return_array

	def get_attack_or_support_for_justification_of_argument_uid(self, argument_uid, is_supportive):
		"""

		:param key:
		:param argument_uid:
		:param is_supportive:
		:param issue:
		:return:
		"""
		return_array = []
		logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
		       'db_undercut against Argument.argument_uid=='+str(argument_uid))
		db_relation = DBDiscussionSession.query(Argument).filter(and_(Argument.is_supportive == is_supportive,
                                                                      Argument.argument_uid == argument_uid)).all()
		given_relations = set()
		index = 0

		if not db_relation:
			return None

		for relation in db_relation:
			if relation.premisesgroup_uid not in given_relations:
				given_relations.add(relation.premisesgroup_uid)
				logger('QueryHelper', 'get_attack_or_support_for_justification_of_argument_uid',
						'found relation, argument uid ' + str(relation.uid))
				tmp_dict = dict()
				tmp_dict['id'] = relation.uid
				tmp_dict['text'], trash = self.get_text_for_premisesgroup_uid(relation.premisesgroup_uid)
				return_array.append(tmp_dict)
				index += 1
		return return_array

	def get_user_with_same_opinion(self, argument_uid, lang): # TODO USE THIS get_user_with_same_opinion
		"""

		:param argument_uid:
		:param lang:
		:return:
		"""
		logger('QueryHelper', 'get_user_with_same_opinion', 'Argument ' + str(argument_uid))

		ret_dict = dict()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			return ret_dict

		db_votes = DBDiscussionSession.query(Vote).filter_by(weight_uid=db_argument.weight_uid).all()
		uh = UserHandler()
		for vote in db_votes:
			voted_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
			logger('QueryHelper', 'get_user_with_same_opinion', 'User ' + str(voted_user.nickname)
			       + ', avatar ' + uh.get_profile_picture(voted_user))
			ret_dict[voted_user.nickname] = {'avatar_url': uh.get_profile_picture(voted_user),
			                                 'vote_timestamp': self.sql_timestamp_pretty_print(str(vote.timestamp), lang)}
		return ret_dict

	def get_id_of_slug(self, slug, request):
		"""
		Returns the uid
		:param slug: slug
		:param request: self.request for a fallback
		:return: uid
		"""
		db_issues = DBDiscussionSession.query(Issue).all()
		for issue in db_issues:
			if str(slugify(issue.title)) == str(slug):
				return issue.uid
		return self.get_issue(request)

	def get_title_for_issue_uid(self, uid):
		"""
		Returns the title or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return db_issue.title if db_issue else 'none'

	def get_slug_for_issue_uid(self, uid):
		"""
		Returns the slug of the title or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return slugify(db_issue.title) if db_issue else 'none'

	def get_info_for_issue_uid(self, uid):
		"""
		Returns the slug or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
		db_issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
		return db_issue.info if db_issue else 'none'

	def get_date_for_issue_uid(self, uid, lang):
		"""
		Returns the date or none for the issue uid
		:param uid: Issue.uid
		:return: String
		"""
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

	def add_discussion_end_text(self, discussion_dict, extras_dict, logged_in, lang, at_start=False, at_dont_know=False, at_justify_argumentation=False, at_justify=False, current_premise=''):
		"""

		:param discussion_dict: dict()
		:param extras_dict: dict()
		:param logged_in: Boolean
		:param lang: String
		:param at_start: Boolean
		:param at_dont_know: Boolean
		:param at_justify_argumentation: Boolean
		:param at_justify: Boolean
		:param current_premise: id
		:return: None
		"""
		_t = Translator(lang)
		discussion_dict['heading'] += '<br><br>'

		if at_start:
			discussion_dict['heading'] = _t.get(_t.firstPositionText)
			extras_dict['add_statement_container_style'] = '' # this will remove the 'display: none;'-style
			extras_dict['show_display_style'] = False
			extras_dict['show_bar_icon'] = False
			extras_dict['is_editable'] = False
			extras_dict['is_reportable'] = False

		elif at_justify_argumentation:
			extras_dict['add_premise_container_style'] = '' # this will remove the 'display: none;'-style
			extras_dict['show_display_style'] = False

		elif at_dont_know:
			discussion_dict['heading'] += _t.get(_t.otherParticipantsDontHaveOpinion) + '<br><br>' + (_t.get(_t.discussionEnd) + ' ' + _t.get(_t.discussionEndText))

		elif at_justify:
			discussion_dict['heading'] = _t.get(_t.firstPremiseText1) + ' <strong>' + current_premise + '</strong>.<br><br>' + _t.get(_t.whyDoYouThinkThat) + '?'
			extras_dict['add_premise_container_style'] = '' # this will remove the 'display: none;'-style
			extras_dict['show_display_style'] = False
			extras_dict['show_bar_icon'] = False
			extras_dict['is_editable'] = False
			extras_dict['is_reportable'] = False

		else:
			discussion_dict['heading'] += (_t.get(_t.discussionEnd) + ' ' + _t.get(_t.discussionEndText)) if logged_in else _t.get(_t.discussionEndFeelFreeToLogin)

	def get_everything_for_island_view(self, arg_uid, lang):
		"""

		:param arg_uid:
		:param lang:
		:param issue:
		:return:
		"""
		logger('QueryHelper', 'get_everything_for_island_view', 'def with arg_uid: ' + str(arg_uid))
		return_dict = {}
		_t = Translator(lang)

		undermine   = self.get_undermines_for_argument_uid(arg_uid)
		support     = self.get_supports_for_argument_uid(arg_uid)
		undercut    = self.get_undercuts_for_argument_uid(arg_uid)
		overbid     = self.get_overbids_for_argument_uid(arg_uid)
		rebut       = self.get_rebuts_for_argument_uid(arg_uid)

		undermine   = undermine if undermine else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		support     = support   if support   else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		undercut    = undercut  if undercut  else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		overbid     = overbid   if overbid   else [{'id': 0, 'text': _t.get(_t.no_entry)}]
		rebut       = rebut     if rebut     else [{'id': 0, 'text': _t.get(_t.no_entry)}]

		return_dict.update({'undermine': undermine})
		return_dict.update({'support':   support})
		return_dict.update({'undercut':  undercut})
		return_dict.update({'overbid':   overbid})
		return_dict.update({'rebut':     rebut})

		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(undermine)) + ' undermines')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(support)) + ' supports')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(undercut)) + ' undercuts')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(overbid)) + ' overbids')
		logger('QueryHelper', 'get_everything_for_island_view', 'summary: ' + str(len(rebut)) + ' rebuts')

		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first()
		return_dict['premise'], tmp = self.get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
		return_dict['conclusion'] = self.get_text_for_statement_uid(db_argument.conclusion_uid,) \
			if db_argument.conclusion_uid != 0 else \
			self.get_text_for_argument_uid(db_argument.argument_uid, lang)
		return_dict['heading'] = self.get_text_for_argument_uid(arg_uid, lang)

		return return_dict

	def get_language(self, request, current_registry):
		"""

		:param request: self.request
		:param current_registry: get_current_registry()
		:return: language abr
		"""
		try:
			lang = str(request.cookies['_LOCALE_'])
		except KeyError:
			lang = current_registry().settings['pyramid.default_locale_name']
		return lang

	def get_issue(self, request):
		"""
		Returns issue uid
		:param request: self.request
		:return: uid
		"""

		# first matchdict, then params, then session, afterwards fallback
		issue = request.matchdict['issue'] if 'issue' in request.matchdict \
			else request.params['issue'].split('=')[1] if 'issue' in request.params \
			else request.session['issue'] if 'issue' in request.session \
			else DBDiscussionSession.query(Issue).first().uid

		if str(issue) is 'undefined':
			self.issue_fallback = 1

		# save issue in session
		request.session['issue'] = issue
		logger('discussion_init', 'def', 'set session[issue] to ' + str(issue))

		return issue

	def get_statement_dict(self, id, title, premises, attitude, url, leading_because):
		if leading_because:
			title = title[0:1].lower() + title[1:]

		return {'id': 'item_' + str(id),
		        'title': title,
		        'premises': premises,
		        'attitude': attitude,
		        'url': url,
		        'leading_because': leading_because}

	def sql_timestamp_pretty_print(self, ts, lang):
		"""

		:param ts: timestamp as string
		:param lang: language
		:return:
		"""

		format = '%-I:%M %p, %d. %b. %Y'
		if lang == 'de':
			try:
				locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
				format = '%-H:%M Uhr, %d. %b. %Y'
			except:
				locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

		time = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

		return time.strftime(format)

	def correct_statement(self, transaction, user, uid, corrected_text):
		"""
		Corrects a statement
		:param transaction: current transaction
		:param user: requesting user
		:param uid: requested statement uid
		:param corrected_text: new text
		:return: True
		"""
		logger('QueryHelper', 'correct_statement', 'def ' + str(uid))

		return_dict = dict()
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()

		if corrected_text.endswith(('.','?','!')):
			corrected_text = corrected_text[:-1]

		# duplicate check
		db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(TextVersion.uid.desc()).first()

		if db_user:
			logger('QueryHelper', 'correct_statement', 'given user exists and correction will be set')
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
			logger('QueryHelper', 'correct_statement', 'user not found')
			return_dict['status'] = '-1'

		return_dict['uid'] = uid
		return_dict['text'] = corrected_text
		return return_dict

	def get_news(self):
		"""
		Returns all news in a dicitionary, sorted by date
		:return: dict()
		"""
		logger('QueryHelper', 'get_news', 'main')
		db_news = DBNewsSession.query(News).all()
		logger('QueryHelper', 'get_news', 'we have ' + str(len(db_news)) + ' news')
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
			sec = (date_object - datetime.datetime(1970,1,1)).total_seconds() + index
			logger('QueryHelper', 'get_news', 'news from  ' + str(news.date) + ', ' + str(sec))
			ret_dict[str(sec)] = news_dict

		ret_dict = collections.OrderedDict(sorted(ret_dict.items()))

		return ret_dict

	def get_dump(self, issue, lang):
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
			tmp_dict['uid']         = user.uid
			tmp_dict['nickname']    = user.nickname
			user_dict[str(index)]   = tmp_dict
		ret_dict['user'] = user_dict

		# getting all statements
		db_statements = DBDiscussionSession.query(Statement).all()
		statement_dict = dict()
		for index, statement in enumerate(db_statements):
			tmp_dict = dict()
			tmp_dict['uid']             = statement.uid
			tmp_dict['textversion_uid'] = statement.textversion_uid
			tmp_dict['is_startpoint']   = statement.is_startpoint
			statement_dict[str(index)]  = tmp_dict
		ret_dict['statement'] = statement_dict

		# getting all textversions
		db_textversions = DBDiscussionSession.query(TextVersion).all()
		textversion_dict = dict()
		for index, textversion in enumerate(db_textversions):
			tmp_dict = dict()
			tmp_dict['uid']              = textversion.uid
			tmp_dict['statement_uid']    = textversion.statement_uid
			tmp_dict['content']          = textversion.content
			tmp_dict['author_uid']       = textversion.author_uid
			tmp_dict['timestamp']        = self.sql_timestamp_pretty_print(str(textversion.timestamp), lang)
			textversion_dict[str(index)] = tmp_dict
		ret_dict['textversion'] = textversion_dict

		# getting all premisegroups
		db_premisegroups = DBDiscussionSession.query(PremiseGroup).all()
		premisegroup_dict = dict()
		for index, premisegroup in enumerate(db_premisegroups):
			tmp_dict = dict()
			tmp_dict['uid']                 = premisegroup.uid
			tmp_dict['author_uid']          = premisegroup.author_uid
			premisegroup_dict[str(index)]   = tmp_dict
		ret_dict['premisegroup'] = premisegroup_dict

		# getting all premises
		db_premises = DBDiscussionSession.query(Premise).all()
		premise_dict = dict()
		for index, premise in enumerate(db_premises):
			tmp_dict = dict()
			tmp_dict['premisesgroup_uid'] = premise.premisesgroup_uid
			tmp_dict['statement_uid']     = premise.statement_uid
			tmp_dict['is_negated']        = premise.is_negated
			tmp_dict['author_uid']        = premise.author_uid
			tmp_dict['timestamp']         = self.sql_timestamp_pretty_print(str(premise.timestamp), lang)
			premise_dict[str(index)]      = tmp_dict
		ret_dict['premise'] = premise_dict

		# getting all arguments
		db_arguments = DBDiscussionSession.query(Argument).all()
		argument_dict = dict()
		for index, argument in enumerate(db_arguments):
			tmp_dict = dict()
			tmp_dict['uid']                 = argument.uid
			tmp_dict['premisesgroup_uid']   = argument.premisesgroup_uid
			tmp_dict['conclusion_uid']      = argument.conclusion_uid
			tmp_dict['argument_uid']        = argument.argument_uid
			tmp_dict['is_supportive']       = argument.is_supportive
			tmp_dict['author_uid']          = argument.author_uid
			tmp_dict['timestamp']           = self.sql_timestamp_pretty_print(str(argument.timestamp), lang)
			argument_dict[str(index)]       = tmp_dict
		ret_dict['argument'] = argument_dict

		# getting all votes
		db_votes = DBDiscussionSession.query(Vote).all()
		vote_dict = dict()
		for index, vote in enumerate(db_votes):
			tmp_dict = dict()
			tmp_dict['argument_uid'] = vote.argument_uid
			tmp_dict['author_uid']   = vote.author_uid
			tmp_dict['is_up_vote']   = vote.is_up_vote
			tmp_dict['is_valid']     = vote.is_valid
			vote_dict[str(index)]    = tmp_dict
		ret_dict['vote'] = vote_dict

		return ret_dict

	def get_all_users(self, user, lang):
		"""

		:param user:
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

	def get_attack_overview(self, user, issue, lang):  # TODO
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
			logger('QueryHelper', 'get_attack_overview', 'argument with uid ' + str(argument.uid))
			tmp_dict = dict()
			tmp_dict['uid'] = str(argument.uid)
			tmp_dict['text'] = self.get_text_for_argument_uid(argument.uid, lang)
			db_votes = DBDiscussionSession.query(Vote).filter_by(argument_uid=argument.uid).all()
			db_valid_votes = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==argument.uid,
			                                                             Vote.is_valid==True)).all()
			db_valid_upvotes = DBDiscussionSession.query(Vote).filter(and_(Vote.argument_uid==argument.uid,
			                                                               Vote.is_valid==True,
			                                                               Vote.is_up_vote)).all()
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
			logger('QueryHelper', 'get_logfile_for_statement', 'statement ' + str(index) + ': ' + versions.content)
		return_dict['content'] = content_dict

		return return_dict

	def handle_insert_new_premise_for_argument(self, text, current_attack, arg_uid, supportive, issue, user, transaction):
		"""

		:param relation:
		:param arg_uid:
		:param supportive:
		:return:
		"""
		logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'def')

		# insert text as premise
		new_statement, is_duplicate = self.set_statement(transaction, text, user, False, issue)
		if new_statement == -1:
			return 0
		new_premisegroup_uid = self.set_statement_as_new_premise(new_statement, user, issue)

		# current argument
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		# current user
		current_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_uid).first()

		if current_attack == 'undermine' or current_attack == 'support': # TODO handle premise groups
			new_arguments = []
			already_in = []
			# duplicate?
			# all premises out of current pgroup
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).all()
			for premise in db_premises:
				db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == new_premisegroup_uid,
                                                                              Argument.is_supportive == (current_attack == 'support'),
                                                                              Argument.conclusion_uid == premise.statement_uid,
                                                                              Argument.argument_uid == 0)).first()

				if db_argument:
					already_in.append(db_argument.uid)
				else:
					new_argument = Argument(premisegroup=new_premisegroup_uid,
				                            issupportive=current_attack == 'support',
				                            author=db_user.uid,
				                            weight=0,
				                            conclusion=premise.statement_uid,
				                            issue=issue)
					new_argument.conclusions_argument(0)
					new_arguments.append(new_argument)

				logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'new_arguments ' + str(new_arguments))
				if len(new_arguments)>0:
					DBDiscussionSession.add_all(new_arguments)
					DBDiscussionSession.flush()
					transaction.commit()
					for argument in new_arguments:
						logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'new_argument_uid ' + str(argument.uid))
						already_in.append(argument.uid)

				rnd = random.randint(0, len(already_in)-1)

				logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'already_in ' + str(already_in))
				logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'return a ' + str(already_in[rnd]))
				return already_in[rnd]


		elif current_attack == 'undercut' or current_attack == 'overbid':
			# duplicate?
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == new_premisegroup_uid,
                                                                          Argument.is_supportive == (current_attack == 'overbid'),
                                                                          Argument.conclusion_uid == 0,
                                                                          Argument.argument_uid == current_argument.uid)).first()
			if db_argument:
				logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'return b ' + str(db_argument.uid))
				return db_argument.uid
			else:
				new_argument = Argument(premisegroup=new_premisegroup_uid,
				                        issupportive=current_attack == 'overbid',
				                        author=db_user.uid,
				                        weight=0,
				                        conclusion=0,
				                        issue=issue)
				new_argument.conclusions_argument(current_argument.uid)
				DBDiscussionSession.add(new_argument)
				DBDiscussionSession.flush()
				transaction.commit()

		elif current_attack == 'rebut':
			# duplicate?
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == new_premisegroup_uid,
                                                                          Argument.is_supportive == False,
                                                                          Argument.conclusion_uid == current_argument.conclusion_uid,
                                                                          Argument.argument_uid == 0)).first()
			if db_argument:
				logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'return c ' + str(db_argument.uid))
				return db_argument.uid
			else:
				new_argument = Argument(premisegroup=new_premisegroup_uid,
				                        issupportive=False,
				                        author=db_user.uid,
				                        weight=0,
				                        conclusion=current_argument.conclusion_uid,
				                        issue=issue)
				new_argument.conclusions_argument(0)
				DBDiscussionSession.add(new_argument)
				DBDiscussionSession.flush()
				transaction.commit()

		logger('QueryHelper', 'handle_insert_new_premise_for_argument', 'return d ' + str(new_argument.uid if new_argument else 0))
		return new_argument.uid if new_argument else 0

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
		news = News(title = title, author = author, date = date, news = text)

		DBNewsSession.add(news)
		DBNewsSession.flush()

		db_news = DBNewsSession.query(News).filter_by(title=title).first()
		return_dict = dict()

		if db_news:
			logger('QueryHelper', 'set_news', 'new news is in db')
			return_dict['status'] = '1'
		else:

			logger('QueryHelper', 'set_news', 'new news is not in db')
			return_dict['status'] = '-'

		transaction.commit()

		return_dict['title'] = title
		return_dict['date'] = date
		return_dict['author'] = author
		return_dict['news'] = text

		return return_dict

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
		logger('QueryHelper', 'set_statement', 'user: ' + str(user) + ', user_id: ' + str(db_user.uid) + ', statement: ' + str(
			statement) + ', issue: ' + str(issue))

		if len(statement) < 5: # TODO IMPROVE
			return -1, False

		# check for dot at the end
		if not statement.endswith(('.','?','!')):
			statement += '.'
		if statement.lower().startswith('because '):
			statement = statement[8:]

		# check, if the statement already exists
		logger('QueryHelper', 'set_statement', 'check for duplicate with: ' + statement)
		db_duplicate = DBDiscussionSession.query(TextVersion).filter(func.lower(TextVersion.content)==func.lower(statement)).first()
		if db_duplicate:
			db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.textversion_uid == db_duplicate.uid,
			                                                                Statement.issue_uid == issue)).first()
			logger('QueryHelper', 'set_statement', 'duplicate, returning old statement with uid ' + str(db_statement.uid))
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

		logger('QueryHelper', 'set_statement', 'returning new statement with uid ' + str(new_statement.uid))
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
		logger('QueryHelper', 'set_premises_for_conclusion', 'main')
		# current conclusion
		db_conclusion = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == conclusion_id,
                                                                         Statement.issue_uid == issue)).first()

		# first, save the premise as statement
		new_statement, is_duplicate = self.set_statement(transaction, text, user, False, issue)
		if new_statement == -1:
			return -1, False
		# duplicates do not count, because they will be fetched in set_statement_as_new_premise

		# second, set the new statement as premise
		new_premisegroup_uid = qh.set_statement_as_new_premise(new_statement, user, issue)
		logger('QueryHelper', 'set_premises_for_conclusion', text + ' in new_premisegroup_uid ' + str(new_premisegroup_uid)
		       + ' to statement ' + str(db_conclusion.uid) + ', ' + ('' if is_supportive else '' ) + 'supportive')

		# third, insert the argument
		new_argument_uid = qh.set_argument(transaction, user, new_premisegroup_uid, db_conclusion.uid, 0, is_supportive, issue)

		transaction.commit()
		return new_argument_uid, is_duplicate

