"""
Provides helping function for handling reputation.
"""
import logging
from enum import Enum
from typing import Optional

import arrow

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason, sql_timestamp_pretty_print
from dbas.lib import nick_of_anonymous_user
from dbas.review.queue import review_queues, all_queues, key_edit, key_delete, key_duplicate, key_optimization, \
    key_merge, key_split, key_history, key_ongoing
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio

LOG = logging.getLogger(__name__)
smallest_border = 30
limit_to_open_issues = 10
reputation_borders = {**{key: smallest_border for key in review_queues}, **{key_history: 150, key_ongoing: 300}}
reputation_icons = {
    key_edit: 'fa fa-pencil-square-o',
    key_delete: 'fa fa-trash-o',
    key_duplicate: 'fa fa-files-o',
    key_optimization: 'fa fa-compress',
    key_merge: 'fa fa-flag',
    key_split: 'fa fa-expand',
    key_history: 'fa fa-history',
    key_ongoing: 'fa fa-clock-o'
}


class ReputationReasons(Enum):
    first_position = 'first_position'
    first_justification = 'first_justification'
    first_argument_click = 'first_argument_click'
    first_confrontation = 'first_confrontation'
    first_new_argument = 'first_new_argument'
    new_statement = 'new_statement'
    success_flag = 'success_flag'
    success_edit = 'success_edit'
    success_duplicate = 'success_duplicate'
    bad_flag = 'bad_flag'
    bad_edit = 'bad_edit'
    bad_duplicate = 'bad_duplicate'

    @staticmethod
    def values():
        return list(map(lambda r: r.value, ReputationReasons))

    @staticmethod
    def list():
        return list(ReputationReasons)


def get_privilege_list(translator):
    """
    Returns a list with all privileges and points.

    :param translator: instance of translator
    :return: list()
    """
    return [{
        'points': reputation_borders[key],
        'icon': reputation_icons[key],
        'text': translator.get(_.get_key_by_string(_.priv_access_x_queue.value.format(key))),
    } for key in all_queues]


def get_reputation_reasons_list(translator):
    """
    Returns a list with all reputations and points.

    :param translator:
    :return: list()
    """
    gains = list()
    looses = list()

    db_gains = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points > 0).all()
    for gain in db_gains:
        key = _.get_key_by_string(gain.reason)
        gains.append({
            'text': translator.get(key),
            'points': f'+{gain.points}'
        })

    db_looses = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points < 0).all()
    for loose in db_looses:
        key = _.get_key_by_string(loose.reason)
        looses.append({
            'text': translator.get(key),
            'points': loose.points
        })

    return {'gains': gains, 'looses': looses}


def get_reputation_of(db_user: User, only_today=False):
    """
    Return the total sum of reputation_borders points for the given nickname

    :param db_user: Should be of type "User"
    :param only_today: Boolean
    :return: Integer and Boolean, if the user is author
    """
    if not db_user:
        return 0, False

    db_reputation = DBDiscussionSession.query(ReputationHistory)

    if only_today:
        today = arrow.utcnow().to('Europe/Berlin')
        db_reputation = db_reputation.filter(ReputationHistory.timestamp >= today)

    db_reputation = db_reputation.filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .all()

    count = sum([rep.reputations.points for rep in db_reputation])

    return count, db_user.is_author() or db_user.is_admin()


def add_reputation_for(db_user: User, db_reason: ReputationReason):
    """
    Add reputation for the given nickname with the reason only iff the reason can be added. For example all reputation
    for 'first' things cannot be given twice.

    Anonymous user is not eligible to receive reputation.

    :param db_user: User in refactored fns, else nickname
    :param db_reason: ReputationReason
    :return: boolean that is true, when the user reached 30points
    """
    LOG.debug("Main %s, user %s", db_reason.reason, db_user.uid)
    # special case:
    if db_user.nickname == nick_of_anonymous_user:
        return False

    if '_first_' in db_reason.reason:
        db_already_farmed = DBDiscussionSession.query(ReputationHistory).filter(
            ReputationHistory.reputation_uid == db_reason.uid,
            ReputationHistory.reputator_uid == db_user.uid).first()
        if db_already_farmed:
            LOG.debug("Karma already farmed")
            return False

    LOG.debug("Add %s for %s", db_reason.reason, db_user.nickname)
    new_rep = ReputationHistory(reputator=db_user.uid, reputation=db_reason.uid)
    DBDiscussionSession.add(new_rep)
    DBDiscussionSession.flush()
    return True


def has_access_to_review_system(db_user: User):
    """
    Check if the user has more points than the lowers border in the review system

    :param db_user:
    :return:
    """
    if db_user.nickname == nick_of_anonymous_user:
        return False

    db_points = DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).join(
        ReputationReason).all()
    points = _collect_points(db_points)
    return points >= smallest_border


def _collect_points(reputation_history):
    """
    Sums up the points

    :param reputation_history: List of ReputationHistory joined with ReputationReason
    :return:
    """
    return sum([history.reputations.points for history in reputation_history])


def get_reason_by_action(reason: ReputationReasons) -> Optional[ReputationReason]:
    """
    Returns the reason string from database by its action. Currently we have the following actions:
     - first_position -> rep_reason_first_position
     - first_justification -> rep_reason_first_justification
     - first_argument_click -> rep_reason_first_argument_click
     - first_confrontation -> rep_reason_first_confrontation
     - first_new_argument -> rep_reason_first_new_argument
     - new_statement -> rep_reason_new_statement
     - success_flag -> rep_reason_success_flag
     - success_edit -> rep_reason_success_edit
     - success_duplicate -> rep_reason_success_duplicate
     - bad_flag -> rep_reason_bad_flag
     - bad_edit -> rep_reason_bad_edit
     - bad_duplicate -> rep_reason_bad_duplicate

    :param reason:
    :return:
    """
    reason_str = f'rep_reason_{reason.value}'
    return DBDiscussionSession.query(ReputationReason).filter_by(reason=reason_str).first()


def get_history_of(db_user: User, translator: Translator):
    """
    Returns the reputation history of an user

    :param db_user: User
    :param translator: Translator
    :return: dict()
    """

    db_reputation = DBDiscussionSession.query(ReputationHistory) \
        .filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .order_by(ReputationHistory.uid.asc()) \
        .all()

    rep_list = []
    for rep in db_reputation:
        date = sql_timestamp_pretty_print(rep.timestamp, translator.get_lang(), humanize=False)
        points_data = ('+' if rep.reputations.points > 0 else '') + str(rep.reputations.points)
        rep_list.append({
            'date': date,
            'points_data': points_data,
            'action': translator.get(rep.reputations.reason),
            'points': rep.reputations.points
        })

    count, all_rights = get_reputation_of(db_user)
    return {
        'count': count,
        'all_rights': all_rights,
        'history': list(reversed(rep_list))
    }


def add_reputation_and_check_review_access(db_user: User, reason: ReputationReasons) -> bool:
    """

    :param db_user:
    :param reason:
    :return:
    """
    had_access = has_access_to_review_system(db_user)
    add_reputation_for(db_user, get_reason_by_action(reason))
    broke_limit = has_access_to_review_system(db_user) and not had_access
    return broke_limit


def add_reputation_and_send_popup(db_user: User, db_rep_reason: Optional[ReputationReason], main_page: str,
                                  translator: Translator) -> bool:
    """
    Adds reputation to a specific user and checks (send info popup) to this user. Returns true if the user now has
    access

    :param db_user: user, which should get reputation
    :param db_rep_reason: Any reputation reason
    :param main_page: URL of the app
    :param translator: Instance of a translator
    :return:
    """
    has_access = has_access_to_review_system(db_user)
    add_reputation_for(db_user, db_rep_reason)

    # send popup if the user had not access but not she has
    if not has_access and has_access_to_review_system(db_user):
        send_request_for_info_popup_to_socketio(db_user.nickname, translator.get(_.youAreAbleToReviewNow),
                                                f'{main_page}/review')
        return True
    return False
