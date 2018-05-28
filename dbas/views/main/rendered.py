import pkg_resources
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config, forbidden_view_config

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler import news as news_handler, user
from dbas.handler.language import set_language_for_visit, get_language_from_cookie
from dbas.handler.rss import get_list_of_all_feeds
from dbas.helper.decoration import prep_extras_dict
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import is_integer
from dbas.lib import escape_string, nick_of_anonymous_user, get_changelog
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.user import valid_user, valid_user_optional
from dbas.views.helper import main_dict, name, full_version


@view_config(route_name='main_page', renderer='../../templates/index.pt', permission='everybody')
@forbidden_view_config(renderer='../../templates/index.pt')
@validate(check_authentication, prep_extras_dict)
def main_page(request):
    """
    View configuration for the main page

    :param request: current request of the server
    :return: HTTP 200 with several information
    """
    logger('main_page', 'request.matchdict: {}'.format(request.matchdict))

    set_language_for_visit(request)
    session_expired = 'session_expired' in request.params and request.params['session_expired'] == 'true'
    ui_locales = get_language_from_cookie(request)

    prep_dict = main_dict(request, name + ' ' + full_version)
    prep_dict.update({
        'session_expired': session_expired,
        'news': news_handler.get_latest_news(ui_locales)
    })
    return prep_dict


@view_config(route_name='main_settings', renderer='../../templates/settings.pt', permission='use')
@validate(valid_user, check_authentication, prep_extras_dict)
def main_settings(request):
    """
    View configuration for the personal settings view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_settings', 'main: {}'.format(request.params))

    ui_locales = get_language_from_cookie(request)
    old_pw, new_pw, confirm_pw, message = '', '', '', ''
    success, error = False, False
    db_user = request.validated['user']

    if 'form.passwordchange.submitted' in request.params:
        old_pw = escape_string(request.params['passwordold'])
        new_pw = escape_string(request.params['password'])
        confirm_pw = escape_string(request.params['passwordconfirm'])

        message, success = user.change_password(db_user, old_pw, new_pw, confirm_pw, ui_locales)
        error = not success

    settings_dict = DictionaryHelper(ui_locales).prepare_settings_dict(success, old_pw, new_pw, confirm_pw, error,
                                                                       message, db_user, request.application_url,
                                                                       request.decorated['extras']['use_with_ldap'])

    prep_dict = main_dict(request, Translator(ui_locales).get(_.settings))
    prep_dict.update({
        'settings': settings_dict
    })
    return prep_dict


@view_config(route_name='main_notification', renderer='../../templates/notifications.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def main_notifications(request):
    """
    View configuration for the notification view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_notifications', 'main')
    _tn = Translator(get_language_from_cookie(request))
    return main_dict(request, _tn.get(_.message))


@view_config(route_name='main_news', renderer='../../templates/news.pt', permission='everybody')
@validate(valid_user_optional, check_authentication, prep_extras_dict)
def main_news(request):
    """
    View configuration for the news.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_news', 'main')

    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    is_author = db_user.is_admin() or db_user.is_author()

    prep_dict = main_dict(request, 'News')
    prep_dict.update({
        'is_author': is_author,
        'news': news_handler.get_news(ui_locales)
    })
    return prep_dict


@view_config(route_name='main_user', renderer='../../templates/user.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_user(request):
    """
    View configuration for the public user page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    match_dict = request.matchdict
    logger('main_user', 'request.matchdict: {}'.format(match_dict))

    uid = match_dict.get('uid', 0)
    logger('main_user', 'uid: {}'.format(uid))

    if not is_integer(uid):
        raise HTTPNotFound

    current_user = DBDiscussionSession.query(User).get(uid)
    if current_user is None or current_user.nickname == nick_of_anonymous_user:
        logger('main_user', 'no user: {}'.format(uid), error=True)
        raise HTTPNotFound()

    ui_locales = get_language_from_cookie(request)
    user_dict = user.get_information_of(current_user, ui_locales)

    db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    can_send_notification = False
    if db_user_of_request:
        can_send_notification = current_user.uid != db_user_of_request.uid

    prep_dict = main_dict(request, user_dict['public_nick'])
    prep_dict.update({
        'user': user_dict,
        'can_send_notification': can_send_notification
    })
    return prep_dict


@view_config(route_name='main_imprint', renderer='../../templates/imprint.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_imprint(request):
    """
    View configuration for the imprint.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_imprint', 'main')
    # add version of pyramid
    request.decorated['extras'].update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

    prep_dict = main_dict(request, Translator(get_language_from_cookie(request)).get(_.imprint))
    prep_dict.update({'imprint': get_changelog(5)})
    return prep_dict


@view_config(route_name='main_privacy', renderer='../../templates/privacy.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_privacy(request):
    """
    View configuration for the privacy.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_privacy', 'main')
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.privacy_policy))


@view_config(route_name='main_faq', renderer='../../templates/faq.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_faq(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_faq', 'main')
    return main_dict(request, 'FAQ')


@view_config(route_name='main_experiment', renderer='../../templates/fieldtest.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_experiment(request):
    """
    View configuration for fieldtest.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_experiment', 'main')
    ui_locales = get_language_from_cookie(request)
    return main_dict(request, Translator(ui_locales).get(_.fieldtest))


@view_config(route_name='main_docs', renderer='../../templates/docs.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_docs(request):
    """
    View configuration for the documentation.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_docs', 'main')
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.docs))


@view_config(route_name='main_rss', renderer='../../templates/rss.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_rss(request):
    """
    View configuration for the RSS feed.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_rss', 'main')
    ui_locales = get_language_from_cookie(request)
    rss = get_list_of_all_feeds(ui_locales)

    prep_dict = main_dict(request, 'RSS')
    prep_dict.update({'rss': rss})
    return prep_dict
