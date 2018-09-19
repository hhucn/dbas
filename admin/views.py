"""
Introducing an admin interface to enable easy database management.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import logging
from cornice import Service
from pyramid.httpexceptions import exception_response

import admin.lib as lib
from dbas.handler import user
from dbas.handler.language import get_language_from_cookie
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.validators.core import has_keywords, validate
from dbas.validators.database import valid_table_name
from dbas.validators.user import valid_user_as_admin, valid_user_optional
from dbas.views import user_logout
from dbas.views.helper import project_name

LOG = logging.getLogger(__name__)
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
                    description='Admin Page',
                    renderer='templates/admin.pt',
                    permission='everybody',
                    cors_policy=cors_policy)

z_table = Service(name='table_page',
                  path='/{table}',
                  description='Table Page',
                  renderer='templates/table.pt',
                  permission='admin',
                  cors_policy=cors_policy)

update_row = Service(name='update_table_row',
                     path='/{url:.*}update',
                     description='Update',
                     renderer='json',
                     permission='admin',
                     cors_policy=cors_policy)

delete_row = Service(name='delete_table_row',
                     path='/{url:.*}delete',
                     description='Delete',
                     renderer='json',
                     permission='admin',
                     cors_policy=cors_policy)

add_row = Service(name='add_table_row',
                  path='/{url:.*}add',
                  description='Add',
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
@validate(valid_user_optional)
def main_admin(request):
    """
    View configuration for the content view. Only logged in user can reach this page.

    :param request: current webservers request
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("def")
    db_user = request.validated['user']

    should_log_out = user.update_last_action(request.validated['user'])
    if should_log_out:
        return user_logout(request, True)

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   db_user)
    dashboard_elements = {
        'entities': lib.get_overview(request.path),
        'api_tokens': lib.get_application_tokens()
    }

    return {
        'language': str(ui_locales),
        'title': 'Admin' if db_user.is_admin() else '(B)admin',
        'project': project_name,
        'extras': extras_dict,
        'dashboard': dashboard_elements,
        'discussion': {'broke_limit': False}
    }


@z_table.get()
@validate(valid_user_as_admin)
def main_table(request):
    """
    View configuration for the content view. Only logged in user can reach this page.

    :param request: current webservers request
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("def")
    should_log_out = user.update_last_action(request.validated['user'])
    if should_log_out:
        return user_logout(request, True)

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.validated['user'])
    table_name = request.matchdict['table']
    if not table_name.lower() in lib.table_mapper:
        return exception_response(400)
    table_dict = lib.get_table_dict(table_name, request.application_url)

    return {
        'language': str(ui_locales),
        'title': 'Admin - ' + table_name,
        'project': project_name,
        'extras': extras_dict,
        'table': table_dict,
        'discussion': {'broke_limit': False}
    }


@update_row.post()
@validate(valid_user_as_admin, valid_table_name, has_keywords(('keys', list), ('uids', list), ('values', list)))
def main_update(request):
    """
    View configuration for updating any row

    :param request: current webservers request
    :return: dict()
    """
    LOG.debug("def %s", request.params)
    table = request.validated['table']
    uids = request.validated['uids']
    keys = request.validated['keys']
    values = request.validated['values']
    return lib.update_row(table, uids, keys, values)


@delete_row.post()
@validate(valid_user_as_admin, valid_table_name, has_keywords(('uids', list)))
def main_delete(request):
    """
    View configuration for deleting any row

    :param request: current webservers request
    :return: dict()
    """
    LOG.debug("def %s", request.json_body)
    return lib.delete_row(request.validated['table'], request.validated['uids'])


@add_row.post()
@validate(valid_user_as_admin, valid_table_name, has_keywords(('new_data', dict)))
def main_add(request):
    """
    View configuration for adding any row

    :param request: current webservers request
    :return: dict()
    """
    LOG.debug("def %s", request.json_body)
    return lib.add_row(request.validated['table'], request.validated['new_data'])


@api_token.post()
def generate_api_token(request):
    owner = request.params['owner']
    token = lib.generate_application_token(owner)
    LOG.debug("API-Token for %s was created.", owner)
    return {'token': token}


@revoke_token.delete()
def revoke_api_token(request):
    token_id = request.matchdict['id']
    lib.revoke_application_token(token_id)
    LOG.debug("API-Token %s was revoked.", token_id)
