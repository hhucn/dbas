# Handle references from other websites, prepare, store and load them into DBAS-
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de
import transaction

from dbas import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences
from .lib import escape_html, logger

log = logger()


def store_reference(api_data, statement_uid=None):
    """
    Validate provided reference and store it in the database.
    :param api_data:
    :param statement_uid:
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
        origin = escape_html(api_data["origin"])
        issue_uid = api_data["issue_id"]

        db_ref = StatementReferences(escape_html(reference), origin, user_uid, statement_uid, issue_uid)
        DBDiscussionSession.add(db_ref)
        DBDiscussionSession.flush()
        transaction.commit()
        log.debug("[API/Reference] Successfully saved reference for statement.")
    except KeyError:
        log.error("[API/Reference] KeyError: could not access field in api_data.")
