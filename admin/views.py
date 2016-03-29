# Introducing an API to enable exports
#
# @author Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import json, transaction
from admin.lib import argument_overview
from cornice import Service
from dbas.dictionary_helper import DictionaryHelper
from dbas.query_helper import QueryHelper
from dbas.logger import logger
from dbas.user_management import UserHandler
from dbas.views import project_name
from pyramid.threadlocal import get_current_registry
from pyramid.view import view_config

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

# main_page = Service(name='main_page',
#                     path='/main',
#                     description="Admin Page",
#                     cors_policy=cors_policy)

all_arguments = Service(name='admin',
                            path='/argument_overview',
                            description="Argument Overview",
                            cors_policy=cors_policy)


# =============================================================================
# EXPORT-RELATED REQUESTS
# =============================================================================

# @view_config(renderer='dbas/templates/admin.pt', permission='everybody')  # or permission='use'
# @main_page.get()
# def main_admin(self):
# 	"""
# 	View configuration for the content view. Only logged in user can reach this page.
# 	:return: dictionary with title and project name as well as a value, weather the user is logged in
# 	"""
# 	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
# 	logger('main_admin', 'def', 'main')
# 	should_log_out = UserHandler().update_last_action(transaction, self.request.authenticated_userid)
# 	if should_log_out:
# 		return self.user_logout(True)
#
# 	_qh = QueryHelper()
# 	ui_locales = _qh.get_language(self.request, get_current_registry())
# 	extras_dict = DictionaryHelper().prepare_extras_dict('', False, False, False, False, False, False, ui_locales, self.request.authenticated_userid)
# 	users = _qh.get_all_users(self.request.authenticated_userid, ui_locales)
# 	dashboard = _qh.get_dashboard_infos()
#
# 	return {
# 		'layout': self.base_layout(),
# 		'language': str(ui_locales),
# 		'title': 'Admin',
# 		'project': project_name,
# 		'extras': extras_dict,
# 		'users': users,
# 		'dashboard': dashboard
# 	}


@all_arguments.get()
def get_argument_overview(request):
	logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
	logger('Admin', 'get_argument_overview', 'main')
	_qh = QueryHelper()
	ui_locales = _qh.get_language(request, get_current_registry())
	return_dict = argument_overview(request.authenticated_userid, ui_locales)

	return json.dumps(return_dict, True)
