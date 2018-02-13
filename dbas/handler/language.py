"""
Provides helping function for language changes.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Language
from dbas.logger import logger


def set_language(request, db_lang):
    """
    Saves the new language in the request

    :param request: current request
    :param lang: Language
    :return: dict()
    """
    logger('LanguageHelper', 'set_language', 'setting lang to {}'.format(db_lang.ui_locales))
    request._LOCALE_ = db_lang.ui_locales
    request.response.set_cookie('_LOCALE_', str(db_lang.ui_locales))
    request.cookies['_LOCALE_'] = db_lang.ui_locales
    # we have to set 'ui_locales = get_language_from_cookie(request)' in each view again, because D-BAS is no object
    logger('LanguageHelper', 'set_language', 'switched to {}'.format(db_lang.ui_locales))

    return {'_LOCALE_': db_lang.ui_locales}


def get_language_from_header(request):
    """
    Returns 'de' if 'de' is in requests headers else 'en'

    :param request: current request
    :return: String
    """
    lang = request.headers.get('Accept-Language', '')
    logger('ViewHelper', 'get_language_from_header', 'Accept-Language: {}'.format(lang))
    return 'de' if 'de' in lang else 'en'


def get_language_from_cookie(request):
    """
    Returns current ui locales code which is saved in current cookie or the registry.

    :param request: request
    :return: ui_locales
    """
    try:
        lang = request.cookies['_LOCALE_']
    except (KeyError, AttributeError):
        lang = request.registry.settings['pyramid.default_locale_name']
    request._LOCALE_ = lang
    # we have to set 'ui_locales = get_language_from_cookie(request)' in each view again, because D-BAS is no object
    return str(lang)


def set_language_for_visit(request):
    """
    Sets language and issue uid based on the requests header if there is no _LOCALE_ attribute in the cookie

    :param request: request-dict (necessary, because the language will be set in the cookies dict of the request)
    :return: None
    """

    if '_LOCALE_' in request.cookies:
        logger('ViewHelper', 'set_language_for_first_visit', 'User was already here')
        # user was already here
        return

    logger('ViewHelper', 'set_language_for_first_visit', 'User is first time here')
    ui_locales = get_language_from_header(request)
    lang = DBDiscussionSession.query(Language).filter(ui_locales=ui_locales).first()
    set_language(request, lang)
