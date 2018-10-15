"""
General validators with no need for a specific namespace.
"""

from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Language, User
from dbas.handler.language import get_language_from_cookie
from dbas.handler.user import update_last_action
from dbas.lib import escape_string
from dbas.strings.fuzzy_modes import FuzzyMode
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.lib import add_error, escape_if_string


def valid_language(request):
    """
    Given a nickname of a user, return the object from the database.

    :param request:
    :return:
    """
    lang = escape_if_string(request.json_body, 'lang')
    _tn = Translator(get_language_from_cookie(request))
    if not lang:
        add_error(request, 'Invalid language', _tn.get(_.checkLanguage))
        return False

    db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=lang).first()
    if db_lang:
        request.validated['lang'] = db_lang
        return True
    else:
        add_error(request, 'Invalid language {}'.format(lang), _tn.get(_.checkLanguage))
        return False


def valid_lang_cookie_fallback(request):
    """
    Get provided language from form, else interpret it from the request.

    :param request:
    :return:
    """
    lang = escape_if_string(request.json_body, 'lang')
    if not lang:
        lang = get_language_from_cookie(request)
    request.validated['lang'] = lang


def check_authentication(request):
    """
    Checks whether the user is authenticated and if user gets logged out.

    :param request:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    session_expired = update_last_action(db_user)
    if session_expired:
        request.session.invalidate()
        headers = forget(request)
        location = request.application_url + 'discuss?session_expired=true',
        raise HTTPFound(
            location=location,
            headers=headers
        )


def valid_fuzzy_search_mode(request):
    """
    Validate fuzzy search modes.

    :param request:
    :return:
    """
    mode = request.json_body['type']
    if mode in list(FuzzyMode):
        request.validated['type'] = mode
        return True
    else:
        add_error(request, 'Invalid fuzzy mode')
        return False


def valid_q_parameter(request):
    """
    Validate that a q-GET parameter is given.

    :param request: Request
    :return:
    """
    query_string: str = request.params.get('q')
    if not query_string:
        add_error(request, 'GET-Parameter \'q\' is missing or empty',
                  'Provide a \'q\'-GET Parameter, which is the query-string to search in the database',
                  location='querystring')
        return False
    request.validated['query'] = escape_string(query_string)
    return True
