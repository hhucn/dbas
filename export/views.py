# Introducing an API to enable exports
#
# @author Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import json

from export.lib import get_dump, get_sigma_export
from cornice import Service
from dbas.lib import get_language
from dbas.query_helper import QueryHelper
from dbas.logger import logger
from pyramid.threadlocal import get_current_registry

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

dump = Service(name='export_dump',
			   path='/dump',
			   description="Database Dump")

sigma = Service(name='export_sigma',
                path='/sigma',
                description="Sigma Dump")


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

@dump.get()
def get_database_dump(request):
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Export', 'get_database_dump', 'main')
	_qh = QueryHelper()
	issue = _qh.get_issue_id(request)
	ui_locales = get_language(request, get_current_registry())

	return_dict = get_dump(issue, ui_locales)

	return json.dumps(return_dict, True)

@sigma.get()
def get_sigma_dump(request):
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Export', 'get_sigma_dump', 'main')
	_qh = QueryHelper()
	issue = _qh.get_issue_id(request)
	ui_locales = get_language(request, get_current_registry())

	return_dict = get_sigma_export(issue, ui_locales)
	return json.dumps(return_dict, True)
