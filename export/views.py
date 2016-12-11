"""
Introducing an export manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import dbas.helper.issue as IssueHelper

from cornice import Service
from pyramid.threadlocal import get_current_registry

from dbas.lib import get_language
from dbas.logger import logger
from export.lib import get_dump, get_minimal_graph_export

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

dump = Service(name='export_dump',
               path='/dump',
               description='Database Dump')

doj = Service(name='export_doj',
              path='/doj*issue',
              description='Export for DoJ')


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

@dump.get()
def get_database_dump(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Export', 'get_database_dump', 'main')
    issue = IssueHelper.get_issue_id(request)
    ui_locales = get_language(request)

    return_dict = get_dump(issue, ui_locales)

    return json.dumps(return_dict, True)


@doj.get()
def get_doj_dump(request):
    """

    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Export', 'main', 'def')
    m = request.matchdict
    issue = m['issue'][0] if 'issue' in m and len(m['issue']) > 0 else None

    return json.dumps(get_minimal_graph_export(issue), True)
