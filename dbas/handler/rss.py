"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import PyRSS2Gen

from datetime import datetime
from dbas.database import DBNewsSession
from dbas.database.news_model import News


def create_rss(main_page):
    db_news = DBNewsSession.query(News).order_by(News.date.desc()).all()
    items = []
    for news in db_news:
        items.append(PyRSS2Gen.RSSItem(
            title=news.title,
            description=news.news,
            pubDate=news.date.datetime,
            author=news.author
        ))

    rss = PyRSS2Gen.RSS2(
        title='D-BAS Feed',
        link=main_page + '/static/rss.xml',
        description='The latest news about D-BAS, a Dialog-Based Argumentation System',
        lastBuildDate=datetime.now(),
        items=items
    )

    rss.write_xml(open('dbas/static/rss.xml', 'w'))
