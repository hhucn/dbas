"""
Core component of DBAS.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import time

import requests
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import remember, forget
from pyramid.threadlocal import get_current_registry
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyshorteners.shorteners import Shortener
from requests.exceptions import ReadTimeout
from sqlalchemy import and_
from validate_email import validate_email

import dbas.helper.email_helper as EmailHelper
import dbas.helper.history_helper as HistoryHelper
import dbas.helper.issue_helper as IssueHelper
import dbas.helper.notification_helper as NotificationHelper
import dbas.helper.voting_helper as VotingHelper
import dbas.news_handler as NewsHandler
import dbas.password_handler as PasswordHandler
import dbas.recommender_system as RecommenderSystem
import dbas.string_matcher as FuzzyStringMatcher
import dbas.user_management as UserHandler
from .database import DBDiscussionSession
from .database.discussion_model import User, Group, Issue, Argument, Message, Settings, Language
from .helper.dictionary_helper import DictionaryHelper
from .helper.dictionary_helper_discussion import DiscussionDictHelper
from .helper.dictionary_helper_items import ItemDictHelper
from .helper.query_helper import QueryHelper
from .input_validator import Validator
from .lib import get_language, escape_string, get_text_for_statement_uid, sql_timestamp_pretty_print, get_discussion_language
from .logger import logger
from .opinion_handler import OpinionHandler
from .strings import Translator
from .url_manager import UrlManager

name = 'D-BAS'
version = '0.6.0'
full_version = version + 'a'
project_name = name + ' ' + full_version
issue_fallback = 1
mainpage = ''


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
        global mainpage
        mainpage = request.application_url
        try:
            self.issue_fallback = DBDiscussionSession.query(Issue).first().uid
        except Exception:
            self.issue_fallback = 1

    @staticmethod
    def base_layout():
        renderer = get_renderer('templates/basetemplate.pt')
        layout = renderer.implementation().macros['layout']
        return layout

    def get_nickname_and_session(self, for_api=None, api_data=None):
        """
        Given data from api, return nickname and session_id.

        :param for_api:
        :param api_data:
        :return:
        """
        nickname = api_data["nickname"] if api_data and for_api else self.request.authenticated_userid
        session_id = api_data["session_id"] if api_data and for_api else self.request.session.id
        return nickname, session_id

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
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        session_expired = True if 'session_expired' in self.request.params and self.request.params['session_expired'] == 'true' else False
        ui_locales      = get_language(self.request, get_current_registry())
        _dh             = DictionaryHelper(ui_locales, ui_locales)
        extras_dict     = _dh.prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)
        _dh.add_language_options_for_extra_dict(extras_dict)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Main',
            'project': project_name,
            'extras': extras_dict,
            'session_expired': session_expired
        }

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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('discussion_init', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('discussion_init', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id = self.get_nickname_and_session(for_api, api_data)
        session_expired = UserHandler.update_last_action(transaction, nickname)
        HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
        HistoryHelper.save_history_in_cookie(self.request, self.request.path, '')
        if session_expired:
            return self.user_logout(True)

        count_of_slugs = len(matchdict['slug']) if 'slug' in matchdict and isinstance(matchdict['slug'], ()) else 1
        if count_of_slugs > 1:
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]], True))

        if for_api and api_data:
            try:
                logged_in = api_data["nickname"]
            except KeyError:
                logged_in = None
        else:
            logged_in = self.request.authenticated_userid

        ui_locales = get_language(self.request, get_current_registry())
        if for_api:
            slug = matchdict['slug'] if 'slug' in matchdict else ''
        else:
            slug = matchdict['slug'][0] if 'slug' in matchdict and len(matchdict['slug']) > 0 else ''

        last_topic      = HistoryHelper.get_saved_issue(nickname)
        if len(slug) == 0 and last_topic != 0:
            issue      = last_topic
        else:
            issue      = IssueHelper.get_id_of_slug(slug, self.request, True)

        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, for_api)
        item_dict       = ItemDictHelper(disc_ui_locales, issue, mainpage, for_api).prepare_item_dict_for_start(logged_in)
        HistoryHelper.save_issue_uid(transaction, issue, nickname)

        discussion_dict = DiscussionDictHelper(disc_ui_locales, session_id, nickname, mainpage=mainpage, slug=slug)\
            .prepare_discussion_dict_for_start()
        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, True, True, True,
                                                                                            False, True, nickname,
                                                                                            application_url=mainpage,
                                                                                            for_api=for_api,
                                                                                            request=self.request)

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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('discussion_attitude', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('discussion_attitude', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id = self.get_nickname_and_session(for_api, api_data)
        session_expired = UserHandler.update_last_action(transaction, nickname)
        history         = params['history'] if 'history' in params else ''
        HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
        HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)
        if session_expired:
            return self.user_logout(True)

        ui_locales      = get_language(self.request, get_current_registry())
        slug            = matchdict['slug'] if 'slug' in matchdict else ''
        statement_id    = matchdict['statement_id'][0] if 'statement_id' in matchdict else ''
        issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)

        if not Validator.check_for_integer(statement_id, True) \
            or not Validator.check_belonging_of_statement(issue, statement_id) \
            or not Validator.is_position(statement_id):
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]], True))

        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, for_api)

        discussion_dict = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)\
            .prepare_discussion_dict_for_attitude(statement_id)
        if not discussion_dict:
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_id]))

        item_dict       = ItemDictHelper(disc_ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)\
            .prepare_item_dict_for_attitude(statement_id)
        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(issue_dict['slug'], False,
                                                                                            False, True, False, True,
                                                                                            nickname,
                                                                                            application_url=mainpage,
                                                                                            for_api=for_api,
                                                                                            request=self.request)
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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('discussion_justify', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('discussion_justify', 'def', 'main, self.request.params: ' + str(params))

        nickname, session_id = self.get_nickname_and_session(for_api, api_data)
        history              = params['history'] if 'history' in params else ''
        HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
        HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)

        _uh = UserHandler
        session_expired = _uh.update_last_action(transaction, nickname)
        if session_expired:
            return self.user_logout(True)

        logged_in = _uh.is_user_logged_in(nickname)

        ui_locales = get_language(self.request, get_current_registry())

        slug                = matchdict['slug'] if 'slug' in matchdict else ''
        statement_or_arg_id = matchdict['statement_or_arg_id'] if 'statement_or_arg_id' in matchdict else ''
        mode                = matchdict['mode'] if 'mode' in matchdict else ''
        supportive          = mode == 't' or mode == 'd'  # supportive = t or dont know mode
        relation            = matchdict['relation'][0] if len(matchdict['relation']) > 0 else ''

        if not Validator.check_for_integer(statement_or_arg_id, True):
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]], True))

        issue               = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
        disc_ui_locales     = get_discussion_language(self.request, issue)
        issue_dict          = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, for_api)
        _ddh                = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)
        _idh                = ItemDictHelper(disc_ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)
        _dh                 = DictionaryHelper(ui_locales, disc_ui_locales)

        if [c for c in ('t', 'f') if c in mode] and relation == '':
            logger('discussion_justify', 'def', 'justify statement')
            # justifying statement
            if not get_text_for_statement_uid(statement_or_arg_id)\
                                or not Validator.check_belonging_of_statement(issue, statement_or_arg_id):
                return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_or_arg_id]))

            VotingHelper.add_vote_for_statement(statement_or_arg_id, nickname, supportive, transaction)

            item_dict       = _idh.prepare_item_dict_for_justify_statement(statement_or_arg_id, nickname, supportive)
            discussion_dict = _ddh.prepare_discussion_dict_for_justify_statement(statement_or_arg_id, mainpage, slug, supportive, len(item_dict), nickname)
            extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, False, True, nickname, mode == 't',
                                                      application_url=mainpage, for_api=for_api, request=self.request)
            # is the discussion at the end?
            if len(item_dict) == 0 or len(item_dict) == 1 and logged_in:
                _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify=True,
                                            current_premise=get_text_for_statement_uid(statement_or_arg_id),
                                            supportive=supportive)

        elif 'd' in mode and relation == '':
            logger('discussion_justify', 'def', 'dont know statement')
            if not Validator.check_belonging_of_argument(issue, statement_or_arg_id) and \
                    not Validator.check_belonging_of_statement(issue, statement_or_arg_id):
                return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_or_arg_id]))

            # dont know
            argument_uid    = RecommenderSystem.get_argument_by_conclusion(statement_or_arg_id, supportive)
            discussion_dict = _ddh.prepare_discussion_dict_for_dont_know_reaction(argument_uid)
            item_dict       = _idh.prepare_item_dict_for_dont_know_reaction(argument_uid, supportive)
            extras_dict     = _dh.prepare_extras_dict(slug, False, False, True, True, True, nickname,
                                                      argument_id=argument_uid, application_url=mainpage, for_api=for_api,
                                                      request=self.request)
            # is the discussion at the end?
            if len(item_dict) == 0:
                _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_dont_know=True,
                                            current_premise=get_text_for_statement_uid(statement_or_arg_id))

        elif [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid') if c in relation]:
            logger('discussion_justify', 'def', 'justify argument')
            if not Validator.check_belonging_of_argument(issue, statement_or_arg_id):
                return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, statement_or_arg_id]))

            # justifying argument
            # is_attack = True if [c for c in ('undermine', 'rebut', 'undercut') if c in relation] else False
            item_dict       = _idh.prepare_item_dict_for_justify_argument(statement_or_arg_id, relation, logged_in)
            discussion_dict = _ddh.prepare_discussion_dict_for_justify_argument(statement_or_arg_id, supportive, relation)
            extras_dict     = _dh.prepare_extras_dict(slug, True, True, True, True, True, nickname,
                                                      argument_id=statement_or_arg_id, application_url=mainpage, for_api=for_api,
                                                      request=self.request)
            # is the discussion at the end?
            if not logged_in and len(item_dict) == 1 or logged_in and len(item_dict) == 1:
                _dh.add_discussion_end_text(discussion_dict, extras_dict, nickname, at_justify_argumentation=True)
        else:
            logger('discussion_justify', 'def', '404')
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([slug, 'justify', statement_or_arg_id, mode, relation]))

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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('discussion_reaction', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('discussion_reaction', 'def', 'main, self.request.params: ' + str(params))

        slug            = matchdict['slug'] if 'slug' in matchdict else ''
        arg_id_user     = matchdict['arg_id_user'] if 'arg_id_user' in matchdict else ''
        attack          = matchdict['mode'] if 'mode' in matchdict else ''
        arg_id_sys      = matchdict['arg_id_sys'] if 'arg_id_sys' in matchdict else ''
        tmp_argument    = DBDiscussionSession.query(Argument).filter_by(uid=arg_id_user).first()
        history         = params['history'] if 'history' in params else ''
        issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)

        valid_reaction = Validator.check_reaction(arg_id_user, arg_id_sys, attack)
        if not tmp_argument or not valid_reaction\
                or not valid_reaction and not Validator.check_belonging_of_argument(issue, arg_id_user)\
                or not valid_reaction and not Validator.check_belonging_of_argument(issue, arg_id_sys):
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]]))

        supportive           = tmp_argument.is_supportive
        nickname, session_id = self.get_nickname_and_session(for_api, api_data)
        session_expired      = UserHandler.update_last_action(transaction, nickname)
        HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
        HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)
        if session_expired:
            return self.user_logout(True)

        # sanity check
        if not [c for c in ('undermine', 'rebut', 'undercut', 'support', 'overbid', 'end') if c in attack]:
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]], True))

        # set votings
        VotingHelper.add_vote_for_argument(arg_id_user, nickname, transaction)

        ui_locales      = get_language(self.request, get_current_registry())
        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, for_api)

        _ddh            = DiscussionDictHelper(disc_ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)
        discussion_dict = _ddh.prepare_discussion_dict_for_argumentation(arg_id_user, supportive, arg_id_sys, attack, history)
        item_dict       = ItemDictHelper(disc_ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)\
            .prepare_item_dict_for_reaction(arg_id_sys, arg_id_user, supportive, attack)
        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, False, True, True,
                                                                                            True, nickname,
                                                                                            argument_id=arg_id_sys,
                                                                                            application_url=mainpage,
                                                                                            for_api=for_api,
                                                                                            request=self.request)

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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('discussion_finish', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('discussion_finish', 'def', 'main, self.request.params: ' + str(params))
        ui_locales      = get_language(self.request, get_current_registry())
        nickname        = self.request.authenticated_userid
        session_expired = UserHandler.update_last_action(transaction, nickname)
        HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(nickname, self.request)
        summary_dict = UserHandler.get_summary_of_today(nickname)

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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('discussion_choose', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('discussion_choose', 'def', 'main, self.request.params: ' + str(params))

        slug            = matchdict['slug'] if 'slug' in matchdict else ''
        is_argument     = matchdict['is_argument'] if 'is_argument' in matchdict else ''
        is_supportive   = matchdict['supportive'] if 'supportive' in matchdict else ''
        uid             = matchdict['id'] if 'id' in matchdict else ''
        pgroup_ids      = matchdict['pgroup_ids'] if 'id' in matchdict else ''
        nickname, session_id = self.get_nickname_and_session(for_api, api_data)
        history         = params['history'] if 'history' in params else ''

        is_argument = True if is_argument is 't' else False
        is_supportive = True if is_supportive is 't' else False

        ui_locales      = get_language(self.request, get_current_registry())
        issue           = IssueHelper.get_id_of_slug(slug, self.request, True) if len(slug) > 0 else IssueHelper.get_issue_id(self.request)
        disc_ui_locales = get_discussion_language(self.request, issue)
        issue_dict      = IssueHelper.prepare_json_of_issue(issue, mainpage, disc_ui_locales, for_api)

        if not Validator.check_belonging_of_premisegroups(issue, pgroup_ids):
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]]))

        session_expired = UserHandler.update_last_action(transaction, nickname)
        HistoryHelper.save_path_in_database(nickname, self.request.path, transaction)
        HistoryHelper.save_history_in_cookie(self.request, self.request.path, history)
        if session_expired:
            return self.user_logout(True)

        discussion_dict = DiscussionDictHelper(ui_locales, session_id, nickname, history, mainpage=mainpage, slug=slug)\
            .prepare_discussion_dict_for_choosing(uid, is_argument, is_supportive)
        item_dict       = ItemDictHelper(disc_ui_locales, issue, mainpage, for_api, path=self.request.path, history=history)\
            .prepare_item_dict_for_choosing(uid, pgroup_ids, is_argument, is_supportive)
        if not item_dict:
            return HTTPFound(location=UrlManager(mainpage, for_api=for_api).get_404([self.request.path[1:]]))

        extras_dict     = DictionaryHelper(ui_locales, disc_ui_locales).prepare_extras_dict(slug, False, False, True,
                                                                                            True, True, nickname,
                                                                                            application_url=mainpage,
                                                                                            for_api=for_api,
                                                                                            request=self.request)

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

    # contact page
    @view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody', require_csrf=False)
    def main_contact(self):
        """
        View configuration for the contact view.

        :return: dictionary with title and project username as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_contact', 'def', 'main, self.request.params: ' + str(self.request.params))
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
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

        try:
            spamanswer = int(spamanswer) if len(spamanswer) > 0 else '#'
        except ValueError and TypeError:
            spamanswer = '#'
        key = 'contact-antispamanswer'
        antispamanswer = self.request.session[key] if key in self.request.session else ''
        spamsolution = int(antispamanswer) if len(antispamanswer) > 0 else '*#*'

        if 'form.contact.submitted' in self.request.params:
            _t = Translator(ui_locales)

            logger('main_contact', 'form.contact.submitted', 'validating email')
            is_mail_valid = validate_email(email, check_mx=True)

            # check for empty username
            if not username:
                logger('main_contact', 'form.contact.submitted', 'username empty')
                contact_error = True
                message = _t.get(_t.emptyName)

            # check for non valid mail
            elif not is_mail_valid:
                logger('main_contact', 'form.contact.submitted', 'mail is not valid')
                contact_error = True
                message = _t.get(_t.invalidEmail)

            # check for empty content
            elif not content:
                logger('main_contact', 'form.contact.submitted', 'content is empty')
                contact_error = True
                message = _t.get(_t.emtpyContent)

            # check for empty spam
            elif str(spamanswer) != str(spamsolution):
                logger('main_contact', 'form.contact.submitted', 'empty or wrong anti-spam answer' + ', given answer ' +
                       str(spamanswer) + ', right answer ' + str(antispamanswer))
                contact_error = True
                message = _t.get(_t.maliciousAntiSpam)

            else:
                subject = _t.get(_t.contact) + ' D-BAS'
                body = _t.get(_t.name) + ': ' + username + '\n'\
                       + _t.get(_t.mail) + ': ' + email + '\n'\
                       + _t.get(_t.phone) + ': ' + phone + '\n'\
                       + _t.get(_t.message) + ':\n' + content
                EmailHelper.send_mail(self.request, subject, body, 'dbas.hhu@gmail.com', ui_locales)
                body = '* ' + _t.get(_t.thisIsACopyOfMail).upper() + ' *\n\n' + body
                subject = '[D-BAS INFO] ' + subject
                send_message, message = EmailHelper.send_mail(self.request, subject, body, email, ui_locales)
                contact_error = not send_message

        spamquestion, answer = UserHandler.get_random_anti_spam_question(ui_locales)
        self.request.session[key] = answer

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)
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
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        old_pw      = ''
        new_pw      = ''
        confirm_pw  = ''
        message     = ''
        error       = False
        success     = False
        group       = '-'

        db_user     = DBDiscussionSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).join(Group).first()
        db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first() if db_user else None
        db_language = DBDiscussionSession.query(Language).filter_by(uid=db_settings.lang_uid).first() if db_settings else None

        _uh         = UserHandler
        if db_user:
            edits       = _uh.get_count_of_statements_of_user(db_user, True)
            statements  = _uh.get_count_of_statements_of_user(db_user, False)
            arg_vote, stat_vote = _uh.get_count_of_votes_of_user(db_user)
            public_nick = db_user.public_nickname
            db_group    = DBDiscussionSession.query(Group).filter_by(uid=db_user.group_uid).first()
            group       = db_group.name if db_group else '-'
        else:
            edits       = 0
            statements  = 0
            arg_vote    = 0
            stat_vote   = 0
            public_nick = str(self.request.authenticated_userid)

        if db_user and 'form.passwordchange.submitted' in self.request.params:
            old_pw = escape_string(self.request.params['passwordold'])
            new_pw = escape_string(self.request.params['password'])
            confirm_pw = escape_string(self.request.params['passwordconfirm'])

            message, error, success = _uh.change_password(transaction, db_user, old_pw, new_pw, confirm_pw, ui_locales)

        # get gravater profile picture
        gravatar_public_url = _uh.get_public_profile_picture(db_user)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)
        settings_dict = {
            'passwordold': '' if success else old_pw,
            'password': '' if success else new_pw,
            'passwordconfirm': '' if success else confirm_pw,
            'change_error': error,
            'change_success': success,
            'message': message,
            'db_firstname': db_user.firstname if db_user else 'unknown',
            'db_surname': db_user.surname if db_user else 'unknown',
            'db_nickname': db_user.nickname if db_user else 'unknown',
            'db_public_nickname': public_nick,
            'db_mail': db_user.email if db_user else 'unknown',
            'db_group': group,
            'avatar_public_url': gravatar_public_url,
            'edits_done': edits,
            'statemens_posted': statements,
            'discussion_arg_votes': arg_vote,
            'discussion_stat_votes': stat_vote,
            'send_mails': db_settings.should_send_mails if db_settings else False,
            'send_notifications': db_settings.should_send_notifications if db_settings else False,
            'public_nick': db_settings.should_show_public_nickname if db_settings else True,
            'title_mails': _tn.get(_tn.mailSettingsTitle),
            'title_notifications': _tn.get(_tn.notificationSettingsTitle),
            'title_public_nick': _tn.get(_tn.publicNickTitle),
            'title_prefered_lang': _tn.get(_tn.preferedLangTitle),
            'public_page_url': mainpage + '/user/' + public_nick,
            'on': _tn.get(_tn.on),
            'off': _tn.get(_tn.off),
            'current_lang': db_language.name if db_language else '?',
            'current_ui_locales': db_language.ui_locales if db_language else '?'
        }

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
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)

        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request, append_notifications=True)

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
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())
        is_author = UserHandler.is_user_author(self.request.authenticated_userid)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)

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
        matchdict = self.request.matchdict
        params = self.request.params
        logger('main_user', 'def', 'main, self.request.matchdict: ' + str(matchdict))
        logger('main_user', 'def', 'main, self.request.params: ' + str(params))

        nickname = matchdict['nickname'] if 'nickname' in matchdict else ''
        nickname = nickname.replace('%20', ' ')
        logger('main_user', 'def', 'nickname: ' + str(nickname))
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        db_public_user = DBDiscussionSession.query(User).filter_by(public_nickname=nickname).first()

        db_settings = None
        current_user = None

        if db_user:
            db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
        elif db_public_user:
            db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_public_user.uid).first()

        if db_settings:
            if db_settings.should_show_public_nickname and db_user:
                current_user = db_user
            elif not db_settings.should_show_public_nickname and db_public_user:
                current_user = db_public_user

        if current_user is None:
            return HTTPFound(location=UrlManager(mainpage).get_404([self.request.path[1:]]))

        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        if session_expired:
            return self.user_logout(True)

        ui_locales = get_language(self.request, get_current_registry())
        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)

        user_dict = UserHandler.get_information_of(current_user, ui_locales)

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
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)
        import pkg_resources
        extras_dict.update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.imprint),
            'project': project_name,
            'extras': extras_dict
        }

    # review
    @view_config(route_name='main_review', renderer='templates/review.pt', permission='everybody')
    def main_review(self):
        """
        View configuration for the imprint.

        :return: dictionary with title and project name as well as a value, weather the user is logged in
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('main_review', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        session_expired = UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        HistoryHelper.save_path_in_database(self.request.authenticated_userid, self.request.path, transaction)
        _tn = Translator(ui_locales)
        if session_expired:
            return self.user_logout(True)

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': _tn.get(_tn.review),
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
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('notfound', 'def', 'main in ' + str(self.request.method) + '-request' +
               ', path: ' + self.request.path +
               ', view name: ' + self.request.view_name +
               ', params: ' + str(self.request.params))
        path = self.request.path
        if path.startswith('/404/'):
            path = path[4:]

        param_error = True if 'param_error' in self.request.params and self.request.params['param_error'] == 'true' else False

        self.request.response.status = 404
        ui_locales = get_language(self.request, get_current_registry())

        extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(self.request.authenticated_userid, self.request)

        # return HTTPFound(location=UrlManager(mainpage, for_api=False).get_404([self.request.path[1:]]))

        return {
            'layout': self.base_layout(),
            'language': str(ui_locales),
            'title': 'Error',
            'project': project_name,
            'page_notfound_viewname': path,
            'extras': extras_dict,
            'param_error': param_error
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
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_user_history', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_list = HistoryHelper.get_history_from_database(self.request.authenticated_userid, ui_locales)
        return json.dumps(return_list, True)

    # ajax - getting all text edits
    @view_config(route_name='ajax_get_all_posted_statements', renderer='json')
    def get_all_posted_statements(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_posted_statements', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_array, tmp = UserHandler.get_textversions_of_user(self.request.authenticated_userid, ui_locales)
        return json.dumps(return_array, True)

    # ajax - getting all text edits
    @view_config(route_name='ajax_get_all_edits', renderer='json')
    def get_all_edits(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_edits', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        tmp, return_array = UserHandler.get_textversions_of_user(self.request.authenticated_userid, ui_locales)
        return json.dumps(return_array, True)

    # ajax - getting all votes for arguments
    @view_config(route_name='ajax_get_all_argument_votes', renderer='json')
    def get_all_argument_votes(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_argument_votes', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_array = UserHandler.get_votes_of_user(self.request.authenticated_userid, True, ui_locales)
        return json.dumps(return_array, True)

    # ajax - getting all votes for statements
    @view_config(route_name='ajax_get_all_statement_votes', renderer='json')
    def get_all_statement_votes(self):
        """

        :return:
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('get_all_statement_votes', 'def', 'main')
        ui_locales = get_language(self.request, get_current_registry())
        return_array = UserHandler.get_votes_of_user(self.request.authenticated_userid, False, ui_locales)
        return json.dumps(return_array, True)

    # ajax - deleting complete history of the user
    @view_config(route_name='ajax_delete_user_history', renderer='json')
    def delete_user_history(self):
        """
        Request the complete user history.

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        logger('delete_user_history', 'def', 'main')
        HistoryHelper.delete_history_in_database(self.request.authenticated_userid, transaction)
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
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        logger('delete_statistics', 'def', 'main')

        return_dict = dict()
        return_dict['removed_data'] = 'true' if VotingHelper.clear_votes_of_user(transaction, self.request.authenticated_userid) else 'false'

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

            db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

            # check for user and password validations
            if not db_user:
                logger('user_login', 'no user', 'user \'' + nickname + '\' does not exists')
                error = _tn.get(_tn.userPasswordNotMatch)
            elif not db_user.validate_password(password):
                logger('user_login', 'password not valid', 'wrong password')
                error = _tn.get(_tn.userPasswordNotMatch)
            else:
                logger('user_login', 'login', 'login successful / keep_login: ' + str(keep_login))
                db_user.should_hold_the_login(keep_login)
                headers = remember(self.request, nickname)

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
            error = _tn.get(_tn.internalError)
            logger('user_login', 'error', repr(e))

        return_dict = {'error': error}

        return return_dict  # json.dumps(return_dict, True)

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
                location=mainpage + '?session_expired=true',
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
            params          = self.request.params
            firstname       = escape_string(params['firstname'])
            lastname        = escape_string(params['lastname'])
            nickname        = escape_string(params['nickname'])
            email           = escape_string(params['email'])
            gender          = escape_string(params['gender'])
            password        = escape_string(params['password'])
            passwordconfirm = escape_string(params['passwordconfirm'])
            spamanswer      = escape_string(params['spamanswer'])

            # database queries mail verification
            db_nick1 = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
            db_nick2 = DBDiscussionSession.query(User).filter_by(public_nickname=nickname).first()
            db_mail = DBDiscussionSession.query(User).filter_by(email=email).first()
            is_mail_valid = validate_email(email, check_mx=True)

            # are the password equal?
            if not password == passwordconfirm:
                logger('user_registration', 'main', 'Passwords are not equal')
                info = _t.get(_t.pwdNotEqual)
            # is the nick already taken?
            elif db_nick1 or db_nick2:
                logger('user_registration', 'main', 'Nickname \'' + nickname + '\' is taken')
                info = _t.get(_t.nickIsTaken)
            # is the email already taken?
            elif db_mail:
                logger('user_registration', 'main', 'E-Mail \'' + email + '\' is taken')
                info = _t.get(_t.mailIsTaken)
            # is the email valid?
            elif not is_mail_valid:
                logger('user_registration', 'main', 'E-Mail \'' + email + '\' is not valid')
                info = _t.get(_t.mailNotValid)
            # is anti-spam correct?
            elif str(spamanswer) != str(self.request.session['antispamanswer']):
                logger('user_registration', 'main', 'Anti-Spam answer \'' + str(spamanswer) + '\' is not equal ' + str(self.request.session['antispamanswer']))
                info = _t.get(_t.maliciousAntiSpam)
            else:
                # getting the authors group
                db_group = DBDiscussionSession.query(Group).filter_by(name="authors").first()

                # does the group exists?
                if not db_group:
                    info = _t.get(_t.errorTryLateOrContant)
                    logger('user_registration', 'main', 'Error occured')
                else:
                    # creating a new user with hashed password
                    logger('user_registration', 'main', 'Adding user')
                    hashed_password = PasswordHandler.get_hashed_password(password)
                    newuser = User(firstname=firstname,
                                   surname=lastname,
                                   email=email,
                                   nickname=nickname,
                                   password=hashed_password,
                                   gender=gender,
                                   group=db_group.uid)
                    DBDiscussionSession.add(newuser)
                    transaction.commit()
                    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
                    settings = Settings(author_uid=db_user.uid, send_mails=True, send_notifications=True, should_show_public_nickname=True)
                    DBDiscussionSession.add(settings)
                    transaction.commit()

                    # sanity check, whether the user exists
                    checknewuser = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
                    if checknewuser:
                        logger('user_registration', 'main', 'New data was added with uid ' + str(checknewuser.uid))
                        success = _t.get(_t.accountWasAdded)

                        # sending an email
                        subject = _t.get(_t.accountRegistration)
                        body = _t.get(_t.accountWasRegistered)
                        EmailHelper.send_mail(self.request, subject, body, email, ui_locales)
                        NotificationHelper.send_welcome_notification(transaction, checknewuser.uid)

                    else:
                        logger('user_registration', 'main', 'New data was not added')
                        info = _t.get(_t.accoutErrorTryLateOrContant)

        except KeyError as e:
            logger('user_registration', 'error', repr(e))
            error = _t.get(_t.internalError)

        # get anti-spam-question
        spamquestion, answer = UserHandler.get_random_anti_spam_question(ui_locales)
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
        error = ''
        info = ''
        return_dict = dict()
        ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
        if not ui_locales:
            ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        try:
            email = escape_string(self.request.params['email'])
            db_user = DBDiscussionSession.query(User).filter_by(email=email).first()

            # does the user exists?
            if db_user:
                # get password and hashed password
                pwd = PasswordHandler.get_rnd_passwd()
                hashedpwd = PasswordHandler.get_hashed_password(pwd)

                # set the hashed one
                db_user.password = hashedpwd
                DBDiscussionSession.add(db_user)
                transaction.commit()

                db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
                db_language = DBDiscussionSession.query(Language).filter_by(uid=db_settings.lang_uid).first()

                body = _t.get(_t.nicknameIs) + db_user.nickname + '\n'
                body += _t.get(_t.newPwdIs) + pwd
                subject = _t.get(_t.dbasPwdRequest)
                reg_success, message = EmailHelper.send_mail(self.request, subject, body, email, db_language.ui_locales)

                if reg_success:
                    success = message
                else:
                    error = message
            else:
                logger('user_password_request', 'form.passwordrequest.submitted', 'Mail unknown')
                info = _t.get(_t.emailUnknown)

        except KeyError as e:
            logger('user_password_request', 'error', repr(e))
            error = _t.get(_t.internalError)

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
                        UserHandler.refresh_public_nickname(db_user)
                    public_nick = db_user.public_nickname
                else:
                    error = _tn.get(_tn.keyword)

                transaction.commit()
                public_page_url = mainpage + '/user/' + public_nick
                gravatar_url = UserHandler.get_public_profile_picture(db_user, 80)
            else:
                error = _tn.get(_tn.checkNickname)
        except KeyError as e:
            error = _tn.get(_tn.internalError)
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
            error = _tn.get(_tn.internalError)
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
            db_recipient = DBDiscussionSession.query(User).filter_by(public_nickname=recipient).first()
            if len(title) < 5 or len(text) < 5:
                error = _tn.get(_tn.empty_notification_input) + ' (' + _tn.get(_tn.minLength) + ': 5)'
            elif not db_recipient or recipient == 'admin' or recipient == 'anonymous':
                error = _tn.get(_tn.recipientNotFound)
            else:
                db_author = DBDiscussionSession.query(User).filter_by(nickname=self.request.authenticated_userid).first()
                if not db_author:
                    error = _tn.get(_tn.notLoggedIn)
                else:
                    db_notification = NotificationHelper.send_notification(db_author, db_recipient, title, text, transaction)
                    uid = db_notification.uid
                    ts = sql_timestamp_pretty_print(db_notification.timestamp, ui_locales)
                    gravatar = UserHandler.get_public_profile_picture(db_recipient, 20)

        except KeyError:
            error = _tn.get(_tn.internalError)

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
                issue       = IssueHelper.get_issue_id(self.request)
                slug        = DBDiscussionSession.query(Issue).filter_by(uid=issue).first().get_slug()

            # escaping will be done in QueryHelper().set_statement(...)
            UserHandler.update_last_action(transaction, nickname)
            new_statement = QueryHelper.insert_as_statements(transaction, statement, nickname, issue, is_start=True)
            if new_statement == -1:
                return_dict['error'] = _tn.get(_tn.notInsertedErrorBecauseEmpty) + ' (' + _tn.get(_tn.minLength) + ': 10)'
            else:
                url = UrlManager(mainpage, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
                return_dict['url'] = url
                return_dict['statement_uids'].append(new_statement[0].uid)
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
                issue           = IssueHelper.get_issue_id(self.request)
                premisegroups   = json.loads(self.request.params['premisegroups'])
                conclusion_id   = self.request.params['conclusion_id']
                supportive      = True if self.request.params['supportive'].lower() == 'true' else False

            # escaping will be done in QueryHelper().set_statement(...)
            UserHandler.update_last_action(transaction, nickname)

            _qh = QueryHelper
            url, statement_uids, error = _qh.process_input_of_start_premises_and_receive_url(self.request, transaction,
                                                                                             premisegroups, conclusion_id,
                                                                                             supportive, issue, nickname,
                                                                                             for_api, mainpage, lang)

            return_dict['error'] = error
            return_dict['statement_uids'] = statement_uids

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
                issue = IssueHelper.get_issue_id(self.request)
                arg_uid = self.request.params['arg_uid']
                attack_type = self.request.params['attack_type']

            # escaping will be done in QueryHelper().set_statement(...)
            _qh = QueryHelper
            url, statement_uids, error = _qh.process_input_of_premises_for_arguments_and_receive_url(self.request,
                                                                                                     transaction, arg_uid,
                                                                                                     attack_type,
                                                                                                     premisegroups, issue,
                                                                                                     nickname, for_api,
                                                                                                     mainpage, lang)
            UserHandler.update_last_action(transaction, nickname)

            return_dict['error'] = error
            return_dict['statement_uids'] = statement_uids

            if url == -1:
                return json.dumps(return_dict, True)

            return_dict['url'] = url

        except KeyError as e:
            logger('set_new_premises_for_argument', 'error', repr(e))
            return_dict['error']  = _tn.get(_tn.notInsertedErrorBecauseInternal)

        logger('set_new_premises_for_argument', 'def', 'returning ' + str(return_dict))
        return json.dumps(return_dict, True)

    # ajax - set new textvalue for a statement
    @view_config(route_name='ajax_set_correcture_of_statement', renderer='json')
    def set_correcture_of_statement(self):
        """
        Sets a new textvalue for a statement

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('set_correcture_of_statement', 'def', 'main, self.request.params: ' + str(self.request.params))
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        _tn = Translator(get_language(self.request, get_current_registry()))

        try:
            uid = self.request.params['uid']
            url = self.request.params['url']
            corrected_text = escape_string(self.request.params['text'])
            return_dict = QueryHelper.correct_statement(transaction, self.request.authenticated_userid, uid,
                                                        corrected_text, url, self.request)
            if return_dict == -1:
                return_dict = dict()
                return_dict['error'] = _tn.get(_tn.noCorrectionsSet)

            return_dict['error'] = ''
        except KeyError as e:
            return_dict = dict()
            return_dict['error'] = ''
            logger('set_correcture_of_statement', 'error', repr(e))

        return json.dumps(return_dict, True)

    # ajax - set notification as read
    @view_config(route_name='ajax_notification_read', renderer='json')
    def set_notification_read(self):
        """
        Set notification as read

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        logger('set_notification_read', 'def', 'main ' + str(self.request.params))
        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        try:
            DBDiscussionSession.query(Message).filter_by(uid=self.request.params['id']).first().set_read(True)
            transaction.commit()
            return_dict['unread_messages'] = NotificationHelper.count_of_new_notifications(self.request.authenticated_userid)
            return_dict['error'] = ''
        except KeyError as e:
            logger('set_message_read', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalError)

        return json.dumps(return_dict, True)

    # ajax - deletes a notification
    @view_config(route_name='ajax_notification_delete', renderer='json')
    def set_notification_delete(self):
        """
        Request the removal of a notification

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        logger('set_notification_delete', 'def', 'main ' + str(self.request.params))
        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())
        _t = Translator(ui_locales)

        try:
            DBDiscussionSession.query(Message).filter_by(uid=self.request.params['id']).delete()
            transaction.commit()
            return_dict['unread_messages'] = NotificationHelper.count_of_new_notifications(self.request.authenticated_userid)
            return_dict['total_in_messages'] = str(len(NotificationHelper.get_box_for(self.request.authenticated_userid, ui_locales, mainpage, True)))
            return_dict['total_out_messages'] = str(len(NotificationHelper.get_box_for(self.request.authenticated_userid, ui_locales, mainpage, False)))
            return_dict['error'] = ''
            return_dict['success'] = _t.get(_t.messageDeleted)
        except KeyError as e:
            logger('set_message_read', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalError)
            return_dict['success'] = ''

        return json.dumps(return_dict, True)

    # ajax - set new issue
    @view_config(route_name='ajax_set_new_issue', renderer='json')
    def set_new_issue(self):
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        logger('set_new_issue', 'def', 'main ' + str(self.request.params))
        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())
        _tn = Translator(ui_locales)

        try:
            info = escape_string(self.request.params['info'])
            title = escape_string(self.request.params['title'])
            lang = escape_string(self.request.params['lang'])
            was_set, error = IssueHelper.set_issue(info, title, lang, self.request.authenticated_userid, transaction, ui_locales)
            if was_set:
                db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
                                                                        Issue.info == info)).first()
                return_dict['issue'] = IssueHelper.get_issue_dict_for(db_issue, mainpage, False, 0, ui_locales)
        except KeyError as e:
            logger('set_new_issue', 'error', repr(e))
            error = _tn.get(_tn.notInsertedErrorBecauseInternal)

        return_dict['error'] = error
        return json.dumps(return_dict, True)

# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################

    # ajax - getting changelog of a statement
    @view_config(route_name='ajax_get_logfile_for_statement', renderer='json')
    def get_logfile_for_statement(self):
        """
        Returns the changelog of a statement

        :return: json-dict()
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('get_logfile_for_statement', 'def', 'main, self.request.params: ' + str(self.request.params))
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

        return_dict = dict()
        ui_locales = get_language(self.request, get_current_registry())

        try:
            uid = self.request.params['uid']
            issue = self.request.params['issue']
            ui_locales = get_discussion_language(self.request, issue)
            return_dict = QueryHelper.get_logfile_for_statement(uid, ui_locales, mainpage)
            return_dict['error'] = ''
        except KeyError as e:
            logger('get_logfile_for_statement', 'error', repr(e))
            _tn = Translator(ui_locales)
            return_dict['error'] = _tn.get(_tn.noCorrections)

        # return_dict = QueryHelper().get_logfile_for_premisegroup(uid)

        return json.dumps(return_dict, True)

    # ajax - for shorten url
    @view_config(route_name='ajax_get_shortened_url', renderer='json')
    def get_shortened_url(self):
        """
        Shortens url with the help of a python lib

        :return: dictionary with shortend url
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)

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
            return_dict['error'] = _tn.get(_tn.internalError)
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
        return_dict = NewsHandler.get_news(get_language(self.request, get_current_registry()))
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
            if not Validator.check_for_integer(uid):
                return_dict['error'] = _t.get(_t.internalError)
            else:
                return_dict = QueryHelper.get_infos_about_argument(uid, ui_locales, mainpage)
                return_dict['error'] = ''
        except KeyError as e:
            logger('get_infos_about_argument', 'error', repr(e))
            return_dict['error'] = _t.get(_t.internalError)

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
            is_argument = params['is_argument'] == 'true' if 'is_argument' in params else False
            is_attitude = params['is_attitude'] == 'true' if 'is_attitude' in params else False
            is_reaction = params['is_reaction'] == 'true' if 'is_reaction' in params else False
            is_position = params['is_position'] == 'true' if 'is_position' in params else False
            is_supporti = params['is_supporti'] if 'is_supporti' in params else None

            _op = OpinionHandler(ui_locales, nickname, mainpage)
            if is_argument:
                if not is_reaction:
                    return_dict = _op.get_user_with_same_opinion_for_argument(uids)
                else:
                    uids = json.loads(uids)
                    return_dict = _op.get_user_and_opinions_for_argument(uids)
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
            return_dict['error'] = _tn.get(_tn.internalError)

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
            return_dict = UserHandler.get_public_information_data(nickname, ui_locales)

        except KeyError as e:
            logger('get_users_with_same_opinion', 'error', repr(e))
            return_dict['error'] = _tn.get(_tn.internalError)

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
        UserHandler.update_last_action(transaction, self.request.authenticated_userid)
        logger('switch_language', 'def', 'main, self.request.params: ' + str(self.request.params))

        return_dict = dict()
        try:
            ui_locales = self.request.params['lang'] if 'lang' in self.request.params else None
            if not ui_locales:
                ui_locales = get_language(self.request, get_current_registry())
            self.request.response.set_cookie('_LOCALE_', str(ui_locales))
        except KeyError as e:
            logger('swich_language', 'error', repr(e))

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
            return_dict = NewsHandler.set_news(transaction, title, text, self.request.authenticated_userid, get_language(self.request, get_current_registry()))
            return_dict['error'] = ''
        except KeyError as e:
            return_dict = dict()
            logger('send_news', 'error', repr(e))
            _tn = Translator(get_language(self.request, get_current_registry()))
            return_dict['error'] = _tn.get(_tn.internalError)

        return json.dumps(return_dict, True)

    # ajax - for fuzzy search
    @view_config(route_name='ajax_fuzzy_search', renderer='json')
    def fuzzy_search(self, for_api=False, api_data=None):
        """
        ajax interface for fuzzy string search

        :param for_api: boolean
        :return: json-set with all matched strings
        """
        logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
        logger('fuzzy_search', 'def', 'main, for_api: ' + str(for_api) + ', self.request.params: ' + str(self.request.params))

        _tn = Translator(get_language(self.request, get_current_registry()))

        try:
            value = api_data["value"] if for_api else self.request.params['value']
            mode = str(api_data["mode"]) if for_api else str(self.request.params['type'])
            issue = api_data["issue"] if for_api else IssueHelper.get_issue_id(self.request)

            return_dict = dict()

            if mode == '0':  # start statement
                return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_start(value, issue, True)
            elif mode == '1':  # edit statement popup
                statement_uid = self.request.params['extra']
                return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_edits(value, statement_uid)
            elif mode == '2':  # start premise
                return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_start(value, issue, False)
            elif mode == '3':  # adding reasons
                return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_reasons(value, issue)
            elif mode == '4':  # getting text
                return_dict = FuzzyStringMatcher.get_strings_for_search(value)
            elif mode == '5':  # getting public nicknames
                nickname, session_id = self.get_nickname_and_session(for_api, api_data)
                return_dict['distance_name'], return_dict['values'] = FuzzyStringMatcher.get_strings_for_public_nickname(value, nickname)
            else:
                logger('fuzzy_search', 'main', 'unknown mode: ' + str(mode))
                return_dict = {'error': _tn.get(_tn.internalError)}

        except KeyError as e:
            return_dict = {'error': _tn.get(_tn.internalError)}
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
