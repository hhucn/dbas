#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ClickedStatement, ClickedArgument, User, MarkedArgument, MarkedStatement
from dbas.lib import get_author_data
from .keywords import Keywords as _
from .translator import Translator

nick_of_anonymous_user = 'anonymous'

tag_type = 'span'


def get_text_for_add_premise_container(lang, confrontation, premise, attack_type, conclusion, is_supportive):
    """
    Based on the users reaction, text will be build. This text can be used for the container where users can
    add their statements

    :param lang: ui_locales
    :param confrontation: chosen confrontation
    :param premise: current premise
    :param attack_type: type of the attack
    :param conclusion: current conclusion
    :param is_supportive: boolean
    :return: string
    """
    _t = Translator(lang)

    if premise[-1] == '.':
        premise = premise[:-1]

    if conclusion[-1] == '.':
        conclusion = premise[:-1]

    confrontation = confrontation[0:1].upper() + confrontation[1:]

    # different cases
    ret_text = ''
    if attack_type == 'undermine':
        ret_text = _t.get(_.itIsFalseThat) + ' ' + premise
    if attack_type == 'support':
        ret_text = _t.get(_.itIsTrueThat) if is_supportive else _t.get(_.itIsFalseThat)
        ret_text += ' ' + conclusion + ' '
        ret_text += _t.get(_.hold) if is_supportive else _t.get(_.doesNotHold)
    if attack_type == 'undercut':
        ret_text = confrontation + ', ' + _t.get(_.butIDoNotBelieveCounterFor).format(conclusion)
    if attack_type == 'overbid':
        ret_text = confrontation + ', ' + _t.get(_.andIDoBelieveCounterFor) + ' ' + conclusion
    # + '.' + _t.get(_.howeverIHaveEvenStrongerArgumentAccepting) + ' ' + longConclusion + '.'
    if attack_type == 'rebut':
        ret_text = confrontation + ' '
        ret_text += _t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat)
        ret_text += ' ' + conclusion

    return ret_text + ' ...'  # + ', ' + _t.get(_.because).lower() + '...'


def get_header_for_users_confrontation_response(db_argument, lang, premise, attack_type, conclusion, start_lower_case,
                                                is_supportive, is_logged_in, redirect_from_jump=False):
    """
    Based on the users reaction, text will be build. This text can be used for the speech bubbles where users
    justify an argument they have chosen.

    :param db_argument: Argument
    :param lang: ui_locales
    :param premise: current premise
    :param attack_type: type of the attack
    :param conclusion: current conclusion
    :param start_lower_case: boolean
    :param is_supportive: boolean
    :param is_logged_in: boolean
    :param redirect_from_jump: boolean
    :return: string
    """
    _t = Translator(lang)

    if premise[-1] == '.':
        premise = premise[:-1]

    if conclusion[-1] == '.':
        conclusion = conclusion[:-1]

    # pretty print
    #  w = (_t.get(_.wrong)[0:1].lower() if start_lower_case else _t.get(_.wrong)[0:1].upper()) + _t.get(_.wrong)[1:] + ', '
    r = (_t.get(_.right)[0:1].lower() if start_lower_case else _t.get(_.right)[0:1].upper()) + _t.get(_.right)[1:] + ', '
    f = (_t.get(_.itIsFalseThat)[0:1].lower() if start_lower_case else _t.get(_.itIsFalseThat)[0:1].upper()) + _t.get(_.itIsFalseThat)[1:]
    t = (_t.get(_.itIsTrueThat)[0:1].lower() if start_lower_case else _t.get(_.itIsTrueThat)[0:1].upper()) + _t.get(_.itIsTrueThat)[1:]

    if lang == 'de':
        r += _t.get(_.itIsTrueThat)[0:1].lower() + _t.get(_.itIsTrueThat)[1:] + ' '
        f = _t.get(_.wrong) + ', ' + _t.get(_.itIsFalseThat)[0:1].lower() + _t.get(_.itIsFalseThat)[1:] + ' '

    if redirect_from_jump:
        r = _t.get(_.maybeItIsTrueThat) + ' '

    # different cases
    user_msg = __get_user_msg_for_users_confrontation_response(db_argument, attack_type, premise, conclusion, f, t, r, is_supportive, _t)
    if not user_msg:
        user_msg = ''

    # is logged in?
    system_msg = _t.get(_.canYouGiveAReasonForThat) if is_logged_in else ''

    return user_msg, system_msg


def __get_user_msg_for_users_confrontation_response(db_argument, attack_type, premise, conclusion, itisfalsethat, itistruethat, right, is_supportive, _t):
    """
    Builds a string based on the attack type to confront the user

    :param db_argument: Argument
    :param attack_type: String
    :param premise: String
    :param conclusion: String
    :param itisfalsethat: String
    :param itistruethat: String
    :param right: String
    :param is_supportive: Boolean
    :param _t: Translator
    :return: String
    """
    # different cases
    if attack_type == 'undermine':
        return __get_user_msg_for_users_undermine_response(premise, _t.get(_.that))

    if attack_type == 'support':
        return __get_user_msg_for_users_support_response(conclusion, itistruethat, itisfalsethat, is_supportive, _t)

    if attack_type == 'undercut':
        return __get_user_msg_for_users_undercut_response(db_argument, premise, conclusion, right, _t)

    if attack_type == 'rebut':
        return __get_user_msg_for_users_rebut_response(premise, conclusion, right, is_supportive, _t)


def __get_user_msg_for_users_undermine_response(premise, that):
    """
    Simple text for an undermine

    :param premise: String
    :param that: String
    :return: String
    """
    return that + ' ' + ' {}' + premise + '{}'


def __get_user_msg_for_users_support_response(conclusion, itistruethat, itisfalsethat, is_supportive, _t):
    """
    Simple text for an support

    :param conclusion: String
    :param itistruethat: String
    :param itisfalsethat: String
    :param is_supportive: String
    :param _t: Translator
    :return: String
    """
    user_msg = itistruethat if is_supportive else itisfalsethat
    user_msg += ' ' + conclusion + ' '
    user_msg += _t.get(_.hold) if is_supportive else _t.get(_.doesNotHold)
    user_msg += '.'
    return '{}' + user_msg + '{}'


def __get_user_msg_for_users_undercut_response(db_argument, premise, conclusion, right, _t):
    """
    Simple text for the undercut

    :param db_argument: Argument
    :param premise: String
    :param conclusion: String
    :param right: String
    :param _t: Translator
    :return:
    """
    tmp = None
    if db_argument.conclusion_uid is None and _t.get_lang() == 'de':
        # undercutting an undercut
        start_text = _t.get(_.itIsTrueThatAnonymous)
        if conclusion.lower().startswith(start_text.lower()):
            conclusion = conclusion[len(start_text):]
            tmp = _t.get(_.butThisDoesNotRejectArgument)

    if tmp is None:
        tmp = _t.get(_.butIDoNotBelieveArgumentFor) if db_argument.is_supportive else _t.get(_.butIDoNotBelieveCounterFor)
    tmp = tmp.format(conclusion)

    return right + premise + '. {}' + tmp + '{}'


def __get_user_msg_for_users_rebut_response(premise, conclusion, right, is_supportive, _t):
    """
    Simple text for the rebut

    :param premise: String
    :param conclusion: String
    :param right: String
    :param is_supportive:
    :param _t: Translator
    :return: String
    """
    user_msg = right + premise + ', '
    user_msg += _t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat)
    user_msg += ' ' + conclusion + '. '
    user_msg += _t.get(_.howeverIHaveMuchStrongerArgumentRejectingThat) if is_supportive else _t.get(
        _.howeverIHaveMuchStrongerArgumentAcceptingThat)
    user_msg += ' ' + conclusion + '.'
    return '{}' + user_msg + '{}'


def get_relation_text_dict_without_substitution(lang, with_no_opinion_text, premise, conclusion, is_dont_know=False, attack_type=None):
    """
    Returns the four different reaction possibilities without any replacement based on the gender of the confrontation

    :param lang: Language.ui_locales
    :param with_no_opinion_text: Boolean
    :param premise: String
    :param conclusion: String
    :param is_dont_know: Boolean
    :param attack_type: String
    :return: dict()
    """
    return __get_relation_text_dict(lang, with_no_opinion_text, premise, conclusion, is_dont_know, attack_type)


def get_relation_text_dict_with_substitution(lang, with_no_opinion_text, is_dont_know=False, attack_type=None, gender=''):
    """
    Returns the four different reaction possibilities with replacements based on the gender of the confrontation

    :param lang: Language.ui_locales
    :param with_no_opinion_text: Boolean
    :param is_dont_know: Boolean
    :param attack_type: String
    :param gender: String
    :return: dict()
    """
    _t = Translator(lang)

    assertion = _t.get(_.herAssertion) if gender is 'f' else _t.get(_.hisAssertion) if gender is 'm' else _t.get(_.theirAssertion)
    reason = _t.get(_.herReason) if gender is 'f' else _t.get(_.hisReason) if gender is 'm' else _t.get(_.theirReason)
    statement = _t.get(_.herStatement) if gender is 'f' else _t.get(_.hisStatement) if gender is 'm' else _t.get(_.theirStatement)
    position = _t.get(_.herPosition) if gender is 'f' else (_t.get(_.hisPosition) if gender is 'm' else _t.get(_.theirPosition))
    opinion = _t.get(_.opinion_her) if gender is 'f' else _t.get(_.opinion_his) if gender is 'm' else _t.get(_.opinion)

    if lang == 'de':
        if is_dont_know:
            premise = assertion
        else:
            premise = statement

        if is_dont_know:
            conclusion = reason
        else:
            conclusion = assertion

    else:
        premise = statement

        if not is_dont_know:
            if attack_type == 'undermine' or attack_type == 'rebut':
                conclusion = position
            else:
                conclusion = _t.get(_.myArgument)
        else:
            conclusion = opinion

    return __get_relation_text_dict(lang, with_no_opinion_text, premise, conclusion, is_dont_know)


def __get_relation_text_dict(lang, with_no_opinion_text, premise, conclusion, is_dont_know=False):
    """
    Text of the different reaction types for an given argument

    :param lang: Language.ui_locales
    :param with_no_opinion_text: Boolean
    :param premise: String
    :param conclusion: String
    :param is_dont_know: Boolean
    :return: dict()
    """
    _t = Translator(lang)

    # adding tags
    start_attack = '<{} data-argumentation-type="attack">'.format(tag_type)
    start_argument = '<{} data-argumentation-type="argument">'.format(tag_type)
    start_position = '<{} data-argumentation-type="position">'.format(tag_type)
    end_tag = '</{}>'.format(tag_type)
    premise = start_attack + premise + end_tag
    conclusion = start_argument + conclusion + end_tag

    ret_dict = dict()

    if with_no_opinion_text:
        ret_dict['step_back_text'] = _t.get(_.goStepBack) + '. (' + _t.get(_.noOtherAttack) + ')'
        ret_dict['no_opinion_text'] = _t.get(_.showMeAnotherArgument) + '.'

    ret_dict['undermine_text'] = _t.get(_.reaction_text_undermine).format(premise)

    ret_dict['support_text'] = _t.get(_.reaction_text_support).format(premise)

    if is_dont_know:
        tmp = start_argument + _t.get(_.reason) + end_tag
        ret_dict['undercut_text'] = _t.get(_.reaction_text_undercut_for_dont_know).format(premise, tmp)
    else:
        # tmp = start_position + _t.get(_.myPositionGenitiv) + end_tag
        ret_dict['undercut_text'] = _t.get(_.reaction_text_undercut).format(premise, conclusion)

    if is_dont_know:
        # conclusion_genitiv = conclusion.replace('ihre', 'ihrer').replace('seine', 'seiner')
        ret_dict['rebut_text'] = _t.get(_.reaction_text_rebut_for_dont_know).format(conclusion)
    else:
        conclusion_user = start_position + _t.get(_.myPosition) + end_tag
        ret_dict['rebut_text'] = _t.get(_.reaction_text_rebut).format(premise, conclusion, conclusion_user)

    return ret_dict


def get_jump_to_argument_text_list(lang):
    """
    Returns answer set for the jumping step

    :param lang: ui_locales
    :return: Array with [Conclusion is (right, wrong), Premise is (right, wrong), Premise does not lead to the conclusion, both hold]
    """
    _t = Translator(lang)

    tag_premise = '<' + tag_type + ' data-argumentation-type="attack">'
    tag_conclusion = '<' + tag_type + ' data-argumentation-type="argument">'
    tag_end = '</' + tag_type + '>'
    premise = tag_premise + (_t.get(_.reason).lower() if lang != 'de' else _t.get(_.reason)) + tag_end
    conclusion = tag_conclusion + (
        _t.get(_.assertion).lower() if lang != 'de' else _t.get(_.assertion)) + tag_end

    answers = list()

    answers.append(_t.get(_.jumpAnswer0).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer1).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer2).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer3).format(conclusion, premise))
    answers.append(_t.get(_.jumpAnswer4).format(premise))

    return answers


def get_support_to_argument_text_list(lang):
    """
    Returns answer set for the supporting step

    :param lang: ui_locales
    :return: Array with [Conclusion is (right, wrong), Premise is (right, wrong), Premise does not lead to the conclusion, both hold]
    """
    _t = Translator(lang)

    tag_premise = '<' + tag_type + ' data-argumentation-type="attack">'
    tag_conclusion = '<' + tag_type + ' data-argumentation-type="argument">'
    tag_end = '</' + tag_type + '>'
    premise = tag_premise + (_t.get(_.reason).lower() if lang != 'de' else _t.get(_.reason)) + tag_end
    conclusion = tag_conclusion + (
        _t.get(_.assertion).lower() if lang != 'de' else _t.get(_.assertion)) + tag_end

    answers = list()

    answers.append(_t.get(_.supportAnswer0).format(premise))
    answers.append(_t.get(_.supportAnswer3).format(premise))
    answers.append(_t.get(_.supportAnswer1).format(premise))
    answers.append(_t.get(_.supportAnswer2).format(premise, conclusion))

    return answers


def get_text_for_confrontation(main_page, lang, nickname, premise, conclusion, sys_conclusion, supportive, attack,
                               confrontation, reply_for_argument, user_is_attacking, user_arg, sys_arg,
                               color_html=True):
    """
    Text for the confrontation of the system

    :param main_page: main_page
    :param lang: ui_locales
    :param nickname: nickname
    :param premise: String
    :param conclusion: String
    :param sys_conclusion: String
    :param supportive: String
    :param attack: String
    :param confrontation: String
    :param reply_for_argument: Boolean
    :param user_is_attacking: Boolean
    :param user_arg: Argument
    :param sys_arg: Argument
    :param color_html: Boolean
    :return: String
    """
    from dbas.logger import logger
    _t = Translator(lang)
    gender = ''

    #  build some confrontation text
    if lang != 'de':
        confrontation = confrontation[0:1].lower() + confrontation[1:]
        premise = premise[0:1].lower() + premise[1:]
        sys_conclusion = sys_conclusion[0:1].lower() + sys_conclusion[1:]
        conclusion = conclusion[0:1].lower() + conclusion[1:]

    # adding tags
    start_attack = ('<' + tag_type + ' data-argumentation-type="attack">') if color_html else ''
    start_argument = ('<' + tag_type + ' data-argumentation-type="argument">') if color_html else ''
    # start_position = ('<' + tag_type + ' data-argumentation-type="position">') if color_html else ''
    end_tag = '</' + tag_type + '>' if color_html else ''
    if color_html:
        confrontation = start_attack + confrontation + end_tag
        conclusion = start_argument + conclusion + end_tag
        if attack == 'undermine':
            premise = start_argument + premise + end_tag
        sys_conclusion = start_argument + sys_conclusion + end_tag

    confrontation_text = ''
    # build some confrontation text
    if attack == 'undermine':
        confrontation_text, gender = __get_confrontation_text_for_undermine(main_page, nickname, premise, _t, sys_arg,
                                                                            end_tag, confrontation)

    elif attack == 'undercut':
        confrontation_text, gender = __get_confrontation_text_for_undercut(main_page, nickname, _t,
                                                                           premise, conclusion, confrontation,
                                                                           supportive, sys_arg)

    elif attack == 'rebut':
        confrontation_text, gender = __get_confrontation_text_for_rebut(main_page, lang, nickname, reply_for_argument,
                                                                        user_arg, user_is_attacking, _t, sys_conclusion,
                                                                        confrontation, premise, conclusion,
                                                                        start_argument, sys_arg)

    b = '<{}>'.format(tag_type)
    e = '</{}>'.format(tag_type)
    sys_text = confrontation_text + b + '.<br><br>' + _t.get(_.whatDoYouThinkAboutThat) + '?' + e
    return sys_text, gender


def get_text_for_support(db_arg, argument_text, nickname, main_page, _t):
    """
    Returns text for the system bubble during the support step

    :param db_arg: Argument
    :param argument_text: string
    :param nickname: User.nickname
    :param main_page: String
    :param _t: translator
    :return: string
    """
    b = '<{}>'.format(tag_type)
    e = '</{}>'.format(tag_type)
    db_other_user, author, gender, is_okay = get_name_link_of_arguments_author(main_page, db_arg, nickname)
    if is_okay:
        if gender == 'm':
            intro = _t.get(_.goodPointAndUserIsInterestedTooM)
        else:
            intro = _t.get(_.goodPointAndUserIsInterestedTooF)
        intro = intro.format(b, e, author, b, e, argument_text)
    else:
        intro = _t.get(_.goodPointAndOtherParticipantsIsInterestedToo).format(b, e, argument_text)

    question = '<br><br>{}?'.format(_t.get(_.whatDoYouThinkAboutThat))

    return intro + question


def get_text_for_edit_text_message(lang, nickname, original, edited, url, for_html=True):
    """
    Returns text for the editing an statement

    :param lang: Language.ui_locales
    :param nickname: User.nickname
    :param original:
    :param edited:
    :param url: String
    :param for_html: Boolean
    :return:
    """
    nl = '<br>' if for_html else '\n'
    _t = Translator(lang)
    content = _t.get(_.textversionChangedContent) + ' ' + nickname
    content += nl + (_t.get(_.fromm)[0:1].upper() + _t.get(_.fromm)[1:]) + ': ' + original + nl
    content += (_t.get(_.to)[0:1].upper() + _t.get(_.to)[1:]) + ': ' + edited + nl
    content += (_t.get(_.where)[0:1].upper() + _t.get(_.where)[1:]) + ': '
    if for_html:
        content += '<a href="' + url + '">' + url + '</a>'
    else:
        content += url

    return content


def get_text_for_add_text_message(nickname, lang, url, for_html=True):
    """
    Returns text for the adding an statement

    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param url: String
    :param for_html: Boolean
    :return:
    """
    nl = '<br>' if for_html else '\n'
    _t = Translator(lang)
    content = _t.get(_.statementAddedMessageContent).format(nickname) + nl
    content += (_t.get(_.where)[0:1].upper() + _t.get(_.where)[1:]) + ': '
    if for_html:
        content += '<a href="' + url + '">' + url + '</a>'
    else:
        content += url

    return content


def get_text_for_add_argument_message(nickname, lang, url, for_html=True):
    """
    Returns text for the adding an argument

    :param nickname: User.nickname
    :param lang: Language.ui_locales
    :param url: String
    :param for_html: Boolean
    :return:
    """
    nl = '<br>' if for_html else '\n'
    _t = Translator(lang)
    content = _t.get(_.statementAddedMessageContent).format(nickname) + nl
    content += (_t.get(_.where)[0:1].upper() + _t.get(_.where)[1:]) + ': '
    if for_html:
        content += '<a href="' + url + '">' + url + '</a>'
    else:
        content += url

    return content


def __get_confrontation_text_for_undermine(main_page, nickname, premise, _t, system_argument, end_tag, confrontation):
    """
    Returns the system bubble text for an undermine

    :param main_page: String
    :param nickname: User.nickname
    :param premise: String
    :param _t: Translator
    :param system_argument: String
    :param end_tag: String
    :param confrontation: String
    :return:
    """
    b = '<' + tag_type + '>'
    bs = '<{} class="triangle-content-text">'.format(tag_type)
    e = '</' + tag_type + '>'
    start_argument = '<{} data-argumentation-type="argument">'.format(tag_type)

    move_end_tag = False
    if tag_type not in premise:
        premise = b + premise + e
    if tag_type not in confrontation:
        confrontation = b + confrontation + e
        move_end_tag = True

    db_other_user, author, gender, is_okay = get_name_link_of_arguments_author(main_page, system_argument, nickname)
    if is_okay:
        confrontation_text = author + ' ' + bs + _t.get(_.thinksThat)
    else:
        confrontation_text = bs + _t.get(_.otherParticipantsThinkThat)

    confrontation_text += e + ' ' + premise
    # confrontation_text += start_position if attack != 'undermine' else start_argument
    confrontation_text += '<{} data-attitude="{}">'.format(tag_type, 'pro' if system_argument.is_supportive else 'con')
    confrontation_text += b + ' ' + start_argument
    confrontation_text += _t.get(_.hold) if system_argument.is_supportive else _t.get(_.doesNotHold)
    confrontation_text += end_tag + e
    confrontation_text += end_tag
    # confrontation_text += end_tag if not move_end_tag else ''
    confrontation_text += b + ', ' + _t.get(_.because).lower() + e + ' ' + confrontation
    confrontation_text += end_tag if move_end_tag else ''
    return confrontation_text, gender if is_okay else ''


def __get_confrontation_text_for_undercut(main_page, nickname, _t, premise, conclusion, confrontation, supportive,
                                          system_argument):
    """
    Returns the system bubble text for an undercut

    :param main_page: String
    :param nickname: User.nickname
    :param _t: Translator
    :param premise: String
    :param conclusion: String
    :param confrontation: String
    :param supportive: Boolean
    :param system_argument: String
    :return:
    """

    db_other_user, author, gender, is_okay = get_name_link_of_arguments_author(main_page, system_argument, nickname)
    b = '<' + tag_type + '>'
    bs = '<{} class="triangle-content-text">'.format(tag_type)
    e = '</' + tag_type + '>'
    if is_okay:
        confrontation_text = author + ' ' + bs + _t.get(_.agreesThat)
        gender_think = (_t.get(_.heThinks) if gender is 'm' else _t.get(_.sheThinks)) if is_okay else _t.get(_.theyThink)
    else:
        confrontation_text = bs + _t.get(_.otherParticipantsDontHaveOpinion)
        gender_think = _t.get(_.participantsThink)

    confrontation_text += ' ' + premise + '. '
    if supportive:
        bind = (_t.get(_.butHeDoesNotBelieveArgument) if gender is 'm' else _t.get(_.butSheDoesNotBelieveArgument)) \
            if is_okay else _t.get(_.butTheyDoNotBelieveArgument)
    else:
        bind = (_t.get(_.butHeDoesNotBelieveCounter) if gender is 'm' else _t.get(_.butSheDoesNotBelieveCounter)) \
            if is_okay else _t.get(_.butTheyDoNotBelieveCounter)
    tag_start = '<{} data-attitude="{}">'.format(tag_type, 'con')
    tag_end = '</{}>'.format(tag_type)
    confrontation_text += bind.format(tag_start, tag_end, tag_start, tag_end)

    confrontation_text += e + ' ' + conclusion + b + '. ' + gender_think + ' ' + e + confrontation
    return confrontation_text, gender if is_okay else ''


def __get_confrontation_text_for_rebut(main_page, lang, nickname, reply_for_argument, user_arg, user_is_attacking, _t,
                                       sys_conclusion, confrontation, premise, conclusion, start_argument,
                                       system_argument):
    """
    Returns the system bubble text for a rebut

    :param main_page: main_page
    :param lang: ui_locales
    :param nickname: of current user
    :param reply_for_argument: Boolean
    :param user_arg: Argument
    :param user_is_attacking: Boolean
    :param _t: Translator
    :param sys_conclusion: String
    :param confrontation: String
    :param premise: String
    :param conclusion: String
    :param start_argument: String
    :param system_argument: Counter argument of the system
    :return: String, String
    """

    db_other_user, author, gender, is_okay = get_name_link_of_arguments_author(main_page, system_argument, nickname)
    db_other_nick = db_other_user.nickname if db_other_user else ''
    b = '<{}>'.format(tag_type)
    bs = '<{} class="triangle-content-text">'.format(tag_type)
    e = '</{}>'.format(tag_type)
    tag_pro_start = '<{} data-attitude="{}">'.format(tag_type, 'pro')
    tag_con_start = '<{} data-attitude="{}">'.format(tag_type, 'con')

    # has the other user any opinion for the users conclusion?
    has_other_user_opinion = False
    if is_okay:
        if user_arg.argument_uid is None:
            db_vote = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.argument_uid == user_arg.argument_uid,
                                                                             ClickedArgument.author_uid == db_other_user.uid,
                                                                             ClickedArgument.is_up_vote == True,
                                                                             ClickedArgument.is_valid == True)).all()
        else:
            db_vote = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.statement_uid == user_arg.conclusion_uid,
                                                                              ClickedStatement.author_uid == db_other_user.uid,
                                                                              ClickedStatement.is_up_vote == True,
                                                                              ClickedStatement.is_valid == True)).all()
        has_other_user_opinion = db_vote and len(db_vote) > 0

    # distinguish between reply for argument and reply for premise group
    if reply_for_argument:  # reply for argument
        # changing arguments for better understanding
        if not user_arg.is_supportive:
            # user_is_attacking = not user_is_attacking
            conclusion = sys_conclusion

        confrontation_text = (author + ' ' + b) if is_okay else bs
        if is_okay:
            bind = b + _t.get(_.otherUsersClaimStrongerArgumentS) + e
        else:
            bind = b + _t.get(_.otherUsersClaimStrongerArgumentP) + e

        start_tag = ('<' + tag_type + ' data-argumentation-type="argument">') if tag_type in confrontation else ''
        end_tag = '</' + tag_type + '>' if tag_type in confrontation else ''
        accept = _.assistance if lang == 'de' else _.accept
        reject = _.rejection if lang == 'de' else _.reject
        # tmp = start_tag + _t.get(reject if user_is_attacking else accept) + ' ' + end_tag
        tmp = start_tag + _t.get(accept if system_argument.is_supportive else reject) + ' ' + end_tag
        confrontation_text += bind.format(tmp) + ' ' + conclusion + '.' + ' ' + b

        if is_okay:
            confrontation_text += _t.get(_.heSays) if gender is 'm' else _t.get(_.sheSays)
        else:
            confrontation_text += _t.get(_.theySay)

        confrontation_text += ' ' if lang == 'de' else ': '
        confrontation_text += e + confrontation

    else:  # reply for premise group
        if is_okay:
            if has_other_user_opinion:
                confrontation_text = author + ' ' + bs + _t.get(_.agreesThat) + ' {}. '
                confrontation_text += _t.get(_.strongerStatementM) if gender is 'm' else _t.get(_.strongerStatementF)
            elif db_other_nick == nickname:
                confrontation_text = author + ' ' + bs + _t.get(_.earlierYouHadNoOpinitionForThisStatement) + ' '
                confrontation_text += _t.get(_.strongerStatementY)
            else:
                confrontation_text = author + ' ' + bs + _t.get(_.otherUserDoesntHaveOpinionForThisStatement) + ' '
                confrontation_text += _t.get(_.strongerStatementM) if gender is 'm' else _t.get(_.strongerStatementF)

        else:
            confrontation_text = bs + _t.get(_.otherParticipantsDontHaveOpinion) + ' {}. '
            confrontation_text += _t.get(_.strongerStatementP)

        tag = tag_pro_start if user_is_attacking else tag_con_start
        tmp = start_argument
        tmp += _t.get(_.accepting) if user_is_attacking else _t.get(_.rejecting)
        tmp += '</{}>'.format(tag_type) if len(start_argument) > 0 else ''
        confrontation_text = confrontation_text.format(premise, tag, tmp, ' ' + e)

        tmp = _t.get(_.strongerStatementEnd)
        if tmp == '':
            tmp += ' '
            conclusion = conclusion[len(start_argument):]

        confrontation_text += ' ' + conclusion + '. '
        confrontation_text += b
        if db_other_nick == nickname:
            confrontation_text += _t.get(_.nowYouSayThat)
        else:
            confrontation_text += (_t.get(_.heSays) if gender is 'm' else _t.get(_.sheSays)) if is_okay else _t.get(_.theySay)
        confrontation_text += ' ' if lang == 'de' else ': '
        confrontation_text += e
        confrontation_text += confrontation

    return confrontation_text, gender if is_okay else ''


def get_name_link_of_arguments_author(main_page, argument, nickname, with_link=True):
    """
    Will return author of the argument, if the first supporting user

    :param main_page: String
    :param argument: Argument
    :param nickname: User.nickname
    :param with_link:
    :return:
    """
    user, text, is_okay = get_author_data(main_page, argument.author_uid, False, True)
    db_author_of_argument = DBDiscussionSession.query(User).get(argument.author_uid)
    gender = db_author_of_argument.gender if db_author_of_argument else 'n'

    db_anonymous_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()

    # if the data of arguments author is not okay, get the first user, who agrees with the argument
    if argument.author_uid == db_anonymous_user.uid or not is_okay:
        # get nick of current user
        nickname = nickname if nickname is not None else nick_of_anonymous_user
        db_current_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        db_author_of_argument = get_author_or_first_supporter_of_element(argument.uid, db_current_user.uid, True)

        if db_author_of_argument:
            user, text, is_okay = get_author_data(main_page, db_author_of_argument.uid, gravatar_on_right_side=False, linked_with_users_page=with_link)
            db_author_of_argument = DBDiscussionSession.query(User).get(db_author_of_argument.uid)
            gender = db_author_of_argument.gender if db_author_of_argument else 'n'
        else:
            return None, '', 'n', False

    return user, text if is_okay else '', gender, is_okay


def get_author_or_first_supporter_of_element(uid, current_user_uid, is_argument):
    """
    Returns the first user with the same opinion and who is not the anonymous or current user

    :param uid: Argument.uid / Statement.uid
    :param current_user_uid: User.uid
    :param is_argument: Boolean
    :return: MarkedArgument or None
    """

    db_anonymous_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    if is_argument:
        db_vote = DBDiscussionSession.query(MarkedArgument).filter(and_(
            ~ClickedArgument.author_uid.in_([db_anonymous_user.uid, current_user_uid]),
            ClickedArgument.argument_uid == uid,
        )).first()
    else:
        db_vote = DBDiscussionSession.query(MarkedStatement).filter(and_(
            ~ClickedArgument.author_uid.in_([db_anonymous_user.uid, current_user_uid]),
            ClickedArgument.statement_uid == uid,
        )).first()

    if db_vote:
        return DBDiscussionSession.query(User).get(db_vote.author_uid)
    else:
        return None
