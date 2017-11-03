"""
Receive and store statement origins.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementOrigins
from .lib import logger

log = logger()


def store_origin(api_data, statement_uid):
    """
    Extract origin of an entity, e.g. a statement, from api_data and store it into the database.

    :param api_data: user provided data
    :param statement_uid: the statement the origin should be assigned to
    :return:
    """
    entity_id = api_data.get("origin_entity_id")
    aggregate_id = api_data.get("origin_aggregate_id")
    author = api_data.get("origin_author")
    version = api_data.get("origin_version")

    if not (entity_id or aggregate_id or statement_uid):
        log.info("[API/StatementOrigin] No origin of statement provided.")
        return  # Early exit if there is no origin provided

    db_origin = StatementOrigins(entity_id, aggregate_id, author, version, statement_uid)
    DBDiscussionSession.add(db_origin)
    DBDiscussionSession.flush()
    transaction.commit()
    return db_origin
