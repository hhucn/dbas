import logging
from typing import Tuple

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import MarkedStatement, Statement, User
from dbas.helper.html_tags import wrap_in_tag
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital
from dbas.strings.text_generator import tag_type
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


def get_user_bubble_text_for_justify_statement(statement: Statement, user: User, is_supportive: bool,
                                               _tn: Translator) -> Tuple[str, str]:
    """
    Returns user text for a bubble when the user has to justify a statement and text for the add-position-container

    :param statement: The statement that shall be justified
    :param user: The user concerned
    :param is_supportive: Indicates whether the justification is too be supportive
    :param _tn: The default Translator
    :return: The bubble text to be shown as well as the text for the corresponding premise
    """
    LOG.debug("%s is supportive? %s", statement, is_supportive)
    text = statement.get_text()

    if _tn.get_lang() == 'de':
        intro = _tn.get(_.itIsTrueThat if is_supportive else _.itIsFalseThat)
        add_premise_text = start_with_capital(intro) + ' ' + text
    else:
        add_premise_text = start_with_capital(text) + ' ' + _tn.get(
            _.holds if is_supportive else _.isNotAGoodIdea).strip()
    add_premise_text += ', ...'

    is_users_opinion = False
    if user:
        db_marked_statement = DBDiscussionSession.query(MarkedStatement).filter(
            MarkedStatement.statement_uid == statement.uid,
            MarkedStatement.author_uid == user.uid
        ).first()
        is_users_opinion = db_marked_statement is not None

    if is_users_opinion:
        intro = _tn.get(_.youHaveTheOpinionThat)
        outro = '' if is_supportive else ', ' + _tn.get(_.isNotAGoodIdea)
        text = intro.format(text) + outro

        return text, add_premise_text

    if is_supportive:
        intro = _tn.get(_.iAgreeWithX) if _tn.get_lang() == 'de' else '{}'
    else:
        intro = _tn.get(_.iDisagreeWith)
    text = intro.format(text)

    return text, add_premise_text


def get_system_bubble_text_for_justify_statement(is_supportive: bool, _tn: Translator, text: str,
                                                 additional_display_attributes: str) -> str:
    """
    Build system text for a bubble when the user has to justify a statement and text for the add-position-container

    :param is_supportive: Indicates whether the user was supportive in regards to the discussed statement
    :param _tn: The default translator
    :param text: The text that shall be displayed
    :param additional_display_attributes: HTML-Attributes to be added to the starting tag
    :return: The readily build system text in form of a question
    """
    if _tn.get_lang() == 'de':
        if is_supportive:
            question = _tn.get(_.whatIsYourMostImportantReasonWhyForInColor)
        else:
            question = _tn.get(_.whatIsYourMostImportantReasonWhyAgainstInColor)
    else:
        question = _tn.get(_.whatIsYourMostImportantReasonWhyFor)

    question += wrap_in_tag(tag_type, text, additional_display_attributes)

    if _tn.get_lang() != 'de':
        question += ' ' + _tn.get(_.holdsInColor if is_supportive else _.isNotAGoodIdeaInColor)
    because = start_with_capital(_tn.get(_.because)) + '...'
    question += '? <br>' + because

    return question
