import logging
import random
from typing import List, Type

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Issue, Statement, StatementToIssue, sql_timestamp_pretty_print, \
    Premise, User, AbstractReviewCase, AbstractLastReviewerCase
from dbas.lib import get_text_for_argument_uid, get_profile_picture
from dbas.review.mapper import get_review_modal_mapping, get_last_reviewer_by_key
from dbas.review.reputation import get_reputation_of, reputation_borders

LOG = logging.getLogger(__name__)


def get_all_allowed_reviews_for_user(session, session_keyword, db_user, review_type, last_reviewer_type):
    """
    Returns all reviews from given type, whereby already seen and reviewed reviews are restricted.

    :param session: session of current webserver request
    :param session_keyword: keyword of 'already_seen' element in request.session
    :param db_user: current user
    :param review_type: data table of reviews
    :param last_reviewer_type: data table of last reviewers
    :return: all reviews, list of already seen reviews as uids, list of already reviewed reviews as uids, boolean if the
        user reviews for the first time in this session
    """
    # only get arguments, which the user has not seen yet
    LOG.debug("Trying to return all reviews for review_type %s", review_type.uid)
    already_seen, first_time = list(), True
    if session_keyword in session:
        already_seen, first_time = session[session_keyword], False

    # and not reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = [last_review.review_uid for last_review in db_last_reviews_of_user]
    relevant_reviews = already_seen + already_reviewed
    db_reviews = DBDiscussionSession.query(review_type).filter(review_type.is_executed == False,
                                                               review_type.detector_uid != db_user.uid,
                                                               ~review_type.uid.in_(relevant_reviews)).all()

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
    LOG.debug("Return statistics for review %s", db_review.uid)

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


def revoke_decision_and_implications(ttype, reviewer_type, uid):
    """
    Revokes the old decision and the implications

    :param ttype: table of Review
    :param reviewer_type: Table of LastReviewer
    :param uid: Review.uid
    :return: None
    """
    DBDiscussionSession.query(reviewer_type).filter_by(review_uid=uid).delete()

    db_review = DBDiscussionSession.query(ttype).get(uid)
    db_review.set_revoked(True)
    set_able_object_of_review(db_review, False)

    DBDiscussionSession.flush()
    transaction.commit()


def set_able_object_of_review(review, is_disabled):
    """
    En- or -disable a specific review, this affects all the statements and arguments

    :param review: Review
    :param is_disabled: boolean
    :return: None
    """
    LOG.debug("Is %s disabled? %s", review.uid, is_disabled)
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
    LOG.debug("Is statement %s disabled? %s", review.uid, is_disabled)
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
    LOG.debug("Is argument %s disabled? %s", review.uid, is_disabled)
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


def undo_premisegroups(pgroups_splitted_or_merged, replacements):
    """

    :param pgroups_splitted_or_merged:
    :param replacements:
    :return:
    """
    LOG.debug("Got %s merge/split pgroups and %s replacements", len(pgroups_splitted_or_merged), len(replacements))

    for element in pgroups_splitted_or_merged:
        old_pgroup = element.old_premisegroup_uid
        new_pgroup = element.new_premisegroup_uid

        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=new_pgroup).all()
        for argument in db_arguments:
            LOG.debug("Reset arguments %s pgroup from %s back to %s", argument.uid, new_pgroup, old_pgroup)
            argument.set_premisegroup(old_pgroup)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.flush()

    for element in replacements:
        old_statement = element.old_statement_uid
        new_statement = element.new_statement_uid

        db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=new_statement).all()
        for argument in db_arguments:
            LOG.debug("Reset arguments %s conclusion from %s back to %s", argument.uid, new_statement, old_statement)
            argument.set_conclusion(old_statement)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.flush()

    DBDiscussionSession.flush()
    transaction.commit()


def get_count_of_all():
    counts = [DBDiscussionSession.query(model).count() for model in get_review_modal_mapping().values()]
    return sum(counts)


def get_complete_review_count(db_user: User) -> int:
    """
    Sums up the review points of the user

    :param db_user: User
    :return: int
    """
    user_rep, all_rights = get_reputation_of(db_user)
    count = 0
    mapping = get_review_modal_mapping()
    for key in mapping:
        if user_rep >= reputation_borders[key] or all_rights:
            last_reviewer = get_last_reviewer_by_key(key)
            count += get_review_count_for(mapping[key], last_reviewer, db_user)
    return count


def get_review_count_for(review_type: Type[AbstractReviewCase], last_reviewer_type: Type[AbstractLastReviewerCase],
                         db_user: User) -> int:
    """
    Returns the count of reviews of *review_type* for the user with *nickname*, whereby all reviewed data
    of *last_reviewer_type* are not observed. Reviews for statements in issues the user has not participated in are
    not returned

    :param review_type: ReviewEdit, ReviewOptimization or ...
    :param last_reviewer_type: LastReviewerEdit, LastReviewer...
    :param db_user: User
    :return: Integer
    """
    #  logger('ReviewQueues', '__get_review_count_for', 'main')
    if not db_user:
        return DBDiscussionSession.query(review_type).filter_by(is_executed=False).count()

    # get all reviews but filter reviews which
    # - the user has detected
    # - the user has reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = [last_review.review_uid for last_review in db_last_reviews_of_user]
    db_reviews = DBDiscussionSession.query(review_type).filter(review_type.is_executed == False,
                                                               review_type.detector_uid != db_user.uid,
                                                               ~review_type.uid.in_(already_reviewed))
    # count only those reviews where the user participated in a related issue
    reviews_with_participation = {r for r in db_reviews.all()
                                  if db_user in participating_users_in_issues(r.get_issues())}
    return len(reviews_with_participation)


def participating_users_in_issues(issues: [Issue]) -> {User}:
    return {u for i in issues for u in i.participating_users}


def add_vote_for(db_user: User, db_review: AbstractReviewCase, is_okay: bool,
                 db_reviewer_type: AbstractLastReviewerCase) -> True:
    """
    Add vote for a specific review

    :param db_user: User
    :param db_review: one table ouf of the Reviews
    :param is_okay: Boolean
    :param db_reviewer_type: one table out of the LastReviews
    :return: True, if the cote can be added
    """
    LOG.debug("%s, user %s, db_review %s, is_okay %s", db_reviewer_type, db_user.uid, db_review, is_okay)
    already_voted = DBDiscussionSession.query(db_reviewer_type).filter(
        db_reviewer_type.reviewer_uid == db_user.uid,
        db_reviewer_type.review_uid == db_review.uid).first()
    if already_voted:
        LOG.warning("Already voted")
        return False

    LOG.debug("Vote Added")
    db_new_review = db_reviewer_type(db_user.uid, db_review.uid, is_okay)
    DBDiscussionSession.add(db_new_review)
    DBDiscussionSession.flush()
    transaction.commit()
    return True


def get_user_dict_for_review(user_id, application_url):
    """
    Fetches some data of the given user.

    :param user_id:
    :param application_url: app url of D-BAS
    :return: dict with gravatar, users page and nickname
    """
    db_user = DBDiscussionSession.query(User).get(user_id)
    image_url = get_profile_picture(db_user, 20)
    return {
        'gravatar_url': image_url,
        'nickname': db_user.global_nickname,
        'userpage_url': f'{application_url}/user/{db_user.uid}'
    }
