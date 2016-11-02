"""
Core component of DBAS.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import time

import requests
import transaction

import dbas.handler.news as news_handler
import dbas.helper.history as history_helper
import dbas.helper.issue as issue_helper
import dbas.review.helper.flags as review_flag_helper
import dbas.review.helper.subpage as review_page_helper
import dbas.review.helper.queues as review_queue_helper
import dbas.review.helper.main as review_main_helper
import dbas.review.helper.reputation as review_reputation_helper
import dbas.review.helper.history as review_history_helper
import dbas.strings.matcher as fuzzy_string_matcher
import dbas.user_management as user_manager

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Issue, Argument, Message, Settings, Language, ReviewDeleteReason
from dbas.handler.opinion import OpinionHandler
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.query import QueryHelper
from dbas.helper.notification import send_notification, count_of_new_notifications, get_box_for
from dbas.helper.references import get_references_for_argument, get_references_for_statements, set_reference
from dbas.helper.voting import add_vote_for_argument, clear_votes_of_user
from dbas.helper.views import preparation_for_view, get_nickname_and_session, preparation_for_justify_statement, \
    preparation_for_dont_know_statement, preparation_for_justify_argument, try_to_contact, \
    try_to_register_new_user_via_ajax, request_password
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_position, rep_reason_first_justification,\
    rep_reason_first_argument_click, rep_reason_first_confrontation, rep_reason_first_new_argument, rep_reason_new_statement
from dbas.input_validator import Validator
from dbas.lib import get_language, escape_string, sql_timestamp_pretty_print, get_discussion_language, \
    get_user_by_private_or_public_nickname, get_text_for_statement_uid, is_user_author, get_all_arguments_with_text_and_url_by_statement_id, \
    get_slug_by_statement_uid, get_profile_picture, get_user_by_case_insensitive_nickname
from dbas.logger import logger
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import remember, forget
from pyramid.threadlocal import get_current_registry
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyshorteners.shorteners import Shortener
from requests.exceptions import ReadTimeout
from sqlalchemy import and_
from websocket.lib import send_request_for_recent_delete_review_to_socketio, send_request_for_recent_optimization_review_to_socketio, send_request_for_recent_edit_review_to_socketio

name = 'D-BAS'
version = '0.7.2'
full_version = version + 'a'
project_name = name + ' ' + full_version
issue_fallback = 1
main_page = ''


class Dbas(object):
    """
    Provides every view and ajax-interface.
    """

    def __init__(self, request):
        """
        Object initialization

        :param request: init http request
        :return: json-dict()
        """
        self.request = request
        global main_page
        main_page = request.application_url

        try:
            self.issue_fallback = DBDiscussionSession.query(Issue).first().uid
        except Exception:
            self.issue_fallback = 1

    @staticmethod
    def base_layout():
        renderer = get_renderer('templates/basetemplate.pt')
        layout = renderer.implementation().macros['layout']
        return layout

    # main page
    @view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
    @forbidden_view_config(renderer='templates/index.pt')
    def main_page(self):
        """
        View configuration for the main page

        :return: HTTP 200 with several information
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_page', 'def', 'main, self.request.params: ' + str(self.request.params))
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        session_expired = True if 'session_expired' in self.request.params and self.request.params['session_expired'] == 'true' else False
        ui_locales      = get_language(self.request, get_current_registry())
        _dh             = DictionaryHelper(ui_locales, ui_locales)
        extras_dict     = _dh.prepare_extras_dict_for_normal_page(self.request)
        _dh.add_language_options_for_extra_dict(extras_dict)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': name + ' ' + full_version,
            'project': project_name,
            'extras': extras_dict,
            'session_expired': session_expired
        }

    # contact page
    @view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody', require_csrf=False)
    def main_contact(self):
        """
        View configuration for the contact view.

        :return: dictionary with title and project username as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_contact', 'def', 'main, self.request.params: ' + str(self.request.params))
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        contact_error = False
        send_message = False
        message = ''

        ui_locales = get_language(self.request, get_current_registry())

        username        = escape_string(self.request.params['name'] if 'name' in self.request.params else '')
        email           = escape_string(self.request.params['mail'] if 'mail' in self.request.params else '')
        phone           = escape_string(self.request.params['phone'] if 'phone' in self.request.params else '')
        content         = escape_string(self.request.params['content'] if 'content' in self.request.params else '')
        spamanswer      = escape_string(self.request.params['spam'] if 'spam' in self.request.params else '')

        if 'form.contact.submitted' in self.request.params:
            contact_error, message, sendmessage = try_to_contact(self.request, username, email, phone, content, ui_locales, spamanswer)

        spamquestion, answer = user_manager.get_random_anti_spam_question(ui_locales)
        key = 'contact-antispamanswer'
        self.request.session[key] = answer

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)
        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Contact',
            'project': project_name,
            'extras': extras_dict,
            'was_message_send': send_message,
            'contact_error': contact_error,
            'message': message,
            'name': username,
            'mail': email,
            'phone': phone,
            'content': content,
            'spamanswer': '',
            'spamquestion': spamquestion
        }

    # settings page, when logged in
    @view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
    def main_settings(self):
        """
        View configuration for the content view. Only logged in user can reach this page.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_settings', 'def', 'main, self.request.params: ' + str(self.request.params))
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        ui_locales  = get_language(self.request, get_current_registry())
        old_pw      = ''
        new_pw      = ''
        confirm_pw  = ''
        message     = ''
        error       = False
        success     = False
        db_user     = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
        _uh         = user_manager

        if db_user and 'form.passwordchange.submitted' in self.request.params:
            old_pw = escape_string(self.request.params['passwordold'])
            new_pw = escape_string(self.request.params['password'])
            confirm_pw = escape_string(self.request.params['passwordconfirm'])

            message, error, success = _uh.change_password(transaction, db_user, old_pw, new_pw, confirm_pw, ui_locales)

        _dh = DictionaryHelper(ui_locales)
        extras_dict = _dh.prepare_extras_dict_for_normal_page(self.request)
        settings_dict = _dh.prepare_settings_dict(success, old_pw, new_pw, confirm_pw, error, message, db_user, main_page)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Settings',
            'project': project_name,
            'extras': extras_dict,
            'settings': settings_dict
        }

    # message page, when logged in
    @view_config(route_name='main_notification', renderer='templates/notifications.pt', permission='use')
    def main_notifications(self):
        """
        View configuration for the content view. Only logged in user can reach this page.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_notifications', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)

        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request, append_notifications=True)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Messages',
            'project': project_name,
            'extras': extras_dict
        }

    # news page for everybody
    @view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
    def main_news(self):
        """
        View configuration for the news.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_news', 'def', 'main')
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())
        is_author = is_user_author(self.request.authenticated_userid)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'News',
            'project': project_name,
            'extras': extras_dict,
            'is_author': is_author
        }

    # public users page for everybody
    @view_config(route_name='main_user', renderer='templates/user.pt', permission='everybody')
    def main_user(self):
        """
        View configuration for the public users.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('main_user', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('main_user', 'def', 'main, self.request.params: ' + str(params))

        nickname = match_dict['nickname'] if 'nickname' in match_dict else ''
        nickname = nickname.replace('%20', ' ')
        logger('main_user', 'def', 'nickname: ' + str(nickname))

        current_user = get_user_by_private_or_public_nickname(nickname)
        if current_user is None:
            return HTTPFound(location=UrlManager(main_page).get_404([self.request.path[1:]]))

        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())
        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        user_dict = user_manager.get_information_of(current_user, ui_locales)

        db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
        can_send_notification = False
        if db_user_of_request:
            can_send_notification = current_user.uid != db_user_of_request.uid

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'User ' + nickname,
            'project': project_name,
            'extras': extras_dict,
            'user': user_dict,
            'can_send_notification': can_send_notification
        }

    # imprint
    @view_config(route_name='main_imprint', renderer='templates/imprint.pt', permission='everybody')
    def main_imprint(self):
        """
        View configuration for the imprint.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_imprint', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)
        import pkg_resources
        extras_dict.update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.imprint),
            'project': project_name,
            'extras': extras_dict
        }

    # imprint
    @view_config(route_name='main_publications', renderer='templates/publications.pt', permission='everybody')
    def main_publications(self):
        """
        View configuration for the publcations.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_publications', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.publications),
            'project': project_name,
            'extras': extras_dict
        }

    # 404 page
    @notfound_view_config(renderer='templates/404.pt')
    def notfound(self):
        """
        View configuration for the 404 page.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('notfound', 'def', 'main in ' + str(self.request.method) + '-request' +
               ', path: ' + self.request.path +
               ', view name: ' + self.request.view_name +
               ', params: ' + str(self.request.params))
        path = self.request.path
        if path.startswith('/404/'):
            path = path[4:]

        param_error = True if 'param_error' in self.request.params and self.request.params['param_error'] == 'true' else False
        revoked_content = True if 'revoked_content' in self.request.params and self.request.params['revoked_content'] == 'true' else False

        self.request.response.status = 404
        ui_locales = get_language(self.request, get_current_registry())

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        # return HTTPFound(location=UrlManager(main_page, for_api=False).get_404([self.request.path[1:]]))

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Error',
            'project': project_name,
            'page_notfound_viewname': path,
            'extras': extras_dict,
            'param_error': param_error,
            'revoked_content': revoked_content
        }


# ####################################
# DISCUSSION                         #
# ####################################

    # content page
    @view_config(route_name='discussion_init', renderer='templates/content.pt', permission='everybody')
    def discussion_init(self, for_api=False, api_data=None):
        """
        View configuration for the content view.

        :param for_api: Boolean
        :param api_data: Dictionary, containing data of a user who logged in via API
        :return: dictionary
        """
        # '/a*slug'
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_init', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_init', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, self.request)
        if session_expired:
            return self.user_logout(True)

        count_of_slugs = len(match_dict['slug']) if 'slug' in match_dict and isinstance(match_dict['slug'], ()) else 1
        if count_of_slugs > 1:
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]], True))

        ui_locales = get_language(self.request, get_current_registry())
        if for_api:
            slug = match_dict['slug'] if 'slug' in match_dict else ''
        else:
            slug = match_dict['slug'][0] if 'slug' in match_dict and len(match_dict['slug']) > 0 else ''

        last_topic      = history_helper.get_saved_issue(nickname)
        if len(slug) == 0 and last_topic != 0:
            issue      = last_topic
        else:
            issue      = issue_helper.get_id_of_slug(slug, self.request, True)

        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, for_api)
        item_dict       = ItemDictHelper(disc_ui_locales, issue, main_page, for_api).get_array_for_start(nickname)
        history_helper.save_issue_uid(transaction, issue, nickname)

        discussion_dict = DiscussionDictHelper(disc_ui_locales, session_id, nickname, main_page=main_page, slug=slug)\
            .get_dict_for_start()
        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, True,
                                                                                            False, True, self.request,
                                                                                            application_url=main_page,
                                                                                            for_api=for_api)

        if len(item_dict) == 0:
            DictionaryHelper(disc_ui_locales, disc_ui_locales).add_discussion_end_text(discussion_dict, extras_dict, nickname, at_start=True)

        return_dict = dict()
        return_dict['issues'] = issue_dict
        return_dict['discussion'] = discussion_dict
        return_dict['items'] = item_dict
        return_dict['extras'] = extras_dict

        if for_api:
            return return_dict
        else:
            return_dict['layout'] = self.base_layout()
            return_dict['language'] = str(ui_locales)
            return_dict['title'] = issue_dict['title']
            return_dict['project'] = project_name
            return return_dict

    # attitude page
    @view_config(route_name='discussion_attitude', renderer='templates/content.pt', permission='everybody')
    def discussion_attitude(self, for_api=False, api_data=None):
        """
        View configuration for the content view.

        :param for_api: Boolean
        :param api_data:
        :return: dictionary
        """
        # '/discuss/{slug}/attitude/{statement_id}'
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_attitude', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_attitude', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, self.request)
        if session_expired:
            return self.user_logout(True)

        ui_locales      = get_language(self.request, get_current_registry())
        slug            = match_dict['slug'] if 'slug' in match_dict else ''
        statement_id    = match_dict['statement_id'][0] if 'statement_id' in match_dict else ''
        issue           = issue_helper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else issue_helper.get_issue_id(self.request)

        if not Validator.is_integer(statement_id, True) \
                or not Validator.check_belonging_of_statement(issue, statement_id) \
                or not Validator.is_position(statement_id):
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]], True))
        if Validator.is_statement_forbidden(statement_id):
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]], revoked_content=True))

        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, for_api)

        discussion_dict = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, main_page=main_page, slug=slug)\
            .get_dict_for_attitude(statement_id)
        if not discussion_dict:
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([slug, statement_id]))

        item_dict       = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=self.request.path, history=history)\
            .prepare_item_dict_for_attitude(statement_id)
        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(issue_dict['slug'], False,
                                                                                            True, False, True,
                                                                                            self.request,
                                                                                            application_url=main_page,
                                                                                            for_api=for_api)
        return_dict = dict()
        return_dict['issues'] = issue_dict
        return_dict['discussion'] = discussion_dict
        return_dict['items'] = item_dict
        return_dict['extras'] = extras_dict

        if for_api:
            return return_dict
        else:
            return_dict['layout'] = self.base_layout()
            return_dict['language'] = str(ui_locales)
            return_dict['title'] = issue_dict['title']
            return_dict['project'] = project_name
            return return_dict

    # justify page
    @view_config(route_name='discussion_justify', renderer='templates/content.pt', permission='everybody')
    def discussion_justify(self, for_api=False, api_data=None):
        """
        View configuration for the content view.

        :param for_api: Boolean
        :param api_data:
        :return: dictionary
        """
        # '/discuss/{slug}/justify/{statement_or_arg_id}/{mode}*relation'
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_justify', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, self.request)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())

        slug                = match_dict['slug'] if 'slug' in match_dict else ''
        statement_or_arg_id = match_dict['statement_or_arg_id'] if 'statement_or_arg_id' in match_dict else ''
        mode                = match_dict['mode'] if 'mode' in match_dict else ''
        supportive          = mode == 't' or mode == 'd'  # supportive = t or dont know mode
        relation            = match_dict['relation'][0] if len(match_dict['relation']) > 0 else ''

        if not Validator.is_integer(statement_or_arg_id, True):
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]], True))

        issue               = issue_helper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else issue_helper.get_issue_id(self.request)
        disc_ui_locales     = get_discussion_language(self.request, issue)
        issue_dict          = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, for_api)

        if [c for c in ('t', 'f') if c in mode] and relation == '':
            if not get_text_for_statement_uid(statement_or_arg_id)\
                    or not Validator.check_belonging_of_statement(issue, statement_or_arg_id):
                return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([slug, statement_or_arg_id]))
            item_dict, discussion_dict, extras_dict = preparation_for_justify_statement(self.request, for_api, api_data,
                                                                                        main_page, slug, statement_or_arg_id,
                                                                                        supportive, mode, ui_locales)

        elif 'd' in mode and relation == '':
            if not Validator.check_belonging_of_argument(issue, statement_or_arg_id) and \
                    not Validator.check_belonging_of_statement(issue, statement_or_arg_id):
                return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([slug, statement_or_arg_id]))
            item_dict, discussion_dict, extras_dict = preparation_for_dont_know_statement(self.request, for_api, api_data,
                                                                                          main_page, slug, statement_or_arg_id,
                                                                                          supportive, ui_locales)

        elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
            if not Validator.check_belonging_of_argument(issue, statement_or_arg_id):
                return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([slug, statement_or_arg_id]))
            item_dict, discussion_dict, extras_dict = preparation_for_justify_argument(self.request, for_api, api_data,
                                                                                       main_page, slug, statement_or_arg_id,
                                                                                       supportive, relation, ui_locales)
            # add reputation
            add_reputation_for(nickname, rep_reason_first_confrontation, transaction)
        else:
            logger('discussion_justify', 'def', '404')
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([slug, 'justify', statement_or_arg_id, mode, relation]))

        return_dict = dict()
        return_dict['issues'] = issue_dict
        return_dict['discussion'] = discussion_dict
        return_dict['items'] = item_dict
        return_dict['extras'] = extras_dict

        if for_api:
            return return_dict
        else:
            return_dict['layout'] = self.base_layout()
            return_dict['language'] = str(ui_locales)
            return_dict['title'] = issue_dict['title']
            return_dict['project'] = project_name
            return return_dict

    # reaction page
    @view_config(route_name='discussion_reaction', renderer='templates/content.pt', permission='everybody')
    def discussion_reaction(self, for_api=False, api_data=None):
        """
        View configuration for the content view.

        :param for_api: Boolean
        :param api_data:
        :return: dictionary
        """
        # '/discuss/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys'
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_reaction', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_reaction', 'def', 'main, self.request.params: ' + str(params))

        slug            = match_dict['slug'] if 'slug' in match_dict else ''
        arg_id_user     = match_dict['arg_id_user'] if 'arg_id_user' in match_dict else ''
        attack          = match_dict['mode'] if 'mode' in match_dict else ''
        arg_id_sys      = match_dict['arg_id_sys'] if 'arg_id_sys' in match_dict else ''
        tmp_argument    = DBDiscussionSession.query(Argument).filter_by(uid=arg_id_user).first()
        issue           = issue_helper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else issue_helper.get_issue_id(self.request)

        valid_reaction = Validator.check_reaction(arg_id_user, arg_id_sys, attack)
        if not tmp_argument or not valid_reaction\
                or not valid_reaction and not Validator.check_belonging_of_argument(issue, arg_id_user)\
                or not valid_reaction and not Validator.check_belonging_of_argument(issue, arg_id_sys):
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]]))

        supportive = tmp_argument.is_supportive
        nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, self.request)
        if session_expired:
            return self.user_logout(True)

        # sanity check
        if not [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid', 'end') if c in attack]:
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]], True))

        # set votes and reputation
        add_reputation_for(nickname, rep_reason_first_argument_click, transaction)
        add_vote_for_argument(arg_id_user, nickname, transaction)

        ui_locales      = get_language(self.request, get_current_registry())
        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, for_api)

        _ddh            = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, main_page=main_page, slug=slug)
        _idh            = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=self.request.path, history=history)
        discussion_dict = _ddh.get_dict_for_argumentation(arg_id_user, supportive, arg_id_sys, attack, history, nickname)
        item_dict       = _idh.get_array_for_reaction(arg_id_sys, arg_id_user, supportive, attack)
        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, True, True, True,
                                                                                            True, self.request,
                                                                                            argument_id=arg_id_sys,
                                                                                            application_url=main_page,
                                                                                            for_api=for_api,
                                                                                            argument_for_island=arg_id_user,
                                                                                            attack=attack)

        return_dict = dict()
        return_dict['issues'] = issue_dict
        return_dict['discussion'] = discussion_dict
        return_dict['items'] = item_dict
        return_dict['extras'] = extras_dict

        if for_api:
            return return_dict
        else:
            return_dict['layout'] = self.base_layout()
            return_dict['language'] = str(ui_locales)
            return_dict['title'] = issue_dict['title']
            return_dict['project'] = project_name
            return return_dict

    # finish page
    @view_config(route_name='discussion_finish', renderer='templates/finish.pt', permission='everybody')
    def discussion_finish(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_finish', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_finish', 'def', 'main, self.request.params: ' + str(params))
        ui_locales      = get_language(self.request, get_current_registry())
        nickname        = self.request.authenticated_userid
        session_expired = user_manager.update_last_action(transaction, nickname)
        history_helper.save_path_in_database(nickname, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)
        summary_dict = user_manager.get_summary_of_today(nickname)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Finish',
            'project': project_name,
            'extras': extras_dict,
            'summary': summary_dict,
            'show_summary': len(summary_dict) != 0
        }

    # choosing page
    @view_config(route_name='discussion_choose', renderer='templates/content.pt', permission='everybody')
    def discussion_choose(self, for_api=False, api_data=None):
        """
        View configuration for the choosing view.

        :param for_api: Boolean
        :param api_data:
        :return: dictionary
        """
        # '/discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids'
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_choose', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_choose', 'def', 'main, self.request.params: ' + str(params))

        slug            = match_dict['slug'] if 'slug' in match_dict else ''
        is_argument     = match_dict['is_argument'] if 'is_argument' in match_dict else ''
        is_supportive   = match_dict['supportive'] if 'supportive' in match_dict else ''
        uid             = match_dict['id'] if 'id' in match_dict else ''
        pgroup_ids      = match_dict['pgroup_ids'] if 'id' in match_dict else ''

        is_argument = True if is_argument is 't' else False
        is_supportive = True if is_supportive is 't' else False

        ui_locales      = get_language(self.request, get_current_registry())
        issue           = issue_helper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else issue_helper.get_issue_id(self.request)
        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, for_api)

        if not Validator.check_belonging_of_premisegroups(issue, pgroup_ids):
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]]))

        nickname, session_id, session_expired, history = preparation_for_view(for_api, api_data, self.request)
        if session_expired:
            return self.user_logout(True)

        discussion_dict = DiscussionDictHelper(ui_locales, session_id, nickname, history, main_page=main_page, slug=slug)\
            .get_dict_for_choosing(uid, is_argument, is_supportive)
        item_dict       = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=self.request.path, history=history)\
            .get_array_for_choosing(uid, pgroup_ids, is_argument, is_supportive, nickname)
        if not item_dict:
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]]))

        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, True,
                                                                                            True, True, self.request,
                                                                                            application_url=main_page,
                                                                                            for_api=for_api)

        return_dict = dict()
        return_dict['issues'] = issue_dict
        return_dict['discussion'] = discussion_dict
        return_dict['items'] = item_dict
        return_dict['extras'] = extras_dict

        if for_api:
            return return_dict
        else:
            return_dict['layout'] = self.base_layout()
            return_dict['language'] = str(ui_locales)
            return_dict['title'] = issue_dict['title']
            return_dict['project'] = project_name
            return return_dict

    # jump page
    @view_config(route_name='discussion_jump', renderer='templates/content.pt', permission='everybody')
    def discussion_jump(self, for_api=False, api_data=None):
        """
        View configuration for the jump view.

        :param for_api: Boolean
        :param api_data:
        :return: dictionary
        """
        # '/discuss/{slug}/jump/{arg_id}'
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        match_dict = self.request.matchdict
        params = self.request.params
        logger('discussion_jump', 'def', 'main, self.request.matchdict: ' + str(match_dict))
        logger('discussion_jump', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id = get_nickname_and_session(self.request, for_api, api_data)
        history = params['history'] if 'history' in params else ''

        if for_api and api_data:
            slug = api_data["slug"]
            arg_uid = api_data["arg_uid"]
        else:
            slug = match_dict['slug'] if 'slug' in match_dict else ''
            arg_uid = match_dict['arg_id'] if 'arg_id' in match_dict else ''

        session_expired = user_manager.update_last_action(transaction, nickname)
        history_helper.save_path_in_database(nickname, self.request.path, transaction)
        history_helper.save_history_in_cookie(self.request, self.request.path, history)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())
        issue = issue_helper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else issue_helper.get_issue_id(self.request)
        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, for_api)

        if not Validator.check_belonging_of_argument(issue, arg_uid):
            return HTTPFound(location=UrlManager(main_page, for_api=for_api).get_404([self.request.path[1:]]))

        _ddh = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, main_page=main_page, slug=slug)
        _idh = ItemDictHelper(disc_ui_locales, issue, main_page, for_api, path=self.request.path, history=history)
        discussion_dict = _ddh.get_dict_for_jump(arg_uid)
        item_dict = _idh.get_array_for_jump(arg_uid, slug, for_api)
        extras_dict = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, True,
                                                                                        True, True, self.request,
                                                                                        application_url=main_page,
                                                                                        for_api=for_api)

        return_dict = dict()
        return_dict['issues'] = issue_dict
        return_dict['discussion'] = discussion_dict
        return_dict['items'] = item_dict
        return_dict['extras'] = extras_dict

        if for_api:
            return return_dict
        else:
            return_dict['layout'] = self.base_layout()
            return_dict['language'] = str(ui_locales)
            return_dict['title'] = issue_dict['title']
            return_dict['project'] = project_name
            return return_dict

# ####################################
# REVIEW                             #
# ####################################


# ####################################
# REVIEW                             #
# ####################################

    # index page for reviews
    @view_config(route_name='review_index', renderer='templates/review.pt', permission='use')
    def main_review(self):
        """
        View configuration for the review index.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_review', 'main', 'def ' + str(self.request.matchdict))
        ui_locales = get_language(self.request, get_current_registry())
        nickname = self.request.authenticated_userid
        session_expired = user_manager.update_last_action(transaction, nickname)
        history_helper.save_path_in_database(nickname, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return Dbas(self.request).user_logout(True)

        issue = issue_helper.get_issue_id(self.request)
        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict = issue_helper.prepare_json_of_issue(issue, main_page, disc_ui_locales, False)
        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        review_dict = review_queue_helper.get_review_queues_as_lists(main_page, _tn, nickname)
        count, all_rights = review_reputation_helper.get_reputation_of(nickname)

        return {
            'layout': Dbas.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.review),
            'project': project_name,
            'extras': extras_dict,
            'review': review_dict,
            'privilege_list': review_reputation_helper.get_privilege_list(_tn),
            'reputation_list': review_reputation_helper.get_reputation_list(_tn),
            'issues': issue_dict,
            'reputation': {'count': count,
                           'has_all_rights': all_rights}
        }

    # content page for reviews
    @view_config(route_name='review_content', renderer='templates/review_content.pt', permission='use')
    def review_content(self):
        """
        View configuration for the review content.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_content', 'main', 'def ' + str(self.request.matchdict))
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return Dbas(self.request).user_logout(True)

        subpage_name = self.request.matchdict['queue']
        subpage_dict = review_page_helper.get_subpage_elements_for(self.request, subpage_name,
                                                                   self.request.authenticated_userid, _tn, main_page)
        if not subpage_dict['elements'] and not subpage_dict['has_access'] and not subpage_dict['no_arguments_to_review']:
            return HTTPFound(location=UrlManager(main_page, for_api=False).get_404([self.request.path[1:]]))

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        return {
            'layout': Dbas.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.review),
            'project': project_name,
            'extras': extras_dict,
            'subpage': subpage_dict,
            'lock_time': review_queue_helper.max_lock_time_in_sec
        }

    # history page for reviews
    @view_config(route_name='review_history', renderer='templates/review_history.pt', permission='use')
    def review_history(self):
        """
        View configuration for the review history.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_history', 'main', 'def ' + str(self.request.matchdict))
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return Dbas(self.request).user_logout(True)

        history = review_history_helper.get_review_history(main_page, self.request.authenticated_userid, _tn)
        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        return {
            'layout': Dbas.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.review_history),
            'project': project_name,
            'extras': extras_dict,
            'history': history
        }

    # history page for reviews
    @view_config(route_name='review_ongoing', renderer='templates/review_history.pt', permission='use')
    def ongoing_history(self):
        """
        View configuration for the current reviews.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('ongoing_history', 'main', 'def ' + str(self.request.matchdict))
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return Dbas(self.request).user_logout(True)

        history = review_history_helper.get_ongoing_reviews(main_page, self.request.authenticated_userid, _tn)
        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        return {
            'layout': Dbas.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.review_history),
            'project': project_name,
            'extras': extras_dict,
            'history': history
        }

    # reputation_borders page for reviews
    @view_config(route_name='review_reputation', renderer='templates/review_reputation.pt', permission='use')
    def review_reputation(self):
        """
        View configuration for the review reputation_borders.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_reputation', 'main', 'def ' + str(self.request.matchdict))
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = user_manager.update_last_action(transaction, self.request.authenticated_userid)
        history_helper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return Dbas(self.request).user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request)

        reputation_dict = review_history_helper.get_reputation_history_of(self.request.authenticated_userid, _tn)

        return {
            'layout': Dbas.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.review),
            'project': project_name,
            'extras': extras_dict,
            'reputation': reputation_dict
        }


# ####################################
# ADDTIONAL AJAX STUFF # USER THINGS #
# ####################################

    # ajax - getting complete track of the user
    @view_config(route_name='ajax_get_user_history', renderer='json')
    def get_user_history(self):
        """
        Request the complete user track.

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_user_history', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_list = history_helper.get_history_from_database(self.request.authenticated_userid, ui_locales)
        return json.dumps(return_list, True)

    # ajax - getting all text edits
    @view_config(route_name='ajax_get_all_posted_statements', renderer='json')
    def get_all_posted_statements(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_posted_statements', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_array, tmp = user_manager.get_textversions_of_user(self.request.authenticated_userid, ui_locales)
        return json.dumps(return_array, True)

    # ajax - getting all text edits
    @view_config(route_name='ajax_get_all_edits', renderer='json')
    def get_all_edits(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_edits', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        tmp, return_array = user_manager.get_textversions_of_user(self.request.authenticated_userid, ui_locales)
        return json.dumps(return_array, True)

    # ajax - getting all votes for arguments
    @view_config(route_name='ajax_get_all_argument_votes', renderer='json')
    def get_all_argument_votes(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_argument_votes', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_array = user_manager.get_votes_of_user(self.request.authenticated_userid, True, ui_locales)
        return json.dumps(return_array, True)

    # ajax - getting all votes for statements
    @view_config(route_name='ajax_get_all_statement_votes', renderer='json')
    def get_all_statement_votes(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_statement_votes', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_array = user_manager.get_votes_of_user(self.request.authenticated_userid, False, ui_locales)
        return json.dumps(return_array, True)

    # ajax - deleting complete history of the user
    @view_config(route_name='ajax_delete_user_history', renderer='json')
    def delete_user_history(self):
        """
        Request the complete user history.

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        logger('delete_user_history', 'def', 'main')
        history_helper.delete_history_in_database(self.request.authenticated_userid, transaction)
        return_dict = dict()
        return_dict['removed_data'] = 'true'  # necessary

        return json.dumps(return_dict, True)

    # ajax - deleting complete history of the user
    @view_config(route_name='ajax_delete_statistics', renderer='json')
    def delete_statistics(self):
        """
        Request the complete user history.

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        logger('delete_statistics', 'def', 'main')

        return_dict = dict()
        return_dict['removed_data'] = 'true' if clear_votes_of_user(transaction, self.request.authenticated_userid) else 'false'

        return json.dumps(return_dict, True)

    # ajax - user login
    @view_config(route_name='ajax_user_login', renderer='json')
    def user_login(self, nickname=None, password=None, for_api=False, keep_login=False):
        """
        Will login the user by his nickname and password

        :param nickname: Manually provide nickname (e.g. from API)
        :param password: Manually provide password (e.g. from API)
        :param for_api: Manually provide boolean (e.g. from API)
        :param keep_login: Manually provide boolean (e.g. from API)
        :return: dict() with error
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('user_login', 'def', 'main, self.request.params: ' + str(self.request.params))

        lang = get_language(self.request, get_current_registry())
        _tn = Translator(lang)

        try:
            if not nickname and not password:
                nickname = escape_string(self.request.params['user'])
                password = escape_string(self.request.params['password'])
                keep_login = escape_string(self.request.params['keep_login'])
                keep_login = True if keep_login == 'true' else False
                url = self.request.params['url']
            else:
                nickname = escape_string(nickname)
                password = escape_string(password)
                url = ''

            db_user = get_user_by_case_insensitive_nickname(nickname)

            # check for user and password validations
            if not db_user:
                logger('user_login', 'no user', 'user \'' + nickname + '\' does not exists')
                error = _tn.get(_tn.userPasswordNotMatch)
            elif not db_user.validate_password(password):
                logger('user_login', 'password not valid', 'wrong password')
                error = _tn.get(_tn.userPasswordNotMatch)
            else:
                logger('user_login', 'login', 'login successful / keep_login: ' + str(keep_login))
                db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
                db_settings.should_hold_the_login(keep_login)
                headers = remember(self.request, db_user.nickname)

                # update timestamp
                logger('user_login', 'login', 'update login timestamp')
                db_user.update_last_login()
                db_user.update_last_action()
                transaction.commit()
                ending = ['/?session_expired=true', '/?session_expired=false']
                for e in ending:
                    if url.endswith(e):
                        url = url[0:-len(e)]

                if for_api:
                    logger('user_login', 'return', 'for api: success')
                    return {'status': 'success'}
                else:
                    logger('user_login', 'return', 'success: ' + url)
                    time.sleep(0.5)
                    return HTTPFound(
                        location=url,
                        headers=headers,
                    )

        except KeyError as e:
            error = _tn.get(_tn.internalKeyError)
            logger('user_login', 'error', repr(e))

        return_dict = dict()
        return_dict['error'] = error

        logger('user_login', 'return', str(return_dict))
        return json.dumps(return_dict, True)

    # ajax - user logout
    @view_config(route_name='ajax_user_logout', renderer='json')
    def user_logout(self, redirect_to_main=False):
        """
        Will logout the user

        :param redirect_to_main: Boolean
        :return: HTTPFound with forgotten headers
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('user_logout', 'def', 'main, user: ' + str(self.request.authenticated_userid) + ', redirect_to_main: ' + str(redirect_to_main))
        self.request.session.invalidate()
        headers = forget(self.request)
        if redirect_to_main:
            return HTTPFound(
                location=main_page + '?session_expired=true',
                headers=headers,
            )
        else:
            self.request.response.headerlist.extend(headers)
            return self.request.response

    # ajax - registration of users
    @view_config(route_name='ajax_user_registration', renderer='json')
    def user_registration(self):
        """
        Registers new user

        :return: dict() with success and message
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('user_registration', 'def', 'main, self.request.params: ' + str(self.request.params))

        # default values
        success = ''
        error = ''
        info = ''
        return_dict = dict()

        ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
        if not ui_locales:
            ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        # getting params
        try:
            success, info = try_to_register_new_user_via_ajax(self.request, ui_locales)

        except KeyError as e:
            logger('user_registration', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        # get anti-spam-question
        spamquestion, answer = user_manager.get_random_anti_spam_question(ui_locales)
        # save answer in session
        self.request.session['antispamanswer'] = answer

        return_dict['success']      = str(success)
        return_dict['error']        = str(error)
        return_dict['info']         = str(info)
        return_dict['spamquestion'] = str(spamquestion)

        return json.dumps(return_dict, True)

    # ajax - password requests
    @view_config(route_name='ajax_user_password_request', renderer='json')
    def user_password_request(self):
        """
        Sends an email, when the user requests his password

        :return: dict() with success and message
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('user_password_request', 'def', 'main, self.request.params: ' + str(self.request.params))

        success = ''
        info = ''
        return_dict = dict()
        ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
        if not ui_locales:
            ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        try:
            success, error, info = request_password(self.request, ui_locales)

        except KeyError as e:
            logger('user_password_request', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        return_dict['success'] = str(success)
        return_dict['error']   = str(error)
        return_dict['info']    = str(info)

        logger('user_password_request', 'success', str(success))
        logger('user_password_request', 'error', str(error))
        logger('user_password_request', 'info', str(info))

        return json.dumps(return_dict, True)

    # ajax - set boolean for receiving information
    @view_config(route_name='ajax_set_user_setting', renderer='json')
    def set_user_settings(self):
        """
        Will logout the user

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_user_settings', 'def', 'main, self.request.params: ' + str(self.request.params))
        _tn = Translator(get_language(self.request, get_current_registry()))

        try:
            error = ''
            public_nick = ''
            public_page_url = ''
            gravatar_url = ''
            settings_value = True if self.request.params['settings_value'] == 'True' else False
            service = self.request.params['service']
            db_user = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
            if db_user:
                public_nick = db_user.public_nickname
                db_setting = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()

                if service == 'mail':
                    db_setting.set_send_mails(settings_value)

                elif service == 'notification':
                    db_setting.set_send_notifications(settings_value)

                elif service == 'public_nick':
                    db_setting.set_show_public_nickname(settings_value)
                    if settings_value:
                        db_user.set_public_nickname(db_user.nickname)
                    elif db_user.nickname == db_user.public_nickname:
                        user_manager.refresh_public_nickname(db_user)
                    public_nick = db_user.public_nickname
                else:
                    error = _tn.get(_tn.keyword)

                transaction.commit()
                public_page_url = main_page + '/user/' + (db_user.nickname if settings_value else public_nick)
                gravatar_url = get_profile_picture(db_user, 80, ignore_privacy_settings=settings_value)
            else:
                error = _tn.get(_tn.checkNickname)
        except KeyError as e:
            error = _tn.get(_tn.internalKeyError)
            public_nick = ''
            public_page_url = ''
            gravatar_url = ''
            logger('set_user_settings', 'error', repr(e))

        return_dict = {'error': error, 'public_nick': public_nick, 'public_page_url': public_page_url, 'gravatar_url': gravatar_url}
        return json.dumps(return_dict, True)

    # ajax - set boolean for receiving information
    @view_config(route_name='ajax_set_user_language', renderer='json')
    def set_user_language(self):
        """
        Will logout the user

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_user_language', 'def', 'main, self.request.params: ' + str(self.request.params))
        _tn = Translator(get_language(self.request, get_current_registry()))

        try:
            error = ''
            current_lang = ''
            ui_locales = self.request.params['ui_locales']
            db_user = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
            if db_user:
                db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
                if db_settings:
                    db_language = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
                    if db_language:
                        current_lang = db_language.name
                        db_settings.set_lang_uid(db_language.uid)
                        transaction.commit()
                    else:
                        error = _tn.get(_tn.internalError)
                else:
                    error = _tn.get(_tn.checkNickname)
            else:
                error = _tn.get(_tn.checkNickname)
        except KeyError as e:
            error = _tn.get(_tn.internalKeyError)
            ui_locales = ''
            current_lang = ''
            logger('set_user_settings', 'error', repr(e))

        return_dict = {'error': error, 'ui_locales': ui_locales, 'current_lang': current_lang}
        return json.dumps(return_dict, True)

    # ajax - sending notification
    @view_config(route_name='ajax_send_notification', renderer='json')
    def send_notification(self):
        """
        Set a new message into the inbox of an recipient, and the outbox of the sender.

        :return: dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('send_notification', 'def', 'main, self.request.params: ' + str(self.request.params))

        error = ''
        ts = ''
        uid = ''
        gravatar = ''
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        try:
            recipient = self.request.params['recipient'].replace('%20', ' ')
            title     = self.request.params['title']
            text      = self.request.params['text']
            db_recipient = get_user_by_private_or_public_nickname(recipient)
            if len(title) < 5 or len(text) < 5:
                error = _tn.get(_tn.empty_notification_input) + ' (' + _tn.get(_tn.minLength) + ': 5)'
            elif not db_recipient or recipient == 'admin' or recipient == 'anonymous':
                error = _tn.get(_tn.recipientNotFound)
            else:
                db_author = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
                if not db_author:
                    error = _tn.get(_tn.notLoggedIn)
                else:
                    db_notification = send_notification(db_author, db_recipient, title, text, main_page, transaction)
                    uid = db_notification.uid
                    ts = sql_timestamp_pretty_print(db_notification.timestamp, ui_locales)
                    gravatar = get_profile_picture(db_recipient, 20)

        except KeyError:
            error = _tn.get(_tn.internalKeyError)

        return_dict = {'error': error, 'timestamp': ts, 'uid': uid, 'recipient_avatar': gravatar}
        return json.dumps(return_dict, True)


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################

    # ajax - send new start statement
    @view_config(route_name='ajax_set_new_start_statement', renderer='json')
    def set_new_start_statement(self, for_api=False, api_data=None):
        """
        Inserts a new statement into the database, which should be available at the beginning

        :param for_api: boolean
        :param api_data: api_data
        :return: a status code, if everything was successful
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_new_start_statement', 'def', 'ajax, self.request.params: ' + str(self.request.params))

        logger('set_new_start_statement', 'def', 'main')

        discussion_lang = get_discussion_language(self.request)
        _tn = Translator(discussion_lang)
        return_dict = dict()
        return_dict['error'] = ''
        return_dict['statement_uids'] = []
        try:
            if for_api and api_data:
                nickname  = api_data["nickname"]
                statement = api_data["statement"]
                issue     = api_data["issue_id"]
                slug      = api_data["slug"]
            else:
                nickname    = self.request.authenticated_userid
                statement   = self.request.params['statement']
                issue       = issue_helper.get_issue_id(self.request)
                slug        = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()

            # escaping will be done in QueryHelper().set_statement(...)
            user_manager.update_last_action(transaction, nickname)
            new_statement = QueryHelper.insert_as_statements(transaction, statement, nickname, issue, is_start=True)
            if new_statement == -1:
                return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseEmpty) + ' (' + _tn.get(_tn.minLength) + ': 10)'
            else:
                url = UrlManager(main_page, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
                return_dict['url'] = url
                return_dict['statement_uids'].append(new_statement[0].uid)

                # add reputation
                if not add_reputation_for(nickname, rep_reason_first_position, transaction):
                    add_reputation_for(nickname, rep_reason_new_statement, transaction)

        except KeyError as e:
            logger('set_new_start_statement', 'error', repr(e))
            return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

        return json.dumps(return_dict, True)

    # ajax - send new start premise
    @view_config(route_name='ajax_set_new_start_premise', renderer='json')
    def set_new_start_premise(self, for_api=False, api_data=None):
        """
        Sets new premise for the start

        :param for_api: boolean
        :param api_data:
        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_new_start_premise', 'def', 'main, self.request.params: ' + str(self.request.params))

        return_dict = dict()
        lang = get_language(self.request, get_current_registry())
        _tn = Translator(lang)
        try:
            if for_api and api_data:
                nickname      = api_data['nickname']
                premisegroups = api_data['statement']
                issue         = api_data['issue_id']
                conclusion_id = api_data['conclusion_id']
                supportive    = api_data['supportive']
            else:
                nickname        = self.request.authenticated_userid
                issue           = issue_helper.get_issue_id(self.request)
                premisegroups   = json.loads(self.request.params['premisegroups'])
                conclusion_id   = self.request.params['conclusion_id']
                supportive      = True if self.request.params['supportive'].lower() == 'true' else False

            # escaping will be done in QueryHelper().set_statement(...)
            user_manager.update_last_action(transaction, nickname)

            _qh = QueryHelper
            url, statement_uids, error = _qh.process_input_of_start_premises_and_receive_url(self.request, transaction,
                                                                                             premisegroups, conclusion_id,
                                                                                             supportive, issue, nickname,
                                                                                             for_api, main_page, lang)

            return_dict['error'] = error
            return_dict['statement_uids'] = statement_uids

            # add reputation
            if not add_reputation_for(nickname, rep_reason_first_justification, transaction):
                add_reputation_for(nickname, rep_reason_new_statement, transaction)

            if url == -1:
                return json.dumps(return_dict, True)

            return_dict['url'] = url
        except KeyError as e:
            logger('set_new_start_premise', 'error', repr(e))
            return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseInternal)

        return json.dumps(return_dict, True)

    # ajax - send new premises
    @view_config(route_name='ajax_set_new_premises_for_argument', renderer='json')
    def set_new_premises_for_argument(self, for_api=False, api_data=None):
        """
        Sets a new premise for an argument

        :param api_data:
        :param for_api: boolean
        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_new_premises_for_argument', 'def', 'main, self.request.params: ' + str(self.request.params))

        return_dict = dict()
        lang = get_language(self.request, get_current_registry())
        _tn = Translator(lang)

        try:
            if for_api and api_data:
                nickname      = api_data['nickname']
                premisegroups = api_data['statement']
                issue         = api_data['issue_id']
                arg_uid       = api_data['arg_uid']
                attack_type   = api_data['attack_type']
            else:
                nickname = self.request.authenticated_userid
                premisegroups = json.loads(self.request.params['premisegroups'])
                issue = issue_helper.get_issue_id(self.request)
                arg_uid = self.request.params['arg_uid']
                attack_type = self.request.params['attack_type']

            # escaping will be done in QueryHelper().set_statement(...)
            _qh = QueryHelper
            url, statement_uids, error = _qh.process_input_of_premises_for_arguments_and_receive_url(self.request,
                                                                                                     transaction, arg_uid,
                                                                                                     attack_type,
                                                                                                     premisegroups, issue,
                                                                                                     nickname, for_api,
                                                                                                     main_page, lang)
            user_manager.update_last_action(transaction, nickname)

            return_dict['error'] = error
            return_dict['statement_uids'] = statement_uids

            # add reputation
            if not add_reputation_for(nickname, rep_reason_first_new_argument, transaction):
                add_reputation_for(nickname, rep_reason_new_statement, transaction)

            if url == -1:
                return json.dumps(return_dict, True)

            return_dict['url'] = url

        except KeyError as e:
            logger('set_new_premises_for_argument', 'error', repr(e))
            return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseInternal)

        logger('set_new_premises_for_argument', 'def', 'returning ' + str(return_dict))
        return json.dumps(return_dict, True)

    # ajax - set new textvalue for a statement
    @view_config(route_name='ajax_set_correction_of_statement', renderer='json')
    def set_correction_of_statement(self):
        """
        Sets a new textvalue for a statement

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_correction_of_statement', 'def', 'main, self.request.params: ' + str(self.request.params))
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        _tn = Translator(get_language(self.request, get_current_registry()))

        return_dict = dict()
        try:
            elements = json.loads(self.request.params['elements'])
            nickname = self.request.authenticated_userid
            return_dict['error'] = review_queue_helper.add_proposals_for_statement_corrections(elements, nickname, _tn, transaction)
        except KeyError as e:
            return_dict['error'] = _tn.get(_tn.noCorrections)
            logger('set_correction_of_statement', 'error', repr(e))

        return json.dumps(return_dict, True)

    # ajax - set notification as read
    @view_config(route_name='ajax_notification_read', renderer='json')
    def set_notification_read(self):
        """
        Set notification as read

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        logger('set_notification_read', 'def', 'main ' + str(self.request.params))
        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        try:
            DBDiscussionSession.query(Message).filter_by(uid=self.request.params['id']).first().set_read(True)
            transaction.commit()
            return_dict['unread_messages'] = count_of_new_notifications(self.request.authenticated_userid)
            return_dict['error'] = ''
        except KeyError as e:
            logger('set_message_read', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - deletes a notification
    @view_config(route_name='ajax_notification_delete', renderer='json')
    def set_notification_delete(self):
        """
        Request the removal of a notification

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        logger('set_notification_delete', 'def', 'main ' + str(self.request.params))
        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        try:
            DBDiscussionSession.query(Message).filter_by(uid=self.request.params['id']).delete()
            transaction.commit()
            return_dict['unread_messages'] = count_of_new_notifications(self.request.authenticated_userid)
            return_dict['total_in_messages'] = str(len(get_box_for(self.request.authenticated_userid, ui_locales, main_page, True)))
            return_dict['total_out_messages'] = str(len(get_box_for(self.request.authenticated_userid, ui_locales, main_page, False)))
            return_dict['error'] = ''
            return_dict['success'] = _t.get(_t.messageDeleted)
        except KeyError as e:
            logger('set_message_read', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalKeyError)
            return_dict['success'] = ''

        return json.dumps(return_dict, True)

    # ajax - set new issue
    @view_config(route_name='ajax_set_new_issue', renderer='json')
    def set_new_issue(self):
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        logger('set_new_issue', 'def', 'main ' + str(self.request.params))
        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        try:
            info = escape_string(self.request.params['info'])
            title = escape_string(self.request.params['title'])
            lang = escape_string(self.request.params['lang'])
            was_set, error = issue_helper.set_issue(info, title, lang, self.request.authenticated_userid, transaction, ui_locales)
            if was_set:
                db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
                                                                        Issue.info == info)).first()
                return_dict['issue'] = issue_helper.get_issue_dict_for(db_issue, main_page, False, 0, ui_locales)
        except KeyError as e:
            logger('set_new_issue', 'error', repr(e))
            error = _tn.get(_tn.notInsertedErrorBecauseInternal)

        return_dict['error'] = error
        return json.dumps(return_dict, True)

# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################

    # ajax - getting changelog of a statement
    @view_config(route_name='ajax_get_logfile_for_statements', renderer='json')
    def get_logfile_for_premisegroup(self):
        """
        Returns the changelog of a statement

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_logfile_for_statements', 'def', 'main, self.request.params: ' + str(self.request.params))
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())

        try:
            uids = json.loads(self.request.params['uids'])
            issue = self.request.params['issue']
            ui_locales = get_discussion_language(self.request, issue)
            return_dict = QueryHelper.get_logfile_for_statements(uids, ui_locales, main_page)
            return_dict['error'] = ''
        except KeyError as e:
            logger('get_logfile_for_premisegroup', 'error', repr(e))
            _tn = Translator(ui_locales)
            return_dict['error'] = _tn.get(_tn.noCorrections)

        return json.dumps(return_dict, True)

    # ajax - for shorten url
    @view_config(route_name='ajax_get_shortened_url', renderer='json')
    def get_shortened_url(self):
        """
        Shortens url with the help of a python lib

        :return: dictionary with shortend url
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)

        logger('get_shortened_url', 'def', 'main')

        return_dict = dict()

        try:
            url = self.request.params['url']
            # google_api_key = 'AIzaSyAw0aPsBsAbqEJUP_zJ9Fifbhzs8xkNSw0' # browser is
            # google_api_key = 'AIzaSyDneaEJN9FNGUpXHDZahe9Rhb21FsFNS14' # server id
            # service = 'GoogleShortener'
            # service_url = 'https://goo.gl/'
            # shortener = Shortener(service, api_key=google_api_key)

            # bitly_login = 'dbashhu'
            # bitly_key = ''
            # bitly_token = 'R_d8c4acf2fb554494b65529314d1e11d1'

            # service = 'BitlyShortener'
            # service_url = 'https://bitly.com/'
            # shortener = Shortener(service, bitly_token=bitly_token)

            service = 'TinyurlShortener'
            service_ = 'Tinyurl'
            service_url = 'http://tinyurl.com/'
            shortener = Shortener(service_)

            short_url = format(shortener.short(url))
            return_dict['url'] = short_url
            return_dict['service'] = service
            return_dict['service_url'] = service_url

            return_dict['error'] = ''
        except KeyError as e:
            logger('get_shortened_url', 'error', repr(e))
            _tn = Translator(get_discussion_language(self.request))
            return_dict['error'] = _tn.get(_tn.internalKeyError)
        except ReadTimeout as e:
            logger('get_shortened_url', 'read timeout error', repr(e))
            _tn = Translator(get_discussion_language(self.request))
            return_dict['error'] = _tn.get(_tn.internalError)

        return json.dumps(return_dict, True)

    # ajax - for getting all news
    @view_config(route_name='ajax_get_news', renderer='json')
    def get_news(self):
        """
        ajax interface for getting news

        :return: json-set with all news
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_news', 'def', 'main')
        return_dict = news_handler.get_news(get_language(self.request, get_current_registry()))
        return json.dumps(return_dict, True)

    # ajax - for getting argument infos
    @view_config(route_name='ajax_get_infos_about_argument', renderer='json')
    def get_infos_about_argument(self):
        """
        ajax interface for getting a dump

        :return: json-set with everything
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_infos_about_argument', 'def', 'main, self.request.params: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            uid = self.request.params['uid']
            if not Validator.is_integer(uid):
                return_dict['error'] = _t.get(_t.internalError)
            else:
                return_dict = QueryHelper.get_infos_about_argument(uid, main_page)
                return_dict['error'] = ''
        except KeyError as e:
            logger('get_infos_about_argument', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - for getting all users with the same opinion
    @view_config(route_name='ajax_get_user_with_same_opinion', renderer='json')
    def get_users_with_same_opinion(self):
        """
        ajax interface for getting a dump
        :return: json-set with everything
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_users_with_same_opinion', 'def', 'main: ' + str(self.request.params))
        nickname = self.request.authenticated_userid
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        return_dict = dict()
        try:
            params = self.request.params
            ui_locales  = params['lang'] if 'lang' in params else 'en'
            uids        = params['uids']
            attack      = params['attack'] if len(params['attack']) > 0 else None
            is_argument = params['is_argument'] == 'true' if 'is_argument' in params else False
            is_attitude = params['is_attitude'] == 'true' if 'is_attitude' in params else False
            is_reaction = params['is_reaction'] == 'true' if 'is_reaction' in params else False
            is_position = params['is_position'] == 'true' if 'is_position' in params else False
            is_supporti = params['is_supporti'] if 'is_supporti' in params else None

            _op = OpinionHandler(ui_locales, nickname, main_page)
            if is_argument:
                if not is_reaction:
                    return_dict = _op.get_user_with_same_opinion_for_argument(uids)
                else:
                    uids = json.loads(uids)
                    return_dict = _op.get_user_and_opinions_for_argument(uids, attack)
            elif is_position:
                uids = json.loads(uids)
                return_dict = _op.get_user_with_same_opinion_for_statements(uids if isinstance(uids, list) else [uids], is_supporti)
            else:
                if not is_attitude:
                    uids = json.loads(uids)
                    return_dict = _op.get_user_with_same_opinion_for_premisegroups(uids if isinstance(uids, list) else [uids])
                else:
                    return_dict = _op.get_user_with_opinions_for_attitude(uids)
            return_dict['error'] = ''
        except KeyError as e:
            logger('get_users_with_same_opinion', 'error', repr(e))
            return_dict['error'] = _tn.get(_tn.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - for getting all users with the same opinion
    @view_config(route_name='ajax_get_public_user_data', renderer='json')
    def get_public_user_data(self):
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_public_user_data', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        return_dict = dict()
        try:
            nickname = self.request.params['nickname']
            return_dict = user_manager.get_public_information_data(nickname, ui_locales)
            return_dict['error'] = '' if len(return_dict) != 0 else _tn.get(_tn.internalKeyError)

        except KeyError as e:
            logger('get_public_user_data', 'error', repr(e))
            return_dict['error'] = _tn.get(_tn.internalKeyError)

        return json.dumps(return_dict, True)

    @view_config(route_name='ajax_get_arguments_by_statement_uid', renderer='json')
    def get_arguments_by_statement_uid(self):
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_arguments_by_statement_uid', 'def', 'main: ' + str(self.request.matchdict))
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        return_dict = dict()
        try:
            uid = self.request.matchdict['uid']
            if not Validator.is_integer(uid):
                return_dict['error'] = _tn.get(_tn.internalKeyError)
            else:
                slug = get_slug_by_statement_uid(uid)
                _um = UrlManager(main_page, slug)
                return_dict['arguments'] = get_all_arguments_with_text_and_url_by_statement_id(uid, _um, True)
                return_dict['error'] = ''

        except KeyError as e:
            logger('get_arguments_by_statement_uid', 'error', repr(e))
            return_dict['error'] = _tn.get(_tn.internalKeyError)

        return json.dumps(return_dict, True)

    @view_config(route_name='ajax_get_references', renderer='json')
    def get_references(self):
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_references', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        try:
            uid = json.loads(self.request.params['uid'])
            is_argument = True if str(self.request.params['is_argument']) == 'true' else False

            if is_argument:
                data, text = get_references_for_argument(uid, main_page)
            else:
                data, text = get_references_for_statements(uid, main_page)

            return_dict = {'error': '',
                           'data': data,
                           'text': text}

        except KeyError as e:
            logger('get_references', 'error', repr(e))
            return_dict = {'error': _tn.get(_tn.internalKeyError)}

        return json.dumps(return_dict, True)

    @view_config(route_name='ajax_set_references', renderer='json')
    def set_references(self):
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_references', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        try:
            nickname    = self.request.authenticated_userid
            issue_uid   = issue_helper.get_issue_id(self.request)

            uid         = self.request.params['uid']
            reference   = escape_string(json.loads(self.request.params['reference']))
            source      = escape_string(json.loads(self.request.params['ref_source']))
            success     = set_reference(reference, source, nickname, uid, issue_uid, transaction)
            return_dict = {'error': '' if success else _tn.get(_tn.internalKeyError)}

        except KeyError as e:
            logger('set_references', 'error', repr(e))
            return_dict = {'error': _tn.get(_tn.internalKeyError)}

        return json.dumps(return_dict, True)

# ########################################
# ADDTIONAL AJAX STUFF # ADDITION THINGS #
# ########################################

    # ajax - for language switch
    @view_config(route_name='ajax_switch_language', renderer='json')
    def switch_language(self):
        """
        Switches the language

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        user_manager.update_last_action(transaction, self.request.authenticated_userid)
        logger('switch_language', 'def', 'main, self.request.params: ' + str(self.request.params))

        return_dict = dict()
        ui_locales = None
        try:
            ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
            if not ui_locales:
                ui_locales = get_language(self.request, get_current_registry())
            self.request.response.set_cookie('_LOCALE_', str(ui_locales))
            return_dict['error'] = ''
        except KeyError as e:
            logger('swich_language', 'error', repr(e))
            if not ui_locales:
                ui_locales = 'en'
            _t = Translator(ui_locales)
            return_dict['error'] = _t.get(_t.internalError)

        return json.dumps(return_dict, True)

    # ajax - for sending news
    @view_config(route_name='ajax_send_news', renderer='json')
    def send_news(self):
        """
        ajax interface for settings news

        :return: json-set with new news
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('send_news', 'def', 'main, self.request.params: ' + str(self.request.params))

        try:
            title = escape_string(self.request.params['title'])
            text = escape_string(self.request.params['text'])
            return_dict = news_handler.set_news(transaction, title, text, self.request.authenticated_userid, get_language(self.request, get_current_registry()))
            return_dict['error'] = ''
        except KeyError as e:
            return_dict = dict()
            logger('send_news', 'error', repr(e))
            _tn = Translator(get_language(self.request, get_current_registry()))
            return_dict['error'] = _tn.get(_tn.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - for fuzzy search
    @view_config(route_name='ajax_fuzzy_search', renderer='json')
    def fuzzy_search(self, for_api=False, api_data=None):
        """
        ajax interface for fuzzy string search

        :param for_api: boolean
        :param api_data: data
        :return: json-set with all matched strings
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('fuzzy_search', 'def', 'main, for_api: ' + str(for_api) + ', self.request.params: ' + str(self.request.params))

        _tn = Translator(get_language(self.request, get_current_registry()))

        try:
            value = api_data["value"] if for_api else self.request.params['value']
            mode = str(api_data["mode"]) if for_api else str(self.request.params['type'])
            issue = api_data["issue"] if for_api else issue_helper.get_issue_id(self.request)

            return_dict = dict()

            if mode == '0':  # start statement
                return_dict['distance_name'], return_dict['values'] = fuzzy_string_matcher.get_strings_for_start(value, issue, True)
            elif mode == '1':  # edit statement popup
                statement_uid = self.request.params['extra']
                return_dict['distance_name'], return_dict['values'] = fuzzy_string_matcher.get_strings_for_edits(value, statement_uid)
            elif mode == '2':  # start premise
                return_dict['distance_name'], return_dict['values'] = fuzzy_string_matcher.get_strings_for_start(value, issue, False)
            elif mode == '3':  # adding reasons
                return_dict['distance_name'], return_dict['values'] = fuzzy_string_matcher.get_strings_for_reasons(value, issue)
            elif mode == '4':  # getting text
                return_dict = fuzzy_string_matcher.get_strings_for_search(value)
            elif mode == '5':  # getting public nicknames
                nickname, session_id = get_nickname_and_session(self.request, for_api, api_data)
                return_dict['distance_name'], return_dict['values'] = fuzzy_string_matcher.get_strings_for_public_nickname(value, nickname)
            else:
                logger('fuzzy_search', 'main', 'unknown mode: ' + str(mode))
                return_dict = {'error': _tn.get(_tn.internalError)}

        except KeyError as e:
            return_dict = {'error': _tn.get(_tn.internalKeyError)}
            logger('fuzzy_search', 'error', repr(e))

        if for_api:
            return return_dict
        return json.dumps(return_dict, True)

    # ajax - for additional service
    @view_config(route_name='ajax_additional_service', renderer='json')
    def additional_service(self):
        """

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('additional_service', 'def', 'main, self.request.params: ' + str(self.request.params))

        rtype = self.request.params['type']

        if rtype == "chuck":
            data = requests.get('http://api.icndb.com/jokes/random')
        else:
            data = requests.get('http://api.yomomma.info/')

        for a in data.json():
            logger('additional_service', 'main', str(a) + ': ' + str(data.json()[a]))

        return data.json()

# #######################################
# ADDITIONAL AJAX STUFF # REVIEW THINGS #
# #######################################

    # ajax - for flagging arguments
    @view_config(route_name='ajax_flag_argument_or_statement', renderer='json')
    def flag_argument_or_statement(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('flag_argument_or_statement', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            uid = self.request.params['uid']
            reason = self.request.params['reason']
            is_argument = True if str(self.request.params['is_argument']) == 'true' else False
            nickname = self.request.authenticated_userid

            db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).all()

            if not Validator.is_integer(uid):
                logger('flag_argument_or_statement', 'def', 'invalid uid', error=True)
                return_dict['error'] = _t.get(_t.internalError)
            elif not (len(db_reason) > 0 or reason == 'optimization'):
                logger('flag_argument_or_statement', 'def', 'invalid reason', error=True)
                return_dict['error'] = _t.get(_t.internalError)
            else:

                success, info, error = review_flag_helper.flag_argument(uid, reason, nickname, _t, is_argument, transaction)

                return_dict['success'] = success
                return_dict['info'] = info
                return_dict['error'] = error
        except KeyError as e:
            logger('flag_argument', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - for feedback on flagged arguments
    @view_config(route_name='ajax_review_delete_argument', renderer='json')
    def review_delete_argument(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_delete_argument', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            should_delete = True if str(self.request.params['should_delete']) == 'true' else False
            review_uid = self.request.params['review_uid']
            nickname = self.request.authenticated_userid
            if not Validator.is_integer(review_uid):
                logger('review_delete_argument', 'def', 'invalid uid', error=True)
                error = _t.get(_t.internalKeyError)
            else:
                error = review_main_helper.add_review_opinion_for_delete(nickname, should_delete, review_uid, transaction)
                send_request_for_recent_delete_review_to_socketio(nickname, main_page)
        except KeyError as e:
            logger('review_delete_argument', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        return_dict['error'] = error
        return json.dumps(return_dict, True)

    # ajax - for feedback on flagged arguments
    @view_config(route_name='ajax_review_edit_argument', renderer='json')
    def review_edit_argument(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_edit_argument', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            is_edit_okay = True if str(self.request.params['is_edit_okay']) == 'true' else False
            review_uid = self.request.params['review_uid']
            nickname = self.request.authenticated_userid
            if not Validator.is_integer(review_uid):
                logger('review_delete_argument', 'error', str(review_uid) + ' is no int')
                error = _t.get(_t.internalKeyError)
            else:
                error = review_main_helper.add_review_opinion_for_edit(nickname, is_edit_okay, review_uid, transaction)
                send_request_for_recent_edit_review_to_socketio(nickname, main_page)
        except KeyError as e:
            logger('review_delete_argument', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        return_dict['error'] = error
        return json.dumps(return_dict, True)

    # ajax - for feedback on optimization arguments
    @view_config(route_name='ajax_review_optimization_argument', renderer='json')
    def review_optimization_argument(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_optimization_argument', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            should_optimized = True if str(self.request.params['should_optimized']) == 'true' else False
            review_uid = self.request.params['review_uid']
            new_data = json.loads(self.request.params['new_data']) if 'new_data' in self.request.params else None
            nickname = self.request.authenticated_userid

            if not Validator.is_integer(review_uid):
                logger('review_delete_argument', 'error', str(review_uid) + ' is no int')
                error = _t.get(_t.internalKeyError)
            else:
                error = review_main_helper.add_review_opinion_for_optimization(nickname, should_optimized, review_uid, new_data, transaction)

                if len(error) == 0:
                    send_request_for_recent_optimization_review_to_socketio(nickname, main_page)

        except KeyError as e:
            logger('review_optimization_argument', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        return_dict['error'] = error
        return json.dumps(return_dict, True)

    # ajax - for undoing reviews
    @view_config(route_name='ajax_undo_review', renderer='json')
    def undo_review(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('undo_review', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            queue = self.request.params['queue']
            uid = self.request.params['uid']
            nickname = self.request.authenticated_userid

            if is_user_author(nickname):
                success, error = review_history_helper.revoke_old_decision(queue, uid, ui_locales, nickname, transaction)
                return_dict['success'] = success
                return_dict['error'] = error
            else:
                return_dict['info'] = _t.get(_t.justLookDontTouch)

        except KeyError as e:
            logger('undo_review', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - for canceling reviews
    @view_config(route_name='ajax_cancel_review', renderer='json')
    def cancel_review(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('cancel_review', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        try:
            queue = self.request.params['queue']
            uid = self.request.params['uid']
            nickname = self.request.authenticated_userid

            if is_user_author(nickname):
                success, error = review_history_helper.cancel_ongoing_decision(queue, uid, ui_locales, transaction)
                return_dict['success'] = success
                return_dict['error'] = error
            else:
                return_dict['info'] = _t.get(_t.justLookDontTouch)

        except KeyError as e:
            logger('undo_review', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalKeyError)

        return json.dumps(return_dict, True)

    # ajax - for undoing reviews
    @view_config(route_name='ajax_review_lock', renderer='json', require_csrf=False)
    def review_lock(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('review_lock', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        info = ''
        error = ''
        success = ''
        is_locked = False

        try:
            review_uid = self.request.params['review_uid']
            lock = True if self.request.params['lock'] == 'true' else False
            is_locked = True

            if not Validator.is_integer(review_uid):
                error = _t.get(_t.internalKeyError)
            else:
                if lock:
                    success, info, error, is_locked = review_queue_helper.lock_optimization_review(self.request.authenticated_userid, review_uid, _t, transaction)
                else:
                    review_queue_helper.unlock_optimization_review(review_uid, transaction)
                    is_locked = False

        except KeyError as e:
            logger('review_lock', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        return_dict['info'] = info
        return_dict['error'] = error
        return_dict['success'] = success
        return_dict['is_locked'] = is_locked

        return json.dumps(return_dict, True)

    # ajax - for revoking content
    @view_config(route_name='ajax_revoke_content', renderer='json', require_csrf=False)
    def revoke_content(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('ajax_revoke_content', 'def', 'main: ' + str(self.request.params))
        ui_locales = get_discussion_language(self.request)
        _t = Translator(ui_locales)
        return_dict = dict()

        info = ''
        success = ''

        try:
            uid = self.request.params['uid']
            is_argument = True if self.request.params['is_argument'] == 'true' else False

            if not Validator.is_integer(uid):
                error = _t.get(_t.internalKeyError)
            else:
                error = QueryHelper.revoke_content(uid, is_argument, self.request.authenticated_userid, _t, transaction)

        except KeyError as e:
            logger('review_lock', 'error', repr(e))
            error = _t.get(_t.internalKeyError)

        return_dict['info'] = info
        return_dict['error'] = error
        return_dict['success'] = success

        return json.dumps(return_dict, True)
