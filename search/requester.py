import requests

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.url_manager import UrlManager
from search.routes import get_statements_with_value_path, get_duplicates_or_reasons_path, \
    get_edits_path, get_suggestions_path


def request_as_json(query):
    return requests.get(url=query).json()


def get_suggestions(issue_uid: int, is_start_point: bool, search=""):
    query = get_suggestions_path(issue_uid, is_start_point, search)
    return request_as_json(query)


def get_statements_with_value(issue_uid: int, application_url, search=""):
    query = get_statements_with_value_path(issue_uid, search)
    slug = DBDiscussionSession.query(Issue).get("4").slug
    _um = UrlManager(application_url, for_api=False, slug=slug)

    results = []
    current_results = request_as_json(query)
    for result in current_results:
        new_content = {
            "text": result["text"],
            "statement_uid": result["statement_uid"],
            "content": result["content"],
            "score": result["score"],
            "url": _um.get_url_for_statement_attitude(False, result["statement_uid"])
        }
        results.append(new_content)
    return results


def get_duplicates_or_reasons(issue_uid: int, statement_uid: int, search=""):
    query = get_duplicates_or_reasons_path(issue_uid, statement_uid, search)
    return request_as_json(query)


def get_edits(issue_uid: int, statement_uid: int, search=""):
    query = get_edits_path(issue_uid, statement_uid, search)
    return request_as_json(query)
