"""
Provides helping function for handling reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.lib import is_user_author
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from sqlalchemy import and_

reputation_borders = {'deletes': 30,
                      'optimizations': 30,
                      'edits': 30,
                      'history': 150}

reputation_icons = {'deletes': 'fa fa-pencil-square-o',
                    'optimizations': 'fa fa-flag',
                    'edits': 'fa fa-pencil-square-o',
                    'history': 'fa fa-history'}

# every reason by its name
rep_reason_first_position = 'rep_reason_first_position'
rep_reason_first_justification = 'rep_reason_first_justification'
rep_reason_first_argument_click = 'rep_reason_first_argument_click'
rep_reason_first_confrontation = 'rep_reason_first_confrontation'
rep_reason_first_new_argument = 'rep_reason_first_new_argument'
rep_reason_new_statement = 'rep_reason_new_statement'
rep_reason_success_flag = 'rep_reason_success_flag'
rep_reason_success_edit = 'rep_reason_success_edit'
rep_reason_bad_flag = 'rep_reason_bad_flag'
rep_reason_bad_edit = 'rep_reason_bad_edit'


def get_privilege_list(translator):
    """
    Returns a list with all privileges and points.

    :param translator: instance of translator
    :return: list()
    """
    return [{'points': reputation_borders['history'], 'icon': reputation_icons['history'],
             'text': translator.get(_.priv_history_queue)},
            {'points': reputation_borders['deletes'], 'icon': reputation_icons['deletes'],
             'text': translator.get(_.priv_access_opti_queue)},
            {'points': reputation_borders['optimizations'], 'icon': reputation_icons['optimizations'],
             'text': translator.get(_.priv_access_del_queue)},
            {'points': reputation_borders['edits'], 'icon': reputation_icons['optimizations'],
             'text': translator.get(_.priv_access_edit_queue)}]


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


def get_reputation_of(nickname):
    """
    Return the total sum of reputation_borders points for the given nickname

    :param nickname: Nickname of the user
    :return: Integer and Boolean, if the user is author
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    count = 0

    if db_user:
        db_reputation = DBDiscussionSession.query(ReputationHistory) \
            .filter_by(reputator_uid=db_user.uid) \
            .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
            .all()

        for reputation in db_reputation:
            count += reputation.reputations.points

    return count, is_user_author(nickname)


def add_reputation_for(user, reason, transaction):
    """
    Add reputation for the given nickname with the reason only iff the reason can be added. (For example all reputataion
    for 'first' things cannot be given twice.

    :param user: current user oder his nickname
    :param reason: reason as string, as given in reputation.py
    :param transaction: current transaction
    :return: True, if the user gained reputation
    """
    logger('ReputationPointHelper', 'add_reputation_for', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first() if isinstance(user, str) else user
    db_reason = DBDiscussionSession.query(ReputationReason).filter_by(reason=reason).first()
    if not db_reason or not db_user:
        return False

    # special case:
    if '_first_' in reason:
        db_already_farmed = DBDiscussionSession.query(ReputationHistory).filter(
            and_(ReputationHistory.reputation_uid == db_reason.uid,
                 ReputationHistory.reputator_uid == db_user.uid)).first()
        if db_already_farmed:
            return False

    logger('ReputationPointHelper', 'add_reputation_for', 'add ' + str(db_reason.points) + ' for ' + db_user.nickname)
    new_rep = ReputationHistory(reputator=db_user.uid, reputation=db_reason.uid)
    DBDiscussionSession.add(new_rep)
    DBDiscussionSession.flush()
    transaction.commit()
    return True
