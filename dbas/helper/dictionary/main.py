"""
Provides helping function for dictionaries.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import datetime
import random

import arrow

from dbas.auth.recaptcha import client_key as google_recaptcha_client_key
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, Language, Group, Settings, Issue
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.helper.notification import count_of_new_notifications, get_box_for
from dbas.helper.query import get_every_attack_for_island_view
from dbas.lib import get_text_for_argument_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion, \
    create_speechbubble_dict, get_profile_picture, get_public_profile_picture, is_usage_with_ldap, is_development_mode
from dbas.logger import logger
from dbas.review.helper.queues import get_complete_review_count
from dbas.review.helper.reputation import get_reputation_of
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_relation_text_dict_with_substitution
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager
from dbas.user_management import is_user_in_group, get_count_of_statements_of_user, get_count_of_votes_of_user, get_count_of_clicks_of_user


class DictionaryHelper(object):
    """
    General function for dictionaries as well as the extras-dict()
    """

    def __init__(self, system_lang='', discussion_lang=''):
        """
        Initialize default values

        :param system_lang: system_lang
        :param discussion_lang: discussion_lang
        :return:
        """
        self.system_lang = system_lang
        self.discussion_lang = discussion_lang if len(discussion_lang) > 0 else system_lang

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
        logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'count: ' + str(count))
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

    def prepare_extras_dict_for_normal_page(self, request, append_notifications=False):
        """
        Calls self.prepare_extras_dict('', False, False, False, False, False, nickname)
        :param request: Request
        :param append_notifications: Boolean
        :return: dict()
        """
        return self.prepare_extras_dict('', False, False, False, False, request, append_notifications=append_notifications, nickname=request.authenticated_userid)

    def prepare_extras_dict(self, current_slug, is_reportable, show_bar_icon, show_island_icon,
                            show_graph_icon, request, nickname, argument_id=0, argument_for_island=0,
                            for_api=False, append_notifications=False, attack=None, broke_limit=False,
                            add_premise_container_style='display: none', add_statement_container_style='display: none'):
        """
        Creates the extras.dict() with many options!

        :param current_slug:
        :param is_reportable: Boolean
        :param show_bar_icon: Boolean
        :param show_island_icon: Boolean
        :param show_graph_icon: Boolean
        :param request: Request
        :param argument_id: Argument.uid, default is 0
        :param argument_for_island: Argument.uid, default is 0
        :param for_api: Boolean
        :param append_notifications: Boolean
        :param attack: String
        :param nickname: String
        :param add_premise_container_style: style string, default 'display:none;'
        :param add_statement_container_style: style string, default 'display:none;'
        :return: dict()
        """
        logger('DictionaryHelper', 'prepare_extras_dict', 'def user ' + str(nickname))
        request_authenticated_userid = nickname
        public_nickname = nickname
        nickname = ''

        db_user = DBDiscussionSession.query(User).filter_by(nickname=str(request_authenticated_userid)).first()
        is_logged_in = db_user is not None
        if request_authenticated_userid:
            nickname = request_authenticated_userid if request_authenticated_userid else nick_of_anonymous_user
            db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
            public_nickname = db_user.get_global_nickname()

        if not db_user or request_authenticated_userid is None:
            nickname = nick_of_anonymous_user
            public_nickname = nick_of_anonymous_user
            db_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()

        is_ldap = is_usage_with_ldap(request)
        is_development = is_development_mode(request)

        rrs = request.registry.settings
        application_url = request.application_url
        if application_url is None:
            application_url = ''
            logger('DictionaryHelper', 'prepare_extras_dict', 'application_url is None', error=True)

        return_dict = dict()
        return_dict['year']                          = datetime.datetime.now().year
        return_dict['restart_url']                   = UrlManager(application_url, current_slug, for_api).get_slug_url(True)
        return_dict['is_in_discussion']              = 'discuss' in request.path
        return_dict['logged_in']                     = is_logged_in
        return_dict['nickname']                      = request_authenticated_userid
        return_dict['public_nickname']               = public_nickname
        return_dict['add_premise_container_style']   = add_premise_container_style
        return_dict['add_statement_container_style'] = add_statement_container_style
        return_dict['users_avatar']                  = get_profile_picture(db_user, 25)
        return_dict['is_user_male']                  = db_user.gender == 'm' if db_user else False
        return_dict['is_user_female']                = db_user.gender == 'f' if db_user else False
        return_dict['is_user_neutral']               = not return_dict['is_user_male'] and not return_dict['is_user_female']
        return_dict['broke_limit']                   = 'true' if broke_limit else 'false'
        return_dict['use_with_ldap']                 = is_ldap
        return_dict['development_mode']              = is_development
        return_dict['is_development']                = rrs['mode'] == 'development' if 'mode' in rrs else ''
        return_dict['is_production']                 = rrs['mode'] == 'production' if 'mode' in rrs else ''
        return_dict['review_count']                  = get_complete_review_count(nickname)
        return_dict['g_recaptcha_key']               = google_recaptcha_client_key

        # add german and english discussion links
        db_issues = DBDiscussionSession.query(Issue).filter_by(is_disabled=False)
        db_de = DBDiscussionSession.query(Language).filter_by(ui_locales='de').first()
        db_en = DBDiscussionSession.query(Language).filter_by(ui_locales='en').first()
        db_issue_de = db_issues.filter_by(lang_uid=db_de.uid).first()
        db_issue_en = db_issues.filter_by(lang_uid=db_en.uid).first()

        return_dict['de_discussion_link'] = '{}/discuss/{}'.format(request.application_url, db_issue_de.get_slug())
        return_dict['en_discussion_link'] = '{}/discuss/{}'.format(request.application_url, db_issue_en.get_slug())

        self.add_language_options_for_extra_dict(return_dict)

        if not for_api:
            return_dict['is_reportable']             = is_reportable
            return_dict['is_admin']                  = is_user_in_group(nickname, 'admins')
            return_dict['is_author']                 = is_user_in_group(nickname, 'authors')
            return_dict['show_bar_icon']             = show_bar_icon
            return_dict['show_island_icon']          = show_island_icon
            return_dict['show_graph_icon']           = show_graph_icon
            return_dict['close_premise_container']   = True
            return_dict['close_statement_container'] = True
            return_dict['date']                      = arrow.utcnow().format('DD-MM-YYYY')
            self.add_title_text(return_dict)
            self.add_button_text(return_dict)
            self.add_tag_text(is_ldap, return_dict)

            message_dict = dict()
            message_dict['new_count']    = count_of_new_notifications(nickname)
            message_dict['has_unread']   = (message_dict['new_count'] > 0)
            inbox = get_box_for(nickname, self.system_lang, application_url, True)
            outbox = get_box_for(nickname, self.system_lang, application_url, False)
            if append_notifications:
                message_dict['inbox']    = inbox
                message_dict['outbox']   = outbox
            message_dict['total_in']     = len(inbox)
            message_dict['total_out']    = len(outbox)
            return_dict['notifications'] = message_dict

            # add everything for the island view
            if show_island_icon:
                # does an argument exists?
                db_argument = DBDiscussionSession.query(Argument).get(argument_id)
                if db_argument:
                    island_dict = get_every_attack_for_island_view(argument_id)

                    premise, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid)
                    conclusion = get_text_for_conclusion(db_argument)
                    island_dict['heading'] = get_text_for_argument_uid(argument_id)

                    island_dict['premise'] = premise[0:1].lower() + premise[1:]
                    island_dict['conclusion'] = conclusion[0:1].lower() + conclusion[1:]
                    db_argument = DBDiscussionSession.query(Argument).get(argument_for_island)
                    _tn = Translator(self.discussion_lang)
                    text_dict = get_relation_text_dict_with_substitution(db_argument.lang, True, attack_type=attack)
                    for t in text_dict:
                        text_dict[t] = text_dict[t][:-1] + ', ' + _tn.get(_.because).lower() + ' ...'

                    island_dict.update(text_dict)
                    return_dict['island'] = island_dict
                else:
                    return_dict['is_editable']      = False
                    return_dict['is_reportable']    = False
                    return_dict['show_bar_icon']    = False
                    return_dict['show_island_icon'] = False
        return return_dict

    def prepare_settings_dict(self, pw_change_success, old_pw, new_pw, confirm_pw, pw_change_error, message, db_user, main_page):
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
        :return: dict()
        """
        _tn         = Translator(self.system_lang)
        edits       = get_count_of_statements_of_user(db_user, True) if db_user else 0
        statements  = get_count_of_statements_of_user(db_user, False) if db_user else 0
        arg_vote, stat_vote = get_count_of_votes_of_user(db_user) if db_user else (0, 0)
        arg_clicks, stat_clicks = get_count_of_clicks_of_user(db_user) if db_user else (0, 0)
        public_nick = db_user.get_global_nickname() if db_user else ''
        db_group    = DBDiscussionSession.query(Group).get(db_user.group_uid) if db_user else None
        group       = db_group.name if db_group else '-'
        gravatar_public_url = get_public_profile_picture(db_user, 120)
        reputation, tmp = get_reputation_of(db_user.nickname)

        db_settings = DBDiscussionSession.query(Settings).get(db_user.uid) if db_user else None
        db_language = DBDiscussionSession.query(Language).get(db_settings.lang_uid) if db_settings else None

        return {
            'passwordold': '' if pw_change_success else old_pw,
            'password': '' if pw_change_success else new_pw,
            'passwordconfirm': '' if pw_change_success else confirm_pw,
            'pw_change_error': pw_change_error,
            'pw_change_success': pw_change_success,
            'message': message,
            'db_firstname': db_user.firstname if db_user else '',
            'db_surname': db_user.surname if db_user else '',
            'db_nickname': db_user.nickname if db_user else '',
            'db_public_nickname': public_nick,
            'db_mail': db_user.email if db_user else '',
            'db_group': group,
            'avatar_public_url': gravatar_public_url,
            'edits_done': edits,
            'statements_posted': statements,
            'discussion_arg_votes': arg_vote,
            'discussion_stat_votes': stat_vote,
            'discussion_arg_clicks': arg_clicks,
            'discussion_stat_clicks': stat_clicks,
            'send_mails': db_settings.should_send_mails if db_settings else False,
            'send_notifications': db_settings.should_send_notifications if db_settings else False,
            'public_nick': db_settings.should_show_public_nickname if db_settings else True,
            'title_mails': _tn.get(_.mailSettingsTitle),
            'title_notifications': _tn.get(_.notificationSettingsTitle),
            'title_public_nick': _tn.get(_.publicNickTitle),
            'title_preferred_lang': _tn.get(_.preferedLangTitle),
            'public_page_url': (main_page + '/user/' + str(db_user.uid)) if db_user else '',
            'on': _tn.get(_.on),
            'off': _tn.get(_.off),
            'current_lang': db_language.name if db_language else '?',
            'current_ui_locales': db_language.ui_locales if db_language else '?',
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
        logger('DictionaryHelper', 'add_discussion_end_text', 'main')
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
            self.__add_discussion_end_text_at_justify_statement(discussion_dict, extras_dict, nickname, current_premise, supportive, gender, _tn)

        else:
            mid_text = _tn.get(_.discussionEnd) + ' ' + _tn.get(_.discussionEndLinkTextLoggedIn if nickname else _.feelFreeToLogin)
            discussion_dict['bubbles'].append(
                create_speechbubble_dict(is_info=True, message=mid_text, lang=self.system_lang, nickname=nickname))

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
        discussion_dict['bubbles'].append(
            create_speechbubble_dict(is_status=True, id='end', message=user_text, lang=self.system_lang, nickname=nickname))

        if nickname:
            extras_dict['add_statement_container_style'] = ''  # this will remove the 'display: none;'-style
            extras_dict['close_statement_container'] = False

        extras_dict['show_display_style'] = False
        extras_dict['show_bar_icon']      = False
        extras_dict['is_editable']        = False
        extras_dict['is_reportable']      = False

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
        if nickname:
            extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
        extras_dict['close_premise_container'] = False
        extras_dict['show_display_style'] = False
        if nickname:
            if gender == 'f':
                mid_text = _tn.get(_.firstOneReasonF)
            elif gender == 'm':
                mid_text = _tn.get(_.firstOneReasonM)
            else:
                mid_text = _tn.get(_.firstOneReason)
            sdict = create_speechbubble_dict(is_info=True, id='end', message=mid_text, lang=self.system_lang, nickname=nickname)
            discussion_dict['bubbles'].append(sdict)
        # else:
            #     mid_text = _tn.get(_.discussionEnd) + ' ' + _tn.get(_.feelFreeToLogin)

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

        if len(current_premise) != 0:
            if gender == 'f':
                sys_text = _tn.get(_.firstOneInformationTextF)
            elif gender == 'm':
                sys_text = _tn.get(_.firstOneInformationTextM)
            else:
                sys_text = _tn.get(_.firstOneInformationText)
            sys_text = sys_text.format('<em>' + current_premise + ' </em>') + ' '
            sys_text += _tn.get(_.untilNowThereAreNoMoreInformation)
            mid_text = _tn.get(_.discussionEnd) + ' ' + _tn.get(_.discussionEndLinkTextLoggedIn if gender else _.discussionEndLinkTextNotLoggedIn)
        else:
            sys_text = _tn.get(_.untilNowThereAreNoMoreInformation)
            mid_text = _tn.get(_.discussionEnd) + ' ' + _tn.get(_.discussionEndLinkTextLoggedIn if gender else _.discussionEndLinkTextNotLoggedIn)

        discussion_dict['bubbles'].append(
            create_speechbubble_dict(is_system=True, id='end', message=sys_text, lang=self.system_lang, nickname=nickname))
        discussion_dict['bubbles'].append(
            create_speechbubble_dict(is_info=True, id='end', message=mid_text, lang=self.system_lang, nickname=nickname))

    def __add_discussion_end_text_at_justify_statement(self, discussion_dict, extras_dict, nickname, current_premise, supportive, gender, _tn):
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
        current_premise = current_premise[0:1].lower() + current_premise[1:]
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

        if nickname:
            extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
            mid_text += _tn.get(_.firstPremiseText2)
        else:
            mid_text += _tn.get(_.discussionEnd) + ' ' + _tn.get(_.discussionEndLinkTextLoggedIn if gender else _.discussionEndLinkTextNotLoggedIn)

        discussion_dict['bubbles'].append(
            create_speechbubble_dict(is_info=True, id='end', message=mid_text, lang=self.system_lang, nickname=nickname))
        extras_dict['close_premise_container'] = False
        extras_dict['show_display_style']      = False
        extras_dict['show_bar_icon']           = False
        extras_dict['is_editable']             = False
        extras_dict['is_reportable']           = False

    def add_language_options_for_extra_dict(self, extras_dict):
        """
        Adds language options to the extra-dictionary

        :param extras_dict: current dict()
        :return: dict()
        """
        logger('DictionaryHelper', 'add_language_options_for_extra_dict', 'def')
        lang_is_en = (self.system_lang != 'de')
        lang_is_de = (self.system_lang == 'de')
        extras_dict.update({
            'ui_locales': self.system_lang,
            'lang_is_de': lang_is_de,
            'lang_is_en': lang_is_en,
            'link_de_class': ('active' if lang_is_de else ''),
            'link_en_class': ('active' if lang_is_en else '')
        })

    def add_button_text(self, return_dict):
        """
        Adds string-map in the return dict with the client_key 'buttons'

        :param return_dict: current dictionary
        :return: None
        """
        _tn_dis = Translator(self.discussion_lang)
        _tn_sys = Translator(self.system_lang)
        return_dict['buttons'] = {'show_all_arguments': _tn_sys.get(_.showAllArguments),
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
                                  'share_url': _tn_sys.get(_.shareUrl),
                                  'lets_go_back': _tn_sys.get(_.letsGoBack),
                                  'go_back': _tn_sys.get(_.goBack),
                                  'go_forward': _tn_sys.get(_.goForward),
                                  'resume_here': _tn_sys.get(_.resumeHere),
                                  'request_password': _tn_sys.get(_.requestPassword),
                                  'ldap_info': _tn_sys.get(_.ldapInfo),
                                  'show_all_statements': _tn_dis.get(_.statementsShowAll),
                                  'hide_statements': _tn_dis.get(_.statementsHideAll),
                                  }

    def add_title_text(self, return_dict):
        """
        Adds string-map in the return dict with the client_key 'title'

        :param return_dict: current dictionary
        :return: None
        """
        _tn_dis = Translator(self.discussion_lang)
        _tn_sys = Translator(self.system_lang)
        return_dict['title'] = {'barometer': _tn_sys.get(_.opinionBarometer),
                                'guided_view': _tn_sys.get(_.displayControlDialogGuidedTitle),
                                'island_view': _tn_sys.get(_.displayControlDialogIslandTitle),
                                'graph_view': _tn_sys.get(_.displayControlDialogGraphTitle),
                                'edit_statement': _tn_dis.get(_.editTitle),
                                'edit_statement_already': _tn_dis.get(_.editAlreadyTitle),
                                'view_changelog': _tn_dis.get(_.viewChangelog),
                                'report_statement': _tn_dis.get(_.reportStatement),
                                'report_argument': _tn_dis.get(_.reportArgument),
                                'delete_statement': _tn_dis.get(_.deleteStatement),
                                'disassociate_statement': _tn_dis.get(_.disassociateStatement),
                                'finish_title': _tn_sys.get(_.finishTitle),
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
                                }

    def add_tag_text(self, is_ldap, return_dict):
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
            'island_view_for': _tn_dis.get(_.islandViewFor),
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
            'placeholder_nickname': _tn_sys.get(_.exampleNicknameLdap) if is_ldap else _tn_sys.get(_.exampleNickname),
            'placeholder_password': _tn_sys.get(_.examplePassword),
            'placeholder_firstname': _tn_sys.get(_.exampleFirstname),
            'placeholder_lastname': _tn_sys.get(_.exampleLastname),
            'placeholder_mail': _tn_sys.get(_.exampleMail),
            'placeholder_statement': _tn_sys.get(_.exampleStatement),
            'placeholder_source': _tn_sys.get(_.exampleSource),
            'placeholder_search_duplicate': _tn_sys.get(_.exampleSearchDuplicate),
            'search': _tn_sys.get(_.searchForStatements),
            'premisegroup_popup_warning': _tn_dis.get(_.premisegroupPopupWarning)
        }
