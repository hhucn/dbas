import collections
from sqlalchemy import and_

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, User, TextVersion, History
from .logger import logger
from .strings import Translator
from .query_helper import QueryHelper, UrlManager

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class BreadcrumbHelper(object):

	def save_breadcrumb(self, path, user, slug, session_id, transaction, lang):
		"""

		:param path:
		:param user:
		:param slug:
		:param session_id:
		:return:
		"""
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'path ' + path + ', user ' + str(user))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
		if not db_user:
			return []

		url = UrlManager(slug).get_url(path)

		db_already_in = DBDiscussionSession.query(History).filter_by(url=url).first()
		if db_already_in:
			DBDiscussionSession.query(History).filter(and_(History.author_uid==db_user.uid, History.uid>db_already_in.uid)).delete()
		else:
			DBDiscussionSession.add(History(user=db_user.uid, url=url, session_id=session_id))
		transaction.commit()

		return self.get_breadcrumbs(user, lang)

	def get_breadcrumbs(self, user, lang):
		"""

		:param user:
		:return:
		"""
		logger('BreadcrumbHelper', 'get_breadcrumbs', 'user ' + str(user))
		db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

		if not db_user:
			logger('BreadcrumbHelper', 'get_breadcrumbs', 'no user')
			return dict()

		db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()

		if not db_history:
			logger('BreadcrumbHelper', 'get_breadcrumbs', 'no track')
			return dict()

		breadcrumbs = []
		for index, history in enumerate(db_history):
			hist = dict()
			hist['index']   = str(index)
			hist['url']     = str(history.url)
			hist['text']    = self.__get_text_for_url__(history.url, lang)
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

		if '/r/' in url:
			splitted = url.split('/')
			uid = splitted[len(splitted)-3]
			conf = splitted[len(splitted)-1]
			text = _qh.get_text_for_argument_uid(uid, lang)
			text = text[0:1].lower() + text[1:]
			return _t.get(_t.otherParticipantDisagree) + ' ' + text + '.'

		elif '/j/' in url:
			splitted = url.split('/')
			supportive = splitted[len(splitted)-1] == 't'
			uid = splitted[len(splitted)-2]
			text = _qh.get_text_for_statement_uid(uid)
			text = text[0:1].lower() + text[1:]
			return _t.get(_t.whyDoYouThinkThat) + ' ' + text + ' ' + (_t.get(_t.isTrue) if supportive else _t.get(_t.isFalse)) + '?'

		elif '/a/' in url:
			uid = url[url.rfind('/')+1:]
			text = _qh.get_text_for_statement_uid(uid)
			text = text[0:1].lower() + text[1:]
			return _t.get(_t.whatDoYouThinkAbout) + ' ' + text + '?'

		else:
			return url[url.index('/d/')+3:] if '/d/' in url else 'Start'

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
			logger('BreadcrumbHelper', 'del_breadcrumbs_of_user','user ' + str(db_user.uid))
			DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).delete()
			transaction.commit()