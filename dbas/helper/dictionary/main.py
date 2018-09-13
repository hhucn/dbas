"""
Provides helping function for dictionaries.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import arrow
import datetime
import os
import random
from pyramid.registry import Registry

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Language, Group, Issue, Argument
from dbas.handler import user
from dbas.handler.notification import count_of_new_notifications, get_box_for
from dbas.lib import BubbleTypes, create_speechbubble_dict, get_profile_picture, is_development_mode, \
    nick_of_anonymous_user, get_global_url, usage_of_matomo, usage_of_modern_bubbles
from dbas.logger import logger
from dbas.review.queue.lib import get_count_of_all, get_complete_review_count
from dbas.review.reputation import get_reputation_of, limit_to_open_issues
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class DictionaryHelper(object):
    """
    General function for dictionaries as well as the extras-dict()
    """

    def __init__(self, system_lang: str, discussion_lang=None):
        """
        Initialize default values

        :param system_lang: system_lang
        :param discussion_lang: discussion_lang
        :return:
        """
        self.system_lang = system_lang
        self.discussion_lang = discussion_lang if discussion_lang else system_lang

    @staticmethod
    def get_random_subdict_out_of_ordered_dict(ordered_dict, count):
        """
        Creates a random subdictionary with given count out of the given ordered_dict.
        With a count of <2 the dictionary itself will be returned.

        :param ordered_dict: dictionary for the function
        :param count: count of entries for the new dictionary
        :return: dictionary
        """
        return_dict = dict()
        logger('DictionaryHelper', 'count: ' + str(count))
        items = list(ordered_dict.items())

        if count < 0:
            return ordered_dict
        elif count == 1:
            if len(items) > 1:
                rnd = random.randint(0, len(items) - 1)
                return_dict[items[rnd][0]] = items[rnd][1]
            else:
                return ordered_dict
        else:

            for i in range(0, count):
                rnd = random.randint(0, len(items) - 1)
                return_dict[items[rnd][0]] = items[rnd][1]
                items.pop(rnd)

        return return_dict

    def prepare_extras_dict_for_normal_page(self, registry, application_url, path, db_user):
        """
        Calls self.prepare_extras_dict(...

        :param registry: request.registry
        :param application_url: request.application_url
        :param path: request.path
        :param db_user: db_user
        :return: dict()
        """
        return self.prepare_extras_dict('', False, False, False, registry, application_url, path,
                                        db_user=db_user, ongoing_discussion=False)

    def prepare_extras_dict(self, current_slug: str, is_reportable: bool, show_bar_icon: bool, show_graph_icon: bool,
                            registry: Registry, application_url: str, path: str, db_user: User,
                            broke_limit=False, add_premise_container_style='display: none',
                            add_statement_container_style='display: none', ongoing_discussion=True):
        """
        Creates the extras.dict() with many options!

        :param current_slug:
        :param is_reportable: Same as discussion.bubbles.last.is_markable, but TAL has no last indicator
        :param show_bar_icon: True, if the discussion space should show the graph icon
        :param show_graph_icon: True, if the discussion space should show the barometer icon
        :param registry: Pyramids registry
        :param application_url: current app url
        :param path: current path
        :param db_user: User
        :param broke_limit: Boolean
        :param add_premise_container_style: style string, default 'display:none;'
        :param add_statement_container_style: style string, default 'display:none;'
        :param ongoing_discussion: Boolean
        :return: dict()
        """
        logger('DictionaryHelper', 'def')

        is_user_from_ldap = None
        is_logged_in = False
        nickname = None
        public_nickname = None
        is_user_male = False
        is_user_female = False
        is_admin = False
        is_special = False

        if db_user:
            is_user_from_ldap = db_user.validate_password('NO_PW_BECAUSE_LDAP')
            is_logged_in = True
            nickname = db_user.nickname
            public_nickname = db_user.public_nickname
            is_user_male = db_user.gender == 'm'
            is_user_female = db_user.gender == 'f'
            is_admin = db_user.is_admin()
            is_special = db_user.is_special()
            if db_user.nickname == nick_of_anonymous_user:
                db_user = None
                is_logged_in = False

        return_dict = dict()
        return_dict['url'] = get_global_url()
        return_dict['year'] = datetime.datetime.now().year
        return_dict['restart_url'] = current_slug
        return_dict['is_in_discussion'] = 'discuss' in path
        return_dict['logged_in'] = is_logged_in
        return_dict['nickname'] = nickname
        return_dict['public_nickname'] = public_nickname
        return_dict['add_premise_container_style'] = add_premise_container_style
        return_dict['add_statement_container_style'] = add_statement_container_style
        return_dict['users_avatar'] = get_profile_picture(db_user, 25)
        return_dict['ongoing_discussion'] = ongoing_discussion
        return_dict['slug'] = current_slug
        return_dict['is_user_male'] = is_user_male
        return_dict['is_user_female'] = is_user_female
        return_dict['is_user_neutral'] = not return_dict['is_user_male'] and not return_dict['is_user_female']
        return_dict['broke_limit'] = 'true' if broke_limit else 'false'
        return_dict['use_with_ldap'] = is_user_from_ldap
        return_dict['development_mode'] = is_development_mode(registry)
        return_dict['is_development'] = registry.settings.get('mode', '') == 'development'
        return_dict['is_production'] = registry.settings.get('mode', '') == 'production'
        return_dict['review_count'] = get_complete_review_count(db_user)
        return_dict['modern_bubbles'] = usage_of_modern_bubbles(registry)
        return_dict['usage_of_matomo'] = usage_of_matomo(registry)

        self.add_language_options_for_extra_dict(return_dict)
        is_author, points = get_reputation_of(db_user)
        is_author_bool = is_author or points > limit_to_open_issues

        return_dict['is_reportable'] = is_reportable
        return_dict['is_admin'] = is_admin
        return_dict['is_special'] = is_special
        return_dict['is_author'] = is_author_bool
        return_dict['is_user'] = not (is_admin or is_author_bool or is_special)
        return_dict['show_bar_icon'] = show_bar_icon
        return_dict['show_graph_icon'] = show_graph_icon
        return_dict['close_premise_container'] = True
        return_dict['close_statement_container'] = True
        return_dict['date'] = arrow.utcnow().format('DD-MM-YYYY')
        return_dict['count_of'] = {
            'arguments': DBDiscussionSession.query(Argument).count(),
            'users': DBDiscussionSession.query(User).count(),
            'discussions': DBDiscussionSession.query(Issue).count(),
            'reviews': get_count_of_all(),
        }
        self.__add_title_text(return_dict, is_logged_in)
        self.__add_button_text(return_dict)
        self.__add_tag_text(return_dict)
        self.__add_login_button_properties(return_dict)

        message_dict = dict()
        message_dict['new_count'] = count_of_new_notifications(db_user) if db_user else 0
        message_dict['has_unread'] = message_dict['new_count'] > 0
        inbox = get_box_for(db_user, self.system_lang, application_url, True) if db_user else []
        outbox = get_box_for(db_user, self.system_lang, application_url, False) if db_user else []
        message_dict['inbox'] = inbox
        message_dict['outbox'] = outbox
        message_dict['total_in'] = len(inbox)
        message_dict['total_out'] = len(outbox)
        return_dict['notifications'] = message_dict

        return return_dict

    def prepare_settings_dict(self, pw_change_success, old_pw, new_pw, confirm_pw, pw_change_error, message, db_user,
                              main_page, use_with_ldap):
        """
        Prepares the dictionary for settings.ow

        :param pw_change_success: Boolean
        :param old_pw: String
        :param new_pw: String
        :param confirm_pw: String
        :param pw_change_error: Boolean
        :param message: String
        :param db_user: User
        :param main_page: String
        :param use_with_ldap: Boolean
        :return: dict()
        """
        _tn = Translator(self.system_lang)

        edits = user.get_edit_count_of(db_user, False)
        statements = user.get_statement_count_of(db_user, False)
        arg_vote, stat_vote = user.get_mark_count_of(db_user)
        arg_clicks, stat_clicks = user.get_click_count_of(db_user)
        public_nick = db_user.global_nickname
        db_group = DBDiscussionSession.query(Group).get(db_user.group_uid)
        db_settings = db_user.settings
        db_language = DBDiscussionSession.query(Language).get(db_settings.lang_uid)

        group = db_group.name if db_group else '-'
        gravatar_public_url = get_profile_picture(db_user, 80)
        reputation, tmp = get_reputation_of(db_user)

        return {
            'passwordold': '' if pw_change_success else old_pw,
            'password': '' if pw_change_success else new_pw,
            'passwordconfirm': '' if pw_change_success else confirm_pw,
            'pw_change_error': pw_change_error,
            'pw_change_success': pw_change_success,
            'message': message,
            'db_firstname': db_user.firstname,
            'db_surname': db_user.surname,
            'db_nickname': db_user.nickname,
            'db_public_nickname': public_nick,
            'db_mail': db_user.email,
            'has_mail': db_user.email is not 'None',
            'can_change_password': not use_with_ldap and db_user.token is None,
            'db_group': group,
            'avatar_public_url': gravatar_public_url,
            'edits_done': edits,
            'statements_posted': statements,
            'discussion_arg_votes': arg_vote,
            'discussion_stat_votes': stat_vote,
            'discussion_arg_clicks': arg_clicks,
            'discussion_stat_clicks': stat_clicks,
            'send_mails': db_settings.should_send_mails,
            'send_notifications': db_settings.should_send_notifications,
            'public_nick': db_settings.should_show_public_nickname,
            'title_mails': _tn.get(_.mailSettingsTitle),
            'title_notifications': _tn.get(_.notificationSettingsTitle),
            'title_public_nick': _tn.get(_.publicNickTitle),
            'title_preferred_lang': _tn.get(_.preferredLangTitle),
            'public_page_url': main_page + '/user/' + str(db_user.uid),
            'on': _tn.get(_.on),
            'off': _tn.get(_.off),
            'current_lang': db_language.name,
            'current_ui_locales': db_language.ui_locales,
            'reputation': reputation
        }

    def add_discussion_end_text(self, discussion_dict, extras_dict, nickname, at_start=False, at_dont_know=False,
                                at_justify_argumentation=False, at_justify=False, current_premise='', supportive=False):
        """
        Adds a specific text when the discussion is at the end

        :param discussion_dict: dict()
        :param extras_dict: dict()
        :param nickname: String or None
        :param at_start: Boolean
        :param at_dont_know: Boolean
        :param at_justify_argumentation: Boolean
        :param at_justify: Boolean
        :param current_premise: id
        :param supportive: supportive
        :return: None
        """
        logger('DictionaryHelper', 'main')
        _tn = Translator(self.discussion_lang)
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        gender = db_user.gender if db_user else None

        if at_start:
            self.__add_discussion_end_text_at_start(discussion_dict, extras_dict, nickname, gender, _tn)

        elif at_justify_argumentation:
            self.__add_discussion_end_text_at_justify_argumentation(discussion_dict, extras_dict, nickname, gender, _tn)

        elif at_dont_know:
            self.__add_discussion_end_text_at_dont_know(discussion_dict, current_premise, gender, _tn, nickname)

        elif at_justify:
            self.__add_discussion_end_text_at_justify_statement(discussion_dict, extras_dict, nickname,
                                                                current_premise, supportive, gender, _tn)

    def __add_discussion_end_text_at_start(self, discussion_dict, extras_dict, nickname, gender, _tn):
        """
        Replaced some text parts in the discussion dict() when the discussion ends in the beginning

        :param discussion_dict: dict()
        :param extras_dict: dict()
        :param nickname: User.nickname
        :param gender: User.gender
        :param _tn: Translator
        :return: None
        """
        discussion_dict['mode'] = 'start'
        if gender == 'f':
            user_text = _tn.get(_.firstPositionTextF)
        elif gender == 'm':
            user_text = _tn.get(_.firstPositionTextM)
        else:
            user_text = _tn.get(_.firstPositionText)
        user_text += '<br>' + (_tn.get(_.pleaseAddYourSuggestion if nickname else _.feelFreeToLogin))

        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        discussion_dict['bubbles'].append(
            create_speechbubble_dict(BubbleTypes.STATUS, content=user_text, db_user=db_user,
                                     lang=self.system_lang))

        is_read_only = DBDiscussionSession.query(Issue).filter_by(slug=extras_dict['slug']).first().is_read_only
        if nickname and not is_read_only:
            extras_dict['add_statement_container_style'] = ''  # this will remove the 'display: none;'-style
            extras_dict['close_statement_container'] = False

        extras_dict['show_display_style'] = False
        extras_dict['show_bar_icon'] = False
        extras_dict['is_editable'] = False
        extras_dict['is_reportable'] = False

    def __add_discussion_end_text_at_justify_argumentation(self, discussion_dict, extras_dict, nickname, gender, _tn):
        """
        Replaced some text parts in the discussion dict() when the discussion ends during the justification

        :param discussion_dict: dict()
        :param extras_dict: dict()
        :param nickname: User.nickname
        :param gender: User.gender
        :param _tn: Translator
        :return: None
        """
        discussion_dict['mode'] = 'justify_argumentation'
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

        is_read_only = DBDiscussionSession.query(Issue).filter_by(slug=extras_dict['slug']).first().is_read_only
        if nickname and not is_read_only:
            extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
        extras_dict['close_premise_container'] = False
        extras_dict['show_display_style'] = False
        if is_read_only:
            mid_text = _tn.get(_.discussionEndAndReadOnly)
            sdict = create_speechbubble_dict(BubbleTypes.INFO, content=mid_text, db_user=db_user,
                                             lang=self.system_lang)
            discussion_dict['bubbles'].append(sdict)

        elif nickname:
            if gender == 'f':
                mid_text = _tn.get(_.firstOneReasonF)
            elif gender == 'm':
                mid_text = _tn.get(_.firstOneReasonM)
            else:
                mid_text = _tn.get(_.firstOneReason)
            sdict = create_speechbubble_dict(BubbleTypes.INFO, content=mid_text, db_user=db_user,
                                             lang=self.system_lang)
            discussion_dict['bubbles'].append(sdict)
        else:
            mid_text = _tn.get(_.discussionEnd) + ' ' + _tn.get(_.feelFreeToLogin)
            sdict = create_speechbubble_dict(BubbleTypes.INFO, content=mid_text, db_user=db_user,
                                             lang=self.system_lang)
            discussion_dict['bubbles'].append(sdict)

    def __add_discussion_end_text_at_dont_know(self, discussion_dict, current_premise, gender, _tn, nickname):
        """
        Replaced some text parts in the discussion dict() when the discussion ends during the don't know step

        :param discussion_dict: dict()
        :param current_premise: String
        :param gender: User.gender
        :param _tn: Translator
        :param nickname: User.nickname
        :return: None
        """
        discussion_dict['mode'] = 'dont_know'
        endtext = _tn.get(_.discussionEndLinkTextLoggedIn if gender else _.discussionEndLinkTextNotLoggedIn)

        if len(current_premise) != 0:
            if gender == 'f':
                sys_text = _tn.get(_.firstOneInformationTextF)
            elif gender == 'm':
                sys_text = _tn.get(_.firstOneInformationTextM)
            else:
                sys_text = _tn.get(_.firstOneInformationText)
            sys_text = sys_text.format('<em>' + current_premise + ' </em>') + ' '
            sys_text += _tn.get(_.untilNowThereAreNoMoreInformation)
            mid_text = _tn.get(_.discussionEnd) + ' ' + endtext
        else:
            sys_text = _tn.get(_.untilNowThereAreNoMoreInformation)
            mid_text = _tn.get(_.discussionEnd) + ' ' + endtext

        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        discussion_dict['bubbles'].append(
            create_speechbubble_dict(BubbleTypes.SYSTEM, content=sys_text, db_user=db_user,
                                     lang=self.system_lang))
        discussion_dict['bubbles'].append(
            create_speechbubble_dict(BubbleTypes.INFO, content=mid_text, db_user=db_user, lang=self.system_lang))

    def __add_discussion_end_text_at_justify_statement(self, discussion_dict, extras_dict, nickname, current_premise,
                                                       supportive, gender, _tn):
        """
        Replaced some text parts in the discussion dict() when the discussion ends during the justification

        :param discussion_dict: dict()
        :param extras_dict: dict()
        :param nickname: User.nickname
        :param current_premise: String
        :param supportive: Boolean
        :param gender: User.gender
        :param _tn: Translator
        :return: None
        """
        discussion_dict['mode'] = 'justify'
        if gender == 'f':
            mid_text = _tn.get(_.firstPremiseText1F)
        elif gender == 'm':
            mid_text = _tn.get(_.firstPremiseText1M)
        else:
            mid_text = _tn.get(_.firstOneInformationText)
        mid_text = mid_text.format('<em>{}</em>'.format(current_premise))

        if not supportive:
            mid_text += ' ' + _tn.get(_.doesNotHold)
        mid_text += '. '

        is_read_only = DBDiscussionSession.query(Issue).filter_by(slug=extras_dict['slug']).first().is_read_only
        if nickname and not is_read_only:
            extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
            mid_text += _tn.get(_.firstPremiseText2)
        else:
            endtext = _tn.get(_.discussionEndLinkTextLoggedIn if gender else _.discussionEndLinkTextNotLoggedIn)
            mid_text += _tn.get(_.discussionEnd) + ' ' + endtext

        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        discussion_dict['bubbles'].append(
            create_speechbubble_dict(BubbleTypes.INFO, content=mid_text, db_user=db_user, lang=self.system_lang))
        extras_dict['close_premise_container'] = False
        extras_dict['show_display_style'] = False
        extras_dict['show_bar_icon'] = False
        extras_dict['is_editable'] = False
        extras_dict['is_reportable'] = False

    def add_language_options_for_extra_dict(self, extras_dict):
        """
        Adds language options to the extra-dictionary

        :param extras_dict: current dict()
        :return: dict()
        """
        logger('DictionaryHelper', 'def')
        lang_is_en = self.system_lang != 'de'
        lang_is_de = self.system_lang == 'de'
        extras_dict.update({
            'ui_locales': self.system_lang,
            'lang_is_de': lang_is_de,
            'lang_is_en': lang_is_en,
            'link_de_class': 'active' if lang_is_de else '',
            'link_en_class': 'active' if lang_is_en else ''
        })

    def __add_button_text(self, return_dict):
        """
        Adds string-map in the return dict with the client_key 'buttons'

        :param return_dict: current dictionary
        :return: None
        """
        _tn_dis = Translator(self.discussion_lang)
        _tn_sys = Translator(self.system_lang)
        return_dict['buttons'] = {
            'show_all_arguments': _tn_sys.get(_.showAllArguments),
            'show_all_users': _tn_sys.get(_.showAllUsers),
            'delete_track': _tn_sys.get(_.deleteTrack),
            'request_track': _tn_sys.get(_.requestTrack),
            'delete_history': _tn_sys.get(_.deleteHistory),
            'request_history': _tn_sys.get(_.requestHistory),
            'password_submit': _tn_sys.get(_.passwordSubmit),
            'contact_submit': _tn_sys.get(_.contactSubmit),
            'bug_submit': _tn_sys.get(_.bugSubmit),
            'previous': _tn_sys.get(_.previous),
            'next': _tn_sys.get(_.next),
            'clear_statistics': _tn_sys.get(_.clearStatistics),
            'go_home': _tn_sys.get(_.letsGoHome),
            'count_of_posts': _tn_sys.get(_.countOfPosts),
            'report': _tn_sys.get(_.report),
            'opinion_barometer': _tn_sys.get(_.opinionBarometer),
            'save_my_statement': _tn_dis.get(_.saveMyStatement),
            'lets_go_back': _tn_sys.get(_.letsGoBack),
            'go_back': _tn_sys.get(_.goBack),
            'go_forward': _tn_sys.get(_.goForward),
            'resume_here': _tn_sys.get(_.resumeHere),
            'request_password': _tn_sys.get(_.requestPassword),
            'ldap_info': _tn_sys.get(_.ldapInfo),
            'show_all_statements': _tn_dis.get(_.statementsShowAll),
            'hide_statements': _tn_dis.get(_.statementsHideAll)
        }

    def __add_title_text(self, return_dict, logged_in):
        """
        Adds string-map in the return dict with the client_key 'title'

        :param return_dict: current dictionary
        :param logged_in: Boolean
        :return: None
        """
        _tn_dis = Translator(self.discussion_lang)
        _tn_sys = Translator(self.system_lang)
        return_dict['title'] = {
            'add_issue_info': _tn_sys.get(_.addIssueInfo).format(
                limit_to_open_issues) if logged_in else _tn_sys.get(_.notLoggedIn),
            'edit_statement': _tn_dis.get(_.editTitle),
            'edit_statement_already': _tn_dis.get(_.editAlreadyTitle),
            'view_changelog': _tn_dis.get(_.viewChangelog),
            'report_statement': _tn_dis.get(_.reportStatement),
            'report_argument': _tn_dis.get(_.reportArgument),
            'delete_statement': _tn_dis.get(_.deleteStatement),
            'disassociate_statement': _tn_dis.get(_.disassociateStatement),
            'question_title': _tn_sys.get(_.questionTitle),
            'more_title': _tn_dis.get(_.more),
            'add_statement_row_title': _tn_dis.get(_.addStatementRow),
            'rem_statement_row_title': _tn_dis.get(_.remStatementRow),
            'recipient': _tn_dis.get(_.recipient),
            'topic': _tn_dis.get(_.topicString),
            'message': _tn_dis.get(_.message),
            'reference': _tn_dis.get(_.reference),
            'attack_statement': _tn_dis.get(_.attackStatement),
            'statement_is_duplicate': _tn_dis.get(_.statementIsDuplicate),
            'you_have_selected_statement': _tn_dis.get(_.youHaveSelectedStatement),
            'no_data_selected': _tn_dis.get(_.noDataSelected),
            'select_statement': _tn_dis.get(_.selectStatement),
            'select_multiple_statements': _tn_dis.get(_.selectMultipleStatementsWhichFlag),
            'because': _tn_dis.get(_.because).lower(),
            'mark_as_opinion': _tn_dis.get(_.mark_as_opinion),
            'unmark_as_opinion': _tn_dis.get(_.unmark_as_opinion),
            'user_is_admin': _tn_dis.get(_.user_is_admin),
            'user_is_special': _tn_dis.get(_.user_is_special),
            'user_is_author': _tn_dis.get(_.user_is_author)
        }

        if logged_in:
            return_dict['add_issue_info'] = _tn_sys.get(_.addIssueInfo).format(limit_to_open_issues)
        else:
            return_dict['add_issue_info'] = _tn_sys.get(_.notLoggedIn),

    def __add_tag_text(self, return_dict):
        """
        Adds string-map in the return dict with the client_key 'tag'

        :param return_dict: current dictionary
        :return: None
        """
        _tn_dis = Translator(self.discussion_lang)
        _tn_sys = Translator(self.system_lang)

        return_dict['tag'] = {
            'add_a_topic': _tn_dis.get(_.addATopic),
            'edit_issue_view_changelog': _tn_dis.get(_.editIssueViewChangelog),
            'edit_title_here': _tn_dis.get(_.editTitleHere),
            'edit_info_here': _tn_dis.get(_.editInfoHere),
            'edit_statement_here': _tn_dis.get(_.editStatementHere),
            'save': _tn_dis.get(_.save),
            'cancel': _tn_dis.get(_.cancel),
            'submit': _tn_dis.get(_.submit),
            'delete': _tn_dis.get(_.delete),
            'close': _tn_dis.get(_.close),
            'url_sharing': _tn_dis.get(_.urlSharing),
            'url_sharing_description': _tn_dis.get(_.urlSharingDescription),
            'fetchurl': _tn_dis.get(_.fetchLongUrl),
            'warning': _tn_dis.get(_.warning),
            'language': self.discussion_lang,
            'aand': _tn_dis.get(_.aand),
            'add_premise_title': _tn_dis.get(_.addPremiseRadioButtonText),
            'arguments': _tn_dis.get(_.arguments),
            'seperated': _tn_dis.get(_.seperated),
            'error': _tn_dis.get(_.error),
            'forgot_input_radio': _tn_dis.get(_.forgotInputRadio),
            'i_actually_have': _tn_dis.get(_.iActuallyHave),
            'insert_one_argument': _tn_dis.get(_.insertOneArgument),
            'insert_dont_care': _tn_dis.get(_.insertDontCare),
            'need_help_to_understand_statement': _tn_dis.get(_.needHelpToUnderstandStatement),
            'set_premisegroups_intro1': _tn_dis.get(_.setPremisegroupsIntro1),
            'set_premisegroups_intro2': _tn_dis.get(_.setPremisegroupsIntro2),
            'placeholder_nickname': _tn_sys.get(_.exampleNickname),
            'placeholder_password': _tn_sys.get(_.examplePassword),
            'placeholder_firstname': _tn_sys.get(_.exampleFirstname),
            'placeholder_lastname': _tn_sys.get(_.exampleLastname),
            'placeholder_mail': _tn_sys.get(_.exampleMail),
            'placeholder_statement': _tn_sys.get(_.exampleStatement),
            'placeholder_source': _tn_sys.get(_.exampleSource),
            'placeholder_search_duplicate': _tn_sys.get(_.exampleSearchDuplicate),
            'placeholder_position': _tn_dis.get(_.examplePosition),
            'placeholder_reason': _tn_dis.get(_.exampleReason),
            'placeholder_add_topic_title': _tn_dis.get(_.exampleAddTopicTitle),
            'placeholder_add_topic_question': _tn_dis.get(_.exampleAddTopicQuestion),
            'placeholder_add_topic_description': _tn_dis.get(_.exampleAddTopicDescription),
            'premisegroup_popup_warning': _tn_dis.get(_.premisegroupPopupWarning),
            'argument_optimization_description': _tn_dis.get(_.argument_optimization_description),
            'argument_offtopic_or_irrelevant_description': _tn_dis.get(_.argument_offtopic_or_irrelevant_description),
            'argument_statement_harmful_description': _tn_dis.get(_.argument_statement_harmful_description),
            'statement_offtopic_or_irrelevant_description': _tn_dis.get(_.statement_offtopic_or_irrelevant_description),
            'statement_duplicate_description': _tn_dis.get(_.statement_duplicate_description),
            'statement_merge_description': _tn_dis.get(_.statement_merge_description),
            'statement_split_description': _tn_dis.get(_.statement_split_description),
            'statement_optimization_description': _tn_dis.get(_.statement_optimization_description),
            'issue_enabled': _tn_sys.get(_.issueEnableDescription),
            'issue_public': _tn_sys.get(_.issuePublicDescription),
            'issue_writable': _tn_sys.get(_.issueWritableDescription)
        }

    def __add_login_button_properties(self, return_dict):
        """
        Check if oauth client ids are available and updates the dict

        :param return_dict: current dictionary
        :return: updated dictionary
        """
        ids = {
            'oauth_google': os.environ.get('OAUTH_GOOGLE_CLIENTID', None),
            'oauth_facebook': os.environ.get('OAUTH_FACEBOOK_CLIENTID', None),
            'oauth_twitter': os.environ.get('OAUTH_TWITTER_CLIENTID', None),
            'oauth_github': os.environ.get('OAUTH_GITHUB_CLIENTID', None),
            'hhu_ldap': os.environ.get('HHU_LDAP_SERVER', None)
        }

        return_dict['login_btns'] = {key: ids[key] is not None for key in ids}
