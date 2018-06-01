"""
Provides helping function for displaying subpages like the edit queue.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import difflib
import random

from requests import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, ReviewOptimization, ReviewDeleteReason, Argument, \
    Issue, LastReviewerDelete, LastReviewerOptimization, ReviewEdit, LastReviewerEdit, ReviewEditValue, Statement, \
    sql_timestamp_pretty_print, ReviewDuplicate, LastReviewerDuplicate, ReviewMerge, ReviewSplit, LastReviewerMerge, \
    LastReviewerSplit, Premise, ReviewMergeValues, ReviewSplitValues, StatementToIssue
from dbas.lib import get_all_arguments_by_statement
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, \
    get_text_for_premisegroup_uid, get_profile_picture
from dbas.logger import logger
from dbas.review import review_queues, key_merge, key_delete, key_duplicate, key_edit, \
    key_optimization, key_split
from dbas.review.queue.lib import get_all_allowed_reviews_for_user
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def get_subpage_elements_for(db_user: User, session: Session, application_url: str, subpage_name: str,
                             translator: Translator):
    """
    Returns subpage for a specific review queue

    :param db_user: current user
    :param session: current session in the request
    :param application_url: current application_url in the request
    :param subpage_name: String
    :param translator: Translator
    :return: dict()
    """

    logger('ReviewSubpagerHelper', subpage_name)
    no_arguments_to_review = False
    button_set = {f'is_{key}': False for key in review_queues}

    ret_dict = {'page_name': subpage_name}

    text = translator.get(_.internalError)
    issue = translator.get(_.internalError)
    reason = ''
    stats = ''

    if subpage_name == key_delete:
        subpage_dict = __get_subpage_dict_for_deletes(session, application_url, db_user, translator)
        button_set['is_delete'] = True

    elif subpage_name == key_optimization:
        subpage_dict = __get_subpage_dict_for_optimization(session, application_url, db_user, translator)
        button_set['is_optimization'] = True

    elif subpage_name == key_edit:
        subpage_dict = __get_subpage_dict_for_edits(session, application_url, db_user, translator)
        button_set['is_edit'] = True

    elif subpage_name == key_duplicate:
        subpage_dict = __get_subpage_dict_for_duplicates(session, application_url, db_user, translator)
        button_set['is_duplicate'] = True

    elif subpage_name == key_split:
        subpage_dict = __get_subpage_dict_for_splits(session, application_url, db_user, translator)
        button_set['is_split'] = True

    elif subpage_name == key_merge:
        subpage_dict = __get_subpage_dict_for_merges(session, application_url, db_user, translator)
        button_set['is_merge'] = True

    else:
        subpage_dict = {'stats': stats, 'text': text, 'reason': reason, 'issue': issue, 'session': {}}

    # logger('ReviewSubpagerHelper', 'get_subpage_elements_for', 'subpage_dict ' + str(subpage_dict))
    ret_dict['reviewed_element'] = subpage_dict
    ret_dict['session'] = subpage_dict['session']
    if subpage_dict['text'] is None and subpage_dict['reason'] is None and subpage_dict['stats'] is None:
        return __wrap_subpage_dict({}, True, button_set)

    return __wrap_subpage_dict(ret_dict, no_arguments_to_review, button_set)


def __wrap_subpage_dict(ret_dict, no_arguments_to_review, button_set):
    """
    Set up dict()

    :param ret_dict: dict()
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
        'no_arguments_to_review': no_arguments_to_review,
        'button_set': button_set,
        'session': session
    }


def __get_base_subpage_dict(review_type, db_reviews, already_seen, first_time, db_user, already_reviewed):
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
        db_statement2issues = DBDiscussionSession.query(StatementToIssue).filter_by(
            statement_uid=rnd_review.statement_uid).all()
        statement2issues_uid = [el.issue_uid for el in db_statement2issues]
        db_issues = DBDiscussionSession.query(Issue).filter(Issue.uid.in_(statement2issues_uid)).all()
        issue_titles = [issue.title for issue in db_issues]

    return {
        'rnd_review': rnd_review,
        'already_seen_reviews': already_seen,
        'extra_info': extra_info,
        'text': text,
        'issue_titles': issue_titles
    }


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
    all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_delete}', db_user, ReviewDelete,
                                                    LastReviewerDelete)

    rev_dict = __get_base_subpage_dict(ReviewDelete, all_rev_dict['reviews'], all_rev_dict['already_seen_reviews'],
                                       all_rev_dict['first_time'], db_user, all_rev_dict['already_voted_reviews'])
    if not rev_dict['rnd_review']:
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue_titles': None,
            'extra_info': None,
            'session': session
        }

    db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(rev_dict['rnd_review'].reason_uid)
    stats = __get_stats_for_review(rev_dict['rnd_review'], translator.get_lang(), application_url)

    reason = ''
    if db_reason.reason == 'offtopic':
        reason = translator.get(_.argumentFlaggedBecauseOfftopic)
    if db_reason.reason == 'spam':
        reason = translator.get(_.argumentFlaggedBecauseSpam)
    if db_reason.reason == 'harmful':
        reason = translator.get(_.argumentFlaggedBecauseHarmful)

    rev_dict['already_seen_reviews'].append(rev_dict['rnd_review'].uid)
    session[f'already_seen_{key_delete}'] = rev_dict['already_seen_reviews']

    return {'stats': stats,
            'text': rev_dict['text'],
            'reason': reason,
            'issue_titles': rev_dict['issue_titles'],
            'extra_info': rev_dict['extra_info'],
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
    all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_optimization}', db_user,
                                                    ReviewOptimization, LastReviewerOptimization)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not all_rev_dict['reviews']:
        all_rev_dict['already_seen_reviews'] = list()
        extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
        db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(ReviewOptimization.is_executed == False,
                                                                          ReviewOptimization.detector_uid != db_user.uid)
        if len(all_rev_dict['already_voted_reviews']) > 0:
            db_reviews = db_reviews.filter(~ReviewOptimization.uid.in_(all_rev_dict['already_voted_reviews']))
        all_rev_dict['reviews'] = db_reviews.all()

    if not all_rev_dict['reviews']:
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue_titles': None,
            'context': [],
            'extra_info': None,
            'session': session
        }

    rnd_review = random.choice(all_rev_dict['reviews'])
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).get(rnd_review.argument_uid)
        text = get_text_for_argument_uid(db_argument.uid)
        issue_titles = [DBDiscussionSession.query(Issue).get(db_argument.issue_uid).title]
        parts = __get_text_parts_of_argument(db_argument)
        context = [text]
    else:
        db_statement = DBDiscussionSession.query(Statement).get(rnd_review.statement_uid)
        text = db_statement.get_text()
        db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter_by(
            statement_uid=rnd_review.statement_uid).all()
        statement2issue_uids = [el.issue_uid for el in db_statement2issue]
        db_issues = DBDiscussionSession.query(Issue).filter(Issue.uid.in_(statement2issue_uids)).all()
        issue_titles = [issue.title for issue in db_issues]
        parts = [__get_part_dict('statement', text, 0, rnd_review.statement_uid)]
        context = []
        args = get_all_arguments_by_statement(rnd_review.statement_uid)
        if args:
            html_wrap = '<span class="text-info"><strong>{}</strong></span>'
            context = [get_text_for_argument_uid(arg.uid).replace(text, html_wrap.format(text)) for arg in args]

    reason = translator.get(_.argumentFlaggedBecauseOptimization)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
    session[f'already_seen_{key_optimization}'] = all_rev_dict['already_seen_reviews']

    return {
        'stats': stats,
        'text': text,
        'reason': reason,
        'issue_titles': issue_titles,
        'extra_info': extra_info,
        'context': context,
        'parts': parts,
        'session': session
    }


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
    all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_edit}', db_user, ReviewEdit,
                                                    LastReviewerEdit)

    rev_dict = __get_base_subpage_dict(ReviewEdit, all_rev_dict['reviews'], all_rev_dict['already_seen_reviews'],
                                       all_rev_dict['first_time'], db_user, all_rev_dict['already_voted_reviews'])
    if not rev_dict['rnd_review']:
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
    db_edit_value = DBDiscussionSession.query(ReviewEditValue).filter_by(
        review_edit_uid=rev_dict['rnd_review'].uid).first()
    stats = __get_stats_for_review(rev_dict['rnd_review'], translator.get_lang(), application_url)

    if not db_edit_value:
        logger('ReviewSubpagerHelper', 'ReviewEdit {} has no edit value!'.format(rev_dict['rnd_review'].uid),
               error=True)
        # get all valid reviews
        db_allowed_reviews = DBDiscussionSession.query(ReviewEdit).filter(
            ReviewEdit.uid.in_(DBDiscussionSession.query(ReviewEditValue.review_edit_uid))).all()

        if len(db_allowed_reviews) > 0:
            return __get_subpage_dict_for_edits(session, db_user, translator, application_url)
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue_titles': None,
            'extra_info': None,
            'session': session
        }

    correction_list = [char for char in rev_dict['text']]
    __difference_between_string(rev_dict['text'], db_edit_value.content, correction_list)
    correction = ''.join(correction_list)

    rev_dict[f'already_seen_{key_edit}'].append(not rev_dict['rnd_review'].uid)
    session[f'already_seen_{key_edit}'] = rev_dict[f'already_seen_{key_edit}']

    return {
        'stats': stats,
        'text': rev_dict['text'],
        'corrected_version': db_edit_value.content,
        'corrections': correction,
        'reason': reason,
        'issue_titles': rev_dict['issue_titles'],
        'extra_info': rev_dict['extra_info'],  # TODO KILL
        'session': session
    }


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
    all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_duplicate}', db_user, ReviewDuplicate,
                                                    LastReviewerDuplicate)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not all_rev_dict['reviews']:
        logger('ReviewSubpagerHelper', 'no unseen reviews')
        all_rev_dict['already_seen_reviews'] = list()
        extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
        all_rev_dict['reviews'] = DBDiscussionSession.query(ReviewDuplicate).filter(
            ReviewDuplicate.is_executed == False,
            ReviewDuplicate.detector_uid != db_user.uid)
        if len(all_rev_dict['already_voted_reviews']) > 0:
            logger('ReviewSubpagerHelper', 'everything was seen')
            all_rev_dict['reviews'] = all_rev_dict['reviews'].filter(
                ~ReviewDuplicate.uid.in_(all_rev_dict['already_voted_reviews'])).all()

    if not all_rev_dict['reviews']:
        logger('ReviewSubpagerHelper', 'no reviews')
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue_titles': None,
            'extra_info': None,
            'session': session
        }

    rnd_review = random.choice(all_rev_dict['reviews'])
    db_statement = DBDiscussionSession.query(Statement).get(rnd_review.duplicate_statement_uid)
    text = db_statement.get_text()

    db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter_by(
        statement_uid=rnd_review.duplicate_statement_uid)
    statement2issue_uids = [el.issue_uid for el in db_statement2issue]
    db_issues = DBDiscussionSession.query(Issue).filter(Issue.uid.in_(statement2issue_uids)).all()
    issue_titles = [issue.title for issue in db_issues]
    reason = translator.get(_.argumentFlaggedBecauseDuplicate)
    duplicate_of_text = get_text_for_statement_uid(rnd_review.original_statement_uid)
    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
    session['already_seen_duplicate'] = all_rev_dict['already_seen_reviews']

    return {
        'stats': stats,
        'text': text,
        'duplicate_of': duplicate_of_text,
        'reason': reason,
        'issue_titles': issue_titles,
        'extra_info': extra_info,
        'session': session
    }


def __get_subpage_dict_for_splits(session, application_url, db_user, translator):
    """

    :param session: session of current webserver request
    :param application_url: current url of the app
    :param db_user: User
    :param translator: Translator
    :return:
    """
    logger('ReviewSubpagerHelper', 'main')
    all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_split}', db_user, ReviewSplit,
                                                    LastReviewerSplit)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not all_rev_dict['reviews']:
        logger('ReviewSubpagerHelper', 'no unseen reviews')
        all_rev_dict['already_seen_reviews'] = list()
        extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
        db_reviews = DBDiscussionSession.query(ReviewSplit).filter(ReviewSplit.is_executed == False,
                                                                   ReviewSplit.detector_uid != db_user.uid)
        if len(all_rev_dict['already_voted_reviews']) > 0:
            logger('ReviewSubpagerHelper', 'everything was seen')
            db_reviews = db_reviews.filter(~ReviewSplit.uid.in_(all_rev_dict['already_voted_reviews']))
            all_rev_dict['reviews'] = db_reviews.all()

    if not all_rev_dict['reviews']:
        logger('ReviewSubpagerHelper', 'no reviews')
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue': None,
            'extra_info': None,
            'issue_titles': [],
            'session': session
        }

    rnd_review = random.choice(all_rev_dict['reviews'])
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

    statement_uids = [p.statement_uid for p in premises]
    db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter(
        StatementToIssue.statement_uid.in_(statement_uids)).all()
    statement2issue_uids = [el.issue_uid for el in db_statement2issue]
    db_issues = DBDiscussionSession.query(Issue).filter(Issue.uid.in_(statement2issue_uids)).all()
    issue_titles = [issue.title for issue in db_issues]

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
    session[f'already_seen_{key_split}'] = all_rev_dict['already_seen_reviews']

    return {
        'stats': stats,
        'text': text,
        'splitted_text': splitted_text,
        'reason': reason,
        'issue': issue,
        'extra_info': extra_info,
        'pgroup_only': pgroup_only,
        'issue_titles': issue_titles,
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
    all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_merge}', db_user, ReviewMerge,
                                                    LastReviewerMerge)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not all_rev_dict['reviews']:
        logger('ReviewSubpagerHelper', 'no unseen reviews')
        all_rev_dict['already_seen_reviews'] = list()
        extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
        db_reviews = DBDiscussionSession.query(ReviewMerge).filter(ReviewMerge.is_executed == False,
                                                                   ReviewMerge.detector_uid != db_user.uid)
        if len(all_rev_dict['already_voted_reviews']) > 0:
            logger('ReviewSubpagerHelper', 'everything was seen')
            db_reviews = db_reviews.filter(~ReviewMerge.uid.in_(all_rev_dict['already_voted_reviews']))
        all_rev_dict['reviews'] = db_reviews.all()

    if not all_rev_dict['reviews']:
        logger('ReviewSubpagerHelper', 'no reviews')
        return {
            'stats': None,
            'text': None,
            'reason': None,
            'issue_titles': [],
            'extra_info': None,
            'session': session
        }

    rnd_review = random.choice(all_rev_dict['reviews'])
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

    statement_uids = [p.statement_uid for p in premises]
    db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter(
        StatementToIssue.statement_uid.in_(statement_uids)).all()
    statement2issue_uids = [el.issue_uid for el in db_statement2issue]
    db_issues = DBDiscussionSession.query(Issue).filter(Issue.uid.in_(statement2issue_uids)).all()
    issue_titles = [issue.title for issue in db_issues]
    reason = translator.get(_.argumentFlaggedBecauseMerge)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), application_url)

    all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
    session[f'already_seen_{key_merge}'] = all_rev_dict['already_seen_reviews']

    return {
        'stats': stats,
        'text': text,
        'merged_text': merged_text,
        'reason': reason,
        'issue_titles': issue_titles,
        'extra_info': extra_info,
        'pgroup_only': pgroup_only,
        'session': session
    }


def __difference_between_string(a: str, b: str, correction_list: list(str)):
    """
    Colors the difference between two strings

    :param a: first string
    :param b: second string
    :param correction_list: character list of the first string
    :return: modified correction list with html strings around the modified characters
    """
    base = '<strong><span class="text-{}">'
    tag_p = base.format('success')
    tag_m = base.format('danger')
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


def __get_stats_for_review(db_review, ui_locales, main_page):
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


def __get_text_parts_of_argument(argument):
    """
    Get all parts of an argument as string

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
