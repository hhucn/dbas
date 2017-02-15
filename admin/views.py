"""
Introducing an admin interface to enable easy database management.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json

import admin.lib as lib
import dbas.user_management as UserHandler
from cornice import Service
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.lib import get_language
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.views import user_logout, base_layout, project_name

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
                  permission='admin',
                  cors_policy=cors_policy)

update_row = Service(name='update_table_row',
                     path='/{url:.*}ajax_admin_update',
                     description="Update",
                     renderer='json',
                     permission='admin',
                     cors_policy=cors_policy)

delete_row = Service(name='delete_table_row',
                     path='/{url:.*}ajax_admin_delete',
                     description="Delete",
                     renderer='json',
                     permission='admin',
                     cors_policy=cors_policy)

add_row = Service(name='add_table_row',
                  path='/{url:.*}ajax_admin_add',
                  description="Add",
                  renderer='json',
                  permission='admin',
                  cors_policy=cors_policy)

update_badge = Service(name='update_badge_counter',
                       path='/{url:.*}ajax_admin_update_badges',
                       description="Update",
                       renderer='json',
                       permission='admin',
                       cors_policy=cors_policy)


@dashboard.get()
def main_admin(request):
    """
    View configuration for the content view. Only logged in user can reach this page.

    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_admin', 'def')
    request_authenticated_userid = request.authenticated_userid
    should_log_out = UserHandler.update_last_action(request_authenticated_userid)
    if should_log_out:
        return user_logout(request, True)

    ui_locales = get_language(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request, request_authenticated_userid)
    overview = lib.get_overview(request.path)

    return {
        'layout': base_layout(),
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
    request_authenticated_userid = request.authenticated_userid
    logger('Admin', 'main_table', 'def')
    should_log_out = UserHandler.update_last_action(request_authenticated_userid)
    if should_log_out:
        return user_logout(request, True)

    ui_locales = get_language(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request, request_authenticated_userid)
    table = request.matchdict['table']
    try:
        table_dict = lib.get_table_dict(table, request.application_url)
        table_dict['has_error'] = False
        table_dict['error'] = ''
    except Exception as e:
        table_dict = dict()
        table_dict['is_existing'] = False
        table_dict['has_error'] = True
        table_dict['error'] = str(e)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Admin - ' + table,
        'project': project_name,
        'extras': extras_dict,
        'table': table_dict
    }


@update_row.get()
def main_update(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_update', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request)
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


@delete_row.get()
def main_delete(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_delete', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request)
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


@add_row.get()
def main_add(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_add', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request)
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


@update_badge.get()
def main_update_badge(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Admin', 'main_update_badge', 'def ' + str(request.params))

    nickname = request.authenticated_userid
    ui_locales = get_language(request)
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        data, error = lib.update_badge(nickname, _tn)
        return_dict['error'] = error
        return_dict['data'] = data
    except KeyError as e:
        logger('Admin', 'main_add main_update_badge', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return json.dumps(return_dict, True)
