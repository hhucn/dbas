"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import arrow
import logging
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, News, sql_timestamp_pretty_print
from dbas.handler.rss import create_news_rss


def set_news(title: str, text: str, db_user: User, lang: str, main_page: str) -> dict():
    """
    Sets a new news into the news table

    :param title: of the news
    :param text: of the news
    :param db_user: author of the news
    :param lang: ui_locales
    :param main_page: url
    :return:
    """
    log = logging.getLogger(__name__)
    log.debug("Entering set_news function")

    author = db_user.firstname
    if db_user.firstname != 'admin':
        author += ' {}'.format(db_user.surname)

    date = arrow.now()
    DBDiscussionSession.add(News(title=title, author=author, date=arrow.now(), news=text))
    DBDiscussionSession.flush()
    transaction.commit()

    return_dict = {
        'status': 'success',
        'title': title,
        'date': sql_timestamp_pretty_print(date, lang, False),
        'author': author,
        'news': text
    }

    create_news_rss(main_page, lang)

    return return_dict


def get_news(ui_locales):
    """
    Returns all news in an array, sorted by date

    :param ui_locales:
    :return: dict()
    """
    log = logging.getLogger(__name__)
    log.debug("Entering get_news function")
    db_news = DBDiscussionSession.query(News).order_by(News.date.desc()).all()
    ret_news = []
    for news in db_news:
        news_dict = {
            'title': news.title,
            'author': news.author,
            'date': sql_timestamp_pretty_print(news.date, ui_locales, False),
            'news': news.news,
            'title_id': 'news_{}_title'.format(news.uid),
            'date_id': 'news_{}_date'.format(news.uid),
            'author_id': 'news_{}_author'.format(news.uid),
            'uid': 'news_' + str(news.uid)
        }
        ret_news.append(news_dict)

    return ret_news


def get_latest_news(ui_locales):
    """
    Returns the latest news for the carousel

    :param ui_locales:
    :return: dict()
    :return:
    """
    log = logging.getLogger(__name__)
    log.debug("Entering get_latest_news function")
    db_news = DBDiscussionSession.query(News).order_by(News.date.desc()).all()
    ret_news = []
    for index, news in enumerate(db_news[:5]):
        news_dict = {
            'indicator_class': '',
            'block_class': 'carousel-item',
            'title': news.title,
            'author': news.author,
            'date': sql_timestamp_pretty_print(news.date, ui_locales, False),
            'news': news.news,
            'id': index
        }
        ret_news.append(news_dict)
    ret_news[0]['indicator_class'] += 'active'
    ret_news[0]['block_class'] += ' active'
    return ret_news
