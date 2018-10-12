"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import logging

from cornice.util import json_error
from pyramid.view import view_config

import dbas.handler.news as news_handler
import dbas.strings.matcher as fuzzy_string_matcher
from dbas.handler import user
from dbas.handler.language import set_language, get_language_from_cookie
from dbas.handler.references import set_reference, get_references
from dbas.helper.query import generate_short_url
from dbas.lib import escape_string
from dbas.validators.common import valid_language, valid_fuzzy_search_mode
from dbas.validators.core import has_keywords, validate
from dbas.validators.discussion import valid_issue_by_id, valid_statement, valid_text_length_of, valid_any_issue_by_id
from dbas.validators.lib import add_error
from dbas.validators.user import valid_user, valid_user_optional, valid_user_as_author
from search.requester import get_statements_with_similarity_to

LOG = logging.getLogger(__name__)


def __modifiy_discussion_url(prep_dict: dict) -> dict:
    """
    Adds the /discuss prefix for every url entry

    :param prep_dict:
    :return:
    """
    # modify urls for the radio buttons
    for el in prep_dict:
        if el is 'url':
            prep_dict['url'] = '/discuss' + prep_dict['url']
    return prep_dict


# fallback for an empty api route
@view_config(route_name='main_api', renderer='json')
def main_api(request):
    add_error(request, 'Route not found', 'There was no route given')
    return json_error(request)


# ajax - set new issue


# ajax - set seen premisegroup


# ajax - set users opinion


# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################


# ajax - getting changelog of a statement


# ajax - for shorten url
@view_config(route_name='get_shortened_url', renderer='json')
@validate(has_keywords(('url', str)))
def get_shortened_url(request):
    """
    Shortens url with the help of a python lib

    :param request: current request of the server
    :return: dictionary with shortend url
    """
    LOG.debug("Shorten URL")
    return generate_short_url(request.validated['url'])


# ajax - for getting all news
@view_config(route_name='get_news', renderer='json')
def get_news(request):
    """
    ajax interface for getting news

    :param request: current request of the server
    :return: json-set with all news
    """
    LOG.debug("Return News from AJAX")
    return news_handler.get_news(get_language_from_cookie(request))


# ajax - for getting argument infos


# ajax - for getting all users with the same opinion
@view_config(route_name='get_user_with_same_opinion', renderer='json')
@validate(valid_language, valid_user_optional,
          has_keywords(('uids', list), ('is_argument', bool), ('is_attitude', bool), ('is_reaction', bool),
                       ('is_position', bool)))
def get_users_with_opinion(request):
    """
    ajax interface for getting a dump

    :params request: current request of the web  server
    :return: json-set with everything
    """
    LOG.debug("Return a dump via AJAX, for: %s", request.json_body)
    db_lang = request.validated['lang']
    uids = request.json_body.get('uids')
    is_arg = request.validated['is_argument']
    is_att = request.validated['is_attitude']
    is_rea = request.validated['is_reaction']
    is_pos = request.validated['is_position']
    db_user = request.validated['user']
    return user.get_users_with_same_opinion(uids, request.application_url, request.path, db_user, is_arg, is_att,
                                            is_rea, is_pos, db_lang)


@view_config(route_name='get_references', renderer='json')
@validate(has_keywords(('uids', list), ('is_argument', bool)))
def get_reference(request):
    """
    Returns all references for an argument or statement


    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Return references for request: %s", request.json_body)
    uids = request.validated['uids']
    is_argument = request.validated['is_argument']
    return get_references(uids, is_argument, request.application_url)


@view_config(route_name='set_references', renderer='json')
@validate(valid_user, valid_any_issue_by_id, valid_statement('json_body'),
          has_keywords(('reference', str), ('ref_source', str)))
def set_references(request):
    """
    Sets a reference for a statement or an arguments

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Set a reference for a statement or an argument. Request: %s", request.json_body)
    db_statement = request.validated['statement']
    reference = escape_string(request.validated['reference'])
    source = escape_string(request.validated['ref_source'])
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    return set_reference(reference, source, db_user, db_statement, db_issue.uid)


# ########################################
# ADDTIONAL AJAX STUFF # ADDITION THINGS #
# ########################################


# ajax - for language switch
@view_config(route_name='switch_language', renderer='json')
@validate(valid_language)
def switch_language(request):
    """
    Switches the language

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Switching the language: %s", request.json_body)
    lang = set_language(request, request.validated['lang'])
    return {'_LOCALE_': lang}


@view_config(route_name='get_suggestion_with_similarity_to', renderer='json')
def get_suggestion_with_similarity_to(request):
    """
    Get statements an all regarding information to a given search value.
    The results statements which have a similarity to the search value.

    :param request: current request of the server
    :return: List of statements with a similarity to the search value
    """
    value = request.params.get('q')
    return get_statements_with_similarity_to(value)


# ajax - for sending news
@view_config(route_name='send_news', renderer='json')
@validate(valid_user_as_author, valid_text_length_of('title'), valid_text_length_of('text'))
def send_news(request):
    """
    ajax interface for settings news

    :param request: current request of the server
    :return: json-set with new news
    """
    LOG.debug("Set news via AJAX: %s", request.json_body)
    title = escape_string(request.validated['title'])
    text = escape_string(request.validated['text'])
    db_user = request.validated['user']
    return news_handler.set_news(title, text, db_user, request.registry.settings['pyramid.default_locale_name'],
                                 request.application_url)


# ajax - for fuzzy search
@view_config(route_name='fuzzy_search', renderer='json')
@validate(valid_issue_by_id, valid_user_optional, valid_fuzzy_search_mode,
          has_keywords(('value', str), ('statement_uid', int)))
def fuzzy_search(request):
    """
    ajax interface for fuzzy string search

    :param request: request of the web server
    :return: json-set with all matched strings
    """
    LOG.debug("Fuzzy String search for AJAX: %s", request.json_body)

    mode = request.validated['type']
    value = request.validated['value']
    db_issue = request.validated['issue']
    statement_uid = request.validated['statement_uid']
    db_user = request.validated['user']
    prepared_dict = fuzzy_string_matcher.get_prediction(db_user, db_issue, value, mode, statement_uid)
    for part_dict in prepared_dict['values']:
        __modifiy_discussion_url(part_dict)
    return prepared_dict


# ajax - for fuzzy search of nickname
@view_config(route_name='fuzzy_nickname_search', renderer='json')
@validate(valid_user_optional, has_keywords(('value', str)))
def fuzzy_nickname_search(request):
    """
    ajax interface for fuzzy string search

    :param request: request of the web server
    :return: json-set with all matched strings
    """
    LOG.debug("Fuzzy nickname search via AJAX: %s", request.json_body)
    return fuzzy_string_matcher.get_nicknames(request.validated['user'], request.validated['value'])
