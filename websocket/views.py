"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

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

subscribe = Service(name='subscribe',
                    path='/subscribe',
                    description="Subscribe for notifications",
                    permission='use',
                    cors_policy=cors_policy)

unsubscribe = Service(name='unsubscribe',
                      path='/unsubscribe',
                      description="Subscribe for notifications",
                      permission='use',
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


@subscribe.get()
def subscribe_function(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'subscribe_function', 'main')

    nickname = request.authenticated_userid

    try:
        socketid = request.params['socketid']
        success = True
        request.session['iosocketid'] = socketid
    except KeyError as e:
        socketid = 'empty'
        success = False
        logger('Websocket', 'error', repr(e))

    logger('Websocket', 'subscribe_function', 'nickname ' + nickname)
    logger('Websocket', 'subscribe_function', 'socketid ' + socketid)

    return {'nickname': nickname,
            'socketid': socketid,
            'success': success}


@unsubscribe.get()
def unsubscribe_function(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'unsubscribe_function', 'main')

    nickname = request.authenticated_userid

    if 'iosocketid' in request.session and len(request.session['iosocketid']) > 0:
        request.session['iosocketid'] = ''
        success = True
    else:
        success = False

    logger('Websocket', 'unsubscribe_function', 'nickname ' + nickname)

    return {'nickname': nickname,
            'success': success}
