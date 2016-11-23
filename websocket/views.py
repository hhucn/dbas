"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from cornice import Service
from dbas.lib import get_language
from dbas.logger import logger
from dbas.views import base_layout
from dbas.views import project_name
from dbas.helper.dictionary.main import DictionaryHelper
from pyramid.threadlocal import get_current_registry

# =============================================================================
# CORS configuration
# =============================================================================
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
                   origins=('*',),
                   max_age=42)

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

debug_data = Service(name='debug',
                     path='/debug',
                     renderer='templates/main.pt',
                     description="Debug Data",
                     permission='everybody',  # or permission='use'
                     cors_policy=cors_policy)


# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================

@debug_data.get()
def debug_function(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'socketio', 'debug_function')

    request_authenticated_userid = request.authenticated_userid
    ui_locales = get_language(request, get_current_registry())
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request, request_authenticated_userid)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Debug Socket.IO Connection',
        'project': project_name,
        'extras': extras_dict
    }
