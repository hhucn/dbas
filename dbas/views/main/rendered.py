import pkg_resources
from pyramid.view import view_config, forbidden_view_config

from dbas.handler import news as news_handler
from dbas.handler.language import set_language_for_visit, get_language_from_cookie
from dbas.handler.rss import get_list_of_all_feeds
from dbas.helper.decoration import prep_extras_dict
from dbas.lib import get_changelog
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.user import valid_user_optional
from dbas.views.helper import main_dict, name, full_version


@view_config(route_name='main_page', renderer='../../templates/index.pt', permission='everybody')
@forbidden_view_config(renderer='../../templates/index.pt')
@validate(check_authentication, prep_extras_dict)
def index(request):
    """
    View configuration for the overview page

    :param request: current request of the server
    :return: HTTP 200 with several information
    """
    logger('page', 'request.matchdict: {}'.format(request.matchdict))

    set_language_for_visit(request)
    session_expired = 'session_expired' in request.params and request.params['session_expired'] == 'true'
    ui_locales = get_language_from_cookie(request)

    prep_dict = main_dict(request, name + ' ' + full_version)
    prep_dict.update({
        'session_expired': session_expired,
        'news': news_handler.get_latest_news(ui_locales)
    })
    return prep_dict


@view_config(route_name='main_news', renderer='../../templates/news.pt', permission='everybody')
@validate(valid_user_optional, check_authentication, prep_extras_dict)
def news(request):
    """
    View configuration for the news.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('news', 'main')

    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    is_author = db_user.is_admin() or db_user.is_author()

    prep_dict = main_dict(request, 'News')
    prep_dict.update({
        'is_author': is_author,
        'news': news_handler.get_news(ui_locales)
    })
    return prep_dict


@view_config(route_name='main_imprint', renderer='../../templates/imprint.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def imprint(request):
    """
    View configuration for the imprint.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('imprint', 'main')
    # add version of pyramid
    request.decorated['extras'].update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

    prep_dict = main_dict(request, Translator(get_language_from_cookie(request)).get(_.imprint))
    prep_dict.update({'imprint': get_changelog(5)})
    return prep_dict


@view_config(route_name='main_privacy', renderer='../../templates/privacy.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def privacy(request):
    """
    View configuration for the privacy.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('privacy', 'main')
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.privacy_policy))


@view_config(route_name='main_faq', renderer='../../templates/faq.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def faq(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('faq', 'main')
    return main_dict(request, 'FAQ')


@view_config(route_name='main_experiment', renderer='../../templates/fieldtest.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def experiment(request):
    """
    View configuration for fieldtest.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('experiment', 'main')
    ui_locales = get_language_from_cookie(request)
    return main_dict(request, Translator(ui_locales).get(_.fieldtest))


@view_config(route_name='main_docs', renderer='../../templates/docs.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def docs(request):
    """
    View configuration for the documentation.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('docs', 'main')
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.docs))


@view_config(route_name='main_rss', renderer='../../templates/rss.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def rss(request):
    """
    View configuration for the RSS feed.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('rss', 'main')
    ui_locales = get_language_from_cookie(request)
    rss = get_list_of_all_feeds(ui_locales)

    prep_dict = main_dict(request, 'RSS')
    prep_dict.update({'rss': rss})
    return prep_dict
