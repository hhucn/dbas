import logging
import re

from pyramid.httpexceptions import HTTPNotFound
from pyramid.registry import Registry
from pyramid.request import Request

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User, Statement
from dbas.handler import history as history_handler, issue as issue_handler
from dbas.handler.language import get_language_from_cookie, set_language_for_visit
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.lib import usage_of_modern_bubbles, nick_of_anonymous_user, Attitudes

LOG = logging.getLogger(__name__)
name = 'D-BAS'
version = '1.25.1'
full_version = version
project_name = name + ' ' + full_version


def modify_discussion_url(prep_dict: dict):
    """
    Adds the /discuss prefix for every url entry

    :param prep_dict:
    :return:
    """
    # modify urls for the radio buttons and urls of the bubbles
    dict_tuples = [('items', 'elements'), ('discussion', 'bubbles')]
    for (x, y) in dict_tuples:
        for i, el in enumerate(prep_dict[x][y]):
            if '/' in el.get('url', ''):
                prep_dict[x][y][i]['url'] = '/discuss' + prep_dict[x][y][i]['url']
            if '/' in el.get('attack_url', ''):
                prep_dict[x][y][i]['attack_url'] = '/discuss' + prep_dict[x][y][i]['attack_url']

    # modify urls for topic switch
    for i, el in enumerate(prep_dict['issues']['all']):
        prep_dict['issues']['all'][i]['url'] = '/discuss' + prep_dict['issues']['all'][i]['url']


def modify_discussion_bubbles(prep_dict: dict, registry: Registry):
    """
    Removes gravatar from the bubbles if we use the modern interface

    :param prep_dict:
    :param registry:
    :return:
    """
    if usage_of_modern_bubbles(registry):
        for bubble in prep_dict['discussion']['bubbles']:
            if bubble['is_system']:
                bubble['message'] = re.sub('<img[^>]*>', '', bubble['message'])


def modifiy_issue_main_url(prep_dict: dict):
    # modify urls for topic switch
    pdict = ['user', 'other']
    for p in pdict:
        for i, el in enumerate(prep_dict[p]):
            prep_dict[p][i]['url'] = '/discuss' + prep_dict[p][i]['url']
    return prep_dict


def prepare_request_dict(request: Request):
    """

    :param request:
    :return:
    """
    LOG.debug("Preparing request dict for renderer")
    db_user = request.validated['user']
    nickname = db_user.nickname if db_user.nickname != nick_of_anonymous_user else None
    db_last_topic = history_handler.get_last_issue_of(db_user)

    slug = __get_slug(request.matchdict)
    db_issue = __get_issue(request, slug, db_last_topic)

    issue_handler.save_issue_in_session(db_issue, request)
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    set_language_for_visit(request)

    return {
        'nickname': nickname,
        'user': db_user,
        'path': request.path,
        'app_url': request.application_url,
        'matchdict': request.matchdict,
        'params': request.params,
        'session': request.session,
        'registry': request.registry,
        'issue': db_issue,
        'history': history,
        'ui_locales': get_language_from_cookie(request)
    }


def __get_slug(matchdict) -> str:
    """

    :param matchdict: matchdict of current request object
    :return:
    """
    slug = None
    if 'slug' in matchdict:
        slug = matchdict['slug']
        if not isinstance(matchdict['slug'], str) and len(matchdict['slug']) > 0:
            slug = matchdict['slug'][0]
    return slug


def __get_issue(request: Request, slug: str, db_last_topic: Issue) -> Issue:
    """

    :param request:
    :param slug:
    :param db_last_topic:
    :return:
    """
    if 'slug' in request.matchdict:
        slug = request.matchdict['slug']
        if not isinstance(request.matchdict['slug'], str) and len(request.matchdict['slug']) > 0:
            slug = request.matchdict['slug'][0]

    if not slug and db_last_topic:
        issue = db_last_topic
    elif slug:
        issue = issue_handler.get_id_of_slug(slug)
    else:
        issue = issue_handler.get_issue_id(request)

    if not issue:
        raise HTTPNotFound()

    if isinstance(issue, int):
        db_issue = DBDiscussionSession.query(Issue).get(issue)
    else:
        db_issue = issue

    return db_issue


def append_extras_dict(pdict: dict, rdict: dict, nickname: str, is_reportable: bool) -> None:
    """

    :param pdict: prepared dict for rendering
    :param rdict: request dictionary
    :param nickname: request.authenticated_userid
    :param is_reportable: Same as discussion.bubbles.last.is_markable, but TAL has no last indicator
    :return:
    """
    _dh = DictionaryHelper(rdict['ui_locales'], pdict['issues']['lang'])
    db_user = DBDiscussionSession.query(User).filter_by(
        nickname=nickname if nickname else nick_of_anonymous_user).first()
    pdict['extras'] = _dh.prepare_extras_dict(rdict['issue'].slug, is_reportable, True, True, rdict['registry'],
                                              rdict['app_url'], rdict['path'], db_user)


def append_extras_dict_during_justification_argument(request: Request, db_user: User, db_issue: Issue, pdict: dict):
    """

    :param request:
    :param db_user:
    :param db_issue:
    :param pdict:
    :return:
    """
    system_lang = get_language_from_cookie(request)
    item_len = len(pdict['items']['elements'])
    _dh = DictionaryHelper(system_lang, db_issue.lang)
    logged_in = (db_user and db_user.nickname != nick_of_anonymous_user) is not None
    extras_dict = _dh.prepare_extras_dict(db_issue.slug, False, True, True, request.registry,
                                          request.application_url, request.path, db_user=db_user)
    # is the discussion at the end?
    if item_len == 0 or item_len == 1 and logged_in or 'login' in pdict['items']['elements'][0].get('id'):
        _dh.add_discussion_end_text(pdict['discussion'], extras_dict, request.authenticated_userid,
                                    at_justify_argumentation=True)

    pdict['extras'] = extras_dict


def append_extras_dict_during_justification_statement(request: Request, db_user: User, db_issue: Issue,
                                                      db_statement: Statement,
                                                      pdict: dict, attitude: Attitudes):
    """

    :param request:
    :param db_user:
    :param db_issue:
    :param db_statement:
    :param pdict:
    :param attitude:
    :return:
    """
    if attitude in (Attitudes.AGREE, Attitudes.DISAGREE):
        __append_extras_dict_without_flag(request, db_user, db_issue, db_statement, pdict, attitude)
    else:
        __append_extras_dict_with_flag(request, db_user, db_issue, db_statement, pdict)


def __append_extras_dict_with_flag(request: Request, db_user: User, db_issue: Issue, db_statement: Statement,
                                   pdict: dict):
    """

    :param request:
    :param db_user:
    :param db_issue:
    :param db_statement:
    :param pdict:
    :return:
    """
    item_len = len(pdict['items']['elements'])
    _dh = DictionaryHelper(get_language_from_cookie(request), db_issue.lang)
    extras_dict = _dh.prepare_extras_dict(db_issue.slug, True, True, True, request.registry,
                                          request.application_url, request.path, db_user=db_user)

    if item_len == 0:  # is the discussion at the end?
        _dh.add_discussion_end_text(pdict['discussion'], extras_dict, db_user.nickname,
                                    at_dont_know=True, current_premise=db_statement.get_text())
    pdict['extras'] = extras_dict


def __append_extras_dict_without_flag(request: Request, db_user: User, db_issue: Issue, db_statement: Statement,
                                      pdict: dict, attitude: Attitudes):
    """

    :param request:
    :param db_user:
    :param db_issue:
    :param db_statement:
    :param pdict:
    :param attitude:
    :return:
    """
    item_len = len(pdict['items']['elements'])
    _dh = DictionaryHelper(get_language_from_cookie(request), db_issue.lang)
    supportive = attitude in [Attitudes.AGREE, Attitudes.DONT_KNOW]
    logged_in = db_user is not None and db_user.nickname != nick_of_anonymous_user
    extras_dict = _dh.prepare_extras_dict(db_issue.slug, False, True, True, request.registry,
                                          request.application_url, request.path, db_user)

    if item_len == 0 or item_len == 1 and logged_in:  # is the discussion at the end?
        _dh.add_discussion_end_text(pdict['discussion'], extras_dict, db_user.nickname, at_justify=True,
                                    current_premise=db_statement.get_text(),
                                    supportive=supportive)
    pdict['extras'] = extras_dict


def main_dict(request, title):
    return {
        'title': title,
        'project': project_name,
        'extras': request.decorated['extras'],
        'discussion': {'broke_limit': False}
    }
