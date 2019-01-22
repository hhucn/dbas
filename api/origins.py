"""
Receive and store statement origins.
"""
from typing import Optional, List, Set

from api.models import DataOrigin
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementOrigins
from .lib import logger

log = logger()


def __store_origin(origin: DataOrigin, statement_uid: int) -> Optional[StatementOrigins]:
    """
    Extract origin of an entity, e.g. a statement, from api_data and store it into the database.
    """
    log.debug("Storing origin from %s by %s for statement %d", str(origin.aggregate_id), str(origin.author),
              statement_uid)

    db_origin: StatementOrigins = StatementOrigins(origin.entity_id, origin.aggregate_id, origin.version,
                                                   origin.author.nickname, statement_uid)
    if db_origin:
        DBDiscussionSession.add(db_origin)
        return db_origin


def add_origin_for_list_of_statements(origin: DataOrigin, list_of_statement_uids: List[int]) \
        -> Optional[List[StatementOrigins]]:
    """
    Create a new origin and connect it to the newly created statements.

    :param origin: Describes where the data comes from, if reused
    :param list_of_statement_uids: List of statement_uids containing newly created statements
    :return:
    """
    if not isinstance(list_of_statement_uids, list):
        return None
    newly_added_statement_uids: Set[int] = set(list_of_statement_uids)
    return [__store_origin(origin, statement_uid) for statement_uid in newly_added_statement_uids]
