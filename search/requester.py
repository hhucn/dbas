import logging

import requests

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.helper.url import UrlManager
from dbas.strings.fuzzy_modes import FuzzyMode
from search.routes import get_statements_with_value_path, get_duplicates_or_reasons_path, \
    get_edits_path, get_suggestions_path

LOG = logging.getLogger(__name__)
mechanism = 'elastic'


def response_as_dict(query: str) -> dict:
    """
    Request with a certain query and return the result as a dict.

    :param query: path to search at
    :return: return results as a dict
    """
    LOG.debug("Call %s", query)
    return requests.get(query, timeout=1.0).json()


def get_suggestions(issue_uid: int, position: bool, search_value: str = '') -> dict:
    """
    Return the search results for suggestions of the textversions of statements fitting
    the parametes.

    :param issue_uid: uid of the issue to search in
    :param position: the position of the statement
    :param search_value: the text to be searched for
    :return: suggestions of the textversions fitting the given parameters
    """
    query = get_suggestions_path(issue_uid, position, search_value)
    return response_as_dict(query)['result']


def get_statements_with_value(issue_uid: int, search_value: str = '') -> list:
    """
    This method returns statements fitting the given parametes.
    It returns the result as a list of single dicts containing the information of each result
    with the data: text, statement_uid, content, score, url.

    :param issue_uid: uid of the issue to search in
    :param search_value: the position of the statement
    :return: statements fitting a certain text
    """
    query = get_statements_with_value_path(issue_uid, search_value)
    slug = DBDiscussionSession.query(Issue).get(issue_uid).slug
    _um = UrlManager(slug=slug)

    results = []
    current_results = response_as_dict(query)['result']
    if current_results is not None:
        results = list(map(lambda res: {
            'text': res['text'],
            'statement_uid': res['statement_uid'],
            'html': res['html'],
            'score': res['score'],
            'url': _um.get_url_for_statement_attitude(res['statement_uid'])
        }, current_results))

    return results


def get_duplicates_or_reasons(issue_uid: int, statement_uid: int, search_value: str = '') -> dict:
    """
    This method returns suggestions for duplicated or reasoned statements.

    :param issue_uid: uid of the issue to search in
    :param statement_uid: uid of the statement which is supposed to be a duplicate or reason
    :param search_value: text to be searched for
    :return: duplicates or reasons fitting the parameters
    """
    query = get_duplicates_or_reasons_path(issue_uid, statement_uid, search_value)
    return response_as_dict(query)['result']


def get_edits(issue_uid: int, statement_uid: int, search_value=''):
    """
    This method returns suggestions for edits fitting a the parameters.

    :param issue_uid: uid of the issue to search in
    :param statement_uid: uid of the statement with edits
    :param search_value: text to be searched for
    :return: edits fitting the parameters
    """
    query = get_edits_path(issue_uid, statement_uid, search_value)
    return response_as_dict(query)['result']


def elastic_search(db_issue: Issue, search_value: str, mode: int, statement_uid: int) -> dict:
    """
    This method returns the search results for the specific search modes.
    It requests to search and can therefor cause Connection errors etc.
    This method is used in matcher.

    :param db_issue:  current Issue the user looks at, used to get the uid of the issue to search at
    :param search_value: users value, which should be the base for searching
    :param mode: form of search the user chooses
    :param statement_uid: the uid of the statement to be looked at
    :return: search results of elastic search fitting the specific mode
    """
    return_dict = {'distance_name': mechanism}

    if mode in [FuzzyMode.START_STATEMENT.value, FuzzyMode.START_PREMISE.value]:  # start statement / premise
        return_dict['values'] = get_suggestions(db_issue.uid, mode == 0, search_value)

    elif mode in [FuzzyMode.EDIT_STATEMENT.value]:  # edit statement popup
        return_dict['values'] = get_edits(db_issue.uid, statement_uid, search_value)

    elif mode in [FuzzyMode.ADD_REASON.value, FuzzyMode.FIND_DUPLICATE.value]:  # adding reasons / duplicates
        return_dict['values'] = get_duplicates_or_reasons(db_issue.uid, statement_uid, search_value)

    elif mode in [FuzzyMode.FIND_MERGESPLIT.value, FuzzyMode.FIND_STATEMENT.value]:  # search everything
        return_dict['values'] = get_statements_with_value(db_issue.uid, search_value)

    return return_dict
