"""
Provides helping function for creating the history as bubbles.

.. codeauthor: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, History, Settings, sql_timestamp_pretty_print, Issue
from dbas.input_validator import check_reaction
from dbas.lib import create_speechbubble_dict, get_text_for_argument_uid, get_text_for_statement_uid,\
    get_text_for_premisesgroup_uid, get_text_for_conclusion, bubbles_already_last_in_list
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import tag_type, get_text_for_confrontation, get_text_for_support
from dbas.strings.translator import Translator
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.helper.dictionary.bubbles import get_user_bubble_text_for_justify_statement


def save_issue_uid(issue_uid, nickname):
    """
    Saves the Issue.uid for an user

    :param issue_uid: Issue.uid
    :param nickname: User.nickname
    :return: Boolean
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return False

    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    if not db_settings:
        return False

    db_settings.set_last_topic_uid(issue_uid)
    transaction.commit()
    return True


def get_saved_issue(nickname):
    """
    Returns the last used issue of the user

    :param nickname: User.nickname
    :return: Issue.uid
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return 0

    db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    if not db_settings:
        return 0

    val = db_settings.last_topic_uid
    db_issue = DBDiscussionSession.query(Issue).get(val)
    if not db_issue:
        return 0
    return 0 if db_issue.is_disabled else val


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

    nickname = nickname if nickname else nick_of_anonymous_user

    for index, step in enumerate(splitted_history):
        url = application_url + '/discuss/' + slug + '/' + step
        if len(consumed_history) != 0:
            url += '?history=' + consumed_history
        consumed_history += step if len(consumed_history) == 0 else '-' + step

        if 'justify/' in step:
            __prepare_justify_statement_step(bubble_array, index, step, nickname, lang, url)

        elif 'reaction/' in step:
            __prepare_reaction_step(bubble_array, index, application_url, step, nickname, lang, splitted_history, url)

        elif 'support/' in step:
            __prepare_support_step(bubble_array, index, step, nickname, lang, application_url)

        else:
            logger('history_helper', 'create_bubbles_from_history', str(index) + ': unused case -> ' + step)

    return bubble_array


def __is_last_step_duplicate(index, step, splitted_history, main_url):
    """
    Check if the last step in the history are duplicates

    :param index: int
    :param step: String
    :param splitted_history: [String]
    :param main_url: String
    :return: Boolean
    """
    if step not in main_url:
        return False

    if 'justify/' in splitted_history[index:] or 'reaction/' in splitted_history[index:]:
        return False

    return True


def __prepare_justify_statement_step(bubble_array, index, step, nickname, lang, url):
    """
    Preparation for creating the justification bubbles

    :param bubble_array: [dict()]
    :param index: int
    :param step: String
    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param url: String
    :return: None
    """
    logger('history_helper', '__prepare_justify_statement_step', str(index) + ': justify case -> ' + step)
    steps = step.split('/')
    if len(steps) < 3:
        return
    mode = steps[2]
    relation = steps[3] if len(steps) > 3 else ''

    if [c for c in ('t', 'f') if c in mode] and relation == '':
        bubble = __get_bubble_from_justify_statement_step(step, nickname, lang, url)
        if bubble and not bubbles_already_last_in_list(bubble_array, bubble):
            bubble_array += bubble

    elif 'd' in mode and relation == '':
        bubbles = __get_bubble_from_dont_know_step(step, nickname, lang, url)
        if bubbles and not bubbles_already_last_in_list(bubble_array, bubbles):
            bubble_array += bubbles


def __prepare_reaction_step(bubble_array, index, application_url, step, nickname, lang, splitted_history, url):
    """
    Preparation for creating the reaction bubbles

    :param bubble_array: [dict()]
    :param index: int
    :param application_url: String
    :param step: String
    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param splitted_history:
    :param url: String
    :return: None
    """
    logger('history_helper', '__prepare_reaction_step', str(index) + ': reaction case -> ' + step)
    bubbles = get_bubble_from_reaction_step(application_url, step, nickname, lang, splitted_history, url)
    if bubbles and not bubbles_already_last_in_list(bubble_array, bubbles):
        bubble_array += bubbles


def __prepare_support_step(bubble_array, index, step, nickname, lang, application_url):
    """
    Preparation for creating the support bubbles

    :param bubble_array: [dict()]
    :param index: int
    :param step: String
    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param application_url: String
    :return: None
    """
    logger('history_helper', '__prepare_support_step', str(index) + ': support case -> ' + step)
    steps = step.split('/')
    if len(steps) < 3:
        return
    user_uid = steps[1]
    system_uid = steps[2]

    bubble = __get_bubble_from_support_step(user_uid, system_uid, nickname, lang, application_url)
    if bubble and not bubbles_already_last_in_list(bubble_array, bubble):
        bubble_array += bubble


def __get_bubble_from_justify_statement_step(step, nickname, lang, url):
    """
    Creates bubbles for the justify-keyword for an statement.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    logger('history_helper', '__justify_statement_step', 'def')
    steps = step.split('/')
    uid = int(steps[1])
    is_supportive = steps[2] == 't' or steps[2] == 'd'  # supportive = t(rue) or d(ont know) mode

    _tn = Translator(lang)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    msg, tmp = get_user_bubble_text_for_justify_statement(uid, db_user, is_supportive, _tn)

    bubble_user = create_speechbubble_dict(is_user=True, message=msg, omit_url=False, statement_uid=uid,
                                           is_supportive=is_supportive, nickname=nickname, lang=lang, url=url)
    return [bubble_user]


def __get_bubble_from_support_step(uid_user, uid_system, nickname, lang, application_url):
    """
    Creates bubbles for the support-keyword for an statement.

    :param uid_user: User.uid
    :param uid_system: Argument.uid
    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param application_url: String
    :return: [dict()]
    """
    db_arg_user = DBDiscussionSession.query(Argument).get(uid_user)
    db_arg_system = DBDiscussionSession.query(Argument).get(uid_system)

    if not db_arg_user or not db_arg_system:
        return None

    user_text = get_text_for_argument_uid(uid_user)
    bubble_user = create_speechbubble_dict(is_user=True, message=user_text, omit_url=True, argument_uid=uid_user,
                                           is_supportive=db_arg_user.is_supportive, lang=lang, nickname=nickname)

    argument_text = get_text_for_argument_uid(uid_system, colored_position=True, with_html_tag=True, attack_type='jump')

    offset = len('</' + tag_type + '>') if argument_text.endswith('</' + tag_type + '>') else 1
    while argument_text[:-offset].endswith(('.', '?', '!')):
        argument_text = argument_text[:-offset - 1] + argument_text[-offset:]

    text = get_text_for_support(db_arg_system, argument_text, nickname, application_url, Translator(lang))
    bubble_system = create_speechbubble_dict(is_system=True, message=text, omit_url=True, lang=lang)

    return [bubble_user, bubble_system]


def __get_bubble_from_attitude_step(step, nickname, lang, url):
    """
    Creates bubbles for the attitude-keyword for an statement.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    logger('history_helper', '__attitude_step', 'def')
    steps = step.split('/')
    uid = int(steps[1])
    text = get_text_for_statement_uid(uid)
    if lang != 'de':
        text = text[0:1].upper() + text[1:]
    bubble = create_speechbubble_dict(is_user=True, message=text, omit_url=False, statement_uid=uid, nickname=nickname,
                                      lang=lang, url=url)

    return [bubble]


def __get_bubble_from_dont_know_step(step, nickname, lang, url):
    """
    Creates bubbles for the dont-know-reaction for a statement.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    steps = step.split('/')
    uid = int(steps[1])

    text = get_text_for_argument_uid(uid, rearrange_intro=True, attack_type='dont_know', with_html_tag=False,
                                     start_with_intro=True)
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        text = ''

    from dbas.strings.text_generator import get_name_link_of_arguments_author
    _tn = Translator(lang)

    db_other_user, author, gender, is_okay = get_name_link_of_arguments_author(url, db_argument, nickname, False)
    if is_okay:
        intro = author + ' ' + _tn.get(_.thinksThat)
    else:
        intro = _tn.get(_.otherParticipantsThinkThat)
    sys_text = intro + ' ' + text[0:1].lower() + text[1:] + '. '
    sys_text += '<br><br>' + _tn.get(_.whatDoYouThinkAboutThat) + '?'
    sys_bubble = create_speechbubble_dict(is_system=True, message=sys_text, nickname=nickname)

    text = _tn.get(_.showMeAnArgumentFor) + (' ' if lang == 'de' else ': ') + get_text_for_conclusion(db_argument)
    user_bubble = create_speechbubble_dict(is_user=True, message=text, nickname=nickname)

    return [user_bubble, sys_bubble]


def get_bubble_from_reaction_step(main_page, step, nickname, lang, splitted_history, url, color_steps=False):
    """
    Creates bubbles for the reaction-keyword.

    :param step: String
    :param nickname: User.nickname
    :param lang: ui_locales
    :param splitted_history: [String].uid
    :param url: String
    :param color_steps: Boolean
    :return: [dict()]
    """
    logger('history_helper', 'get_bubble_from_reaction_step', 'def: ' + str(step) + ', ' + str(splitted_history))
    steps = step.split('/')
    if 'reaction' in step:
        uid = int(steps[1])
        additional_uid = int(steps[3])
        attack = steps[2]
    else:
        uid = int(steps[1])
        additional_uid = int(steps[2])
        attack = 'support'

    if not check_reaction(uid, additional_uid, attack, is_history=True):
        logger('history_helper', 'get_bubble_from_reaction_step', 'wrong reaction')
        return None

    is_supportive = DBDiscussionSession.query(Argument).get(uid).is_supportive
    last_relation = splitted_history[-1].split('/')[2]

    user_changed_opinion = len(splitted_history) > 1 and '/undercut/' in splitted_history[-2]
    support_counter_argument = False
    if step in splitted_history:
        index = splitted_history.index(step)
        try:
            support_counter_argument = 'reaction' in splitted_history[index - 1]
        except IndexError:
            support_counter_argument = False

    color_steps = color_steps and attack != 'support'  # special case for the support round
    current_argument = get_text_for_argument_uid(uid, user_changed_opinion=user_changed_opinion,
                                                 support_counter_argument=support_counter_argument,
                                                 colored_position=color_steps, nickname=nickname,
                                                 with_html_tag=color_steps)
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    db_confrontation = DBDiscussionSession.query(Argument).get(additional_uid)
    if db_argument.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)
        reply_for_argument = not (db_statement and db_statement.is_startpoint)
    else:
        reply_for_argument = True

    premise, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
    conclusion = get_text_for_conclusion(db_argument)
    sys_conclusion = get_text_for_conclusion(db_confrontation)
    confr, tmp = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid)
    user_is_attacking = not db_argument.is_supportive

    if lang != 'de':
        if current_argument.startswith('<'):
            pos = current_argument.index('>')
            current_argument = current_argument[0:pos] + current_argument[pos:pos + 1].upper() + current_argument[pos + 1:]
        else:
            current_argument = current_argument[0:1].upper() + current_argument[1:]
    premise = premise[0:1].lower() + premise[1:]

    _tn = Translator(lang)
    user_text = (_tn.get(_.otherParticipantsConvincedYouThat) + ': ') if last_relation == 'support' else ''
    user_text += '<{}>{}</{}>'.format(tag_type, current_argument if current_argument != '' else premise, tag_type)

    sys_text, tmp = get_text_for_confrontation(main_page, lang, nickname, premise, conclusion, sys_conclusion, is_supportive,
                                               attack, confr, reply_for_argument, user_is_attacking, db_argument,
                                               db_confrontation, color_html=False)

    bubble_user = create_speechbubble_dict(is_user=True, message=user_text, omit_url=False, argument_uid=uid,
                                           is_supportive=is_supportive, nickname=nickname, lang=lang, url=url)
    if attack == 'end':
        bubble_syst = create_speechbubble_dict(is_system=True, message=sys_text, omit_url=True, nickname=nickname,
                                               lang=lang)
    else:
        bubble_syst = create_speechbubble_dict(is_system=True, id='question-bubble-' + str(additional_uid),
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


def save_path_in_database(nickname, slug, path, history=''):
    """
    Saves a path into the database

    :param nickname: User.nickname
    :param slug: Issue.slug
    :param path: String
    :param history: String
    :return: None
    """
    logger('XX HistoryHelper', 'save_path_in_database', 'path: {}, history: {}, slug: {}'.format(path, history, slug))

    if not nickname:
        return None

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None

    if path.startswith('/discuss'):
        path = path[len('/discuss'):]
        path = path[path.index('/') if '/' in path else 0:]

    if slug not in path:
        path = '/{}/{}'.format(slug, path)

    if len(history) > 0:
        history = '?history=' + history

    logger('XX HistoryHelper', 'save_path_in_database', 'saving {}{}'.format(path, history))

    DBDiscussionSession.add(History(author_uid=db_user.uid, path=path + history))
    DBDiscussionSession.flush()
    # transaction.commit()  # 207


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
        return_array.append({'path': history.path,
                             'timestamp': sql_timestamp_pretty_print(history.timestamp, lang, False, True) + ' GMT'})

    return return_array


def delete_history_in_database(nickname):
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
