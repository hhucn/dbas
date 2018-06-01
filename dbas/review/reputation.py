"""
Provides helping function for handling reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import arrow
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.logger import logger
from dbas.review import key_history, key_ongoing, key_edit, key_delete, key_duplicate, \
    key_optimization, key_merge, key_split
from dbas.review.queue import review_queues, all_queues
from dbas.strings.keywords import Keywords as _

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
        gains.append({'text': translator.get(key),
                      'points': '+' + str(gain.points)})

    db_looses = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points < 0).all()
    for loose in db_looses:
        key = _.get_key_by_string(loose.reason)
        looses.append({'text': translator.get(key),
                       'points': loose.points})

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


def add_reputation_for(db_user: User, reason):
    """
    Add reputation for the given nickname with the reason only iff the reason can be added. For example all reputation
    for 'first' things cannot be given twice.

    Anonymous user is not eligible to receive reputation.

    :param db_user: User in refactored fns, else nickname
    :param reason: reason as string, as given in reputation.py
    :return: boolean that is true, when the user reached 30points
    """
    logger('Reputation', 'main ' + reason)
    db_reason = DBDiscussionSession.query(ReputationReason).filter_by(reason=reason).first()

    logger('Reputation', 'user ' + str(db_user.uid))
    # special case:
    if '_first_' in reason:
        db_already_farmed = DBDiscussionSession.query(ReputationHistory).filter(
            ReputationHistory.reputation_uid == db_reason.uid,
            ReputationHistory.reputator_uid == db_user.uid).first()
        if db_already_farmed:
            logger('Reputation', 'karma already farmed')
            return False

    logger('Reputation', 'add ' + str(db_reason.points) + ' for ' + db_user.nickname)
    new_rep = ReputationHistory(reputator=db_user.uid, reputation=db_reason.uid)
    DBDiscussionSession.add(new_rep)
    DBDiscussionSession.flush()

    transaction.commit()
    return True


def has_access_to_review_system(db_user: User):
    """
    Check if the user has more points than the lowers border in the review system

    :param db_user:
    :return:
    """
    db_points = DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).join(
        ReputationReason).all()
    points = __collect_points(db_points)
    return points <= smallest_border


def __collect_points(reputation_history):
    """
    Sums up the points

    :param reputation_history: List of ReputationHistory joined with ReputationReason
    :return:
    """
    return sum([history.reputations.points for history in reputation_history])