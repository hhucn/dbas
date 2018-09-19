import logging
import pkg_resources
from pyramid.httpexceptions import HTTPInternalServerError, HTTPOk
from pyramid.view import view_config, forbidden_view_config

from admin.lib import table_mapper
from dbas.database import DBDiscussionSession
from dbas.handler import news as news_handler
from dbas.handler.language import set_language_for_visit, get_language_from_cookie
from dbas.helper.decoration import prep_extras_dict
from dbas.lib import get_changelog
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.user import valid_user_optional
from dbas.views.helper import main_dict, name, full_version

LOG = logging.getLogger(__name__)


@view_config(route_name='main_page', renderer='../../templates/index.pt', permission='everybody')
@forbidden_view_config(renderer='../../templates/index.pt')
@validate(check_authentication, prep_extras_dict)
def index(request):
    """
    View configuration for the overview page

    :param request: current request of the server
    :return: HTTP 200 with several information
    """
    LOG.debug("Return index page. %s", request.matchdict)

    set_language_for_visit(request)
    session_expired = 'session_expired' in request.params and request.params['session_expired'] == 'true'

    prep_dict = main_dict(request, name + ' ' + full_version)
    prep_dict.update({
        'session_expired': session_expired,
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
    LOG.debug("Return news view.")

    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    is_author = db_user.is_admin() or db_user.is_author()

    prep_dict = main_dict(request, 'News')
    prep_dict.update({
        'is_author': is_author, 'news': news_handler.get_news(ui_locales)

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
    LOG.debug("Return imprint view.")
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
    LOG.debug("Return privacy policy view.")
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.privacy_policy))


@view_config(route_name='main_faq', renderer='../../templates/faq.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def faq(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Return FAQ view.")
    return main_dict(request, 'FAQ')


@view_config(route_name='main_experiment', renderer='../../templates/fieldtest.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def experiment(request):
    """
    View configuration for fieldtest.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Return experiment Information view.")
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
    LOG.debug("Return docs view.")
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.docs))


@view_config(route_name='health', permission='everybody')
def health(_):
    """Traefik health check"""
    try:
        tables = [t['table'] for t in table_mapper.values()]
        list(map(lambda x: DBDiscussionSession.query(x).all(), tables))
    except Exception as e:
        LOG.error("Fatal error: %s", e)
        return HTTPInternalServerError()

    LOG.debug("Everything is fine with the instance health.")
    return HTTPOk(detail='Database can be queried successful')
