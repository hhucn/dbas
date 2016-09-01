"""
Provides helping function for the managing reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.lib import is_user_author

reputation_borders = {'deletes': 30,
                      'optimizations': 30,
                      'history': 100}

reputation_icons = {'deletes': 'fa fa-pencil-square-o',
                    'optimizations': 'fa fa-flag',
                    'history': 'fa fa-history'}

# every reason by its name
rep_reason_first_position       = 'rep_reason_first_position'
rep_reason_first_justification  = 'rep_reason_first_justification'
rep_reason_first_argument_click = 'rep_reason_first_argument_click'
rep_reason_first_confrontation  = 'rep_reason_first_confrontation'
rep_reason_first_argument       = 'rep_reason_first_argument'
rep_reason_new_statement        = 'rep_reason_new_statement'
rep_reason_success_flag         = 'rep_reason_success_flag'
rep_reason_success_edit         = 'rep_reason_success_edit'
rep_reason_bad_flag             = 'rep_reason_bad_flag'
rep_reason_bad_edit             = 'rep_reason_bad_edit'


def get_privilege_list(translator):
    """

    :param translator:
    :return:
    """

    reputations = list()
    reputations.append({'points': reputation_borders['history'], 'icon': reputation_icons['history'], 'text': translator.get(translator.priv_history_queue)})
    reputations.append({'points': reputation_borders['deletes'], 'icon': reputation_icons['deletes'], 'text': translator.get(translator.priv_access_opti_queue)})
    reputations.append({'points': reputation_borders['optimizations'], 'icon': reputation_icons['optimizations'], 'text': translator.get(translator.priv_access_del_queue)})
    return reputations


def get_reputation_list(translator):
    """

    :param translator:
    :return:
    """
    gains = list()
    looses = list()

    db_gains = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points > 0).all()
    for gain in db_gains:
        gains.append({'text': translator.get(gain.reason),
                      'points': '+' + str(gain.points)})

    db_looses = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points < 0).all()
    for loose in db_looses:
        looses.append({'text': translator.get(loose.reason),
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
        db_reputation = DBDiscussionSession.query(ReputationHistory)\
            .filter_by(reputator_uid=db_user.uid)\
            .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid)\
            .all()

        for reputation in db_reputation:
            count += reputation.reputations.points

    return count, is_user_author(nickname)


def add_reputation_for(db_user, reason, transaction):
    """
    Add reputation for the given nickname with the reason only iff the reason can be added. (For example all reputataion
    for 'first' things cannot be given twice.

    :param db_user:
    :param reason:
    :param transaction:
    :return:
    """
    db_reason = DBDiscussionSession.query(ReputationReason).filter_by(reason=reason).first()
    if not db_reason:
        return False

    # special case:
    if '_first_' in reason:
        db_already_farmed = DBDiscussionSession.query(ReputationReason).filter(and_(ReputationReason.reputation_uid == db_reason.uid,
                                                                                    ReputationReason.reputator_uid == db_user.uid)).first()
        if db_already_farmed:
            return False

    new_rep = ReputationHistory(reputator=db_user.uid, reputation=db_reason.uid)
    DBDiscussionSession.add(new_rep)
    DBDiscussionSession.flush()
    transaction.commit()
    return True
