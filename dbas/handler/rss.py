"""
Provides functions for our rss feed.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import PyRSS2Gen
import arrow
import logging
import os
import transaction
from datetime import datetime

from dbas.database import DBDiscussionSession as Session
from dbas.database.discussion_model import Issue, RSS, User, News
from dbas.lib import get_enabled_issues_as_query, get_global_url
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)
rss_path = '/static/rss'


def create_news_rss(main_page: str, ui_locale: str) -> bool:
    """
    Creates a new news rss

    :param main_page: Host URL
    :param ui_locale: Language.ui_locale
    :return: Boolean
    """
    LOG.debug("Entering create_new_rss function")
    db_news = Session.query(News).order_by(News.date.desc()).all()
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

    if not os.path.exists('dbas{}'.format(rss_path)):
        os.makedirs('dbas{}'.format(rss_path))

    rss.write_xml(open('dbas{}/news.xml'.format(rss_path), 'w'), encoding='utf-8')

    return True


def create_initial_issue_rss(main_page: str) -> bool:
    """
    Creates the initial RSS entry for an issue

    :param main_page: Host URL
    :return: Boolean
    """
    LOG.debug("Entering create_initial_issue_rss function")

    if not os.path.exists('dbas{}'.format(rss_path)):
        os.makedirs('dbas{}'.format(rss_path))

    db_issues = get_enabled_issues_as_query().all()
    db_authors = {u.uid: u for u in Session.query(User).all()}
    for issue in db_issues:
        db_rss = Session.query(RSS).filter(RSS.issue_uid == issue.uid,
                                           RSS.author_uid.in_(db_authors.keys())).all()

        items = [__get_rss_item(rss.title, rss.description, arrow.utcnow().datetime,
                                db_authors.get(rss.author_uid).global_nickname,
                                '{}/{}'.format(get_global_url(), issue.slug)) for rss in db_rss]

        rss = __get_rss2gen(main_page, issue, items)

        rss.write_xml(open('dbas{}/{}.xml'.format(rss_path, issue.slug) + '.xml', 'w'), encoding='utf-8')

    return True


def append_action_to_issue_rss(db_issue: Issue, db_author: User, title: str, description: str, url: str) -> bool:
    """
    Appends a new action in D-BAS to the RSS

    :param db_issue: Issue
    :param db_author: User
    :param title: String
    :param description: String
    :param url: url of this event
    :return: Boolean
    """
    LOG.debug("Issue_uid: %s", db_issue.uid)
    Session.add(RSS(author=db_author.uid, issue=db_issue.uid, title=title, description=description))
    Session.flush()
    transaction.commit()

    return rewrite_issue_rss(db_issue.uid, url)


def rewrite_issue_rss(issue_uid: int, url: str):
    """
    Writes rss file for the issue

    :param issue_uid: Issue.uid
    :param url: url of this event
    :return: Boolean
    """
    # logger('RSS-Handler', 'rewrite_issue_rss', 'issue_uid ' + str(issue_uid))
    db_issue = Session.query(Issue).get(issue_uid)
    db_authors = {u.uid: u for u in Session.query(User).all()}
    db_rss = Session.query(RSS).filter(RSS.issue_uid == issue_uid,
                                       RSS.author_uid.in_(db_authors.keys())).order_by(RSS.uid.desc()).all()
    items = [__get_rss_item(r.title, r.description, r.timestamp.datetime,
                            db_authors.get(r.author_uid).global_nickname, url) for r in db_rss]

    if not os.path.exists('dbas{}'.format(rss_path)):
        os.makedirs('dbas{}'.format(rss_path))

    rss = __get_rss2gen(get_global_url(), db_issue, items)
    rss.write_xml(open('dbas{}/{}.xml'.format(rss_path, db_issue.slug), 'w'), encoding='utf-8')

    return True


def get_list_of_all_feeds(ui_locale: str) -> list:
    """
    Returns list of all feeds

    :param ui_locale: Language.ui_locale
    :return: list
    """
    LOG.debug("Enter get_list_of_all_feeds with locale %s", ui_locale)

    feeds = []
    feed = {
        'title': 'News',
        'description': 'Latest news about D-BAS, the Dialog-Based Argumentation System',
        'link': '{}/news.xml'.format(rss_path)
    }
    feeds.append(feed)

    _tn = Translator(ui_locale)
    db_issues = get_enabled_issues_as_query().all()
    for issue in db_issues:
        feed = {
            'title': issue.title,
            'description': '{}: <em> {} - {} </em>'.format(_tn.get(_.latestNewsFromDiscussion),
                                                           issue.title,
                                                           issue.info),
            'link': '{}/{}.xml'.format(rss_path, issue.slug)
        }
        feeds.append(feed)

    return feeds


def __get_rss2gen(main_page: str, issue: Issue, items: list) -> PyRSS2Gen.RSS2:
    """
    Creates RSS object

    :param main_page: Host URL
    :param issue: Issue
    :param items: list of PyRSS2Gen.RSSItem
    :return: PyRSS2Gen.RSS2
    """
    _tn = Translator(issue.lang)
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
