"""
Handle references from other websites, prepare, store and load them into D-BAS.
"""
from typing import List

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences, User, Issue, TextVersion, Statement
from dbas.helper.url import url_to_statement
from dbas.lib import get_all_arguments_with_text_by_statement_id, escape_string
from .lib import logger

log = logger()


def store_reference(reference: str, host: str, path: str, user: User, statement: Statement,
                    issue: Issue) -> StatementReferences:
    """
    Store reference to database.

    :param reference: String from external website
    :param user: user which adds the reference
    :param host: external website, where the reference comes from
    :param path: path on website to reference
    :param statement: assign reference to this statement
    :param issue: assign issue to reference
    :return: newly stored reference
    """
    reference_text = escape_string(reference)
    log.debug("New Reference for Statement.uid {}: {}".format(statement.uid, reference_text))
    db_ref: StatementReferences = StatementReferences(escape_string(reference_text), host, path, user.uid,
                                                      statement.uid, issue.uid)
    DBDiscussionSession.add(db_ref)
    DBDiscussionSession.flush()
    transaction.commit()
    return db_ref


# =============================================================================
# Getting references from database
# =============================================================================

def get_all_references_by_reference_text(ref_text=None):
    """
    Query database for all occurrences of a given reference text. Prepare list with information about
    used issue, author and a url to the statement.

    :param ref_text: Reference text
    :return: list of used references
    """
    if ref_text:
        refs = list()
        matched: List[StatementReferences] = DBDiscussionSession.query(StatementReferences).filter(
            StatementReferences.reference == ref_text).all()
        for reference in matched:
            textversion: TextVersion = reference.statement.get_textversion()
            statement_url = url_to_statement(reference.issue, reference.statement)
            refs.append({
                "reference": reference,
                "arguments": get_all_arguments_with_text_by_statement_id(reference.statement_uid),
                "statement": {"uid": reference.statement_uid,
                              "url": statement_url,
                              "text": textversion.content}
            })
        return refs
