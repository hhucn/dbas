"""
Provides helping function for getting some opinions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, ClickedArgument, ClickedStatement, Premise, SeenArgument, SeenStatement, sql_timestamp_pretty_print
from dbas.helper.relation import get_rebuts_for_argument_uid, get_undercuts_for_argument_uid, get_undermines_for_argument_uid, get_supports_for_argument_uid
from dbas.lib import get_text_for_statement_uid, get_text_for_argument_uid,\
    get_text_for_premisesgroup_uid, get_profile_picture
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_relation_text_dict_with_substitution, get_author_or_first_supporter_of_element
from dbas.strings.translator import Translator


def get_user_and_opinions_for_argument(argument_uids, nickname, lang, main_page, path):
    """
    Returns nested dictionary with all kinds of attacks for the argument as well as the users who are supporting
    these attacks.

    :param argument_uids: Argument.uid
    :param nickname: of the user
    :param lang: current language
    :param main_page: main_page
    :param path: path
    :return: { 'attack_type': { 'message': 'string', 'users': [{'nickname': 'string', 'avatar_url': 'url' 'vote_timestamp': 'string' ], ... }],...}
    """

    logger('OpinionHandler', 'get_user_and_opinions_for_argument', 'Arguments ' + str(argument_uids) + ', nickname ' + str(nickname))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_user_uid = db_user.uid if db_user else 0

    # preparation
    all_users = []
    _t = Translator(lang)
    try:
        db_user_argument = DBDiscussionSession.query(Argument).get(argument_uids[0])
    except TypeError:
        return None

    # sanity check
    if not db_user_argument:
        ret_dict = dict()
        ret_dict['message'] = _t.get(_.internalError) + '.'
        ret_dict['users'] = all_users
        ret_dict['opinions'] = ret_dict
        ret_dict['title'] = _t.get(_.internalError)
        return ret_dict

    title = _t.get(_.attitudesOfOpinions)

    # getting uids of all reactions
    arg_uids_for_reactions = [
        get_undermines_for_argument_uid(argument_uids[0]),
        get_supports_for_argument_uid(argument_uids[0]),
        get_undercuts_for_argument_uid(argument_uids[0]),
        get_rebuts_for_argument_uid(argument_uids[0])
    ]

    # get gender of counter user
    db_user = get_author_or_first_supporter_of_element(argument_uids[1], db_user_uid, True)
    gender = db_user.gender if db_user else 'n'

    if '/d' in path.split('?')[0]:
        relation_text = get_relation_text_dict_with_substitution(lang, False, False, False, is_dont_know=True, gender=gender)
    else:
        relation_text = get_relation_text_dict_with_substitution(lang, False, True, db_user_argument.is_supportive, gender=gender)

    # getting votes for every reaction
    ret_list = __get_clicks_for_reactions(arg_uids_for_reactions, relation_text, db_user_uid, _t, main_page)

    return {'opinions': ret_list, 'title': title[0:1].upper() + title[1:]}


def __get_clicks_for_reactions(arg_uids_for_reactions, relation_text, db_user_uid, _t, main_page):
    """
    Returns all clicks for the current reaction

    :param arg_uids_for_reactions: [[Undermines.uid, Supports.uid, Undercuts.uid, Rebuts.uid]
    :param relation_text: String
    :param db_user_uid: User.uid
    :param _t: Translator
    :param main_page: Host URL
    :return: List of dict()
    """
    # getting the text of all reactions
    relation = ['undermine', 'support', 'undercut', 'rebut']

    ret_list = []
    user_query = DBDiscussionSession.query(User)
    db_user = DBDiscussionSession.query(User).get(db_user_uid)
    if db_user:
        if db_user.gender == 'm':
            msg = _t.get(_.voteCountTextMayBeFirst) + '.'
        elif db_user.gender == 'f':
            msg = _t.get(_.voteCountTextMayBeFirstF) + '.'
        else:
            msg = _t.get(_.voteCountTextMayBeFirst) + '.'
    else:
        msg = _t.get(_.voteCountTextMayBeFirst) + '.'

    for rel in relation:
        all_users       = []
        message         = ''
        seen_by         = 0

        if not arg_uids_for_reactions[relation.index(rel)]:
            ret_list.append({'users': [],
                             'message': msg,
                             'text': relation_text[rel + '_text'],
                             'seen_by': 0})
            continue

        for uid in arg_uids_for_reactions[relation.index(rel)]:
            db_votes = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == uid['id'],
                                                                              ClickedArgument.is_up_vote == True,
                                                                              ClickedArgument.is_valid == True,
                                                                              ClickedArgument.author_uid != db_user_uid)).all()

            for vote in db_votes:
                voted_user = user_query.get(vote.author_uid)
                users_dict = create_users_dict(voted_user, vote.timestamp, main_page, _t.get_lang())
                all_users.append(users_dict)

            if len(db_votes) == 0:
                message = msg
            elif len(db_votes) == 1:
                message = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextOneMore) + '.'
            else:
                message = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextMore) + '.'

            db_seen_by = DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=int(uid['id'])).all()
            seen_by += len(db_seen_by) if db_seen_by else 0

        ret_list.append({'users': all_users,
                         'message': message,
                         'text': relation_text[rel + '_text'],
                         'seen_by': seen_by})
    return ret_list


def get_user_with_same_opinion_for_statements(statement_uids, is_supportive, nickname, lang, main_page):
    """
    Returns nested dictionary with all kinds of information about the votes of the statements.

    :param statement_uids: Statement.uid
    :param is_supportive: Boolean
    :param nickname: of the user
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    logger('OpinionHandler', 'get_user_with_same_opinion_for_statements', 'Statement ' + str(statement_uids))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_user_uid = db_user.uid if db_user else 0

    opinions = []
    _t = Translator(lang)
    title = _t.get(_.relativePopularityOfStatements)

    for uid in statement_uids:
        statement_dict = __get_opinions_for_uid(uid, is_supportive, db_user_uid, lang, _t, main_page)
        opinions.append(statement_dict)

    return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}


def __get_opinions_for_uid(uid, is_supportive, db_user_uid, lang, _t, main_page):
    none_dict = {'uid': None,  'text': None,  'message': None,  'users': None,  'seen_by': None}
    statement_dict = dict()
    all_users = []
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    if not db_statement:
        statement_dict.update(none_dict)

    statement_dict['uid'] = str(uid)
    text = get_text_for_statement_uid(uid)
    try:
        if db_statement.is_startpoint and lang == 'de':
            text = _t.get(_.statementIsAbout) + ' ' + text
        statement_dict['text'] = text
    except TypeError:
        statement_dict.update(none_dict)

    is_supportive = (True if str(is_supportive) == 'True' else False) if is_supportive is not None else False
    db_votes = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == uid,
                                                                       ClickedStatement.is_up_vote == is_supportive,
                                                                       ClickedStatement.is_valid == True,
                                                                       ClickedStatement.author_uid != db_user_uid)).all()

    for vote in db_votes:
        voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
        users_dict = create_users_dict(voted_user, vote.timestamp, main_page, lang)
        all_users.append(users_dict)
    statement_dict['users'] = all_users
    statement_dict['message'] = __get_genered_text_for_clickcount(len(db_votes), db_user_uid, _t)

    db_seen_by = DBDiscussionSession.query(SeenStatement).filter_by(statement_uid=int(uid)).all()
    statement_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0
    return statement_dict


def __get_genered_text_for_clickcount(len_db_votes, db_user_uid, _t):
    """
    Generate text for current click counter

    :param len_db_votes: int
    :param db_user_uid: User.uid
    :param _t: Translator
    :return: String
    """
    if len_db_votes == 0:
        db_user = DBDiscussionSession.query(User).get(db_user_uid)
        if db_user:
            if db_user.gender == 'm':
                msg = _t.get(_.voteCountTextMayBeFirst)
            elif db_user.gender == 'f':
                msg = _t.get(_.voteCountTextMayBeFirstF)
            else:
                msg = _t.get(_.voteCountTextMayBeFirst)
        else:
            msg = _t.get(_.voteCountTextMayBeFirst)
        return msg + '.'
    elif len_db_votes == 1:
        return str(len_db_votes) + ' ' + _t.get(_.voteCountTextOneMore) + '.'
    else:
        return str(len_db_votes) + ' ' + _t.get(_.voteCountTextMore) + '.'


def get_user_with_same_opinion_for_premisegroups(argument_uids, nickname, lang, main_page):
    """
    Returns nested dictionary with all kinds of information about the votes of the premisegroups.

    :param argument_uids: Argument.uid
    :param nickname: of the user
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'Arguments ' + str(argument_uids))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_user_uid = db_user.uid if db_user else 0

    opinions = []
    _t = Translator(lang)
    title = _t.get(_.relativePopularityOfStatements)

    for uid in argument_uids:
        logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'argument ' + str(uid))
        statement_dict = dict()
        all_users = []
        db_argument = DBDiscussionSession.query(Argument).get(uid)
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
        if not db_premises:
            statement_dict['uid']       = None
            statement_dict['text']      = None
            statement_dict['message']   = None
            statement_dict['users']     = None
            statement_dict['seen_by']   = None

        statement_dict['uid'] = str(uid)
        text, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        statement_dict['text'] = '... {} {}'.format(_t.get(_.because).lower(), text)

        db_votes = []
        for premise in db_premises:
            logger('OpinionHandler', 'get_user_with_same_opinion_for_premisegroups', 'group ' + str(uid) +
                   ' premises statement ' + str(premise.statement_uid))
            db_votes += DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == premise.statement_uid,
                                                                                ClickedStatement.is_up_vote == True,
                                                                                ClickedStatement.is_valid == True,
                                                                                ClickedStatement.author_uid != db_user_uid)).all()

        for vote in db_votes:
            voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
            users_dict = create_users_dict(voted_user, vote.timestamp, main_page, lang)
            all_users.append(users_dict)
        statement_dict['users'] = all_users
        statement_dict['message'] = __get_genered_text_for_clickcount(len(db_votes), db_user_uid, _t)

        db_seen_by = DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=int(uid)).all()
        statement_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0

        opinions.append(statement_dict)

    return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}


def get_user_with_same_opinion_for_argument(argument_uid, nickname, lang, main_page):
    """
    Returns nested dictionary with all kinds of information about the votes of the argument.

    :param argument_uid: Argument.uid
    :param nickname: of the user
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    try:
        logger('OpinionHandler', 'get_user_with_same_opinion_for_argument', 'Argument ' + str(argument_uid) + ' ' + get_text_for_argument_uid(argument_uid, 'de'))
    except TypeError:
        return None
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_user_uid = db_user.uid if db_user else 0

    opinions = dict()
    all_users = []
    _t = Translator(lang)
    text = get_text_for_argument_uid(argument_uid, lang)
    title = _t.get(_.reactionFor) + ': ' + text[0:1].upper() + text[1:]

    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)
    if not db_argument:
        opinions['uid']       = None
        opinions['text']      = None
        opinions['message']   = None
        opinions['users']     = None
        opinions['seen_by']   = None

    opinions['uid'] = str(argument_uid)
    text = get_text_for_argument_uid(argument_uid, lang)
    opinions['text'] = text[0:1].upper() + text[1:]

    db_votes = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == argument_uid,
                                                                      ClickedArgument.is_up_vote == True,
                                                                      ClickedArgument.is_valid == True,
                                                                      ClickedArgument.author_uid != db_user_uid)).all()

    for vote in db_votes:
        voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
        users_dict = create_users_dict(voted_user, vote.timestamp, main_page, lang)
        all_users.append(users_dict)
    opinions['users'] = all_users
    opinions['message'] = __get_genered_text_for_clickcount(len(db_votes), db_user_uid, _t)

    db_seen_by = DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=int(argument_uid)).all()
    opinions['seen_by'] = len(db_seen_by) if db_seen_by else 0

    return {'opinions': opinions, 'title': title[0:1].upper() + title[1:]}


def get_user_with_opinions_for_attitude(statement_uid, nickname, lang, main_page):
    """
    Returns dictionary with agree- and disagree-votes

    :param statement_uid: Statement.uid
    :param nickname: of the user
    :param lang: language
    :param main_page: url
    :return:
    """

    logger('OpinionHandler', 'get_user_with_opinions_for_attitude', 'Statement ' + str(statement_uid))
    db_statement = DBDiscussionSession.query(Statement).get(statement_uid) if statement_uid else None
    _t = Translator(lang)
    title = _t.get(_.agreeVsDisagree)

    if not db_statement:
        empty_dict = {
            'users': [],
            'text': None,
            'message': ''
        }
        return {
            'text': None,
            'agree': empty_dict,
            'disagree': empty_dict,
            'title': title
        }
    title += ' ' + get_text_for_statement_uid(statement_uid)

    ret_dict = dict()
    text = get_text_for_statement_uid(statement_uid)
    ret_dict['text'] = text[0:1].upper() + text[1:]
    ret_dict['agree'] = None
    ret_dict['disagree'] = None
    ret_dict['title'] = title

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_user_uid = db_user.uid if db_user else 0
    agree_dict    = __collect_pro_clicks(statement_uid, db_user_uid, main_page, _t)
    disagree_dict = __collect_con_clicks(statement_uid, db_user_uid, main_page, _t)
    ret_dict['agree'] = agree_dict
    ret_dict['disagree'] = disagree_dict

    db_seen_by = DBDiscussionSession.query(SeenStatement).filter_by(statement_uid=int(statement_uid)).all()
    ret_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0

    return ret_dict


def __collect_pro_clicks(statement_uid, user_uid, main_page, _t):
    """
    List of all positive interest for the given statements

    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param main_page: Host URL
    :param _t: Translator
    :return: dict()
    """

    db_pro_votes = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == statement_uid,
                                                                           ClickedStatement.is_up_vote == True,
                                                                           ClickedStatement.is_valid == True,
                                                                           ClickedStatement.author_uid != user_uid)).all()
    pro_array = []
    agree_dict = {}
    for vote in db_pro_votes:
        voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
        users_dict = create_users_dict(voted_user, vote.timestamp, main_page, _t.get_lang())
        pro_array.append(users_dict)
    agree_dict['users'] = pro_array
    agree_dict['text'] = _t.get(_.iAgreeWith)
    if len(db_pro_votes) == 0:
        agree_dict['message'] = _t.get(_.agreeToThis0) + '.'
    else:
        agree_dict['message'] = str(len(db_pro_votes)) + ' '
        agree_dict['message'] += _t.get(_.agreeToThis1) if len(db_pro_votes) == 1 else _t.get(_.agreeToThis2)
        agree_dict['message'] += '.'
    return agree_dict


def __collect_con_clicks(statement_uid, user_uid, main_page, _t):
    """
    List of all negative interest for the given statements

    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param main_page: Host URL
    :param _t: Translator
    :return: dict()
    """
    db_con_votes = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == statement_uid,
                                                                           ClickedStatement.is_up_vote == False,
                                                                           ClickedStatement.is_valid == True,
                                                                           ClickedStatement.author_uid != user_uid)).all()

    con_array = []
    disagree_dict = {}
    for vote in db_con_votes:
        voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
        users_dict = create_users_dict(voted_user, vote.timestamp, main_page, _t.get_lang())
        con_array.append(users_dict)
    disagree_dict['users'] = con_array
    disagree_dict['text'] = _t.get(_.iDisagreeWith)
    if len(db_con_votes) == 0:
        disagree_dict['message'] = _t.get(_.disagreeToThis0) + '.'
    else:
        disagree_dict['message'] = str(len(db_con_votes)) + ' '
        disagree_dict['message'] += _t.get(_.disagreeToThis1) if len(db_con_votes) == 1 else _t.get(_.disagreeToThis2)
        disagree_dict['message'] += '.'
    return disagree_dict


def create_users_dict(db_user, timestamp, main_page, lang):
    """
    Creates dictionary with nickname, url and timestamp

    :param db_user: User
    :param timestamp: SQL Timestamp
    :param main_page: url
    :param lang: language
    :return: dict()
    """
    tmp = db_user.get_global_nickname()
    return {'nickname': tmp,
            'public_profile_url': main_page + '/user/' + str(db_user.uid),
            'avatar_url': get_profile_picture(db_user),
            'vote_timestamp': sql_timestamp_pretty_print(timestamp, lang)}


def get_infos_about_argument(uid, main_page, nickname, _t):
    """
    Returns several infos about the argument.

    :param uid: Argument.uid
    :param main_page: url
    :param nickname: current nickname
    :param _t: Translator
    :return: dict()
    """
    return_dict = dict()
    db_votes = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == uid,
                                                                      ClickedArgument.is_valid == True,
                                                                      ClickedStatement.is_up_vote == True)).all()
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        return return_dict

    db_author = DBDiscussionSession.query(User).get(db_argument.author_uid)
    return_dict['vote_count'] = str(len(db_votes))
    return_dict['author'] = db_author.get_global_nickname()
    return_dict['author_url'] = main_page + '/user/' + str(db_author.uid)
    return_dict['gravatar'] = get_profile_picture(db_author)
    return_dict['timestamp'] = sql_timestamp_pretty_print(db_argument.timestamp, db_argument.lang)
    text = get_text_for_argument_uid(uid)
    return_dict['text'] = text[0:1].upper() + text[1:] + '.'

    supporters = []
    gravatars = dict()
    public_page = dict()
    for vote in db_votes:
        db_user = DBDiscussionSession.query(User).get(vote.author_uid)
        name = db_user.get_global_nickname()
        if db_user.nickname == nickname:
            name += ' (' + _t.get(_.itsYou) + ')'
        supporters.append(name)
        gravatars[name] = get_profile_picture(db_user)
        public_page[name] = main_page + '/user/' + str(db_user.uid)

    return_dict['supporter'] = supporters
    return_dict['gravatars'] = gravatars
    return_dict['public_page'] = public_page

    return return_dict
