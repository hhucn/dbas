"""
Introducing an graph manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import dbas.helper.issue_helper as IssueHelper

from cornice import Service

from dbas.logger import logger
from graph.lib import get_sigma_data, get_d3_data

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

sigma_graph = Service(name='sigma',
                      path='/sigma',
                      description="Sigma Dump")

d3_graph = Service(name='d3js',
                   path='/d3',
                   description="D3JS Dump")


# =============================================================================
# GRAPH-RELATED REQUESTS
# =============================================================================


@sigma_graph.get()
def get_sigma_dump(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Graph', 'simap', 'main')
    issue = IssueHelper.get_issue_id(request)

    return_dict = get_sigma_data(issue)
    return json.dumps(return_dict, True)


@d3_graph.get()
def get_d3_dump(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Graph', 'd3', 'main')
    issue = IssueHelper.get_issue_id(request)

    return_dict = get_d3_data(issue)
    return json.dumps(return_dict, True)
