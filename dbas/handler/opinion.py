"""
Provides helping function for getting some opinions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import logging
from typing import List

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, ClickedArgument, ClickedStatement, Premise, \
    SeenArgument, SeenStatement, sql_timestamp_pretty_print
from dbas.helper.relation import get_rebuts_for_argument_uid, get_undercuts_for_argument_uid, \
    get_undermines_for_argument_uid, get_supports_for_argument_uid
from dbas.lib import get_text_for_argument_uid, get_profile_picture, Relations
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital
from dbas.strings.text_generator import get_relation_text_dict_with_substitution, \
    get_author_or_first_supporter_of_element
from dbas.strings.translator import Translator


def get_user_and_opinions_for_argument(argument_uid, db_user, lang, main_page, path):
    """
    Returns nested dictionary with all kinds of attacks for the argument as well as the users who are supporting
    these attacks.

    :param argument_uid: Argument.uid
    :param db_user: User
    :param lang: current language
    :param main_page: main_page
    :param path: path
    :return: { 'attack_type': { 'message': 'string', 'users': [{'nickname': 'string', 'avatar_url': 'url'
               'vote_timestamp': 'string' ], ... }],...}
    """

    log = logging.getLogger(__name__)
    log.debug("Argument %s, nickname %s", argument_uid, db_user.nickname)

    # preparation
    _t = Translator(lang)
    title = _t.get(_.attitudesOfOpinions)

    # getting uids of all reactions
    arg_uids_for_reactions = [
        get_undermines_for_argument_uid(argument_uid),
        get_supports_for_argument_uid(argument_uid),
        get_undercuts_for_argument_uid(argument_uid),
        get_rebuts_for_argument_uid(argument_uid)
    ]

    # get gender of counter use
    db_supporter = get_author_or_first_supporter_of_element(argument_uid, db_user.uid, True)
    gender = 'n'
    if db_supporter:
        gender = db_supporter.gender

    if '/d' in path.split('?')[0]:
        relation_text = get_relation_text_dict_with_substitution(lang, False, is_dont_know=True, gender=gender)
    else:
        relation_text = get_relation_text_dict_with_substitution(lang, True, gender=gender)

    # getting votes for every reaction
    ret_list = __get_clicks_for_reactions(arg_uids_for_reactions, relation_text, db_supporter, _t, main_page)

    return {'opinions': ret_list, 'title': start_with_capital(title)}


def __get_clicks_for_reactions(arg_uids_for_reactions, relation_text, db_user, _t, main_page):
    """
    Returns all clicks for the current reaction

    :param arg_uids_for_reactions: [[Undermines.uid, Supports.uid, Undercuts.uid, Rebuts.uid]
    :param relation_text: String
    :param db_user: User
    :param _t: Translator
    :param main_page: Host URL
    :return: List of dict()
    """
    # getting the text of all reactions
    relations = [relation.value for relation in Relations]

    ret_list = []

    for relation in relations:
        d = __build_reaction_dict_by_relation(relation, relation, relation_text, arg_uids_for_reactions, db_user,
                                              main_page, _t)
        ret_list.append(d)
    return ret_list


def __build_reaction_dict_by_relation(relations, current_relation, relation_text, arg_uids_for_reactions,
                                      db_user, main_page, _t):
    all_users = []
    message = ''
    seen_by = 0

    if db_user and db_user.gender == 'm':
        msg = _t.get(_.voteCountTextMayBeFirst) + '.'
    else:
        msg = _t.get(_.voteCountTextMayBeFirstF) + '.'

    if not arg_uids_for_reactions[relations.index(current_relation)]:
        return {
            'users': [],
            'message': msg,
            'text': relation_text[current_relation + '_text'],
            'seen_by': 0
        }

    for uid in arg_uids_for_reactions[relations.index(current_relation)]:
        db_user_uid = db_user.uid if db_user else 0
        db_votes = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.argument_uid == uid['id'],
                                                                     ClickedArgument.is_up_vote == True,
                                                                     ClickedArgument.is_valid == True,
                                                                     ClickedArgument.author_uid != db_user_uid).all()

        for vote in db_votes:
            voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
            users_dict = create_users_dict(voted_user, vote.timestamp, main_page, _t.get_lang())
            all_users.append(users_dict)

        if len(db_votes) == 0:
            message = msg
        elif len(db_votes) == 1:
            message = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextOneMore) + '.'
        else:
            message = str(len(db_votes)) + ' ' + _t.get(_.voteCountTextMore) + '.'

        db_seen_by = DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=int(uid['id'])).all()
        if db_seen_by:
            seen_by += len(db_seen_by)

    return {
        'users': all_users,
        'message': message,
        'text': relation_text[current_relation + '_text'],
        'seen_by': seen_by
    }


def get_user_with_same_opinion_for_statements(statement_uids, is_supportive, db_user, lang, main_page):
    """
    Returns nested dictionary with all kinds of information about the votes of the statements.

    :param statement_uids: Statement.uids
    :param is_supportive: Boolean
    :param db_user: User
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    log = logging.getLogger(__name__)
    log.debug("Statement %s (%s)", statement_uids, is_supportive)

    opinions = []
    _t = Translator(lang)
    title = _t.get(_.relativePopularityOfStatements)

    for statement_uid in statement_uids:
        statement_dict = __get_opinions_for_uid(statement_uid, is_supportive, db_user, lang, _t, main_page)
        opinions.append(statement_dict)

    return {'opinions': opinions, 'title': start_with_capital(title)}


def __get_opinions_for_uid(uid, is_supportive, db_user, lang, _t, main_page):
    none_dict = {'uid': None, 'text': None, 'message': None, 'users': None, 'seen_by': None}
    statement_dict = dict()
    all_users = []
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    if not db_statement:
        statement_dict.update(none_dict)

    statement_dict['uid'] = str(uid)
    text = db_statement.get_text()
    try:
        if db_statement.is_position and lang == 'de':
            text = _t.get(_.statementIsAbout) + ' ' + text
        statement_dict['text'] = text
    except TypeError:
        statement_dict.update(none_dict)

    is_supportive = (True if str(is_supportive) == 'True' else False) if is_supportive is not None else False
    db_votes = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.statement_uid == uid,
                                                                  ClickedStatement.is_up_vote == is_supportive,
                                                                  ClickedStatement.is_valid == True,
                                                                  ClickedStatement.author_uid != db_user.uid).all()

    for vote in db_votes:
        voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
        users_dict = create_users_dict(voted_user, vote.timestamp, main_page, lang)
        all_users.append(users_dict)
    statement_dict['users'] = all_users
    statement_dict['message'] = __get_text_for_clickcount(len(db_votes), db_user.uid, _t)

    db_seen_by = DBDiscussionSession.query(SeenStatement).filter_by(statement_uid=int(uid)).all()
    statement_dict['seen_by'] = len(db_seen_by) if db_seen_by else 0
    return statement_dict


def __get_text_for_clickcount(len_db_votes, db_user_uid, _t):
    """
    Generate text for current click counter

    :param len_db_votes: int
    :param db_user_uid: User.uid
    :param _t: Translator
    :return: String
    """
    if len_db_votes == 0:
        db_user = DBDiscussionSession.query(User).get(db_user_uid)
        if db_user and db_user.gender == 'f':
            msg = _.voteCountTextMayBeFirstF
        else:
            msg = _.voteCountTextMayBeFirst
        return _t.get(msg) + '.'
    elif len_db_votes == 1:
        return str(len_db_votes) + ' ' + _t.get(_.voteCountTextOneMore) + '.'
    else:
        return str(len_db_votes) + ' ' + _t.get(_.voteCountTextMore) + '.'


def get_user_with_same_opinion_for_premisegroups_of_args(argument_uids, db_user, lang, main_page):
    """
    Returns nested dictionary with all kinds of information about the votes of the premisegroups.

    :param argument_uids: [Argument.uid]
    :param db_user: User
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    log = logging.getLogger(__name__)
    log.debug("Arguments %s", argument_uids)

    opinions = []
    _t = Translator(lang)
    title = _t.get(_.relativePopularityOfStatements)
    for arg_uid in argument_uids:
        db_argument = DBDiscussionSession.query(Argument).get(arg_uid)
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).all()
        if db_premises:
            opinions.append(
                get_user_with_same_opinion_for_premisegroups_of_arg(db_argument, db_premises, db_user, lang, main_page))

    return {'opinions': opinions, 'title': start_with_capital(title)}


def get_user_with_same_opinion_for_premisegroups_of_arg(db_argument: Argument, db_premises: List[Premise],
                                                        db_user: User, lang: str, main_page: str):
    """
    Returns nested dictionary with all kinds of information about the votes of the premisegroups.

    :param db_argument:
    :param db_premises:
    :param db_user: User
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    _t = Translator(lang)
    all_users = []
    text = db_argument.get_premisegroup_text()

    premise_statement_uids = [p.statement_uid for p in db_premises]
    db_clicks = DBDiscussionSession.query(ClickedStatement).filter(
        ClickedStatement.statement_uid.in_(premise_statement_uids),
        ClickedStatement.is_up_vote == True,
        ClickedStatement.is_valid == True,
        ClickedStatement.author_uid != db_user.uid).all()
    db_seens = DBDiscussionSession.query(SeenStatement).filter(
        SeenStatement.statement_uid.in_(premise_statement_uids)).all()

    for click in db_clicks:
        click_user = DBDiscussionSession.query(User).get(click.author_uid)
        users_dict = create_users_dict(click_user, click.timestamp, main_page, lang)
        all_users.append(users_dict)

    return {
        'uid': str(db_argument.uid),
        'text': '... {} {}'.format(_t.get(_.because).lower(), text),
        'users': all_users,
        'message': __get_text_for_clickcount(len(db_clicks), db_user.uid, _t),
        'seen_by': len(db_seens)
    }


def get_user_with_same_opinion_for_argument(argument_uid, db_user, lang, main_page):
    """
    Returns nested dictionary with all kinds of information about the votes of the argument.

    :param argument_uid: Argument.uid
    :param db_user: User
    :param lang: language
    :param main_page: url
    :return: {'users':[{nickname1.avatar_url, nickname1.vote_timestamp}*]}
    """
    try:
        text = get_text_for_argument_uid(argument_uid, 'de')
        log = logging.getLogger(__name__)
        log.debug("Argument %s: %s", argument_uid, text)
        if not text:
            return {'uid': None, 'text': None, 'message': None, 'users': None, 'seen_by': None}
    except TypeError:
        return {'uid': None, 'text': None, 'message': None, 'users': None, 'seen_by': None}

    opinions = dict()
    all_users = []
    _t = Translator(lang)
    text = get_text_for_argument_uid(argument_uid, lang)
    title = _t.get(_.reactionFor) + ': ' + start_with_capital(text)

    db_argument = DBDiscussionSession.query(Argument).get(argument_uid)
    if not db_argument:
        opinions = {'uid': None, 'text': None, 'message': None, 'users': None, 'seen_by': None}

    opinions['uid'] = str(argument_uid)
    text = get_text_for_argument_uid(argument_uid, lang)
    opinions['text'] = start_with_capital(text)

    db_clicks = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.argument_uid == argument_uid,
                                                                  ClickedArgument.is_up_vote == True,
                                                                  ClickedArgument.is_valid == True,
                                                                  ClickedArgument.author_uid != db_user.uid).all()

    for vote in db_clicks:
        voted_user = DBDiscussionSession.query(User).get(vote.author_uid)
        users_dict = create_users_dict(voted_user, vote.timestamp, main_page, lang)
        all_users.append(users_dict)
    opinions['users'] = all_users
    opinions['message'] = __get_text_for_clickcount(len(db_clicks), db_user.uid, _t)

    db_seen_by = DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=int(argument_uid)).all()
    opinions['seen_by'] = len(db_seen_by) if db_seen_by else 0

    return {'opinions': opinions, 'title': start_with_capital(title)}


def get_user_with_opinions_for_attitude(statement_uid, db_user, lang, main_page):
    """
    Returns dictionary with agree- and disagree-votes

    :param statement_uid: Statement.uid
    :param db_user: User
    :param lang: language
    :param main_page: url
    :return:
    """

    log = logging.getLogger(__name__)
    log.debug("Statement %s", statement_uid)
    db_statement = DBDiscussionSession.query(Statement).get(statement_uid) if statement_uid else None
    _t = Translator(lang)
    title = _t.get(_.agreeVsDisagree)

    if not db_statement:
        empty_dict = {'users': [], 'text': None, 'message': ''}
        return {'text': None, 'agree': empty_dict, 'disagree': empty_dict, 'title': title}

    text = db_statement.get_text()
    title += ' ' + text

    ret_dict = dict()
    ret_dict['text'] = start_with_capital(text)
    ret_dict['agree'] = None
    ret_dict['disagree'] = None
    ret_dict['title'] = title

    agree_dict = __collect_pro_clicks(statement_uid, db_user.uid, main_page, _t)
    disagree_dict = __collect_con_clicks(statement_uid, db_user.uid, main_page, _t)
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

    db_pro_votes = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.statement_uid == statement_uid,
                                                                      ClickedStatement.is_up_vote == True,
                                                                      ClickedStatement.is_valid == True,
                                                                      ClickedStatement.author_uid != user_uid).all()
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
    db_con_votes = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.statement_uid == statement_uid,
                                                                      ClickedStatement.is_up_vote == False,
                                                                      ClickedStatement.is_valid == True,
                                                                      ClickedStatement.author_uid != user_uid).all()

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
    tmp = db_user.global_nickname
    return {'nickname': tmp,
            'public_profile_url': main_page + '/user/' + str(db_user.uid),
            'avatar_url': get_profile_picture(db_user),
            'vote_timestamp': sql_timestamp_pretty_print(timestamp, lang)}
