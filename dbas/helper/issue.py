"""
Provides helping function for issues.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
import arrow
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, Issue, Language, Statement, sql_timestamp_pretty_print
from dbas.lib import is_user_author_or_admin
from dbas.logger import logger
from dbas.helper.language import get_language_from_header
from dbas.query_wrapper import get_not_disabled_issues_as_query
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager
from slugify import slugify
from math import ceil


def set_issue(info, long_info, title, lang, nickname, ui_locales):
    """
    Inserts new issue into database

    :param info: String
    :param title: String
    :param lang: String
    :param nickname: User.nickname
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
                                  lang_uid=db_lang.uid))
    DBDiscussionSession.flush()

    transaction.commit()

    return True, ''


def prepare_json_of_issue(uid, application_url, lang, for_api):
    """
    Prepares slug, info, argument count and the date of the issue as dict

    :param uid: Issue.uid
    :param application_url: application_url
    :param lang: ui_locales
    :param for_api: Boolean
    :return: Issue-dict()
    """
    logger('issueHelper', 'prepare_json_of_issue', 'main')
    db_issue = DBDiscussionSession.query(Issue).get(uid)

    slug        = slugify(db_issue.title) if db_issue else 'none'
    title       = db_issue.title if db_issue else 'none'
    info        = db_issue.info if db_issue else 'none'
    long_info   = db_issue.long_info if db_issue else 'none'
    stat_count  = get_number_of_statements(uid)
    date        = sql_timestamp_pretty_print(db_issue.date, lang) if db_issue else 'none'
    duration    = (arrow.utcnow() - db_issue.date ) if db_issue else 0
    days, seconds = (duration.days, duration.seconds) if db_issue else (0, 0)
    duration    = ceil(days * 24 + seconds / 3600)

    db_issues = get_not_disabled_issues_as_query().all()
    all_array = []
    for issue in db_issues:
        issue_dict = get_issue_dict_for(issue, application_url, for_api, uid, lang)
        all_array.append(issue_dict)

    _t = Translator(lang)
    tooltip = _t.get(_.discussionInfoTooltip1) + ' ' + date + ' '
    tooltip += _t.get(_.discussionInfoTooltip2) + ' ' + str(stat_count) + ' '
    tooltip += (_t.get(_.discussionInfoTooltip3sg if stat_count == 1 else _.discussionInfoTooltip3pl))

    return {'slug': slug,
            'info': info,
            'long_info': long_info,
            'title': title,
            'uid': uid,
            'stat_count': stat_count,
            'date': date,
            'all': all_array,
            'tooltip': tooltip,
            'intro': _t.get(_.currentDiscussion),
            'duration': duration}


def get_number_of_arguments(issue):
    """
    Returns number of arguments for the issue

    :param issue: Issue Issue.uid
    :return: Integer
    """
    return len(DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all())


def get_number_of_statements(issue):
    """
    Returns number of statements for the issue

    :param issue: Issue Issue.uid
    :return: Integer
    """
    return len(DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all())


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
    _um = UrlManager(application_url, issue.get_slug(), for_api)
    issue_dict = dict()
    issue_dict['uid']               = str(issue.uid)
    issue_dict['slug']              = issue.get_slug()
    issue_dict['title']             = issue.title
    issue_dict['url']               = _um.get_slug_url(False) if str(uid) != str(issue.uid) else ''
    issue_dict['review_url']        = _um.get_review_url(False) if str(uid) != str(issue.uid) else ''
    issue_dict['info']              = issue.info
    issue_dict['stat_count']        = get_number_of_statements(issue.uid)
    issue_dict['date']              = sql_timestamp_pretty_print(issue.date, lang)
    issue_dict['author']            = issue.users.public_nickname
    issue_dict['author_url']        = application_url + '/user/' + str(issue.users.public_nickname)
    issue_dict['enabled']           = 'disabled' if str(uid) == str(issue.uid) else 'enabled'
    return issue_dict


def get_id_of_slug(slug, request, save_id_in_session):
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
        if str(slugify(issue.title)) == str(slug):
            if save_id_in_session:
                request.session['issue'] = issue.uid
            return issue.uid
    return get_issue_id(request)


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
