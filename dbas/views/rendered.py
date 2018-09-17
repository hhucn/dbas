"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import graphene
import logging
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config, notfound_view_config
from webob_graphql import serve_graphql_request

from api.v2.graphql.core import Query
from dbas.database import DBDiscussionSession
from dbas.helper.decoration import prep_extras_dict
from dbas.validators.core import validate
from dbas.views.helper import main_dict

LOG = logging.getLogger(__name__)


# graphiql
@view_config(route_name='main_graphiql', permission='everybody', require_csrf=False)
def main_graphiql(request):
    """
    View configuration for GraphiQL.

    :param request: current request of the server
    :return: graphql
    """
    LOG.debug("Show GraphiQL configuration")
    schema = graphene.Schema(query=Query)
    context = {'session': DBDiscussionSession}
    return serve_graphql_request(request, schema, batch_enabled=True, context_value=context)


# 404 page
@notfound_view_config(renderer='../templates/404.pt')
@validate(prep_extras_dict)
def notfound(request):
    """
    View configuration for the 404 page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    if request.path.startswith('/api'):
        return HTTPNotFound({
            'path': request.path,
            'message': 'Not Found'
        })

    # check cornice routes
    cornice_services = ['/admin', '/docs']
    for service in cornice_services:
        if request.path.startswith(service):
            LOG.debug("Redirect to %s/", service)
            return HTTPFound(location=service + '/')

    LOG.debug("COnfiguration for 404 page in %s-request. Path: %s, view name: %s, matchdict: %s, params: %s",
              request.method, request.path, request.view_name, request.matchdict, request.params)

    # clear url
    path = request.path
    if path.startswith('/404/'):
        path = path[4:]

    # prepare return dict
    param_error = 'param_error' in request.params and request.params['param_error'] == 'true'
    revoked_content = 'revoked_content' in request.params and request.params['revoked_content'] == 'true'

    request.response.status = 404

    prep_dict = main_dict(request, '404 Error')
    prep_dict.update({
        'page_notfound_viewname': path,
        'param_error': param_error,
        'revoked_content': revoked_content,
        'discussion': {'broke_limit': False}
    })
    return prep_dict


@view_config(route_name='main_batman', renderer='../templates/batman.pt', permission='everybody')
@validate(prep_extras_dict)
def batman(request):
    """
    You are not the user D-BAS deserves!

    :param request: current request of the server
    """
    LOG.debug("NANANANANNANANANANANANANANANANA BATMAAAAAAN!")
    return main_dict(request, 'Batman')
