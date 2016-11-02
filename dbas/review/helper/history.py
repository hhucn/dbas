"""
Provides helping function for the managing the queue with all executed decisions as well as all ongoing decisions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDelete, LastReviewerDelete, ReviewOptimization, LastReviewerOptimization, \
    User, ReputationHistory, ReputationReason, ReviewDeleteReason, ReviewEdit, LastReviewerEdit, ReviewEditValue, TextVersion, Statement, ReviewCanceled
from dbas.lib import sql_timestamp_pretty_print, get_public_nickname_based_on_settings, get_text_for_argument_uid, get_profile_picture, is_user_author, get_text_for_statement_uid
from dbas.review.helper.reputation import get_reputation_of, reputation_borders, reputation_icons
from dbas.review.helper.main import en_or_disable_object_of_review
from sqlalchemy import and_
from dbas.strings.translator import Translator
from dbas.logger import logger


def get_review_history(main_page, nickname, translator):
    return __get_data(main_page, nickname, translator, True)


def get_ongoing_reviews(main_page, nickname, translator):
    return __get_data(main_page, nickname, translator, False)


def __get_data(main_page, nickname, translator, is_executed=False):
    """

    :param main_page:
    :param nickname:
    :param translator:
    :param is_executed:
    :return:
    """
    ret_dict = dict()
    if is_executed:
        ret_dict['has_access'] = __has_access_to_history(nickname)
    else:
        ret_dict['has_access'] = is_user_author(nickname)
    ret_dict['is_history'] = is_executed

    deletes_list = __get_executed_reviews_of('deletes', main_page, ReviewDelete, LastReviewerDelete, translator, is_executed)
    optimizations_list = __get_executed_reviews_of('optimizations', main_page, ReviewOptimization, LastReviewerOptimization, translator, is_executed)
    edits_list = __get_executed_reviews_of('edits', main_page, ReviewEdit, LastReviewerEdit, translator, is_executed)

    past_decision = [{
        'title': 'Delete Queue',
        'icon': reputation_icons['deletes'],
        'queue': 'deletes',
        'content': deletes_list,
        'has_reason': True,
        'has_oem_text': False
    }, {
        'title': 'Optimization Queue',
        'queue': 'optimizations',
        'icon': reputation_icons['optimizations'],
        'content': optimizations_list,
        'has_reason': False,
        'has_oem_text': False
    }, {
        'title': 'Edit Queue',
        'queue': 'edits',
        'icon': reputation_icons['edits'],
        'content': edits_list,
        'has_reason': False,
        'has_oem_text': True
    }]
    ret_dict['past_decision'] = past_decision

    return ret_dict


def get_reputation_history_of(nickname, translator):
    """

    :param nickname:
    :param translator:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return dict()

    ret_dict = dict()
    count, all_rights = get_reputation_of(nickname)
    ret_dict['count'] = count
    ret_dict['all_rights'] = all_rights

    db_reputation = DBDiscussionSession.query(ReputationHistory) \
        .filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .order_by(ReputationHistory.uid.asc())\
        .all()

    rep_list = list()
    for rep in db_reputation:
        date = sql_timestamp_pretty_print(rep.timestamp, translator.get_lang(), humanize=False)
        points_data = ('+' if rep.reputations.points > 0 else '') + str(rep.reputations.points)
        points = rep.reputations.points
        action = translator.get(rep.reputations.reason)
        rep_list.append({'date': date,
                         'points_data': points_data,
                         'action': action,
                         'points': points})

    ret_dict['history'] = rep_list

    return ret_dict


def __get_executed_reviews_of(table, main_page, table_type, last_review_type, translator, is_executed=False):
    """
    Returns array with all relevant information about the last reviews of the given table.

    :param table: Shortcut for the table
    :param main_page: Main page of D-BAS
    :param table_type: Type of the review table
    :param last_review_type: Type of the last reviewer of the table
    :param translator: current ui_locales
    :param is_executed
    :return: Array with all decision per table
    """
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed == is_executed).order_by(table_type.uid.desc()).all()

    for review in db_reviews:
        length = 35
        # getting text
        if review.statement_uid is None:
            full_text = get_text_for_argument_uid(review.argument_uid)
        else:
            full_text = get_text_for_statement_uid(review.statement_uid)

        # pretty print
        intro = translator.get(translator.otherUsersSaidThat) + ' '
        if full_text.startswith(intro):
            short_text = full_text[len(intro):len(intro) + 1].upper() + full_text[len(intro) + 1:len(intro) + length]
        else:
            short_text = full_text[0:length]

        short_text += '...' if len(full_text) > length else '.'
        short_text = '<span class="text-primary">' + short_text + '</span>'

        is_okay = False if table == 'optimizations' else True
        # getting all pro and contra votes for this review
        pro_votes = DBDiscussionSession.query(last_review_type).filter(and_(last_review_type.review_uid == review.uid,
                                                                            last_review_type.is_okay == is_okay)).all()
        con_votes = DBDiscussionSession.query(last_review_type).filter(and_(last_review_type.review_uid == review.uid,
                                                                            last_review_type.is_okay != is_okay)).all()
        # getting the users which have voted
        pro_list = list()
        con_list = list()
        for pro in pro_votes:
            pro_list.append(__get_user_dict_for_review(pro.reviewer_uid, main_page))
        for con in con_votes:
            con_list.append(__get_user_dict_for_review(con.reviewer_uid, main_page))

        # and build up some dict
        entry = dict()
        entry['entry_id'] = review.uid
        if table == 'deletes':
            db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(uid=review.reason_uid).first()
            entry['reason'] = db_reason.reason
        entry['row_id'] = table + str(review.uid)
        entry['argument_shorttext'] = short_text
        entry['argument_fulltext'] = full_text
        if table == 'edits':
            db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=review.statement_uid).order_by(TextVersion.uid.desc()).all()
            entry['argument_oem_shorttext'] = db_textversions[1].content[0:length]
            entry['argument_oem_fulltext'] = db_textversions[1].content
        entry['pro'] = pro_list
        entry['con'] = con_list
        entry['timestamp'] = sql_timestamp_pretty_print(review.timestamp, translator.get_lang())
        entry['votes_pro'] = pro_list
        entry['votes_con'] = con_list
        entry['reporter'] = __get_user_dict_for_review(review.detector_uid, main_page)
        some_list.append(entry)

    return some_list


def __get_user_dict_for_review(user_id, mainpage):
    """
    Fetches some data of the given user.

    :param mainpage: Mainpage of D-BAS
    :return: dcit with gravatar, uerpage and nickname
    """
    db_user = DBDiscussionSession.query(User).filter_by(uid=user_id).first()
    image_url = get_profile_picture(db_user, 20)
    return {
        'gravatar_url': image_url,
        'nickname': get_public_nickname_based_on_settings(db_user),
        'userpage_url': mainpage + '/user/' + get_public_nickname_based_on_settings(db_user)
    }


def __has_access_to_history(nickname):
    """

    :param nickname:
    :return:
    """
    reputation_count, is_user_author = get_reputation_of(nickname)
    return is_user_author or reputation_count > reputation_borders['history']


def revoke_old_decision(queue, uid, lang, nickname, transaction):
    """

    :param queue:
    :param uid:
    :param lang:
    :param nickname:
    :param transaction:
    :return:
    """
    logger('review_history_helper', 'revoke_old_decision', 'queue: ' + queue + ', uid: ' + str(uid))

    success = ''
    error = ''
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    _t = Translator(lang)

    if queue == 'deletes':
        __revoke_decision_and_implications(ReviewDelete, LastReviewerDelete, uid, transaction)
        success = _t.get(_t.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_delete=uid))

    elif queue == 'optimizations':
        __revoke_decision_and_implications(ReviewOptimization, LastReviewerOptimization, uid, transaction)
        success = _t.get(_t.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_optimization=uid))

    elif queue == 'edits':
        db_review = DBDiscussionSession.query(ReviewEdit).filter_by(uid=uid).first()
        db_review.set_revoked(True)
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=uid).delete()
        db_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=uid)
        content = db_value.first().content
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=db_value.first().statement_uid).first()
        db_value.delete()
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_edit=uid))

        # delete forbidden textversion
        DBDiscussionSession.query(TextVersion).filter_by(content=content).delete()
        # grab and set most recent textversion
        db_new_textversion = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=db_statement.uid).order_by(TextVersion.uid.desc()).first()
        db_statement.set_textversion(db_new_textversion.uid)

        success = _t.get(_t.dataRemoved)

    else:
        error = _t.get(_t.internalKeyError)

    DBDiscussionSession.flush()
    transaction.commit()

    return success, error


def cancel_ongoing_decision(queue, uid, lang, transaction):
    """

    :param queue:
    :param uid:
    :param lang:
    :param transaction:
    :return:
    """
    logger('review_history_helper', 'cancel_ongoing_decision', 'queue: ' + queue + ', uid: ' + str(uid))
    success = ''
    error = ''

    _t = Translator(lang)
    if queue == 'deletes':
        DBDiscussionSession.query(ReviewDelete).filter_by(uid=uid).delete()
        DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=uid).delete()
        success = _t.get(_t.dataRemoved)

    elif queue == 'optimizations':
        DBDiscussionSession.query(ReviewOptimization).filter_by(uid=uid).delete()
        DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=uid).delete()
        success = _t.get(_t.dataRemoved)

    elif queue == 'edits':
        DBDiscussionSession.query(ReviewEdit).filter_by(uid=uid).delete()
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=uid).delete()
        DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=uid).delete()
        success = _t.get(_t.dataRemoved)

    else:
        error = _t.get(_t.internalKeyError)

    DBDiscussionSession.flush()
    transaction.commit()

    return success, error


def __revoke_decision_and_implications(type, reviewer_type, uid, transaction):
    """

    :param type:
    :param reviewer_type:
    :param uid:
    :param transaction:
    :return:
    """
    DBDiscussionSession.query(reviewer_type).filter_by(review_uid=uid).delete()

    db_review = DBDiscussionSession.query(type).filter_by(uid=uid).first()
    db_review.set_revoked(True)
    en_or_disable_object_of_review(db_review, False, transaction)

    DBDiscussionSession.flush()
    transaction.commit()
