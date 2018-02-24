"""
Provides helping function for handling reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import arrow
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _

reputation_borders = {'deletes': 30,
                      'optimizations': 30,
                      'edits': 30,
                      'duplicates': 30,
                      'splits': 30,
                      'merges': 30,
                      'history': 150}

reputation_icons = {'deletes': 'fa fa-trash-o',
                    'optimizations': 'fa fa-flag',
                    'edits': 'fa fa-pencil-square-o',
                    'duplicates': 'fa fa-files-o',
                    'splits': 'fa fa-expand',
                    'merges': 'fa fa-compress',
                    'history': 'fa fa-history',
                    'ongoing': 'fa fa-clock-o'}

# every reason by its name
rep_reason_first_position = 'rep_reason_first_position'
rep_reason_first_justification = 'rep_reason_first_justification'
rep_reason_first_argument_click = 'rep_reason_first_argument_click'
rep_reason_first_confrontation = 'rep_reason_first_confrontation'
rep_reason_first_new_argument = 'rep_reason_first_new_argument'
rep_reason_new_statement = 'rep_reason_new_statement'
rep_reason_success_flag = 'rep_reason_success_flag'
rep_reason_success_edit = 'rep_reason_success_edit'
rep_reason_success_duplicate = 'rep_reason_success_duplicate'
rep_reason_bad_flag = 'rep_reason_bad_flag'
rep_reason_bad_edit = 'rep_reason_bad_edit'
rep_reason_bad_duplicate = 'rep_reason_bad_duplicate'


def get_privilege_list(translator):
    """
    Returns a list with all privileges and points.

    :param translator: instance of translator
    :return: list()
    """
    return [
        {'points': reputation_borders['deletes'], 'icon': reputation_icons['deletes'], 'text': translator.get(_.priv_access_opti_queue)},
        {'points': reputation_borders['optimizations'], 'icon': reputation_icons['optimizations'], 'text': translator.get(_.priv_access_del_queue)},
        {'points': reputation_borders['edits'], 'icon': reputation_icons['edits'], 'text': translator.get(_.priv_access_edit_queue)},
        {'points': reputation_borders['splits'], 'icon': reputation_icons['splits'], 'text': translator.get(_.priv_access_splits_queue)},
        {'points': reputation_borders['merges'], 'icon': reputation_icons['merges'], 'text': translator.get(_.priv_access_merges_queue)},
        {'points': reputation_borders['duplicates'], 'icon': reputation_icons['duplicates'], 'text': translator.get(_.priv_access_duplicate_queue)},
        {'points': reputation_borders['history'], 'icon': reputation_icons['history'], 'text': translator.get(_.priv_history_queue)}
    ]


def get_reputation_list(translator):
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


def get_reputation_of(db_user, only_today=False):
    """
    Return the total sum of reputation_borders points for the given nickname

    :param nickname: Nickname of the user
    :param only_today: Boolean
    :return: Integer and Boolean, if the user is author
    """
    if not isinstance(db_user, User):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=db_user).first()
    count = 0

    if not db_user:
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


def add_reputation_for(user, reason):
    """
    Add reputation for the given nickname with the reason only iff the reason can be added. For example all reputation
    for 'first' things cannot be given twice.

    :param user: User in refactored fns, else nickname
    :param reason: reason as string, as given in reputation.py
    :return: True, if the user gained reputation and an additional boolean that is true, when the user reached 30points
    """
    logger('ReputationPointHelper', 'main ' + reason)
    db_reason = DBDiscussionSession.query(ReputationReason).filter_by(reason=reason).first()

    if isinstance(user, str):  # TODO remove this check after refactoring
        db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    else:
        db_user = user

    if not db_reason or not db_user:
        logger('ReputationPointHelper', 'no reason or no user')
        return False, False

    logger('ReputationPointHelper', 'user ' + str(db_user.uid))
    # special case:
    if '_first_' in reason:
        db_already_farmed = DBDiscussionSession.query(ReputationHistory).filter(
            ReputationHistory.reputation_uid == db_reason.uid,
            ReputationHistory.reputator_uid == db_user.uid).first()
        if db_already_farmed:
            logger('ReputationPointHelper', 'karma already farmed')
            return False, False

    logger('ReputationPointHelper', 'add ' + str(db_reason.points) + ' for ' + db_user.nickname)
    db_old_points = __collect_points(DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).join(ReputationReason).all())
    new_rep = ReputationHistory(reputator=db_user.uid, reputation=db_reason.uid)
    DBDiscussionSession.add(new_rep)
    DBDiscussionSession.flush()

    transaction.commit()
    db_new_points = db_old_points + db_reason.points

    return True, db_old_points < 30 <= db_new_points


def __collect_points(reputation_history):
    """
    Sums up the points

    :param reputation_history: List of ReputationHistory joined with ReputationReason
    :return:
    """
    return sum([history.reputations.points for history in reputation_history])
