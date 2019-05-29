"""
Handle references from other websites, prepare, store and load them into D-BAS.
"""
from typing import List

import transaction

from api.models import DataReferenceWithStatement
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReference, User, Issue, Statement
from dbas.lib import escape_string, get_all_arguments_with_text_by_statement_id
from .lib import logger, flatten

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

def _extract_unique_arguments(args: List[dict]) -> List[dict]:
    unique_args = list()
    for arg in args:
        if arg not in unique_args:
            unique_args.append(arg)
    return unique_args


def get_all_references_by_reference(reference: StatementReference) -> DataReferenceWithStatement:
    """
    Query database for all occurrences of a given reference text. Prepare a DTO with all arguments, which are
    referring to this reference.

    :param reference: Reference which is being queried.
    :return: list of used references
    """
    matched: List[StatementReference] = DBDiscussionSession.query(StatementReference).filter(
        StatementReference.text == reference.text,
        StatementReference.host == reference.host,
        StatementReference.path == reference.path).all()
    arguments: List[List[dict]] = [get_all_arguments_with_text_by_statement_id(reference.statement_uid)
                                   for reference in matched]
    unique_arguments = _extract_unique_arguments(flatten(arguments))
    return DataReferenceWithStatement(reference, unique_arguments)
