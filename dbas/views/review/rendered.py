from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

import dbas.review
import dbas.review.helper
from dbas.handler.language import get_language_from_cookie
from dbas.helper.decoration import prep_extras_dict
from dbas.logger import logger
from dbas.review import queues as review_queue_helper, reputation as review_reputation_helper, \
    subpage as review_page_helper, history as review_history_helper
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.user import valid_user_optional, valid_user
from dbas.views.helper import main_dict


@view_config(route_name='review_index', renderer='../../templates/review/index.pt', permission='use')
@validate(check_authentication, prep_extras_dict, valid_user_optional)
def index(request):
    """
    View configuration for the review index.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main', 'def {}'.format(request.matchdict))
    nickname = request.authenticated_userid

    _tn = Translator(get_language_from_cookie(request))
    review_dict = review_queue_helper.get_review_queues_as_lists(request.application_url, _tn, nickname)
    count, all_rights = review_reputation_helper.get_reputation_of(nickname)

    prep_dict = main_dict(request, _tn.get(_.review))
    prep_dict.update({
        'review': review_dict,
        'privilege_list': review_reputation_helper.get_privilege_list(_tn),
        'reputation_list': review_reputation_helper.get_reputation_reasons_list(_tn),
        'reputation': {
            'count': count,
            'has_all_rights': all_rights
        }
    })
    return prep_dict


@view_config(route_name='review_queue', renderer='../../templates/review/queue.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def queue_details(request):
    """
    View configuration for the review content.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('queue_details', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    subpage_name = request.matchdict['queue']
    nickname = request.authenticated_userid
    session = request.session
    application_url = request.application_url

    subpage_dict = review_page_helper.get_subpage_elements_for(nickname, session, application_url, subpage_name, _tn)
    request.session.update(subpage_dict['session'])
    if not subpage_dict['elements'] and not subpage_dict['has_access'] and not subpage_dict['no_arguments_to_review']:
        logger('review_queue', 'subpage error', error=True)
        raise HTTPNotFound()

    title = _tn.get(_.review)
    if subpage_name in dbas.review.title_mapping:
        title = _tn.get(dbas.review.title_mapping[subpage_name])

    prep_dict = main_dict(request, title)
    prep_dict.update({
        'extras': request.decorated['extras'],
        'subpage': subpage_dict,
        'lock_time': dbas.review.max_lock_time_in_sec
    })
    return prep_dict


@view_config(route_name='review_history', renderer='../../templates/review/history.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def history(request):
    """
    View configuration for the review history.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('history', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    request_authenticated_userid = request.authenticated_userid
    _tn = Translator(ui_locales)

    history = review_history_helper.get_review_history(request.application_url, request_authenticated_userid, _tn)
    prep_dict = main_dict(request, _tn.get(_.review_history))
    prep_dict.update({'history': history})
    return prep_dict


@view_config(route_name='review_ongoing', renderer='../../templates/review/history.pt', permission='use')
@validate(valid_user, check_authentication, prep_extras_dict)
def ongoing(request):
    """
    View configuration for the current reviews.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('ongoing', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    history = review_history_helper.get_ongoing_reviews(request.application_url, request.validated['user'], _tn)
    prep_dict = main_dict(request, _tn.get(_.review_ongoing))
    prep_dict.update({'history': history})
    return prep_dict


@view_config(route_name='review_reputation', renderer='../../templates/review/reputation.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def reputation(request):
    """
    View configuration for the review reputation_borders.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('reputation', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    reputation_dict = review_history_helper.get_reputation_history_of(request.authenticated_userid, _tn)
    prep_dict = main_dict(request, _tn.get(_.reputation))
    prep_dict.update({'reputation': reputation_dict})
    return prep_dict
