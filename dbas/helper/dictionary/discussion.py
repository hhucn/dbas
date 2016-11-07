"""
Provides helping function for dictionaries, which are used in discussions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import dbas.helper.history as HistoryHelper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, \
    get_text_for_conclusion, create_speechbubble_dict, is_author_of_argument
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import TextGenerator
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager


class DiscussionDictHelper(object):
    """
    Provides all functions for creating the discussion dictionaries with all bubbles.
    """

    def __init__(self, lang, session_id, nickname=None, history='', main_page='', slug=''):
        """
        Initialize default values

        :param lang: ui_locales
        :param session_id: request.session_id
        :param nickname: self.request.authenticated_userid
        :param history: history
        :param main_page: String
        :param slug: String
        :return:
        """
        self.lang = lang
        self.session_id = session_id
        self.nickname = nickname
        self.history = history
        self.main_page = main_page
        self.slug = slug

    def get_dict_for_start(self):
        """
        Prepares the discussion dict with all bubbles for the first step in discussion, where the user chooses a position.

        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_start', 'at_start')
        _tn                    = Translator(self.lang)
        add_premise_text = _tn.get(_.whatIsYourIdea)
        intro = _tn.get(_.initialPositionInterest)
        save_statement_url  = 'ajax_set_new_start_premise'

        start_bubble = create_speechbubble_dict(is_system=True, uid='start', message=intro, omit_url=True, lang=self.lang)
        bubbles_array = [start_bubble]

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

    def get_dict_for_attitude(self, uid):
        """
        Prepares the discussion dict with all bubbles for the second step in discussion, where the user chooses her attitude.

        :param uid: Argument.uid
        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_attitude', 'at_attitude')
        _tn                    = Translator(self.lang)
        add_premise_text    = ''
        save_statement_url  = 'ajax_set_new_start_statement'
        statement_text      = get_text_for_statement_uid(uid, True)
        if not statement_text:
            return None
        if self.lang != 'de':
            l = len('<' + TextGenerator.tag_type + ' data-argumentation-type="position">')
            statement_text = statement_text[0:l + 1].lower() + statement_text[l + 1:]

        text = _tn.get(_.whatDoYouThinkAbout)
        text += ' ' + statement_text + '?'
        # select_bubble = history_helper.create_speechbubble_dict(is_user=True, '', '', _tn.get(_.youAreInterestedIn) + ': <strong>' + statement_text + '</strong>', lang=self.lang)
        bubble = create_speechbubble_dict(is_system=True, message=text, omit_url=True, lang=self.lang)

        # if save_crumb:
        #     bubbles_array.append(select_bubble)
        #     self.__save_speechbubble(select_bubble, db_user, self.session_id, transaction, statement_uid=uid)
        bubbles_array = [bubble]

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

    def get_dict_for_justify_statement(self, uid, application_url, slug, is_supportive, count_of_items, nickname):
        """
        Prepares the discussion dict with all bubbles for the third step in discussion, where the user justifies his position.

        :param uid: Argument.uid
        :param application_url: URL
        :param slug: Issue.info as Slug
        :param is_supportive: Boolean
        :param count_of_items: Integer
        :param nickname: User.nickname
        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_justify_statement', 'at_justify')
        _tn = Translator(self.lang)

        bubbles_array       = HistoryHelper.create_bubbles_from_history(self.history, self.nickname, self. lang, self.main_page, self.slug)
        save_statement_url  = 'ajax_set_new_start_statement'
        text                = get_text_for_statement_uid(uid)
        if not text:
            return None

        tag_start = '<' + TextGenerator.tag_type + ' data-argumentation-type="position">'
        tag_end = '</' + TextGenerator.tag_type + '>'
        if self.lang == 'de':
            question = _tn.get(
                _.whatIsYourMostImportantReasonWhyForInColor if is_supportive
                else _.whatIsYourMostImportantReasonWhyAgainstInColor)
        else:
            question = _tn.get(_.whatIsYourMostImportantReasonWhyFor)
        question += ' ' + tag_start
        question += text[0:1].lower() if self.lang != 'de' else text[0:1].upper()
        question += text[1:] + tag_end

        if self.lang != 'de':
            question += ' ' + _tn.get(_.holdsInColor if is_supportive else _.isNotAGoodIdeaInColor)
        question += '?'
        because = _tn.get(_.because)[0:1].upper() + _tn.get(_.because)[1:].lower() + '...'

        if self.lang == 'de':
            intro = _tn.get(_.itIsTrueThat if is_supportive else _.itIsFalseThat)
            add_premise_text = intro[0:1].upper() + intro[1:] + ' ' + text
        else:
            add_premise_text = text + ' ' + _tn.get(_.holds if is_supportive else _.isNotAGoodIdea)
        add_premise_text += ', ' + _tn.get(_.because).lower() + '...'

        if self.lang == 'de':
            intro = _tn.get(_.youAgreeWith if is_supportive else _.iyouDisagreeWith) + ' '
        else:
            intro = '' if is_supportive else _tn.get(_.youDisagreeWith) + ': '

        splitted_history = self.history.split('-')
        if len(splitted_history) > 0:
            if '/undercut' in splitted_history[-1] or '/undermine' in splitted_history[-1] or '/rebut' in splitted_history[-1]:
                intro = _tn.get(_.youHaveMuchStrongerArgumentForAccepting) if is_supportive else _tn.get(
                    _.youHaveMuchStrongerArgumentForRejecting)
                intro += ': '

        url = UrlManager(application_url, slug).get_slug_url(False)
        question_bubble = create_speechbubble_dict(is_system=True, message=question + ' <br>' + because, omit_url=True, lang=self.lang)
        if not text.endswith(('.', '?', '!')):
            text += '.'
        select_bubble = create_speechbubble_dict(is_user=True, url=url, message=intro + text, omit_url=False,
                                                 statement_uid=uid, is_supportive=is_supportive, nickname=nickname,
                                                 lang=self.lang)

        bubbles_array.append(select_bubble)
        self.__append_now_bubble(bubbles_array)
        bubbles_array.append(question_bubble)

        if not self.nickname and count_of_items == 1:
            bubbles_array.append(create_speechbubble_dict(is_info=True, uid='now',
                                                          message=_tn.get(_.voteCountTextFirst) + '. ' + _tn.get(
                                                              _.onlyOneItemWithLink),
                                                          omit_url=True, lang=self.lang))

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'is_supportive': is_supportive}

    def get_dict_for_justify_argument(self, uid, is_supportive, attack):
        """
        Prepares the discussion dict with all bubbles for a step in discussion, where the user justifies his attack she has done.

        :param uid: Argument.uid
        :param is_supportive: Boolean
        :param attack: String (undermine, support, undercut, rebut, ...)
        :return: dict()
        """
        logger('DictionaryHelper', 'prepare_discussion_dict', 'get_dict_for_justify_argument')
        _tn                   = Translator(self.lang)
        _tg                = TextGenerator(self.lang)
        bubbles_array      = HistoryHelper.create_bubbles_from_history(self.history, self.nickname, self. lang, self.main_page, self.slug)
        add_premise_text   = ''
        save_statement_url = 'ajax_set_new_premises_for_argument'

        db_argument        = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
        if not db_argument:
            return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

        confr          = get_text_for_argument_uid(uid)
        premise, tmp   = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        conclusion     = get_text_for_conclusion(db_argument)

        user_msg, sys_msg = _tg.get_header_for_users_confrontation_response(premise, attack, conclusion, False, is_supportive, self.nickname)

        if attack == 'undermine':
            add_premise_text = _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
                                                                      db_argument.is_supportive)
            add_premise_text = add_premise_text[0:1].upper() + add_premise_text[1:]

        elif attack == 'support':
            is_supportive = not is_supportive
            # when the user rebuts a system confrontation, he attacks his own negated premise, therefore he supports
            # is own premise. so his premise is the conclusion and we need new premises ;-)
            add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion, is_supportive)
        elif attack == 'undercut':
            add_premise_text += _tg.get_text_for_add_premise_container(premise, premise, attack, conclusion,
                                                                       db_argument.is_supportive)
        else:
            add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
                                                                       db_argument.is_supportive)

        start = '<' + TextGenerator.tag_type + ' data-argumentation-type="position">'
        end = '</' + TextGenerator.tag_type + '>'
        user_msg = start + user_msg[:-1] + end

        sys_msg = _tn.get(_.whatIsYourMostImportantReasonFor) + ': ' + user_msg + '?<br>' + _tn.get(_.because) + '...'
        # bubble_user = history_helper.create_speechbubble_dict(is_user=True, message=user_msg[0:1].upper() + user_msg[1:], omit_url=True, lang=self.lang)

        self.__append_now_bubble(bubbles_array)
        bubbles_array.append(
            create_speechbubble_dict(is_system=True, message=sys_msg, omit_url=True, lang=self.lang))

        # if save_crumb:
        #     db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        #     self.__save_speechbubble(bubble_user, db_user, self.session_id, transaction, argument_uid=uid)
        #     self.__save_speechbubble(bubble_question, db_user, self.session_id, transaction)

        # if not self.nickname and count_of_items == 1:
        #     bubbles_array.append(history_helper.create_speechbubble_dict(is_status=True, 'now', '', _tn.get(_.onlyOneItemWithLink), True))

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'attack_type': attack, 'arg_uid': uid}

    def get_dict_for_dont_know_reaction(self, uid):
        """
        Prepares the discussion dict with all bubbles for the third step, where an supportive argument will be presented.

        :param uid: Argument.uid
        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_dont_know_reaction', 'at_dont_know')
        _tn = Translator(self.lang)
        bubbles_array = HistoryHelper.create_bubbles_from_history(self.history, self.nickname, self. lang, self.main_page, self.slug)
        add_premise_text = ''
        save_statement_url = 'ajax_set_new_start_statement'

        if uid != 0:
            text            = get_text_for_argument_uid(uid, rearrange_intro=True, attack_type='dont_know')
            sys_text = _tn.get(_.otherParticipantsThinkThat) + ' ' + text[0:1].lower() + text[1:] + '. '

            bubble_sys = create_speechbubble_dict(is_system=True, message=sys_text + '<br><br>' + _tn.get(
                _.whatDoYouThinkAboutThat) + '?')
            bubbles_array.append(bubble_sys)

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

    def get_dict_for_argumentation(self, uid, is_supportive, additional_uid, attack, history, nickname):
        """
        Prepares the discussion dict with all bubbles for the argumentation window.

        :param uid: Argument.uid
        :param is_supportive: Boolean
        :param additional_uid: Argument.uid
        :param attack: String (undermine, support, undercut, rebut, ...)
        :param history: History
        :param nickname: Users nickname
        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_argumentation', 'at_argumentation')
        _tn                    = Translator(self.lang)
        bubbles_array       = HistoryHelper.create_bubbles_from_history(self.history, self.nickname, self. lang, self.main_page, self.slug)
        add_premise_text    = ''
        save_statement_url  = 'ajax_set_new_start_statement'
        mid_text            = ''
        bubble_mid          = ''
        splitted_history    = HistoryHelper.get_splitted_history(self.history)
        user_changed_opinion = splitted_history[-1].endswith(str(uid))
        statement_list      = list()
        db_confrontation    = ''

        _tg                     = TextGenerator(self.lang)
        db_argument             = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()

        if attack.startswith('end'):
            #  user_text        = _tn.get(_.soYourOpinionIsThat) + ': '
            text             = get_text_for_argument_uid(uid, user_changed_opinion=user_changed_opinion, minimize_on_undercut=True)
            user_text        = text[0:1].upper() + text[1:]
            sys_text = (_tn.get(_.otherParticipantsDontHaveCounterForThat) + '.') if attack == 'end' else _tn.get(
                _.otherParticipantsDontHaveNewCounterForThat)
            mid_text = _tn.get(_.discussionEnd) + ' ' + _tn.get(_.discussionEndLinkText)
        else:
            premise, tmp     = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
            conclusion       = get_text_for_conclusion(db_argument)
            db_confrontation = DBDiscussionSession.query(Argument).filter_by(uid=additional_uid).first()
            confr, tmp       = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid)
            sys_conclusion   = get_text_for_conclusion(db_confrontation)
            if attack == 'undermine':
                if db_confrontation.conclusion_uid != 0:
                    premise = get_text_for_statement_uid(db_confrontation.conclusion_uid)
                else:
                    premise = get_text_for_argument_uid(db_confrontation.argument_uid, True, colored_position=True, attack_type=attack)

            # did the user changed his opinion?
            history = HistoryHelper.get_splitted_history(history)
            user_changed_opinion = len(history) > 1 and '/undercut/' in history[-2]

            # argumentation is a reply for an argument, if the arguments conclusion of the user is no position
            db_statement        = DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()
            reply_for_argument  = not (db_statement and db_statement.is_startpoint)
            current_argument    = get_text_for_argument_uid(uid, with_html_tag=True, colored_position=True,
                                                            user_changed_opinion=user_changed_opinion, attack_type=attack,
                                                            minimize_on_undercut=True)

            user_is_attacking   = not db_argument.is_supportive

            current_argument = current_argument[0:1].upper() + current_argument[1:]
            if self.lang != 'de':
                premise = premise[0:1].lower() + premise[1:]

            # check for support and build text
            user_text = (_tn.get(_.otherParticipantsConvincedYouThat) + ': ') if user_changed_opinion else ''
            user_text += current_argument if current_argument != '' else premise

            sys_text = _tg.get_text_for_confrontation(premise, conclusion, sys_conclusion, is_supportive, attack, confr,
                                                      reply_for_argument, user_is_attacking, db_argument, db_confrontation)

        bubble_user = create_speechbubble_dict(is_user=True, message=user_text, omit_url=True, argument_uid=uid,
                                               is_supportive=is_supportive, lang=self.lang, nickname=self.nickname)
        if attack.startswith('end'):
            bubble_sys  = create_speechbubble_dict(is_system=True, message=sys_text, omit_url=True, lang=self.lang)
            bubble_mid  = create_speechbubble_dict(is_info=True, message=mid_text, omit_url=True, lang=self.lang)
        else:
            uid = 'question-bubble-' + str(additional_uid) if int(additional_uid) > 0 else ''
            bubble_sys  = create_speechbubble_dict(is_system=True, uid=uid, message=sys_text, omit_url=True, lang=self.lang, is_flaggable=True, is_author=is_author_of_argument(nickname, db_confrontation.uid))
            statement_list = self.__get_all_statement_by_argument(db_confrontation)

        # dirty fixes
        if len(bubbles_array) > 0 and bubbles_array[-1]['message'] == bubble_user['message']:
            bubbles_array.remove(bubbles_array[-1])

        self.__append_now_bubble(bubbles_array)
        bubbles_array.append(bubble_user)
        bubbles_array.append(bubble_sys)

        if attack.startswith('end'):
            bubbles_array.append(bubble_mid)

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'extras': statement_list}

    def get_dict_for_jump(self, uid):
        """
        Prepares the discussion dict with all bubbles for the jump step

        :param uid: Argument.uid
        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_jump', 'argument ' + str(uid))
        _tn = Translator(self.lang)
        argument_text = get_text_for_argument_uid(uid, colored_position=True, with_html_tag=True, attack_type='jump')

        text = _tn.get(_.whatDoYouThinkAbout)
        text += ': ' + argument_text + '?'
        bubble = create_speechbubble_dict(is_system=True, message=text, omit_url=True, lang=self.lang)

        bubbles_array = [bubble]

        return {'bubbles': bubbles_array, 'add_premise_text': '', 'save_statement_url': '', 'mode': ''}

    def get_dict_for_jump_decision(self, uid):
        """
        Prepares the discussion dict with all bubbles for the jump decision step

        :param uid: Argument.uid
        :return: dict()
        """
        logger('DictionaryHelper', 'get_dict_for_jump_decision', 'at_attitude')
        _tn = Translator(self.lang)

        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
        tag_premise = '<' + TextGenerator.tag_type + ' data-argumentation-type="argument">'
        tag_conclusion = '<' + TextGenerator.tag_type + ' data-argumentation-type="attack">'
        tag_end = '</' + TextGenerator.tag_type + '>'
        premise, trash = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        premise = tag_premise + premise + tag_end
        conclusion = tag_conclusion + get_text_for_conclusion(db_argument) + tag_end
        aand = ' ' + _tn.get(_.aand) + ' '

        text = _tn.get(_.whatDoYouThinkAbout)
        text += ' ' + premise + aand + conclusion + '?'
        bubble = create_speechbubble_dict(is_system=True, message=text, omit_url=True, lang=self.lang)

        bubbles_array = [bubble]

        return {'bubbles': bubbles_array, 'add_premise_text': '', 'save_statement_url': '', 'mode': ''}

    def get_dict_for_choosing(self, uid, is_uid_argument, is_supportive):
        """
        Prepares the discussion dict with all bubbles for the choosing an premise, when the user inserted more than one new premise.

        :param uid: Argument.uid
        :param is_uid_argument: Boolean
        :param is_supportive: Boolean
        :return:
        """
        _tn = Translator(self.lang)
        bubbles_array = HistoryHelper.create_bubbles_from_history(self.history, self.nickname, self. lang, self.main_page, self.slug)
        add_premise_text = ''
        save_statement_url = 'ajax_set_new_start_statement'

        logger('DictionaryHelper', 'prepare_discussion_dict', 'at_choosing')
        text = _tn.get(_.soYouEnteredMultipleReasons) + '. '
        text += _tn.get(_.whyAreYouAgreeingWith) if is_supportive else _tn.get(_.whyAreYouDisagreeingWith)
        text += ':<br>'
        text += get_text_for_argument_uid(uid) if is_uid_argument else get_text_for_statement_uid(uid)
        text += '?<br>' + _tn.get(_.because) + '...'

        bubbles_array.append(
            create_speechbubble_dict(is_status=True, uid='now', message='Now', omit_url=True, lang=self.lang))
        bubbles_array.append(
            create_speechbubble_dict(is_user=True, uid='question-bubble', message=text, omit_url=True, lang=self.lang))

        return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

    def __get_all_statement_by_argument(self, argument):
        """

        :param argument:
        :return:
        """
        statement_list = list()
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()

        logger('DictionaryHelper', '__get_all_statement_by_argument', 'Argument ' + str(argument.uid) +
               ' conclusion: ' + str(argument.conclusion_uid) + '/' + str(argument.argument_uid) +
               ' premise count: ' + str(len(db_premises)))

        for premise in db_premises:
            statement_list.append({'text': get_text_for_statement_uid(premise.statement_uid),
                                   'uid': premise.statement_uid})

        if argument.conclusion_uid is not None:
            statement_list.append({'text': get_text_for_statement_uid(argument.conclusion_uid),
                                   'uid': argument.conclusion_uid})

        else:
            db_conclusion_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument.argument_uid).first()
            db_conclusion_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_conclusion_argument.premisesgroup_uid).all()
            for conclusion_premise in db_conclusion_premises:
                statement_list.append({'text': get_text_for_statement_uid(conclusion_premise.statement_uid),
                                       'uid': conclusion_premise.statement_uid})

            statement_list.append({'text': get_text_for_statement_uid(db_conclusion_argument.conclusion_uid),
                                   'uid': db_conclusion_argument.conclusion_uid})

        return statement_list

    def __append_now_bubble(self, bubbles_array):
        if len(bubbles_array) > 0:
            _tn = Translator(self.lang)
            bubbles_array.append(
                create_speechbubble_dict(is_status=True, uid='now', message=_tn.get(_.now), lang=self.lang,
                                         omit_url=True))
