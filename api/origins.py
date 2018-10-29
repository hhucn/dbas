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
    origin = api_data.get("origin")
    if not origin:
        return None

    entity_id = origin.get("entity-id")
    aggregate_id = origin.get("aggregate-id")
    author = origin.get("author")
    version = origin.get("version")

    db_origin = StatementOrigins(entity_id, aggregate_id, version, author, statement_uid)
    if db_origin:
        DBDiscussionSession.add(db_origin)
        DBDiscussionSession.flush()
        transaction.commit()
        return db_origin
