"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import json
import os
from subprocess import call

from dbas.views import Dbas
from dbas.views import project_name

from cornice import Service
from dbas.logger import logger
from dbas.lib import get_language
from pyramid.threadlocal import get_current_registry
from dbas.helper.dictionary_helper import DictionaryHelper

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

trigger = Service(name='webhook',
                  path='/deploy/aqh5lart',
                  description="Webhook",
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

@trigger.get()
def webhook(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'webhook', 'main ' + str(os.path.realpath(__file__)))

    subfile = 'websocket/views.py'
    path = str(os.path.realpath(__file__))[:-len(subfile)]

    logger('Websocket', 'webhook', 'compiling sass from ' + path)
    try:
        logger('Websocket', 'webhook', 'Execute: sass ' + path + 'dbas/static/css/main.sass ' + path + 'dbas/static/css/main.css --style compressed --no-cache')
        ret_val = call(['sass', path + 'dbas/static/css/main.sass', path + 'dbas/static/css/main.css', '--style', 'compressed', '--no-cache'])
        logger('Websocket', 'webhook', 'compiling done: ' + str(ret_val))
    except Exception:
        ret_val = 1
        logger('Websocket', 'webhook', 'compiling failed')

    return_dict = {'success': 1 if ret_val == 0 else 0}

    return json.dumps(return_dict, True)
