"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import os
import pyramid.httpexceptions as exc
import json

from subprocess import call
from cornice import Service
from dbas.logger import logger

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


# webhook
sass_compiling = Service(name='sass',
                         path='/aqh5lart',
                         description='git sass compiling',
                         permission='use',
                         require_csrf=False,
                         cors_policy=cors_policy)
js_compiling = Service(name='js',
                       path='/ldn29sm3',
                       description='git js compiling',
                       permission='use',
                       require_csrf=False,
                       cors_policy=cors_policy)

# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================


@sass_compiling.get()
def webhook_sass(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Webhook', 'sass', 'main ' + str(os.path.realpath(__file__)))

    try:
        token = request.params['secret_token']
        if token != 'SoMeR34Lb42T0K3N':
            logger('Webhook', 'sass', 'access denied')
            raise exc.HTTPForbidden()
    except Exception:
        logger('Webhook', 'sass', 'access denied')
        raise exc.HTTPForbidden()

    subfile = 'views.py'
    path = str(os.path.realpath(__file__))[:-len(subfile)]

    logger('Webhook', 'sass', 'compiling sass from ' + path)
    try:
        path = path.replace('webhook', 'dbas')
        logger('Webhook', 'sass',
               'Execute: sass ' + path + 'static/css/main.sass ' + path + 'static/css/main.css --style compressed --no-cache')
        ret_val = call(
            ['sass', path + 'static/css/main.sass', path + 'static/css/main.css', '--style', 'compressed',
             '--no-cache'])
        logger('Webhook', 'sass', 'compiling done: ' + str(ret_val))
    except Exception as e:
        ret_val = 1
        logger('Webhook', 'sass', 'compiling failed: ' + str(e))

    return_dict = {'success': 1 if ret_val == 0 else 0, 'error': + ret_val}

    return json.dumps(return_dict, True)


@js_compiling.get()
def webhook_js(request):
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Webhook', 'js', 'main')

    try:
        token = request.params['secret_token']
        if token != 'kIKsj3Nsk2kand53Bla':
            logger('Webhook', 'js', 'access denied')
            raise exc.HTTPForbidden()
    except Exception:
        logger('Webhook', 'js', 'access denied')
        raise exc.HTTPForbidden()

    subfile = 'views.py'
    path = str(os.path.realpath(__file__))[:-len(subfile)]

    logger('Webhook', 'js', 'minify js')
    try:
        path = path.replace('webhook', 'dbas')
        logger('Webhook', 'js', 'Execute: ' + path + 'static/minify.sh')
        ret_val = call([path + 'static/minify.sh'])
        logger('Webhook', 'js', 'minify done: ' + str(ret_val))
    except Exception as e:
        ret_val = 1
        logger('Webhook', 'js', 'minify failed: ' + str(e))

    return_dict = {'success': 1 if ret_val == 0 else 0, 'error': + ret_val}

    return json.dumps(return_dict, True)
