import logging
from typing import Dict

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import TextVersion, Statement, User

LOG = logging.getLogger(__name__)


def propose_new_textversion_for_statement(user: User, statement: Statement, corrected_text: str) -> Dict[str, any]:
    """
    Corrects a statement

    :param user: User requesting user
    :param statement: requested statement
    :param corrected_text: new text
    :return: dict()
    """
    LOG.debug("Entering propose_new_textversion_for_statement with uid: %s", statement.uid)

    while corrected_text.endswith(('.', '?', '!')):
        corrected_text = corrected_text[:-1]

    # duplicate check
    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(
        TextVersion.uid.desc()).all()

    # not a duplicate?
    if not db_textversion:
        textversion = TextVersion(content=corrected_text, author=user, statement=statement)
        DBDiscussionSession.add(textversion)
        DBDiscussionSession.flush()

    return {
        'uid': statement.uid,
        'text': corrected_text
    }
