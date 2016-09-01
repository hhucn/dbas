"""
Provides helping function for the managing reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReputationHistory, ReputationReason
from dbas.lib import sql_timestamp_pretty_print, is_user_author

reputation_borders = {'deletes': 15,
                      'optimizations': 15,
                      'history': 100}


def get_reputation_history(nickname, translator):
    """

    :param nickname:
    :param translator:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return dict()

    ret_dict = dict()
    count, all_rights = get_reputation_of(nickname)
    ret_dict['count'] = count
    ret_dict['all_rights'] = all_rights

    db_reputation = DBDiscussionSession.query(ReputationHistory) \
        .filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .all()

    rep_list = list()
    for rep in db_reputation:
        date = sql_timestamp_pretty_print(rep.timestamp, translator.get_lang(), humanize=False)
        points_data = '<span class="success-description points">+' if rep.reputations.points > 0 else '<span class="error-description points">'
        points_data += str(rep.reputations.points) + '</span'
        points = rep.reputations.points
        action = translator.get(rep.reputations.reason)
        rep_list.append({'date': date, 'points_data': points_data, 'action': action, 'points': points})

    ret_dict['history'] = rep_list

    return ret_dict


def get_privilege_list(translator):
    """

    :param translator:
    :return:
    """

    reputations = list()
    # reputations.append({'points': 1000, 'icon': 'fa fa-arrow-down', 'text': 'Some text'})
    # reputations.append({'points': 750, 'icon': 'fa fa-arrow-up', 'text': 'Some text'})
    # reputations.append({'points': 500, 'icon': 'fa fa-hand-o-up', 'text': 'Some text'})
    # reputations.append({'points': 250, 'icon': 'fa fa-hand-o-down', 'text': 'Review a statement with many contra-arguments'})
    # reputations.append({'points': 200, 'icon': 'fa fa-times', 'text': 'Decide, whether it is spam or not'})
    # reputations.append({'points': 100, 'icon': 'fa fa-trash', 'text': 'Decision about statement, which should be deleted'})
    reputations.append({'points': reputation_borders['history'], 'icon': 'fa fa-history', 'text': translator.get(translator.priv_history_queue)})
    reputations.append({'points': reputation_borders['deletes'], 'icon': 'fa fa-pencil-square-o', 'text': translator.get(translator.priv_access_opti_queue)})
    reputations.append({'points': reputation_borders['optimizations'], 'icon': 'fa fa-flag', 'text': translator.get(translator.priv_access_del_queue)})
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
