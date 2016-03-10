import collections
import re
from sqlalchemy import and_, func
from slugify import slugify

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, Breadcrumb, Issue, History
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
		:param delete_duplicates:
		:param for_api:
		:return: all breadcrumbs, boolean (if a crumb was inserted)
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			user = 'anonymous'
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if not db_user:
				return [], False

		if path.startswith('/'):
			path = path[1:]
			
		logger('BreadcrumbHelper', 'save_breadcrumb', 'path ' + path + ', user ' + str(user), debug=True)

		url = UrlManager(application_url, slug, for_api).get_url(path)

		# delete by slugs (dbas version)
		expr_dbas = re.search(re.compile(r"discuss/?[a-zA-Z0-9,-]*"), url)
		if expr_dbas:
			group0 = expr_dbas.group(0)
			if group0 and url.endswith(group0):
				self.del_breadcrumbs_of_user(transaction, user, session_id)

		# delete by slugs (api version)
		expr_api = re.search(re.compile(r"api/[a-zA-Z0-9,-]*"), path)
		if expr_api:
			group1 = expr_api.group(0)
			if group1 and url.endswith(group1):
				self.del_breadcrumbs_of_user(transaction, user, session_id)

		db_already_in = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.url == url,
		                                                                  Breadcrumb.author_uid == db_user.uid)).first()
		db_last = DBDiscussionSession.query(Breadcrumb).order_by(Breadcrumb.uid.desc()).first()
		already_last = db_last.url == db_already_in.url if db_already_in and db_last else False
		is_new_crumb = False

		if db_already_in:
			if user == 'anonymous':
				DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
				                                                  Breadcrumb.uid > db_already_in.uid,
				                                                  Breadcrumb.session_id == session_id)).delete()
			else:
				DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
				                                                  Breadcrumb.uid > db_already_in.uid)).delete()
		elif not already_last:
			DBDiscussionSession.add(Breadcrumb(user=db_user.uid, url=url, session_id=session_id))
			is_new_crumb = True
		transaction.commit()

		return self.get_breadcrumbs(user, session_id, lang), is_new_crumb

	def get_breadcrumbs(self, user, session_id, lang):
		"""

		:param user:
		:param session_id:
		:param lang:
		:return:
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			return dict()

		if user == 'anonymous':
			db_breadcrumbs = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                                   Breadcrumb.session_id == session_id)).all()
		else:
			db_breadcrumbs = DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid).all()

		logger('BreadcrumbHelper', 'get_breadcrumbs', 'user ' + str(user) + ', count ' + str(len(db_breadcrumbs)))

		if not db_breadcrumbs:
			return dict()

		breadcrumbs = []
		for index, crumb in enumerate(db_breadcrumbs):
			try:
				url_text = self.__get_text_for_url__(crumb.url, lang)
			except:
				logger('BreadcrumbHelper', 'get_breadcrumbs', 'error on getting text for ' + crumb.url, error=True)
				return dict()
			
			hist = dict()
			hist['index']       = str(index)
			hist['uid']         = crumb.uid
			hist['url']         = str(crumb.url) + '?breadcrumb=true'  # add this for deleting traces
			hist['text']        = url_text
			hist['shorttext']   = hist['text'][0:30] + '...' if len(hist['text']) > 35 else hist['text']
			breadcrumbs.append(hist)

		return breadcrumbs

	def get_last_breadcrumb_of_user(self, user):
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			return None
		return DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid).order_by(Breadcrumb.uid.desc()).first()

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
			if len(splitted) == 8:
				return _t.get(_t.breadcrumbsJustifyStatement) + ' ' + text + ' ' + _t.get(_t.hold)  + '?'
			else:
				return _t.get(_t.breadcrumbsReplyForResponseOfConfrontation) + ' ' + text

		elif '/attitude/' in url:
			uid  = url[url.rfind('/') + 1:]
			text = _qh.get_text_for_statement_uid(uid)
			text = text[0:1].lower() + text[1:]
			return _t.get(_t.whatDoYouThinkAbout) + ' ' + text + '?'

		elif '/choose/' in url:
			splitted = url.split('/')
			uid = splitted[8]
			if splitted[6] == 't':  # is argument
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

	def del_breadcrumbs_of_user(self, transaction, user, session_id=0):
		"""
		Deletes the complete breadcrumbs of given user
		:param transaction: current transaction
		:param user: current user
		:param session_id: current session id
		:return: undefined
		"""
		# maybe we are anonymous
		if user:
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			logger('BreadcrumbHelper', 'del_breadcrumbs_of_user', 'user ' + str(db_user.uid))
			if user == 'anonymous':
				DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
				                                                  Breadcrumb.session_id == session_id)).delete()
			else:
				DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid).delete()
				DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).delete()
			transaction.commit()
