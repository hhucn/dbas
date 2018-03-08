import requests

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.helper.url import UrlManager
from search.routes import get_statements_with_value_path, get_duplicates_or_reasons_path, \
    get_edits_path, get_suggestions_path


def request_as_json(query: str) -> dict:
    """
    Request with a certain query and return the result as a dict.

    :param query: path to search at
    :return: return results as a dict
    """
    return requests.get(query).json()


def get_suggestions(issue_uid: int, position: bool, search_value: str = "") -> dict:
    """
    Return the search results for suggestions of the textversions of statements fitting
    the parametes.

    :param issue_uid: uid of the issue to search in
    :param position: the position of the statement
    :param search_value: the text to be searched for
    :return: suggestions of the textversions fitting the given parameters
    """
    query = get_suggestions_path(issue_uid, position, search_value)
    return request_as_json(query)["result"]


def get_statements_with_value(issue_uid: int, search_value: str = "") -> list:
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
    current_results = request_as_json(query)["result"]
    if current_results is not None:
        results = list(map(lambda res: {
            "text": res["text"],
            "statement_uid": res["statement_uid"],
            "content": res["content"],
            "score": res["score"],
            "url": _um.get_url_for_statement_attitude(res["statement_uid"])
        }, current_results))

    return results


def get_duplicates_or_reasons(issue_uid: int, statement_uid: int, search_value: str = "") -> dict:
    """
    This method returns suggestions for duplicated or reasoned statements.

    :param issue_uid: uid of the issue to search in
    :param statement_uid: uid of the statement which is supposed to be a duplicate or reason
    :param search_value: text to be searched for
    :return: duplicates or reasons fitting the parameters
    """
    query = get_duplicates_or_reasons_path(issue_uid, statement_uid, search_value)
    return request_as_json(query)["result"]


def get_edits(issue_uid: int, statement_uid: int, search_value=""):
    """
    This method returns suggestions for edits fitting a the parameters.

    :param issue_uid: uid of the issue to search in
    :param statement_uid: uid of the statement with edits
    :param search_value: text to be searched for
    :return: edits fitting the parameters
    """
    query = get_edits_path(issue_uid, statement_uid, search_value)
    return request_as_json(query)["result"]
