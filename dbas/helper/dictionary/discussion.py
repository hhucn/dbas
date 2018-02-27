"""
Provides helping function for dictionaries, which are used in discussions.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import dbas.handler.history as history_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, Premise, User
from dbas.helper.dictionary.bubbles import get_user_bubble_text_for_justify_statement, \
    get_system_bubble_text_for_justify_statement
from dbas.helper.url import UrlManager
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, \
    get_text_for_conclusion, create_speechbubble_dict, is_author_of_argument, bubbles_already_last_in_list, BubbleTypes, \
    nick_of_anonymous_user
from dbas.logger import logger
from dbas.review.helper.queues import get_complete_review_count
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import tag_type, get_header_for_users_confrontation_response, \
    get_text_for_add_premise_container, get_text_for_confrontation, get_text_for_support, \
    get_name_link_of_arguments_author
from dbas.strings.translator import Translator


class DiscussionDictHelper(object):
    """
    Provides all functions for creating the discussion dictionaries with all bubbles.
    """

    def __init__(self, lang, nickname=None, history: str='', slug: str='', broke_limit: bool=False):
        """
        Initialize default values

        :param lang: ui_locales
        :param nickname: request.authenticated_userid
        :param history: history
        :param slug: String
        :return:
        """
        self.lang = lang
        self.nickname = nickname
        self.history = history
        self.slug = slug
        self.broke_limit = broke_limit

    def get_dict_for_start(self, position_count):
        """
        Prepares the discussion dict with all bubbles for the first step in discussion,
        where the user chooses a position.

        :position_count: int
        :return: dict()
        """
        logger('DictionaryHelper', 'at_start with positions: ' + str(position_count))
        _tn = Translator(self.lang)
        add_premise_text = _tn.get(_.whatIsYourIdea)
        intro = _tn.get(_.initialPositionInterest) + (' ...' if self.lang == 'en' else '')
        save_statement_url = 'set_new_start_premise'

        start_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, uid='start', message=intro, omit_url=True,
                                                lang=self.lang)
        bubbles_array = [] if position_count == 1 else [start_bubble]

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_attitude(self, uid):
        """
        Prepares the discussion dict with all bubbles for the second step in discussion,
        where the user chooses her attitude.

        :param uid: Argument.uid
        :return: dict()
        """
        logger('DictionaryHelper', 'at_attitude')
        _tn = Translator(self.lang)
        add_premise_text = ''
        save_statement_url = 'set_new_start_statement'
        statement_text = get_text_for_statement_uid(uid, True)
        if not statement_text:
            return None

        if self.lang != 'de':
            pos = len('<' + tag_type + ' data-argumentation-type="position">')
            statement_text = statement_text[0:pos + 1].lower() + statement_text[pos + 1:]

        text = _tn.get(_.whatDoYouThinkAbout)
        text += ' ' + statement_text + '?'
        bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, message=text, omit_url=True, lang=self.lang)

        bubbles_array = [bubble]

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_justify_statement(self, uid, slug, is_supportive, count_of_items, db_user):
        """
        Prepares the discussion dict with all bubbles for the third step in discussion,
        where the user justifies his position.

        :param uid: Argument.uid
        :param app_url: application url
        :param slug: Issue.slug
        :param is_supportive: Boolean
        :param count_of_items: Integer
        :param nickname: User.nickname
        :return: dict()
        """
        logger('DictionaryHelper', 'at_justify')
        _tn = Translator(self.lang)

        bubbles_array = history_helper.create_bubbles_from_history(self.history, self.nickname, self.lang, self.slug)

        save_statement_url = 'set_new_start_statement'
        text = get_text_for_statement_uid(uid)
        if not text:
            return None

        tag_start = '<{}data-argumentation-type="position">'.format(tag_type)
        tag_end = '</{}>'.format(tag_type)

        # system bubble
        system_question = get_system_bubble_text_for_justify_statement(is_supportive, _tn, tag_start, text, tag_end)

        # user bubble
        nickname = db_user.nickname if db_user and db_user.nickname != nick_of_anonymous_user else None
        user_text, add_premise_text = get_user_bubble_text_for_justify_statement(uid, db_user, is_supportive, _tn)

        question_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, message=system_question, omit_url=True,
                                                   lang=self.lang)
        url = UrlManager(slug).get_url_for_statement_attitude(uid)
        select_bubble = create_speechbubble_dict(BubbleTypes.USER, url=url, message=user_text, omit_url=False,
                                                 statement_uid=uid, is_supportive=is_supportive, nickname=nickname,
                                                 lang=self.lang)

        if not bubbles_already_last_in_list(bubbles_array, select_bubble):
            bubbles_array.append(select_bubble)

        self.__append_now_bubble(bubbles_array)

        if not bubbles_already_last_in_list(bubbles_array, question_bubble):
            bubbles_array.append(question_bubble)

        if not self.nickname and count_of_items == 1:
            _t = Translator(self.lang)
            db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
            msg_dict = {
                'm': _.voteCountTextFirstM,
                'f': _.voteCountTextFirstF,
                'n': _.voteCountTextFirst,
            }

            if db_user:
                msg = msg_dict[db_user.gender]
            else:
                msg = _.voteCountTextFirst

            msg = _t.get(msg) + '.'

            bubbles_array.append(create_speechbubble_dict(BubbleTypes.INFO, uid='now_first',
                                                          message=msg + _tn.get(_.onlyOneItemWithLink),
                                                          omit_url=True, lang=self.lang))
        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'is_supportive': is_supportive,
            'broke_limit': self.broke_limit
        }

    def get_dict_for_justify_argument(self, uid, is_supportive, attack):
        """
        Prepares the discussion dict with all bubbles for a step in discussion,
        where the user justifies his attack she has done.

        :param uid: Argument.uid
        :param is_supportive: Boolean
        :param attack: String (undermine, support, undercut, rebut, ...)
        :return: dict()
        """
        logger('DictionaryHelper', 'def')
        _tn = Translator(self.lang)
        bubbles_array = history_helper.create_bubbles_from_history(self.history, self.nickname, self.lang, self.slug)
        add_premise_text = ''
        save_statement_url = 'set_new_premises_for_argument'

        db_argument = DBDiscussionSession.query(Argument).get(uid)
        if not db_argument:
            return {
                'bubbles': bubbles_array,
                'add_premise_text': add_premise_text,
                'save_statement_url': save_statement_url,
                'mode': '',
                'broke_limit': self.broke_limit
            }

        confrontation = get_text_for_argument_uid(uid)
        premise, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        conclusion = get_text_for_conclusion(db_argument, is_users_opinion=False)

        if db_argument.conclusion_uid is None:
            conclusion = conclusion[0:1].lower() + conclusion[1:]

        while premise.endswith(('.', '?', '!')):
            premise = premise[:-1]
        while conclusion.endswith(('.', '?', '!')):
            conclusion = premise[:-1]

        redirect_from_jump = 'jump/' in self.history.split('-')[-1]
        user_msg, sys_msg = get_header_for_users_confrontation_response(db_argument, self.lang, premise,
                                                                        attack, conclusion, False,
                                                                        is_supportive, self.nickname,
                                                                        redirect_from_jump=redirect_from_jump)

        add_premise_text = self.__get_add_premise_text_for_justify_argument(confrontation, premise, attack,
                                                                            conclusion, db_argument, is_supportive,
                                                                            user_msg)
        start = '<{} data-argumentation-type="position">'.format(tag_type)
        end = '</{}>'.format(tag_type)
        user_msg = user_msg.format(start, end)

        pro_tag = '<{} class="text-success">'.format(tag_type)
        con_tag = '<{} class="text-danger">'.format(tag_type)
        end_tag = '</{}>'.format(tag_type)

        if attack == 'undercut':
            sys_msg = _tn.get(_.whatIsYourMostImportantReasonForArgument).rstrip().format(pro_tag, end_tag) + ': '
            dot = '.'
        else:
            dot = '?'
            if attack == 'undermine':
                sys_msg = _tn.get(_.whatIsYourMostImportantReasonAgainstStatement).rstrip().format(con_tag, end_tag)
                sys_msg += ', ' if self.lang == 'de' else ' '
            else:
                sys_msg = _tn.get(_.whatIsYourMostImportantReasonForStatement).rstrip().format(pro_tag, end_tag) + ': '

        sys_msg += user_msg + dot + '<br>' + _tn.get(_.because) + '...'

        self.__append_now_bubble(bubbles_array)
        sys_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, message=sys_msg, omit_url=True, lang=self.lang)
        if not bubbles_already_last_in_list(bubbles_array, sys_bubble):
            bubbles_array.append(sys_bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'attack_type': attack,
            'arg_uid': uid,
            'broke_limit': self.broke_limit
        }

    def __get_add_premise_text_for_justify_argument(self, confrontation, premise, attack, conclusion, db_argument,
                                                    is_supportive, user_msg):
        """
        Returns the text fot the add premise container during the justification for an argument

        :param confrontation: String
        :param premise: String
        :param attack: String
        :param conclusion: String
        :param db_argument: Argument
        :param is_supportive: Boolean
        :param user_msg: String
        :return: String
        """
        if attack == 'undermine':
            add_premise_text = get_text_for_add_premise_container(self.lang, confrontation, premise, attack,
                                                                  conclusion, db_argument.is_supportive)
            add_premise_text = add_premise_text[0:1].upper() + add_premise_text[1:]

        elif attack == 'support':
            is_supportive = not is_supportive
            # when the user rebuts a system confrontation, he attacks his own negated premise, therefore he supports
            # is own premise. so his premise is the conclusion and we need new premises ;-)
            add_premise_text = get_text_for_add_premise_container(self.lang, confrontation, premise, attack,
                                                                  conclusion, is_supportive)

        elif attack == 'undercut':
            add_premise_text = user_msg.format('', '') + ', ' + '...'

        else:
            add_premise_text = get_text_for_add_premise_container(self.lang, confrontation, premise, attack,
                                                                  conclusion, db_argument.is_supportive)

        return add_premise_text

    def get_dict_for_dont_know_reaction(self, uid, nickname):
        """
        Prepares the discussion dict with all bubbles for the third step,
        where an supportive argument will be presented.

        :param uid: Argument.uid
        :param nickname:
        :return: dict()
        """
        logger('DictionaryHelper', 'at_dont_know')
        _tn = Translator(self.lang)
        bubbles_array = history_helper.create_bubbles_from_history(self.history, self.nickname, self.lang, self.slug)
        add_premise_text = ''
        save_statement_url = 'set_new_start_statement'
        gender = ''
        b = '<' + tag_type + '>'
        e = '</' + tag_type + '>'
        statement_list = list()

        if int(uid) != 0:
            text = get_text_for_argument_uid(uid, rearrange_intro=True, attack_type='dont_know', with_html_tag=True,
                                             start_with_intro=True)
            db_argument = DBDiscussionSession.query(Argument).get(uid)
            if not db_argument:
                text = ''
            db_other_user, author, gender, is_okay = get_name_link_of_arguments_author(db_argument, nickname)
            if is_okay:
                intro = author + ' ' + b + _tn.get(_.thinksThat) + e
            else:
                intro = b + _tn.get(_.otherParticipantsThinkThat) + e
            sys_text = intro + ' ' + text[0:1].lower() + text[1:] + '. '
            sys_text += '<br><br>' + b + _tn.get(_.whatDoYouThinkAboutThat) + '?' + e
            bubble_sys = create_speechbubble_dict(BubbleTypes.SYSTEM, message=sys_text, uid=uid, is_markable=True)
            if not bubbles_already_last_in_list(bubbles_array, bubble_sys):
                bubbles_array.append(bubble_sys)

            # add statements of discussion to report them
            statement_list = self.__get_all_statement_texts_by_argument(db_argument)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'extras': statement_list,
            'gender': gender,
            'broke_limit': self.broke_limit
        }

    def get_dict_for_argumentation(self, uid, is_supportive, additional_uid, attack, history, db_user):
        """
        Prepares the discussion dict with all bubbles for the argumentation window.

        :param uid: Argument.uid
        :param is_supportive: Boolean
        :param additional_uid: Argument.uid / not necessary if attack=end
        :param attack: String (undermine, support, undercut, rebut, ...)
        :param history: History
        :param nickname: Users nickname
        :return: dict()
        """
        logger('DictionaryHelper', 'at_argumentation about ' + str(uid))
        nickname = db_user.nickname if db_user and db_user.nickname != nick_of_anonymous_user else None
        bubbles_array = history_helper.create_bubbles_from_history(self.history, nickname, self.lang, self.slug)
        add_premise_text = ''
        save_statement_url = 'set_new_start_statement'
        bubble_mid = ''
        splitted_history = history_helper.get_splitted_history(self.history)
        user_changed_opinion = splitted_history[-1].endswith(str(uid))
        statement_list = list()
        db_argument = DBDiscussionSession.query(Argument).get(uid)
        gender_of_counter_arg = ''
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        if attack.startswith('end'):
            user_text, mid_text, sys_text = self.__get_dict_for_argumentation_end(uid, user_changed_opinion, db_user,
                                                                                  attack)
            bubble_sys = create_speechbubble_dict(BubbleTypes.SYSTEM, message=sys_text, omit_url=True, lang=self.lang)
            bubble_mid = create_speechbubble_dict(BubbleTypes.INFO, message=mid_text, omit_url=True, lang=self.lang)
        else:
            user_text, sys_text, gender_of_counter_arg, db_confrontation = self.__get_dict_for_argumentation(
                db_argument, additional_uid, history, attack, nickname, is_supportive)
            quid = 'question-bubble-' + str(additional_uid) if int(additional_uid) > 0 else ''
            bubble_sys = create_speechbubble_dict(BubbleTypes.SYSTEM, uid=quid, message=sys_text, omit_url=True,
                                                  lang=self.lang, is_markable=True,
                                                  is_author=is_author_of_argument(db_user, db_confrontation.uid))
            statement_list = self.__get_all_statement_texts_by_argument(db_confrontation)

        bubble_user = create_speechbubble_dict(BubbleTypes.USER, message=user_text, omit_url=True, argument_uid=uid,
                                               is_supportive=is_supportive, lang=self.lang, nickname=nickname)

        # dirty fixes
        if len(bubbles_array) > 0 and bubbles_array[-1]['message'] == bubble_user['message']:
            bubbles_array.remove(bubbles_array[-1])

        self.__append_now_bubble(bubbles_array)
        if not bubbles_already_last_in_list(bubbles_array, bubble_user):
            bubbles_array.append(bubble_user)
        if not bubbles_already_last_in_list(bubbles_array, bubble_sys):
            bubbles_array.append(bubble_sys)

        if attack.startswith('end'):
            bubbles_array.append(bubble_mid)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'extras': statement_list,
            'gender': gender_of_counter_arg,
            'broke_limit': self.broke_limit
        }

    def __get_dict_for_argumentation_end(self, argument_uid, user_changed_opinion, db_user, attack):
        """
        Returns a special dict() when the discussion ends during an argumentation

        :param argument_uid: Argumebt.uid
        :param user_changed_opinion:  Boolean
        :param nickname: User.nickname
        :param attack: String
        :return: String, String, String
        """
        nickname = db_user.nickname if db_user and db_user.nickname != nick_of_anonymous_user else None
        _tn = Translator(self.lang)
        text = get_text_for_argument_uid(argument_uid, user_changed_opinion=user_changed_opinion,
                                         minimize_on_undercut=True, nickname=nickname)
        user_text = text[0:1].upper() + text[1:]
        if attack == 'end':
            sys_text = _tn.get(_.otherParticipantsDontHaveCounterForThat) + '.'
        else:
            sys_text = _tn.get(_.otherParticipantsDontHaveNewCounterForThat)
        trophy = '<i class="fa fa-trophy" aria-hidden="true"></i>'
        mid_text = '{} {} {} <br>{}'.format(trophy, _tn.get(_.congratulation), trophy, _tn.get(_.discussionCongratulationEnd))

        # do we have task in the queue?
        count = get_complete_review_count(db_user)
        if count > 0:
            if nickname is not None:
                mid_text += _tn.get(_.discussionEndLinkTextWithQueueLoggedIn)
            else:
                mid_text += _tn.get(_.discussionEndLinkTextWithQueueNotLoggedIn)
        else:
            if nickname is not None:
                mid_text += _tn.get(_.discussionEndLinkTextLoggedIn)
            else:
                mid_text += _tn.get(_.discussionEndLinkTextNotLoggedIn)

        return user_text, mid_text, sys_text

    def __get_dict_for_argumentation(self, user_arg, confrontation_arg_uid, history, attack, nickname, is_supportive):
        """
        Returns dict() for the reaction step

        :param user_arg: Argument
        :param confrontation_arg_uid:  Argument.uid
        :param history: String
        :param attack: String
        :param nickname: User.nickname
        :param is_supportive: Boolean
        :return: dict()
        """
        premise, tmp = get_text_for_premisesgroup_uid(user_arg.premisesgroup_uid)
        conclusion = get_text_for_conclusion(user_arg)
        db_confrontation = DBDiscussionSession.query(Argument).get(confrontation_arg_uid)
        confr, tmp = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid)
        sys_conclusion = get_text_for_conclusion(db_confrontation)
        if attack == 'undermine':
            if db_confrontation.conclusion_uid != 0:
                premise = get_text_for_statement_uid(db_confrontation.conclusion_uid)
            else:
                premise = get_text_for_argument_uid(db_confrontation.argument_uid, True, colored_position=True,
                                                    attack_type=attack)

        # did the user changed his opinion?
        history = history_helper.get_splitted_history(history)
        user_changed_opinion = len(history) > 1 and '/undercut/' in history[-2]

        # argumentation is a reply for an argument, if the arguments conclusion of the user is no position
        conclusion_uid = user_arg.conclusion_uid
        tmp_arg = user_arg
        while not conclusion_uid:
            tmp_arg = DBDiscussionSession.query(Argument).get(tmp_arg.argument_uid)
            conclusion_uid = tmp_arg.conclusion_uid

        db_statement = DBDiscussionSession.query(Statement).get(conclusion_uid)
        reply_for_argument = not (db_statement and db_statement.is_startpoint)
        support_counter_argument = 'reaction' in self.history.split('-')[-1]

        current_argument = get_text_for_argument_uid(user_arg.uid, nickname=nickname, with_html_tag=True,
                                                     colored_position=True,
                                                     user_changed_opinion=user_changed_opinion, attack_type=attack,
                                                     minimize_on_undercut=True,
                                                     support_counter_argument=support_counter_argument)

        current_argument = current_argument[0:1].upper() + current_argument[1:]
        if self.lang != 'de':
            premise = premise[0:1].lower() + premise[1:]

        # check for support and build text
        _tn = Translator(self.lang)
        user_text = (_tn.get(_.otherParticipantsConvincedYouThat) + ': ') if user_changed_opinion else ''
        user_text += current_argument if current_argument != '' else premise

        sys_text, gender = get_text_for_confrontation(self.lang, nickname, premise, conclusion,
                                                      sys_conclusion, is_supportive, attack, confr, reply_for_argument,
                                                      not user_arg.is_supportive, user_arg, db_confrontation)
        gender_of_counter_arg = gender

        return user_text, sys_text, gender_of_counter_arg, db_confrontation

    def get_dict_for_jump(self, uid):
        """
        Prepares the discussion dict with all bubbles for the jump step

        :param uid: Argument.uid
        :param nickname: User.nickname
        :param history: String
        :return: dict()
        """
        logger('DictionaryHelper', 'argument ' + str(uid))
        _tn = Translator(self.lang)
        argument_text = get_text_for_argument_uid(uid, colored_position=True, with_html_tag=True, attack_type='jump')
        bubbles_array = history_helper.create_bubbles_from_history(self.history, self.nickname, self.lang, self.slug)

        coming_from_jump = False
        if self.history:
            splitted_history = self.history.split('-')
            coming_from_jump = '/jump' in self.history[:-1] if len(splitted_history) > 0 else False
        intro = (_tn.get(_.canYouBeMorePrecise) + '<br><br>') if coming_from_jump else ''

        db_argument = DBDiscussionSession.query(Argument).get(uid)
        if db_argument.conclusion_uid is not None:
            intro += _tn.get(_.whatDoYouThinkArgument).strip() + ': '
        else:
            bind = ', ' if self.lang == 'de' else ' '
            intro += _tn.get(_.whatDoYouThinkAboutThat) + bind + _tn.get(_.that) + ' '

        offset = len('</' + tag_type + '>') if argument_text.endswith('</' + tag_type + '>') else 1
        while argument_text[:-offset].endswith(('.', '?', '!')):
            argument_text = argument_text[:-offset - 1] + argument_text[-offset:]

        text = intro + argument_text + '?'
        bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, message=text, omit_url=True, lang=self.lang,
                                          uid='question-bubble-{}'.format(uid), is_markable=True)
        bubbles_array.append(bubble)

        # add statements of discussion to report them
        statement_list = self.__get_all_statement_texts_by_argument(db_argument)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': '',
            'mode': '',
            'extras': statement_list,
            'broke_limit': self.broke_limit
        }

    def get_dict_for_supporting_each_other(self, uid_system_arg, uid_user_arg, nickname):
        """
        Returns the dictionary during the supporting step

        :param uid_system_arg: Argument.uid
        :param uid_user_arg: Argument.uid
        :param nickname: User.nickname
        :return: dict()
        """
        logger('DictionaryHelper', str(uid_system_arg))
        _tn = Translator(self.lang)
        bubbles_array = history_helper.create_bubbles_from_history(self.history, nickname, self.lang, self.slug)
        db_arg_system = DBDiscussionSession.query(Argument).get(uid_system_arg)
        db_arg_user = DBDiscussionSession.query(Argument).get(uid_user_arg)

        argument_text = get_text_for_argument_uid(uid_system_arg, colored_position=True, with_html_tag=True,
                                                  attack_type='jump')

        offset = len('</' + tag_type + '>') if argument_text.endswith('</' + tag_type + '>') else 1
        while argument_text[:-offset].endswith(('.', '?', '!')):
            argument_text = argument_text[:-offset - 1] + argument_text[-offset:]

        sys_text = get_text_for_support(db_arg_system, argument_text, nickname, _tn)

        self.__append_now_bubble(bubbles_array)

        user_text = get_text_for_argument_uid(uid_user_arg, nickname=nickname)
        bubble_user = create_speechbubble_dict(BubbleTypes.USER, message=user_text, omit_url=True,
                                               argument_uid=uid_user_arg,
                                               is_supportive=db_arg_user.is_supportive, lang=self.lang,
                                               nickname=nickname)
        bubbles_array.append(bubble_user)

        bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, uid='question-bubble-{}'.format(uid_system_arg),
                                          message=sys_text, omit_url=True, lang=self.lang)
        bubbles_array.append(bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': '',
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_jump_decision(self, uid):
        """
        Prepares the discussion dict with all bubbles for the jump decision step

        :param uid: Argument.uid
        :return: dict()
        """
        logger('DictionaryHelper', 'at_attitude')
        _tn = Translator(self.lang)

        db_argument = DBDiscussionSession.query(Argument).get(uid)
        tag_premise = '<' + tag_type + ' data-argumentation-type="argument">'
        tag_conclusion = '<' + tag_type + ' data-argumentation-type="attack">'
        tag_end = '</' + tag_type + '>'
        premise, trash = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
        premise = tag_premise + premise + tag_end
        conclusion = tag_conclusion + get_text_for_conclusion(db_argument) + tag_end
        aand = ' ' + _tn.get(_.aand) + ' '

        text = _tn.get(_.whatDoYouThinkAbout)
        text += ' ' + premise + aand + conclusion + '?'
        bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, message=text, omit_url=True, lang=self.lang)

        bubbles_array = [bubble]

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': '',
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_choosing(self, uid, is_uid_argument, is_supportive):
        """
        Prepares the discussion dict with all bubbles for the choosing an premise,
        when the user inserted more than one new premise.

        :param uid: Argument.uid
        :param is_uid_argument: Boolean
        :param is_supportive: Boolean
        :return:
        """
        _tn = Translator(self.lang)
        bubbles_array = history_helper.create_bubbles_from_history(self.history, self.nickname, self.lang, self.slug)
        add_premise_text = ''
        save_statement_url = 'set_new_start_statement'

        logger('DictionaryHelper', 'at_choosing')
        a = _tn.get(_.soYouEnteredMultipleReasons)
        c = get_text_for_argument_uid(uid) if is_uid_argument else get_text_for_statement_uid(uid)

        if is_supportive:
            if is_uid_argument:
                b = _tn.get(_.whatIsYourMostImportantReasonForArgument)
            else:
                b = _tn.get(_.whatIsYourMostImportantReasonForStatement)
        else:
            if is_uid_argument:
                b = _tn.get(_.whatIsYourMostImportantReasonAgainstArgument)
            else:
                b = _tn.get(_.whatIsYourMostImportantReasonAgainstStatement)
        b = b.replace('{}', '')

        text = '{}. {}: {}?<br>{}...'.format(a, b, c, _tn.get(_.because))

        self.__append_now_bubble(bubbles_array)

        question_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, uid='question-bubble', message=text,
                                                   omit_url=True, lang=self.lang)
        if not bubbles_already_last_in_list(bubbles_array, question_bubble):
            bubbles_array.append(question_bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': save_statement_url,
            'mode': '',
            'broke_limit': self.broke_limit
        }

    @staticmethod
    def __get_all_statement_texts_by_argument(argument):
        """
        Returns all statement texts for a given argument

        :param argument: Argument.uid
        :return: [dict()]
        """
        statement_list = list()
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()

        logger('DictionaryHelper', 'Argument ' + str(argument.uid) +
               ' conclusion: ' + str(argument.conclusion_uid) + '/' + str(argument.argument_uid) +
               ' premise count: ' + str(len(db_premises)))

        for premise in db_premises:
            statement_list.append({'text': get_text_for_statement_uid(premise.statement_uid),
                                   'uid': premise.statement_uid})

        if argument.conclusion_uid is not None:
            statement_list.append({'text': get_text_for_statement_uid(argument.conclusion_uid),
                                   'uid': argument.conclusion_uid})

        else:
            db_conclusion_argument = DBDiscussionSession.query(Argument).get(argument.argument_uid)
            db_conclusion_premises = DBDiscussionSession.query(Premise).filter_by(
                premisesgroup_uid=db_conclusion_argument.premisesgroup_uid).all()
            for conclusion_premise in db_conclusion_premises:
                statement_list.append({'text': get_text_for_statement_uid(conclusion_premise.statement_uid),
                                       'uid': conclusion_premise.statement_uid})

            statement_list.append({'text': get_text_for_statement_uid(db_conclusion_argument.conclusion_uid),
                                   'uid': db_conclusion_argument.conclusion_uid})

        return statement_list

    def __append_now_bubble(self, bubbles_array):
        """
        Appends the "now" bubble to the bubble array

        :param bubbles_array:
        :return:
        """
        if len(bubbles_array) > 0:
            _tn = Translator(self.lang)
            bubble = create_speechbubble_dict(BubbleTypes.STATUS,
                                              uid='now',
                                              message=_tn.get(_.now),
                                              lang=self.lang,
                                              omit_url=True)
            bubbles_array.append(bubble)
