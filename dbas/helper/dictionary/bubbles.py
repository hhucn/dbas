import logging

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import MarkedStatement, Statement
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital


def get_user_bubble_text_for_justify_statement(stmt_uid, db_user, is_supportive, _tn):
    """
    Returns user text for a bubble when the user has to justify a statement and text for the add-position-container

    :param stmt_uid: Statement.uid
    :param db_user: User
    :param is_supportive: Boolean
    :param _tn: Translator
    :return: String, String
    """
    log = logging.getLogger(__name__)
    log.debug("%s is supportive? %s", stmt_uid, is_supportive)
    statement = DBDiscussionSession.query(Statement).get(stmt_uid)
    text = statement.get_text()

    if _tn.get_lang() == 'de':
        intro = _tn.get(_.itIsTrueThat if is_supportive else _.itIsFalseThat)
        add_premise_text = start_with_capital(intro) + ' ' + text
    else:
        add_premise_text = start_with_capital(text) + ' ' + _tn.get(
            _.holds if is_supportive else _.isNotAGoodIdea).strip()
    add_premise_text += ', ...'

    is_users_opinion = False
    if db_user:
        db_marked_statement = DBDiscussionSession.query(MarkedStatement).filter(
            MarkedStatement.statement_uid == stmt_uid,
            MarkedStatement.author_uid == db_user.uid
        ).first()
        is_users_opinion = db_marked_statement is not None

    if is_users_opinion:
        intro = _tn.get(_.youHaveTheOpinionThat)
        outro = '' if is_supportive else ', ' + _tn.get(_.isNotAGoodIdea)
        text = intro.format(text) + outro

        return text, add_premise_text

    if is_supportive:
        intro = _tn.get(_.youAgreeWith) if _tn.get_lang() == 'de' else '{}'
    else:
        intro = _tn.get(_.youDisagreeWith)
    text = intro.format(text)

    return text, add_premise_text


def get_system_bubble_text_for_justify_statement(is_supportive, _tn, tag_start, text, tag_end):
    """
    Returns system text for a bubble when the user has to justify a statement and text for the add-position-container

    :param is_supportive: Boolean
    :param _tn: Translator
    :param tag_start: String
    :param text: String
    :param tag_end: String
    :return: String
    """
    if _tn.get_lang() == 'de':
        if is_supportive:
            question = _tn.get(_.whatIsYourMostImportantReasonWhyForInColor)
        else:
            question = _tn.get(_.whatIsYourMostImportantReasonWhyAgainstInColor)
    else:
        question = _tn.get(_.whatIsYourMostImportantReasonWhyFor)

    question += ' ' + tag_start + text + tag_end

    if _tn.get_lang() != 'de':
        question += ' ' + _tn.get(_.holdsInColor if is_supportive else _.isNotAGoodIdeaInColor)
    because = start_with_capital(_tn.get(_.because)) + '...'
    question += '? <br>' + because

    return question
