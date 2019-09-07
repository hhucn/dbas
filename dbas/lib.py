"""
Common, pure functions used by the D-BAS.
"""
import hashlib
import locale
import logging
import os
import re
import warnings
from collections import defaultdict
from datetime import datetime
from enum import Enum, auto
from html import escape, unescape
from random import randint
from typing import List, Optional
from urllib import parse
from uuid import uuid4

from sqlalchemy import func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Premise, Statement, TextVersion, Issue, User, Settings, \
    ClickedArgument, ClickedStatement, MarkedArgument, MarkedStatement, PremiseGroup
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital, start_with_small
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)

nick_of_anonymous_user = 'anonymous'

fallback_lang = 'en'
tag_type = 'span'
start_attack = '<{} data-argumentation-type="attack">'.format(tag_type)
start_argument = '<{} data-argumentation-type="argument">'.format(tag_type)
start_position = '<{} data-argumentation-type="position">'.format(tag_type)
start_content = '<{} class="triangle-content-text">'.format(tag_type)
start_pro = '<{} data-attitude="pro">'.format(tag_type)
start_con = '<{} data-attitude="con">'.format(tag_type)
start_tag = '<{}>'.format(tag_type)
end_tag = '</{}>'.format(tag_type)


class BubbleTypes(Enum):
    USER = auto()
    SYSTEM = auto()
    STATUS = auto()
    INFO = auto()

    def __str__(self):
        return str(self.value)


class Relations(Enum):
    UNDERMINE = 'undermine'
    SUPPORT = 'support'
    UNDERCUT = 'undercut'
    REBUT = 'rebut'

    def __str__(self):
        return str(self.value)


class Attitudes(Enum):
    AGREE = 'agree'
    DISAGREE = 'disagree'
    DONT_KNOW = 'dontknow'

    def __str__(self):
        return str(self.value)


relation_mapper = {relation.value: relation for relation in Relations}
attitude_mapper = {attitude.value: attitude for attitude in Attitudes}


def get_global_url():
    """
    Returns the global url of the project, based on the ENV

    :return: String
    """
    return os.environ.get('URL', '')


def get_changelog(no):
    """
    Returns the 'no' last entries from the changelog

    :param no: int
    :return: list
    """
    path = str(os.path.realpath(__file__ + '/../../CHANGELOG.md'))
    lines = [line.rstrip('\n').strip() for line in open(path) if len(line.rstrip('\n').strip()) > 0]
    changelog = []
    title = ''
    body = []
    for l in lines:
        if l.startswith('#'):
            if len(title) > 0:
                changelog.append({'title': title, 'body': body})
                body = []
            title = l.replace('### ', '')
        else:
            body.append(l.replace('- ', ''))

    return changelog[0:no]


def is_development_mode(registry):
    """
    Returns true, if mode is set to development in current ini file.

    :param registry: request.registry
    :return: Boolean
    """
    if 'mode' in registry.settings:
        return registry.settings['mode'].lower() == 'development'
    return False


def usage_of_modern_bubbles(registry):
    """
    Returns true, if modern bubbles are set in the current ini file.

    :param registry: request.registry
    :return: Boolean
    """
    if 'modern_bubbles' in registry.settings:
        return registry.settings['modern_bubbles'].lower() == 'true'
    return False


def usage_of_matomo(registry):
    """
    Returns true, if matomo is set in the current ini file.

    :param registry: request.registry
    :return: Boolean
    """
    if 'mode' in registry.settings:
        return registry.settings['usage_of_matomo'].lower() == 'true'
    return False


def escape_string(text):
    """
    Escapes all html special chars.

    :param text: string
    :return: html.escape(text)
    """
    return escape(text)


def get_discussion_language(matchdict, params, session, current_issue_uid=None):
    """
    Returns Language.ui_locales
    CALL AFTER issue_handler.get_id_of_slug(..)!

    :param matchdict: matchdict of the current request
    :param params: params of the current request
    :param session: session of the current request
    :param current_issue_uid: uid
    :return:
    """
    if not current_issue_uid:
        current_issue = DBDiscussionSession.query(Issue).filter(Issue.is_disabled == False,
                                                                Issue.is_private == False).first()
        current_issue_uid = current_issue.uid if current_issue else None

    # first matchdict, then params, then session, afterwards fallback
    issue = matchdict['issue'] if 'issue' in matchdict \
        else params['issue'] if 'issue' in params \
        else session['issue'] if 'issue' in session \
        else current_issue_uid

    db_issue = DBDiscussionSession.query(Issue).get(issue)

    return db_issue.lang if db_issue else 'en'


def pretty_print_timestamp(ts, lang):
    """
    Pretty print of a locale

    :param ts:  Timestamp
    :param lang: ui_locales
    :return: String
    """
    formatter = '%b. %d.'
    if lang == 'de':
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
            formatter = '%d. %b.'
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

    return datetime.strptime(str(ts), '%Y-%m-%d').strftime(formatter)


def get_all_arguments_by_statement(statement_uid, include_disabled=False) -> Optional[List[Argument]]:
    """
    Returns a list of all arguments where the statement is a conclusion or member of the premisegroup

    :param statement_uid: Statement.uid
    :param include_disabled: Boolean
    :return: [Arguments]
    """
    LOG.debug("Retrieving all arguments by statement-uid: %s, include_disabled %s", statement_uid, include_disabled)
    db_arguments = __get_arguments_of_conclusion(statement_uid, include_disabled)
    arg_array = [arg for arg in db_arguments] if db_arguments else []

    premises = DBDiscussionSession.query(Premise).filter_by(statement_uid=statement_uid)
    if not include_disabled:
        premises = premises.filter_by(is_disabled=False)
    premises = premises.all()

    for premise in premises:
        arg_array += __get_argument_of_premisegroup(premise.premisegroup_uid, include_disabled)

    db_undercuts = []
    for arg in arg_array:
        db_undercuts += __get_undercuts_of_argument(arg.uid, include_disabled)

    db_undercutted_undercuts = []
    for arg in db_undercuts:
        db_undercutted_undercuts += __get_undercuts_of_argument(arg.uid, include_disabled)

    arg_array = list(set(arg_array + db_undercuts + db_undercutted_undercuts))

    LOG.debug("returning arguments %s", [arg.uid for arg in arg_array])
    return arg_array if len(arg_array) > 0 else None


def __get_argument_of_premisegroup(premisegroup_uid, include_disabled):
    """
    Returns all arguments with the given premisegroup

    :param premisegroup_uid: PremisgGroup.uid
    :param include_disabled: Boolean
    :return: list of Arguments
    """
    db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=premisegroup_uid)
    if not include_disabled:
        db_arguments = db_arguments.filter_by(is_disabled=False)
    return db_arguments.all() if db_arguments else []


def __get_undercuts_of_argument(argument_uid, include_disabled):
    """
    Returns all undercuts fo the given argument

    :param argument_uid: Argument.uid
    :param include_disabled: boolean
    :return: list of Arguments
    """
    db_undercuts = DBDiscussionSession.query(Argument).filter_by(argument_uid=argument_uid)
    if not include_disabled:
        db_undercuts = db_undercuts.filter_by(is_disabled=False)
    return db_undercuts.all() if db_undercuts else []


def __get_arguments_of_conclusion(statement_uid, include_disabled):
    """
    Returns all arguments, where the statement is set as conclusion

    :param statement_uid: Statement.uid
    :param include_disabled: Boolean
    :return: list of arguments
    """
    db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=statement_uid)
    if not include_disabled:
        db_arguments = db_arguments.filter_by(is_disabled=False)
    return db_arguments.all() if db_arguments else []


def get_all_arguments_with_text_by_statement_id(statement_uid: int) -> List[dict]:
    """
    Given a statement_uid, it returns all arguments, which use this statement and adds
    the corresponding text to it, which normally appears in the bubbles. The resulting
    text depends on the provided language.

    :param statement_uid: uid to a statement, which should be analyzed
    :return: list of dictionaries containing some properties of these arguments
    :rtype: list
    """
    LOG.debug("Retrieving arguments for statement uid: %s", statement_uid)
    arguments: List[Argument] = get_all_arguments_by_statement(statement_uid)
    if arguments:
        return [{
            'uid': arg.uid,
            'texts': {
                'display': get_text_for_argument_uid(arg.uid),
                'conclusion': arg.get_conclusion_text(),
                'premise': arg.get_premisegroup_text(),
                'attacks': arg.get_attacked_argument_text(),
            },
            'author': arg.author,
            'issue': arg.issue
        }
            for arg in arguments]
    return []


def get_all_arguments_with_text_and_url_by_statement(db_statement: Statement, urlmanager, color_statement=False,
                                                     is_jump=False):
    """
    Given a statement_uid, it returns all arguments, which use this statement and adds
    the corresponding text to it, which normally appears in the bubbles. The resulting
    text depends on the provided language.

    :param db_statement: Statement
    :param urlmanager:
    :param color_statement: True, if the statement (specified by the ID) should be colored
    :return: list of dictionaries containing some properties of these arguments
    :rtype: list
    """
    LOG.debug("main %s", db_statement.uid)
    arguments = get_all_arguments_by_statement(db_statement.uid)
    uids = [arg.uid for arg in arguments] if arguments else None
    results = list()
    sb = '<{} data-argumentation-type="position">'.format(tag_type) if color_statement else ''
    se = '</{}>'.format(tag_type) if color_statement else ''

    if not uids:
        return []

    uids.sort()
    for uid in uids:
        statement_text = db_statement.get_text()
        attack_type = 'jump' if is_jump else ''
        argument_text = get_text_for_argument_uid(uid, anonymous_style=True, attack_type=attack_type)
        pos = argument_text.lower().find(statement_text.lower())

        argument_text = argument_text[:pos] + sb + argument_text[pos:]
        pos += len(statement_text) + len(sb)
        argument_text = argument_text[:pos] + se + argument_text[pos:]

        results.append({
            'uid': uid,
            'text': argument_text,
            'url': urlmanager.get_url_for_jump(uid)
        })
    return results


def get_text_for_argument_uid(uid: int, nickname: str = None, with_html_tag: bool = False,
                              start_with_intro: bool = False, first_arg_by_user: bool = False,
                              user_changed_opinion: bool = False, rearrange_intro: bool = False,
                              colored_position: bool = False, attack_type: str = None,
                              minimize_on_undercut: bool = False, is_users_opinion: bool = True,
                              anonymous_style: bool = False, support_counter_argument: bool = False) -> str:
    """
    Returns current argument as string like "conclusion, because premise1 and premise2"

    :param uid: Integer
    :param nickname: String
    :param with_html_tag: Boolean
    :param start_with_intro: Boolean
    :param first_arg_by_user: Boolean
    :param user_changed_opinion: Boolean
    :param rearrange_intro: Boolean
    :param colored_position: Boolean
    :param attack_type: String
    :param minimize_on_undercut: Boolean
    :param anonymous_style: Boolean
    :param support_counter_argument: Boolean
    :param is_users_opinion: Boolean
    :return: String
    """
    LOG.debug("Constructing text for argument with uid %s", uid)
    db_argument: Argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        return None

    lang = db_argument.lang
    _t = Translator(lang)
    premisegroup_by_user = False
    author_uid = None
    db_user: User = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()

    if db_user:
        author_uid = db_user.uid
        pgroup: PremiseGroup = DBDiscussionSession.query(PremiseGroup).get(db_argument.premisegroup_uid)
        marked_argument: MarkedArgument = DBDiscussionSession.query(MarkedArgument).filter_by(
            argument_uid=uid,
            author_uid=db_user.uid).first()
        premisegroup_by_user = pgroup.author_uid == db_user.uid or marked_argument is not None

    arguments = __get_chain_of_attacking_arguments(db_argument)

    if attack_type == 'jump':
        return __build_argument_for_jump(arguments, with_html_tag)

    if len(arguments) == 1:
        # build one argument only
        return __build_single_argument(arguments[0], rearrange_intro, with_html_tag, colored_position, attack_type, _t,
                                       start_with_intro, is_users_opinion, anonymous_style, support_counter_argument,
                                       author_uid)

    else:
        # get all pgroups and at last, the conclusion
        return __build_nested_argument(arguments, first_arg_by_user, user_changed_opinion, with_html_tag,
                                       start_with_intro, minimize_on_undercut, anonymous_style, premisegroup_by_user,
                                       _t)


def __get_chain_of_attacking_arguments(argument: Argument) -> List[Argument]:
    """
    Traverse through all arguments which might be connected to our starting argument and collect them all.

    :param argument:
    :return:
    """
    arguments = [argument]
    while argument.attacks:
        argument: Argument = argument.attacks
        arguments.append(argument)
    return arguments


def __build_argument_for_jump(arg_array: List[Argument], with_html_tag: bool) -> str:
    """
    Build text for an argument, if we jump to this argument

    :param arg_array: [Argument]
    :param with_html_tag: This parameter is ignored in the next steps, which is why we should rewrite this function.
    "intro" in the next steps will always add html attributes.
    :return: String
    """
    tag_premise = ('<{} data-argumentation-type="attack">'.format(tag_type))
    tag_conclusion = ('<{} data-argumentation-type="argument">'.format(tag_type))
    tag_end = ('</{}>'.format(tag_type))
    _t = Translator(arg_array[0].lang)

    if len(arg_array) == 1:
        ret_value = __build_val_for_jump(arg_array[0], tag_premise, tag_conclusion, tag_end, _t)
    elif len(arg_array) == 2:
        ret_value = __build_val_for_undercut(arg_array, tag_premise, tag_conclusion, tag_end, _t)
    else:
        ret_value = __build_val_for_undercutted_undercut(arg_array, tag_premise, tag_conclusion, tag_end, _t)

    ret_value = unhtmlify(ret_value) if not with_html_tag else ret_value

    return ret_value.replace('  ', ' ')


def __build_val_for_jump(db_argument: Argument, tag_premise, tag_conclusion, tag_end, _t) -> str:
    premises = db_argument.get_premisegroup_text()
    if premises[-1] != '.':
        premises += '.'
    conclusion = db_argument.get_conclusion_text()

    because = _t.get(_.because).lower()
    conclusion = tag_conclusion + conclusion + tag_end
    premises = tag_premise + premises + tag_end

    intro = (start_con + _t.get(_.isNotRight).lower() + end_tag) if not db_argument.is_supportive else ''
    ret_value = '{} {} {} {}'.format(conclusion, intro, because, premises)
    if _t.get_lang() == 'de':
        intro = _t.get(_.itIsTrueThatAnonymous) if db_argument.is_supportive else _t.get(_.itIsFalseThatAnonymous)
        intro = start_with_capital(intro)
        intro = (start_pro if db_argument.is_supportive else start_con) + intro + end_tag
        ret_value = '{} {}, {} {}'.format(intro, conclusion, because, premises)

    return ret_value


def __build_val_for_undercut(arg_array: List[Argument], tag_premise, tag_conclusion, tag_end, _t):
    db_undercut = arg_array[0]
    db_conclusion_argument = arg_array[1]
    premise = db_undercut.get_premisegroup_text()
    conclusion_premise = db_conclusion_argument.get_premisegroup_text()
    conclusion_conclusion = db_conclusion_argument.get_conclusion_text()

    premise = tag_premise + premise + tag_end
    conclusion_premise = tag_conclusion + conclusion_premise + tag_end
    conclusion_conclusion = tag_conclusion + conclusion_conclusion + tag_end

    intro = (_t.get(_.statementAbout) + ' ') if _t.get_lang() == 'de' else ''
    bind = start_con + _t.get(_.isNotAGoodReasonFor) + end_tag
    because = _t.get(_.because)
    ret_value = '{}{} {} {}. {} {}.'.format(intro, conclusion_premise, bind, conclusion_conclusion, because, premise)

    return ret_value


def __build_val_for_undercutted_undercut(arg_array: List[Argument], tag_premise, tag_conclusion, tag_end, _t):
    premise1 = arg_array[0].get_premisegroup_text()
    premise2 = arg_array[1].get_premisegroup_text()
    premise3 = arg_array[2].get_premisegroup_text()
    conclusion = arg_array[2].get_conclusion_text()

    bind = start_con + _t.get(_.isNotAGoodReasonAgainstArgument) + end_tag
    because = _t.get(_.because)
    seperator = ',' if _t.get_lang() == 'de' else ''

    premise1 = tag_premise + premise1 + tag_end
    premise2 = tag_conclusion + premise2 + tag_end
    argument = '{}{} {} {}'.format(conclusion, seperator, because.lower(), premise3)
    argument = tag_conclusion + argument + tag_end

    # P2 ist kein guter Grund gegen das Argument, dass C weil P3. Weil P1
    ret_value = '{} {} {}. {} {}'.format(premise2, bind, argument, because, premise1)
    return ret_value


def __build_single_argument(db_argument: Argument, rearrange_intro: bool, with_html_tag: bool, colored_position: bool,
                            attack_type: str, _t: Translator, start_with_intro: bool, is_users_opinion: bool,
                            anonymous_style: bool, support_counter_argument: bool = False, author_uid=None):
    """
    Build up argument text for a single argument

    Please, do not touch this!

    :param rearrange_intro: Boolean
    :param with_html_tag: Boolean
    :param colored_position: Boolean
    :param attack_type: String
    :param _t: Translator
    :param start_with_intro: Boolean
    :param is_users_opinion: Boolean
    :param anonymous_style: Boolean
    :param support_counter_argument: Boolean
    :param author_uid: User.uid
    :return: String
    """
    premises_text = db_argument.get_premisegroup_text()
    conclusion_text = db_argument.get_conclusion_text()
    lang = db_argument.lang

    if lang != 'de':
        premises_text = start_with_small(premises_text)

    tag_dict = __get_tags_for_building_single_argument(with_html_tag, attack_type, colored_position, premises_text,
                                                       conclusion_text)
    premises_text = tag_dict['premise']
    conclusion_text = tag_dict['conclusion']
    sb = tag_dict['tag_begin']
    sb_none = tag_dict['tag_none']
    se = tag_dict['tag_end']

    marked_element = False
    if author_uid:
        db_marked = DBDiscussionSession.query(MarkedArgument).filter(MarkedArgument.argument_uid == db_argument.uid,
                                                                     MarkedArgument.author_uid == author_uid).first()
        marked_element = db_marked is not None

    you_have_the_opinion_that = _t.get(_.youHaveTheOpinionThat).format('').strip()

    if lang == 'de':
        text = __build_single_argument_for_de(_t, sb, se, you_have_the_opinion_that, start_with_intro,
                                              anonymous_style, rearrange_intro, db_argument, attack_type, sb_none,
                                              marked_element, premises_text, conclusion_text,
                                              is_users_opinion,
                                              support_counter_argument)
    else:
        text = __build_single_argument_for_en(_t, sb, se, you_have_the_opinion_that, marked_element,
                                              conclusion_text,
                                              premises_text, db_argument)
    return text.replace('  ', ' ')


def __get_tags_for_building_single_argument(with_html_tag, attack_type, colored_position, premises, conclusion):
    if attack_type in ['dont_know', 'jump']:
        return __get_tags_for_building_single_unknown_argument(with_html_tag, premises, conclusion)
    else:
        return __get_tags_for_building_single_user_argument(with_html_tag, premises, conclusion, colored_position,
                                                            attack_type)


def __get_tags_for_building_single_unknown_argument(with_html_tag, premises, conclusion):
    sb = start_argument if with_html_tag else ''
    sb_tmp = start_attack if with_html_tag else ''
    sb_none = start_tag if with_html_tag else ''
    se = end_tag if with_html_tag else ''
    premises = sb + premises + se
    conclusion = sb_tmp + conclusion + se

    return {
        'premise': premises,
        'conclusion': conclusion,
        'tag_begin': sb,
        'tag_none': sb_none,
        'tag_end': se
    }


def __get_tags_for_building_single_user_argument(with_html_tag, premises, conclusion, colored_position, attack_type):
    sb_none = start_tag if with_html_tag else ''
    se = end_tag if with_html_tag else ''
    sb = start_tag if with_html_tag else ''
    if colored_position:
        sb = start_position if with_html_tag else ''

    if attack_type == Relations.UNDERMINE:
        premises = sb + premises + se
    else:
        conclusion = sb + conclusion + se

    return {
        'premise': premises,
        'conclusion': conclusion,
        'tag_begin': sb,
        'tag_none': sb_none,
        'tag_end': se
    }


def __build_single_argument_for_de(_t: Translator, sb: str, se: str, you_have_the_opinion_that: str,
                                   start_with_intro: bool, anonymous_style: bool, rearrange_intro: bool,
                                   db_argument: Argument, attack_type: str, sb_none: str, marked_element, premises: str,
                                   conclusion: str, is_users_opinion: bool, support_counter_argument) -> str:
    if start_with_intro and not anonymous_style:
        intro = _t.get(_.itIsTrueThat) if db_argument.is_supportive else _t.get(_.itIsFalseThat)
        if rearrange_intro:
            intro = _t.get(_.itTrueIsThat) if db_argument.is_supportive else _t.get(_.itFalseIsThat)

        text = (sb_none if attack_type in ['dont_know'] else sb) + intro + se + ' '

    elif is_users_opinion and not anonymous_style:
        text = sb_none
        if support_counter_argument:
            text += _t.get(_.youAgreeWithThecounterargument)
        elif marked_element:
            text += you_have_the_opinion_that
        else:
            text += _t.get(_.youArgue)
        text += se + ' '
    else:
        tmp = _t.get(_.itIsTrueThatAnonymous if db_argument.is_supportive else _.itIsFalseThatAnonymous)
        text = sb_none + sb + tmp + se + ' '

    text += f' {sb}{_t.get(_.itIsNotRight)}{se} ' if not db_argument.is_supportive else ''
    text += f'{conclusion}, {sb_none}{_t.get(_.because).lower()}{se} {premises}'
    return text


def __build_single_argument_for_en(_t: Translator, sb: str, se: str, you_have_the_opinion_that: str, marked_element,
                                   conclusion: str, premises: str, argument: Argument):
    tmp = sb + ' ' + _t.get(_.isNotRight).lower() + se + ', ' + _t.get(_.because).lower() + ' '
    text = (you_have_the_opinion_that + ' ' if marked_element else '') + conclusion + ' '
    text += _t.get(_.because).lower() if argument.is_supportive else tmp
    text += ' ' + premises
    return text


def __build_nested_argument(arg_array: List[Argument], first_arg_by_user, user_changed_opinion, with_html_tag,
                            start_with_intro, minimize_on_undercut, anonymous_style, premisegroup_by_user, _t):
    """

    :param arg_array:
    :param first_arg_by_user:
    :param user_changed_opinion:
    :param with_html_tag:
    :param start_with_intro:
    :param minimize_on_undercut:
    :param anonymous_style:
    :param premisegroup_by_user:
    :param _t:
    :return:
    """
    # get all pgroups and at last, the conclusion
    pgroups = []
    supportive = []
    arg_array = arg_array[::-1]
    local_lang = arg_array[0].lang

    # grepping all arguments in the chain
    for db_argument in arg_array:
        text = db_argument.get_premisegroup_text()

        pgroups.append(text)
        supportive.append(db_argument.is_supportive)

    conclusion = arg_array[0].get_conclusion_text()

    # html tags for framing
    sb = start_position if with_html_tag else ''
    se = end_tag if with_html_tag else ''

    because = (', ' if local_lang == 'de' else ' ') + _t.get(_.because).lower() + ' '

    if len(arg_array) % 2 == 0 and not first_arg_by_user and not anonymous_style:  # system starts
        ret_value = _t.get(_.earlierYouArguedThat if user_changed_opinion else _.otherUsersSaidThat) + ' '
        tmp_users_opinion = True  # user after system

    elif not anonymous_style:  # user starts
        ret_value = (_t.get(_.soYourOpinionIsThat) + ': ') if start_with_intro else ''
        tmp_users_opinion = False  # system after user
        conclusion = se + start_with_capital(conclusion)  # pretty print

    else:
        ret_value = _t.get(_.someoneArgued) + ' '
        tmp_users_opinion = False

    tmp = _t.get(_.itFalseIsThat) + ' ' if not supportive[0] else ''
    ret_value += tmp + conclusion + because + pgroups[0] + '.'
    del pgroups[0]

    # just display the last premise group on undercuts, because the story is always saved in all bubbles
    if minimize_on_undercut and not user_changed_opinion and len(pgroups) > 2:
        return _t.get(_.butYouCounteredWith).strip() + ' ' + sb + pgroups[len(pgroups) - 1] + se + '.'

    for i, pgroup in enumerate(pgroups):
        ret_value += ' '
        if tmp_users_opinion and not anonymous_style:
            tmp = _.butYouCounteredWithArgument if premisegroup_by_user else _.butYouCounteredWithInterest
            ret_value += _t.get(_.otherParticipantsConvincedYouThat if user_changed_opinion else tmp)
        elif not anonymous_style:
            ret_value += _t.get(_.youAgreeWithThatNow)
        else:
            ret_value += _t.get(_.otherUsersSaidThat) if i == 0 else _t.get(_.thenOtherUsersSaidThat)

        ret_value += sb + ' ' + pgroups[i] + '.'
        tmp_users_opinion = not tmp_users_opinion

    return ret_value.replace('  ', ' ')


def get_text_for_premisegroup_uid(uid):
    """
    Returns joined text of the premise group and the premise ids

    :param uid: premisegroup_uid
    :return: text, uids
    """
    warnings.warn("Use PremiseGroup.get_text() instead.", DeprecationWarning)

    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=uid).join(Statement).all()
    if len(db_premises) == 0:
        return ''
    texts = [premise.get_text() for premise in db_premises]
    lang = DBDiscussionSession.query(Statement).get(db_premises[0].statement.uid).lang
    _t = Translator(lang)

    return ' {} '.format(_t.get(_.aand)).join(texts)


def get_text_for_statement_uid(uid: int, colored_position=False) -> Optional[str]:
    """
    Returns text of statement with given uid

    :param uid: Statement.uid
    :param colored_position: Boolean
    :return: String
    """
    warnings.warn("Use Statement.get_text() or Statement.get_html() instead.", DeprecationWarning)

    if not isinstance(uid, int):
        return None
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    if not db_statement:
        return None

    content = db_statement.get_text()

    while content.endswith(('.', '?', '!')):
        content = content[:-1]

    sb, se = '', ''
    if colored_position:
        sb = f'<{tag_type} data-argumentation-type="position">'
        se = f'</{tag_type}>'

    return sb + content + se


def get_text_for_conclusion(argument, start_with_intro=False, rearrange_intro=False, is_users_opinion=True):
    """
    Check the arguments conclusion whether it is an statement or an argument and returns the text

    :param argument: Argument
    :param start_with_intro: Boolean
    :param rearrange_intro: Boolean
    :return: String
    """
    if argument.argument_uid:
        return get_text_for_argument_uid(argument.argument_uid, start_with_intro, rearrange_intro=rearrange_intro,
                                         is_users_opinion=is_users_opinion)
    else:
        return argument.get_conclusion_text()


def get_all_attacking_arg_uids_from_history(history):
    """
    Returns all arguments of the history, which attacked the user

    :param history: String
    :return: [Arguments.uid]
    :rtype: list
    """
    try:
        splitted_history = history.split('-')
        uids = []
        for part in splitted_history:
            if 'reaction' in part:
                parts = part.split('/')
                pos = parts.index('reaction')
                uids.append(part.split('/')[pos + 3])
        return uids
    except AttributeError:
        return []


def get_user_by_private_or_public_nickname(nickname):
    """
    Gets the user by his (public) nickname, based on the option, whether his nickname is public or not

    :param nickname: Nickname of the user
    :return: Current user or None
    """
    db_user = get_user_by_case_insensitive_nickname(nickname)
    db_public_user = get_user_by_case_insensitive_public_nickname(nickname)
    uid = 0

    if db_user:
        uid = db_user.uid
    elif db_public_user:
        uid = db_public_user.uid

    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=uid).first()

    if not db_settings:
        return None

    if db_settings.should_show_public_nickname and db_user:
        return db_user
    elif not db_settings.should_show_public_nickname and db_public_user:
        return db_public_user

    return None


def get_user_by_case_insensitive_nickname(nickname):
    """
    Returns user with given nickname

    :param nickname: String
    :return: User or None
    """
    return DBDiscussionSession.query(User).filter(func.lower(User.nickname) == func.lower(nickname)).first()


def get_user_by_case_insensitive_public_nickname(public_nickname):
    """
    Returns user with given public nickname

    :param public_nickname: String
    :return: User or None
    """
    return DBDiscussionSession.query(User).filter(
        func.lower(User.public_nickname) == func.lower(public_nickname)).first()


def pretty_print_options(message):
    """
    Some modifications for pretty printing.
    Use uppercase for first letter in text and a single dot for the end if there isn't one already.

    :param message: String
    :return:  String
    """

    # check for html
    if message[0:1] == '<':
        pos = message.index('>')
        message = message[0:pos + 1] + message[pos + 1:pos + 2].upper() + message[pos + 2:]
    else:
        message = start_with_capital(message)

    # check for html
    if message[-1] == '>':
        pos = message.rfind('<')
        if message[pos - 1] not in ['.', '?', '!']:
            message = message[0:pos] + '.' + message[pos:]
    elif not message.endswith(tuple(['.', '?', '!'])) and id != 'now':
        message += '.'

    return message


def create_speechbubble_dict(bubble_type: BubbleTypes, is_markable: bool = False, is_author: bool = False,
                             uid: str = '', bubble_url: str = '', content: str = '', omit_bubble_url: bool = False,
                             omit_vote_info: bool = False, argument_uid: int = None, statement_uid: int = None,
                             is_supportive: bool = False, db_user: User = None, lang: str = 'en',
                             is_users_opinion: bool = False, other_author: User = None):
    """
    Creates an dictionary which includes every information needed for a bubble.

    :param bubble_type: BubbleTypes
    :param is_markable: True if the content itself could be flagged
    :param is_author: True if the current user is author of the content
    :param uid: Identifier for the bubble
    :param bubble_url: URL for the click event of the bubble
    :param content: Text of the bubble
    :param omit_bubble_url: True if the bubble should have a link
    :param omit_vote_info: True if the bubble have the little, grey information text
    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :param db_user: current
    :param omit_bubble_url: Boolean
    :param lang: is_users_opinion
    :param is_users_opinion: Boolean
    :param other_author:
    :return: dict()
    """
    gravatar_link = get_global_url() + '/static/images/icon.png'
    profile = None

    is_enemy_user = {
        'admin': False,
        'author': False,
        'special': False
    }

    if uid != 'now':
        content = pretty_print_options(content)

    if bubble_type is BubbleTypes.SYSTEM and other_author is not None:
        gravatar_link = get_profile_picture(other_author, 25)
        profile = '/user/{}'.format(other_author.uid),
        is_enemy_user['admin'] = other_author.is_admin()
        is_enemy_user['author'] = other_author.is_author()
        is_enemy_user['special'] = other_author.is_special()

    # check for users opinion
    if bubble_type is BubbleTypes.USER and db_user and db_user.nickname != nick_of_anonymous_user:
        db_marked = None
        gravatar_link = get_profile_picture(db_user, 25)
        if argument_uid is not None and db_user is not None:
            db_marked = DBDiscussionSession.query(MarkedArgument).filter(
                MarkedArgument.argument_uid == argument_uid,
                MarkedArgument.author_uid == db_user.uid).first()

        if statement_uid is not None and db_user is not None:
            db_marked = DBDiscussionSession.query(MarkedStatement).filter(
                MarkedStatement.statement_uid == statement_uid,
                MarkedStatement.author_uid == db_user.uid).first()

        is_users_opinion = db_marked is not None

    speech = {
        'is_user': bubble_type is BubbleTypes.USER,
        'is_system': bubble_type is BubbleTypes.SYSTEM,
        'is_status': bubble_type is BubbleTypes.STATUS,
        'is_info': bubble_type is BubbleTypes.INFO,
        'is_markable': is_markable,
        'is_author': is_author,
        'is_enemy_user': is_enemy_user,
        'id': uid if len(str(uid)) > 0 else uuid4().hex,
        'bubble_url': bubble_url,
        'message': content,
        'omit_bubble_url': omit_bubble_url,
        'omit_vote_info': omit_vote_info,
        'data_type': 'argument' if argument_uid else 'statement' if statement_uid else 'None',
        'data_argument_uid': argument_uid,
        'data_statement_uid': statement_uid,
        'data_is_supportive': is_supportive,
        'is_users_opinion': is_users_opinion,
        'enemy': {
            'avatar': gravatar_link,
            'profile': profile,
            'available': profile is not None
        }
    }

    votecount_keys = __get_text_for_click_and_mark_count(db_user, bubble_type is BubbleTypes.USER, argument_uid,
                                                         statement_uid, speech, lang)

    speech['votecounts_message'] = votecount_keys[speech['votecounts']]

    return speech


def __get_text_for_click_and_mark_count(db_user: User, is_user: bool, argument_uid: int, statement_uid: int,
                                        speech: dict, lang: str):
    """
    Build text for a bubble, how many other participants have the same interest?

    :param nickname: User.nickname
    :param is_user: boolean
    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param speech: dict()
    :param lang: ui_locales
    :return: [String]
    """
    if not db_user:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    db_clicks, db_marks = __get_clicks_and_marks(argument_uid, statement_uid, db_user)

    _t = Translator(lang)
    speech['votecounts'] = len(db_clicks) if db_clicks else 0
    if db_marks:
        speech['votecounts'] += len(db_marks)

    votecount_keys = defaultdict(lambda: "{} {}.".format(speech['votecounts'], _t.get(_.voteCountTextMore)))

    if is_user and db_user.gender == 'm':
        gender_key = _.voteCountTextFirstM
    elif is_user and db_user.gender == 'f':
        gender_key = _.voteCountTextFirstF
    else:
        gender_key = _.voteCountTextFirst

    votecount_keys[0] = '{}.'.format(_t.get(gender_key))
    votecount_keys[1] = _t.get(_.voteCountTextOneOther) + '.'

    return votecount_keys


def __get_clicks_and_marks(argument_uid, statement_uid, db_user):
    db_clicks = None
    db_marks = None
    if argument_uid:
        db_clicks = DBDiscussionSession.query(ClickedArgument). \
            filter(ClickedArgument.argument_uid == argument_uid,
                   ClickedArgument.is_up_vote == True,
                   ClickedArgument.is_valid,
                   ClickedArgument.author_uid != db_user.uid).all()
        db_marks = DBDiscussionSession.query(MarkedArgument). \
            filter(MarkedArgument.argument_uid == argument_uid,
                   MarkedArgument.author_uid != db_user.uid).all()

    elif statement_uid:
        db_clicks = DBDiscussionSession.query(ClickedStatement). \
            filter(ClickedStatement.statement_uid == statement_uid,
                   ClickedStatement.is_up_vote == True,
                   ClickedStatement.is_valid,
                   ClickedStatement.author_uid != db_user.uid).all()
        db_marks = DBDiscussionSession.query(MarkedStatement). \
            filter(MarkedStatement.statement_uid == statement_uid,
                   MarkedStatement.author_uid != db_user.uid).all()

    return db_clicks, db_marks


def is_argument_disabled_due_to_disabled_statements(argument):
    """
    Returns true if any involved statement is disabled.

    :param argument: Argument
    :return: Boolean
    """
    if argument.conclusion_uid is None:
        # check conclusion of given arguments conclusion
        db_argument = DBDiscussionSession.query(Argument).get(argument.argument_uid)
        conclusion = DBDiscussionSession(Statement).get(db_argument.conclusion_uid)
        if conclusion.is_disabled:
            return True
        # check premisegroup of given arguments conclusion
        premises = __get_all_premises_of_argument(db_argument)
        for premise in premises:
            if premise.statement.is_disabled:
                return True
    else:
        # check conclusion of given argument
        conclusion = DBDiscussionSession.query(Statement).get(argument.conclusion_uid)
        if conclusion.is_disabled:
            return True

    # check premisegroup of given argument
    premises = __get_all_premises_of_argument(argument)
    for premise in premises:
        if premise.statement.is_disabled:
            return True

    return False


def is_author_of_statement(db_user: User, statement_uid: int) -> bool:
    """
    Is the user with given nickname author of the statement?

    :param db_user: User
    :param statement_uid: Statement.uid
    :return: Boolean
    """
    db_user = db_user if db_user and db_user.nickname != nick_of_anonymous_user else None
    if not db_user:
        return False

    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).order_by(
        TextVersion.uid.asc()).first()
    if not db_textversion:
        return False
    return db_textversion.author_uid == db_user.uid


def is_author_of_argument(db_user: User, argument_uid: int) -> bool:
    """
    Is the user with given nickname author of the argument?

    :param db_user: User
    :param argument_uid: Argument.uid
    :return: Boolean
    """
    db_user = db_user if db_user and db_user.nickname != nick_of_anonymous_user else None
    if not db_user:
        return False
    db_argument = DBDiscussionSession.query(Argument).filter(Argument.uid == argument_uid,
                                                             Argument.author_uid == db_user.uid).first()
    return True if db_argument else False


def __get_all_premises_of_argument(argument):
    """
    Returns list with all premises of the argument.

    :param argument: Argument
    :return: list()
    """
    ret_list = []
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=argument.premisegroup_uid).join(
        Statement).all()
    for premise in db_premises:
        ret_list.append(premise)
    return ret_list


def get_profile_picture(user: User, size: int = 80, ignore_privacy_settings: bool = False) -> str:
    """
    Returns the user's profile picture with the specified size.

    :param user: User
    :param size: Integer, default 80
    :param ignore_privacy_settings:
    :return: String
    """
    if user:
        additional_id = '' if user.settings.should_show_public_nickname or ignore_privacy_settings else 'x'
        email = (user.email + additional_id).encode('utf-8')
    else:
        email = str(randint(0, 999999)).encode('utf-8')

    gravatar_url = 'https://secure.gravatar.com/avatar/{}?'.format(hashlib.md5(email.lower()).hexdigest())
    gravatar_url += parse.urlencode({'d': 'identicon', 's': str(size)})
    return gravatar_url


def get_author_data(uid, gravatar_on_right_side=True, linked_with_users_page=True, profile_picture_size=20):
    """
    Returns a-tag with gravatar of current author and users page as href

    :param uid: Uid of the author
    :param gravatar_on_right_side: True, if the gravatar is on the right of authors name
    :param linked_with_users_page: True, if the text is a link to the authors site
    :param profile_picture_size: Integer
    :return: HTML-String
    """
    db_user = DBDiscussionSession.query(User).get(int(uid))
    if not db_user:
        return None, 'Missing author with uid ' + str(uid), False

    nick = db_user.global_nickname
    img_src = get_profile_picture(db_user, profile_picture_size)
    link_begin = ''
    link_end = ''
    if linked_with_users_page:
        link_begin = '<a href="/user/{}" title="{}">'.format(db_user.uid, nick)
        link_end = '</a>'

    side = 'left' if gravatar_on_right_side else 'right'
    img = '<img class="img-circle" src="{}" style="padding-{}: 0.3em">'.format(img_src, side)

    if gravatar_on_right_side:
        return db_user, '{}{}{}{}'.format(link_begin, nick, img, link_end), True
    else:
        return db_user, '{}{}{}{}'.format(link_begin, img, nick, link_end), True


def bubbles_already_last_in_list(bubble_list, bubbles):
    """
    Are the given bubbles already at the end of the bubble list

    :param bubble_list: list of Bubbles
    :param bubbles:  list of bubbles
    :return: Boolean
    """
    if isinstance(bubbles, list):
        length = len(bubbles)
    else:
        length = 1
        bubbles = [bubbles]

    if len(bubble_list) < length:
        return False

    for bubble in bubbles:
        if 'message' not in bubble:
            return False

    start_index = - length
    is_already_in = False
    for bubble in bubbles:

        last = bubble_list[start_index]
        if 'message' not in last or 'message' not in bubble:
            return False

        text1 = unhtmlify(last['message'].lower()).strip()
        text2 = unhtmlify(bubble['message'].lower()).strip()
        is_already_in = is_already_in or (text1 == text2)
        start_index += 1

    return is_already_in


def unhtmlify(html):
    """
    Remove html-tags and unescape encoded html-entities.

    :param html: Evil-string containing html
    :return:
    """
    return unescape(re.sub(r'<.*?>', '', html))


def get_enabled_statement_as_query():
    """
    Returns query with all statements, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Statement).filter_by(is_disabled=False)


def get_enabled_arguments_as_query():
    """
    Returns query with all arguments, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Argument).filter_by(is_disabled=False)


def get_enabled_premises_as_query():
    """
    Returns query with all premises, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Premise).filter_by(is_disabled=False)


def get_enabled_issues_as_query():
    """
    Returns query with all issues, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Issue).filter_by(is_disabled=False)


def checks_if_user_is_ldap_user(db_user: User) -> bool:
    """
    Checks if user is ldap user

    :param db_user
    :return:
    """

    pw_for_ldap_user = 'NO_PW_BECAUSE_LDAP'
    return db_user.validate_password(pw_for_ldap_user)
