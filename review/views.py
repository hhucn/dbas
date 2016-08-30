"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import dbas.helper.history as HistoryHelper
import dbas.helper.issue as IssueHelper
import dbas.user_management as UserManager
import review.review_helper as ReviewHelper
import transaction

from cornice import Service
from pyramid.httpexceptions import HTTPFound
from dbas.lib import get_language
from dbas.logger import logger
from dbas.strings.translator import Translator
from dbas.views import mainpage, Dbas, get_discussion_language
from dbas.views import project_name
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.url_manager import UrlManager
from pyramid.threadlocal import get_current_registry

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
                  path='/{queue}',
                  renderer='templates/review_content.pt',
                  description='Review Queue',
                  permission='use',
                  cors_policy=cors_policy)

areputation = Service(name='review_reputation',
                     path='/reputation',
                     renderer='templates/review_reputation.pt',
                     description='Review Reputation',
                     permission='use',
                     cors_policy=cors_policy)

# services are sorted alphabetically, so index has to be
# after reputation, because of the *slug
zindex = Service(name='review_index',
                 path='*slug',
                 renderer='templates/review.pt',
                 description='Review Index',
                 permission='use',
                 cors_policy=cors_policy)

switch_language = Service(name='lang',
                          path='ajax_switch_language',
                          description='Switch Language',
                          permission='use',
                          cors_policy=cors_policy)


# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================

@content.get()
def main_review_content(request):
    """
    View configuration for the review content.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Review', 'main_review_content', 'main')
    ui_locales = get_language(request, get_current_registry())
    session_expired = UserManager.update_last_action(transaction, request.authenticated_userid)
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    subpage_name = request.matchdict['queue']
    elements, user_has_access = ReviewHelper.get_subpage_elements_for(subpage_name, request.authenticated_userid, _tn)
    if not elements:
        return HTTPFound(location=UrlManager(mainpage, for_api=False).get_404([request.path[1:]]))

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'subpage': {
            'elements': elements,
            'has_access': user_has_access
                    }
    }


@areputation.get()
def main_review_reputation(request):
    """
    View configuration for the review reputation.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Review', 'main_review_reputation', 'main')
    ui_locales = get_language(request, get_current_registry())
    session_expired = UserManager.update_last_action(transaction, request.authenticated_userid)
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    reputation_dict = ReviewHelper.get_reputation_history(request.authenticated_userid)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'reputation': reputation_dict
    }


@zindex.get()
def main_review(request):
    """
    View configuration for the review index.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Review', 'main_review', 'main ' + str(request.matchdict))
    ui_locales      = get_language(request, get_current_registry())
    nickname        = request.authenticated_userid
    session_expired = UserManager.update_last_action(transaction, nickname)
    HistoryHelper.save_path_in_database(nickname, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    issue           = IssueHelper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, False)
    extras_dict     = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(nickname, request)

    review_dict = ReviewHelper.get_review_queues_array(mainpage, _tn, nickname)
    count, all_rights = ReviewHelper.get_reputation_of(nickname)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'review': review_dict,
        'reputation_list': ReviewHelper.get_reputation_list(),
        'issues': issue_dict,
        'reputation': {'count': count,
                       'has_all_rights': all_rights}
    }
