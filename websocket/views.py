"""
Introducing websockets.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from cornice import Service
from pyramid_mailer import get_mailer
from dbas.handler.language import get_language_from_cookie
from dbas.logger import logger
from dbas.views import base_layout
from dbas.views import project_name
from dbas.handler.user import is_admin
from dbas.handler.email import send_mail
from dbas.helper.dictionary.main import DictionaryHelper

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User

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

path = '/{url:.*}ajax_admin_add',

# =============================================================================
# WEBSOCKET REQUESTS
# =============================================================================


@debug_data.get()
def debug_function(request):
    """
    Minimal debug interface for the websocket

    :param request: current webservers reqquest
    :return: dict()
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'debug_function', 'main')

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Debug Socket.IO Connection',
        'project': project_name,
        'extras': extras_dict,
        'is_admin': is_admin(request.authenticated_userid)
    }


@debug_mail.get()
def debug_that_mail(request):
    """

    :param request:
    :return:
    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Websocket', 'debug_mail', 'debug_mail')
    if request.authenticated_userid in ['Tobias', 'tokra100']:
        text = request.params['text'] if 'text' in request.params else 'empty text input'
        logger('Websocket', 'debug_mail', 'you got access: {}'.format(text))
        db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
        send_mail(get_mailer(request), '[D-BAS] Debug Mail', 'Debug: {}'.format(text), db_user.email, 'en')
        return {'success': True}
    else:
        logger('Websocket', 'debug_mail', 'access denied')
        return {'success': False}
