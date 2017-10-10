"""
Provides helping function round about the news.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import PyRSS2Gen
import arrow
import transaction
import os

from datetime import datetime
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, RSS, User, News
from dbas.lib import get_global_url
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def create_news_rss(main_page, ui_locale):
    """
    Creates a new news rss

    :param main_page: Host URL
    :param ui_locale: Language.ui_locale
    :return: Boolean
    """
    logger('RSS-Handler', 'create_news_rss', 'def')
    db_news = DBDiscussionSession.query(News).order_by(News.date.desc()).all()
    items = []
    for news in db_news:
        items.append(PyRSS2Gen.RSSItem(
            title=news.title,
            description=news.news,
            pubDate=news.date.datetime,
            author=news.author
        ))

    _tn = Translator(ui_locale)
    rss = PyRSS2Gen.RSS2(
        title='D-BAS Feed',
        link=main_page + '/static/rss/rss.xml',
        description=_tn.get(_.latestNewsFromDBAS),
        lastBuildDate=datetime.now(),
        items=items
    )

    if not os.path.exists('dbas/static/rss'):
        os.makedirs('dbas/static/rss')

    rss.write_xml(open('dbas/static/rss/news.xml', 'w'), encoding='utf-8')

    return True


def create_initial_issue_rss(main_page, ui_locale):
    """
    Creates the initial RSS entry for an issue

    :param main_page: Host URL
    :param ui_locale: Language.ui_locale
    :return: Boolean
    """
    logger('RSS-Handler', 'create_initial_issue_rss', 'def')
    db_issues = DBDiscussionSession.query(Issue).all()
    for issue in db_issues:
        db_rss = DBDiscussionSession.query(RSS).filter_by(issue_uid=issue.uid).all()
        items = []
        for rss in db_rss:
            db_author = DBDiscussionSession.query(User).get(rss.author_uid)
            if not db_author:
                continue
            items.append(PyRSS2Gen.RSSItem(
                title=rss.title,
                description=rss.description,
                pubDate=arrow.utcnow().datetime,
                author=db_author.get_global_nickname()
            ))

        rss = __get_issue_rss_gen(main_page, issue, items, ui_locale)

        if not os.path.exists('dbas/static/rss'):
            os.makedirs('dbas/static/rss')

        rss.write_xml(open('dbas/static/rss/' + issue.slug + '.xml', 'w'), encoding='utf-8')

    return True


def append_action_to_issue_rss(issue_uid, author_uid, title, description, ui_locale, url):
    """
    Appends a new action in D-BAS to the RSS

    :param issue_uid: Issue.uid
    :param author_uid: User.uid
    :param title: String
    :param description: String
    :param ui_locale: Language.ui_locale
    :param url: url of this event
    :return: Boolean
    """
    logger('RSS-Handler', 'append_action_to_issue_rss', 'issue_uid ' + str(issue_uid))
    db_issue = DBDiscussionSession.query(Issue).get(issue_uid)
    if not db_issue:
        return False

    db_author = DBDiscussionSession.query(User).get(author_uid)
    if not db_author:
        return False

    DBDiscussionSession.add(RSS(author=author_uid, issue=issue_uid, title=title, description=description))
    DBDiscussionSession.flush()
    transaction.commit()

    db_rss = DBDiscussionSession.query(RSS).filter_by(issue_uid=issue_uid).order_by(RSS.uid.desc()).all()
    items = []
    for rss in db_rss:
        db_author = DBDiscussionSession.query(User).get(rss.author_uid)
        if not db_author:
            continue
        items.append(PyRSS2Gen.RSSItem(
            title=rss.title,
            description=rss.description,
            pubDate=rss.timestamp.datetime,
            author=db_author.get_global_nickname(),
            link=url
        ))

    rss = __get_issue_rss_gen(get_global_url(), db_issue, items, ui_locale)

    if not os.path.exists('dbas/static/rss'):
        os.makedirs('dbas/static/rss')

    rss.write_xml(open('dbas/static/rss/' + db_issue.slug + '.xml', 'w'), encoding='utf-8')

    return True


def get_list_of_all_feeds(ui_locale):
    """
    Returns list of all feeds

    :param ui_locale: Language.ui_locale
    :return: list
    """
    logger('RSS-Handler', 'get_list_of_all_feeds', 'def with ' + str(ui_locale))

    feeds = []
    feed = {'title': 'News',
            'description': 'Latest news about D-BAS, a Dialog-Based Argumentation System',
            'link': '/static/rss/news.xml'}
    feeds.append(feed)

    _tn = Translator(ui_locale)
    db_issues = DBDiscussionSession.query(Issue).all()
    for issue in db_issues:
        feed = {'title': issue.title,
                'description': _tn.get(_.latestNewsFromDiscussion) + ': <em>' + issue.title + ' - ' + issue.info + '</em>',
                'link': '/static/rss/' + issue.slug + '.xml'}
        feeds.append(feed)

    return feeds


def __get_issue_rss_gen(main_page, issue, items, ui_locale):
    """
    Creates RSS object

    :param main_page: Host URL
    :param issue: Issue
    :param items: [PyRSS2Gen.RSSItem]
    :param ui_locale: Language.ui_locale
    :return: PyRSS2Gen.RSS2
    """
    _tn = Translator(ui_locale)
    return PyRSS2Gen.RSS2(
        title='D-BAS Feed',
        link=main_page + '/static/rss/' + issue.slug + '.xml',
        description=_tn.get(_.latestNewsFromDiscussion) + ': ' + issue.title + ' - ' + issue.info,
        lastBuildDate=datetime.now(),
        items=items
    )
