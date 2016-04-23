"""
Class for managing breadcrumbs of each user.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import re
from sqlalchemy import and_
from slugify import slugify

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, Breadcrumb, Issue, Bubble
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid
from dbas.logger import logger
from dbas.strings import Translator


class BreadcrumbHelper:
	"""
	Managing breadcrumbs
	"""

	@staticmethod
	def save_breadcrumb(path, user, session_id, transaction, lang):
		"""
		Saves curren path as breadcrumb for the user

		:param path: request.past
		:param user: User.nickname
		:param session_id: request.session_id
		:param transaction: transaction
		:param lang: ui_locales
		:return: all breadcrumbs, boolean (if a crumb was inserted)
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			user = 'anonymous'
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if not db_user:
				logger('BreadcrumbHelper', 'save_breadcrumb', 'return [], False')
				return [], False
		logger('BreadcrumbHelper', 'save_breadcrumb', 'path: ' + path + ', user ' + user)

		# delete by slugs (dbas version)
		expr_dbas = re.search(re.compile(r"/?discuss/?[a-zA-Z0-9,-]*"), path)
		if expr_dbas:
			group0 = expr_dbas.group(0)
			if group0 and path.endswith(group0):
				BreadcrumbHelper.del_all_breadcrumbs_of_user(transaction, user, session_id)

		# delete by slugs (api version)
		expr_api = re.search(re.compile(r"/?api/[a-zA-Z0-9,-]*"), path)
		if expr_api:
			group1 = expr_api.group(0)
			if group1 and path.endswith(group1):
				BreadcrumbHelper.del_all_breadcrumbs_of_user(transaction, user, session_id)

		# remove replicates (removed due to #25)
		#db_already_in = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.url == path,
		#                                                                  Breadcrumb.author_uid == db_user.uid)).first()
		#db_last = DBDiscussionSession.query(Breadcrumb).order_by(Breadcrumb.uid.desc()).first()
		#already_last = db_last.url == db_already_in.url if db_already_in and db_last else False
		#is_new_crumb = False

		#if db_already_in:
		#	BreadcrumbHelper.__delete_breadcrumbs_from_uid(db_user, db_already_in.uid, session_id)
		#elif not already_last:
		DBDiscussionSession.add(Breadcrumb(user=db_user.uid, url=path, session_id=session_id))
		is_new_crumb = True

		transaction.commit()

		return BreadcrumbHelper.get_breadcrumbs(user, session_id, lang), is_new_crumb

	@staticmethod
	def get_breadcrumbs(user, session_id, lang):
		"""
		Returns list with breadcrumbs for the given user.

		:param user: User.nickname
		:param session_id: request.session_id
		:param lang: ui_locales
		:return: Array of breadcrumb-object with the fields: index, uid, url, text
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
				url_text = BreadcrumbHelper.__get_text_for_url__(crumb.url, lang)
			except:
				logger('BreadcrumbHelper', 'get_breadcrumbs', 'error on getting text for ' + crumb.url, error=True)
				return dict()
			
			hist = dict()
			hist['index']       = str(index)
			hist['uid']         = crumb.uid
			hist['url']         = str(crumb.url)
			hist['text']        = url_text
			breadcrumbs.append(hist)

		logger('BreadcrumbHelper', 'get_breadcrumbs', 'return crumbs #' + str(len(breadcrumbs)))
		return breadcrumbs

	@staticmethod
	def del_duplicated_breacrumbs_of_user(url, user, session_id=0):
		"""
		Deletes duplicated breadcrumbs of given user

		:param url: Breadcrumb.url
		:param user: User.nickname
		:param session_id: request.session_id
		:return: undefined
		"""
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		logger('BreadcrumbHelper', 'del_duplicated_breacrumbs_of_user', '1')
		if not db_user:
			logger('BreadcrumbHelper', 'del_duplicated_breacrumbs_of_user', '2')
			user = 'anonymous'
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if not db_user:
				logger('BreadcrumbHelper', 'del_duplicated_breacrumbs_of_user', '3')
				return

		db_already_in = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.url == url,
		                                                                  Breadcrumb.author_uid == db_user.uid)).first()
		db_last = DBDiscussionSession.query(Breadcrumb).order_by(Breadcrumb.uid.desc()).first()

		if db_already_in:
			BreadcrumbHelper.__delete_breadcrumbs_from_uid(db_user, db_already_in.uid, session_id)

	@staticmethod
	def del_all_breadcrumbs_of_user(transaction, user, session_id=0):
		"""
		Deletes the complete breadcrumbs of given user

		:param transaction: transaction
		:param user: User.nickname
		:param session_id: request.session_id
		:return: undefined
		"""

		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		# BreadcrumbHelper.__delete_breadcrumbs_from_uid(db_user, 0, session_id)  # TODO
		if user == 'anonymous':
			logger('BreadcrumbHelper', 'del_all_breadcrumbs_of_user', 'user ' + str(db_user.uid) + ' with session_id ' + str(session_id))

			bubbles = DBDiscussionSession.query(Bubble).filter(and_(Bubble.author_uid == db_user.uid,
			                                                        Bubble.session_id == session_id))
			if bubbles.all():
				bubbles.delete()

			crumbs = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                           Breadcrumb.session_id == session_id))
			if crumbs.all():
				crumbs.delete()
		else:
			logger('BreadcrumbHelper', 'del_all_breadcrumbs_of_user', 'user ' + str(db_user.uid))
			bubbles = DBDiscussionSession.query(Bubble).filter_by(author_uid=db_user.uid)
			crumbs = DBDiscussionSession.query(Breadcrumb).filter_by(author_uid=db_user.uid)
			if bubbles.all():
				bubbles.delete()
			if crumbs.all():
				crumbs.delete()

		transaction.commit()

	@staticmethod
	def __get_text_for_url__(url, lang):
		"""
		Interprets the given url and returns situation-based text.

		:param url: String
		:param lang: ui_locales
		:return: String
		"""
		_t = Translator(lang)

		if '/reaction/' in url:
			splitted = url.split('/')
			uid  = splitted[4]
			text = get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]

			# for index, s in enumerate(splitted):
			#   logger('-',str(index), s)

			return _t.get(_t.otherParticipantDisagreeThat) + ' ' + text + '.'

		elif '/justify/' in url:
			splitted = url.split('/')
			uid  = splitted[4]
			text = get_text_for_statement_uid(uid) if len(splitted) == 6 else get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]
			# 5 choose action for start statemens
			# 6 choose justification for a relation
			if len(splitted) == 6:
				return _t.get(_t.breadcrumbsJustifyStatement) + ' ' + text + ' ' + _t.get(_t.hold)  + '?'
			else:
				return _t.get(_t.breadcrumbsReplyForResponseOfConfrontation) + ' ' + text

		elif '/attitude/' in url:
			uid  = url[url.rfind('/') + 1:]
			text = get_text_for_statement_uid(uid)
			text = text[0:1].lower() + text[1:]
			return _t.get(_t.whatDoYouThinkAbout) + ' ' + text + '?'

		elif '/choose/' in url:
			splitted = url.split('/')
			uid = splitted[6]
			if splitted[4] == 't':  # is argument
				arg = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
				if arg.argument_uid is None:
					text = get_text_for_statement_uid(arg.conclusion_uid)
				else:
					text = get_text_for_argument_uid(arg.argument_uid, lang)
			else:
				text = get_text_for_statement_uid(uid)
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

	@staticmethod
	def __delete_breadcrumbs_from_uid(db_user, uid, session_id):
		"""
		Deletes all breadcrumbs with uid greater than given uid

		:param db_user: User
		:param uid: Argument.uid
		:param session_id: request.session.id
		:return: undefined
		"""
		# getting all breadcrumbs for deleting
		logger('BreadcrumbHelper', '__delete_breadcrumbs_from_uid', 'user ' + str(db_user.uid) +
		       ' with session_id ' + str(session_id) +
		       ' and breadcrumbs from ' + str(uid))
		if db_user.nickname == 'anonymous':
			crumbs_for_del = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                                   Breadcrumb.uid > uid,
			                                                                   Breadcrumb.session_id == session_id)).all()
		else:
			crumbs_for_del = DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                                   Breadcrumb.uid > uid)).all()
		# delete all bubbles with fkeys for the crumbs
		for crumb in crumbs_for_del:
			DBDiscussionSession.query(Bubble).filter_by(breadcrumb_uid=crumb.uid).delete()

		# delete the breadcrumbs
		if db_user.nickname == 'anonymous':
			DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                  Breadcrumb.uid > uid,
			                                                  Breadcrumb.session_id == session_id)).delete()
		else:
			DBDiscussionSession.query(Breadcrumb).filter(and_(Breadcrumb.author_uid == db_user.uid,
			                                                  Breadcrumb.uid > uid)).delete()
