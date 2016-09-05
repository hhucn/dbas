"""
Provides helping function for the review page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, ReviewOptimization, ReviewDeleteReason, Argument,\
    ArgumentSeenBy, Issue, LastReviewerDelete, LastReviewerOptimization
from dbas.helper.relation import RelationHelper
from dbas.lib import get_text_for_argument_uid, sql_timestamp_pretty_print, get_text_for_statement_uid, get_text_for_premisesgroup_uid
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of, reputation_borders
from sqlalchemy import and_

pages = ['deletes', 'optimizations']


def get_subpage_elements_for(request, subpage_name, nickname, translator):
    """

    :param request:
    :param subpage_name:
    :param nickname:
    :param translator:
    :return:
    """
    logger('ReviewPagerHelper', 'get_subpage_elements_for', subpage_name)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    user_has_access = False
    no_arguments_to_review = False
    button_set = {'is_delete': False, 'is_optimize': False}

    # does the subpage exists
    if subpage_name not in pages and subpage_name != 'history':
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    rep_count, all_rights = get_reputation_of(nickname)
    user_has_access = rep_count >= reputation_borders[subpage_name] or all_rights
    # does the user exists and does he has the rights for this queue?
    if not db_user or not user_has_access:
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    ret_dict = dict()
    ret_dict['page_name'] = subpage_name

    # get a random argument for reviewing
    text = translator.get(translator.internalError)
    reason = ''
    stats = ''
    issue = translator.get(translator.internalError)

    if subpage_name == 'deletes':
        subpage_dict = __get_subpage_dict_for_deletes(request, db_user, translator)
        button_set['is_delete'] = True

    elif subpage_name == 'optimizations':
        subpage_dict = __get_subpage_dict_for_optimization(request, db_user, translator)
        button_set['is_optimize'] = True
    else:
        subpage_dict = {'stats': stats,
                        'text': text,
                        'reason': reason,
                        'issue': issue}

    ret_dict['reviewed_argument'] = subpage_dict
    if subpage_dict['text'] is None and subpage_dict['reason'] is None and subpage_dict['stats'] is None:
        no_arguments_to_review = True
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    return __get_subpage_dict(ret_dict, True, no_arguments_to_review, button_set)


def __get_subpage_dict(ret_dict, has_access, no_arguments_to_review, button_set):
    """

    :param ret_dict:
    :param has_access:
    :param no_arguments_to_review:
    :param button_set:
    :return:
    """
    return {'elements': ret_dict,
            'has_access': has_access,
            'no_arguments_to_review': no_arguments_to_review,
            'button_set': button_set}


def __get_all_allowed_reviews_for_user(request, session_keword, db_user, review_type, last_reviewer_type):
    """
    Returns all reviews from given type, whereby already seen and reviewed reviews are restricted.

    :param request: current request
    :param session_keword: keyword of 'already_seen' element in request.session
    :param db_user: current user
    :param review_type: data table of reviews
    :param last_reviewer_type: data table of last reviewers
    :return: all revies, list of already seen reviews as uids, list of already reviewed reviews as uids, boolean if the user reviews for the first time in this session
    """
    # only get arguments, which the user has not seen yet
    already_seen, first_time = (request.session[session_keword], False) if session_keword in request.session else (list(), True)

    # and not reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = []
    for last_review in db_last_reviews_of_user:
        already_reviewed.append(last_review.review_uid)

    # get all reviews
    db_reviews = DBDiscussionSession.query(review_type).filter(and_(review_type.is_executed == False,
                                                                    review_type.detector_uid != db_user.uid))
    # filter the ones, we have already seen
    if len(already_seen) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_seen))

    # filter the ones, we have already reviewed
    if len(already_reviewed) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_reviewed))

    return db_reviews.all(), already_seen, already_reviewed, first_time


def __get_subpage_dict_for_deletes(request, db_user, translator):
    """

    :param request:
    :param db_user:
    :param translator:
    :return:
    """
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(request, 'already_seen_deletes', db_user, ReviewDelete, LastReviewerDelete)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.is_executed == False,
                                                                         ReviewDelete.detector_uid != db_user.uid,
                                                                         ~ReviewDelete.uid.in_(already_reviewed))).all()
    if not db_reviews:
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
    text = get_text_for_argument_uid(db_argument.uid)
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(uid=rnd_review.reason_uid).first()
    issue = DBDiscussionSession.query(Issue).filter_by(uid=db_argument.issue_uid).first().title

    stats = __get_stats_for_argument(db_argument.uid)
    stats['reported'] = sql_timestamp_pretty_print(rnd_review.timestamp, translator.get_lang())
    stats['id'] = str(rnd_review.uid)

    reason = ''
    if db_reason.reason == 'offtopic':
        reason = translator.get(translator.argumentFlaggedBecauseOfftopic)
    if db_reason.reason == 'spam':
        reason = translator.get(translator.argumentFlaggedBecauseSpam)
    if db_reason.reason == 'harmful':
        reason = translator.get(translator.argumentFlaggedBecauseHarmful)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_deletes'] = already_seen

    return {'stats': stats,
            'text': text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info}


def __get_subpage_dict_for_optimization(request, db_user, translator):
    """

    :param request:
    :param db_user:
    :param translator:
    :return:
    """
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(request, 'already_seen_deletes', db_user, ReviewOptimization, LastReviewerOptimization)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.is_executed == False,
                                                                               ReviewOptimization.detector_uid != db_user.uid,
                                                                               ~ReviewOptimization.uid.in_(already_reviewed))).all()

    if not db_reviews:
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
    text = get_text_for_argument_uid(db_argument.uid)
    reason = translator.get(translator.argumentFlaggedBecauseOptimization)
    issue = DBDiscussionSession.query(Issue).filter_by(uid=db_argument.issue_uid).first().title

    stats = __get_stats_for_argument(db_argument.uid)
    stats['reported'] = sql_timestamp_pretty_print(rnd_review.timestamp, translator.get_lang())
    stats['id'] = str(rnd_review.uid)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_optimization'] = already_seen

    return {'stats': stats,
            'text': text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'parts': __get_text_parts_of_argument(db_argument)}


def __get_stats_for_argument(argument_uid):
    """

    :param argument_uid:
    :return:
    """
    viewed = len(DBDiscussionSession.query(ArgumentSeenBy).filter_by(argument_uid=argument_uid).all())

    _rh = RelationHelper(argument_uid)
    undermines = _rh.get_undermines_for_argument_uid()
    undercuts = _rh.get_undercuts_for_argument_uid()
    rebuts = _rh.get_rebuts_for_argument_uid()
    supports = _rh.get_supports_for_argument_uid()

    len_undermines = len(undermines) if undermines else 0
    len_undercuts = len(undercuts) if undercuts else 0
    len_rebuts = len(rebuts) if rebuts else 0
    len_supports = len(supports) if supports else 0

    attacks = len_undermines + len_undercuts + len_rebuts

    return {'viewed': viewed, 'attacks': attacks, 'supports': len_supports}


def __get_text_parts_of_argument(argument):
    """

    :param argument:
    :return:
    """
    ret_list = list()
    premisegroup, trash = get_text_for_premisesgroup_uid(argument.premisesgroup_uid)
    ret_list.append({'type': 'premisegroup',
                     'text': premisegroup,
                     'uid': argument.premisesgroup_uid})

    if argument.argument_uid is None:
        conclusion = get_text_for_statement_uid(argument.conclusion_uid)
        ret_list.append({'type': 'statement',
                         'text': conclusion,
                         'uid': argument.conclusion_uid})
    else:
        db_conclusions_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument.argument_uid).first()
        while db_conclusions_argument.argument_uid is not None:
            premisegroup, trash = get_text_for_premisesgroup_uid(db_conclusions_argument.premisesgroup_uid)
            ret_list.append({'type': 'premisegroup',
                             'text': premisegroup,
                             'uid': db_conclusions_argument.premisesgroup_uid})
            db_conclusions_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument.argument_uid).first()
        conclusion = get_text_for_statement_uid(db_conclusions_argument.conclusion_uid)
        ret_list.append({'type': 'statement',
                         'text': conclusion,
                         'uid': argument.conclusion_uid})

    return ret_list
