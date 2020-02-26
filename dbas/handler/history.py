"""
Provides helping function for creating the history as bubbles.
"""
import logging
from typing import List, Optional

from pyramid.request import Request

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, History, sql_timestamp_pretty_print, \
    Issue
from dbas.helper.dictionary.bubbles import get_user_bubble_text_for_justify_statement
from dbas.input_validator import check_reaction
from dbas.lib import create_speechbubble_dict, get_text_for_argument_uid, get_text_for_conclusion, \
    bubbles_already_last_in_list, BubbleTypes, nick_of_anonymous_user, Relations, Attitudes, \
    relation_mapper, wrap_history_onto_enum, ArgumentationStep
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital, start_with_small, replace_multiple_chars
from dbas.strings.text_generator import tag_type, get_text_for_confrontation, get_text_for_support, remove_punctuation
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


class SessionHistory:
    def __init__(self, history: str = None):
        """
        Creates current history object for user

        :return:
        """
        session_history_array = []
        if history is not None:
            session_history_array = history.split('-')
        self.session_history_array: List[str] = session_history_array

    def append_action(self, request: Request):
        """
        Appends new action to current history

        :param request
        :return:
        """
        history_action = request.params.get(ArgumentationStep.HISTORY.value, '')
        if len(history_action) > 0:
            # Splits history url by "-" and appends last history action to history array without a leading "/"
            split_history = history_action.split('-')
            last_split_history = split_history[-1]
            cleaned_last_split = last_split_history[1:]
            self.get_session_history_as_list().append(cleaned_last_split)

    def get_nth_last_action(self, n: int) -> str:
        """
        This method returns the nth last actions of the session history.

        :param n:
        :return: nth last actions of the session history.
        """
        return self.get_session_history_as_list()[-n] if len(self.get_session_history_as_list()) > 0 else ''

    def get_session_history_as_list(self) -> List[str]:
        """
        Returns session history

        :return:
        """
        return self.session_history_array

    def get_session_history_as_string(self) -> str:
        """
        Returns session history as string

        :return:
        """
        return "-".join(self.get_session_history_as_list())

    def create_bubbles(self, nickname: str = '', lang: str = '', slug: str = '') -> List[dict]:
        """
        Creates the bubbles for every history step

        :param history: String
        :param nickname: User.nickname
        :param lang: ui_locales
        :param slug: String
        :return: Array
        """
        if len(self.session_history_array) == 0:
            return []

        LOG.debug("nickname: %s, history: %s", nickname, self.get_session_history_as_string())

        bubble_array = []
        consumed_history = ''

        nickname = nickname if nickname else nick_of_anonymous_user
        db_user = nickname if isinstance(nickname, User) else DBDiscussionSession.query(User).filter_by(
            nickname=nickname).first()

        for index, step in enumerate(self.get_session_history_as_list()):
            url = '/' + slug + '/' + step
            if len(consumed_history) != 0:
                url += '?' + ArgumentationStep.HISTORY.value + '=' + consumed_history

            consumed_history += step if len(consumed_history) == 0 else '-' + step
            if ArgumentationStep.JUSTIFY.value + '/' in step:
                _prepare_justify_statement_step(bubble_array, index, step, db_user, lang, url)

            elif ArgumentationStep.REACTION.value + '/' in step:
                _prepare_reaction_step(bubble_array, index, step, db_user, lang, self.get_session_history_as_list(),
                                       url)

            elif ArgumentationStep.SUPPORT.value + '/' in step:
                _prepare_support_step(bubble_array, index, step, db_user, lang)

            else:
                LOG.debug("%s: unused case -> %s", index, step)

        return bubble_array


def cleaned_split_history_step(step):
    return list(map(lambda x: int(x) if x.isdigit() else x, step.split('/')[1:]))


def save_history_to_session_history(request: Request):
    """
    Saves the current history from the URL to the history object in the request session

    :param request:
    :return:
    """
    session_history = request.session.get('session_history')
    if session_history is not None:
        session_history.append_action(request)
        request.session.update({'session_history': session_history})


def save_issue(issue: Issue, db_user: User) -> None:
    """
    Saves the Issue.uid for an user

    :param issue: Issue.uid
    :param db_user: User
    :return: Boolean
    """
    db_settings = db_user.settings
    db_settings.last_topic = issue
    DBDiscussionSession.add(db_settings)


def get_last_issue_of(db_user: User) -> Optional[Issue]:
    """
    Returns the last used issue of the user or None

    :param db_user: User
    :return: Issue.uid or 0
    """
    if not db_user or db_user.is_anonymous():
        return None

    db_issue = db_user.settings.last_topic
    if not db_issue:
        return None

    return None if db_issue.is_disabled else db_issue


def split(history: str) -> list:
    """
    Splits history by specific keyword and removes leading '/'

    :param history: String
    :return: [String]
    """
    return [his[1:] if his[0:1] == '/' else his for his in history.split('-')]


def get_seen_statements_from(path: str) -> set:
    """
    This method returns a list of statement_uids which the user has seen or chosen while discussing

    :param path: Should be the latest path in the history of the current user
    :return: a list of seen statement_uids
    """
    return set([int(s) for s in replace_multiple_chars(path, ['/', '-', '?'], ' ').split() if s.isdigit()])


def _prepare_justify_statement_step(bubble_array: List[dict], index: int, step: str, db_user: User, lang: str,
                                    url: str) -> None:
    """
    Preparation for creating the justification bubbles

    :param bubble_array: [dict()]
    :param index: int
    :param step: String
    :param db_user: User
    :param lang: Language.ui_locales
    :param url: String
    :return: None
    """
    LOG.debug("%s: justify case -> %s", index, step)
    single_split_history_step = cleaned_split_history_step(step)
    LOG.debug(single_split_history_step)
    if len(single_split_history_step) < 3:
        return
    single_split_history_step_enum = wrap_history_onto_enum(single_split_history_step)
    mode = single_split_history_step_enum.ATTITUDE_TYPE
    relation = single_split_history_step_enum.ATTITUDE_TYPE if len(single_split_history_step) > 3 else ''

    LOG.debug(mode)

    if [c for c in (Attitudes.AGREE.value, Attitudes.DISAGREE.value) if c in mode] and relation == '':
        bubble = _get_bubble_from_justify_statement_step(step, db_user, lang, url)
        if bubble and not bubbles_already_last_in_list(bubble_array, bubble):
            bubble_array += bubble

    elif Attitudes.DONT_KNOW.value in mode and relation == '':
        bubbles = _get_bubble_from_dont_know_step(step, db_user, lang)
        if bubbles and not bubbles_already_last_in_list(bubble_array, bubbles):
            bubble_array += bubbles


def _prepare_reaction_step(bubble_array: List[dict], index: int, step: str, db_user: User, lang: str,
                           split_history: list, url: str) -> None:
    """
    Preparation for creating the reaction bubbles

    :param bubble_array: [dict()]
    :param index: int
    :param step: String
    :param db_user: User
    :param lang: Language.ui_locales
    :param split_history:
    :param url: String
    :return: None
    """
    LOG.debug("%s: reaction case -> %s", index, step)
    bubbles = get_bubble_from_reaction_step(step, db_user, lang, split_history, url)
    if bubbles and not bubbles_already_last_in_list(bubble_array, bubbles):
        bubble_array += bubbles


def _prepare_support_step(bubble_array: List[dict], index: int, step: str, db_user: User, lang: str) -> None:
    """
    Preparation for creating the support bubbles

    :param bubble_array: [dict()]
    :param index: int
    :param step: String
    :param db_user: User
    :param lang: Language.ui_locales
    :return: None
    """
    LOG.debug("%s: support case -> %s", index, step)
    single_split_history_step = cleaned_split_history_step(step)
    if len(single_split_history_step) < 3:
        return
    single_split_history_step_enum = wrap_history_onto_enum(single_split_history_step)
    user_uid = single_split_history_step_enum.UID
    system_uid = single_split_history_step_enum.ATTITUDE_TYPE

    bubble = _get_bubble_from_support_step(user_uid, system_uid, db_user, lang)
    if bubble and not bubbles_already_last_in_list(bubble_array, bubble):
        bubble_array += bubble


def _get_bubble_from_justify_statement_step(step: str, db_user: User, lang: str, url: str) -> List[dict]:
    """
    Creates bubbles for the justify-keyword for an statement.

    :param step: String
    :param db_user: User
    :param lang: ui_locales
    :param url: String
    :return: [dict()]
    """
    single_split_history_step = wrap_history_onto_enum(cleaned_split_history_step(step))
    uid = single_split_history_step.UID
    is_supportive = single_split_history_step.ATTITUDE_TYPE == Attitudes.AGREE.value or single_split_history_step.ATTITUDE_TYPE == Attitudes.DONT_KNOW.value

    _tn = Translator(lang)
    statement = DBDiscussionSession.query(Statement).get(uid)
    msg, tmp = get_user_bubble_text_for_justify_statement(statement, db_user, is_supportive, _tn)

    bubble_user = create_speechbubble_dict(BubbleTypes.USER, bubble_url=url, content=msg, omit_bubble_url=False,
                                           statement_uid=uid, is_supportive=is_supportive, db_user=db_user,
                                           lang=lang)
    return [bubble_user]


def _get_bubble_from_support_step(arg_uid_user: int, uid_system: int, db_user: User, lang: str) \
        -> Optional[List[list]]:
    """
    Creates bubbles for the support-keyword for an statement.

    :param arg_uid_user: User.uid
    :param uid_system: Argument.uid
    :param db_user: User
    :param lang: Language.ui_locales
    :return: [dict()]
    """
    db_arg_user = DBDiscussionSession.query(Argument).get(arg_uid_user)
    db_arg_system = DBDiscussionSession.query(Argument).get(uid_system)

    if not db_arg_user or not db_arg_system:
        return None

    user_text = get_text_for_argument_uid(arg_uid_user)
    bubble_user = create_speechbubble_dict(BubbleTypes.USER, content=user_text, omit_bubble_url=True,
                                           argument_uid=arg_uid_user, is_supportive=db_arg_user.is_supportive,
                                           db_user=db_user, lang=lang)

    argument_text = get_text_for_argument_uid(uid_system, colored_position=True, with_html_tag=True, attack_type='jump')
    argument_text = remove_punctuation(argument_text)

    text = get_text_for_support(db_arg_system, argument_text, db_user.nickname, Translator(lang))
    db_other_author = DBDiscussionSession.query(User).get(db_arg_system.author_uid)
    bubble_system = create_speechbubble_dict(BubbleTypes.SYSTEM, content=text, omit_bubble_url=True, lang=lang,
                                             other_author=db_other_author)

    return [bubble_user, bubble_system]


def _get_bubble_from_dont_know_step(step: str, db_user: User, lang: str) -> List[dict]:
    """
    Creates bubbles for the don't-know-reaction for a statement.

    :param step: String
    :param db_user: User
    :param lang: ui_locales
    :return: [dict()]
    """
    single_split_history_step = wrap_history_onto_enum(cleaned_split_history_step(step))
    uid = single_split_history_step.UID

    text = get_text_for_argument_uid(uid, rearrange_intro=True, attack_type='dont_know', with_html_tag=False,
                                     start_with_intro=True)
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        text = ''

    from dbas.strings.text_generator import get_name_link_of_arguments_author
    _tn = Translator(lang)

    data = get_name_link_of_arguments_author(db_argument, db_user.nickname, False)
    if data['is_valid']:
        intro = data['link'] + ' ' + _tn.get(_.thinksThat)
    else:
        intro = _tn.get(_.otherParticipantsThinkThat)
    sys_text = intro + ' ' + start_with_small(text) + '. '
    sys_text += '<br><br>' + _tn.get(_.whatDoYouThinkAboutThat) + '?'
    sys_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, content=sys_text, db_user=db_user,
                                          other_author=data['user'])

    text = _tn.get(_.showMeAnArgumentFor) + (' ' if lang == 'de' else ': ') + get_text_for_conclusion(db_argument)
    user_bubble = create_speechbubble_dict(BubbleTypes.USER, content=text, db_user=db_user)

    return [user_bubble, sys_bubble]


def get_bubble_from_reaction_step(step: str, db_user: User, lang: str, split_history: list, url: str,
                                  color_steps: bool = False) -> Optional[list]:
    """
    Creates bubbles for the reaction-keyword.

    :param step: String
    :param db_user: User
    :param lang: ui_locales
    :param split_history: [String].uid
    :param url: String
    :param color_steps: Boolean
    :return: [dict()]
    """
    LOG.debug("def: %s, %s", step, split_history)

    cleaned_split_history = cleaned_split_history_step(step)
    if cleaned_split_history[0] == ArgumentationStep.REACTION.value:
        cleaned_split_history = cleaned_split_history[1:]

    single_split_history_step = wrap_history_onto_enum(cleaned_split_history,
                                                       ArgumentationStep.REACTION.value in step)
    uid = single_split_history_step.UID

    LOG.debug(step)

    additional_uid = single_split_history_step.ADDITIONAL_UID
    attack = relation_mapper[single_split_history_step.RELATION]

    if not check_reaction(uid, additional_uid, attack):
        LOG.debug("Wrong reaction")
        return None

    return _create_reaction_history_bubbles(step, db_user, lang, split_history, url, color_steps, uid,
                                            additional_uid, attack)


def _create_reaction_history_bubbles(step: str, db_user: User, lang: str, split_history: list, url: str,
                                     color_steps: bool, uid: int, additional_uid: int,
                                     attack) -> list:
    is_supportive = DBDiscussionSession.query(Argument).get(uid).is_supportive
    last_relation = get_last_relation(split_history)

    user_changed_opinion = len(split_history) > 1 and '/' + Relations.UNDERCUT.value + '/' in split_history[-2]
    support_counter_argument = False

    if step in split_history:
        index = split_history.index(step)
        try:
            support_counter_argument = ArgumentationStep.REACTION.value in split_history[index - 1]
        except IndexError:
            support_counter_argument = False

    color_steps = color_steps and attack != Relations.SUPPORT  # special case for the support round
    current_arg = get_text_for_argument_uid(uid, user_changed_opinion=user_changed_opinion,
                                            support_counter_argument=support_counter_argument,
                                            colored_position=color_steps, nickname=db_user.nickname,
                                            with_html_tag=color_steps)

    db_argument = DBDiscussionSession.query(Argument).get(uid)
    db_confrontation = DBDiscussionSession.query(Argument).get(additional_uid)
    reply_for_argument = True
    if db_argument.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)
        reply_for_argument = not (db_statement and db_statement.is_position)

    premise = db_argument.get_premisegroup_text()
    conclusion = get_text_for_conclusion(db_argument)
    sys_conclusion = get_text_for_conclusion(db_confrontation)
    confr = db_confrontation.get_premisegroup_text()
    user_is_attacking = not db_argument.is_supportive

    if lang != 'de':
        current_arg = start_with_capital(current_arg)
        if current_arg.startswith('<'):
            pos = current_arg.index('>')
            current_arg = current_arg[0:pos] + current_arg[pos:pos + 1].upper() + current_arg[pos + 1:]

    premise = start_with_small(premise)

    _tn = Translator(lang)
    user_text = ''
    if last_relation == Relations.SUPPORT:
        user_text = _tn.get(_.otherParticipantsConvincedYouThat) + ': '

    user_text += '<{}>{}</{}>'.format(tag_type, current_arg if current_arg != '' else premise, tag_type)

    sys_text, tmp = get_text_for_confrontation(lang, db_user.nickname, premise, conclusion, sys_conclusion,
                                               is_supportive, attack, confr, reply_for_argument, user_is_attacking,
                                               db_argument, db_confrontation, color_html=False)

    bubble_user = create_speechbubble_dict(BubbleTypes.USER, bubble_url=url, content=user_text, omit_bubble_url=False,
                                           argument_uid=uid, is_supportive=is_supportive, db_user=db_user,
                                           lang=lang)
    db_tmp = DBDiscussionSession.query(User).get(db_confrontation.author_uid)
    if not attack:
        bubble_syst = create_speechbubble_dict(BubbleTypes.SYSTEM, content=sys_text, omit_bubble_url=True,
                                               db_user=db_user, lang=lang, other_author=db_tmp)
    else:
        bubble_syst = create_speechbubble_dict(BubbleTypes.SYSTEM, uid='question-bubble-' + str(additional_uid),
                                               content=sys_text, omit_bubble_url=True, db_user=db_user,
                                               lang=lang, other_author=db_tmp)
    return [bubble_user, bubble_syst]


def get_last_relation(split_history):
    if len(split_history) <= 1:
        return ''
    split_last_history_item = split_history[-1].split('/')
    if len(split_last_history_item) <= 2:
        return ''
    return split_last_history_item[2]


def save_database(db_user: User, slug: str, path: str, history: str = '') -> None:
    """
    Saves a path into the database

    :param db_user: User
    :param slug: Issue.slug
    :param path: String
    :param history: String
    :return: None
    """
    LOG.debug("Path: %s, history: %s, slug: %s", path, history, slug)

    if path.startswith('/discuss'):
        path = path[len('/discuss'):]
        path = path[path.index('/') if '/' in path else 0:]

    db_issues = DBDiscussionSession.query(Issue).all()
    slugs = [issue.slug for issue in db_issues]
    if not any([slug in path for slug in slugs]) or slug not in path:
        path = '/{}/{}'.format(slug, path)

    if len(history) > 0:
        history = '?{}={}'.format(ArgumentationStep.HISTORY.value, history)

    LOG.debug("Saving %s%s", path, history)
    DBDiscussionSession.add(History(author_uid=db_user.uid, path=path + history))
    DBDiscussionSession.flush()


def get_from_database(db_user: User, lang: str) -> List[dict]:
    """
    Returns history from database

    :param db_user: User
    :param lang: ui_locales
    :return: [String]
    """
    db_history = DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).all()
    return_array = []
    for history in db_history:
        return_array.append({
            'path': history.path,
            'timestamp': sql_timestamp_pretty_print(history.timestamp, lang, False, True) + ' GMT'
        })

    return return_array


def delete_in_database(db_user: User) -> True:
    """
    Deletes history from database

    :param db_user: User
    :return: [String]
    """
    DBDiscussionSession.query(History).filter_by(author_uid=db_user.uid).delete()
    DBDiscussionSession.flush()
    return True


def save_and_set_cookie(request: Request, db_user: User, issue: Issue) -> str:
    """

    :param request: pyramid's request object
    :param db_user: the user
    :param issue: the discussion's issue od
    :rtype: str
    :return: current user's history
    """
    history = request.params.get(ArgumentationStep.HISTORY.value, '')
    save_history_to_session_history(request)

    if db_user and db_user.nickname != nick_of_anonymous_user:
        save_database(db_user, issue.slug, request.path, history)
        save_issue(issue, db_user)

    if request.path.startswith('/discuss/'):
        path = request.path[len('/discuss/'):]
        path = path[path.index('/') if '/' in path else 0:]
        request.response.set_cookie('_HISTORY_', history + '-' + path)

    return history
