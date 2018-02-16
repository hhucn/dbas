from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget

from dbas.handler.language import get_language_from_cookie
from dbas.handler.user import update_last_action
from dbas.helper.dictionary.main import DictionaryHelper


def check_authentication(request):
    """
    Checks whether the user is authenticated and if not logs user out.

    :param view_callable:
    :return:
    """
    session_expired = update_last_action(request.authenticated_userid)
    if session_expired:
        request.session.invalidate()
        headers = forget(request)
        location = request.application_url + 'discuss?session_expired=true',
        raise HTTPFound(
            location=location,
            headers=headers
        )


def prep_extras_dict(request):
    """

    :param view_callable:
    :return:
    """
    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)
    setattr(request, 'decorated', {})
    request.decorated['extras'] = extras_dict
