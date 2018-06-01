import random
from typing import Union, List

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import LastReviewerSplit, LastReviewerMerge, LastReviewerDelete, \
    LastReviewerDuplicate, LastReviewerEdit, LastReviewerOptimization, User, ReviewDelete, ReviewEdit, ReviewMerge, \
    ReviewOptimization, ReviewSplit, ReviewDuplicate, Argument, Issue, Statement, StatementToIssue, \
    sql_timestamp_pretty_print, TextVersion, ReviewEditValue, Premise
from dbas.lib import get_text_for_argument_uid, get_profile_picture
from dbas.logger import logger
from dbas.review.queue import Code
from dbas.review.reputation import add_reputation_for, has_access_to_review_system
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio


def add_vote_for(db_user: User, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge,
                                                 ReviewOptimization, ReviewSplit], is_okay: bool,
                 db_reviewer_type: Union[LastReviewerDelete, LastReviewerDuplicate, LastReviewerEdit, LastReviewerMerge,
                                         LastReviewerOptimization, LastReviewerSplit]) -> True:
    """
    Add vote for a specific review

    :param db_user: User
    :param db_review: one table ouf of the Reviews
    :param is_okay: Boolean
    :param db_reviewer_type: one table out of the LastReviews
    :return: True, if the cote can be added
    """
    logger('review.lib', f'{db_reviewer_type}, user {db_user.uid}, db_review {db_review}, is_okay {is_okay}')
    already_voted = DBDiscussionSession.query(db_reviewer_type).filter(db_reviewer_type.reviewer_uid == db_user.uid,
                                                                       db_reviewer_type.review_uid == db_review.uid).first()
    if already_voted:
        logger('review.lib', 'already voted')
        return False

    logger('review.lib', 'vote added')
    db_new_review = db_reviewer_type(db_user.uid, db_review.uid, is_okay)
    DBDiscussionSession.add(db_new_review)
    DBDiscussionSession.flush()
    transaction.commit()
    return True


def add_reputation_and_check_review_access(db_user: User, rep_reason: str, main_page: str, translator: Translator):
    """
    Adds reputation to a specific user and checks (send info popup) to this user

    :param db_user: user, which should get reputation
    :param rep_reason: Any reputation reason as string
    :param main_page: URL of the app
    :param translator: Instance of a translator
    :return:
    """
    if not rep_reason:
        return

    add_reputation_for(db_user, rep_reason)

    if has_access_to_review_system(db_user):
        send_request_for_info_popup_to_socketio(db_user.nickname, translator.get(_.youAreAbleToReviewNow),
                                                main_page + '/review')


def get_all_allowed_reviews_for_user(session, session_keyword, db_user, review_type, last_reviewer_type):
    """
    Returns all reviews from given type, whereby already seen and reviewed reviews are restricted.

    :param session: session of current webserver request
    :param session_keyword: keyword of 'already_seen' element in request.session
    :param db_user: current user
    :param review_type: data table of reviews
    :param last_reviewer_type: data table of last reviewers
    :return: all revies, list of already seen reviews as uids, list of already reviewed reviews as uids, boolean if the user reviews for the first time in this session
    """
    # only get arguments, which the user has not seen yet
    logger('review.lib', 'main')
    already_seen, first_time = list(), True
    if session_keyword in session:
        already_seen, first_time = session[session_keyword], False

    # and not reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = [last_review.review_uid for last_review in db_last_reviews_of_user]
    db_reviews = DBDiscussionSession.query(review_type).filter(review_type.is_executed == False,
                                                               review_type.detector_uid != db_user.uid,
                                                               ~review_type.uid.in_(
                                                                   already_seen + already_reviewed)).all()

    return {
        'reviews': db_reviews,
        'already_seen_reviews': already_seen,
        'already_voted_reviews': already_reviewed,
        'first_time': first_time
    }


def get_base_subpage_dict(review_type, db_reviews, already_seen, first_time, db_user, already_reviewed):
    """

    :param review_type:
    :param db_reviews:
    :param already_seen:
    :param first_time:
    :param db_user:
    :param already_reviewed:
    :return:
    """
    extra_info = ''
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(review_type).filter(review_type.is_executed == False,
                                                                   review_type.detector_uid != db_user.uid)
        if len(already_reviewed) > 0:
            db_reviews = db_reviews.filter(~review_type.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        return {
            'rnd_review': None,
            'already_seen_reviews': None,
            'extra_info': None,
            'text': None,
            'issue_titles': None,
        }

    rnd_review = random.choice(db_reviews)
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).get(rnd_review.argument_uid)
        text = get_text_for_argument_uid(db_argument.uid)
        issue_titles = [DBDiscussionSession.query(Issue).get(db_argument.issue_uid).title]
    else:
        db_statement = DBDiscussionSession.query(Statement).get(rnd_review.statement_uid)
        text = db_statement.get_text()
        issue_titles = [issue.title for issue in get_issues_for_statement_uids([rnd_review.statement_uid])]

    return {
        'rnd_review': rnd_review,
        'already_seen_reviews': already_seen,
        'extra_info': extra_info,
        'text': text,
        'issue_titles': issue_titles
    }


def get_reporter_stats_for_review(db_review, ui_locales, main_page):
    """
    Get statistics for the current review

    :param db_review: Review-Row
    :param ui_locales: Language.ui_locales
    :param main_page: Host URL
    :return: dict()
    """
    logger('ReviewSubpagerHelper', 'main')

    db_reporter = DBDiscussionSession.query(User).get(db_review.detector_uid)

    return {
        'reported': sql_timestamp_pretty_print(db_review.timestamp, ui_locales),
        'reporter': db_reporter.global_nickname,
        'reporter_gravatar': get_profile_picture(db_reporter, 20),
        'reporter_url': main_page + '/user/' + str(db_reporter.uid),
        'id': str(db_review.uid)
    }


def get_issues_for_statement_uids(statement_uids: List[int]) -> List[Issue]:
    """
    Get all issues via the statement-to-issue table of a list of statement uids

    :param statement_uids: list of Statements.uids
    :return: List of Issues
    """
    db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter(
        StatementToIssue.statement_uid.in_(statement_uids)).all()
    statement2issue_uids = [el.issue_uid for el in db_statement2issue]
    db_issues = DBDiscussionSession.query(Issue).filter(Issue.uid.in_(statement2issue_uids)).all()
    return db_issues


def add_edit_reviews(db_user: User, uid: int, text: str):
    """
    Setup a new ReviewEdit row

    :param db_user: User
    :param uid: Statement.uid
    :param text: New content for statement
    :return: -1 if the statement of the element does not exists, -2 if this edit already exists, 1 on success, 0 otherwise
    """
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    if not db_statement:
        logger('review.lib', f'statement {uid} not found (return {Code.DOESNT_EXISTS})')
        return Code.DOESNT_EXISTS

    # already set an correction for this?
    if is_statement_in_edit_queue(uid):  # if we already have an edit, skip this
        logger('review.lib', f'statement {uid} already got an edit (return {Code.DUPLICATE})')
        return Code.DUPLICATE

    # is text different?
    db_tv = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)
    if len(text) > 0 and db_tv.content.lower().strip() != text.lower().strip():
        logger('review.lib', f'added review element for {uid} (return {Code.SUCCESS})')
        DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, statement=uid))
        return Code.SUCCESS

    logger('review.lib', f'no case for {uid} (return {Code.ERROR})')
    return Code.ERROR


def add_edit_values_review(db_user: User, uid: int, text: str):
    """
    Setup a new ReviewEditValue row

    :param db_user: User
    :param uid: Statement.uid
    :param text: New content for statement
    :return: 1 on success, 0 otherwise
    """
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    if not db_statement:
        logger('review.lib', f'{uid} not found')
        return Code.ERROR

    db_textversion = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)

    if len(text) > 0 and db_textversion.content.lower().strip() != text.lower().strip():
        db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.detector_uid == db_user.uid,
                                                                      ReviewEdit.statement_uid == uid).order_by(
            ReviewEdit.uid.desc()).first()
        DBDiscussionSession.add(ReviewEditValue(db_review_edit.uid, uid, 'statement', text))
        logger('review.lib', f'{uid} - \'{text}\' accepted')
        return Code.SUCCESS

    logger('review.lib', f'{uid} - \'{text}\' malicious edit')
    return Code.ERROR


def is_statement_in_edit_queue(uid: int, is_executed: bool = False) -> bool:
    """
    Returns true if the statement is not in the edit queue

    :param uid: Statement.uid
    :param is_executed: Bool
    :return: Boolean
    """
    db_already_edit_count = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.statement_uid == uid,
                                                                         ReviewEdit.is_executed == is_executed).count()
    return db_already_edit_count > 0


def is_arguments_premise_in_edit_queue(db_argument: Argument, is_executed: bool = False) -> bool:
    """
    Returns true if the premises of an argument are not in the edit queue

    :param db_argument: Argument
    :param is_executed: Bool
    :return: Boolean
    """
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).all()
    statement_uids = [db_premise.statement_uid for db_premise in db_premises]
    db_already_edit_count = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.statement_uid.in_(statement_uids),
                                                                         ReviewEdit.is_executed == is_executed).count()
    return db_already_edit_count > 0
