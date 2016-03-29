# Introducing an API to enable exports
#
# @author Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import json

from admin.lib import argument_overview
from cornice import Service
from dbas.query_helper import QueryHelper
from dbas.logger import logger
from pyramid.threadlocal import get_current_registry

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

all_arguments = Service(name='overview_of_arguments',
                            path='/argument_overview',
                            description="Database Dump",
                            cors_policy=cors_policy)


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

@all_arguments.get()
def get_argument_overview(request):
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Admin', 'get_argument_overview', 'main')
	_qh = QueryHelper()
	ui_locales = _qh.get_language(request, get_current_registry())
	return_dict = argument_overview(request.authenticated_userid, ui_locales)

	return json.dumps(return_dict, True)
