"""
Handle references from other websites, prepare, store and load them into D-BAS.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from dbas import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences
from dbas.lib import resolve_issue_uid_to_slug
from dbas.url_manager import UrlManager

from .lib import escape_html, logger

log = logger()


def url_to_statement(issue_uid, statement_uid):
    """
    Generate URL to given statement_uid in specific issue (by slug).
    Used to directly jump into the discussion.

    :param issue_uid: uid of current issue
    :type issue_uid: id
    :param statement_uid: Statement id to generate the link to
    :type statement_uid: int
    :return: Direct URL to jump to the provided statement
    :rtype: str
    """
    slug = resolve_issue_uid_to_slug(issue_uid)
    url_manager = UrlManager(application_url="", slug=slug, for_api=True)
    return url_manager.get_url_for_justifying_statement(as_location_href=True,
                                                        statement_uid=statement_uid,
                                                        mode="t")


def store_reference(api_data, statement_uid=None):
    """
    Validate provided reference and store it in the database.
    Has side-effects.

    .. todo::
        Remove parameter discuss_url and calculate here the correct url

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
        log.debug("[API/Reference] Successfully saved reference for statement.")
    except KeyError:
        log.error("[API/Reference] KeyError: could not access field in api_data.")
