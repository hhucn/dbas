"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from cornice import Service
from pyramid_mailer import get_mailer
from dbas.handler.language import get_language_from_cookie
from dbas.logger import logger
from dbas.validators.user import valid_user_as_admin, invalid_user
from dbas.views import base_layout, validate
from dbas.views import project_name
from dbas.handler.email import send_mail
from dbas.helper.dictionary.main import DictionaryHelper

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
debug_mail = Service(name='mail',
                     path='debug_mail',
                     description="Debug Mail",
                     renderer='json',
                     permission='admin',
                     cors_policy=cors_policy)

path = '/{url:.*}add',

# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================


@debug_data.get()
@validate(invalid_user)
def debug_function(request):
    """
    Minimal debug interface for the websocket

    :param request: current webservers reqquest
    :return: dict()
    """
    logger('Websocket', 'main')

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.validated['user'])

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Debug Socket.IO Connection',
        'project': project_name,
        'extras': extras_dict,
        'is_admin': request.validated['user'].is_admin()
    }


@debug_mail.get()
@validate(valid_user_as_admin)
def debug_that_mail(request):
    """

    :param request:
    :return:
    """
    logger('Websocket', 'debug_mail')
    text = request.get('text', 'empty text input')
    logger('Websocket', 'you got access: {}'.format(text))
    send_mail(get_mailer(request), '[D-BAS] Debug Mail', 'Debug: {}'.format(text), request.validated['user'].email, 'en')
    return {'success': True}
