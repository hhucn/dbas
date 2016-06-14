"""
Common, pure functions used by the D-BAS.


.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import locale
from datetime import datetime
from html import escape

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Premise, Statement, TextVersion, Issue, Language
from .strings import Translator


def escape_string(text):
	"""
	Escapes all html special chars.

	:param text: string
	:return: html.escape(text)
	"""
	return escape(text)


def get_language(request, current_registry):
	"""
	Returns current ui locales code which is saved in current cookie or the registry.

	:param request: request
	:param current_registry: get_current_registry()
	:return: language abrreviation
	"""
	try:
		lang = str(request.cookies['_LOCALE_'])
	except KeyError:
		lang = str(current_registry.settings['pyramid.default_locale_name'])
	except AttributeError:
		lang = str(current_registry.settings['pyramid.default_locale_name'])
	return lang


def get_discussion_language(request, current_issue_uid=1):
	"""
	Returns Language.ui_locales
	CALL AFTER IssueHelper.get_id_of_slug(..)!

	:param request: self.request
	:return:
	"""
	# first matchdict, then params, then session, afterwards fallback
	issue = request.matchdict['issue'] if 'issue' in request.matchdict \
		else request.params['issue'] if 'issue' in request.params \
		else request.session['issue'] if 'issue' in request.session \
		else current_issue_uid

	db_lang = DBDiscussionSession.query(Issue).filter_by(uid=issue).join(Language).first()

	return db_lang.languages.ui_locales if db_lang else 'en'


def sql_timestamp_pretty_print(ts, lang, humanize=True, with_exact_time=False):
	"""
	Pretty printing for sql timestamp in dependence of the language.

	:param ts: timestamp (arrow) as string
	:param lang: language
	:param lang: humanize: Boolean
	:param lang: with_exact_time: Boolean
	:return:
	"""

	# ts = str(ts)
	# formatter = '%-I:%M %p, %d. %b. %Y'
	# if lang == 'de':
	# 	try:
	# 		locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
	# 		formatter = '%-H:%M Uhr, %d. %b. %Y'
	# 	except locale.Error:
	# 		locale.setlocale(locale.LC_TIME, 'en_US.UTF8')
	# try:  # sqlite
	# 	time = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
	# except ValueError:  # postgres
	# 	time = datetime.strptime(ts[:-6], '%Y-%m-%d %H:%M:%S.%f')
	if humanize:
		#if lang == 'de':
		ts = ts.to('Europe/Berlin')
		#else:
		#	ts = ts.to('US/Pacific')
		return ts.humanize(locale=lang)
	else:
		if lang == 'de':
			return ts.format('DD.MM.YYYY' + (', HH:mm:ss ' if with_exact_time else ''))
		else:
			return ts.format('YYYY-MM-DD' + (', HH:mm:ss ' if with_exact_time else ''))


def python_datetime_pretty_print(ts, lang):
	"""


	:param ts:
	:param lang:
	:return:
	"""
	formatter = '%d. %b.'
	if lang == 'de':
		try:
			locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
			formatter = '%b. %Y'
		except locale.Error:
			locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

	return datetime.strptime(str(ts), '%Y-%m-%d').strftime(formatter)


def get_text_for_argument_uid(uid, lang, with_strong_html_tag=False, start_with_intro=False, first_arg_by_user=False,
                              user_changed_opinion=False, rearrange_intro=False):
	"""
	Returns current argument as string like "conclusion, because premise1 and premise2"

	:param uid: Integer
	:param lang: String
	:param with_strong_html_tag: Boolean
	:param start_with_intro: Boolean
	:param first_arg_by_user: Boolean
	:param user_changed_opinion: Boolean
	:param rearrange_intro: Boolean
	:return: String
	"""
	db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
	# catch error
	if not db_argument:
		return None

	_t = Translator(lang)
	sb = '<strong>' if with_strong_html_tag else ''
	se = '</strong>' if with_strong_html_tag else ''
	because = (se + ', ') if lang == 'de' else (' ' + se)
	because += _t.get(_t.because).lower() + ' ' + sb
	doesnt_hold_because = ' ' + se + _t.get(_t.doesNotHoldBecause).lower() + ' ' + sb

	# getting all argument id
	arg_array = [db_argument.uid]
	while db_argument.argument_uid:
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=db_argument.argument_uid).first()
		arg_array.append(db_argument.uid)

	if len(arg_array) == 1:
		# build one argument only
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=arg_array[0]).first()
		premises, uids = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
		conclusion = get_text_for_statement_uid(db_argument.conclusion_uid)
		if lang != 'de':
			conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
			premises = premises[0:1].lower() + premises[1:]  # pretty print
		ret_value = (se + _t.get(_t.soYourOpinionIsThat) + ': ' + sb) if start_with_intro else ''

		if lang == 'de':
			if rearrange_intro:
				intro = _t.get(_t.itTrueIs) if db_argument.is_supportive else _t.get(_t.itFalseIs)
			else:
				intro = _t.get(_t.itIsTrue) if db_argument.is_supportive else _t.get(_t.itIsFalse)
			ret_value += se + intro[0:1].upper() + intro[1:] + ' ' + sb + conclusion + because + premises
		else:
			ret_value += conclusion + (because if db_argument.is_supportive else doesnt_hold_because) + premises

		return ret_value

	else:
		# get all pgroups and at last, the conclusion
		pgroups = []
		supportive = []
		arg_array = arg_array[::-1]
		for uid in arg_array:
			db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
			text, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, lang)
			pgroups.append((text[0:1].lower() + text[1:])if lang != 'de' else text)
			supportive.append(db_argument.is_supportive)
		conclusion = get_text_for_statement_uid(DBDiscussionSession.query(Argument).filter_by(uid=arg_array[0]).first().conclusion_uid)

		if len(arg_array) % 2 is 0 and not first_arg_by_user:  # system starts
			ret_value = se
			ret_value += _t.get(_t.earlierYouArguedThat) if user_changed_opinion else _t.get(_t.otherUsersSaidThat)
			ret_value += sb + ' '
			users_opinion = True  # user after system
			if lang != 'de':
				conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
		else:  # user starts
			ret_value = (se + _t.get(_t.soYourOpinionIsThat) + ': ' + sb) if start_with_intro else ''
			users_opinion = False  # system after user
			conclusion = conclusion[0:1].upper() + conclusion[1:]  # pretty print
		ret_value += conclusion + (because if supportive[0] else doesnt_hold_because) + pgroups[0] + '.'

		for i in range(1, len(pgroups)):
			ret_value += ' ' + se
			if users_opinion:
				if user_changed_opinion:
					ret_value += _t.get(_t.otherParticipantsConvincedYouThat)
				else:
					ret_value += _t.get(_t.butYouCounteredWith)
			else:
				ret_value += _t.get(_t.otherUsersHaveCounterArgument)
			ret_value += sb + ' ' + pgroups[i] + '.'

			# if user_changed_opinion:
			# ret_value += ' ' + se + _t.get(_t.butThenYouCounteredWith) + sb + ' ' + pgroups[i] + '.'
			# else:
			# ret_value += ' ' + se + (_t.get(_t.butYouCounteredWith) if users_opinion else _t.get(_t.otherUsersHaveCounterArgument)) + sb + ' ' + pgroups[i] + '.'
			users_opinion = not users_opinion

		ret_value = ret_value.replace('.</strong>', '</strong>.').replace('. </strong>', '</strong>. ')
		return ret_value[:-1]  # cut off punctuation


def get_text_for_premisesgroup_uid(uid, lang):
	"""
	Returns joined text of the premise group and the premise ids

	:param uid: premisesgroup_uid
	:param lang: ui_locales
	:return: text, uids
	"""
	db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=uid).join(Statement).all()
	text = ''
	uids = []
	_t = Translator(lang)
	for premise in db_premises:
		tmp = get_text_for_statement_uid(premise.statements.uid)
		if lang != 'de':
			tmp[0:1].lower() + tmp[1:]
		uids.append(str(premise.statements.uid))
		text += ' ' + _t.get(_t.aand) + ' ' + tmp

	return text[5:], uids


def get_text_for_statement_uid(uid):
	"""
	Returns text of statement with given uid

	:param uid: Statement.uid
	:return: String
	"""
	db_statement = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
	if not db_statement:
		return None

	db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
		uid=db_statement.textversion_uid).first()
	tmp = db_textversion.content

	while tmp.endswith(('.', '?', '!')):
		tmp = tmp[:-1]

	return tmp


def get_text_for_conclusion(argument, lang, start_with_intro=False, rearrange_intro=False):
	"""
	Check the arguments conclusion whether it is an statement or an argument and returns the text

	:param argument: Argument
	:param lang: ui_locales
	:param start_with_intro: Boolean
	:param rearrange_intro: Boolean
	:return: String
	"""
	if argument.argument_uid:
		return get_text_for_argument_uid(argument.argument_uid, lang, start_with_intro,rearrange_intro=rearrange_intro)
	else:
		return get_text_for_statement_uid(argument.conclusion_uid)


def resolve_issue_uid_to_slug(uid):
	"""
	Given the issue uid query database and return the correct slug of the issue.

	:param uid: issue_uid
	:type uid: int
	:return: Slug of issue
	:rtype: str
	"""
	issue = DBDiscussionSession.query(Issue).filter_by(uid=uid).first()
	return issue.get_slug() if issue else None
