"""
Provides helping function for handling reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import arrow
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.lib import nick_of_anonymous_user
from dbas.logger import logger
from dbas.review import reputation_borders, reputation_icons, all_queues, smallest_border
from dbas.strings.keywords import Keywords as _


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

    :param db_user: Should be of type "User", but also accepts nickname for legacy support
    :param only_today: Boolean
    :return: Integer and Boolean, if the user is author
    """
    if not isinstance(db_user, User):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=db_user).first()
    count = 0

    if not db_user or db_user.nickname == nick_of_anonymous_user:
        return count, False

    db_reputation = DBDiscussionSession.query(ReputationHistory)

    if only_today:
        today = arrow.utcnow().to('Europe/Berlin')
        db_reputation = db_reputation.filter(ReputationHistory.timestamp >= today)

    db_reputation = db_reputation.filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .all()

    count = sum([r.reputations.points for r in db_reputation])

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

    :param db_user:
    :return:
    """
    points = __collect_points(DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).join(ReputationReason).all())
    return points <= smallest_border


def __collect_points(reputation_history):
    """
    Sums up the points

    :param reputation_history: List of ReputationHistory joined with ReputationReason
    :return:
    """
    return sum([history.reputations.points for history in reputation_history])
