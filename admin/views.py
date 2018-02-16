"""
Introducing an admin interface to enable easy database management.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json

from cornice import Service
from pyramid.httpexceptions import exception_response

import admin.lib as lib
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.validation import valid_user, validate, valid_table_name, has_keywords
from dbas.logger import logger
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

api_token = Service(name='api_token',
                    path='/{url:.*}api_token/',
                    renderer='json',
                    permission='admin',
                    cors_policy=cors_policy)

revoke_token = Service(name='revoke_token',
                       path='/{url:.*}revoke_token/{id}',
                       renderer='json',
                       permission='admin',
                       cors_policy=cors_policy)

# IMPORTANT: we do not need to validate if the user in an admin because we set the permission of this views


@dashboard.get()
@validate(valid_user)
def main_admin(request):
    """
    View configuration for the content view. Only logged in user can reach this page.

    :param request: current webservers request
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('Admin', 'main_admin', 'def')
    should_log_out = user.update_last_action(request.authenticated_userid)
    if should_log_out:
        return user_logout(request, True)

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry, request.application_url, request.path, request.authenticated_userid)
    dashboard_elements = {
        'entities': lib.get_overview(request.path),
        'api_tokens': lib.get_application_tokens()
    }

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Admin' if 'is_admin' in extras_dict and extras_dict['is_admin'] else '(B)admin',
        'project': project_name,
        'extras': extras_dict,
        'dashboard': dashboard_elements
    }


@z_table.post()
@validate(valid_user)
def main_table(request):
    """
    View configuration for the content view. Only logged in user can reach this page.

    :param request: current webservers request
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('Admin', 'main_table', 'def')
    should_log_out = user.update_last_action(request.authenticated_userid)
    if should_log_out:
        return user_logout(request, True)

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)
    table_name = request.matchdict['table']
    if not table_name.lower() in lib.table_mapper:
        return exception_response(400)
    try:
        table_dict = lib.get_table_dict(table_name, request.application_url)
        table_dict['has_error'] = False
        table_dict['error'] = ''
    except Exception as e:
        table_dict = dict()
        table_dict['has_error'] = True
        table_dict['error'] = str(e)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Admin - ' + table_name,
        'project': project_name,
        'extras': extras_dict,
        'table': table_dict
    }


@update_row.post()
@validate(valid_user, valid_table_name, has_keywords(('keys', list()), ('values', list())))
def main_update(request):
    """
    View configuration for updating any row

    :param request: current webservers request
    :return: dict()
    """
    logger('Admin', 'main_update', 'def ' + str(request.params))
    table = request.validated['table']
    uids = request.validated['uids']
    keys = request.validated['keys']
    values = request.validated['values']
    return lib.update_row(table, uids, keys, values)


@delete_row.post()
@validate(valid_user, valid_table_name, has_keywords(('uids', list())))
def main_delete(request):
    """
    View configuration for deleting any row

    :param request: current webservers request
    :return: dict()
    """
    logger('Admin', 'main_delete', 'def ' + str(request.json_body))
    table = request.params['table']
    uids = json.loads(request.params['uids'])
    return lib.delete_row(table, uids)


@add_row.post()
@validate(valid_user, valid_table_name, has_keywords(('new_data', dict())))
def main_add(request):
    """
    View configuration for adding any row

    :param request: current webservers request
    :return: dict()
    """
    logger('Admin', 'main_add', 'def ' + str(request.json_body))
    new_data = request.validated['new_data']
    table = request.validated['table']
    return lib.add_row(table, new_data)


@update_badge.get()
@validate(valid_user)
def main_update_badge(request):
    """
    View configuration for updating a badge

    :param request: current webservers request
    :return: dict()
    """
    logger('Admin', 'main_update_badge', 'def ' + str(request.json_body))
    return lib.update_badge()


@api_token.post()
def generate_api_token(request):
    owner = request.params['owner']
    token = lib.generate_application_token(owner)
    logger('Admin', 'Application Tokens', 'API-Token for {} was created.'.format(owner))
    return {'token': token}


@revoke_token.delete()
def revoke_api_token(request):
    token_id = request.matchdict['id']
    lib.revoke_application_token(token_id)
    logger('Admin', 'Application Tokens', 'API-Token {} was revoked.'.format(token_id))
