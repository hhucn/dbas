"""
Provides helping function for creating the history as bubbles.

.. codeauthor: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, History, Settings
from dbas.input_validator import Validator
from dbas.lib import create_speechbubble_dict
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion, sql_timestamp_pretty_print
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import TextGenerator
from dbas.strings.translator import Translator


def save_issue_uid(transaction, issue_uid, nickname):
    """

    :param transaction:
    :param issue_uid:
    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return False

    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
    if not db_settings:
        return False

    db_settings.set_last_topic_uid(issue_uid)
    transaction.commit()


def get_saved_issue(nickname):
    """

    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return 0

    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
    if not db_settings:
        return 0

    return db_settings.last_topic_uid


def get_splitted_history(history):
    """
    Splits history by specific keyword and removes leading '/'

    :param history: String
    :return: [String]
    """
    history = history.split('-')
    tmp = []
    for h in history:
        tmp.append(h[1:] if h[0:1] == '/' else h)

    return tmp


def create_bubbles_from_history(history, nickname='', lang='', application_url='', slug=''):
    """
    Creates the bubbles for every history step

    :param history: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param application_url: String
    :param slug: String
    :return: Array
    """
    if len(history) == 0:
        return []

    logger('history_helper', 'create_bubbles_from_history', 'nickname: ' + str(nickname) + ', history: ' + history)
    splitted_history = get_splitted_history(history)

    bubble_array = []
    consumed_history = ''

    nickname = nickname if nickname else 'anonymous'

    for index, step in enumerate(splitted_history):
        url = application_url + '/discuss/' + slug + '/' + step
        if len(consumed_history) != 0:
            url += '?history=' + consumed_history
        consumed_history += step if len(consumed_history) == 0 else '-' + step

        if 'justify/' in step:
            logger('history_helper', 'create_bubbles_from_history', str(index) + ': justify case -> ' + step)
            steps    = step.split('/')
            mode     = steps[2]
            relation = steps[3] if len(steps) > 3 else ''

            if [c for c in ('t', 'f') if c in mode] and relation == '':
                bubbles = __justify_statement_step(step, nickname, lang, url)
                if bubbles:
                    bubble_array += bubbles

        elif 'reaction/' in step:
            logger('history_helper', 'create_bubbles_from_history', str(index) + ': reaction case -> ' + step)
            bubbles = __reaction_step(step, nickname, lang, splitted_history, url)
            if bubbles:
                bubble_array += bubbles

        # elif 'attitude/' in step:
        #    logger('history_helper', 'create_bubbles_from_history', str(index) + ': attitude case -> ' + step)
        #    bubbles = __attitude_step(step, nickname, lang, url)
        #    if bubbles:
        #        bubble_array += bubbles

        else:
            logger('history_helper', 'create_bubbles_from_history', str(index) + ': unused case -> ' + step)

    return bubble_array


def __justify_statement_step(step, nickname, lang, url):
    """
    Creates bubbles for the justify-keyword for an statement.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    logger('history_helper', '__justify_statement_step', 'def')
    steps   = step.split('/')
    uid     = int(steps[1])
    #  slug    = ''
    is_supportive = steps[2] == 't' or steps[2] == 'd'  # supportive = t(rue) or d(ont know) mode

    _tn         = Translator(lang)
    #  url     = UrlManager(application_url, slug).get_slug_url(False)
    if lang == 'de':
        intro = _tn.get(_.youAgreeWith if is_supportive else _tn.youDisagreeWith) + ' '
    else:
        intro = '' if is_supportive else _tn.get(_.youDisagreeWith) + ': '
    text    = get_text_for_statement_uid(uid)
    if lang != 'de':
        text    = text[0:1].upper() + text[1:]

    msg = intro + '<' + TextGenerator.tag_type + '>' + text + '</' + TextGenerator.tag_type + '>'
    bubbsle_user = create_speechbubble_dict(is_user=True, message=msg, omit_url=False, statement_uid=uid,
                                            is_supportive=is_supportive, nickname=nickname, lang=lang, url=url)
    return [bubbsle_user]


def __attitude_step(step, nickname, lang, url):
    """
    Creates bubbles for the attitude-keyword for an statement.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    logger('history_helper', '__attitude_step', 'def')
    steps   = step.split('/')
    uid     = int(steps[1])
    text    = get_text_for_statement_uid(uid)
    if lang != 'de':
        text    = text[0:1].upper() + text[1:]
    bubble = create_speechbubble_dict(is_user=True, message=text, omit_url=False, statement_uid=uid, nickname=nickname,
                                      lang=lang, url=url)

    return [bubble]


def __dont_know_step(step, nickname, lang, url):
    """
    Creates bubbles for the dont-know-reaction for a statement.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    steps    = step.split('/')
    uid      = int(steps[1])

    _tn      = Translator(lang)
    text     = get_text_for_argument_uid(uid)
    text = text.replace(_tn.get(_.because).lower(), '</' + TextGenerator.tag_type + '>' + _tn.get(
        _.because).lower() + '<' + TextGenerator.tag_type + '>')
    sys_text = _tn.get(_.otherParticipantsThinkThat) + ' <' + TextGenerator.tag_type + '>' + text[0:1].lower() + text[
                                                                                                                 1:] + '</' + TextGenerator.tag_type + '>. '
    return [create_speechbubble_dict(is_system=True, message=sys_text, nickname=nickname, lang=lang, url=url, is_supportive=True)]


def __reaction_step(step, nickname, lang, splitted_history, url):
    """
    Creates bubbles for the reaction-keyword.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param splitted_history: [String].uid
    :param url: String
    :return: [dict()]
    """
    logger('history_helper', '__reaction_step', 'def: ' + str(splitted_history))
    steps           = step.split('/')
    uid             = int(steps[1])
    additional_uid  = int(steps[3])
    attack          = steps[2]

    if not Validator.check_reaction(uid, additional_uid, attack, is_history=True):
        return None

    is_supportive   = DBDiscussionSession.query(Argument).filter_by(uid=uid).first().is_supportive
    last_relation   = splitted_history[-1].split('/')[2]

    user_changed_opinion = len(splitted_history) > 1 and '/undercut/' in splitted_history[-2]
    current_argument     = get_text_for_argument_uid(uid, user_changed_opinion=user_changed_opinion)
    db_argument          = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
    db_confrontation     = DBDiscussionSession.query(Argument).filter_by(uid=additional_uid).first()
    db_statement         = DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()

    premise, tmp         = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
    conclusion           = get_text_for_conclusion(db_argument)
    sys_conclusion       = get_text_for_conclusion(db_confrontation)
    confr, tmp           = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid)
    reply_for_argument   = not (db_statement and db_statement.is_startpoint)
    user_is_attacking    = not db_argument.is_supportive

    if lang != 'de':
        current_argument = current_argument[0:1].upper() + current_argument[1:]
    premise = premise[0:1].lower() + premise[1:]

    _tn = Translator(lang)
    user_text = (_tn.get(_.otherParticipantsConvincedYouThat) + ': ') if last_relation == 'support' else ''
    user_text += '<' + TextGenerator.tag_type + '>'
    user_text += current_argument if current_argument != '' else premise
    user_text += '</' + TextGenerator.tag_type + '>.'
    sys_text = TextGenerator(lang).get_text_for_confrontation(premise, conclusion, sys_conclusion, is_supportive,
                                                              attack, confr, reply_for_argument, user_is_attacking,
                                                              db_argument, db_confrontation, color_html=False)

    bubble_user = create_speechbubble_dict(is_user=True, message=user_text, omit_url=False,
                                           argument_uid=uid, is_supportive=is_supportive,
                                           nickname=nickname, lang=lang, url=url)
    if attack == 'end':
        bubble_syst  = create_speechbubble_dict(is_system=True, message=sys_text, omit_url=True,
                                                nickname=nickname, lang=lang)
    else:
        bubble_syst  = create_speechbubble_dict(is_system=True, uid='question-bubble-' + str(additional_uid),
                                                message=sys_text, omit_url=True, nickname=nickname, lang=lang)
    return [bubble_user, bubble_syst]


def save_history_in_cookie(request, path, history):
    """
    Saves history + new path in cookie

    :param request: request
    :param path: String
    :param history: String
    :return: none
    """
    if path.startswith('/discuss/'):
        path = path[len('/discuss/'):]
        path = path[path.index('/') if '/' in path else 0:]
        request.response.set_cookie('_HISTORY_', history + '-' + path)


def save_path_in_database(nickname, path, transaction):
    """
    Saves a path into the database

    :param nickname: User.nickname
    :param path: String
    :param transaction: Transaction
    :return: Boolean
    """

    if path.startswith('/discuss/'):
        path = path[len('/discuss/'):]
        path = path[path.index('/') if '/' in path else 0:]

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname if nickname else '').first()
    if not nickname or not db_user:
        return []

    DBDiscussionSession.add(History(author_uid=db_user.uid, path=path))
    DBDiscussionSession.flush()
    transaction.commit()


def get_history_from_database(nickname, lang):
    """
    Returns history from database

    :param nickname: User.nickname
    :param lang: ui_locales
    :return: [String]
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname if nickname else '').first()
    if not nickname or not db_user:
        return []

    db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()
    return_array = []
    for history in db_history:
        return_array.append({'path': history.path, 'timestamp': sql_timestamp_pretty_print(history.timestamp, lang, False, True) + ' GMT'})

    return return_array


def delete_history_in_database(nickname, transaction):
    """
    Deletes history from database

    :param nickname: User.nickname
    :return: [String]
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname if nickname else '').first()
    if not nickname or not db_user:
        return []
    DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).delete()
    DBDiscussionSession.flush()
    transaction.commit()
