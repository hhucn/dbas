# Handle references from other websites, prepare, store and load them into DBAS-
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

from dbas import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences
from .lib import logger

log = logger()


def store_reference(api_data):
    """
    Validate provided reference and store it in the database.

    .. todo::

        Sanitize input, issue #2

    :param api_data:
    :return:
    """
    try:
        reference = api_data["reference"]
        if not reference or len(reference) < 1:
            return  # Early exit if there is no reference

        user_uid = api_data["user_uid"]
        origin = api_data["origin"]
        statement_uid = api_data["arg_uid"] if api_data["arg_uid"] is not None else api_data["conclusion_id"]
        issue_uid = api_data["issue_id"]

        db_ref = StatementReferences(reference, origin, user_uid, statement_uid, issue_uid)
        DBDiscussionSession.add(db_ref)
        DBDiscussionSession.flush()
        log.debug("[API/Reference] Successfully saved reference for statement.")
    except KeyError:
        log.error("[API/Reference] KeyError: could not access field in api_data.")
