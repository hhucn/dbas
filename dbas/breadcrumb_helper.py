import re
from sqlalchemy import and_
from slugify import slugify

from .database import DBDiscussionSession
from .database.discussion_model import Argument, User, Breadcrumb, Issue, Bubble
from .logger import logger
from .strings import Translator
from .query_helper import QueryHelper

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class BreadcrumbHelper(object):

	def save_breadcrumb(self, path, user, session_id, transaction, lang):
		"""

		:param path:
		:param user:
		:param session_id:
		:param transaction:
		:param lang:

		:return: all breadcrumbs, boolean (if a crumb was inserted)
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			user = 'anonymous'
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if not db_user:
				return [], False
		logger('BreadcrumbHelper', 'save_breadcrumb', 'path: ' + path + ', user ' + user)

		# delete by slugs (dbas version)
		expr_dbas = re.search(re.compile(r"/?discuss/?[a-zA-Z0-9,-]*"), path)
		if expr_dbas:
			group0 = expr_dbas.group(0)
			if group0 and path.endswith(group0):
				self.del_breadcrumbs_of_user(transaction, user, session_id)

		# delete by slugs (api version)
		expr_api = re.search(re.compile(r"/?api/[a-zA-Z0-9,-]*"), path)
		if expr_api:
			group1 = expr_api.group(0)
			if group1 and path.endswith(group1):
				self.del_breadcrumbs_of_user(transaction, user, session_id)

		db_already_in = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.url == path,
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
			DBDiscussionSession.add(Breadcrumb(user=db_user.uid, url=path, session_id=session_id))
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
			logger('BreadcrumbHelper', 'get_breadcrumbs', 'user ' + str(db_user.uid) + ', session_id ' + session_id + ', count ' + str(len(db_breadcrumbs)))
		else:
			db_breadcrumbs = DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid).all()
			logger('BreadcrumbHelper', 'get_breadcrumbs', 'user ' + str(db_user.uid) + ', count ' + str(len(db_breadcrumbs)))

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
			hist['url']         = str(crumb.url)
			hist['text']        = url_text
			breadcrumbs.append(hist)

		return breadcrumbs

	@staticmethod
	def __get_text_for_url__(url, lang):
		"""

		:param url:
		:param lang:
		:return:
		"""
		_t = Translator(lang)
		_qh = QueryHelper()

		if '/reaction/' in url:
			splitted = url.split('/')
			uid  = splitted[4]
			text = _qh.get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]

			# for index, s in enumerate(splitted):
			#   logger('-',str(index), s)

			return _t.get(_t.otherParticipantDisagree) + ' ' + text + '.'

		elif '/justify/' in url:
			splitted = url.split('/')
			uid  = splitted[4]
			text = _qh.get_text_for_statement_uid(uid) if len(splitted) == 6 else _qh.get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]
			# 5 choose action for start statemens
			# 6 choose justification for a relation
			if len(splitted) == 6:
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
			uid = splitted[6]
			if splitted[4] == 't':  # is argument
				arg = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
				if arg.argument_uid is None:
					text = _qh.get_text_for_statement_uid(arg.conclusion_uid)
				else:
					text = _qh.get_text_for_argument_uid(arg.argument_uid, lang)
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

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if user == 'anonymous':
			logger('BreadcrumbHelper', 'del_breadcrumbs_of_user', 'user ' + str(db_user.uid) + ' with session_id ' + str(session_id))

			if DBDiscussionSession.query(Bubble).filter(and_(Bubble.author_uid == db_user.uid,
			                                                 Bubble.session_id == session_id)).all():
				DBDiscussionSession.query(Bubble).filter(and_(Bubble.author_uid == db_user.uid,
			                                                  Bubble.session_id == session_id)).delete()
			if DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                    Breadcrumb.session_id == session_id)).all():
				DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
				                                                  Breadcrumb.session_id == session_id)).delete()
		else:
			logger('BreadcrumbHelper', 'del_breadcrumbs_of_user', 'user ' + str(db_user.uid))
			if DBDiscussionSession.query(Bubble).filter_by(author_uid=db_user.uid).all():
				DBDiscussionSession.query(Bubble).filter_by(author_uid=db_user.uid).delete()
			if DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid).all():
				DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid).delete()

		transaction.commit()
