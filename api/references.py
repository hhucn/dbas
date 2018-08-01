"""
Handle references from other websites, prepare, store and load them into D-BAS.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import transaction

from api.extractor import extract_reference_information, extract_author_information, extract_issue_information
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences, User, Issue, TextVersion
from dbas.helper.url import url_to_statement
from dbas.lib import get_all_arguments_with_text_by_statement_id
from .lib import escape_html, logger

log = logger()


def store_reference(api_data, statement_uid=None):
    """
    Validate provided reference and store it in the database.
    Has side-effects.

    :param api_data: user provided data
    :param statement_uid: the statement the reference should be assigned to
    :return:
    """
    try:
        reference = api_data["reference"]
        if not reference:
            return  # Early exit if there is no reference
        if not statement_uid:
            log.error("[API/Reference] No statement_uid provided.")
            return

        user_uid = api_data["user_uid"]
        host = escape_html(api_data["host"])
        path = escape_html(api_data["path"])
        issue_uid = api_data["issue_id"]

        db_ref = StatementReferences(escape_html(reference), host, path, user_uid, statement_uid, issue_uid)
        DBDiscussionSession.add(db_ref)
        DBDiscussionSession.flush()
        transaction.commit()
        return db_ref
    except KeyError as e:
        log.error("[API/Reference] KeyError: could not access field in api_data. " + repr(e))


# =============================================================================
# Getting references from database
# =============================================================================

def get_complete_reference(ref_id=None):
    """
    Given a reference uid, query all interesting information and retrieve the database objects.

    :param ref_id: StatementReference.uid
    :return: reference, user, issue
    :rtype: tuple
    """
    if ref_id:
        reference = DBDiscussionSession.query(StatementReferences).get(ref_id)
        user = DBDiscussionSession.query(User).get(reference.author_uid)
        issue = DBDiscussionSession.query(Issue).get(reference.issue_uid)
        textversion = DBDiscussionSession.query(TextVersion).get(reference.statement_uid)
        return reference, user, issue, textversion


def get_all_references_by_reference_text(ref_text=None):
    """
    Query database for all occurrences of a given reference text. Prepare list with information about
    used issue, author and a url to the statement.

    :param ref_text: Reference text
    :return: list of used references
    """
    if ref_text:
        refs = list()
        matched = DBDiscussionSession.query(StatementReferences).filter_by(reference=ref_text).all()
        for reference in matched:
            user = DBDiscussionSession.query(User).get(reference.author_uid)
            issue = DBDiscussionSession.query(Issue).get(reference.issue_uid)
            textversion = DBDiscussionSession.query(TextVersion).get(reference.statement_uid)
            statement_url = url_to_statement(issue, reference.statement)
            refs.append({"reference": extract_reference_information(reference),
                         "author": extract_author_information(user),
                         "issue": extract_issue_information(issue),
                         "arguments": get_all_arguments_with_text_by_statement_id(reference.statement_uid),
                         "statement": {"uid": reference.statement_uid,
                                       "url": statement_url,
                                       "text": textversion.content}})
        return refs


def get_references_for_url(host=None, path=None):
    """
    Query database for given URL and return all references.

    :param host: sanitized string of the reference's host
    :type host: str
    :param path: path to article / reference on reference's host
    :type path: str
    :return: list of strings representing quotes from the given site, which were stored in our database
    :rtype: list
    """
    if host and path:
        return DBDiscussionSession.query(StatementReferences).filter_by(host=host, path=path).all()


def get_reference_by_id(ref_id=None):
    """
    Query database to get a reference by its id.

    :param ref_id: StatementReferences.uid
    :return: StatementReference
    """
    if ref_id:
        return DBDiscussionSession.query(StatementReferences).get(ref_id)
