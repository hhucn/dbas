"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import arrow
import transaction

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import User, sql_timestamp_pretty_print
from dbas.database.news_model import News
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie
from dbas.handler.rss import create_news_rss
from dbas.lib import escape_string
from dbas.logger import logger


def set_news(request):
    """
    Sets a new news into the news table

    :param request: current request of the webserver
    :return: dict(), Boolean
    """
    logger('NewsHelper', 'set_news', 'def')

    title = escape_string(request.params['title']) if 'title' in request.params else None
    text = escape_string(request.params['text']) if 'text' in request.params else None
    nickname = request.authenticated_userid
    lang = get_language_from_cookie(request)
    main_page = request.application_url

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    if not db_user or user.is_in_group(nickname, 'author') or not title or not text:
        return {}, False

    author = db_user.firstname
    if db_user.firstname != 'admin':
        author += db_user.surname

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

    create_news_rss(main_page, request.registry.settings['pyramid.default_locale_name'])

    return return_dict, True


def get_news(ui_locales):
    """
    Returns all news in an array, sorted by date

    :return: dict()
    """
    logger('NewsHelper', 'get_news', 'main')
    db_news = DBNewsSession.query(News).order_by(News.date.desc()).all()
    ret_news = []
    for index, news in enumerate(db_news):
        news_dict = dict()
        news_dict['title'] = news.title
        news_dict['author'] = news.author
        news_dict['date'] = sql_timestamp_pretty_print(news.date, ui_locales, False)
        news_dict['news'] = news.news
        news_dict['title_id'] = 'news_{}_title'.format(news.uid)
        news_dict['date_id'] = 'news_{}_date'.format(news.uid)
        news_dict['author_id'] = 'news_{}_author'.format(news.uid)
        news_dict['uid'] = 'news_' + str(news.uid)
        ret_news.append(news_dict)

    return ret_news
