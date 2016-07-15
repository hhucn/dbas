"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.views import Dbas
from dbas.views import project_name

import json
import gevent
import time
import math

from cornice import Service
from dbas.logger import logger
from dbas.lib import get_language
from pyramid.threadlocal import get_current_registry
from dbas.helper.dictionary_helper import DictionaryHelper

from socketio import socketio_manage
from socketio.namespace import BaseNamespace

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

test_data = Service(name='test',
                    path='/test',
                    renderer='templates/test.pt',
                    description="Test Dump",
                    permission='everybody',  # or permission='use'
                    cors_policy=cors_policy)

# =============================================================================
# SOCKETIO STUFF
# =============================================================================


# Namespace
class SomeNamespace(BaseNamespace):
    def initialize(self):
        print('INIT!')

    def on_boo(self):
        print('Boo')
        self.emit('Boo back')

    def job_send_sine(self):
        cnt = 0
        while True:
            cnt += 1
            tm = time.time()
            self.emit('sine', {'value': (tm * 1000, math.sin(tm))})
            gevent.sleep(1)


# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================

@test_data.get()
def socketio(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'socketio', 'main')

    ui_locales = get_language(request, get_current_registry())
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.authenticated_userid, request)

    # socketio_manage(request.environ,
    #                {'/test': SomeNamespace},
    #                request=request)

    return {
        'layout': Dbas.base_layout(),
        'language': str(ui_locales),
        'title': 'Admin',
        'project': project_name,
        'extras': extras_dict,
        'value': 'environ[socketio] = ' + (request.environ['socketio'] if 'socketio' in request.environ else 'Nope')
    }
