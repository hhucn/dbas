"""
Provides helping function for the managing reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.lib import sql_timestamp_pretty_print, is_user_author

reputation_borders = {'deletes': 30,
                      'optimizations': 30,
                      'history': 100}
reputation_icons = {'deletes': 'fa fa-pencil-square-o',
                    'optimizations': 'fa fa-flag',
                    'history': 'fa fa-history'}


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
