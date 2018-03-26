"""
Provides helping function for displaying subpages like the edit queue.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import difflib
import random

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, ReviewOptimization, ReviewDeleteReason, Argument, \
    Issue, LastReviewerDelete, LastReviewerOptimization, ReviewEdit, LastReviewerEdit, ReviewEditValue, Statement, \
    sql_timestamp_pretty_print, ReviewDuplicate, LastReviewerDuplicate, ReviewMerge, ReviewSplit, LastReviewerMerge, \
    LastReviewerSplit, Premise, ReviewMergeValues, ReviewSplitValues
from dbas.lib import get_all_arguments_by_statement
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, \
    get_text_for_premisegroup_uid, get_profile_picture
from dbas.logger import logger
from dbas.review.helper.queues import review_queues
from dbas.review.helper.reputation import get_reputation_of, reputation_borders
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def get_subpage_elements_for(nickname, session, application_url, subpage_name, translator):
    """
    Returns subpage for a specific review queue

    :param nickname: current nickname in the request
    :param session: current session in the request
    :param application_url: current application_url in the request
    :param subpage_name: String
    :param translator: Translator
    :return: dict()
    """

    logger('ReviewSubpagerHelper', subpage_name)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    user_has_access = False
    no_arguments_to_review = False
    button_set = {
        'is_delete': False,
        'is_optimize': False,
        'is_edit': False,
        'is_duplicate': False,
        'is_split': False,
        'is_merge': False
    }

    # does the subpage exists
    if subpage_name not in review_queues and subpage_name != 'history':
        logger('ReviewSubpagerHelper', 'No page found', error=True)
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    rep_count, all_rights = get_reputation_of(nickname)
    user_has_access = rep_count >= reputation_borders[subpage_name] or all_rights
    # does the user exists and does he has the rights for this queue?
    if not db_user or not user_has_access:
        logger('ReviewSubpagerHelper', 'No user found', error=True)
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    ret_dict = {'page_name': subpage_name}

    text = translator.get(_.internalError)
    issue = translator.get(_.internalError)
    reason = ''
    stats = ''

    if subpage_name == 'deletes':
        subpage_dict = __get_subpage_dict_for_deletes(session, application_url, db_user, translator)
        button_set['is_delete'] = True

    elif subpage_name == 'optimizations':
        subpage_dict = __get_subpage_dict_for_optimization(session, application_url, db_user, translator)
        button_set['is_optimize'] = True

    elif subpage_name == 'edits':
        subpage_dict = __get_subpage_dict_for_edits(session, application_url, db_user, translator)
        button_set['is_edit'] = True

    elif subpage_name == 'duplicates':
        subpage_dict = __get_subpage_dict_for_duplicates(session, application_url, db_user, translator)
        button_set['is_duplicate'] = True

    elif subpage_name == 'splits':
        subpage_dict = __get_subpage_dict_for_splits(session, application_url, db_user, translator)
        button_set['is_split'] = True

    elif subpage_name == 'merges':
        subpage_dict = __get_subpage_dict_for_merges(session, application_url, db_user, translator)
        button_set['is_merge'] = True

    else:
        subpage_dict = {'stats': stats, 'text': text, 'reason': reason, 'issue': issue, 'session': {}}

    # logger('ReviewSubpagerHelper', 'get_subpage_elements_for', 'subpage_dict ' + str(subpage_dict))
    ret_dict['reviewed_element'] = subpage_dict
    ret_dict['session'] = subpage_dict['session']
    if subpage_dict['text'] is None and subpage_dict['reason'] is None and subpage_dict['stats'] is None:
        no_arguments_to_review = True
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    return __get_subpage_dict(ret_dict, True, no_arguments_to_review, button_set)


def __get_subpage_dict(ret_dict, has_access, no_arguments_to_review, button_set):
    """
    Set up dict()

    :param ret_dict: dict()
    :param has_access: Boolean
    :param no_arguments_to_review: Boolean
    :param button_set: dict()
    :return: dict()
    """
    session = {}
    if ret_dict and 'session' in ret_dict:
        session = ret_dict['session']
        ret_dict.pop('session')

    return {
        'elements': ret_dict,
        'has_access': has_access,
        'no_arguments_to_review': no_arguments_to_review,
        'button_set': button_set,
        'session': session
    }


def __get_all_allowed_reviews_for_user(session, session_keyword, db_user, review_type, last_reviewer_type):
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
    logger('ReviewSubpagerHelper', 'main')
    already_seen, first_time = (session[session_keyword], False) if session_keyword in session else (list(), True)

    # and not reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = []
    for last_review in db_last_reviews_of_user:
        already_reviewed.append(last_review.review_uid)

    # get all reviews
    db_reviews = DBDiscussionSession.query(review_type).filter(review_type.is_executed == False,
                                                               review_type.detector_uid != db_user.uid)

    # filter the ones, we have already seen
    if len(already_seen) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_seen))

    # filter the ones, we have already reviewed
    if len(already_reviewed) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_reviewed))

    return db_reviews.all(), already_seen, already_reviewed, first_time


def __get_base_subpage_dict(review_type, db_reviews, already_seen, first_time, db_user, already_reviewed):
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
        return None, None, None, None, None

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).get(rnd_review.argument_uid)
        text = get_text_for_argument_uid(db_argument.uid)
        issue = DBDiscussionSession.query(Issue).get(db_argument.issue_uid).title
    else:
        db_statement = DBDiscussionSession.query(Statement).get(rnd_review.statement_uid)
        text = db_statement.get_text()
        issue = DBDiscussionSession.query(Issue).get(db_statement.issue_uid).title

    return rnd_review, already_seen, extra_info, text, issue


def __get_subpage_dict_for_deletes(session, application_url, db_user, translator):
    """
    Setup the subpage for the delete queue

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    logger('ReviewSubpagerHelper', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(session,
                                                                                                'already_seen_deletes',
                                                                                                db_user,
                                                                                                ReviewDelete,
                                                                                                LastReviewerDelete)

    rnd_review, already_seen, extra_info, text, issue = __get_base_subpage_dict(ReviewDelete, db_reviews, already_seen,
                                                                                first_time, db_user, already_reviewed)
    if not rnd_review:
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue': None,
            'extra_info': None,
            'session': session
        }

    db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(rnd_review.reason_uid)
    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    reason = ''
    if db_reason.reason == 'offtopic':
        reason = translator.get(_.argumentFlaggedBecauseOfftopic)
    if db_reason.reason == 'spam':
        reason = translator.get(_.argumentFlaggedBecauseSpam)
    if db_reason.reason == 'harmful':
        reason = translator.get(_.argumentFlaggedBecauseHarmful)

    already_seen.append(rnd_review.uid)
    session['already_seen_deletes'] = already_seen

    return {'stats': stats,
            'text': text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'session': session}


def __get_subpage_dict_for_optimization(session, application_url, db_user, translator):
    """
    Setup the subpage for the optimization queue

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    logger('ReviewSubpagerHelper', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(session,
                                                                                                'already_seen_optimization',
                                                                                                db_user,
                                                                                                ReviewOptimization,
                                                                                                LastReviewerOptimization)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(ReviewOptimization.is_executed == False,
                                                                          ReviewOptimization.detector_uid != db_user.uid)
        if len(already_reviewed) > 0:
            db_reviews = db_reviews.filter(~ReviewOptimization.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'context': [],
                'extra_info': None,
                'session': session}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).get(rnd_review.argument_uid)
        text = get_text_for_argument_uid(db_argument.uid)
        issue = DBDiscussionSession.query(Issue).get(db_argument.issue_uid).title
        parts = __get_text_parts_of_argument(db_argument)
        context = [text]
    else:
        db_statement = DBDiscussionSession.query(Statement).get(rnd_review.statement_uid)
        text = db_statement.get_text()
        issue = DBDiscussionSession.query(Issue).get(db_statement.issue_uid).title
        parts = [__get_part_dict('statement', text, 0, rnd_review.statement_uid)]
        context = []
        args = get_all_arguments_by_statement(rnd_review.statement_uid)
        if args:
            context = [get_text_for_argument_uid(arg.uid).replace(text,
                                                                  '<span class="text-info"><strong>{}</strong></span>'.format(
                                                                      text)) for arg in args]

    reason = translator.get(_.argumentFlaggedBecauseOptimization)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    already_seen.append(rnd_review.uid)
    session['already_seen_optimization'] = already_seen

    return {'stats': stats,
            'text': text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'context': context,
            'parts': parts,
            'session': session}


def __get_subpage_dict_for_edits(session, application_url, db_user, translator):
    """
    Setup the subpage for the edits queue

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    logger('ReviewSubpagerHelper', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(session,
                                                                                                'already_seen_edit',
                                                                                                db_user,
                                                                                                ReviewEdit,
                                                                                                LastReviewerEdit)

    rnd_review, already_seen, extra_info, text, issue = __get_base_subpage_dict(ReviewEdit, db_reviews, already_seen,
                                                                                first_time, db_user, already_reviewed)
    if not rnd_review:
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue': None,
            'extra_info': None,
            'session': session
        }

    reason = translator.get(_.argumentFlaggedBecauseEdit)

    # build correction
    db_edit_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=rnd_review.uid).first()
    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    if not db_edit_value:
        logger('ReviewSubpagerHelper', 'ReviewEdit {} has no edit value!'.format(rnd_review.uid), error=True)
        # get all valid reviews
        db_allowed_reviews = DBDiscussionSession.query(ReviewEdit).filter(
            ReviewEdit.uid.in_(DBDiscussionSession.query(ReviewEditValue.review_edit_uid))).all()

        if len(db_allowed_reviews) > 0:
            return __get_subpage_dict_for_edits(session, db_user, translator, application_url)
        else:
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None,
                'session': session
            }

    correction_list = [char for char in text]
    __difference_between_string(text, db_edit_value.content, correction_list)
    correction = ''.join(correction_list)

    already_seen.append(rnd_review.uid)
    session['already_seen_edit'] = already_seen

    return {'stats': stats,
            'text': text,
            'corrected_version': db_edit_value.content,
            'corrections': correction,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'session': session}


def __get_subpage_dict_for_duplicates(session, application_url, db_user, translator):
    """
    Setup the subpage for the duplicates queue

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    logger('ReviewSubpagerHelper', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(session,
                                                                                                'already_seen_duplicate',
                                                                                                db_user,
                                                                                                ReviewDuplicate,
                                                                                                LastReviewerDuplicate)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        logger('ReviewSubpagerHelper', 'no unseen reviews')
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewDuplicate).filter(ReviewDuplicate.is_executed == False,
                                                                       ReviewDuplicate.detector_uid != db_user.uid)
        if len(already_reviewed) > 0:
            logger('ReviewSubpagerHelper', 'everything was seen')
            db_reviews = db_reviews.filter(~ReviewDuplicate.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        logger('ReviewSubpagerHelper', 'no reviews')
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None,
                'session': session}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    db_statement = DBDiscussionSession.query(Statement).get(rnd_review.duplicate_statement_uid)
    text = db_statement.get_text()
    issue = DBDiscussionSession.query(Issue).get(db_statement.issue_uid).title
    reason = translator.get(_.argumentFlaggedBecauseDuplicate)

    duplicate_of_text = get_text_for_statement_uid(rnd_review.original_statement_uid)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    already_seen.append(rnd_review.uid)
    session['already_seen_duplicate'] = already_seen

    return {'stats': stats,
            'text': text,
            'duplicate_of': duplicate_of_text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'session': session}


def __get_subpage_dict_for_splits(session, application_url, db_user, translator):
    """

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return:
    """
    logger('ReviewSubpagerHelper', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(session,
                                                                                                'already_seen_split',
                                                                                                db_user,
                                                                                                ReviewSplit,
                                                                                                LastReviewerSplit)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        logger('ReviewSubpagerHelper', 'no unseen reviews')
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewSplit).filter(ReviewSplit.is_executed == False,
                                                                   ReviewSplit.detector_uid != db_user.uid)
        if len(already_reviewed) > 0:
            logger('ReviewSubpagerHelper', 'everything was seen')
            db_reviews = db_reviews.filter(~ReviewSplit.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        logger('ReviewSubpagerHelper', 'no reviews')
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue': None,
            'extra_info': None,
            'session': session
        }

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=rnd_review.premisegroup_uid).all()
    text = get_text_for_premisegroup_uid(rnd_review.premisegroup_uid)
    db_review_values = DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=rnd_review.uid).all()
    if db_review_values:
        splitted_text = [rsv.content for rsv in db_review_values]
        pgroup_only = False
    else:
        splitted_text = [premise.get_text() for premise in premises]
        pgroup_only = True
    issue = DBDiscussionSession.query(Issue).get(premises[0].issue_uid).title
    reason = translator.get(_.argumentFlaggedBecauseSplit)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    already_seen.append(rnd_review.uid)
    session['already_seen_split'] = already_seen

    return {
        'stats': stats,
        'text': text,
        'splitted_text': splitted_text,
        'reason': reason,
        'issue': issue,
        'extra_info': extra_info,
        'pgroup_only': pgroup_only,
        'session': session
    }


def __get_subpage_dict_for_merges(session, application_url, db_user, translator):
    """

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return:
    """
    logger('ReviewSubpagerHelper', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(session,
                                                                                                'already_seen_merge',
                                                                                                db_user,
                                                                                                ReviewMerge,
                                                                                                LastReviewerMerge)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        logger('ReviewSubpagerHelper', 'no unseen reviews')
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewMerge).filter(ReviewMerge.is_executed == False,
                                                                   ReviewMerge.detector_uid != db_user.uid)
        if len(already_reviewed) > 0:
            logger('ReviewSubpagerHelper', 'everything was seen')
            db_reviews = db_reviews.filter(~ReviewMerge.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        logger('ReviewSubpagerHelper', 'no reviews')
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue': None,
            'extra_info': None,
            'session': session
        }

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=rnd_review.premisegroup_uid).all()
    text = [premise.get_text() for premise in premises]
    db_review_values = DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=rnd_review.uid).all()

    discussion_lang = DBDiscussionSession.query(Statement).get(premises[0].uid).lang
    translator_discussion = Translator(discussion_lang)

    if db_review_values:
        aand = translator_discussion.get(_.aand)
        merged_text = ' {} '.format(aand).join([rsv.content for rsv in db_review_values])
        pgroup_only = False
    else:
        merged_text = get_text_for_premisegroup_uid(rnd_review.premisegroup_uid)
        pgroup_only = True
    issue = DBDiscussionSession.query(Issue).get(premises[0].issue_uid).title
    reason = translator.get(_.argumentFlaggedBecauseMerge)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    already_seen.append(rnd_review.uid)
    session['already_seen_merge'] = already_seen

    return {
        'stats': stats,
        'text': text,
        'merged_text': merged_text,
        'reason': reason,
        'issue': issue,
        'extra_info': extra_info,
        'pgroup_only': pgroup_only,
        'session': session
    }


def __difference_between_string(a, b, correction_list):
    tag_p = '<strong><span class="text-success">'
    tag_m = '<strong><span class="text-danger">'
    tag_e = '</span></strong>'

    for i, s in enumerate(difflib.ndiff(a, b)):
        if i >= len(correction_list):
            correction_list.append('')
        if s[0] == ' ':
            correction_list[i] = s[-1]
            continue
        elif s[0] == '-':
            correction_list[i] = tag_m + s[-1] + tag_e
        elif s[0] == '+':
            correction_list[i] = tag_p + s[-1] + tag_e


def __get_stats_for_review(review, ui_locales, main_page):
    """
    Get statistics for the current review

    :param review: Review-Row
    :param ui_locales: Language.ui_locales
    :param main_page: Host URL
    :return: dict()
    """
    logger('ReviewSubpagerHelper', 'main')

    db_reporter = DBDiscussionSession.query(User).get(review.detector_uid)

    stats = dict()
    stats['reported'] = sql_timestamp_pretty_print(review.timestamp, ui_locales)
    stats['reporter'] = db_reporter.global_nickname
    stats['reporter_gravatar'] = get_profile_picture(db_reporter, 20)
    stats['reporter_url'] = main_page + '/user/' + str(db_reporter.uid)
    stats['id'] = str(review.uid)

    return stats


def __get_text_parts_of_argument(argument):
    """
    Get all parts of ana rgument as string

    :param argument: Argument.uid
    :return: list of strings
    """
    logger('ReviewSubpagerHelper', 'main')
    ret_list = list()

    # get premise of current argument
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=argument.premisegroup_uid).all()
    premises_uids = [premise.uid for premise in db_premises]
    for uid in premises_uids:
        logger('ReviewSubpagerHelper', 'add premise of argument ' + str(argument.uid))
        text = get_text_for_statement_uid(uid)
        ret_list.append(__get_part_dict('premise', text, argument.uid, uid))

    if argument.argument_uid is None:  # get conclusion of current argument
        conclusion = argument.get_conclusion_text()
        logger('ReviewSubpagerHelper', 'add statement of argument ' + str(argument.uid))
        ret_list.append(__get_part_dict('conclusion', conclusion, argument.uid, argument.conclusion_uid))
    else:  # or get the conclusions argument
        db_conclusions_argument = DBDiscussionSession.query(Argument).get(argument.argument_uid)

        while db_conclusions_argument.argument_uid is not None:  # get further conclusions arguments

            # get premise of conclusions arguments
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=argument.premisegroup_uid).all()
            premises_uids = [premise.uid for premise in db_premises]
            for uid in premises_uids:
                text = get_text_for_statement_uid(uid)
                logger('ReviewSubpagerHelper', 'add premise of argument ' + str(db_conclusions_argument.uid))
                ret_list.append(__get_part_dict('premise', text, db_conclusions_argument.uid, uid))

            db_conclusions_argument = DBDiscussionSession.query(Argument).get(db_conclusions_argument.argument_uid)

        # get the last conclusion of the chain
        conclusion = db_conclusions_argument.get_conclusion_text()
        logger('ReviewSubpagerHelper', 'add statement of argument ' + str(db_conclusions_argument.uid))
        ret_list.append(__get_part_dict('conclusion', conclusion, db_conclusions_argument.uid,
                                        db_conclusions_argument.conclusion_uid))

    return ret_list[::-1]


def __get_part_dict(typeof, text, argument_uid, conclusion_uid):
    """
    Collects the aprts of the argument-string and builds up a little dict

    :param typeof: String
    :param text: String
    :param argument_uid: Argument.uid
    :return: dict()
    """
    logger('ReviewSubpageHelper',
           'type: ' + str(typeof) + ', text: ' + str(text) + ', arg: ' + str(argument_uid) + ', uid: ' + str(
               conclusion_uid))
    return {
        'type': typeof,
        'text': text,
        'argument_uid': argument_uid,
        'statement_uid': conclusion_uid
    }
