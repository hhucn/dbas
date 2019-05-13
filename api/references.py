"""
Handle references from other websites, prepare, store and load them into D-BAS.
"""
from typing import List

import transaction

from api.models import DataReferenceWithStatement
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReference, User, Issue, Statement
from dbas.lib import escape_string
from .lib import logger

log = logger()


def store_reference(reference: str, host: str, path: str, user: User, statement: Statement,
                    issue: Issue) -> StatementReference:
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
    db_ref: StatementReference = StatementReference(escape_string(reference_text), host, path, user.uid,
                                                    statement.uid, issue.uid)
    DBDiscussionSession.add(db_ref)
    DBDiscussionSession.flush()
    transaction.commit()
    return db_ref


# =============================================================================
# Getting references from database
# =============================================================================

def get_all_references_by_reference_text(ref_text: str) -> List[DataReferenceWithStatement]:
    """
    Query database for all occurrences of a given reference text. Prepare list with information about
    used issue, author and a url to the statement.

    :param ref_text: Reference text
    :return: list of used references
    """
    matched: List[StatementReference] = DBDiscussionSession.query(StatementReference).filter(
        StatementReference.text == ref_text).all()
    return [DataReferenceWithStatement(reference) for reference in matched]
