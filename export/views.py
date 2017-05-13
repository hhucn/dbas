"""
Introducing an export manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from cornice import Service

import dbas.helper.issue as IssueHelper
from dbas.logger import logger
from export.lib import get_dump, get_doj_data, get_table_rows

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

table_row = Service(name='export_table_row',
                    path='/{table}/*ids',
                    description='Export several columns from a table')


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

@dump.get()
def get_database_dump(request):
    """
    Dumps dict() for D3

    :param request: current webservers request
    :return: dict()
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Export', 'get_database_dump', 'main')
    issue = IssueHelper.get_issue_id(request)

    return get_dump(issue)


@doj.get()
def get_doj_dump(request):
    """
    Returns necessary data for the DoJ

    :param request: current webservers request
    :return: dict()
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Export', 'get_doj_dump', 'def')
    m = request.matchdict
    issue = m['issue'][0] if 'issue' in m and len(m['issue']) > 0 else None

    return get_doj_data(issue)


@table_row.get()
def get_table_row(request):
    """
    Coming soon

    :param request: current webservers request
    :return: dict()
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Export', 'get_table_row', 'def: {}'.format(request.matchdict))
    matchdict = request.matchdict
    table = matchdict['table'] if 'table' in matchdict else None
    ids = matchdict['ids'] if 'table' in matchdict else None

    return get_table_rows(request.authenticated_userid, table, ids)
