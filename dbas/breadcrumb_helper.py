import collections
import re
from sqlalchemy import and_, func
from slugify import slugify

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, History, Issue
from .logger import logger
from .strings import Translator
from .query_helper import QueryHelper
from .url_manager import UrlManager

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class BreadcrumbHelper(object):

	def save_breadcrumb(self, path, user, slug, session_id, transaction, lang, application_url, for_api):
		"""

		:param path:
		:param user:
		:param slug:
		:param session_id:
		:param transaction:
		:param lang:
		:param application_url:
		:param for_api:
		:return:
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user or for_api:
			return []
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'path ' + path + ', user ' + str(user))
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'path ' + path + ', user ' + str(user))
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'path ' + path + ', user ' + str(user))

		url = UrlManager(application_url, slug, for_api).get_url(path)

		expr = re.search(re.compile(r"discuss/?[a-zA-Z0-9,-]*"), url)
		if expr:
			group0 = expr.group(0)
			if group0 and url.endswith(group0):
				self.del_breadcrumbs_of_user(transaction, user)

		db_already_in = DBDiscussionSession.query(History).filter_by(url=url).first()
		if db_already_in:
			DBDiscussionSession.query(History).filter(and_(History.author_uid == db_user.uid, History.uid > db_already_in.uid)).delete()
		else:
			DBDiscussionSession.add(History(user=db_user.uid, url=url, session_id=session_id))
		transaction.commit()

		return self.get_breadcrumbs(user, lang)

	def get_breadcrumbs(self, user, lang):
		"""

		:param user:
		:param lang:
		:return:
		"""
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'user ' + str(user))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			return dict()

		db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()
		logger('BreadcrumbHelper', 'get_breadcrumbs', str(len(db_history)))
		logger('BreadcrumbHelper', 'get_breadcrumbs', str(len(db_history)))
		logger('BreadcrumbHelper', 'get_breadcrumbs', str(len(db_history)))

		if not db_history:
			return dict()

		breadcrumbs = []
		for index, history in enumerate(db_history):
			hist = dict()
			hist['index']       = str(index)
			hist['url']         = str(history.url)
			hist['text']        = self.__get_text_for_url__(history.url, lang)
			hist['shorttext']   = hist['text'][0:30] + '...' if len(hist['text']) > 35 else hist['text']
			breadcrumbs.append(hist)

		return breadcrumbs

	def __get_text_for_url__(self, url, lang):
		"""

		:param url:
		:param lang:
		:return:
		"""
		_t = Translator(lang)
		_qh = QueryHelper()

		if '/reaction/' in url:
			splitted = url.split('/')
			uid  = splitted[6]
			text = _qh.get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]

			# for index, s in enumerate(splitted):
			#   logger('-',str(index), s)

			return _t.get(_t.otherParticipantDisagree) + ' ' + text + '.'

		elif '/justify/' in url:
			splitted = url.split('/')
			uid  = splitted[6]
			text = _qh.get_text_for_statement_uid(uid) if len(splitted) == 8 else _qh.get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]
			# 7 choose action for start statemens
			# 8 choose justification for a relation
			hold = _t.get(_t.hold) if '/t' in url else _t.get(_t.doesNotHold)
			return ((_t.get(_t.breadcrumbsJustifyStatement) + ' ' + text + ' ' + hold + '?'))\
				if len(splitted) == 8 else\
				(_t.get(_t.breadcrumbsReplyForResponseOfConfrontation) + ' ' + text)

		elif '/attitude/' in url:
			uid  = url[url.rfind('/') + 1:]
			text = _qh.get_text_for_statement_uid(uid)
			text = text[0:1].lower() + text[1:]
			return _t.get(_t.whatDoYouThinkAbout) + ' ' + text + '?'

		elif '/choose/' in url:
			splitted = url.split('/')
			uid = splitted[8]
			if splitted[6] == 't': # is argument
				arg = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
				text = _qh.get_text_for_statement_uid(arg.conclusion_uid) if arg.argument_uid == 0 else _qh.get_text_for_argument_uid(arg.argument_uid, lang)
			else:
				text = _qh.get_text_for_statement_uid(uid)
			return _t.get(_t.breadcrumbsChoose) + ' ' + text[0:1].lower() + text[1:]

		else:
			slug = url[url.index('/d/') + 3:] if '/d/' in url else None
			if slug:
				issues = DBDiscussionSession.query(Issue).all()
				for issue in issues:
					if slugify(issue.title) == slug:
						slug = issue.title
						break
			return slug if slug else _t.get(_t.breadcrumbsStart)

	def del_breadcrumbs_of_user(self, transaction, user):
		"""
		Deletes the complete breadcrumbs of given user
		:param transaction: current transaction
		:param user: current user
		:return: undefined
		"""
		# maybe we are anonymous
		if user:
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			logger('BreadcrumbHelper', 'del_breadcrumbs_of_user', 'user ' + str(db_user.uid))
			DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).delete()
			transaction.commit()
