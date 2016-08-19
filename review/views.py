"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import dbas.helper.history as HistoryHelper
import dbas.helper.issue as IssueHelper
import dbas.user_management as UserHandler
import review.review_helper as ReviewHelper
import transaction
from cornice import Service
from dbas.lib import get_language
from dbas.logger import logger
from dbas.strings.translator import Translator
from dbas.views import mainpage, Dbas, get_discussion_language
from dbas.views import project_name
from dbas.helper.dictionary.main import DictionaryHelper
from pyramid.threadlocal import get_current_registry
from slugify import slugify

# =============================================================================
# CORS configuration
# =============================================================================

cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
                   origins=('*',),
                   max_age=42)

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

content = Service(name='review_content',
                  path='/{queue}/{slug}',
                  renderer='templates/review_content.pt',
                  description="Review Queue",
                  permission='use',
                  cors_policy=cors_policy)

reputation = Service(name='review_reputation',
                     path='/*slug',
                     renderer='templates/review_reputation.pt',
                     description="Review Reputation",
                     permission='use',
                     cors_policy=cors_policy)

index = Service(name='review_index',
                path='/*slug',
                renderer='templates/review.pt',
                description="Review Index",
                permission='use',
                cors_policy=cors_policy)


# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================

@index.get()
def main_review(request):
    """
    View configuration for the review index.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Review', 'main_review', 'main ' + str(request.matchdict))
    ui_locales = get_language(request, get_current_registry())
    session_expired = UserHandler.update_last_action(transaction, request.authenticated_userid)
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    issue           = IssueHelper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, False)
    extras_dict     = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    try:
        slug = request.matchdict['slug'][0]
        issue = IssueHelper.get_title_for_slug(slug)
        if not issue:
            issue = issue_dict['title']
    except KeyError and IndexError:
        issue = issue_dict['title']

    if len(issue) == 0:
        issue = issue_dict['title']

    review_dict = ReviewHelper.get_review_array(mainpage, slugify(issue), _tn)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'review': review_dict,
        'issues': issue_dict,
        'current_issue_title': issue,
        'reputation_count': 4
    }


@content.get()
def main_review_content(request):
    """
    View configuration for the review content.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Review', 'main_review_content', 'main')
    ui_locales = get_language(request, get_current_registry())
    session_expired = UserHandler.update_last_action(transaction, request.authenticated_userid)
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    subpage_name = request.matchdict['queue']
    issue = IssueHelper.get_title_for_slug(request.matchdict['slug'])
    subpage = ReviewHelper.get_subpage_for(subpage_name, request.authenticated_userid)
    enough_reputation = True if subpage is not None else False

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'subpage': {'queue': subpage,
                    'issue': issue,
                    'enough_reputation': enough_reputation}
    }


@reputation.get()
def main_review_reputation(request):
    """
    View configuration for the review reputation.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Review', 'main_review_reputation', 'main')
    ui_locales = get_language(request, get_current_registry())
    session_expired = UserHandler.update_last_action(transaction, request.authenticated_userid)
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'reputation_count': 4
    }
