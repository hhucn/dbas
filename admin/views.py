"""
Introducing an admin interface to enable easy database mangement.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import transaction
import dbas.helper.history_helper as HistoryHelper
import dbas.user_management as UserHandler

from cornice import Service
from pyramid.threadlocal import get_current_registry
from admin.lib import get_overview_of_arguments, get_all_users, get_dashboard_infos
from dbas.lib import get_language
from dbas.logger import logger
from dbas.views import Dbas
from dbas.views import project_name
from dbas.helper.dictionary_helper import DictionaryHelper

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

dashboard = Service(name='dashboard_page',
                    path='/main',
                    description="Admin Page",
                    renderer='templates/admin.pt',
                    permission='everybody',  # or permission='use'
                    cors_policy=cors_policy)

all_arguments = Service(name='admin',
                        path='/argument_overview',
                        description="Argument Overview",
                        cors_policy=cors_policy)


@dashboard.get()
def main_admin(request):
	"""
	View configuration for the content view. Only logged in user can reach this page.
	:return: dictionary with title and project name as well as a value, weather the user is logged in
	"""
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Admin', 'main_admin', 'def')
	HistoryHelper.save_path_in_database(request.authenticated_userid, request.path, transaction)
	should_log_out = UserHandler.update_last_action(transaction, request.authenticated_userid)
	if should_log_out:
		return Dbas(request).user_logout(True)

	ui_locales = get_language(request, get_current_registry())
	extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid)
	users = get_all_users(request.authenticated_userid, ui_locales, request.application_url)
	dashboard = get_dashboard_infos()

	return {
		'layout': Dbas.base_layout(),
		'language': str(ui_locales),
		'title': 'Admin',
		'project': project_name,
		'extras': extras_dict,
		'users': users,
		'dashboard': dashboard
 	}


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

@all_arguments.get()
def get_argument_overview(request):
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Admin', 'get_argument_overview', 'main')
	ui_locales = get_language(request, get_current_registry())
	return_dict = get_overview_of_arguments(request.authenticated_userid, ui_locales)

	return json.dumps(return_dict, True)
