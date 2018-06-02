"""
Provides helping function for the managing the queue with all executed decisions as well as all ongoing decisions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDelete, User, ReviewDeleteReason, \
    ReviewEdit, \
    ReviewEditValue, TextVersion, sql_timestamp_pretty_print, \
    ReviewDuplicate, Premise, ReviewMerge, ReviewSplit, \
    ReviewSplitValues, \
    ReviewMergeValues
from dbas.lib import get_text_for_argument_uid, get_profile_picture, get_text_for_statement_uid, \
    get_text_for_premisegroup_uid
from dbas.logger import logger
from dbas.review.mapper import get_last_reviewer_by_key, get_review_model_by_key
from dbas.review.queue import key_edit, key_delete, key_duplicate, key_optimization, key_merge, key_split, review_queues
from dbas.review.reputation import get_reputation_of, reputation_borders
from dbas.review.reputation import reputation_icons
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital


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
    past_decision = []
    for key in review_queues:
        review_table = get_review_model_by_key(key)
        last_reviewer = get_last_reviewer_by_key(key)
        executed_list = __get_executed_reviews_of(key, main_page, review_table, last_reviewer, translator, is_executed)
        past_decision.append({
            'title': start_with_capital(key) + ' Queue',
            'icon': reputation_icons[key],
            'queue': key,
            'content': executed_list,
            'has_reason': key in [key_delete],
            'has_oem_text': key in [key_edit, key_merge, key_split],
            'has_duplicate_text': key in [key_duplicate]
        })

    return {
        'has_access': is_executed and __has_access_to_history(db_user),
        'is_history': is_executed,
        'past_decision': past_decision
    }


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
    logger('History', f'Table: {table} ({table_type})')
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
    if table == key_duplicate:
        full_text = get_text_for_statement_uid(review.duplicate_statement_uid)
    elif table in [key_split, key_merge]:
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
    is_okay = False if table == key_optimization else True
    if table is key_merge:
        pro_votes = all_votes.filter_by(should_merge=is_okay).all()
        con_votes = all_votes.filter(last_review_type.should_merge != is_okay).all()
    elif table is key_split:
        pro_votes = all_votes.filter_by(should_split=is_okay).all()
        con_votes = all_votes.filter(last_review_type.should_split != is_okay).all()
    else:
        pro_votes = all_votes.filter_by(is_okay=is_okay).all()
        con_votes = all_votes.filter(last_review_type.is_okay != is_okay).all()

    # getting the users which have voted
    pro_list = [__get_user_dict_for_review(pro.reviewer_uid, main_page) for pro in pro_votes]
    con_list = [__get_user_dict_for_review(con.reviewer_uid, main_page) for con in con_votes]

    if table == key_duplicate:
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

    if table == key_delete:
        return __handle_table_of_review_delete(review, entry)

    if table == key_edit:
        return __handle_table_of_review_edit(review, length, entry, is_executed, short_text, full_text)

    if table == key_duplicate:
        return __handle_table_of_review_duplicate(review, length, entry)

    if table is key_split:
        return __handle_table_of_review_split(review, length, entry)

    if table is key_merge:
        return __handle_table_of_review_merge(review, length, entry)

    return entry


def __handle_table_of_review_delete(review: ReviewDelete, entry):
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(review.reason_uid)
    entry['reason'] = db_reason.reason
    return entry


def __handle_table_of_review_edit(review: ReviewEdit, length, entry, is_executed, short_text, full_text):
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


def __handle_table_of_review_duplicate(review: ReviewDuplicate, length, entry):
    text = get_text_for_statement_uid(review.original_statement_uid)
    if text is None:
        text = '...'
    entry['statement_duplicate_shorttext'] = text[0:length] + ('...' if len(text) > length else '')
    entry['statement_duplicate_fulltext'] = text
    return entry


def __handle_table_of_review_split(review: ReviewSplit, length, entry):
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


def __handle_table_of_review_merge(review: ReviewMerge, length, entry):
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
    rights = db_user.is_admin() or db_user.is_author()
    points = reputation_count > reputation_borders['history']
    return rights or points
