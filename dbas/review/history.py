"""
Provides helping function for the managing the queue with all executed decisions as well as all ongoing decisions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, sql_timestamp_pretty_print, Statement, PremiseGroup
from dbas.lib import get_text_for_argument_uid, get_profile_picture
from dbas.logger import logger
from dbas.review import txt_len_history_page
from dbas.review.mapper import get_last_reviewer_by_key, get_review_model_by_key, get_queue_by_key
from dbas.review.queue import key_edit, key_delete, key_duplicate, key_optimization, key_merge, key_split, review_queues
from dbas.review.queue.adapter import QueueAdapter
from dbas.review.reputation import get_reputation_of, reputation_borders
from dbas.review.reputation import reputation_icons
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital


def get_review_history(main_page, db_user, translator):
    """
    Returns the history of all reviews

    :param main_page: Host URL
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    return __get_reviews_from_histor_queue(main_page, db_user, translator, True)


def get_ongoing_reviews(main_page, db_user, translator):
    """"
    Returns the history of all reviews

    :param main_page: Host URL
    :param nickname: User.nickname
    :param translator: Translator
    :return: dict()
    """
    return __get_reviews_from_histor_queue(main_page, db_user, translator, False)


def __get_reviews_from_histor_queue(main_page, db_user, translator, is_executed=False):
    """

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


def __get_executed_review_element_of(table_key, main_page, db_review, last_review_type, translator, is_executed):
    """

    :param table_key: Shortcut for the table
    :param main_page: Main page of D-BAS
    :param db_review: Element
    :param last_review_type: Type of the last reviewer of the table
    :param translator: current ui_locales
    :param is_executed
    :return: Element
    """

    full_text = __get_full_text(db_review, table_key)

    # pretty print
    intro = translator.get(_.otherUsersSaidThat) + ' '
    if full_text.startswith(intro):
        short_text = full_text[len(intro):len(intro) + 1].upper()
        short_text += full_text[len(intro) + 1:len(intro) + txt_len_history_page]
    else:
        short_text = full_text[0:txt_len_history_page]

    short_text += '...' if len(full_text) > txt_len_history_page else '.'
    short_text = f'<span class="text-primary">{short_text}</span>'

    pro_list, con_list = __get_votes(db_review, table_key, last_review_type, main_page)

    # and build up some dict
    entry = dict()
    entry['entry_id'] = db_review.uid
    tmp = __handle_table_of_review_element(table_key, entry, db_review, short_text, full_text, is_executed)
    if not tmp:
        return None

    entry.update(tmp)
    entry['pro'] = pro_list
    entry['con'] = con_list
    entry['timestamp'] = sql_timestamp_pretty_print(db_review.timestamp, translator.get_lang())
    entry['votes_pro'] = pro_list
    entry['votes_con'] = con_list
    entry['reporter'] = __get_user_dict_for_review(db_review.detector_uid, main_page)

    return entry


def __get_full_text(db_review, table_key):
    """

    :param db_review:
    :param table_key:
    :return:
    """
    if table_key == key_duplicate:
        full_text = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid).get_text()
    elif table_key in [key_split, key_merge]:
        full_text = DBDiscussionSession.query(PremiseGroup).get(db_review.premisegroup_uid).get_text()
    elif db_review.statement_uid is None:
        full_text = get_text_for_argument_uid(db_review.argument_uid)
    else:
        full_text = DBDiscussionSession.query(Statement).get(db_review.statement_uid).get_text()
    return full_text


def __get_votes(db_review, table_key, last_review_type, main_page):
    """

    :param db_review:
    :param table_key:
    :param last_review_type:
    :param main_page:
    :return:
    """
    all_votes = DBDiscussionSession.query(last_review_type).filter_by(review_uid=db_review.uid)
    is_okay = False if table_key == key_optimization else True

    if table_key is key_merge:
        pro_votes = all_votes.filter_by(should_merge=is_okay).all()
        con_votes = all_votes.filter(last_review_type.should_merge != is_okay).all()
    elif table_key is key_split:
        pro_votes = all_votes.filter_by(should_split=is_okay).all()
        con_votes = all_votes.filter(last_review_type.should_split != is_okay).all()
    else:
        pro_votes = all_votes.filter_by(is_okay=is_okay).all()
        con_votes = all_votes.filter(last_review_type.is_okay != is_okay).all()

    # getting the users which have voted
    pro_list = [__get_user_dict_for_review(pro.reviewer_uid, main_page) for pro in pro_votes]
    con_list = [__get_user_dict_for_review(con.reviewer_uid, main_page) for con in con_votes]

    if table_key == key_duplicate:
        # switch it, because contra is: it should not be there!
        pro_list, con_list = con_list, pro_list

    return pro_list, con_list


def __handle_table_of_review_element(table_key, entry, review, short_text, full_text, is_executed):
    """

    :param table_key:
    :param entry:
    :param review:
    :param short_text:
    :param full_text:
    :param is_executed:
    :return:
    """
    entry['row_id'] = table_key + str(review.uid)
    entry['argument_shorttext'] = short_text
    entry['argument_fulltext'] = full_text
    entry['is_innocent'] = True

    if table_key in review_queues:
        queue = get_queue_by_key(table_key)
        adapter = QueueAdapter(queue())
        return adapter.get_history_table_row(review, entry, is_executed=is_executed, short_text=short_text,
                                             full_text=full_text)

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
