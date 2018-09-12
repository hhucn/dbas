"""
Provides helping function for language changes.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Language
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.logger import logger


def set_language(request, db_lang) -> str:
    """
    Saves the new language in the request

    :param request: current request
    :param lang: Language
    :return: dict()
    """
    logger('LanguageHelper', 'setting lang to {}'.format(db_lang.ui_locales))
    request._LOCALE_ = db_lang.ui_locales
    request.response.set_cookie('_LOCALE_', str(db_lang.ui_locales))
    request.cookies['_LOCALE_'] = db_lang.ui_locales
    # we have to set 'ui_locales = get_language_from_cookie(request)' in each view again, because D-BAS is no object
    logger('LanguageHelper', 'switched to {}'.format(db_lang.ui_locales))

    return db_lang.ui_locales


def get_language_from_header(request):
    """
    Returns the header lang attribute if D-BAS has this one else the default lang

    :param request: current request
    :return: String
    """
    lang = request.headers.get('Accept-Language')
    all_lang = [lang.ui_locales for lang in DBDiscussionSession.query(Language).all()]
    if not lang or lang not in all_lang:
        logger('LanguageHelper', 'No accepted language found in header -> get default lang')
        lang = request.registry.settings['pyramid.default_locale_name']
    logger('LanguageHelper', f'Return {lang}')
    return lang


def get_language_from_cookie(request) -> str:
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


def set_language_for_visit(request) -> str:
    """
    Sets language and issue uid based on the requests header if there is no _LOCALE_ attribute in the cookie

    :param request: request-dict (necessary, because the language will be set in the cookies dict of the request)
    :return: None
    """

    if '_LOCALE_' in request.cookies:
        logger('LanguageHelper', 'User was already here')
        # user was already here
        ui_locales = request.cookies['_LOCALE_']
    else:
        logger('LanguageHelper', 'User is first time here')
        ui_locales = get_language_from_header(request)

    lang = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
    if hasattr(request, 'request'):
        DictionaryHelper(ui_locales).add_language_options_for_extra_dict(request.decorated['extras'])
    return set_language(request, lang)
