import logging
from pyramid.view import view_config

import dbas.review
import dbas.review.queue
from dbas.handler.language import get_language_from_cookie
from dbas.helper.decoration import prep_extras_dict
from dbas.review.history import get_ongoing_reviews, get_review_history
from dbas.review.mapper import get_title_by_key
from dbas.review.queue.abc_queue import subclass_by_name
from dbas.review.queue.adapter import QueueAdapter
from dbas.review.reputation import get_reputation_of, get_privilege_list, get_reputation_reasons_list, \
    get_history_of
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.reviews import valid_review_queue_name, valid_user_has_review_access
from dbas.validators.user import valid_user
from dbas.views.helper import main_dict

LOG = logging.getLogger(__name__)


@view_config(route_name='review_index', renderer='../../templates/review/index.pt', permission='use')
@validate(check_authentication, valid_user, prep_extras_dict)
def index(request):
    """
    View configuration for the review index.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Review Index: %s / %s", request.matchdict, request.params)
    db_user = request.validated['user']

    _tn = Translator(get_language_from_cookie(request))
    adapter = QueueAdapter(db_user=db_user, main_page=request.application_url, translator=_tn)
    review_dict = adapter.get_review_queues_as_lists()
    count, all_rights = get_reputation_of(db_user)

    prep_dict = main_dict(request, _tn.get(_.review))
    prep_dict.update({
        'review': review_dict,
        'privilege_list': get_privilege_list(_tn),
        'reputation_list': get_reputation_reasons_list(_tn),
        'reputation': {
            'count': count,
            'has_all_rights': all_rights
        }
    })
    return prep_dict


@view_config(route_name='review_queue', renderer='../../templates/review/queue.pt', permission='use')
@validate(check_authentication, valid_user, prep_extras_dict, valid_review_queue_name, valid_user_has_review_access)
def queue_details(request):
    """
    View configuration for the review content.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Queue Details %s / %s", request.matchdict, request.params)
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    queue_name = request.validated['queue']
    db_user = request.validated['user']
    application_url = request.application_url

    queue = subclass_by_name(queue_name)
    adapter = QueueAdapter(queue=queue(), db_user=db_user, application_url=application_url, translator=_tn)
    subpage_dict = adapter.get_subpage_of_queue(request.session, queue_name)
    request.session.update(subpage_dict['session'])

    prep_dict = main_dict(request, _tn.get(get_title_by_key(queue_name)))
    prep_dict.update({
        'extras': request.decorated['extras'],
        'subpage': subpage_dict,
        'lock_time': dbas.review.queue.max_lock_time_in_sec
    })
    return prep_dict


@view_config(route_name='review_history', renderer='../../templates/review/history.pt', permission='use')
@validate(check_authentication, valid_user, prep_extras_dict)
def history(request):
    """
    View configuration for the review history.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("View history of a review case. %s / %s", request.matchdict, request.params)
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    specific_history = get_review_history(request.application_url, request.validated['user'], _tn)
    prep_dict = main_dict(request, _tn.get(_.review_history))
    prep_dict.update({'history': specific_history})
    return prep_dict


@view_config(route_name='review_ongoing', renderer='../../templates/review/history.pt', permission='use')
@validate(check_authentication, valid_user, prep_extras_dict)
def ongoing(request):
    """
    View configuration for the current reviews.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Current reviews view. %s / %s", request.matchdict, request.params)
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    specific_history = get_ongoing_reviews(request.application_url, request.validated['user'], _tn)
    prep_dict = main_dict(request, _tn.get(_.review_ongoing))
    prep_dict.update({'history': specific_history})
    return prep_dict


@view_config(route_name='review_reputation', renderer='../../templates/review/reputation.pt', permission='use')
@validate(check_authentication, valid_user, prep_extras_dict)
def reputation(request):
    """
    View configuration for the review reputation_borders.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    LOG.debug("Reputation Borders view. %s / %s", request.matchdict, request.params)
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    reputation_dict = get_history_of(request.validated['user'], _tn)
    prep_dict = main_dict(request, _tn.get(_.reputation))
    prep_dict.update({'reputation': reputation_dict})
    return prep_dict
