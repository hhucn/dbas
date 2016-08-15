"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import review.review_helper as ReviewHelper
import transaction
import dbas.helper.history_helper as HistoryHelper
import dbas.user_management as UserHandler

from cornice import Service
from dbas.views import project_name
from pyramid.threadlocal import get_current_registry
from dbas.helper.dictionary_helper import DictionaryHelper
from dbas.lib import get_language
from dbas.logger import logger
from dbas.strings import Translator
from dbas.views import mainpage, Dbas

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

index = Service(name='review_index',
                path='/',
                renderer='templates/review.pt',
                description="Review Index",
                permission='use',
                cors_policy=cors_policy)

content = Service(name='review_content',
                  path='/{queue}',
                  renderer='templates/review_content.pt',
                  description="Review Queue",
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
    logger('Review', 'main_review', 'main')
    ui_locales = get_language(request, get_current_registry())
    session_expired = UserHandler.update_last_action(transaction, request.authenticated_userid)
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    _tn = Translator(ui_locales)
    if session_expired:
        return Dbas(request).user_logout(True)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    review_dict = ReviewHelper.get_review_array(mainpage, _tn)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'review': review_dict
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
    subpage = ReviewHelper.get_subpage_for(subpage_name, request.authenticated_userid)
    enough_reputation = True if subpage is not None else False

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_tn.review),
        'project': project_name,
        'extras': extras_dict,
        'subpage': {'name': subpage,
                    'enough_reputation': enough_reputation}
    }
