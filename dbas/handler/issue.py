"""
Provides helping function for issues.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from math import ceil

import arrow
import transaction
from slugify import slugify
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.database.discussion_model import Argument, User, Issue, Language, Statement, sql_timestamp_pretty_print, \
    ClickedStatement
from dbas.handler import user
from dbas.handler.language import get_language_from_header
from dbas.helper.query import get_short_url
from dbas.lib import is_user_author_or_admin
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_issues_as_query, get_visible_issues_for_user_as_query
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager

limit_for_open_issues = 10


def set_issue(nickname, info, long_info, title, lang, is_public, is_read_only, application_url, ui_locales) -> dict:
    """
    Sets new issue, which will be a new discussion

    :param nickname: Users nickname
    :param info: Short information about the new issue
    :param long_info: Long information about the new issue
    :param title: Title of the new issue
    :param lang: Language of the new issue
    :param application_url: Url of the app itself
    :param is_public: Boolean
    :param is_read_only: Boolean
    :param ui_locales: Current language
    :rtype: dict
    :return: Collection with information about the new issue
    """
    user.update_last_action(nickname)

    logger('setter', 'set_new_issue', 'main')
    prepared_dict = dict()

    was_set, error = __set_issue(info, long_info, title, lang, is_public, is_read_only, nickname, ui_locales)
    if was_set:
        db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
                                                                Issue.info == info)).first()
        prepared_dict['issue'] = get_issue_dict_for(db_issue, application_url, False, 0, ui_locales)
    prepared_dict['error'] = '' if was_set else error

    return prepared_dict


def __set_issue(info, long_info, title, lang, is_public, is_read_only, nickname, ui_locales):
    """
    Inserts new issue into database

    :param info: String
    :param title: String
    :param lang: String
    :param nickname: User.nickname
    :param is_public: Boolean
    :param is_read_only: Boolean
    :param ui_locales: ui_locales
    :return: True, '' on success, False, String on error
    """

    _tn = Translator(ui_locales)

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not is_user_author_or_admin(nickname):
        logger('IssueHelper', 'set_issue', 'User has no rights', error=True)
        return False, _tn.get(_.noRights)

    if len(info) < 10 or len(long_info) < 10:
        logger('IssueHelper', 'set_issue', 'Short text', error=True)
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = _tn.get(_.eachStatement)
        error = '{} ({}: {} {})'.format(a, b, str(10), c)
        return False, error

    db_duplicates1 = DBDiscussionSession.query(Issue).filter_by(title=title).all()
    db_duplicates2 = DBDiscussionSession.query(Issue).filter_by(info=info).all()
    db_duplicates3 = DBDiscussionSession.query(Issue).filter_by(long_info=long_info).all()
    if db_duplicates1 or db_duplicates2 or db_duplicates3:
        logger('IssueHelper', 'set_issue', 'Duplicates', error=True)
        return False, _tn.get(_.duplicate)

    db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=lang).first()
    if not db_lang:
        logger('IssueHelper', 'set_issue', 'No language', error=True)
        return False, _tn.get(_.internalError)

    DBDiscussionSession.add(Issue(title=title,
                                  info=info,
                                  long_info=long_info,
                                  author_uid=db_user.uid,
                                  is_read_only=is_read_only,
                                  is_private=not is_public,
                                  lang_uid=db_lang.uid))
    DBDiscussionSession.flush()

    transaction.commit()

    return True, ''


def prepare_json_of_issue(uid, application_url, lang, for_api, nickname):
    """
    Prepares slug, info, argument count and the date of the issue as dict

    :param uid: Issue.uid
    :param application_url: application_url
    :param lang: ui_locales
    :param for_api: Boolean
    :param nickname: Nickname of current user
    :return: Issue-dict()
    """
    logger('issueHelper', 'prepare_json_of_issue', 'main')
    db_issue = DBDiscussionSession.query(Issue).get(uid)

    slug = slugify(db_issue.title) if db_issue else 'none'
    title = db_issue.title if db_issue else 'none'
    info = db_issue.info if db_issue else 'none'
    long_info = db_issue.long_info if db_issue else 'none'
    stat_count = get_number_of_statements(uid)
    date_pretty = sql_timestamp_pretty_print(db_issue.date, lang) if db_issue else 'none'
    duration = (arrow.utcnow() - db_issue.date) if db_issue else 0
    days, seconds = (duration.days, duration.seconds) if db_issue else (0, 0)
    duration = ceil(days * 24 + seconds / 3600)
    date_ms = int(db_issue.date.format('X') if db_issue else arrow.utcnow().format('X')) * 1000
    date = db_issue.date.format('DD.MM. HH:mm') if db_issue else 'none'

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname if nickname else nick_of_anonymous_user).first()
    db_issues = get_visible_issues_for_user_as_query(db_user.uid).all()
    all_array = []
    for issue in db_issues:
        issue_dict = get_issue_dict_for(issue, application_url, for_api, uid, lang)
        all_array.append(issue_dict)

    _t = Translator(lang)
    t1 = _t.get(_.discussionInfoTooltip1)
    t2 = _t.get(_.discussionInfoTooltip2)
    t3 = _t.get(_.discussionInfoTooltip3sg if stat_count == 1 else _.discussionInfoTooltip3pl)
    tooltip = '{} {} {} {} {}'.format(t1, date, t2, stat_count, t3)

    return {
        'slug': slug,
        'info': info,
        'long_info': long_info,
        'title': title,
        'uid': uid,
        'stat_count': stat_count,
        'date': date,
        'date_ms': date_ms,
        'date_pretty': date_pretty,
        'all': all_array,
        'tooltip': tooltip,
        'intro': _t.get(_.currentDiscussion),
        'duration': duration,
        'read_only': db_issue.is_read_only
    }


def get_number_of_arguments(issue_uid):
    """
    Returns number of arguments for the issue

    :param issue_uid: Issue Issue.uid
    :return: Integer
    """
    return len(DBDiscussionSession.query(Argument).filter_by(issue_uid=issue_uid).all())


def get_number_of_statements(issue_uid):
    """
    Returns number of statements for the issue

    :param issue_uid: Issue Issue.uid
    :return: Integer
    """
    return len(DBDiscussionSession.query(Statement).filter_by(issue_uid=issue_uid).all())


def get_issue_dict_for(issue, application_url, for_api, uid, lang):
    """
    Creates an dictionary for the issue

    :param issue: Issue
    :param application_url:
    :param for_api: Boolean
    :param uid: current selected Issue.uid
    :param lang: ui_locales
    :return: dict()
    """
    if str(type(issue)) != str(Issue):
        return {'uid': '', 'slug': '', 'title': '', 'url': '', 'review_url': '', 'info': '', 'stat_count': '',
                'date': '', 'author': '', 'author_url': '', 'enabled': '', 'error': 'true'}

    _um = UrlManager(application_url, issue.slug, for_api)
    issue_dict = dict()
    issue_dict['uid'] = str(issue.uid)
    issue_dict['slug'] = issue.slug
    issue_dict['title'] = issue.title
    issue_dict['url'] = _um.get_slug_url(False) if str(uid) != str(issue.uid) else ''
    issue_dict['review_url'] = _um.get_review_url(False) if str(uid) != str(issue.uid) else ''
    issue_dict['info'] = issue.info
    issue_dict['stat_count'] = get_number_of_statements(issue.uid)
    issue_dict['date'] = sql_timestamp_pretty_print(issue.date, lang)
    issue_dict['author'] = issue.users.public_nickname
    issue_dict['error'] = ''
    issue_dict['author_url'] = '{}/user/{}'.format(application_url, issue.users.public_nickname)
    issue_dict['enabled'] = 'disabled' if str(uid) == str(issue.uid) else 'enabled'
    return issue_dict


def get_id_of_slug(slug, request, save_id_in_session, for_api=False):
    """
    Returns the uid

    :param slug: slug
    :param request: self.request for a fallback
    :param save_id_in_session: Boolean
    :return: uid
    """
    logger('IssueHelper', 'get_id_of_slug', 'slug: {}'.format(slug))
    db_issues = get_not_disabled_issues_as_query().all()
    for issue in db_issues:
        if str(issue.slug) == str(slug):
            if save_id_in_session:
                request.session['issue'] = issue.uid
            return issue.uid
    return -1 if for_api else get_issue_id(request)


def get_issue_id(request):
    """
    Returns issue uid saved in request. If there is no uid, we will choose an
    issue based on the language from the requests header

    :param request: self.request
    :return: uid
    """
    logger('IssueHelper', 'get_issue_id', 'def')
    # first matchdict, then params, then session
    issue_uid = request.matchdict['issue'] if 'issue' in request.matchdict \
        else request.params['issue'] if 'issue' in request.params \
        else request.session['issue'] if 'issue' in request.session \
        else None

    # no issue found
    if not issue_uid:
        logger('IssueHelper', 'get_issue_id', 'no saved issue found')
        ui_locales = get_language_from_header(request)
        db_issues = get_not_disabled_issues_as_query()
        db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
        db_issue = db_issues.filter_by(lang_uid=db_lang.uid).first()
        if not db_issue:
            db_issue = db_issues.first()
        issue_uid = db_issue.uid

    # save issue in session
    request.session['issue'] = issue_uid

    return issue_uid


def get_title_for_slug(slug):
    """
    Returns the issues title for a given slug

    :param slug: String
    :return: String
    """
    db_issues = DBDiscussionSession.query(Issue).all()
    for issue in db_issues:
        if str(slugify(issue.title)) == str(slug):
            return issue.title
    return None


def get_issues_overiew(nickname, application_url) -> dict:
    """
    Returns dictionary with keywords 'user' and 'others', which got lists with dicts with infos

    :param nickname: Users.nickname
    :param application_url: current applications url
    :return: dict
    """
    logger('IssueHelper', 'get_issues_overiew', 'def')
    user.update_last_action(nickname)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return {
            'user': [],
            'other': []
        }

    is_admin = user.is_admin(nickname)
    if is_admin:
        db_issues_other_users = DBDiscussionSession.query(Issue).filter(Issue.author_uid != db_user.uid).all()
    else:
        db_issues_other_users = get_visible_issues_for_user_as_query(db_user.uid).filter(Issue.author_uid != db_user.uid).all()

    db_issues_of_user = DBDiscussionSession.query(Issue).filter_by(author_uid=db_user.uid).all()

    return {
        'user': [__create_issue_dict(issue, application_url) for issue in db_issues_of_user],
        'other': [__create_issue_dict(issue, application_url) for issue in db_issues_other_users]
    }


def set_discussions_properties(nickname, uid, checked, key, translator) -> dict:
    """

    :param nickname:
    :param uid:
    :param checked:
    :param key:
    :param translator:
    :return:
    """
    logger('IssueHelper', 'set_discussions_properties', 'uid: {}, key: {}, checked: {}'.format(uid, key, checked))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return {'error': translator.get(_.userNotFound)}

    db_issue = DBDiscussionSession.query(Issue).get(uid)
    if not db_issue:
        return {'error': translator.get(_.internalKeyError)}

    if db_issue.author_uid != db_user.uid and not user.is_admin(nickname):
        return {'error': translator.get(_.noRights)}

    if key == 'enable':
        db_issue.set_disable(not checked)
    elif key == 'public':
        db_issue.set_private(not checked)
    elif key == 'writable':
        db_issue.set_read_only(not checked)
    else:
        return {'error': translator.get(_.internalKeyError)}

    DBDiscussionSession.add(db_issue)
    DBDiscussionSession.flush()
    transaction.commit()

    return {'error': ''}


def __create_issue_dict(issue, application_url) -> dict:
    """
    Returns dictionary with several informationa bout the given issue

    :param issue: database row of issue
    :param application_url: current applications url
    :return: dict()
    """
    short_url_dict = get_short_url(application_url + '/' + issue.slug, '', 'en')
    url = short_url_dict['url'] if len(short_url_dict['error']) == 0 else application_url + '/' + issue.slug

    # we do nto have to check for clicked arguments, cause arguments consist out of statements
    statements = [s.uid for s in DBDiscussionSession.query(Statement).filter_by(issue_uid=issue.uid).all()]
    db_clicked_statements = DBDiscussionSession.query(ClickedStatement).filter(
        ClickedStatement.statement_uid.in_(statements)).all()
    authors_clicked_statement = [click.author_uid for click in db_clicked_statements]
    db_authors = DBDiscussionSession.query(User).filter(User.uid.in_(authors_clicked_statement)).all()
    involved_users = str(len(db_authors))

    prepared_dict = {
        'uid': issue.uid,
        'title': issue.title,
        'url': application_url + '/' + issue.slug,
        'short_url': url,
        'date': issue.date.format('DD.MM. HH:mm'),
        'count_of_statements': str(get_number_of_statements(issue.uid)),
        'is_enabled': not issue.is_disabled,
        'is_public': not issue.is_private,
        'is_writable': not issue.is_read_only,
        'involved_users': involved_users,
        'lang': DBDiscussionSession.query(Language).get(issue.lang_uid).ui_locales,
        'toggle_on': "<i class='fa fa-check'></i>",
        'toggle_off': "<i class='fa fa-times'></i>",
    }
    return prepared_dict
