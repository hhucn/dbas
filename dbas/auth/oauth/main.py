from dbas.auth.oauth import google as google, github, facebook, twitter
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Group
from dbas.handler import user
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def login_oauth_user(request, service, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param service: name of the oauth service
    :param redirect_uri:
    :param old_redirect: redirect_url without modifications
    :param ui_locales:
    :return:
    """
    logger('Auth.Login', 'service: {}'.format(service))
    providers = {
        'google': google,
        'github': github,
        'facebook': facebook,
        'twitter': twitter
    }
    keywords = {
        'google': ['state', 'code'],
        'github': ['code'],
        'facebook': ['state', 'code'],
        'twitter': ['code']
    }

    provider = providers.get(service)
    keyword = keywords.get(service)

    if provider and keyword:
        return __do_oauth(request, service, provider, keyword, redirect_uri, old_redirect, ui_locales)

    return None


def __do_oauth(request, service, provider, keywords, redirect_uri, old_redirect, ui_locales):
    """

    :param request:
    :param service:
    :param provider:
    :param keywords:
    :param redirect_uri:
    :param old_redirect:
    :param ui_locales:
    :return:
    """
    if all([kw in redirect_uri for kw in keywords]):
        url = '{}/{}'.format(request.application_url, 'discuss').replace('http:', 'https:')
        data = provider.continue_flow(url, redirect_uri, ui_locales)
        if len(data['error']) != 0 or len(data['missing']) != 0:
            return data

        value_dict = __set_oauth_user(data['user'], service, ui_locales)
        if isinstance(value_dict, dict):
            if len(value_dict['error']) != 0:
                return value_dict
        else:
            return value_dict

        return {'status': 'success'}  # api
    else:
        request.session['oauth_redirect_url'] = old_redirect
        return provider.start_flow(request=request, redirect_uri=redirect_uri)


def __set_oauth_user(user_data, service, ui_locales):
    """

    :param user_data:
    :param service:
    :param ui_locales:
    :return:
    """
    _tn = Translator(ui_locales)

    db_group = DBDiscussionSession.query(Group).filter_by(name='users').first()
    if not db_group:
        logger('Auth.Login', 'Error occured')
        return {'error': _tn.get(_.errorTryLateOrContant)}

    ret_dict = user.set_new_oauth_user(user_data, user_data['id'], service, _tn)

    if ret_dict['success']:
        return {'status': 'success'}  # api
    else:
        return {
            'error': ret_dict['error'],
            'success': ret_dict['success']
        }
