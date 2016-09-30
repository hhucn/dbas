"""
Introducing an admin interface to enable easy database management.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import dbas.helper.history as HistoryHelper
import dbas.user_management as UserHandler
import transaction
from admin.lib import get_dashboard_infos, get_table_dict
from cornice import Service
from dbas.lib import get_language
from dbas.logger import logger
from dbas.views import Dbas
from dbas.views import project_name
from dbas.helper.dictionary.main import DictionaryHelper
from pyramid.threadlocal import get_current_registry

#
# CORS configuration
#
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
                   origins=('*',),
                   max_age=42)


# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

dashboard = Service(name='dashboard_page',
                    path='/',
                    description="Admin Page",
                    renderer='templates/admin.pt',
                    permission='everybody',  # or permission='use'
                    cors_policy=cors_policy)

table = Service(name='table_page',
                path='/{table}',
                description="Table Page",
                renderer='templates/table.pt',
                permission='use',
                cors_policy=cors_policy)


@dashboard.get()
def main_admin(request):
    """
    View configuration for the content view. Only logged in user can reach this page.
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_admin', 'def')
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    should_log_out = UserHandler.update_last_action(transaction, request.authenticated_userid)
    if should_log_out:
        return Dbas(request).user_logout(True)

    ui_locales = get_language(request, get_current_registry())
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)
    dashboard = get_dashboard_infos(request.path)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': 'Admin',
        'project': project_name,
        'extras': extras_dict,
        'dashboard': dashboard
    }


@table.get()
def main_table(request):
    """
    View configuration for the content view. Only logged in user can reach this page.
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_table', 'def')
    HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
    should_log_out = UserHandler.update_last_action(transaction, request.authenticated_userid)
    if should_log_out:
        return Dbas(request).user_logout(True)

    ui_locales = get_language(request, get_current_registry())
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)
    table = request.matchdict['table']
    table_dict = get_table_dict(table)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': table,
        'project': project_name,
        'extras': extras_dict,
        'table': table_dict
    }
