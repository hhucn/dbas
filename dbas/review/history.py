"""
Provides helping function for the managing the queue with all executed decisions as well as all ongoing decisions.
"""
import logging
from typing import Optional

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, sql_timestamp_pretty_print
from dbas.lib import get_profile_picture
from dbas.review import txt_len_history_page
from dbas.review.mapper import get_review_model_by_key, get_queue_by_key
from dbas.review.queue import key_edit, key_delete, key_duplicate, key_merge, key_split, review_queues, key_history, \
    key_ongoing
from dbas.review.queue.adapter import QueueAdapter
from dbas.review.reputation import get_reputation_of, reputation_borders
from dbas.review.reputation import reputation_icons
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital

LOG = logging.getLogger(__name__)


def get_review_history(main_page, db_user, translator):
    """
    Returns the history of all reviews

    :param main_page: Host URL
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    return __get_reviews_from_history_queue(main_page, db_user, translator, True)


def get_ongoing_reviews(main_page, db_user, translator):
    """"
    Returns the history of all reviews

    :param main_page: Host URL
    :param db_user: User
    :param translator: Translator
    :return: dict()
    """
    return __get_reviews_from_history_queue(main_page, db_user, translator, False)


def __get_reviews_from_history_queue(main_page, db_user, translator, is_executed=False):
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
        executed_list = __get_executed_reviews_of(key, main_page, review_table, translator, is_executed)
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
        'has_access': __has_access_to_history(db_user, is_executed),
        'is_history': is_executed,
        'past_decision': past_decision
    }


def __get_executed_reviews_of(table, main_page, table_type, translator, is_executed=False):
    """
    Returns array with all relevant information about the last reviews of the given table.

    :param table: Shortcut for the table
    :param main_page: Main page of D-BAS
    :param table_type: Type of the review table
    :param translator: current ui_locales
    :param is_executed
    :return: Array with all decision per table
    """
    LOG.debug("Table: %s (%s)", table, table_type)
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed == is_executed).order_by(
        table_type.uid.desc()).all()

    for review in db_reviews:
        entry = __get_executed_review_element_of(table, main_page, review, translator, is_executed)
        if entry:
            some_list.append(entry)

    return some_list


def __get_executed_review_element_of(table_key, main_page, db_review, translator, is_executed) -> Optional[dict]:
    """

    :param table_key: Shortcut for the table
    :param main_page: Main page of D-BAS
    :param db_review: Element
    :param translator: current ui_locales
    :param is_executed
    :return: Element
    """
    queue = get_queue_by_key(table_key)
    adapter = QueueAdapter(queue=queue(), application_url=main_page, translator=translator)
    full_text = adapter.get_text_of_element(db_review)
    if not full_text:
        return None

    # pretty print
    intro = translator.get(_.otherUsersSaidThat) + ' '
    if full_text.startswith(intro):
        short_text = full_text[len(intro):len(intro) + 1].upper()
        short_text += full_text[len(intro) + 1:len(intro) + txt_len_history_page]
    else:
        short_text = full_text[0:txt_len_history_page]

    short_text += '...' if len(full_text) > txt_len_history_page else '.'
    short_text = f'<span class="text-primary">{short_text}</span>'

    pro_list, con_list = adapter.get_all_votes_for(db_review)

    # and build up some dict
    pdict = __handle_table_of_review_element(table_key, db_review, short_text, full_text, is_executed)
    if not pdict:
        return None

    pdict['entry_id'] = db_review.uid
    pdict['timestamp'] = sql_timestamp_pretty_print(db_review.timestamp, translator.get_lang())
    pdict['votes_pro'] = pro_list
    pdict['votes_con'] = con_list
    pdict['reporter'] = __get_user_dict_for_review(db_review.detector_uid, main_page)

    return pdict


def __handle_table_of_review_element(table_key, review, short_text, full_text, is_executed):
    """

    :param table_key:
    :param review:
    :param short_text:
    :param full_text:
    :param is_executed:
    :return:
    """
    pdict = dict()
    pdict['row_id'] = table_key + str(review.uid)
    pdict['argument_shorttext'] = short_text
    pdict['argument_fulltext'] = full_text

    queue = get_queue_by_key(table_key)
    adapter = QueueAdapter(queue())
    return adapter.get_history_table_row(review, pdict, is_executed=is_executed, short_text=short_text,
                                         full_text=full_text)


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
        'userpage_url': f'{main_page}/user/{db_user.uid}'
    }


def __has_access_to_history(db_user, is_executed: bool) -> bool:
    """
    Does the user has access to the history?

    :param db_user: User
    :return: Boolean
    """
    reputation_count, is_user_author = get_reputation_of(db_user)
    rights = db_user.is_admin() or db_user.is_author()
    queue_key = key_history if is_executed else key_ongoing
    points = reputation_count > reputation_borders[queue_key]
    return rights or points
