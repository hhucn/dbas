"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import json

from dbas.views import Dbas
from dbas.views import project_name

from cornice import Service
from dbas.logger import logger
from dbas.lib import get_language
from pyramid.threadlocal import get_current_registry
from dbas.helper.dictionary_helper import DictionaryHelper

from dbas.database.discussion_model import DBDiscussionSession, User, Settings

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

test_data = Service(name='test',
                    path='/test',
                    renderer='templates/main.pt',
                    description="Test Dump",
                    permission='everybody',  # or permission='use'
                    cors_policy=cors_policy)


# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================

@test_data.get()
def some_function(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'socketio', 'main')

    ui_locales = get_language(request, get_current_registry())
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': 'Admin',
        'project': project_name,
        'extras': extras_dict,
        'value': ':('
    }
