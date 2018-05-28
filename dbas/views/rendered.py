"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import graphene
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config, notfound_view_config
from webob_graphql import serve_graphql_request

from api.v2.graphql.core import Query
from dbas.database import DBDiscussionSession
from dbas.helper.decoration import prep_extras_dict
from dbas.logger import logger
from dbas.validators.core import validate
from dbas.views.helper import main_dict


# graphiql
@view_config(route_name='main_graphiql', permission='everybody', require_csrf=False)
def main_graphiql(request):
    """
    View configuration for GraphiQL.

    :param request: current request of the server
    :return: graphql
    """
    logger('main_graphiql', 'main')
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

    logger('notfound', 'main in {}'.format(request.method) + '-request' +
           ', path: ' + request.path +
           ', view name: ' + request.view_name +
           ', matchdict: {}'.format(request.matchdict) +
           ', params: {}'.format(request.params))
    path = request.path
    if path.startswith('/404/'):
        path = path[4:]

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
