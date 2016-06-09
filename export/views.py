"""
Introducing an export manager.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import dbas.helper.issue_helper as IssueHelper

from cornice import Service
from pyramid.threadlocal import get_current_registry

from dbas.lib import get_language
from dbas.logger import logger
from export.lib import get_dump

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

dump = Service(name='export_dump',
			   path='/dump',
			   description="Database Dump")


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

@dump.get()
def get_database_dump(request):
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Export', 'get_database_dump', 'main')
	issue = IssueHelper.get_issue_id(request)
	ui_locales = get_language(request, get_current_registry())

	return_dict = get_dump(issue, ui_locales)

	return json.dumps(return_dict, True)
