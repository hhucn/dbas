from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.history import SessionHistory
from dbas.handler.language import get_language_from_cookie
from dbas.helper.dictionary.main import DictionaryHelper


def prep_extras_dict(request):
    """

    :param view_callable:
    :return:
    """
    ui_locales = get_language_from_cookie(request)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   db_user)
    setattr(request, 'decorated', {})
    request.session.update({'session_history': SessionHistory()})

    request.decorated['extras'] = extras_dict
