import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Premise, Argument
from dbas.logger import logger


def set_able_object_of_review(review, is_disabled):
    """
    En- or -disable a specific review, this affects all the statements and arguments

    :param review: Review
    :param is_disabled: boolean
    :return: None
    """
    logger('review_main_helper', str(review.uid) + ' ' + str(is_disabled))
    if review.statement_uid is not None:
        __set_able_of_reviews_statement(review, is_disabled)
    else:
        __set_able_of_reviews_argument(review, is_disabled)


def __set_able_of_reviews_statement(review, is_disabled):
    """
    En- or -disable a specific review, this affects all the statements

    :param review: Review
    :param is_disabled: boolean
    :return: None
    """
    logger('review_main_helper', str(review.uid) + ' ' + str(is_disabled))
    db_statement = DBDiscussionSession.query(Statement).get(review.statement_uid)
    db_statement.set_disabled(is_disabled)
    DBDiscussionSession.add(db_statement)
    db_premises = DBDiscussionSession.query(Premise).filter_by(statement_uid=review.statement_uid).all()

    for premise in db_premises:
        premise.set_disabled(is_disabled)
        DBDiscussionSession.add(premise)

    DBDiscussionSession.flush()
    transaction.commit()


def __set_able_of_reviews_argument(review, is_disabled):
    """
    En- or -disable a specific review, this affects all the arguments

    :param review: Review
    :param is_disabled: boolean
    :return: None
    """
    logger('review_main_helper', str(review.uid) + ' ' + str(is_disabled))
    db_argument = DBDiscussionSession.query(Argument).get(review.argument_uid)
    db_argument.set_disabled(is_disabled)
    DBDiscussionSession.add(db_argument)
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).all()

    for premise in db_premises:
        db_statement = DBDiscussionSession.query(Statement).get(premise.statement_uid)
        db_statement.set_disabled(is_disabled)
        premise.set_disabled(is_disabled)
        DBDiscussionSession.add(premise)

    if db_argument.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)
        db_statement.set_disabled(is_disabled)
        DBDiscussionSession.add(db_statement)

    DBDiscussionSession.flush()
    transaction.commit()
