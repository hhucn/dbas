"""
Provides helping function for dictionaries, which are used in discussions.
"""
import logging
from typing import List, Optional, Any, Dict, Union

import dbas.handler.history as history_handler
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User
from dbas.helper.dictionary.bubbles import get_user_bubble_text_for_justify_statement, \
    get_system_bubble_text_for_justify_statement
from dbas.helper.html_tags import wrap_in_tag
from dbas.helper.url import UrlManager
from dbas.lib import get_text_for_argument_uid, get_text_for_conclusion, create_speechbubble_dict, \
    is_author_of_argument, bubbles_already_last_in_list, BubbleTypes, nick_of_anonymous_user, \
    Relations
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital, start_with_small
from dbas.strings.text_generator import tag_type, get_header_for_users_confrontation_response, \
    get_text_for_add_premise_container, get_text_for_confrontation, get_text_for_support, \
    get_name_link_of_arguments_author, remove_punctuation
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


class DiscussionDictHelper:
    """
    Provides all functions for creating the discussion dictionaries with all bubbles.
    """

    def __init__(self, lang: str, nickname: str = None,
                 history: history_handler.SessionHistory = None, slug: str = '',
                 broke_limit: bool = False):
        """
        Initialize default values

        :param lang: A ui_locales string for the desired language
        :param nickname: The nickname of the concerned user, if any
        :param history: The history encoded as a string
        :param slug: The slug of the current issue
        :param broke_limit: Whether the user just now got enough points to access the Review-System
        """

        self.lang = lang
        self.nickname = nickname
        if history is None:
            history = history_handler.SessionHistory()
        self.session_history = history
        self.slug = slug
        self.broke_limit = broke_limit

    def get_dict_for_start(self, start_empty: bool) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the first step in discussion,
        where the user chooses a position.

        :param start_empty: Indicates whether the bubbles shall start empty or with the initial start bubble
        :return: A dictionary representing the bubbles needed for the start
        """
        LOG.debug("At start with positions")
        _tn = Translator(self.lang)

        bubbles_array = []
        if not start_empty:
            start_bubble = create_speechbubble_dict(BubbleTypes.USER, uid='start',
                                                    content=_tn.get(_.initialPositionInterest), omit_bubble_url=True,
                                                    lang=self.lang)
            bubbles_array = [start_bubble]

        return {
            'bubbles': bubbles_array,
            'add_premise_text': _tn.get(_.whatIsYourIdea),
            'save_statement_url': 'set_new_start_premise',
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_attitude(self, position: Statement, user: User = None) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the second step in discussion,
        where the user chooses her attitude.

        :param user: Current user
        :param position: The special statement that should be presented
        :return: A dictionary representing the bubbles needed to show a position
        """
        LOG.debug("Entering get_dict_for_attitude")
        _tn = Translator(self.lang)
        statement_text = position.get_html()

        if self.lang != 'de':
            pos = len('<' + tag_type + ' data-argumentation-type="position">')
            statement_text = statement_text[0:pos + 1].lower() + statement_text[pos + 1:]

        text = _tn.get(_.whatDoYouThinkAbout)
        text += ' ' + statement_text + '?'
        start_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, content=text, omit_bubble_url=True, lang=self.lang,
                                                db_user=user)

        return {
            'bubbles': [start_bubble],
            'add_premise_text': '',
            'save_statement_url': 'set_new_start_statement',
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_justify_statement(self, statement: Statement, slug: str, is_supportive: bool,
                                       first_bubble: bool, user: User) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the third step in discussion,
        where the user justifies his position.

        :param statement: The statement that needs to be justified
        :param user: The user doing the justification
        :param slug: The slug of the corresponding issue
        :param is_supportive: Whether the justification is supportive
        :param first_bubble: Indicates whether this justification is the first real element
        :return: A dictionary representing the bubbles needed to justify a statement
        """
        LOG.debug("Entering get_dict_for_justify_statement")
        _tn = Translator(self.lang)

        bubbles_array = self.session_history.create_bubbles(self.nickname, self.lang, self.slug)

        text = statement.get_text()
        if not text:
            return {}

        # system bubble
        system_question = get_system_bubble_text_for_justify_statement(is_supportive, _tn, text,
                                                                       'data-argumentation-type="position"')

        # user bubble
        nickname = user.nickname if user and user.nickname != nick_of_anonymous_user else None
        user_text, add_premise_text = get_user_bubble_text_for_justify_statement(statement, user, is_supportive, _tn)
        question_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, content=system_question, omit_bubble_url=True,
                                                   lang=self.lang)
        url = UrlManager(slug).get_url_for_statement_attitude(statement.uid)
        select_bubble = create_speechbubble_dict(BubbleTypes.USER, bubble_url=url, content=user_text,
                                                 omit_bubble_url=False, statement_uid=statement.uid,
                                                 is_supportive=is_supportive, db_user=user, lang=self.lang)

        if not bubbles_already_last_in_list(bubbles_array, select_bubble):
            bubbles_array.append(select_bubble)

        self._append_now_bubble(bubbles_array)

        if not bubbles_already_last_in_list(bubbles_array, question_bubble):
            bubbles_array.append(question_bubble)

        if not self.nickname and first_bubble:
            _t = Translator(self.lang)
            user = User.by_nickname(nickname)
            msg_dict = {
                'm': _.voteCountTextFirstM,
                'f': _.voteCountTextFirstF,
                'n': _.voteCountTextFirst,
            }

            if user:
                msg = msg_dict[user.gender]
            else:
                msg = _.voteCountTextFirst

            msg = _t.get(msg) + '.'

            bubbles_array.append(create_speechbubble_dict(BubbleTypes.INFO, uid='now_first',
                                                          content=msg + _tn.get(_.onlyOneItemWithLink),
                                                          omit_bubble_url=True, lang=self.lang))
        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': 'set_new_start_statement',
            'mode': '',
            'is_supportive': is_supportive,
            'broke_limit': self.broke_limit
        }

    def get_dict_for_justify_argument(self, argument: Argument, is_supportive: bool, relation: str) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for a step in discussion,
        where the user justifies his attack she has done.

        :param argument: The argument being justified
        :param is_supportive: Whether the justification is supportive
        :param relation: The type of relation used for the justification
        :return: A dictionary representing the bubbles needed to justify an argument
        """
        LOG.debug("Entering get_dict_for_justify_argument")
        _tn = Translator(self.lang)
        bubbles_array = self.session_history.create_bubbles(self.nickname, self.lang, self.slug)

        if argument is None:
            return {
                'bubbles': bubbles_array,
                'add_premise_text': '',
                'save_statement_url': 'set_new_premises_for_argument',
                'mode': '',
                'broke_limit': self.broke_limit
            }

        premise = argument.get_premisegroup_text()
        conclusion = get_text_for_conclusion(argument, is_users_opinion=False)

        if argument.conclusion_uid is None:
            conclusion = start_with_small(conclusion)

        while premise.endswith(('.', '?', '!')):
            premise = premise[:-1]
        while conclusion.endswith(('.', '?', '!')):
            conclusion = premise[:-1]
        redirect_from_jump = 'jump/' in self.session_history.get_nth_last_action(1)
        user_msg, sys_msg = get_header_for_users_confrontation_response(argument, self.lang, premise, relation,
                                                                        conclusion, False, is_supportive, self.nickname,
                                                                        redirect_from_jump=redirect_from_jump)

        add_premise_text = self._add_premise_text_for_justify_argument(get_text_for_argument_uid(argument.uid),
                                                                       premise, relation, conclusion, argument,
                                                                       is_supportive, user_msg)
        start = '<{} data-argumentation-type="position">'.format(tag_type)
        end = '</{}>'.format(tag_type)
        user_msg = user_msg.format(start, end)

        pro_tag = '<{} class="text-success">'.format(tag_type)
        con_tag = '<{} class="text-danger">'.format(tag_type)
        end_tag = '</{}>'.format(tag_type)

        if relation == Relations.UNDERCUT:
            sys_msg = _tn.get(_.whatIsYourMostImportantReasonForArgument).rstrip().format(pro_tag, end_tag) + ': '
            dot = '.'
        else:
            dot = '?'
            if relation == Relations.UNDERMINE:
                sys_msg = _tn.get(_.whatIsYourMostImportantReasonAgainstStatement).rstrip().format(con_tag, end_tag)
                sys_msg += ', ' if self.lang == 'de' else ' '
            else:
                sys_msg = _tn.get(_.whatIsYourMostImportantReasonForStatement).rstrip().format(pro_tag, end_tag) + ': '

        sys_msg += user_msg + dot + '<br>' + _tn.get(_.because) + '...'

        self._append_now_bubble(bubbles_array)
        sys_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, content=sys_msg, omit_bubble_url=True, lang=self.lang)
        if not bubbles_already_last_in_list(bubbles_array, sys_bubble):
            bubbles_array.append(sys_bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': add_premise_text,
            'save_statement_url': 'set_new_premises_for_argument',
            'mode': '',
            'attack_type': relation,
            'arg_uid': argument.uid,
            'broke_limit': self.broke_limit
        }

    def _add_premise_text_for_justify_argument(self, confrontation: str, premise: str, relation: str,
                                               conclusion: str, argument: Argument, is_supportive: bool,
                                               user_msg: str) -> str:
        """
        Returns the text fot the add premise container during the justification for an argument

        :param confrontation: The arguments text
        :param premise: Content of the premise
        :param relation: Type of relation encoded as a string
        :param conclusion: The text of the conclusion
        :param argument: The argument for which we try to build the justification
        :param is_supportive: Whether the justification is supportive
        :param user_msg: The users input
        :return: Returns the text for the justification premise
        """
        if relation == Relations.UNDERMINE:
            add_premise_text = get_text_for_add_premise_container(self.lang, confrontation, premise, relation,
                                                                  conclusion, argument.is_supportive)
            add_premise_text = start_with_capital(add_premise_text)

        elif relation == Relations.SUPPORT:
            # when the user rebuts a system confrontation, he attacks his own negated premise, therefore he supports
            # is own premise. so his premise is the conclusion and we need new premises ;-)
            add_premise_text = get_text_for_add_premise_container(self.lang, confrontation, premise, relation,
                                                                  conclusion, not is_supportive)

        elif relation == Relations.UNDERCUT:
            add_premise_text = user_msg.format('', '') + ', ' + '...'

        else:
            add_premise_text = get_text_for_add_premise_container(self.lang, confrontation, premise, relation,
                                                                  conclusion, argument.is_supportive)

        return add_premise_text

    def get_dict_for_dont_know_reaction(self, argument: Argument, user: User) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the third step,
        where an supportive argument will be presented.

        :param argument: The argument which shall be presented for the don't know reaction
        :param user: The Nickname of the user for whom the bubble needs to be shown
        :return: A dictionary representing the bubbles needed to present an argument for the don't know reaction
        """
        LOG.debug("Entering get_dict_for_dont_know_reaction")
        _tn = Translator(self.lang)
        bubbles_array = self.session_history.create_bubbles(self.nickname, self.lang, self.slug)
        gender = ''
        statement_list = list()

        if argument is not None:
            text = get_text_for_argument_uid(argument, rearrange_intro=True, attack_type='dont_know',
                                             with_html_tag=True, start_with_intro=True)
            data = get_name_link_of_arguments_author(argument, user.nickname)
            intro = wrap_in_tag(tag_type, _tn.get(_.iThinkThat))
            sys_text = intro + ' ' + start_with_small(text) + '. '
            sys_text += '<br><br> ' + wrap_in_tag(tag_type, _tn.get(_.whatDoYouThinkAboutThat) + '?')
            bubble_sys = create_speechbubble_dict(BubbleTypes.SYSTEM, is_markable=True, uid=str(argument.uid),
                                                  content=sys_text, other_author=data['user'])
            if not bubbles_already_last_in_list(bubbles_array, bubble_sys):
                bubbles_array.append(bubble_sys)

            # add statements of discussion to report them
            statement_list = self._get_all_statement_texts_by_argument(argument)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': 'set_new_start_statement',
            'mode': '',
            'extras': statement_list,
            'gender': gender,
            'broke_limit': self.broke_limit
        }

    def get_dict_for_argumentation(self, argument: Argument, arg_sys_id: Optional[int],
                                   relation: Optional[Relations],
                                   user: User) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the argumentation window.

        :param argument: Argument which is presented
        :param arg_sys_id: Argument.uid / not necessary if attack=end
        :param relation: String (undermine, support, undercut, rebut, ...)
        :param history: History
        :param user: User
        :return: dict()
        """
        LOG.debug("At_argumentation about %s", argument.uid)
        nickname = user.nickname
        if user.nickname == nick_of_anonymous_user:
            user = None
            nickname = None

        bubbles_array = self.session_history.create_bubbles(nickname, self.lang, self.slug)
        bubble_mid = ''
        has_user_changed_opinion = self.session_history.get_nth_last_action(1).endswith(str(argument.uid))
        statement_list = list()
        gender_of_counter_arg = ''

        enemy_user = None
        if arg_sys_id is not None:
            enemy_argument = DBDiscussionSession.query(Argument).get(arg_sys_id)
            enemy_data = get_name_link_of_arguments_author(enemy_argument, nickname)
            enemy_user = enemy_data['user']

        if not relation:
            prep_dict = self._get_dict_for_argumentation_end(argument, has_user_changed_opinion, user)
            bubble_sys = create_speechbubble_dict(BubbleTypes.SYSTEM, content=prep_dict['sys'], omit_bubble_url=True,
                                                  lang=self.lang, other_author=enemy_user)
            bubble_mid = create_speechbubble_dict(BubbleTypes.INFO, content=prep_dict['mid'], omit_bubble_url=True,
                                                  lang=self.lang)
        else:
            prep_dict = self._get_dict_for_argumentation(
                argument, arg_sys_id, relation, nickname,
                argument.is_supportive)
            quid = 'question-bubble-' + str(arg_sys_id) if int(arg_sys_id) > 0 else ''
            is_author = is_author_of_argument(user, prep_dict['confrontation'].uid)
            bubble_sys = create_speechbubble_dict(BubbleTypes.SYSTEM, is_markable=True, is_author=is_author, uid=quid,
                                                  content=prep_dict['sys'], omit_bubble_url=True, lang=self.lang,
                                                  other_author=enemy_user)
            statement_list = self._get_all_statement_texts_by_argument(prep_dict['confrontation'])
            gender_of_counter_arg = prep_dict['gender']

        bubble_user = create_speechbubble_dict(BubbleTypes.USER, content=prep_dict['user'], omit_bubble_url=True,
                                               argument_uid=argument.uid, is_supportive=argument.is_supportive,
                                               db_user=user, lang=self.lang, other_author=enemy_user)

        # dirty fixes
        if len(bubbles_array) > 0 and bubbles_array[-1]['message'] == bubble_user['message']:
            bubbles_array.remove(bubbles_array[-1])

        self._append_now_bubble(bubbles_array)
        if not bubbles_already_last_in_list(bubbles_array, bubble_user):
            bubbles_array.append(bubble_user)
        if not bubbles_already_last_in_list(bubbles_array, bubble_sys):
            bubbles_array.append(bubble_sys)

        if not relation:
            bubbles_array.append(bubble_mid)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': 'set_new_start_statement',
            'mode': '',
            'extras': statement_list,
            'gender': gender_of_counter_arg,
            'broke_limit': self.broke_limit
        }

    def _get_dict_for_argumentation_end(self, argument: Argument, has_user_changed_opinion: bool, user: User) -> \
            Dict[str, str]:
        """
        Returns a special dict() when the discussion ends during an argumentation

        :param argument: The argument which ends the discussion
        :param has_user_changed_opinion:  Whether the user has changed opinion regarding `argument`
        :param user: The user arguing
        :return: Returns a dictionary with information which help build the end of the argumentation
        """
        nickname = user.nickname if user and user.nickname != nick_of_anonymous_user else None
        _tn = Translator(self.lang)
        text = get_text_for_argument_uid(argument.uid, user_changed_opinion=has_user_changed_opinion,
                                         minimize_on_undercut=True, nickname=nickname)
        trophy = '<i class="fa fa-trophy" aria-hidden="true"></i>'
        mid_text = '{} {} {} <br>{}'.format(trophy, _tn.get(_.congratulation), trophy,
                                            _tn.get(_.discussionCongratulationEnd))

        if nickname is not None:
            mid_text += _tn.get(_.discussionEndLinkTextWithQueueLoggedIn)
        else:
            mid_text += _tn.get(_.discussionEndLinkTextWithQueueNotLoggedIn)

        return {
            'user': start_with_capital(text),
            'mid': mid_text,
            'sys': _tn.get(_.otherParticipantsDontHaveCounterForThat) + '.'
        }

    def _get_dict_for_argumentation(self, user_arg: Argument, confrontation_arg_uid: int,
                                    relation: Relations, nickname: str, is_supportive: bool) -> Dict[str, Any]:
        """
        Returns dict() for the reaction step

        :param user_arg: Argument that the system reacts to
        :param confrontation_arg_uid:  The id of the argument with which is reacted
        :param history: The history up to this point of the discussion as a string
        :param relation: The relation which is used in the confrontation
        :param nickname: The nickname of the use being confronted
        :param is_supportive: Whether the relation is supportive
        :return: Returns a dictionary with information which help build a specific part of the argumentation
        """
        premise = user_arg.get_premisegroup_text()
        confrontation = DBDiscussionSession.query(Argument).get(confrontation_arg_uid)
        if relation == Relations.UNDERMINE:
            if confrontation.conclusion_uid != 0:
                premise = confrontation.get_conclusion_text()
            else:
                premise = get_text_for_argument_uid(confrontation.argument_uid, with_html_tag=True,
                                                    colored_position=True, attack_type=str(relation))

        # did the user change his opinion?
        has_user_changed_opinion = len(
            self.session_history.get_session_history_as_list()) > 1 and '/undercut/' in self.session_history.get_nth_last_action(
            2)

        # argumentation is a reply for an argument, if the arguments conclusion of the user is no position
        conclusion_uid = user_arg.conclusion_uid
        tmp_arg = user_arg
        while not conclusion_uid:
            tmp_arg = DBDiscussionSession.query(Argument).get(tmp_arg.argument_uid)
            conclusion_uid = tmp_arg.conclusion_uid

        statement = DBDiscussionSession.query(Statement).get(conclusion_uid)
        reply_for_argument = not (statement and statement.is_position)
        support_counter_argument = 'reaction' in self.session_history.get_nth_last_action(1)

        current_argument = get_text_for_argument_uid(user_arg.uid, nickname=nickname, with_html_tag=True,
                                                     colored_position=True,
                                                     user_changed_opinion=has_user_changed_opinion,
                                                     attack_type=str(relation), minimize_on_undercut=True,
                                                     support_counter_argument=support_counter_argument)

        current_argument = start_with_capital(current_argument)
        if self.lang != 'de':
            premise = start_with_small(premise)

        # check for support and build text
        _tn = Translator(self.lang)
        user_text = (_tn.get(_.otherParticipantsConvincedYouThat) + ': ') if has_user_changed_opinion else ''
        user_text += current_argument if current_argument != '' else premise

        sys_text, gender = get_text_for_confrontation(self.lang, nickname, premise, get_text_for_conclusion(user_arg),
                                                      confrontation.get_conclusion_text(), is_supportive, relation,
                                                      confrontation.get_premisegroup_text(), reply_for_argument,
                                                      not user_arg.is_supportive, user_arg, confrontation)
        gender_of_counter_arg = gender

        return {
            'user': user_text,
            'sys': sys_text,
            'gender': gender_of_counter_arg,
            'confrontation': confrontation
        }

    def get_dict_for_jump(self, argument: Argument) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the jump step

        :param argument: The argument to which the system shall jump
        :return: A dictionary representing an argument after a user jumps to it
        """
        LOG.debug("Argument: %s", argument)
        _tn = Translator(self.lang)
        argument_text = get_text_for_argument_uid(argument.uid, colored_position=True, with_html_tag=True,
                                                  attack_type='jump')
        bubbles_array = self.session_history.create_bubbles(self.nickname, self.lang, self.slug)

        coming_from_jump = False
        if self.session_history is not None:
            coming_from_jump = '/jump' in self.session_history.get_nth_last_action(1) if len(
                self.session_history.get_session_history_as_list()) > 0 else False
        intro = (_tn.get(_.canYouBeMorePrecise) + '<br><br>') if coming_from_jump else ''

        if argument.conclusion_uid is not None:
            intro += _tn.get(_.whatDoYouThinkArgument).strip() + ': '
        else:
            bind = ', ' if self.lang == 'de' else ' '
            intro += _tn.get(_.whatDoYouThinkAboutThat) + bind + _tn.get(_.that) + ' '

        argument_text = remove_punctuation(argument_text)

        text = intro + argument_text + '?'
        bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, is_markable=True,
                                          uid='question-bubble-{}'.format(argument.uid), content=text,
                                          omit_bubble_url=True, lang=self.lang)
        bubbles_array.append(bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': '',
            'mode': '',
            'extras': self._get_all_statement_texts_by_argument(argument),
            'broke_limit': self.broke_limit
        }

    def get_dict_for_supporting_each_other(self, system_argument: Argument, user_argument: Argument, user: User) -> \
            Dict[str, Any]:
        """
        Returns the dictionary during the supporting step

        :param system_argument: Argument chosen by the system
        :param user_argument: Argument chosen by the user to support
        :param user: The users attempting the support
        :return: A dictionary representing an argument at the support step
        """
        LOG.debug("Entering get_dict_for_supporting_each_other for arg: %s", system_argument)
        _tn = Translator(self.lang)
        bubbles_array = self.session_history.create_bubbles(user.nickname, self.lang, self.slug)

        argument_text = get_text_for_argument_uid(system_argument.uid, colored_position=True, with_html_tag=True,
                                                  attack_type='jump')
        argument_text = remove_punctuation(argument_text)

        sys_text = get_text_for_support(system_argument, argument_text, user.nickname, _tn)

        self._append_now_bubble(bubbles_array)

        user_text = get_text_for_argument_uid(user_argument.uid, nickname=user.nickname)
        bubble_user = create_speechbubble_dict(BubbleTypes.USER, content=user_text, omit_bubble_url=True,
                                               argument_uid=user_argument.uid,
                                               is_supportive=user_argument.is_supportive, db_user=user, lang=self.lang)
        bubbles_array.append(bubble_user)
        bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, uid='question-bubble-{}'.format(system_argument),
                                          content=sys_text, omit_bubble_url=True, lang=self.lang)
        bubbles_array.append(bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': '',
            'mode': '',
            'broke_limit': self.broke_limit
        }

    def get_dict_for_choosing(self, discussion_object: Union[Argument, Statement], discussion_obj_is_argument: bool,
                              is_supportive: bool) -> Dict[str, Any]:
        """
        Prepares the discussion dict with all bubbles for the choosing an premise,
        when the user inserted more than one new premise.

        :param discussion_object: The argument/statement which is used for the choice
        :param discussion_obj_is_argument: Whether the discussion object is an argument
        :param is_supportive: Whether the object is supportive
        :return: A dictionary representing the choice the user needs to make
        """
        _tn = Translator(self.lang)
        bubbles_array = self.session_history.create_bubbles(self.nickname, self.lang, self.slug)

        LOG.debug("Choosing dictionary for bubbles.")

        if discussion_obj_is_argument:
            discussed_text = get_text_for_argument_uid(discussion_object.uid)
            if is_supportive:
                question = _tn.get(_.whatIsYourMostImportantReasonForArgument)
            else:
                question = _tn.get(_.whatIsYourMostImportantReasonAgainstArgument)
        else:
            discussed_text = discussion_object.get_text()
            if is_supportive:
                question = _tn.get(_.whatIsYourMostImportantReasonForStatement)
            else:
                question = _tn.get(_.whatIsYourMostImportantReasonAgainstStatement)

        question = question.replace('{}', '')

        text = '{}. {}: {}?<br>{}...'.format(_tn.get(_.soYouEnteredMultipleReasons), question, discussed_text,
                                             _tn.get(_.because))

        self._append_now_bubble(bubbles_array)

        question_bubble = create_speechbubble_dict(BubbleTypes.SYSTEM, uid='question-bubble', content=text,
                                                   omit_bubble_url=True, lang=self.lang)
        if not bubbles_already_last_in_list(bubbles_array, question_bubble):
            bubbles_array.append(question_bubble)

        return {
            'bubbles': bubbles_array,
            'add_premise_text': '',
            'save_statement_url': 'set_new_start_statement',
            'mode': '',
            'broke_limit': self.broke_limit
        }

    @staticmethod
    def _get_all_statement_texts_by_argument(argument: Argument) -> List[Dict[str, Any]]:
        """
        Returns all statement texts for a given argument

        :param argument: The argument for which the texts shall be returned.
        :return: A list containing dictionaries representing the texts of the statements of `argument`
        """
        statement_list = list()
        LOG.debug("Argument %s, conclusion: %s / %s, premise count: %s", argument.uid, argument.conclusion_uid,
                  argument.argument_uid, len(argument.premises))

        for premise in argument.premises:
            statement_list.append({
                'text': premise.get_text(),
                'uid': premise.statement_uid
            })

        if argument.conclusion_uid is not None:
            statement_list.append({
                'text': argument.get_conclusion_text(),
                'uid': argument.conclusion_uid
            })

        else:
            for conclusion_premise in argument.attacks.premises:
                statement_list.append({
                    'text': conclusion_premise.get_text(),
                    'uid': conclusion_premise.statement_uid
                })

            statement_list.append({
                'text': argument.attacks.get_conclusion_text(),
                'uid': argument.attacks.conclusion_uid
            })

        return statement_list

    def _append_now_bubble(self, bubbles_array: List[Dict[str, Any]]) -> None:
        """
        Appends the "now" bubble to the bubble array

        :param bubbles_array: A list of bubbles that shall be added
        """
        if len(bubbles_array) > 0:
            _tn = Translator(self.lang)
            bubble = create_speechbubble_dict(BubbleTypes.STATUS, uid='now', content=_tn.get(_.now),
                                              omit_bubble_url=True, lang=self.lang)
            bubbles_array.append(bubble)
