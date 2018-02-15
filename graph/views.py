"""
Introducing an graph manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from cornice import Service

import dbas.handler.issue as IssueHelper
from dbas.handler.language import get_language_from_cookie
from dbas.helper.validation import validate, has_keywords
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from graph.lib import get_d3_data, get_doj_data, get_opinion_data, get_path_of_user
from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement

# =============================================================================
# SERVICES - Define services for several actions of D-BAS
# =============================================================================

complete_graph = Service(name='d3js_complete',
                         path='/complete',
                         description="D3JS Complete Dump")

partial_graph = Service(name='d3js_partial',
                        path='/partial',
                        description="D3JS Partial Dump")


# =============================================================================
# GRAPH-RELATED REQUESTS
# =============================================================================


@complete_graph.post()
def get_d3_complete_dump(request):
    logger('Graph', 'get_d3_complete_dump', 'main: ' + str(request.json_body))
    path = request.json_body.get('path', '')
    issue = IssueHelper.get_issue_id(request)

    graph, error = get_d3_data(issue)
    return_dict = graph
    return_dict.update({'type': 'complete'})
    if not error:
        # return_dict.update({'node_doj_factors': get_doj_nodes(issue)})
        # return_dict.update({'node_opinion_factors': get_opinion_data(issue)})
        return_dict.update({'path': get_path_of_user(request.application_url, path, issue)})
        return_dict.update({'error': ''})
    else:
        ui_locales = get_language_from_cookie(request)
        _t = Translator(ui_locales)
        error = _t.get(_.internalKeyError)
        return_dict = {'error': error}

    return return_dict


@partial_graph.post()
@validate(has_keywords(('uid', int), ('is_argument', bool), ('path', str)))
def get_d3_partial_dump(request):
    logger('Graph', 'get_d3_partial_dump', 'main: ' + str(request.json_body))
    path = request.validated['path']
    uid = request.validated['uid']
    is_argument = request.validated['is_argument']
    issue = IssueHelper.get_issue_id(request)
    return_dict = {
        'type': 'partial'
    }

    if not uid:
        graph, error = get_d3_data(issue, request.authenticated_userid)
        if not error:
            return_dict = graph
    else:
        if is_argument:
            graph, error = get_partial_graph_for_argument(uid, issue)
        else:
            graph, error = get_partial_graph_for_statement(uid, issue, path)
        if not error:
            return_dict.update(graph)
            return_dict.update({'node_doj_factors': get_doj_data(issue)})
            return_dict.update({'node_opinion_factors': get_opinion_data(issue)})
            return_dict.update({'path': get_path_of_user(request.application_url, path, issue)})
            return_dict.update({'error': ''})

    if error:
        ui_locales = get_language_from_cookie(request)
        _t = Translator(ui_locales)
        error = _t.get(_.internalKeyError)
        return_dict = {
            'error': error
        }

    return return_dict
