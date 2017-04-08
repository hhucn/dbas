"""
Provides helping function for the managing the queue with all executed decisions as well as all ongoing decisions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDelete, LastReviewerDelete, ReviewOptimization, \
    LastReviewerOptimization, User, ReputationHistory, ReputationReason, ReviewDeleteReason, ReviewEdit,\
    LastReviewerEdit, ReviewEditValue, TextVersion, Statement, ReviewCanceled, sql_timestamp_pretty_print,\
    ReviewDuplicate, LastReviewerDuplicate, RevokedDuplicate, Argument, Premise
from dbas.lib import get_text_for_argument_uid, get_profile_picture, is_user_author_or_admin, get_text_for_statement_uid
from dbas.logger import logger
from dbas.review.helper.main import en_or_disable_object_of_review
from dbas.review.helper.reputation import get_reputation_of, reputation_borders, reputation_icons
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from sqlalchemy import and_


def get_review_history(main_page, nickname, translator):
    """
    Returns the history of all reviews

    :param main_page: Host URL
    :param nickname: User.nickname
    :param translator: Translator
    :return: dict()
    """
    if not DBDiscussionSession.query(User).filter_by(nickname=nickname).first():
        return dict()
    return __get_data(main_page, nickname, translator, True)


def get_ongoing_reviews(main_page, nickname, translator):
    """"
    Returns the history of all reviews

    :param main_page: Host URL
    :param nickname: User.nickname
    :param translator: Translator
    :return: dict()
    """
    if not DBDiscussionSession.query(User).filter_by(nickname=nickname).first():
        return dict()
    return __get_data(main_page, nickname, translator, False)


def __get_data(main_page, nickname, translator, is_executed=False):
    """
    Collects data for every review queue

    :param main_page: Host URL
    :param nickname: User.nickname
    :param translator: Translator
    :param is_executed: Boolean
    :return: dict()
    """
    ret_dict = dict()
    if is_executed:
        ret_dict['has_access'] = __has_access_to_history(nickname)
    else:
        ret_dict['has_access'] = is_user_author_or_admin(nickname)
    ret_dict['is_history'] = is_executed

    deletes_list = __get_executed_reviews_of('deletes', main_page, ReviewDelete, LastReviewerDelete, translator, is_executed)
    optimizations_list = __get_executed_reviews_of('optimizations', main_page, ReviewOptimization, LastReviewerOptimization, translator, is_executed)
    edits_list = __get_executed_reviews_of('edits', main_page, ReviewEdit, LastReviewerEdit, translator, is_executed)
    duplicates_list = __get_executed_reviews_of('duplicates', main_page, ReviewDuplicate, LastReviewerDuplicate, translator, is_executed)

    past_decision = [{
        'title': 'Delete Queue',
        'icon': reputation_icons['deletes'],
        'queue': 'deletes',
        'content': deletes_list,
        'has_reason': True,
        'has_oem_text': False,
        'has_duplicate_text': False
    }, {
        'title': 'Optimization Queue',
        'queue': 'optimizations',
        'icon': reputation_icons['optimizations'],
        'content': optimizations_list,
        'has_reason': False,
        'has_oem_text': False,
        'has_duplicate_text': False
    }, {
        'title': 'Edit Queue',
        'queue': 'edits',
        'icon': reputation_icons['edits'],
        'content': edits_list,
        'has_reason': False,
        'has_oem_text': True,
        'has_duplicate_text': False
    }, {
        'title': 'Duplicates Queue',
        'queue': 'duplicates',
        'icon': reputation_icons['duplicates'],
        'content': duplicates_list,
        'has_reason': False,
        'has_oem_text': False,
        'has_duplicate_text': True
    }]
    ret_dict['past_decision'] = past_decision

    return ret_dict


def get_reputation_history_of(nickname, translator):
    """
    Returns the reputation history of an user

    :param nickname: User.nickname
    :param translator: Translator
    :return: dict()
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
    logger('History', '__get_executed_reviews_of', 'Table: {} ({})'.format(table, table_type))
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed == is_executed).order_by(table_type.uid.desc()).all()

    for review in db_reviews:
        entry = __get_executed_review_element_of(table, main_page, review, last_review_type, translator, is_executed)
        if entry:
            some_list.append(entry)

    return some_list


def __get_executed_review_element_of(table, main_page, review, last_review_type, translator, is_executed):
    """

    :param table: Shortcut for the table
    :param main_page: Main page of D-BAS
    :param review: Element
    :param last_review_type: Type of the last reviewer of the table
    :param translator: current ui_locales
    :param is_executed
    :return: Element
    """

    length = 35
    # getting text
    if table == 'duplicates':
        full_text = get_text_for_statement_uid(review.duplicate_statement_uid)
    elif review.statement_uid is None:
        full_text = get_text_for_argument_uid(review.argument_uid)
    else:
        full_text = get_text_for_statement_uid(review.statement_uid)

    # pretty print
    intro = translator.get(_.otherUsersSaidThat) + ' '
    if full_text.startswith(intro):
        short_text = full_text[len(intro):len(intro) + 1].upper() + full_text[len(intro) + 1:len(intro) + length]
    else:
        short_text = full_text[0:length]

    short_text += '...' if len(full_text) > length else '.'
    short_text = '<span class="text-primary">' + short_text + '</span>'

    is_okay = False if table == 'optimizations' else True
    # getting all pro and contra votes for this review
    all_votes = DBDiscussionSession.query(last_review_type).filter_by(review_uid=review.uid)
    pro_votes = all_votes.filter_by(is_okay=is_okay).all()
    con_votes = all_votes.filter(and_(last_review_type.is_okay != is_okay)).all()

    # getting the users which have voted
    pro_list = [__get_user_dict_for_review(pro.reviewer_uid, main_page) for pro in pro_votes]
    con_list = [__get_user_dict_for_review(con.reviewer_uid, main_page) for con in con_votes]

    if table == 'duplicates':
        # switch it, because contra is: it should not be there!
        tmp_list = pro_list
        pro_list = con_list
        con_list = tmp_list

    # and build up some dict
    entry = dict()
    entry['entry_id'] = review.uid
    tmp = __handle_table_of_review_element(table, entry, review, short_text, full_text, length, is_executed)
    if not tmp:
        entry = None
    else:
        entry.update(tmp)
        entry['pro'] = pro_list
        entry['con'] = con_list
        entry['timestamp'] = sql_timestamp_pretty_print(review.timestamp, translator.get_lang())
        entry['votes_pro'] = pro_list
        entry['votes_con'] = con_list
        entry['reporter'] = __get_user_dict_for_review(review.detector_uid, main_page)

    return entry


def __handle_table_of_review_element(table, entry, review, short_text, full_text, length, is_executed):
    """

    :param table:
    :param entry:
    :param review:
    :param short_text:
    :param full_text:
    :param length:
    :param is_executed:
    :return:
    """
    if table == 'deletes':
        db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(review.reason_uid)
        entry['reason'] = db_reason.reason
    entry['row_id'] = table + str(review.uid)
    entry['argument_shorttext'] = short_text
    entry['argument_fulltext'] = full_text

    if table == 'edits':
        if is_executed:
            db_textversions = DBDiscussionSession.query(TextVersion).filter_by(
                statement_uid=review.statement_uid).order_by(TextVersion.uid.desc()).all()
            entry['argument_oem_shorttext'] = db_textversions[1].content[0:length]
            entry['argument_oem_fulltext'] = db_textversions[1].content
        else:
            db_edit_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=review.uid).first()
            if not db_edit_value:
                entry = None
            else:
                entry['argument_oem_shorttext'] = short_text
                entry['argument_oem_fulltext'] = full_text
                entry['argument_shorttext'] = short_text.replace(short_text,
                                                                 (db_edit_value.content[0:length] + '...') if len(
                                                                     full_text) > length else db_edit_value.content)
                entry['argument_fulltext'] = db_edit_value.content

    if table == 'duplicates':
        text = get_text_for_statement_uid(review.original_statement_uid)
        entry['statement_duplicate_shorttext'] = text[0:length] + ('...' if len(text) > length else '')
        entry['statement_duplicate_fulltext'] = text

    return entry


def __get_user_dict_for_review(user_id, main_page):
    """
    Fetches some data of the given user.

    :param main_page: main_page of D-BAS
    :return: dict with gravatar, users page and nickname
    """
    db_user = DBDiscussionSession.query(User).get(user_id)
    image_url = get_profile_picture(db_user, 20)
    return {
        'gravatar_url': image_url,
        'nickname': db_user.get_global_nickname(),
        'userpage_url': main_page + '/user/' + str(db_user.uid)
    }


def __has_access_to_history(nickname):
    """
    Does the user has access to the history?

    :param nickname: User.nickname
    :return: Boolean
    """
    reputation_count, is_user_author = get_reputation_of(nickname)
    return is_user_author or reputation_count > reputation_borders['history']


def revoke_old_decision(queue, uid, lang, nickname):
    """
    Trys to revoke an old decision

    :param queue: Type of review
    :param uid: Review.uid
    :param lang: Language.ui_locales
    :param nickname: User.nickname
    :return: success, error
    :rtype: String, String
    """
    logger('review_history_helper', 'revoke_old_decision', 'queue: ' + queue + ', uid: ' + str(uid))

    success = ''
    error = ''
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    _t = Translator(lang)

    if queue == 'deletes':
        __revoke_decision_and_implications(ReviewDelete, LastReviewerDelete, uid)
        success = _t.get(_.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_delete=uid))

    elif queue == 'optimizations':
        __revoke_decision_and_implications(ReviewOptimization, LastReviewerOptimization, uid)
        success = _t.get(_.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_optimization=uid))

    elif queue == 'edits':
        db_review = DBDiscussionSession.query(ReviewEdit).get(uid)
        db_review.set_revoked(True)
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=uid).delete()
        db_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=uid)
        content = db_value.first().content
        db_statement = DBDiscussionSession.query(Statement).get(db_value.first().statement_uid)
        db_value.delete()
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_edit=uid))

        # delete forbidden textversion
        DBDiscussionSession.query(TextVersion).filter_by(content=content).delete()
        # grab and set most recent textversion
        db_new_textversion = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=db_statement.uid).order_by(TextVersion.uid.desc()).first()
        db_statement.set_textversion(db_new_textversion.uid)

        success = _t.get(_.dataRemoved)

    elif queue == 'duplicates':
        db_review = DBDiscussionSession.query(ReviewDuplicate).get(uid)
        db_review.set_revoked(True)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_duplicate=uid))
        __rebend_objects_of_duplicate_review(db_review)

        success = _t.get(_.dataRemoved)

    else:
        error = _t.get(_.internalKeyError)

    DBDiscussionSession.flush()
    transaction.commit()

    return success, error


def cancel_ongoing_decision(queue, uid, lang, nickname):
    """
    Cancel an ongoing review

    :param queue: Table of review
    :param uid: Review.uid
    :param lang: Translator.ui_locales
    :return: Success, Error
    :rtype: String, String
    """
    logger('review_history_helper', 'cancel_ongoing_decision', 'queue: ' + queue + ', uid: ' + str(uid))
    success = ''
    error = ''
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    _t = Translator(lang)
    if queue == 'deletes':
        DBDiscussionSession.query(ReviewDelete).get(uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=uid).delete()
        success = _t.get(_.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_delete=uid, was_ongoing=True))

    elif queue == 'optimizations':
        DBDiscussionSession.query(ReviewOptimization).get(uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=uid).delete()
        success = _t.get(_.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_optimization=uid, was_ongoing=True))

    elif queue == 'edits':
        DBDiscussionSession.query(ReviewEdit).filter_by(uid=uid).delete()
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=uid).first().set_revoked(True)
        DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=uid).delete()
        success = _t.get(_.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_edit=uid, was_ongoing=True))

    elif queue == 'duplicates':
        DBDiscussionSession.query(ReviewDuplicate).get(uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=uid).delete()
        success = _t.get(_.dataRemoved)
        DBDiscussionSession.add(ReviewCanceled(author=db_user.uid, review_duplicate=uid, was_ongoing=True))

    else:
        error = _t.get(_.internalKeyError)

    DBDiscussionSession.flush()
    transaction.commit()

    return success, error


def __revoke_decision_and_implications(type, reviewer_type, uid):
    """
    Revokes the old decision and the implications

    :param type: table of Review
    :param reviewer_type: Table of LastReviewer
    :param uid: Review.uid
    :return: None
    """
    DBDiscussionSession.query(reviewer_type).filter_by(review_uid=uid).delete()

    db_review = DBDiscussionSession.query(type).get(uid)
    db_review.set_revoked(True)
    en_or_disable_object_of_review(db_review, False)

    DBDiscussionSession.flush()
    transaction.commit()


def __rebend_objects_of_duplicate_review(db_review):
    """
    If something was bend (due to duplicates), lets rebend this

    :param db_review: Review
    :return: None
    """
    logger('review_history_helper', '__rebend_objects_of_duplicate_review', 'review: ' + str(db_review.uid))

    db_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
    db_statement.set_disable(False)   # TODO reset more than this ?
    DBDiscussionSession.add(db_statement)

    db_revoked_elements = DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=db_review.uid).all()
    for revoke in db_revoked_elements:
        if revoke.bend_position:
            db_statement = DBDiscussionSession.query(Statement).get(revoke.statement_uid)
            db_statement.set_position(False)
            DBDiscussionSession.add(db_statement)

        if revoke.argument_uid is not None:
            db_argument = DBDiscussionSession.query(Argument).get(revoke.argument_uid)
            text = 'Rebend conclusion of argument {} from {} to {}'.format(revoke.argument_uid, db_argument.conclusion_uid, db_review.duplicate_statement_uid)
            logger('review_history_helper', '__rebend_objects_of_duplicate_review', text)
            db_argument.conclusion_uid = db_review.duplicate_statement_uid
            DBDiscussionSession.add(db_argument)

        if revoke.premise_uid is not None:
            db_premise = DBDiscussionSession.query(Premise).get(revoke.premise_uid)
            text = 'Rebend premise {} from {} to {}'.format(revoke.premise_uid, db_premise.statement_uid, db_review.duplicate_statement_uid)
            logger('review_history_helper', '__rebend_objects_of_duplicate_review', text)
            db_premise.statement_uid = db_review.duplicate_statement_uid
            DBDiscussionSession.add(db_premise)
    DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=db_review.uid).delete()

    DBDiscussionSession.flush()
    transaction.commit()
