"""
Common, pure functions used by the D-BAS.


.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import hashlib
import locale
import time
import os

import requests

from collections import defaultdict
from datetime import datetime
from html import escape
from urllib import parse

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Premise, Statement, TextVersion, Issue, Language, User, Settings, \
    VoteArgument, VoteStatement, Group
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from sqlalchemy import and_, func
from dbas.logger import logger

fallback_lang = 'en'
tag_type = 'span'


def get_global_url():
    """
    Returns the global url of the project.
    Important: the global url has to be in setup.py like "url='http://foo.bar'"

    :return: String
    """
    path = str(os.path.realpath(__file__ + '/../../setup.py'))
    lines = [line.rstrip('\n').strip() for line in open(path)]

    return str([l[l.index('htt'):-2] for l in lines if 'url=' in l][0])


def get_changelog(no):
    """
    Returns the c last entries from the changelog

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
            title = l.replace('## ', '')
        else:
            body.append(l.replace('- ', ''))

    return changelog[0:no]


def is_usage_with_ldap(request):
    """

    :return:
    """
    if 'settings:ldap:usage' in request.registry.settings:
        return True if request.registry.settings['settings:ldap:usage'] == 'true' else False
    return False


def escape_string(text):
    """
    Escapes all html special chars.

    :param text: string
    :return: html.escape(text)
    """
    return escape(text)


def get_language(request):
    """
    Returns current ui locales code which is saved in current cookie or the registry.

    :param request: request
    :param current_registry: get_current_registry()
    :return: ui_locales
    """
    try:
        lang = request.cookies['_LOCALE_']
    except (KeyError, AttributeError):
        lang = request.registry.settings['pyramid.default_locale_name']
    return str(lang)


def get_discussion_language(request, current_issue_uid=1):
    """
    Returns Language.ui_locales
    CALL AFTER issue_helper.get_id_of_slug(..)!

    :param request: self.request
    :return:
    """
    # first matchdict, then params, then session, afterwards fallback
    issue = request.matchdict['issue'] if 'issue' in request.matchdict \
        else request.params['issue'] if 'issue' in request.params \
        else request.session['issue'] if 'issue' in request.session \
        else current_issue_uid

    db_lang = DBDiscussionSession.query(Issue).filter_by(uid=issue).join(Language).first()

    return db_lang.languages.ui_locales if db_lang else 'en'


def python_datetime_pretty_print(ts, lang):
    """


    :param ts:
    :param lang:
    :return:
    """
    formatter = '%d. %b.'
    if lang == 'de':
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
            formatter = '%b. %Y'
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

    return datetime.strptime(str(ts), '%Y-%m-%d').strftime(formatter)


def get_all_arguments_by_statement(statement_uid, include_disabled=False):
    """
    Returns a list of all arguments where the statement is a conclusion or member of the premisegroup

    :param statement_uid: Statement.uid
    :param include_disabled: Boolean
    :return: [Arguments]
    """
    logger('DBAS.LIB', 'get_all_arguments_by_statement', 'main ' + str(statement_uid))
    db_arguments = DBDiscussionSession.query(Argument).filter_by(
        is_disabled=include_disabled,
        conclusion_uid=statement_uid
    ).all()

    premises = DBDiscussionSession.query(Premise).filter_by(
        is_disabled=include_disabled,
        statement_uid=statement_uid
    ).all()

    return_array = [arg for arg in db_arguments] if db_arguments else []

    for premise in premises:
        db_arguments = DBDiscussionSession.query(Argument).filter_by(is_disabled=include_disabled,
                                                                     premisesgroup_uid=premise.premisesgroup_uid).all()
        if db_arguments:
            return_array = return_array + db_arguments

    logger('DBAS.LIB', 'get_all_arguments_by_statement', 'returning arguments ' + str([arg.uid for arg in return_array]))
    return return_array if len(return_array) > 0 else None


def get_text_for_argument_uid(uid, with_html_tag=False, start_with_intro=False, first_arg_by_user=False,
                              user_changed_opinion=False, rearrange_intro=False, colored_position=False,
                              attack_type=None, minimize_on_undercut=False, is_users_opinion=True, anonymous_style=False):
    """
    Returns current argument as string like "conclusion, because premise1 and premise2"

    :param uid: Integer
    :param with_html_tag: Boolean
    :param start_with_intro: Boolean
    :param first_arg_by_user: Boolean
    :param user_changed_opinion: Boolean
    :param rearrange_intro: Boolean
    :param colored_position: Boolean
    :param attack_type: String
    :param minimize_on_undercut: Boolean
    :param anonymous_style: Boolean
    :return: String
    """
    logger('DBAS.LIB', 'get_text_for_argument_uid', 'main ' + str(uid))
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    if not db_argument:
        return None

    lang = db_argument.lang
    # catch error

    _t = Translator(lang)

    # getting all argument id
    arg_array = [db_argument.uid]
    while db_argument.argument_uid:
        db_argument = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)
        arg_array.append(db_argument.uid)

    if attack_type == 'jump':
        return __build_argument_for_jump(arg_array, with_html_tag)

    if len(arg_array) == 1:
        # build one argument only
        return __build_single_argument(arg_array[0], rearrange_intro, with_html_tag, colored_position, attack_type, _t,
                                       start_with_intro, is_users_opinion, anonymous_style)

    else:
        # get all pgroups and at last, the conclusion
        sb = '<' + tag_type + '>' if with_html_tag else ''
        se = '</' + tag_type + '>' if with_html_tag else ''
        doesnt_hold_because = ' ' + se + _t.get(_.doesNotHold).lower() + ' ' + _t.get(_.because).lower() + ' ' + sb
        return __build_nested_argument(arg_array, first_arg_by_user, user_changed_opinion, with_html_tag,
                                       start_with_intro, doesnt_hold_because, minimize_on_undercut, anonymous_style, _t)


def get_all_arguments_with_text_by_statement_id(statement_uid):
    """
    Given a statement_uid, it returns all arguments, which use this statement and adds
    the corresponding text to it, which normally appears in the bubbles. The resulting
    text depends on the provided language.

    :param statement_uid: uid to a statement, which should be analyzed
    :return: list of dictionaries containing some properties of these arguments
    :rtype: list
    """
    logger('DBAS.LIB', 'get_all_arguments_with_text_by_statement_id', 'main ' + str(statement_uid))
    arguments = get_all_arguments_by_statement(statement_uid)
    results = list()
    if arguments:
        for argument in arguments:
            results.append({'uid': argument.uid,
                            'text': get_text_for_argument_uid(argument.uid)})
        return results


def get_all_arguments_with_text_and_url_by_statement_id(statement_uid, urlmanager, color_statement=False):
    """
    Given a statement_uid, it returns all arguments, which use this statement and adds
    the corresponding text to it, which normally appears in the bubbles. The resulting
    text depends on the provided language.

    :param statement_uid: Id to a statement, which should be analyzed
    :param color_statement: True, if the statement (specified by the ID) should be colored
    :return: list of dictionaries containing some properties of these arguments
    :rtype: list
    """
    logger('DBAS.LIB', 'get_all_arguments_with_text_by_statement_id', 'main ' + str(statement_uid))
    arguments = get_all_arguments_by_statement(statement_uid)
    results = list()
    sb = '<{} data-argumentation-type="position">'.format(tag_type) if color_statement else ''
    se = '</{}>'.format(tag_type) if color_statement else ''
    if arguments:
        for argument in arguments:
            statement_text = get_text_for_statement_uid(statement_uid)
            argument_text = get_text_for_argument_uid(argument.uid, anonymous_style=True)
            pos = argument_text.lower().find(statement_text.lower())
            argument_text = argument_text[0:pos] + sb + argument_text[pos:pos + len(statement_text)] + se + argument_text[pos + len(statement_text):]
            results.append({'uid': argument.uid,
                            'text': argument_text,
                            'url': urlmanager.get_url_for_jump(False, argument.uid)})
        return results


def get_slug_by_statement_uid(uid):
    """

    :param uid:
    :return:
    """
    db_statement = DBDiscussionSession.query(Statement).get(uid)
    return resolve_issue_uid_to_slug(db_statement.issue_uid)


def __build_argument_for_jump(arg_array, with_html_tag):
    """

    :param arg_array:
    :param with_html_tag:
    :return:
    """
    tag_premise = ('<' + tag_type + ' data-argumentation-type="argument">') if with_html_tag else ''
    tag_conclusion = ('<' + tag_type + ' data-argumentation-type="attack">') if with_html_tag else ''
    tag_end = ('</' + tag_type + '>') if with_html_tag else ''
    lang = DBDiscussionSession.query(Argument).get(arg_array[0]).lang
    _t = Translator(lang)

    if len(arg_array) == 1:
        db_argument = DBDiscussionSession.query(Argument).get(arg_array[0])
        premises, uids = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        conclusion = get_text_for_statement_uid(db_argument.conclusion_uid)

        if lang == 'de':
            intro = _t.get(_.rebut1) if db_argument.is_supportive else _t.get(_.overbid1)
            ret_value = tag_conclusion + intro[0:1].upper() + intro[1:] + ' ' + conclusion + tag_end
            ret_value += ' ' + _t.get(_.because).lower() + ' ' + tag_premise + premises + tag_end
        else:
            ret_value = tag_conclusion + conclusion + ' ' + (
                _t.get(_.isNotRight).lower() if not db_argument.is_supportive else '') + tag_end
            ret_value += ' ' + _t.get(_.because).lower() + ' '
            ret_value += tag_premise + premises + tag_end

    else:
        db_argument = DBDiscussionSession.query(Argument).get(arg_array[1])
        conclusions_premises, uids = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        if db_argument.conclusion_uid:
            conclusions_conclusion = get_text_for_statement_uid(db_argument.conclusion_uid)
        else:
            conclusions_conclusion = get_text_for_argument_uid(db_argument.argument_uid)

        db_argument = DBDiscussionSession.query(Argument).get(arg_array[0])
        premises, uids = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)

        ret_value = tag_conclusion + conclusions_premises + ' '
        ret_value += _t.get(_.doesNotJustify) + ' '
        ret_value += conclusions_conclusion + tag_end + ' '
        ret_value += _t.get(_.because).lower() + ' ' + tag_premise + premises + tag_end

    return ret_value


def __build_single_argument(uid, rearrange_intro, with_html_tag, colored_position, attack_type, _t, start_with_intro,
                            is_users_opinion, anonymous_style):
    """

    :param uid:
    :param rearrange_intro:
    :param with_html_tag:
    :param colored_position:
    :param attack_type:
    :param _t:
    :param start_with_intro:
    :return:
    """
    logger('DBAS.LIB', '__build_single_argument', 'main ' + str(uid))
    db_argument = DBDiscussionSession.query(Argument).get(uid)
    premises, uids = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
    conclusion = get_text_for_statement_uid(db_argument.conclusion_uid)
    lang = DBDiscussionSession.query(Argument).get(uid).lang

    if lang != 'de':
        # conclusion = conclusion[0:1].lower() + conclusion[1:]  # pretty print
        premises = premises[0:1].lower() + premises[1:]  # pretty print

    sb_tmp = ''
    sb_none = '<' + tag_type + '>'
    se = '</' + tag_type + '>' if with_html_tag else ''
    if attack_type not in ['dont_know', 'jump']:
        sb = '<' + tag_type + '>' if with_html_tag else ''
        if colored_position:
            sb = '<' + tag_type + ' data-argumentation-type="position">' if with_html_tag else ''
    else:
        sb = '<' + tag_type + ' data-argumentation-type="argument">'
        sb_tmp = '<' + tag_type + ' data-argumentation-type="attack">'

    # color_everything = attack_type == 'undercut' and False
    if attack_type not in ['dont_know', 'jump']:
        if attack_type == 'undermine':
            premises = sb + premises + se
        else:
            conclusion = sb + conclusion + se
    else:
        premises = sb + premises + se
        conclusion = sb_tmp + conclusion + se

    if lang == 'de':
        if start_with_intro and not anonymous_style:
            if rearrange_intro:
                intro = _t.get(_.itTrueIsThat) if db_argument.is_supportive else _t.get(_.itFalseIsThat)
            else:
                intro = _t.get(_.itIsTrueThat) if db_argument.is_supportive else _t.get(_.itIsFalseThat)

            ret_value = (sb_none if attack_type in ['dont_know'] else sb) + intro + se + ' '
        elif is_users_opinion and not anonymous_style:
            ret_value = se + _t.get(_.youArgue) + se + ' '
        else:
            ret_value = se + _t.get(_.itIsTrueThatAnonymous if db_argument.is_supportive else _.itIsFalseThatAnonymous) + se + ' '
        ret_value += conclusion
        ret_value += (', ' + _t.get(_.itIsNotRight)) if not db_argument.is_supportive else ''
        ret_value += ', ' if lang == 'de' else ' '
        ret_value += sb_none + _t.get(_.because).lower() + se + ' ' + premises
    else:
        tmp = sb + ' ' + _t.get(_.isNotRight).lower() + se + ', ' + _t.get(_.because).lower() + ' '
        ret_value = conclusion + ' '
        ret_value += _t.get(_.because).lower() if db_argument.is_supportive else tmp
        ret_value += ' ' + premises

    # if color_everything:
    #     return sb + ret_value + se
    # else:
    return ret_value


def __build_nested_argument(arg_array, first_arg_by_user, user_changed_opinion, with_html_tag, start_with_intro,
                            doesnt_hold_because, minimize_on_undercut, anonymous_style, _t):
    """

    :param arg_array:
    :param first_arg_by_user:
    :param user_changed_opinion:
    :param with_html_tag:
    :param start_with_intro:
    :param doesnt_hold_because:
    :param minimize_on_undercut:
    :param _t:
    :param anonymous_style:
    :return:
    """
    logger('DBAS.LIB', '__build_nested_argument', 'main ' + str(arg_array))

    # get all pgroups and at last, the conclusion
    pgroups = []
    supportive = []
    arg_array = arg_array[::-1]
    local_lang = DBDiscussionSession.query(Argument).get(arg_array[0]).lang

    # grepping all arguments in the chain
    for uid in arg_array:
        db_argument = DBDiscussionSession.query(Argument).get(uid)
        text, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)

        pgroups.append(text)
        supportive.append(db_argument.is_supportive)

    uid = DBDiscussionSession.query(Argument).get(arg_array[0]).conclusion_uid
    conclusion = get_text_for_statement_uid(uid)

    # html tags for framing
    sb = '<{} data-argumentation-type="position">'.format(tag_type) if with_html_tag else ''
    se = '</{}>'.format(tag_type) if with_html_tag else ''

    because = (', ' if local_lang == 'de' else ' ') + _t.get(_.because).lower() + ' '

    if len(arg_array) % 2 is 0 and not first_arg_by_user and not anonymous_style:  # system starts
        ret_value = _t.get(_.earlierYouArguedThat if user_changed_opinion else _.otherUsersSaidThat) + ' '
        tmp_users_opinion = True  # user after system

    elif not anonymous_style:  # user starts
        ret_value = (_t.get(_.soYourOpinionIsThat) + ': ') if start_with_intro else ''
        tmp_users_opinion = False  # system after user
        conclusion = se + conclusion[0:1].upper() + conclusion[1:]  # pretty print
    else:
        ret_value = _t.get(_.someoneArgued) + ' '
        tmp_users_opinion = False

    ret_value += conclusion + (because if supportive[0] else doesnt_hold_because) + pgroups[0] + '.'

    # just display the last premise group on undercuts, because the story is always saved in all bubbles
    if minimize_on_undercut and not user_changed_opinion and len(pgroups) > 2:
        return _t.get(_.butYouCounteredWith) + ' ' + sb + pgroups[len(pgroups) - 1] + se + '.'

    for i, pgroup in enumerate(pgroups):
        ret_value += ' '
        if tmp_users_opinion and not anonymous_style:
            ret_value += _t.get(_.otherParticipantsConvincedYouThat if user_changed_opinion else _.butYouCounteredWith)
        elif not anonymous_style:
            ret_value += _t.get(_.youAgreeWithThatNow)
        else:
            ret_value += _t.get(_.otherUsersSaidThat) if i == 0 else _t.get(_.thenOtherUsersSaidThat)

        ret_value += sb + ' ' + pgroups[i] + '.'
        tmp_users_opinion = not tmp_users_opinion

    return ret_value


def get_text_for_premisesgroup_uid(uid):
    """
    Returns joined text of the premise group and the premise ids

    :param uid: premisesgroup_uid
    :return: text, uids
    """
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=uid).join(Statement).all()
    uids = []
    texts = []
    if len(db_premises) > 0:
        lang = DBDiscussionSession.query(Statement).get(db_premises[0].statements.uid).lang
    else:
        return '', uids

    _t = Translator(lang)

    for premise in db_premises:
        tmp = get_text_for_statement_uid(premise.statements.uid)
        uids.append(str(premise.statements.uid))
        texts.append(str(tmp))

    return ' {} '.format(_t.get(_.aand)).join(texts), uids


def get_text_for_statement_uid(uid, colored_position=False):
    """
    Returns text of statement with given uid

    :param uid: Statement.uid
    :param colored_position: Boolean
    :return: String
    """
    try:
        if isinstance(int(uid), int):
            db_statement = DBDiscussionSession.query(Statement).get(uid)
            if not db_statement:
                return None

            db_textversion = DBDiscussionSession.query(TextVersion).order_by(TextVersion.uid.desc()).filter_by(
                uid=db_statement.textversion_uid).first()
            content = db_textversion.content

            while content.endswith(('.', '?', '!')):
                content = content[:-1]

            sb = '<' + tag_type + ' data-argumentation-type="position">' if colored_position else ''
            se = '</' + tag_type + '>' if colored_position else ''
            return sb + content + se

    except (ValueError, TypeError):
        return None


def get_text_for_premise(uid, colored_position=False):
    """
    Returns text of premise with given uid

    :param uid: Statement.uid
    :param colored_position: Boolean
    :return: String
    """
    db_premise = DBDiscussionSession.query(Premise).filter_by(uid).first()
    if db_premise:
        return get_text_for_statement_uid(db_premise.statement_uid, colored_position)
    else:
        return None


def get_text_for_conclusion(argument, start_with_intro=False, rearrange_intro=False, is_users_opinion=True):
    """
    Check the arguments conclusion whether it is an statement or an argument and returns the text

    :param argument: Argument
    :param lang: ui_locales
    :param start_with_intro: Boolean
    :param rearrange_intro: Boolean
    :return: String
    """
    if argument.argument_uid:
        return get_text_for_argument_uid(argument.argument_uid, start_with_intro, rearrange_intro=rearrange_intro, is_users_opinion=is_users_opinion)
    else:
        return get_text_for_statement_uid(argument.conclusion_uid)


def resolve_issue_uid_to_slug(uid):
    """
    Given the issue uid query database and return the correct slug of the issue.

    :param uid: issue_uid
    :type uid: int
    :return: Slug of issue
    :rtype: str
    """
    issue = DBDiscussionSession.query(Issue).get(uid)
    return issue.get_slug() if issue else None


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
                tmp = part.replace('/', 'X', 2).find('/') + 1
                uids.append(part[tmp])
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

    db_settings = None
    current_user = None

    if db_user:
        db_settings = DBDiscussionSession.query(Settings).get(db_user.uid)
    elif db_public_user:
        db_settings = DBDiscussionSession.query(Settings).get(db_public_user.uid)

    if db_settings:
        if db_settings.should_show_public_nickname and db_user:
            current_user = db_user
        elif not db_settings.should_show_public_nickname and db_public_user:
            current_user = db_public_user

    return current_user


def get_user_by_case_insensitive_nickname(nickname):
    """
    :param nickname:
    :return:
    """
    return DBDiscussionSession.query(User).filter(func.lower(User.nickname) == func.lower(nickname)).first()


def get_user_by_case_insensitive_public_nickname(public_nickname):
    """
    :param public_nickname:
    :return:
    """
    return DBDiscussionSession.query(User).filter(
        func.lower(User.public_nickname) == func.lower(public_nickname)).first()


def create_speechbubble_dict(is_user=False, is_system=False, is_status=False, is_info=False, is_flagable=False,
                             is_author=False, uid='', url='', message='', omit_url=False, argument_uid=None,
                             statement_uid=None, is_supportive=None, nickname='anonymous', lang='en'):
    """
    Creates an dictionary which includes every information needed for a bubble.

    :param is_user: Boolean
    :param is_system: Boolean
    :param is_status: Boolean
    :param is_info: Boolean
    :param is_flagable: Boolean
    :param uid: Argument.uid
    :param url: URL
    :param message: String
    :param omit_url: Boolean
    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param is_supportive: Boolean
    :param nickname: String
    :param lang: String
    :return: dict()
    """

    # check for html
    if message[0:1] == '<':
        pos = message.index('>')
        message = message[0:pos + 1] + message[pos + 1:pos + 2].upper() + message[pos + 2:]
    else:
        message = message[0:1].upper() + message[1:]

    # check for html
    if message[-1] == '>':
        pos = message.rfind('<')
        if message[pos - 1:pos] not in ['.', '?', '!']:
            message = message[0:pos] + '.' + message[pos:]
    else:
        if not message.endswith(tuple(['.', '?', '!'])):
            message += '.'

    speech = {'is_user': is_user,
              'is_system': is_system,
              'is_status': is_status,
              'is_info': is_info,
              'is_flagable': is_flagable,
              'is_author': is_author,
              'id': uid if len(str(uid)) > 0 else str(time.time()),
              'url': url if len(str(url)) > 0 else 'None',
              'message': message,
              'omit_url': omit_url,
              'data_type': 'argument' if argument_uid else 'statement' if statement_uid else 'None',
              'data_argument_uid': str(argument_uid), 'data_statement_uid': str(statement_uid),
              'data_is_supportive': str(is_supportive),
              # 'url': url if len(str(url)) > 0 else 'None'
              }
    db_votecounts = None

    if is_supportive is None:
        is_supportive = False

    if not nickname:
        nickname = 'anonymous'
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        db_user = DBDiscussionSession.query(User).filter_by(nickname='anonymous').first()

    if argument_uid:
        db_votecounts = DBDiscussionSession.query(VoteArgument). \
            filter(and_(VoteArgument.argument_uid == argument_uid,
                        VoteArgument.is_up_vote == is_supportive,
                        VoteArgument.is_valid,
                        VoteArgument.author_uid != db_user.uid)). \
            all()

    elif statement_uid:
        db_votecounts = DBDiscussionSession.query(VoteStatement). \
            filter(and_(VoteStatement.statement_uid == statement_uid,
                        VoteStatement.is_up_vote == is_supportive,
                        VoteStatement.is_valid,
                        VoteStatement.author_uid != db_user.uid)). \
            all()
    _t = Translator(lang)
    speech['votecounts'] = len(db_votecounts) if db_votecounts else 0

    votecount_keys = defaultdict(lambda: "{} {}.".format(speech['votecounts'], _t.get(_.voteCountTextMore)))
    votecount_keys[0] = _t.get(_.voteCountTextFirst) + '.'
    votecount_keys[1] = _t.get(_.voteCountTextOneOther) + '.'

    speech['votecounts_message'] = votecount_keys[speech['votecounts']]

    return speech


def is_user_author(nickname):
    """
    Check, if the given uid has admin rights or is admin

    :param nickname: current user name
    :return: true, if user is admin, false otherwise
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
    db_author_group = DBDiscussionSession.query(Group).filter_by(name='authors').first()
    #  logger('Lib', 'is_user_author', 'main')
    if db_user:
        if db_user.group_uid == db_author_group.uid or db_user.group_uid == db_admin_group.uid:
            return True

    return False


def is_user_admin(nickname):
    """
    Check, if the given uid has admin rights or is admin

    :param nickname: current user name
    :return: true, if user is admin, false otherwise
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    db_admin_group = DBDiscussionSession.query(Group).filter_by(name='admins').first()
    #  logger('Lib', 'is_user_author', 'main')
    return db_user and db_user.group_uid == db_admin_group.uid


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
            if premise.statements.is_disabled:
                return True
    else:
        # check conclusion of given argument
        conclusion = DBDiscussionSession(Statement).get(argument.conclusion_uid)
        if conclusion.is_disabled:
            return True

    # check premisegroup of given argument
    premises = __get_all_premises_of_argument(argument)
    for premise in premises:
        if premise.statements.is_disabled:
            return True

    return False


def is_author_of_statement(nickname, statement_uid):
    """

    :param nickname:
    :param statement_uid:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return False
    db_textversion = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).order_by(
        TextVersion.uid.asc()).first()
    if not db_textversion:
        return False
    return db_textversion.author_uid == db_user.uid


def is_author_of_argument(nickname, argument_uid):
    """

    :param nickname:
    :param argument_uid:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return False
    db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == argument_uid,
                                                                  Argument.author_uid == db_user.uid)).first()
    return True if db_argument else False


def __get_all_premises_of_argument(argument):
    """
    Returns list with all premises of the argument.

    :param argument: Argument
    :return: list()
    """
    ret_list = []
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).join(
        Statement).all()
    for premise in db_premises:
        ret_list.append(premise)
    return ret_list


def get_profile_picture(user, size=80, ignore_privacy_settings=False):
    """
    Returns the url to a https://secure.gravatar.com picture, with the option wavatar and size of 80px

    :param user: User
    :param size: Integer, default 80
    :param ignore_privacy_settings:
    :return: String
    """
    db_settings = DBDiscussionSession.query(Settings).get(user.uid)
    additional_id = '' if db_settings.should_show_public_nickname or ignore_privacy_settings else 'x'
    url = get_global_url()
    url = url[url.index('//') + 2:]
    unknown = 'unknown@' + url
    email = (user.email + additional_id).encode('utf-8') if user else unknown.encode('utf-8')

    gravatar_url = 'https://secure.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += parse.urlencode({'d': 'wavatar', 's': str(size)})
    return gravatar_url


def get_public_profile_picture(user, size=80):
    """
    Returns the url to a https://secure.gravatar.com picture, with the option wavatar and size of 80px
    If the user doesn want an public profile, an anoynmous image will be returned

    :param user: User
    :param size: Integer, default 80
    :return: String
    """
    if user:
        additional_id = '' if DBDiscussionSession.query(Settings).get(user.uid).should_show_public_nickname else 'x'
    else:
        additional_id = 'y'
    url = get_global_url()
    url = url[url.index('//') + 2:]
    email = (user.email + additional_id).encode('utf-8') if user else ('unknown@' + url).encode('utf-8')
    gravatar_url = 'https://secure.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += parse.urlencode({'d': 'wavatar', 's': str(size)})
    return gravatar_url


def get_author_data(main_page, uid, gravatar_on_right_side=True, linked_with_users_page=True, profile_picture_size=20):
    """
    Returns a-tag with gravatar of current author and users page as href

    :param main_page: Current mainpage
    :param uid: Uid of the author
    :param gravatar_on_right_side: True, if the gravatar is on the right of authors name
    :param linked_with_users_page: True, if the text is a link to the authors site
    :param profile_picture_size: Integer
    :return: HTML-String
    """
    db_user = DBDiscussionSession.query(User).get(int(uid))
    db_settings = DBDiscussionSession.query(Settings).get(int(uid))
    if not db_user:
        return 'Missing author with uid ' + str(uid), False
    if not db_settings:
        return 'Missing settings of author with uid ' + str(uid), False
    img = '<img class="img-circle" src="' + get_profile_picture(db_user, profile_picture_size, True) + '">'
    nick = db_user.get_global_nickname()
    link_begin = ('<a href="' + main_page + '/user/' + nick + ' " title="' + nick + '">') if linked_with_users_page else ''
    link_end = ('</a>') if linked_with_users_page else ''
    if gravatar_on_right_side:
        return link_begin + nick + ' ' + img + link_end, True
    else:
        return link_begin + img + ' ' + nick + link_end, True


def validate_recaptcha(recaptcha):
    logger('Lib', 'validate_recaptcha', 'recaptcha ' + str(recaptcha))
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': '6Lc0eQ4TAAAAAJBcq97lYwM8byadNWmUYuTZaPzz',
                                                                                   'response': recaptcha})
        json = r.json()
    except:
        logger('Lib', 'validate_recaptcha', 'Unexcepcted error', error=True)
        return False, True

    logger('Lib', 'validate_recaptcha', 'answer ' + str(json))
    error = False

    if 'missing-input-secret' in json['error-codes']:
        logger('Lib', 'validate_recaptcha', 'The secret parameter is missing.', error=True)
        error = True
    if 'invalid-input-secret' in json['error-codes']:
        logger('Lib', 'validate_recaptcha', 'The secret parameter is invalid or malformed.', error=True)
        error = True
    if 'missing-input-response' in json['error-codes']:
        logger('Lib', 'validate_recaptcha', 'The response parameter is missing.', error=True)
        error = True
    if 'invalid-input-response' in json['error-codes']:
        logger('Lib', 'validate_recaptcha', 'The response parameter is invalid or malformed.', error=True)
        error = True

    return json['success'], error
