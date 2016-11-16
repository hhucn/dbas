"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
import arrow
import collections

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import User
from dbas.database.news_model import News
from dbas.logger import logger
from dbas.lib import sql_timestamp_pretty_print


def set_news(title, text, user, lang):
    """
    Sets a new news into the news table

    :param title: news title
    :param text: String news text
    :param user: User.nickname self.request.authenticated_userid
    :param lang: lang
    :return: dictionary {title,date,author,news}
    """
    logger('QueryHelper', 'set_news', 'def')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    author = db_user.firstname if db_user.firstname == 'admin' else db_user.firstname + ' ' + db_user.surname
    # now = datetime.now()
    # day = str(now.day) if now.day > 9 else ('0' + str(now.day))
    # month = str(now.month) if now.month > 9 else ('0' + str(now.month))
    # date = day + '.' + month + '.' + str(now.year)
    date = arrow.now()
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
    return_dict['date'] = sql_timestamp_pretty_print(date, lang, False)
    return_dict['author'] = author
    return_dict['news'] = text

    return return_dict


def get_news(ui_locales):
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
        news_dict['date'] = sql_timestamp_pretty_print(news.date, ui_locales, False)
        news_dict['news'] = news.news
        news_dict['uid'] = str(news.uid)
        uid = news.date.format('YYYY-MM-DD HH:mm:ss ZZ') + ' ' + str(index)
        ret_dict[uid] = news_dict

    ret_dict = collections.OrderedDict(sorted(ret_dict.items()))

    return ret_dict
