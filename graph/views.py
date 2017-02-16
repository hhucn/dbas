"""
Introducing an graph manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import dbas.helper.issue as IssueHelper
from dbas.lib import get_language
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from cornice import Service
from dbas.logger import logger
from graph.lib import get_d3_data, get_doj_data, get_opinion_data, get_path_of_user
from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement

# =============================================================================
# SERVICES - Define services for several actions of D-BAS
# =============================================================================

d3_graph = Service(name='d3js',
                   path='/d3',
                   description="D3JS Dump")


# =============================================================================
# GRAPH-RELATED REQUESTS
# =============================================================================


@d3_graph.get()
def get_d3_dump(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Graph', 'd3', 'main: ' + str(request.params))
    path = request.params['path'] if 'path' in request.params else ''
    uid = request.params['uid'] if 'uid' in request.params else '0'
    is_argument = True if 'is_argument' in request.params and request.params['is_argument'] == 'true' else False
    issue = IssueHelper.get_issue_id(request)

    graph, error = get_d3_data(issue, request.authenticated_userid)
    return_dict = {'complete_graph': graph}
    if not error:
        return_dict.update({'node_doj_factors': get_doj_data(issue)})
        return_dict.update({'node_opinion_factors': get_opinion_data(issue)})
        return_dict.update({'path': get_path_of_user(request.application_url, path, issue)})
        if uid != '0':
            if is_argument:
                return_dict.update({'partial_graph': get_partial_graph_for_argument(uid, issue, request.authenticated_userid)})
            else:
                return_dict.update({'partial_graph': get_partial_graph_for_statement(uid, issue, request.authenticated_userid)})
        else:
            return_dict.update({'partial_graph': {}})

        return_dict.update({'error': ''})
    else:
        ui_locales = get_language(request)
        _t = Translator(ui_locales)
        error = _t.get(_.internalKeyError)
        return_dict = {'error': error}

    return json.dumps(return_dict)
