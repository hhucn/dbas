#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbas.database.discussion_model import Premise, Statement, VoteStatement
from dbas.database import DBDiscussionSession
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
            ret_text = _t.get(_t.itIsFalseThat) + ' ' + premise
        if attack_type == 'support':
            ret_text = _t.get(_t.itIsTrueThat) if is_supportive else _t.get(_t.itIsFalseThat)
            ret_text += ' ' + conclusion + ' '
            ret_text += _t.get(_t.hold) if is_supportive else _t.get(_t.doesNotHold)
        if attack_type == 'undercut':
            ret_text = confrontation + ', ' + _t.get(_t.butIDoNotBelieveCounterFor) + ' ' + conclusion
        if attack_type == 'overbid':
            ret_text = confrontation + ', ' + _t.get(_t.andIDoBelieveCounterFor) + ' ' + conclusion
        #  + '.' + _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) + ' ' + longConclusion + '.'
        if attack_type == 'rebut':
            ret_text = confrontation + ' ' \
                       + (_t.get(_t.iAcceptCounterThat) if is_supportive else _t.get(_t.iAcceptArgumentThat)) \
                       + ' ' + conclusion

        return ret_text + ', '  + _t.get(_t.because).lower() + '...'

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
        user_msg   = ''
        system_msg = ''
        premise    = premise[0:1].lower() + premise[1:]
        if self.lang != 'de':
            conclusion = conclusion[0:1].lower() + conclusion[1:]

        if premise[-1] == '.':
            premise = premise[:-1]

        if conclusion[-1] == '.':
            conclusion = premise[:-1]

        # pretty print
        #  w = (_t.get(_t.wrong)[0:1].lower() if start_lower_case else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:] + ', '
        r = (_t.get(_t.right)[0:1].lower() if start_lower_case else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:] + ', '
        f = (_t.get(_t.itIsFalseThat)[0:1].lower() if start_lower_case else _t.get(_t.itIsFalseThat)[0:1].upper()) + _t.get(_t.itIsFalseThat)[1:]
        t = (_t.get(_t.itIsTrueThat)[0:1].lower() if start_lower_case else _t.get(_t.itIsTrueThat)[0:1].upper()) + _t.get(_t.itIsTrueThat)[1:]

        if self.lang == 'de':
            r += _t.get(_t.itIsTrueThat)[0:1].lower() + _t.get(_t.itIsTrueThat)[1:] + ' '
            f = _t.get(_t.wrong) + ', ' + _t.get(_t.itIsFalseThat)[0:1].lower() + _t.get(_t.itIsFalseThat)[1:] + ' '

        # different cases
        if attack_type == 'undermine':
            user_msg = f + ' ' + premise + '.'

        if attack_type == 'support':
            user_msg = t if is_supportive else f
            user_msg += ' ' + conclusion + ' '
            user_msg += _t.get(_t.hold) if is_supportive else _t.get(_t.doesNotHold)
            user_msg += '.'

        if attack_type == 'undercut':
            user_msg = r + premise + ', '
            user_msg += _t.get(_t.butIDoNotBelieveCounterFor) if is_supportive else _t.get(_t.butIDoNotBelieveArgumentFor)
            user_msg += ' ' + conclusion + '.'

        if attack_type == 'overbid':
            user_msg = r + premise + ', '
            user_msg += _t.get(_t.andIDoBelieveCounterFor) if is_supportive else _t.get(_t.andIDoBelieveArgument)
            user_msg += ' ' + conclusion + '. '
            user_msg += _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting) if is_supportive else _t.get(_t.howeverIHaveEvenStrongerArgumentRejecting)
            user_msg += ' ' + conclusion + '.'

        if attack_type == 'rebut':
            user_msg = r + premise + ', '
            user_msg += _t.get(_t.iAcceptCounterThat) if is_supportive else _t.get(_t.iAcceptArgumentThat)
            user_msg += ' ' + conclusion + '. '
            user_msg += _t.get(_t.howeverIHaveMuchStrongerArgumentRejectingThat) if is_supportive else _t.get(_t.howeverIHaveMuchStrongerArgumentAcceptingThat)
            user_msg += ' ' + conclusion + '.'

        # is logged in?
        if is_logged_in:
            system_msg  = _t.get(_t.canYouGiveAReasonForThat)

        return user_msg, system_msg

    def get_relation_text_dict(self, start_lower_case, with_no_opinion_text, is_attacking, is_dont_know=False,
                               first_conclusion=None, for_island_view=False, attack_type=None):
        """
        Text of the different reaction types for an given argument

        :param start_lower_case: Boolean
        :param with_no_opinion_text: Boolean
        :param is_attacking: Boolean
        :param is_dont_know: Boolean
        :param first_conclusion: String
        :param for_island_view: Boolean
        :return: dict()
        """
        _t = Translator(self.lang)
        ret_dict = dict()

        if first_conclusion and first_conclusion[-1] == '.':
            first_conclusion = first_conclusion[:-1]

        if not is_dont_know:
            premise = _t.get(_t.theirArgument)
            if attack_type == 'undermine' or attack_type == 'rebut':
                conclusion = _t.get(_t.theirPosition)
            else:
                conclusion = _t.get(_t.myArgument)
        else:
            premise = _t.get(_t.thisArgument)
            conclusion = _t.get(_t.opinion)

        # adding tags
        start_attack = '<' + self.tag_type + ' data-argumentation-type="attack">'
        start_argument = '<' + self.tag_type + ' data-argumentation-type="argument">'
        start_position = '<' + self.tag_type + ' data-argumentation-type="position">'
        end_tag = '</' + self.tag_type + '>'
        premise = start_attack + premise + end_tag
        conclusion = start_argument + conclusion + end_tag

        w = (_t.get(_t.wrong)[0:1].lower() if start_lower_case else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
        r = (_t.get(_t.right)[0:1].lower() if start_lower_case else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]

        w += ', ' + _t.get(_t.itIsFalse1) + ' '
        r += ', ' + _t.get(_t.itIsTrue1) + ' '

        ret_dict['undermine_text'] = w + premise + ' ' + _t.get(_t.itIsFalse2) + '.'

        ret_dict['support_text'] = r + premise + _t.get(_t.itIsTrue2) + '.'

        # tmp = _t.get(_t.butIDoNotBelieveCounter) if is_attacking else _t.get(_t.butIDoNotBelieveArgument)
        tmp = _t.get(_t.butIDoNotBelieveArgument) if not is_attacking or not attack_type == 'undercut' else _t.get(_t.butIDoNotBelieveCounter)
        ret_dict['undercut_text'] = r + premise + _t.get(_t.itIsTrue2) + ', '
        ret_dict['undercut_text'] += (_t.get(_t.butIDoNotBelieveArgumentFor) if is_dont_know else tmp)
        ret_dict['undercut_text'] += ' ' + conclusion + (' ist.' if self.lang == 'de' else '.')

        ret_dict['overbid_text'] = r + premise + _t.get(_t.itIsTrue2) + ', '
        ret_dict['overbid_text'] += (_t.get(_t.andIDoBelieveArgument) if is_dont_know else _t.get(_t.andIDoBelieveCounterFor))
        ret_dict['overbid_text'] += ' ' + conclusion + '. '
        ret_dict['overbid_text'] += (_t.get(_t.howeverIHaveEvenStrongerArgumentRejecting) if is_attacking else _t.get(_t.howeverIHaveEvenStrongerArgumentAccepting))
        ret_dict['overbid_text'] += ' ' + conclusion + '.'

        ret_dict['rebut_text'] = r + premise + _t.get(_t.itIsTrue2) + ' '
        # ret_dict['rebut_text'] += (_t.get(_t.iAcceptCounter) if is_attacking else _t.get(_t.iAcceptArgument))
        ret_dict['rebut_text'] += _t.get(_t.iAcceptArgument) if not is_attacking or not attack_type == 'undercut' else _t.get(_t.iAcceptCounter)
        ret_dict['rebut_text'] += ' ' + conclusion + (' ist. ' if self.lang == 'de' else '. ')
        ret_dict['rebut_text'] += _t.get(_t.howeverIHaveMuchStrongerArgument) + ' '
        ret_dict['rebut_text'] += start_argument if is_dont_know else start_position
        ret_dict['rebut_text'] += _t.get(_t.rejecting if is_dont_know else _t.accepting)
        # ret_dict['rebut_text'] += _t.get(_t.accepting if is_attacking else _t.rejecting)
        ret_dict['rebut_text'] += ' ' + (first_conclusion if first_conclusion else conclusion) + end_tag + '.'
        # + (_t.get(_t.doesNotHold) if is_attacking else _t.get(_t.hold)) + '.'

        if for_island_view and self.lang == 'de':
            ret_dict['undermine_text'] = ret_dict['undermine_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['support_text'] = ret_dict['support_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['undercut_text'] = ret_dict['undercut_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['overbid_text'] = ret_dict['overbid_text'][:-1] + ', ' + _t.get(_t.because).lower()
            ret_dict['rebut_text'] = ret_dict['rebut_text'][:-1] + ', ' + _t.get(_t.because).lower()

        if with_no_opinion_text:
            ret_dict['step_back_text'] = _t.get(_t.iHaveNoOpinion) + '. ' + _t.get(_t.goStepBack) + '. (' + _t.get(_t.noOtherAttack) + ')'
            ret_dict['no_opinion_text'] = _t.get(_t.iHaveNoOpinion) + '. ' + _t.get(_t.showMeAnotherArgument) + '.'

        return ret_dict

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

        sys_text = confrontation_text + '.<br><br>' + _t.get(_t.whatDoYouThinkAboutThat) + '?'
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
        content = _t.get(_t.textversionChangedContent) + ' ' + nickname
        content += nl + (_t.get(_t.fromm)[0:1].upper() + _t.get(_t.fromm)[1:]) + ': ' + original + nl
        content += (_t.get(_t.to)[0:1].upper() + _t.get(_t.to)[1:]) + ': ' + edited + nl
        content += (_t.get(_t.where)[0:1].upper() + _t.get(_t.where)[1:]) + ': '
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
        content = _t.get(_t.statementAddedMessageContent) + nl
        content += (_t.get(_t.where)[0:1].upper() + _t.get(_t.where)[1:]) + ': '
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
        content = _t.get(_t.statementAddedMessageContent) + nl
        content += (_t.get(_t.where)[0:1].upper() + _t.get(_t.where)[1:]) + ': '
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
            premise += premises[p]['text'] + _t.get(_t.aand)
        premise = premise[0:-4]

        w = (_t.get(_t.wrong)[0:1].lower() if start_lower_case else _t.get(_t.wrong)[0:1].upper()) + _t.get(_t.wrong)[1:]
        r = (_t.get(_t.right)[0:1].lower() if start_lower_case else _t.get(_t.right)[0:1].upper()) + _t.get(_t.right)[1:]
        counter_justi = ' ' + conclusion + ', ' + _t.get(_t.because).toLocaleLowerCase() + ' ' + premise

        ret_dict['undermine_text'] = w + ', ' + premise + '.'
        ret_dict['undercut_text'] = r + ', ' + conclusion + ', ' + _t.get(_t.butIDoNotBelieveArgumentFor) + ' ' + counter_justi + '.'
        ret_dict['rebut_text'] = r + ', ' + premise + ' ' + _t.get(_t.iAcceptArgumentThat) + ' ' + conclusion + '. '\
                                 + _t.get(_t.howeverIHaveMuchStrongerArgumentRejectingThat) + ' ' + conclusion + '.'
        ret_dict['no_opinion_text'] = _t.get(_t.iNoOpinion) + ': ' + conclusion + ', ' + _t.get(_t.because).toLocaleLowerCase() \
                                      + ' ' + premise + '. ' + _t.get(_t.goStepBack) + '.'
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
        confrontation_text = _t.get(_t.otherParticipantsThinkThat) + ' ' + premise + ' '
        confrontation_text += start_position if attack != 'undermine' else start_argument
        confrontation_text += _t.get(_t.hold) if sys_arg.is_supportive else _t.get(_t.doesNotHold)
        confrontation_text += end_tag
        confrontation_text += ', ' + _t.get(_t.because).lower() + ' ' + confrontation
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
                confrontation_text += _t.get(_t.otherUsersClaimStrongerArgumentRejecting)
            else:
                confrontation_text += _t.get(_t.otherUsersClaimStrongerArgumentAccepting)
            confrontation_text += ' ' + conclusion + (end_tag if color_html[0] else '') + '.' + ' ' + _t.get(_t.theySay)
            confrontation_text += ' ' if self.lang == 'de' else ': '
            confrontation_text += confrontation
        else:  # reply for premise group
            confrontation_text = _t.get(_t.otherParticipantsAgreeThat) if len(db_votes) > 1 else _t.get(_t.otherParticipantsDontHaveOpinion)
            confrontation_text += ' ' + premise + ', '
            tmp = _t.get(_t.strongerStatementForAccepting1 if user_is_attacking else _t.strongerStatementForRecjecting1)
            tmp += start_argument
            tmp += _t.get(_t.strongerStatementForAccepting2 if user_is_attacking else _t.strongerStatementForRecjecting2)
            if (_t.get(_t.strongerStatementForAccepting3 if user_is_attacking else _t.strongerStatementForRecjecting3)) == '':
                tmp += ' '
                conclusion = conclusion[len(start_argument):]
            else:
                tmp += end_tag + ' '
                tmp += _t.get(_t.strongerStatementForAccepting3 if user_is_attacking else _t.strongerStatementForRecjecting3) + ' '
            confrontation_text += tmp
            confrontation_text += conclusion + '.' + ' '
            confrontation_text += _t.get(_t.theySay)
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
        confrontation_text = _t.get(_t.otherParticipantsAgreeThat) if len(db_votes) > 1 else _t.get(_t.otherParticipantsDontHaveOpinion)
        confrontation_text += ' ' + premise + ', '
        confrontation_text += (_t.get(_t.butTheyDoNotBelieveArgument) if supportive else _t.get(_t.butTheyDoNotBelieveCounter))
        confrontation_text += ' ' + conclusion
        if self.lang == 'de':
            confrontation_text += '. ' + _t.get(_t.theyThink)
        else:
            confrontation_text += ', ' + _t.get(_t.because).lower() + ' ' + _t.get(_t.theyThink).lower()
        confrontation_text += ' ' if self.lang == 'de' else ': '
        confrontation_text += confrontation
        return confrontation_text