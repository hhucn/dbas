from sqlalchemy import and_

from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import MarkedStatement
from dbas.strings.keywords import Keywords as _


def get_user_bubble_text_for_justify_statement(uid, db_user, text, is_supportive, _tn):
    """

    :param uid:
    :param db_user:
    :param text:
    :param is_supportive:
    :param _tn:
    :return:
    """
    logger('BubbleHelper', 'get_user_bubble_text_for_justify_statement', '{} {}'.format(uid, is_supportive))
    if _tn.get_lang() == 'de':
        intro = _tn.get(_.itIsTrueThat if is_supportive else _.itIsFalseThat)
        add_premise_text = intro[0:1].upper() + intro[1:] + ' ' + text
    else:
        add_premise_text = text + ' ' + _tn.get(_.holds if is_supportive else _.isNotAGoodIdea).strip()
    add_premise_text += ', ' + '...'

    is_users_opinion = False
    if db_user:
        db_marked_statement = DBDiscussionSession.query(MarkedStatement).filter(and_(
            MarkedStatement.statement_uid == uid,
            MarkedStatement.author_uid == db_user.uid
        )).first()
        is_users_opinion = db_marked_statement is not None

    if is_users_opinion:
        intro = _tn.get(_.youHaveTheOpinionThat)
        outro = '' if is_supportive else (', ' + _tn.get(_.isNotAGoodIdea))
        text = intro.format(text) + outro
    else:
        if _tn.get_lang() == 'de':
            intro = _tn.get(_.youAgreeWith if is_supportive else _.youDisagreeWith)
        else:
            intro = '{}: ' if is_supportive else _tn.get(_.youDisagreeWith)
        text = intro.format(text)

    return text, add_premise_text


def get_system_bubble_text_for_justify_statement(is_supportive, _tn, tag_start, text, tag_end):
    """

    :param is_supportive:
    :param _tn:
    :param tag_start:
    :param text:
    :param tag_end:
    :return:
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
    because = _tn.get(_.because)[0:1].upper() + _tn.get(_.because)[1:].lower() + '...'
    question += '?' + ' <br>' + because

    return question