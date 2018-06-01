from typing import Union

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Premise, Argument, ReputationReason
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


def get_reputation_reason_by_action(action: str) -> Union[ReputationReason, None]:
    """
    Returns the reason string from database by its action. Currently we have the following actions:
     - first_position -> rep_reason_first_position
     - first_justification -> rep_reason_first_justification
     - first_argument_click -> rep_reason_first_argument_click
     - first_confrontation -> rep_reason_first_confrontation
     - first_new_argument -> rep_reason_first_new_argument
     - new_statement -> rep_reason_new_statement
     - success_flag -> rep_reason_success_flag
     - success_edit -> rep_reason_success_edit
     - success_duplicate -> rep_reason_success_duplicate
     - bad_flag -> rep_reason_bad_flag
     - bad_edit -> rep_reason_bad_edit
     - bad_duplicate -> rep_reason_bad_duplicate

    :param action:
    :return:
    """
    return DBDiscussionSession.query(ReputationReason).filter_by(reason=f'rep_reason_{action}').first()
