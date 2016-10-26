"""
Introducing an admin interface to enable easy database management.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json

import admin.lib as lib
import dbas.helper.history as HistoryHelper
import dbas.user_management as UserHandler
import transaction
from cornice import Service
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.lib import get_language
from dbas.logger import logger
from dbas.strings.translator import Translator
from dbas.views import Dbas, project_name
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

z_table = Service(name='table_page',
                  path='/{table}',
                  description="Table Page",
                  renderer='templates/table.pt',
                  permission='use',
                  cors_policy=cors_policy)

update = Service(name='update_row',
                 path='/{url:.*}ajax_admin_update',
                 description="Update",
                 renderer='json',
                 permission='use',
                 cors_policy=cors_policy)

delete = Service(name='delete_row',
                 path='/{url:.*}ajax_admin_delete',
                 description="Delete",
                 renderer='json',
                 permission='use',
                 cors_policy=cors_policy)

add = Service(name='add_row',
              path='/{url:.*}ajax_admin_add',
              description="Add",
              renderer='json',
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
    overview = lib.get_overview(request.path)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': 'Admin',
        'project': project_name,
        'extras': extras_dict,
        'dashboard': overview
    }


@z_table.get()
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
    try:
        table_dict = lib.get_table_dict(table)
        table_dict['has_error'] = False
        table_dict['error'] = ''
    except Exception as e:
        table_dict = dict()
        table_dict['is_existing'] = False
        table_dict['has_error'] = True
        table_dict['error'] = str(e)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': 'Admin - ' + table,
        'project': project_name,
        'extras': extras_dict,
        'table': table_dict
    }


@update.get()
def main_update(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_update', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request, get_current_registry())
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        table = request.params['table']
        uids = json.loads(request.params['uids'])
        keys = json.loads(request.params['keys'])
        values = json.loads(request.params['values'])
        return_dict['error'] = lib.update_row(table, uids, keys, values, nickname, _tn)
    except KeyError as e:
        logger('Admin', 'main_update error', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return json.dumps(return_dict, True)


@delete.get()
def main_delete(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_delete', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request, get_current_registry())
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        table = request.params['table']
        uids = json.loads(request.params['uids'])
        return_dict['error'] = lib.delete_row(table, uids, nickname, _tn)
    except KeyError as e:
        logger('Admin', 'main_delete error', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return json.dumps(return_dict, True)


@add.get()
def main_add(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_add', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request, get_current_registry())
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        table = request.params['table']
        new_data = json.loads(request.params['new_data'])
        return_dict['error'] = lib.add_row(table, new_data, nickname, _tn)
    except KeyError as e:
        logger('Admin', 'main_add error', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return json.dumps(return_dict, True)
