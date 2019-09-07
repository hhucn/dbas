import logging

from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render_to_response
from pyramid.view import view_config

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.language import get_language_from_cookie
from dbas.handler.user import get_information_of, change_password
from dbas.helper.decoration import prep_extras_dict
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import is_integer
from dbas.lib import escape_string, checks_if_user_is_ldap_user
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.user import valid_user
from dbas.views.helper import main_dict

LOG = logging.getLogger(__name__)


@view_config(route_name='main_user', renderer='../../templates/user/details.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def user(request):
    """
    View configuration for the public user page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    match_dict = request.matchdict
    LOG.debug("Return public user page: %s", match_dict)

    uid = match_dict.get('uid', 0)
    LOG.debug("User being shown: %s", uid)

    if not is_integer(uid):
        raise HTTPNotFound

    current_user = DBDiscussionSession.query(User).get(uid)
    if current_user is None:
        LOG.error("No user found: %s", uid)
        raise HTTPNotFound()

    ui_locales = get_language_from_cookie(request)
    user_dict = get_information_of(current_user, ui_locales)

    db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    can_send_notification = False
    if db_user_of_request:
        can_send_notification = current_user.uid not in [db_user_of_request.uid, 1]

    prep_dict = main_dict(request, user_dict['public_nick'])
    prep_dict.update({
        'user': user_dict,
        'can_send_notification': can_send_notification
    })
    return prep_dict


@view_config(route_name='main_settings', permission='use')
@validate(valid_user, check_authentication, prep_extras_dict)
def settings(request):
    """
    View configuration for the personal settings view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Show settings %s", request.params)

    renderer = '../../templates/user/settings.pt'
    ui_locales = get_language_from_cookie(request)
    old_pw, new_pw, confirm_pw, message = '', '', '', ''
    success, error = False, False
    db_user: User = request.validated['user']

    if checks_if_user_is_ldap_user(db_user):
        renderer = '../../templates/user/settings_ldap_user.pt'
    else:
        if 'form.passwordchange.submitted' in request.params:
            old_pw = escape_string(request.params['passwordold'])
            new_pw = escape_string(request.params['password'])
            confirm_pw = escape_string(request.params['passwordconfirm'])

            message, success = change_password(db_user, old_pw, new_pw, confirm_pw, ui_locales)
            error = not success

    settings_dict = DictionaryHelper(ui_locales).prepare_settings_dict(success, old_pw, new_pw, confirm_pw, error,
                                                                       message, db_user, request.application_url,
                                                                       request.decorated['extras']['use_with_ldap'])

    prep_dict = main_dict(request, Translator(ui_locales).get(_.settings))
    prep_dict.update({
        'settings': settings_dict
    })

    return render_to_response(renderer, prep_dict, request=request)


@view_config(route_name='main_notification', renderer='../../templates/user/notifications.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def notifications(request):
    """
    View configuration for the notification view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Show Notifications")
    _tn = Translator(get_language_from_cookie(request))
    return main_dict(request, _tn.get(_.message))
