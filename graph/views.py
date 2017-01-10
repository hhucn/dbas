"""
Introducing an graph manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import dbas.helper.issue as IssueHelper

from cornice import Service

from dbas.logger import logger
from graph.lib import get_d3_data, get_doj_data, get_opinion_data, get_path_of_user

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
    logger('Graph', 'd3', 'main')
    path = request.params['path'] if 'path' in request.params else ''
    issue = IssueHelper.get_issue_id(request)

    return_dict = get_d3_data(issue, request.authenticated_userid)
    return_dict.update({'node_doj_factors': get_doj_data(issue)})
    return_dict.update({'node_opinion_factors': get_opinion_data(issue)})
    return_dict.update({'path': get_path_of_user(request.application_url, path, issue)})

    return json.dumps(return_dict, True)
