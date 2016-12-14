"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
import arrow

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import User, sql_timestamp_pretty_print
from dbas.database.news_model import News
from dbas.logger import logger
from dbas.user_management import is_user_in_group
from dbas.handler.rss import create_rss


def set_news(title, text, user, lang, main_page):
    """
    Sets a new news into the news table

    :param title: news title
    :param text: String news text
    :param user: User.nickname request.authenticated_userid
    :param lang: lang
    :return: dictionary {title,date,author,news}
    """
    logger('QueryHelper', 'set_news', 'def')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

    if not db_user or is_user_in_group(user, 'author'):
        return {}, False

    author = db_user.firstname
    if db_user.firstname != 'admin':
        author += db_user.surname
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
    return_dict['status'] = '1' if db_news is not None else '_'
    return_dict['title'] = title
    return_dict['date'] = sql_timestamp_pretty_print(date, lang, False)
    return_dict['author'] = author
    return_dict['news'] = text
    transaction.commit()

    create_rss(main_page)

    return return_dict, True


def get_news(ui_locales):
    """
    Returns all news in an array, sorted by date

    :return: dict()
    """
    logger('QueryHelper', 'get_news', 'main')
    db_news = DBNewsSession.query(News).order_by(News.date.desc()).all()
    ret_news = []
    for index, news in enumerate(db_news):
        news_dict = dict()
        news_dict['title'] = news.title
        news_dict['author'] = news.author
        news_dict['date'] = sql_timestamp_pretty_print(news.date, ui_locales, False)
        news_dict['news'] = news.news
        news_dict['uid'] = 'news_' + str(news.uid)
        ret_news.append(news_dict)

    return ret_news
