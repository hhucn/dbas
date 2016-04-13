"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import collections
from datetime import datetime

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import User
from dbas.database.news_model import News
from dbas.logger import logger


class NewsHandler:
	"""
	Setting and getting news
	"""

	@staticmethod
	def set_news(transaction, title, text, user):
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

	@staticmethod
	def get_news():
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
