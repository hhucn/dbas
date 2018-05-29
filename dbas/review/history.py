"""
Provides helping function for the managing the queue with all executed decisions as well as all ongoing decisions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDelete, LastReviewerDelete, ReviewOptimization, \
    LastReviewerOptimization, User, ReputationHistory, ReputationReason, ReviewDeleteReason, ReviewEdit, \
    LastReviewerEdit, ReviewEditValue, TextVersion, Statement, ReviewCanceled, sql_timestamp_pretty_print, \
    ReviewDuplicate, LastReviewerDuplicate, RevokedDuplicate, Argument, Premise, ReviewMerge, ReviewSplit, \
    PremiseGroupMerged, PremiseGroupSplitted, LastReviewerSplit, LastReviewerMerge, ReviewSplitValues, \
    ReviewMergeValues, StatementReplacementsByPremiseGroupSplit, StatementReplacementsByPremiseGroupMerge, \
    ArgumentsAddedByPremiseGroupSplit
from dbas.lib import get_text_for_argument_uid, get_profile_picture, get_text_for_statement_uid, \
    get_text_for_premisegroup_uid
from dbas.logger import logger
from dbas.review import reputation_borders, reputation_icons, key_delete, key_merge, key_split, key_duplicate, key_edit, \
    key_optimization
from dbas.review.helper import set_able_object_of_review
from dbas.review.reputation import get_reputation_of
from dbas.strings.keywords import Keywords as _


def get_review_history(main_page, nickname, translator):
    """
    Returns the history of all reviews

    :param main_page: Host URL
    :param nickname: User.nickname
    :param translator: Translator
    :return: dict()
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return dict()
    return __get_data(main_page, db_user, translator, True)


def get_ongoing_reviews(main_page, db_user, translator):
    """"
    Returns the history of all reviews

    :param main_page: Host URL
    :param nickname: User.nickname
    :param translator: Translator
    :return: dict()
    """
    return __get_data(main_page, db_user, translator, False)


def __get_data(main_page, db_user, translator, is_executed=False):
    """
    Collects data for every review queue

    :param main_page: Host URL
    :param db_user: User
    :param translator: Translator
    :param is_executed: Boolean
    :return: dict()
    """
    ret_dict = dict()
    if is_executed:
        ret_dict['has_access'] = __has_access_to_history(db_user)
    else:
        ret_dict['has_access'] = db_user.is_admin() or db_user.is_author()
    ret_dict['is_history'] = is_executed

    deletes_list = __get_executed_reviews_of('deletes', main_page, ReviewDelete, LastReviewerDelete, translator,
                                             is_executed)
    optimizations_list = __get_executed_reviews_of('optimizations', main_page, ReviewOptimization,
                                                   LastReviewerOptimization, translator, is_executed)
    edits_list = __get_executed_reviews_of('edits', main_page, ReviewEdit, LastReviewerEdit, translator, is_executed)
    duplicates_list = __get_executed_reviews_of('duplicates', main_page, ReviewDuplicate, LastReviewerDuplicate,
                                                translator, is_executed)
    splits_list = __get_executed_reviews_of('splits', main_page, ReviewSplit, LastReviewerSplit, translator,
                                            is_executed)
    merges_list = __get_executed_reviews_of('merges', main_page, ReviewMerge, LastReviewerMerge, translator,
                                            is_executed)

    past_decision = [{
        'title': 'Delete Queue',
        'icon': reputation_icons[key_delete],
        'queue': 'deletes',
        'content': deletes_list,
        'has_reason': True,
        'has_oem_text': False,
        'has_duplicate_text': False
    }, {
        'title': 'Optimization Queue',
        'queue': 'optimizations',
        'icon': reputation_icons[key_optimization],
        'content': optimizations_list,
        'has_reason': False,
        'has_oem_text': False,
        'has_duplicate_text': False
    }, {
        'title': 'Edit Queue',
        'queue': 'edits',
        'icon': reputation_icons[key_edit],
        'content': edits_list,
        'has_reason': False,
        'has_oem_text': True,
        'has_duplicate_text': False
    }, {
        'title': 'Duplicates Queue',
        'queue': 'duplicates',
        'icon': reputation_icons[key_duplicate],
        'content': duplicates_list,
        'has_reason': False,
        'has_oem_text': False,
        'has_duplicate_text': True
    }, {
        'title': 'Splits Queue',
        'queue': 'splits',
        'icon': reputation_icons[key_split],
        'content': splits_list,
        'has_reason': False,
        'has_oem_text': True,
        'has_duplicate_text': False
    }, {
        'title': 'Merges Queue',
        'queue': 'merges',
        'icon': reputation_icons[key_merge],
        'content': merges_list,
        'has_reason': False,
        'has_oem_text': True,
        'has_duplicate_text': False
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
        .order_by(ReputationHistory.uid.asc()) \
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

    ret_dict['history'] = list(reversed(rep_list))

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
    logger('History', 'Table: {} ({})'.format(table, table_type))
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed == is_executed).order_by(
        table_type.uid.desc()).all()

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
    elif table in ['splits', 'merges']:
        full_text = get_text_for_premisegroup_uid(review.premisegroup_uid)
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

    all_votes = DBDiscussionSession.query(last_review_type).filter_by(review_uid=review.uid)
    is_okay = False if table == 'optimizations' else True
    if table is 'merges':
        pro_votes = all_votes.filter_by(should_merge=is_okay).all()
        con_votes = all_votes.filter(last_review_type.should_merge != is_okay).all()
    elif table is 'splits':
        pro_votes = all_votes.filter_by(should_split=is_okay).all()
        con_votes = all_votes.filter(last_review_type.should_split != is_okay).all()
    else:
        pro_votes = all_votes.filter_by(is_okay=is_okay).all()
        con_votes = all_votes.filter(last_review_type.is_okay != is_okay).all()

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
    entry['row_id'] = table + str(review.uid)
    entry['argument_shorttext'] = short_text
    entry['argument_fulltext'] = full_text
    entry['is_innocent'] = True

    if table == 'deletes':
        return __handle_table_of_review_delete(review, entry)

    if table == 'edits':
        return __handle_table_of_review_edit(review, length, entry, is_executed, short_text, full_text)

    if table == 'duplicates':
        return __handle_table_of_review_duplicate(review, length, entry)

    if table is 'splits':
        return __handle_table_of_review_split(review, length, entry)

    if table is 'merges':
        return __handle_table_of_review_merge(review, length, entry)

    return entry


def __handle_table_of_review_delete(review, entry):
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(review.reason_uid)
    entry['reason'] = db_reason.reason
    return entry


def __handle_table_of_review_edit(review, length, entry, is_executed, short_text, full_text):
    if is_executed:
        db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=review.statement_uid).order_by(
            TextVersion.uid.desc()).all()
        if len(db_textversions) == 0:
            entry['is_innocent'] = False
            text = 'Review {} is malicious / no text for statement'.format(review.uid)
            entry['argument_oem_shorttext'] = '<span class="text-danger">{}</span>'.format(text)
            entry['argument_oem_fulltext'] = text
        else:
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
    return entry


def __handle_table_of_review_duplicate(review, length, entry):
    text = get_text_for_statement_uid(review.original_statement_uid)
    if text is None:
        text = '...'
    entry['statement_duplicate_shorttext'] = text[0:length] + ('...' if len(text) > length else '')
    entry['statement_duplicate_fulltext'] = text
    return entry


def __handle_table_of_review_split(review, length, entry):
    oem_fulltext = get_text_for_premisegroup_uid(review.premisegroup_uid)
    full_text = oem_fulltext
    db_values = DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=review.uid).all()
    if db_values:
        full_text = str([value.content for value in db_values])
    entry['argument_oem_shorttext'] = oem_fulltext[0:length] + '...' if len(oem_fulltext) > length else oem_fulltext
    entry['argument_oem_fulltext'] = oem_fulltext
    entry['argument_shorttext'] = full_text[0:length] + '...' if len(full_text) > length else full_text
    entry['argument_fulltext'] = full_text
    return entry


def __handle_table_of_review_merge(review, length, entry):
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=review.premisegroup_uid).all()
    oem_fulltext = str([get_text_for_statement_uid(p.statement_uid) for p in db_premises])
    full_text = oem_fulltext
    db_values = DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=review.uid).all()
    if db_values:
        full_text = str([value.content for value in db_values])
    full_text = ' and '.join(full_text)
    entry['argument_oem_shorttext'] = oem_fulltext[0:length] + '...' if len(oem_fulltext) > length else oem_fulltext
    entry['argument_oem_fulltext'] = oem_fulltext
    entry['argument_shorttext'] = full_text[0:length] + '...' if len(full_text) > length else full_text
    entry['argument_fulltext'] = full_text
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
        'nickname': db_user.global_nickname,
        'userpage_url': main_page + '/user/' + str(db_user.uid)
    }


def __has_access_to_history(db_user):
    """
    Does the user has access to the history?

    :param nickname: User.nickname
    :return: Boolean
    """
    reputation_count, is_user_author = get_reputation_of(db_user)
    return is_user_author or reputation_count > reputation_borders['history']


def revoke_old_decision(queue, db_review, db_user):
    """
    Trys to revoke an old decision

    :param queue: Type of review
    :param db_review: Review
    :param db_user: User

    :return:
    """
    logger('review_history_helper', 'queue {} with uid {}'.format(queue, db_review.uid))

    review_canceled = None
    if queue == 'deletes':
        review_canceled = __revoke_old_deletes_decision(db_review, db_user)
    elif queue == 'optimizations':
        review_canceled = __revoke_old_optimizations_decision(db_review, db_user)
    elif queue == 'edits':
        review_canceled = __revoke_old_edits_decision(db_review, db_user)
    elif queue == 'duplicates':
        review_canceled = __revoke_old_duplicates_decision(db_review, db_user)
    elif queue == 'merges':
        review_canceled = __revoke_old_merges_decision(db_review, db_user)
    elif queue == 'splits':
        review_canceled = __revoke_old_splits_decision(db_review, db_user)
    DBDiscussionSession.add(review_canceled)
    DBDiscussionSession.flush()
    transaction.commit()
    return True


def __revoke_old_deletes_decision(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_history_helper', str(db_review.uid))
    __revoke_decision_and_implications(ReviewDelete, LastReviewerDelete, db_review.uid)
    return ReviewCanceled(author=db_user.uid, review_data={'delete': db_review.uid})


def __revoke_old_optimizations_decision(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_history_helper', str(db_review.uid))
    __revoke_decision_and_implications(ReviewOptimization, LastReviewerOptimization, db_review.uid)
    return ReviewCanceled(author=db_user.uid, review_data={'optimization': db_review.uid})


def __revoke_old_edits_decision(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_history_helper', str(db_review.uid))
    db_review = DBDiscussionSession.query(ReviewEdit).get(db_review.uid)
    db_review.set_revoked(True)
    DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).delete()
    db_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid)
    content = db_value.first().content
    db_value.delete()
    # delete forbidden textversion
    DBDiscussionSession.query(TextVersion).filter_by(content=content).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'edit': db_review.uid})


def __revoke_old_duplicates_decision(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_history_helper', str(db_review.uid))
    db_review = DBDiscussionSession.query(ReviewDuplicate).get(db_review.uid)
    db_review.set_revoked(True)
    __rebend_objects_of_duplicate_review(db_review)
    return ReviewCanceled(author=db_user.uid, review_data={'duplicate': db_review.uid})


def __revoke_old_merges_decision(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_history_helper', str(db_review.uid))
    db_review = DBDiscussionSession.query(ReviewMerge).get(db_review.uid)
    db_review.set_revoked(True)
    db_pgroup_merged = DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=db_review.uid).all()
    replacements = DBDiscussionSession.query(StatementReplacementsByPremiseGroupMerge).filter_by(
        review_uid=db_review.uid).all()
    __undo_premisegroups(db_pgroup_merged, replacements)
    DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=db_review.uid).delete()
    DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=db_review.uid).delete()
    DBDiscussionSession.query(StatementReplacementsByPremiseGroupMerge).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'merges': db_review.uid})


def __revoke_old_splits_decision(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_history_helper', str(db_review.uid))
    db_review = DBDiscussionSession.query(ReviewSplit).get(db_review.uid)
    db_review.set_revoked(True)
    db_pgroup_splitted = DBDiscussionSession.query(PremiseGroupSplitted).filter_by(review_uid=db_review.uid).all()
    replacements = DBDiscussionSession.query(StatementReplacementsByPremiseGroupSplit).filter_by(
        review_uid=db_review.uid).all()
    disable_args = [arg.uid for arg in DBDiscussionSession.query(ArgumentsAddedByPremiseGroupSplit).filter_by(
        review_uid=db_review.uid).all()]
    __undo_premisegroups(db_pgroup_splitted, replacements)
    __disable_arguments_by_id(disable_args)
    DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=db_review.uid).delete()
    DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=db_review.uid).delete()
    DBDiscussionSession.query(StatementReplacementsByPremiseGroupSplit).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'splits': db_review.uid})


def __disable_arguments_by_id(argument_uids):
    """
    Disbale the list of argument by their id

    :param Argument_uids: list of argument.uid
    :return: None
    """
    for uid in argument_uids:
        db_arg = DBDiscussionSession.query(Argument).get(uid)
        db_arg.set_disabled(True)
        DBDiscussionSession.add(db_arg)
        DBDiscussionSession.flush()


def __undo_premisegroups(pgroups_splitted_or_merged, replacements):
    """

    :param pgroups_splitted_or_merged:
    :param replacements:
    :return:
    """
    logger('review_history_helper',
           'Got {} merge/splitted pgroups and {} replacements'.format(len(pgroups_splitted_or_merged),
                                                                      len(replacements)))

    for element in pgroups_splitted_or_merged:
        old_pgroup = element.old_premisegroup_uid
        new_pgroup = element.new_premisegroup_uid

        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=new_pgroup).all()
        for argument in db_arguments:
            logger('review_history_helper',
                   'reset arguments {} pgroup from {} back to {}'.format(argument.uid, new_pgroup, old_pgroup))
            argument.set_premisegroup(old_pgroup)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.flush()

    for element in replacements:
        old_statement = element.old_statement_uid
        new_statement = element.new_statement_uid

        db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=new_statement).all()
        for argument in db_arguments:
            logger('review_history_helper',
                   'reset arguments {} conclusion from {} back to {}'.format(argument.uid, new_statement,
                                                                             old_statement))
            argument.set_conclusion(old_statement)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.flush()

    DBDiscussionSession.flush()
    transaction.commit()


def cancel_ongoing_decision(queue, db_review, db_user):
    """
    Cancel an ongoing review

    :param queue: Table name of review
    :param db_review: Review
    :param db_user: User
    :return: Success, Error
    """
    logger('review_history_helper', 'queue {} uid {}'.format(queue, db_review.uid))

    review_canceled = None
    if queue == 'deletes':
        review_canceled = __cancel_ongoing_deletes_decision(db_review, db_user)
    elif queue == 'optimizations':
        review_canceled = __cancel_ongoing_optimizations_decision(db_review, db_user)
    elif queue == 'edits':
        review_canceled = __cancel_ongoing_edits_decision(db_review, db_user)
    elif queue == 'duplicates':
        review_canceled = __cancel_ongoing_duplicates_decision(db_review, db_user)
    elif queue == 'merges':
        review_canceled = __cancel_ongoing_merges_decision(db_review, db_user)
    elif queue == 'splits':
        review_canceled = __cancel_ongoing_splits_decision(db_review, db_user)

    DBDiscussionSession.add(review_canceled)
    DBDiscussionSession.flush()
    transaction.commit()
    return True


def __cancel_ongoing_deletes_decision(db_review: ReviewDelete, db_user: User):
    """
    Cancel an ongoing vote of the deletes queue

    :param db_review: ReviewDelete
    :param db_user: User
    :return:
    """
    DBDiscussionSession.query(ReviewDelete).get(db_review.uid).set_revoked(True)
    DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'delete': db_review.uid}, was_ongoing=True)


def __cancel_ongoing_optimizations_decision(db_review: ReviewOptimization, db_user: User):
    """
    Cancel an ongoing vote of the optimizations queue

    :param db_review: ReviewOptimization
    :param db_user: User
    :return:
    """
    DBDiscussionSession.query(ReviewOptimization).get(db_review.uid).set_revoked(True)
    DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'optimization': db_review.uid}, was_ongoing=True)


def __cancel_ongoing_edits_decision(db_review: ReviewEdit, db_user: User):
    """
    Cancel an ongoing vote of the edits queue

    :param db_review: ReviewOptimization
    :param db_user: User
    """
    DBDiscussionSession.query(ReviewEdit).filter_by(uid=db_review.uid).delete()
    DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).first().set_revoked(True)
    DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'edit': db_review.uid}, was_ongoing=True)


def __cancel_ongoing_duplicates_decision(db_review: ReviewDuplicate, db_user: User):
    """
    Cancel an ongoing vote of the duplications queue

    :param db_review: ReviewDuplicate
    :param db_user: User
    """
    DBDiscussionSession.query(ReviewDuplicate).get(db_review.uid).set_revoked(True)
    DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'duplicate': db_review.uid}, was_ongoing=True)


def __cancel_ongoing_merges_decision(db_review: ReviewMerge, db_user: User):
    """
    Cancel an ongoing vote of the merges queue

    :param db_review: ReviewOptimization
    :param db_user: User
    """
    DBDiscussionSession.query(ReviewMerge).get(db_review.uid).set_revoked(True)
    DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=db_review.uid).delete()
    DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'merge': db_review.uid}, was_ongoing=True)


def __cancel_ongoing_splits_decision(db_review: ReviewSplit, db_user: User):
    """
    Cancel an ongoing vote of the splits queue

    :param db_review: ReviewSplit
    :param db_user: User
    """
    DBDiscussionSession.query(ReviewSplit).get(db_review.uid).set_revoked(True)
    DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=db_review.uid).delete()
    DBDiscussionSession.query(PremiseGroupSplitted).filter_by(review_uid=db_review.uid).delete()
    return ReviewCanceled(author=db_user.uid, review_data={'split': db_review.uid}, was_ongoing=True)


def __is_uid_valid(uid, queue):
    """
    Check for the specific review in the fiven queue

    :param queue: Table of review
    :param uid: Review.uid
    :return: Boolean
    :rtype: Boolean
    """

    mapping = {
        'deletes': ReviewDelete,
        'optimizations': ReviewOptimization,
        'edits': ReviewEdit,
        'duplicates': ReviewDuplicate,
        'merges': ReviewMerge,
        'splits': ReviewSplit,
    }

    if queue in mapping:
        logger('review_history_helper', 'query table {} with uid {}'.format(mapping[queue], uid))
        return DBDiscussionSession.query(mapping[queue]).get(uid) is not None

    logger('review_history_helper', 'no table found for {}'.format(queue), error=True)
    return False


def __revoke_decision_and_implications(ttype, reviewer_type, uid):
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


def __rebend_objects_of_duplicate_review(db_review):
    """
    If something was bend (due to duplicates), lets rebend this

    :param db_review: Review
    :return: None
    """
    logger('review_history_helper', 'review: ' + str(db_review.uid))

    db_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
    db_statement.set_disabled(False)
    DBDiscussionSession.add(db_statement)

    db_revoked_elements = DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=db_review.uid).all()
    for revoke in db_revoked_elements:
        if revoke.bend_position:
            db_statement = DBDiscussionSession.query(Statement).get(revoke.statement_uid)
            db_statement.set_position(False)
            DBDiscussionSession.add(db_statement)

        if revoke.argument_uid is not None:
            db_argument = DBDiscussionSession.query(Argument).get(revoke.argument_uid)
            text = 'Rebend conclusion of argument {} from {} to {}'.format(revoke.argument_uid,
                                                                           db_argument.conclusion_uid,
                                                                           db_review.duplicate_statement_uid)
            logger('review_history_helper', text)
            db_argument.conclusion_uid = db_review.duplicate_statement_uid
            DBDiscussionSession.add(db_argument)

        if revoke.premise_uid is not None:
            db_premise = DBDiscussionSession.query(Premise).get(revoke.premise_uid)
            text = 'Rebend premise {} from {} to {}'.format(revoke.premise_uid, db_premise.statement_uid,
                                                            db_review.duplicate_statement_uid)
            logger('review_history_helper', text)
            db_premise.statement_uid = db_review.duplicate_statement_uid
            DBDiscussionSession.add(db_premise)
    DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=db_review.uid).delete()

    DBDiscussionSession.flush()
    transaction.commit()
