#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbas.lib import get_author_data
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Premise, Statement, VoteStatement, VoteArgument, User
from dbas.database.initializedb import nick_of_anonymous_user
from sqlalchemy import and_
from .keywords import Keywords as _
from .translator import Translator


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

    premise = premise[0:1].lower() + premise[1:]
    conclusion = conclusion[0:1].lower() + conclusion[1:]

    # different cases
    ret_text = ''
    if attack_type == 'undermine':
        ret_text = _t.get(_.itIsFalseThat) + ' ' + premise
    if attack_type == 'support':
        ret_text = _t.get(_.itIsTrueThat) if is_supportive else _t.get(_.itIsFalseThat)
        ret_text += ' ' + conclusion + ' '
        ret_text += _t.get(_.hold) if is_supportive else _t.get(_.doesNotHold)
    if attack_type == 'undercut':
        ret_text = confrontation + ', ' + _t.get(_.butIDoNotBelieveCounterFor) + ' ' + conclusion
    if attack_type == 'overbid':
        ret_text = confrontation + ', ' + _t.get(_.andIDoBelieveCounterFor) + ' ' + conclusion
    # + '.' + _t.get(_.howeverIHaveEvenStrongerArgumentAccepting) + ' ' + longConclusion + '.'
    if attack_type == 'rebut':
        ret_text = confrontation + ' '
        ret_text += (_t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat))
        ret_text += ' ' + conclusion

    return ret_text + ', ' + _t.get(_.because).lower() + '...'


def get_header_for_users_confrontation_response(lang, premise, attack_type, conclusion, start_lower_case, is_supportive, is_logged_in):
    """
    Based on the users reaction, text will be build. This text can be used for the speech bubbles where users
    justify an argument they have chosen.

    :param lang: ui_locales
    :param premise: current premise
    :param attack_type: type of the attack
    :param conclusion: current conclusion
    :param start_lower_case: boolean
    :param is_supportive: boolean
    :param is_logged_in: boolean
    :return: string
    """
    _t = Translator(lang)

    system_msg = ''
    premise    = premise[0:1].lower() + premise[1:]
    if lang != 'de':
        conclusion = conclusion[0:1].lower() + conclusion[1:]

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

    # different cases
    user_msg = __get_user_msg_for_users_confrontation_response(attack_type, premise, conclusion, f, t, r, is_supportive, _t)
    if not user_msg:
        user_msg = ''

    # is logged in?
    if is_logged_in:
        system_msg = _t.get(_.canYouGiveAReasonForThat)

    return user_msg, system_msg


def __get_user_msg_for_users_confrontation_response(attack_type, premise, conclusion, f, t, r, is_supportive, _t):
    # different cases
    if attack_type == 'undermine':
        return __get_user_msg_for_users_undermine_response(premise, f)

    if attack_type == 'support':
        return __get_user_msg_for_users_support_response(conclusion, t, f, is_supportive, _t)

    if attack_type == 'undercut':
        return __get_user_msg_for_users_undercut_response(premise, conclusion, r, is_supportive, _t)

    if attack_type == 'overbid':
        return __get_user_msg_for_users_overbid_response(premise, r, conclusion, is_supportive, _t)

    if attack_type == 'rebut':
        return __get_user_msg_for_users_rebut_response(premise, conclusion, r, is_supportive, _t)


def __get_user_msg_for_users_undermine_response(premise, f):
    return f + ' ' + premise + '.'


def __get_user_msg_for_users_support_response(conclusion, t, f, is_supportive, _t):
    user_msg = t if is_supportive else f
    user_msg += ' ' + conclusion + ' '
    user_msg += _t.get(_.hold) if is_supportive else _t.get(_.doesNotHold)
    user_msg += '.'
    return user_msg


def __get_user_msg_for_users_undercut_response(premise, conclusion, r, is_supportive, _t):
    user_msg = r + premise + ', '
    user_msg += _t.get(_.butIDoNotBelieveArgumentFor) if is_supportive else _t.get(_.butIDoNotBelieveCounterFor)
    user_msg += ' ' + conclusion + '.'
    return user_msg


def __get_user_msg_for_users_overbid_response(premise, r, conclusion, is_supportive, _t):
    user_msg = r + premise + ', '
    user_msg += _t.get(_.andIDoBelieveCounterFor) if is_supportive else _t.get(_.andIDoBelieveArgument)
    user_msg += ' ' + conclusion + '. '
    user_msg += _t.get(_.howeverIHaveEvenStrongerArgumentAccepting) if is_supportive else _t.get(
        _.howeverIHaveEvenStrongerArgumentRejecting)
    user_msg += ' ' + conclusion + '.'
    return user_msg


def __get_user_msg_for_users_rebut_response(premise, conclusion, r, is_supportive, _t):
    user_msg = r + premise + ', '
    user_msg += _t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat)
    user_msg += ' ' + conclusion + '. '
    user_msg += _t.get(_.howeverIHaveMuchStrongerArgumentRejectingThat) if is_supportive else _t.get(
        _.howeverIHaveMuchStrongerArgumentAcceptingThat)
    user_msg += ' ' + conclusion + '.'
    return user_msg


def get_relation_text_dict_without_substitution(lang, start_lower_case, with_no_opinion_text, is_attacking, premise,
                                                conclusion, is_dont_know=False, first_conclusion=None,
                                                for_island_view=False, attack_type=None):
    """

    :param start_lower_case:
    :param with_no_opinion_text:
    :param is_attacking:
    :param premise:
    :param conclusion:
    :param is_dont_know:
    :param first_conclusion:
    :param for_island_view:
    :param attack_type:
    :return:
    """
    return __get_relation_text_dict(lang, start_lower_case, with_no_opinion_text, is_attacking, premise, conclusion,
                                    is_dont_know, first_conclusion, for_island_view, attack_type)


def get_relation_text_dict_with_substitution(lang, start_lower_case, with_no_opinion_text, is_attacking,
                                             is_dont_know=False, first_conclusion=None, for_island_view=False,
                                             attack_type=None, gender=''):
    """

    :param lang: ui_locales
    :param start_lower_case:
    :param with_no_opinion_text:
    :param is_attacking:
    :param is_dont_know:
    :param first_conclusion:
    :param for_island_view:
    :param attack_type:
    :param gender:
    :return:
    """
    _t = Translator(lang)

    if not is_dont_know:
        premise = _t.get(_.herArgument) if gender is 'f' else (_t.get(_.hisArgument) if gender is 'm' else _t.get(_.theirArgument))
        if attack_type == 'undermine' or attack_type == 'rebut':
            conclusion = _t.get(_.herPosition) if gender is 'f' else (_t.get(_.hisPosition) if gender is 'm' else _t.get(_.theirPosition))
        else:
            conclusion = _t.get(_.myArgument)
    else:
        premise = _t.get(_.thisArgument)
        conclusion = _t.get(_.opinion)

    return __get_relation_text_dict(lang, start_lower_case, with_no_opinion_text, is_attacking, premise, conclusion,
                                    is_dont_know, first_conclusion, for_island_view, attack_type)


def __get_relation_text_dict(lang, start_lower_case, with_no_opinion_text, is_attacking, premise, conclusion,
                             is_dont_know=False, first_conclusion=None, for_island_view=False, attack_type=None):
    """
    Text of the different reaction types for an given argument

    :param lang: ui_locales
    :param start_lower_case:
    :param with_no_opinion_text:
    :param is_attacking:
    :param premise:
    :param conclusion:
    :param is_dont_know:
    :param first_conclusion:
    :param for_island_view:
    :param attack_type:
    :return:
    """
    _t = Translator(lang)

    ret_dict = dict()

    if first_conclusion and first_conclusion[-1] == '.':
        first_conclusion = first_conclusion[:-1]

    # adding tags
    start_attack = '<' + tag_type + ' data-argumentation-type="attack">'
    start_argument = '<' + tag_type + ' data-argumentation-type="argument">'
    start_position = '<' + tag_type + ' data-argumentation-type="position">'
    end_tag = '</' + tag_type + '>'
    premise = start_attack + premise + end_tag
    conclusion = start_argument + conclusion + end_tag

    w = (_t.get(_.wrong)[0:1].lower() if start_lower_case else _t.get(_.wrong)[0:1].upper()) + _t.get(_.wrong)[1:]
    r = (_t.get(_.right)[0:1].lower() if start_lower_case else _t.get(_.right)[0:1].upper()) + _t.get(_.right)[1:]

    w += ', ' + _t.get(_.itIsFalse1) + ' '
    r += ', ' + _t.get(_.itIsTrue1) + ' '

    ret_dict['undermine_text'] = w + premise + ' ' + _t.get(_.itIsFalse2) + '.'

    ret_dict['support_text'] = r + premise + _t.get(_.itIsTrue2) + '.'

    # tmp = _t.get(_.butIDoNotBelieveCounter) if is_attacking else _t.get(_.butIDoNotBelieveArgument)
    tmp = _t.get(_.butIDoNotBelieveArgument) if not is_attacking or not attack_type == 'undercut' else _t.get(
        _.butIDoNotBelieveCounter)
    ret_dict['undercut_text'] = r + premise + _t.get(_.itIsTrue2) + ', '
    ret_dict['undercut_text'] += (_t.get(_.butIDoNotBelieveArgumentFor) if is_dont_know else tmp)
    ret_dict['undercut_text'] += ' ' + conclusion + (' ist.' if lang == 'de' else '.')

    ret_dict['overbid_text'] = r + premise + _t.get(_.itIsTrue2) + ', '
    ret_dict['overbid_text'] += (
        _t.get(_.andIDoBelieveArgument) if is_dont_know else _t.get(_.andIDoBelieveCounterFor))
    ret_dict['overbid_text'] += ' ' + conclusion + '. '
    ret_dict['overbid_text'] += (_t.get(_.howeverIHaveEvenStrongerArgumentRejecting) if is_attacking else _t.get(
        _.howeverIHaveEvenStrongerArgumentAccepting))
    ret_dict['overbid_text'] += ' ' + conclusion + '.'

    ret_dict['rebut_text'] = r + premise + _t.get(_.itIsTrue2) + ' '
    # ret_dict['rebut_text'] += (_t.get(_.iAcceptCounter) if is_attacking else _t.get(_.iAcceptArgument))
    ret_dict['rebut_text'] += _t.get(
        _.iAcceptArgument) if not is_attacking or not attack_type == 'undercut' else _t.get(_.iAcceptCounter)
    ret_dict['rebut_text'] += ' ' + conclusion + (' ist. ' if lang == 'de' else '. ')
    ret_dict['rebut_text'] += _t.get(_.howeverIHaveMuchStrongerArgument) + ' '
    ret_dict['rebut_text'] += start_argument if is_dont_know else start_position
    ret_dict['rebut_text'] += _t.get(_.reject if is_dont_know else _.accept)
    # ret_dict['rebut_text'] += _t.get(_.accept if is_attacking else _.reject)
    ret_dict['rebut_text'] += ' ' + (first_conclusion if first_conclusion else conclusion) + end_tag + '.'
    # + (_t.get(_.doesNotHold) if is_attacking else _t.get(_.hold)) + '.'

    if for_island_view and lang == 'de':
        ret_dict['undermine_text'] = ret_dict['undermine_text'][:-1] + ', ' + _t.get(_.because).lower()
        ret_dict['support_text'] = ret_dict['support_text'][:-1] + ', ' + _t.get(_.because).lower()
        ret_dict['undercut_text'] = ret_dict['undercut_text'][:-1] + ', ' + _t.get(_.because).lower()
        ret_dict['overbid_text'] = ret_dict['overbid_text'][:-1] + ', ' + _t.get(_.because).lower()
        ret_dict['rebut_text'] = ret_dict['rebut_text'][:-1] + ', ' + _t.get(_.because).lower()

    if with_no_opinion_text:
        ret_dict['step_back_text'] = _t.get(_.iHaveNoOpinion) + '. ' + _t.get(_.goStepBack) + '. (' + _t.get(
            _.noOtherAttack) + ')'
        ret_dict['no_opinion_text'] = _t.get(_.iHaveNoOpinion) + '. ' + _t.get(_.showMeAnotherArgument) + '.'

    return ret_dict


def get_jump_to_argument_text_list(lang):
    """

    :param lang: ui_locales
    :return: Array with [Conclusion is (right, wrong), Premise is (right, wrong), Premise does not lead to the conclusion, both hold]
    """
    _t = Translator(lang)

    tag_premise = '<' + tag_type + ' data-argumentation-type="argument">'
    tag_conclusion = '<' + tag_type + ' data-argumentation-type="attack">'
    tag_end = '</' + tag_type + '>'
    premise = tag_premise + (_t.get(_.reason).lower() if lang != 'de' else _t.get(_.reason)) + tag_end
    conclusion = tag_conclusion + (
        _t.get(_.assertion).lower() if lang != 'de' else _t.get(_.assertion)) + tag_end

    answers = list()

    answers.append(_t.get(_.jumpAnswer0).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
    answers.append(_t.get(_.jumpAnswer1).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
    answers.append(_t.get(_.jumpAnswer2).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
    answers.append(_t.get(_.jumpAnswer3).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
    answers.append(_t.get(_.jumpAnswer4).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))

    return answers


def get_text_for_confrontation(main_page, lang, nickname, premise, conclusion, sys_conclusion, supportive, attack, confrontation,
                               reply_for_argument, user_is_attacking, user_arg, sys_arg, color_html=True):
    """
    Text for the confrontation of the system

    :param lang: ui_locales
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
    _t = Translator(lang)
    gender = ''

    #  build some confrontation text
    if lang != 'de':
        confrontation   = confrontation[0:1].lower() + confrontation[1:]
        premise         = premise[0:1].lower() + premise[1:]
        sys_conclusion  = sys_conclusion[0:1].lower() + sys_conclusion[1:]
        conclusion      = conclusion[0:1].lower() + conclusion[1:]

    # adding tags
    start_attack = ('<' + tag_type + ' data-argumentation-type="attack">') if color_html else ''
    start_argument = ('<' + tag_type + ' data-argumentation-type="argument">') if color_html else ''
    start_position = ('<' + tag_type + ' data-argumentation-type="position">') if color_html else ''
    end_tag = '</' + tag_type + '>'
    if color_html:
        confrontation = start_attack + confrontation + end_tag
        conclusion = start_argument + conclusion + end_tag
        if attack == 'undermine':
            premise = start_argument + premise + end_tag
            sys_conclusion = start_argument + sys_conclusion + end_tag
        elif attack == 'undercut':
            sys_conclusion = start_argument + sys_conclusion + end_tag

    confrontation_text = ''
    db_users_premise = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=user_arg.premisesgroup_uid).join(Statement).first()

    # build some confrontation text
    if attack == 'undermine':
        confrontation_text, gender = __get_confrontation_text_for_undermine(main_page, nickname, premise, _t, start_position,
                                                                            start_argument, attack, sys_arg, end_tag,
                                                                            confrontation)

    elif attack == 'undercut':
        confrontation_text, gender = __get_confrontation_text_for_undercut(main_page, lang, nickname, db_users_premise, _t,
                                                                           premise, conclusion, confrontation,
                                                                           supportive, sys_arg)

    elif attack == 'rebut':
        confrontation_text, gender = __get_confrontation_text_for_rebut(main_page, lang, nickname, reply_for_argument,
                                                                        user_arg, user_is_attacking, _t, sys_conclusion,
                                                                        confrontation, premise, conclusion,
                                                                        start_argument, end_tag, db_users_premise,
                                                                        sys_arg,)

    sys_text = confrontation_text + '.<br><br>' + _t.get(_.whatDoYouThinkAboutThat) + '?'
    return sys_text, gender


def get_text_for_edit_text_message(lang, nickname, original, edited, url, for_html=True):
    """

    :param lang:
    :param nickname:
    :param original:
    :param edited:
    :param url:
    :param for_html:
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


def get_text_for_add_text_message(lang, url, for_html=True):
    """

    :param lang:
    :param url:
    :param for_html:
    :return:
    """
    nl = '<br>' if for_html else '\n'
    _t = Translator(lang)
    content = _t.get(_.statementAddedMessageContent) + nl
    content += (_t.get(_.where)[0:1].upper() + _t.get(_.where)[1:]) + ': '
    if for_html:
        content += '<a href="' + url + '">' + url + '</a>'
    else:
        content += url

    return content


def get_text_for_add_argument_message(lang, url, for_html=True):
    """

    :param lang:
    :param url:
    :param for_html:
    :return:
    """
    nl = '<br>' if for_html else '\n'
    _t = Translator(lang)
    content = _t.get(_.statementAddedMessageContent) + nl
    content += (_t.get(_.where)[0:1].upper() + _t.get(_.where)[1:]) + ': '
    if for_html:
        content += '<a href="' + url + '">' + url + '</a>'
    else:
        content += url

    return content


def __get_text_dict_for_attacks_only(lang, premises, conclusion, start_lower_case):
    """

    :param lang: ui_locales
    :param premises: String
    :param conclusion: String
    :param start_lower_case: Boolean
    :return: dict()
    """
    _t = Translator(lang)
    ret_dict = dict()

    if conclusion[-1] == '.':
        conclusion = conclusion[:-1]

    premise = ''
    for p in premises:
        premise += premises[p]['text'] + _t.get(_.aand)
    premise = premise[0:-4]

    w = (_t.get(_.wrong)[0:1].lower() if start_lower_case else _t.get(_.wrong)[0:1].upper()) + _t.get(_.wrong)[1:]
    r = (_t.get(_.right)[0:1].lower() if start_lower_case else _t.get(_.right)[0:1].upper()) + _t.get(_.right)[1:]
    counter_justi = ' ' + conclusion + ', ' + _t.get(_.because).toLocaleLowerCase() + ' ' + premise

    ret_dict['undermine_text'] = w + ', ' + premise + '.'
    ret_dict['undercut_text'] = r + ', ' + conclusion + ', ' + _t.get(
        _.butIDoNotBelieveArgumentFor) + ' ' + counter_justi + '.'
    ret_dict['rebut_text'] = r + ', ' + premise + ' ' + _t.get(_.iAcceptArgumentThat) + ' ' + conclusion + '. '
    ret_dict['rebut_text'] += _t.get(_.howeverIHaveMuchStrongerArgumentRejectingThat) + ' ' + conclusion + '.'
    ret_dict['no_opinion_text'] = _t.get(_.iNoOpinion) + ': ' + conclusion + ', ' + _t.get(
        _.because).toLocaleLowerCase()
    ret_dict['no_opinion_text'] += ' ' + premise + '. ' + _t.get(_.goStepBack) + '.'
    return ret_dict


def __get_confrontation_text_for_undermine(main_page, nickname, premise, _t, start_position, start_argument, attack, system_argument,
                                           end_tag, confrontation):
    """

    :param: nickname of current user
    :param premise:
    :param _t:
    :param start_position:
    :param start_argument:
    :param attack:
    :param system_argument: Counter argument of the system
    :param end_tag:
    :param confrontation:
    :return:
    """
    author, gender, is_okay = __get_name_link_of_arguments_author(main_page, system_argument, nickname)
    if is_okay:
        confrontation_text = author + ' ' + _t.get(_.thinksThat)
    else:
        confrontation_text = _t.get(_.otherParticipantsThinkThat)
    confrontation_text += ' ' + premise + ' '
    confrontation_text += start_position if attack != 'undermine' else start_argument
    confrontation_text += _t.get(_.hold) if system_argument.is_supportive else _t.get(_.doesNotHold)
    confrontation_text += end_tag
    confrontation_text += ', ' + _t.get(_.because).lower() + ' ' + confrontation
    return confrontation_text, gender if is_okay else ''


def __get_confrontation_text_for_undercut(main_page, lang, nickname, db_users_premise, _t, premise, conclusion, confrontation, supportive, system_argument):
    """

    :param lang:
    :param: nickname of current user
    :param db_users_premise:
    :param _t:
    :param premise:
    :param conclusion:
    :param confrontation:
    :param supportive:
    :param system_argument: Counter argument of the system
    :return:
    """

    author, gender, is_okay = __get_name_link_of_arguments_author_with_statement_agree(main_page, system_argument,
                                                                                       db_users_premise.statements,
                                                                                       nickname)
    if is_okay:
        confrontation_text = author + ' ' + _t.get(_.agreesThat)
    else:
        confrontation_text = _t.get(_.otherParticipantsDontHaveOpinion)

    confrontation_text += ' ' + premise + ', '
    if supportive:
        confrontation_text += (_t.get(_.butHeDoesNotBelieveArgument) if gender is 'm' else _t.get(_.butSheDoesNotBelieveArgument)) \
            if is_okay else _t.get(_.butTheyDoNotBelieveArgument)
    else:
        confrontation_text += (_t.get(_.butHeDoesNotBelieveCounter) if gender is 'm' else _t.get(_.butSheDoesNotBelieveCounter)) \
            if is_okay else _t.get(_.butTheyDoNotBelieveCounter)
    confrontation_text += ' ' + conclusion

    gender_think = (_t.get(_.heThinks) if gender is 'm' else _t.get(_.sheThinks)) if is_okay else _t.get(_.theyThink)
    if lang == 'de':
        confrontation_text += '. ' + gender_think
    else:
        confrontation_text += ', ' + _t.get(_.because).lower() + ' ' + gender_think.lower()

    confrontation_text += ' ' if lang == 'de' else ': '
    confrontation_text += confrontation
    return confrontation_text, gender if is_okay else ''


def __get_confrontation_text_for_rebut(main_page, lang, nickname, reply_for_argument, user_arg, user_is_attacking, _t, sys_conclusion,
                                       confrontation, premise, conclusion, start_argument, end_tag, db_users_premise,
                                       system_argument):
    """
    Builds the string for a rebut of the system.

    :param lang: ui_locales
    :param: nickname of current user
    :param reply_for_argument: Boolean
    :param user_arg: Argument
    :param user_is_attacking: Boolean
    :param _t: Translator
    :param sys_conclusion: String
    :param confrontation: String
    :param premise: String
    :param conclusion: String
    :param start_argument: String
    :param end_tag: String
    :param db_users_premise: Premise of the user
    :param system_argument: Counter argument of the system
    :return: String
    """
    author, gender, is_okay = __get_name_link_of_arguments_author_with_statement_agree(main_page, system_argument,
                                                                                       db_users_premise.statements,
                                                                                       nickname)

    # distinguish between reply for argument and reply for premise group
    if reply_for_argument:  # reply for argument
        # changing arguments for better understanding
        if not user_arg.is_supportive:
            user_is_attacking = not user_is_attacking
            conclusion = sys_conclusion

        confrontation_text = author + ' ' if is_okay else ''
        if is_okay:
            bind = _t.get(_.otherUsersClaimStrongerArgumentS)
        else:
            bind = _t.get(_.otherUsersClaimStrongerArgumentP)
        confrontation_text += bind.replace('XXX', _t.get(_.reject if user_is_attacking else _.accept))
        confrontation_text += ' ' + conclusion + '.' + ' '
        if is_okay:
            confrontation_text += _t.get(_.heSays) if gender is 'm' else _t.get(_.sheSays)
        else:
            confrontation_text += _t.get(_.theySay)
        confrontation_text += ' ' if lang == 'de' else ': '
        confrontation_text += confrontation

    else:  # reply for premise group
        if is_okay:
            confrontation_text = author + ' ' + _t.get(_.agreesThat)
            confrontation_text += ' XYZZYX, '
            confrontation_text += _t.get(_.strongerStatementForM) if gender is 'm' else _t.get(_.strongerStatementForF)
        else:
            confrontation_text = _t.get(_.otherParticipantsDontHaveOpinion)
            confrontation_text += ' XYZZYX, '
            confrontation_text += _t.get(_.strongerStatementForP)

        confrontation_text = confrontation_text.replace('XYZZYX', premise)

        confrontation_text += ' ' + start_argument
        confrontation_text += _t.get(_.accepting) if user_is_attacking else _t.get(_.rejecting)

        tmp = _t.get(_.strongerStatementEnd)
        if tmp == '':
            tmp += ' '
            conclusion = conclusion[len(start_argument):]

        confrontation_text += ' ' + conclusion + end_tag + '. '
        confrontation_text += (_t.get(_.heSays) if gender is 'm' else _t.get(_.sheSays)) if is_okay else _t.get(_.theySay)
        confrontation_text += ' ' if lang == 'de' else ': '
        confrontation_text += confrontation

    return confrontation_text, gender if is_okay else ''


def __get_name_link_of_arguments_author(main_page, argument, nickname):
    """
    Get the first author, who wrote or agreed with the argument

    :param main_page:
    :param argument:
    :param nickname:
    :return:
    """
    text, is_okay = get_author_data(main_page, argument.author_uid, False, True)
    db_user = DBDiscussionSession.query(User).filter_by(uid=argument.author_uid).first()
    gender = db_user.gender if db_user else 'n'

    db_anonymous_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()

    # if the data of arguments author is not okay, get the first user, who agrees with the argument
    if argument.author_uid == db_anonymous_user.uid or not is_okay:
        # get nick of current user
        nickname = nickname if nickname is not None else nick_of_anonymous_user
        db_current_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        # get all valid up votes
        db_vote = DBDiscussionSession.query(VoteArgument).filter(and_(
            VoteArgument.author_uid != db_anonymous_user.uid,
            VoteArgument.argument_uid == argument.uid,
            VoteArgument.is_valid == True,
            VoteArgument.is_up_vote == True
        ))

        if db_current_user:
            db_vote = db_vote.filter(VoteArgument.author_uid != db_current_user.uid)

        db_vote = db_vote.order_by(VoteArgument.uid.desc()).first()

        if db_vote:
            text, is_okay = get_author_data(main_page, db_vote.author_uid, False, True)
            db_user = DBDiscussionSession.query(User).filter_by(uid=db_vote.author_uid).first()
            gender = db_user.gender if db_user else 'n'
        else:
            return '', '', False

    return text if is_okay else '', gender, is_okay


def __get_name_link_of_arguments_author_with_statement_agree(main_page, argument, statement, nickname):
    """

    :param main_page:
    :param argument:
    :param statement:
    :param nickname:
    :return:
    """

    # grep all participants who agree with the users premise
    db_statement_votes = DBDiscussionSession.query(VoteStatement).filter(and_(
        VoteStatement.statement_uid == statement.uid,
        VoteStatement.is_valid == True,
        VoteStatement.is_up_vote == True
    )).all()
    statement_agrees = [s.author_uid for s in db_statement_votes]

    nickname = nickname if nickname is not None else nick_of_anonymous_user
    db_current_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_current_user.uid in statement_agrees:
        statement_agrees.remove(db_current_user.uid)

    # grep all participants who agree with system counter argument
    db_argument_votes = DBDiscussionSession.query(VoteArgument).filter(and_(
        VoteArgument.argument_uid == argument.uid,
        VoteArgument.is_valid == True,
        VoteArgument.is_up_vote == True
    )).all()

    # grep the set of participants who agree with counter and users premise
    votes = [v for v in db_argument_votes if v.author_uid in statement_agrees]

    # get data
    text = ''
    is_okay = False
    gender = 'n'
    for vote in votes:
        text, is_okay = get_author_data(main_page, vote.author_uid, False, True)
        if is_okay:
            db_user = DBDiscussionSession.query(User).filter_by(uid=vote.author_uid).first()
            gender = db_user.gender if db_user else 'n'
            break

    return text, gender, is_okay
