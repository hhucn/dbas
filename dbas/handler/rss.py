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

rss_path = '/static/rss'


def create_news_rss(main_page: str, ui_locale: str) -> bool:
    """
    Creates a new news rss

    :param main_page: Host URL
    :param ui_locale: Language.ui_locale
    :return: Boolean
    """
    logger('RSS-Handler', 'create_news_rss', 'def')
    db_news = DBDiscussionSession.query(News).order_by(News.date.desc()).all()
    items = [__get_rss_item(n.title, n.news, n.date.datetime, n.author, '{}/news'.format(get_global_url())) for n in
             db_news]

    _tn = Translator(ui_locale)
    rss = PyRSS2Gen.RSS2(
        title='D-BAS Feed',
        link=main_page + '{}/rss.xml'.format(rss_path),
        description=_tn.get(_.latestNewsFromDBAS),
        lastBuildDate=datetime.now(),
        items=items
    )

    if not os.path.exists('dbas{}').format(rss_path):
        os.makedirs('dbas{}').format(rss_path)

    rss.write_xml(open('dbas{}/news.xml'.format(rss_path), 'w'), encoding='utf-8')

    return True


def create_initial_issue_rss(main_page: str, ui_locale: str) -> bool:
    """
    Creates the initial RSS entry for an issue

    :param main_page: Host URL
    :param ui_locale: Language.ui_locale
    :return: Boolean
    """
    logger('RSS-Handler', 'create_initial_issue_rss', 'def')

    if not os.path.exists('dbas{}').format(rss_path):
        os.makedirs('dbas{}').format(rss_path)

    db_issues = DBDiscussionSession.query(Issue).all()
    db_authors = {u.uid: u for u in DBDiscussionSession.query(User).all()}
    for issue in db_issues:
        db_rss = DBDiscussionSession.query(RSS).filter_by(issue_uid=issue.uid).all()
        db_rss = [rss for rss in db_rss if rss.author_uid in db_authors.keys()]

        items = [__get_rss_item(rss.title, rss.description, arrow.utcnow().datetime,
                                db_authors.get(rss.author_uid).get_global_nickname(),
                                '{}/{}'.format(get_global_url(), issue.slug)) for rss in db_rss]

        rss = __get_rss2gen(main_page, issue, items, ui_locale)

        rss.write_xml(open('dbas{}/{}.xml'.format(rss_path, issue.slug) + '.xml', 'w'), encoding='utf-8')

    return True


def append_action_to_issue_rss(issue_uid: int, author_uid: int, title: str, description: str, ui_locale: str,
                               url: str) -> bool:
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
        tmp = __get_rss_item(rss.title, rss.description, rss.timestamp.datetime, db_author.get_global_nickname(), url)
        items.append(tmp)

    rss = __get_rss2gen(get_global_url(), db_issue, items, ui_locale)

    if not os.path.exists('dbas{}').format(rss_path):
        os.makedirs('dbas{}').format(rss_path)

    rss.write_xml(open('dbas{}/{}.xml'.format(rss_path, db_issue.slug) + '.xml', 'w'), encoding='utf-8')

    return True


def get_list_of_all_feeds(ui_locale: str) -> list:
    """
    Returns list of all feeds

    :param ui_locale: Language.ui_locale
    :return: list
    """
    logger('RSS-Handler', 'get_list_of_all_feeds', 'def with ' + str(ui_locale))

    feeds = []
    feed = {
        'title': 'News',
        'description': 'Latest news about D-BAS, the Dialog-Based Argumentation System',
        'link': '{}/news.xml'.format(rss_path)
    }
    feeds.append(feed)

    _tn = Translator(ui_locale)
    db_issues = DBDiscussionSession.query(Issue).all()
    for issue in db_issues:
        feed = {
            'title': issue.title,
            'description': '{}: <em> {} - {} </em>'.format(_tn.get(_.latestNewsFromDiscussion), issue.title,
                                                           issue.info),
            'link': '{}/{}.xml'.format(rss_path, issue.slug)
        }
        feeds.append(feed)

    return feeds


def __get_rss2gen(main_page: str, issue: Issue, items: list, ui_locale: str) -> PyRSS2Gen.RSS2:
    """
    Creates RSS object

    :param main_page: Host URL
    :param issue: Issue
    :param items: list of PyRSS2Gen.RSSItem
    :param ui_locale: Language.ui_locale
    :return: PyRSS2Gen.RSS2
    """
    _tn = Translator(ui_locale)
    return PyRSS2Gen.RSS2(
        title='D-BAS Feed',
        link='{}{}/{}.xml'.format(main_page, rss_path, issue.slug),
        description='{}: {} - {}'.format(_tn.get(_.latestNewsFromDiscussion), issue.title, issue.info),
        lastBuildDate=datetime.now(),
        items=items
    )


def __get_rss_item(title: str, description: str, pubdate: datetime, author: str, link: str) -> PyRSS2Gen.RSSItem:
    """
    Creates an RSS item

    :param title: title of the rss item
    :param description: description of the rss item
    :param pubdate: pubdate of the rss item
    :param author: author of the rss item
    :param link: link of the rss item
    :return: PyRSS2Gen.RSSItem
    """
    return PyRSS2Gen.RSSItem(
        title=title,
        description=description,
        pubDate=pubdate,
        author=author,
        link=link
    )
