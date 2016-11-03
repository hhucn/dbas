#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Premise, Statement, VoteStatement

from .keywords import Keywords as _
from .translator import Translator


class TextGenerator(object):
    """
    Generates text for D-BAS
    """
    tag_type = 'span'

    def __init__(self, lang):
        """
        Sets current language

        :param lang: current language
        :return:
        """
        self.lang = lang

    def get_text_for_add_premise_container(self, confrontation, premise, attack_type, conclusion, is_supportive):
        """
        Based on the users reaction, text will be build. This text can be used for the container where users can
        add their statements

        :param confrontation: choosen confrontation
        :param premise: current premise
        :param attack_type: type of the attack
        :param conclusion: current conclusion
        :param is_supportive: boolean
        :return: string
        """
        _t = Translator(self.lang)

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

    def get_header_for_users_confrontation_response(self, premise, attack_type, conclusion, start_lower_case,
                                                    is_supportive, is_logged_in):
        """
        Based on the users reaction, text will be build. This text can be used for the speech bubbles where users
        justify an argument they have choosen.

        :param premise: current premise
        :param attack_type: type of the attack
        :param conclusion: current conclusion
        :param start_lower_case: boolean
        :param is_supportive: boolean
        :param is_logged_in: boolean
        :return: string
        """
        _t         = Translator(self.lang)
        system_msg = ''
        premise    = premise[0:1].lower() + premise[1:]
        if self.lang != 'de':
            conclusion = conclusion[0:1].lower() + conclusion[1:]

        if premise[-1] == '.':
            premise = premise[:-1]

        if conclusion[-1] == '.':
            conclusion = conclusion[:-1]

        # pretty print
        #  w = (_t.get(_.wrong)[0:1].lower() if start_lower_case else _t.get(_.wrong)[0:1].upper()) + _t.get(_.wrong)[1:] + ', '
        r = (_t.get(_.right)[0:1].lower() if start_lower_case else _t.get(_.right)[0:1].upper()) + _t.get(_.right)[
                                                                                                   1:] + ', '
        f = (_t.get(_.itIsFalseThat)[0:1].lower() if start_lower_case else _t.get(_.itIsFalseThat)[
                                                                           0:1].upper()) + _t.get(_.itIsFalseThat)[1:]
        t = (_t.get(_.itIsTrueThat)[0:1].lower() if start_lower_case else _t.get(_.itIsTrueThat)[0:1].upper()) + _t.get(
            _.itIsTrueThat)[1:]

        if self.lang == 'de':
            r += _t.get(_.itIsTrueThat)[0:1].lower() + _t.get(_.itIsTrueThat)[1:] + ' '
            f = _t.get(_.wrong) + ', ' + _t.get(_.itIsFalseThat)[0:1].lower() + _t.get(_.itIsFalseThat)[1:] + ' '

        # different cases
        user_msg = self.__get_user_msg_for_users_confrontation_response(attack_type, premise, conclusion, f, t, r, is_supportive, _t)
        if not user_msg:
            user_msg = ''

        # is logged in?
        if is_logged_in:
            system_msg = _t.get(_.canYouGiveAReasonForThat)

        return user_msg, system_msg

    def __get_user_msg_for_users_confrontation_response(self, attack_type, premise, conclusion, f, t, r, is_supportive, _t):
        # different cases
        if attack_type == 'undermine':
            return self.__get_user_msg_for_users_undermine_response(premise, f)

        if attack_type == 'support':
            return self.__get_user_msg_for_users_support_response(conclusion, t, f, is_supportive, _t)

        if attack_type == 'undercut':
            return self.__get_user_msg_for_users_undercut_response(premise, conclusion, r, is_supportive, _t)

        if attack_type == 'overbid':
            return self.__get_user_msg_for_users_overbid_response(premise, r, conclusion, is_supportive, _t)

        if attack_type == 'rebut':
            return self.__get_user_msg_for_users_rebut_response(premise, conclusion, r, is_supportive, _t)

    def __get_user_msg_for_users_undermine_response(self, premise, f):
        return f + ' ' + premise + '.'

    def __get_user_msg_for_users_support_response(self, conclusion, t, f, is_supportive, _t):
        user_msg = t if is_supportive else f
        user_msg += ' ' + conclusion + ' '
        user_msg += _t.get(_.hold) if is_supportive else _t.get(_.doesNotHold)
        user_msg += '.'
        return user_msg

    def __get_user_msg_for_users_undercut_response(self, premise, conclusion, r, is_supportive, _t):
        user_msg = r + premise + ', '
        user_msg += _t.get(_.butIDoNotBelieveArgumentFor) if is_supportive else _t.get(_.butIDoNotBelieveCounterFor)
        user_msg += ' ' + conclusion + '.'
        return user_msg

    def __get_user_msg_for_users_overbid_response(self, premise, r, conclusion, is_supportive, _t):
        user_msg = r + premise + ', '
        user_msg += _t.get(_.andIDoBelieveCounterFor) if is_supportive else _t.get(_.andIDoBelieveArgument)
        user_msg += ' ' + conclusion + '. '
        user_msg += _t.get(_.howeverIHaveEvenStrongerArgumentAccepting) if is_supportive else _t.get(
            _.howeverIHaveEvenStrongerArgumentRejecting)
        user_msg += ' ' + conclusion + '.'
        return user_msg

    def __get_user_msg_for_users_rebut_response(self, premise, conclusion, r, is_supportive, _t):
        user_msg = r + premise + ', '
        user_msg += _t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat)
        user_msg += ' ' + conclusion + '. '
        user_msg += _t.get(_.howeverIHaveMuchStrongerArgumentRejectingThat) if is_supportive else _t.get(
            _.howeverIHaveMuchStrongerArgumentAcceptingThat)
        user_msg += ' ' + conclusion + '.'
        return user_msg

    def get_relation_text_dict_without_substitution(self, start_lower_case, with_no_opinion_text, is_attacking, premise,
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
        return self.__get_relation_text_dict(start_lower_case, with_no_opinion_text, is_attacking, premise, conclusion,
                                             is_dont_know, first_conclusion, for_island_view, attack_type)

    def get_relation_text_dict_with_substitution(self, start_lower_case, with_no_opinion_text, is_attacking,
                                                 is_dont_know=False, first_conclusion=None, for_island_view=False,
                                                 attack_type=None):
        """

        :param start_lower_case:
        :param with_no_opinion_text:
        :param is_attacking:
        :param is_dont_know:
        :param first_conclusion:
        :param for_island_view:
        :param attack_type:
        :return:
        """
        _t = Translator(self.lang)
        if not is_dont_know:
            premise = _t.get(_.theirArgument)
            if attack_type == 'undermine' or attack_type == 'rebut':
                conclusion = _t.get(_.theirPosition)
            else:
                conclusion = _t.get(_.myArgument)
        else:
            premise = _t.get(_.thisArgument)
            conclusion = _t.get(_.opinion)

        return self.__get_relation_text_dict(start_lower_case, with_no_opinion_text, is_attacking, premise, conclusion,
                                             is_dont_know, first_conclusion, for_island_view, attack_type)

    def __get_relation_text_dict(self, start_lower_case, with_no_opinion_text, is_attacking, premise, conclusion,
                                 is_dont_know=False, first_conclusion=None, for_island_view=False, attack_type=None):
        """
        Text of the different reaction types for an given argument

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
        _t = Translator(self.lang)
        ret_dict = dict()

        if first_conclusion and first_conclusion[-1] == '.':
            first_conclusion = first_conclusion[:-1]

        # adding tags
        start_attack = '<' + self.tag_type + ' data-argumentation-type="attack">'
        start_argument = '<' + self.tag_type + ' data-argumentation-type="argument">'
        start_position = '<' + self.tag_type + ' data-argumentation-type="position">'
        end_tag = '</' + self.tag_type + '>'
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
        ret_dict['undercut_text'] += ' ' + conclusion + (' ist.' if self.lang == 'de' else '.')

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
        ret_dict['rebut_text'] += ' ' + conclusion + (' ist. ' if self.lang == 'de' else '. ')
        ret_dict['rebut_text'] += _t.get(_.howeverIHaveMuchStrongerArgument) + ' '
        ret_dict['rebut_text'] += start_argument if is_dont_know else start_position
        ret_dict['rebut_text'] += _t.get(_.rejecting if is_dont_know else _.accepting)
        # ret_dict['rebut_text'] += _t.get(_.accepting if is_attacking else _.rejecting)
        ret_dict['rebut_text'] += ' ' + (first_conclusion if first_conclusion else conclusion) + end_tag + '.'
        # + (_t.get(_.doesNotHold) if is_attacking else _t.get(_.hold)) + '.'

        if for_island_view and self.lang == 'de':
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

    def get_jump_to_argument_text_list(self):
        """

        :return: Array with [Conclusion is (right, wrong), Premise is (right, wrong), Premise does not lead to the conclusion, both hold]
        """
        _t = Translator(self.lang)
        tag_premise = '<' + TextGenerator.tag_type + ' data-argumentation-type="argument">'
        tag_conclusion = '<' + TextGenerator.tag_type + ' data-argumentation-type="attack">'
        tag_end = '</' + TextGenerator.tag_type + '>'
        premise = tag_premise + (_t.get(_.reason).lower() if self.lang != 'de' else _t.get(_.reason)) + tag_end
        conclusion = tag_conclusion + (
            _t.get(_.assertion).lower() if self.lang != 'de' else _t.get(_.assertion)) + tag_end

        answers = list()

        answers.append(_t.get(_.jumpAnswer0).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
        answers.append(_t.get(_.jumpAnswer1).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
        answers.append(_t.get(_.jumpAnswer2).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))
        answers.append(_t.get(_.jumpAnswer3).replace('XXCONCLUSIONXX', conclusion).replace('XXPREMISEXX', premise))

        return answers

    def get_text_for_confrontation(self, premise, conclusion, sys_conclusion, supportive, attack, confrontation,
                                   reply_for_argument, user_is_attacking, user_arg, sys_arg, color_html=True):
        """
        Text for the confrontation of the system

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
        _t = Translator(self.lang)

        #  build some confrontation text
        if self.lang != 'de':
            confrontation   = confrontation[0:1].lower() + confrontation[1:]
            premise         = premise[0:1].lower() + premise[1:]
            sys_conclusion  = sys_conclusion[0:1].lower() + sys_conclusion[1:]
            conclusion      = conclusion[0:1].lower() + conclusion[1:]

        # adding tags
        start_attack = ('<' + self.tag_type + ' data-argumentation-type="attack">') if color_html else ''
        start_argument = ('<' + self.tag_type + ' data-argumentation-type="argument">') if color_html else ''
        start_position = ('<' + self.tag_type + ' data-argumentation-type="position">') if color_html else ''
        end_tag = '</' + self.tag_type + '>'
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
        db_votes = DBDiscussionSession.query(VoteStatement).filter_by(statement_uid=db_users_premise.statements.uid).all()

        # build some confrontation text
        if attack == 'undermine':
            confrontation_text = self.__get_confrontation_text_for_undermine(premise, _t, start_position, start_argument,
                                                                             attack, sys_arg, end_tag, confrontation)

        elif attack == 'undercut':
            confrontation_text = self.__get_confrontation_text_for_undercut(db_votes, _t, premise, conclusion,
                                                                            confrontation, supportive)

        elif attack == 'rebut':
            confrontation_text = self.__get_confrontation_text_for_rebut(reply_for_argument, user_arg, user_is_attacking,
                                                                         _t, sys_conclusion, confrontation, premise,
                                                                         conclusion, start_argument, end_tag, db_votes,
                                                                         [color_html, start_argument])

        sys_text = confrontation_text + '.<br><br>' + _t.get(_.whatDoYouThinkAboutThat) + '?'
        return sys_text

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    def __get_text_dict_for_attacks_only(self, premises, conclusion, start_lower_case):
        """

        :param premises: String
        :param conclusion: String
        :param start_lower_case: Boolean
        :return: dict()
        """
        _t = Translator(self.lang)
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

    def __get_confrontation_text_for_undermine(self, premise, _t, start_position, start_argument, attack, sys_arg,
                                               end_tag, confrontation):
        """

        :param premise:
        :param _t:
        :param start_position:
        :param start_argument:
        :param attack:
        :param sys_arg:
        :param end_tag:
        :param confrontation:
        :return:
        """
        confrontation_text = _t.get(_.otherParticipantsThinkThat) + ' ' + premise + ' '
        confrontation_text += start_position if attack != 'undermine' else start_argument
        confrontation_text += _t.get(_.hold) if sys_arg.is_supportive else _t.get(_.doesNotHold)
        confrontation_text += end_tag
        confrontation_text += ', ' + _t.get(_.because).lower() + ' ' + confrontation
        return confrontation_text

    def __get_confrontation_text_for_rebut(self, reply_for_argument, user_arg, user_is_attacking, _t, sys_conclusion,
                                           confrontation, premise, conclusion, start_argument, end_tag, db_votes,
                                           color_html=[False, '']):
        """
        Builds the string for a rebut of the system.

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
        :param db_votes: Votes
        :param color_html: [Boolean, String]
        :return: String
        """
        # distinguish between reply for argument and reply for premise group
        if reply_for_argument:  # reply for argument
            # changing arguments for better understanding
            if not user_arg.is_supportive:
                user_is_attacking = not user_is_attacking
                conclusion = sys_conclusion

            confrontation_text = color_html[1] if color_html[0] else ''
            if user_is_attacking:
                confrontation_text += _t.get(_.otherUsersClaimStrongerArgumentRejecting)
            else:
                confrontation_text += _t.get(_.otherUsersClaimStrongerArgumentAccepting)
            confrontation_text += ' ' + conclusion + (end_tag if color_html[0] else '') + '.' + ' ' + _t.get(_.theySay)
            confrontation_text += ' ' if self.lang == 'de' else ': '
            confrontation_text += confrontation
        else:  # reply for premise group
            confrontation_text = _t.get(_.otherParticipantsAgreeThat) if len(db_votes) > 1 else _t.get(
                _.otherParticipantsDontHaveOpinion)
            confrontation_text += ' ' + premise + ', '
            tmp = _t.get(_.strongerStatementForAccepting1 if user_is_attacking else _.strongerStatementForRecjecting1)
            tmp += start_argument
            tmp += _t.get(_.strongerStatementForAccepting2 if user_is_attacking else _.strongerStatementForRecjecting2)
            if (_t.get(
                    _.strongerStatementForAccepting3 if user_is_attacking else _.strongerStatementForRecjecting3)) == '':
                tmp += ' '
                conclusion = conclusion[len(start_argument):]
            else:
                tmp += end_tag + ' '
                tmp += _t.get(
                    _.strongerStatementForAccepting3 if user_is_attacking else _.strongerStatementForRecjecting3) + ' '
            confrontation_text += tmp
            confrontation_text += conclusion + '.' + ' '
            confrontation_text += _t.get(_.theySay)
            confrontation_text += ' ' if self.lang == 'de' else ': '
            confrontation_text += confrontation
        return confrontation_text

    def __get_confrontation_text_for_undercut(self, db_votes, _t, premise, conclusion, confrontation, supportive):
        """

        :param db_votes:
        :param _t:
        :param premise:
        :param conclusion:
        :param confrontation:
        :param supportive:
        :return:
        """
        confrontation_text = _t.get(_.otherParticipantsAgreeThat) if len(db_votes) > 1 else _t.get(
            _.otherParticipantsDontHaveOpinion)
        confrontation_text += ' ' + premise + ', '
        confrontation_text += (
            _t.get(_.butTheyDoNotBelieveArgument) if supportive else _t.get(_.butTheyDoNotBelieveCounter))
        confrontation_text += ' ' + conclusion
        if self.lang == 'de':
            confrontation_text += '. ' + _t.get(_.theyThink)
        else:
            confrontation_text += ', ' + _t.get(_.because).lower() + ' ' + _t.get(_.theyThink).lower()
        confrontation_text += ' ' if self.lang == 'de' else ': '
        confrontation_text += confrontation
        return confrontation_text
