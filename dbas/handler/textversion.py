import logging

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, TextVersion


def propose_new_textversion_for_statement(db_user, uid, corrected_text):
    """
    Corrects a statement

    :param db_user: User requesting user
    :param uid: requested statement uid
    :param corrected_text: new text
    :return: dict()
    """
    log = logging.getLogger(__name__)
    log.debug("Entering propose_new_textversion_for_statement with uid: %s", uid)

    while corrected_text.endswith(('.', '?', '!')):
        corrected_text = corrected_text[:-1]

    # duplicate check
    return_dict = dict()
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=corrected_text).order_by(
        TextVersion.uid.desc()).all()

    # not a duplicate?
    if not db_textversion:
        textversion = TextVersion(content=corrected_text, author=db_user.uid)
        textversion.set_statement(db_statement.uid)
        DBDiscussionSession.add(textversion)
        DBDiscussionSession.flush()

    return_dict['uid'] = uid
    return_dict['text'] = corrected_text
    return return_dict
