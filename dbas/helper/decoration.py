from dbas.handler.language import get_language_from_cookie
from dbas.helper.dictionary.main import DictionaryHelper


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
