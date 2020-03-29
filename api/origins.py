"""
Receive and store statement origins.
"""
from typing import Optional, List

from api.models import DataOrigin
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementOrigins, Statement
from .lib import logger

log = logger()


def _store_origin(origin: DataOrigin, statement: Statement) -> Optional[StatementOrigins]:
    """
    Extract origin of an entity, e.g. a statement, from api_data and store it into the database.
    """
    log.debug("Storing origin from %s by %s for statement %d", str(origin.aggregate_id), str(origin.author),
              statement.uid)

    db_origin: StatementOrigins = StatementOrigins(origin.entity_id, origin.aggregate_id, origin.version,
                                                   origin.author.nickname, statement)
    if db_origin:
        DBDiscussionSession.add(db_origin)
        return db_origin


def add_origin_for_list_of_statements(origin: DataOrigin, list_of_statements: List[Statement]) \
        -> Optional[List[StatementOrigins]]:
    """
    Create a new origin and connect it to the newly created statements.

    :param origin: Describes where the data comes from, if reused
    :param list_of_statements: List of statement_uids containing newly created statements
    :return:
    """
    return [_store_origin(origin, statement) for statement in set(list_of_statements)]
