"""
Introducing an graph manager.
"""

import logging

from cornice import Service

from dbas.handler.language import get_language_from_cookie
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.core import has_keywords_in_json_path, validate
from dbas.validators.discussion import valid_issue_by_id
from graph.lib import get_d3_data, get_opinion_data, get_path_of_user
from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement

LOG = logging.getLogger(__name__)
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
@validate(valid_issue_by_id)
def get_d3_complete_dump(request):
    LOG.debug("Creating a complete d3 dump. %s", request.json_body)
    path = request.json_body.get('path', '')
    db_issue = request.validated['issue']

    graph, error = get_d3_data(db_issue)
    return_dict = graph
    return_dict.update({'type': 'complete'})
    if not error:
        return_dict.update({'path': get_path_of_user(request.application_url, path, db_issue)})
        return_dict.update({'error': ''})
    else:  # gets called if the data itself is malicious
        ui_locales = get_language_from_cookie(request)
        _t = Translator(ui_locales)
        error = _t.get(_.internalKeyError)
        return_dict = {'error': error}

    return return_dict


@partial_graph.post()
@validate(valid_issue_by_id, has_keywords_in_json_path(('uid', int), ('is_argument', bool), ('path', str)))
def get_d3_partial_dump(request):
    LOG.debug("Create partial d3 dump. %s", request.json_body)
    path = request.validated['path']
    uid = request.validated['uid']
    is_argument = request.validated['is_argument']
    db_issue = request.validated['issue']
    return_dict = {
        'type': 'partial'
    }

    if is_argument:
        graph, error = get_partial_graph_for_argument(uid, db_issue)
    else:
        graph, error = get_partial_graph_for_statement(uid, db_issue, path)

    if not error:
        return_dict.update(graph)
        return_dict.update({'node_opinion_factors': get_opinion_data(db_issue)})
        return_dict.update({'path': get_path_of_user(request.application_url, path, db_issue)})
        return_dict.update({'error': ''})
    else:  # gets called if the data itself is malicious
        ui_locales = get_language_from_cookie(request)
        _t = Translator(ui_locales)
        error = _t.get(_.internalKeyError)
        return_dict = {
            'error': error
        }

    return return_dict
