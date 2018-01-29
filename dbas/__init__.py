"""
Core component of D-BAS. The Dialog-Based Argumentation Software avoids the pitfalls of unstructured systems such as
asynchronous threaded discussions and it is usable by any participant without training while still supporting the full
complexity of real-world argumentation. The key idea is to let users exchange arguments with each other in the form of
a time-shifted dialog where arguments are presented and acted upon one-at-a-time.

.. sectionauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

# from wsgiref.simple_server import make_server

import logging
import os
import re
import time

from .database import load_discussion_database
from .security import groupfinder
from configparser import ConfigParser, NoSectionError
from dbas.database import get_db_environs
from dbas.handler.rss import rewrite_issue_rss, create_news_rss
from dbas.lib import get_global_url
from dbas.query_wrapper import get_not_disabled_issues_as_query
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.static import QueryStringConstantCacheBuster
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings
from sqlalchemy import engine_from_config


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # Patch in all environment variables
    settings.update(get_dbas_environs())

    # Patch in beaker url
    settings.update(get_db_environs(key="session.url", db_name="beaker"))

    # log settings
    log = logging.getLogger(__name__)
    development = False
    for k, v in settings.items():
        development = development or 'testing' in str(v)
        log.debug('__INIT__() main() <{} : {}>'.format(str(k), str(v)))

    # authentication and authorization
    authn_policy = AuthTktAuthenticationPolicy(settings["authn.secret"], callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    # load database
    settings.update(get_db_environs("sqlalchemy.discussion.url", db_name="discussion"))

    discussion_engine = engine_from_config(settings, "sqlalchemy.discussion.")
    load_discussion_database(discussion_engine)

    # session management and cache region support
    session_factory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)

    # include custom parts
    sections = ['service']
    for s in sections:
        try:
            parser = ConfigParser()
            parser.read(global_config['__file__'])
            custom_settings = dict()
            for k, v in parser.items('settings:{}'.format(s)):
                log.debug('__init__() '.upper() + 'main() <settings:' + str(s) + ':' + str(k) + ' : ' + str(v) + '>')
                custom_settings['settings:{}:{}'.format(s, k)] = v
            settings.update(custom_settings)
        except NoSectionError as e:
            log.debug('__init__() '.upper() + 'main() <No ' + s + '-Section> ' + str(e))

    # creating the configurator
    config = Configurator(settings=settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,
                          root_factory='dbas.security.RootFactory',
                          session_factory=session_factory
                          )
    config.add_translation_dirs('dbas:locale',
                                'admin:locale')  # add this before the locale negotiator
    config.set_default_csrf_options(require_csrf=True)

    # Include apps
    config.include('api', route_prefix='/api')
    config.include('api.v2', route_prefix='/api/v2')
    config.include('graph', route_prefix='/graph')
    config.include('admin', route_prefix='/admin')
    config.include('websocket', route_prefix='/websocket')

    # more includes are in the config
    config.include('pyramid_chameleon')
    config.include('pyramid_mailer')
    config.include('pyramid_tm')

    config.add_static_view(name='static', path='dbas:static/', cache_max_age=3600)
    config.add_static_view(name='websocket', path='websocket:static/', cache_max_age=3600)
    config.add_static_view(name='admin', path='admin:static/', cache_max_age=3600)
    config.add_cache_buster('static', QueryStringConstantCacheBuster(str(int(time.time()))))
    config.add_cache_buster('admin:static/', QueryStringConstantCacheBuster(str(int(time.time()))))
    config.add_cache_buster('websocket:static/', QueryStringConstantCacheBuster(str(int(time.time()))))

    # adding main routes
    config.add_route('main_page', '/')
    config.add_route('main_settings', '/settings')
    config.add_route('main_notification', '/notifications')
    config.add_route('main_news', '/news')
    config.add_route('main_imprint', '/imprint')
    config.add_route('main_rss', '/rss')
    config.add_route('main_faq', '/faq')
    config.add_route('main_docs', '/docs')
    config.add_route('main_experiment', '/fieldexperiment')
    config.add_route('main_mydiscussions', '/mydiscussions')
    config.add_route('main_user', '/user/{uid}')
    config.add_route('main_graphiql', '/graphiql')

    # ajax for navigation logic, administration, settings and editing/viewing log
    config.add_route('ajax_user_login', '{url:.*}ajax_user_login')
    config.add_route('ajax_user_login_oauth', '{url:.*}ajax_user_login_oauth')
    config.add_route('ajax_user_logout', '{url:.*}ajax_user_logout')
    config.add_route('ajax_set_new_start_argument', '/{url:.*}ajax_set_new_start_argument')
    config.add_route('ajax_set_new_start_statement', '/{url:.*}ajax_set_new_start_statement')
    config.add_route('ajax_set_new_start_premise', '/{url:.*}ajax_set_new_start_premise')
    config.add_route('ajax_set_new_premises_for_argument', '/{url:.*}ajax_set_new_premises_for_argument')
    config.add_route('ajax_set_correction_of_statement', '/{url:.*}ajax_set_correction_of_statement')
    config.add_route('ajax_set_new_issue', '/{url:.*}ajax_set_new_issue')
    config.add_route('ajax_get_logfile_for_statements', '/{url:.*}ajax_get_logfile_for_statements')
    config.add_route('ajax_get_shortened_url', '/{url:.*}ajax_get_shortened_url')
    config.add_route('ajax_user_registration', '/{url:.*}ajax_user_registration')
    config.add_route('ajax_user_password_request', '/{url:.*}ajax_user_password_request')
    config.add_route('ajax_fuzzy_search', '/{url:.*}ajax_fuzzy_search')
    config.add_route('ajax_switch_language', '{url:.*}ajax_switch_language{params:.*}')
    config.add_route('ajax_send_notification', '{url:.*}ajax_send_notification')
    config.add_route('ajax_get_infos_about_argument', '/{url:.*}ajax_get_infos_about_argument')
    config.add_route('ajax_get_user_with_same_opinion', '/{url:.*}ajax_get_user_with_same_opinion')
    config.add_route('ajax_get_public_user_data', '/{url:.*}ajax_get_public_user_data')
    config.add_route('ajax_get_user_history', 'ajax_get_user_history')
    config.add_route('ajax_get_all_edits', 'ajax_get_all_edits')
    config.add_route('ajax_get_all_posted_statements', 'ajax_get_all_posted_statements')
    config.add_route('ajax_get_all_argument_clicks', 'ajax_get_all_argument_clicks')
    config.add_route('ajax_get_all_statement_clicks', 'ajax_get_all_statement_clicks')
    config.add_route('ajax_get_all_marked_arguments', 'ajax_get_all_marked_arguments')
    config.add_route('ajax_get_all_marked_statements', 'ajax_get_all_marked_statements')
    config.add_route('ajax_set_user_setting', 'ajax_set_user_setting')
    config.add_route('ajax_set_user_language', 'ajax_set_user_language')
    config.add_route('ajax_delete_user_history', 'ajax_delete_user_history')
    config.add_route('ajax_delete_statistics', 'ajax_delete_statistics')
    config.add_route('ajax_get_news', 'ajax_get_news')
    config.add_route('ajax_send_news', 'ajax_send_news')
    config.add_route('ajax_notifications_read', 'ajax_notifications_read')
    config.add_route('ajax_notifications_delete', 'ajax_notifications_delete')
    config.add_route('ajax_get_arguments_by_statement_uid', 'ajax_get_arguments_by_statement/{uid}')
    config.add_route('ajax_additional_service', '{stuff:.*}additional_service')
    config.add_route('ajax_flag_argument_or_statement', '{url:.*}ajax_flag_argument_or_statement')
    config.add_route('ajax_split_or_merge_statement', '{url:.*}ajax_split_or_merge_statement')
    config.add_route('ajax_split_or_merge_premisegroup', '{url:.*}ajax_split_or_merge_premisegroup')
    config.add_route('ajax_review_delete_argument', '{url:.*}ajax_review_delete_argument')
    config.add_route('ajax_review_optimization_argument', '{url:.*}ajax_review_optimization_argument')
    config.add_route('ajax_review_duplicate_statement', '{url:.*}ajax_review_duplicate_statement')
    config.add_route('ajax_review_edit_argument', '{url:.*}ajax_review_edit_argument')
    config.add_route('ajax_review_splitted_premisegroup', '{url:.*}ajax_review_splitted_premisegroup')
    config.add_route('ajax_review_merged_premisegroup', '{url:.*}ajax_review_merged_premisegroup')
    config.add_route('ajax_undo_review', '{url:.*}ajax_undo_review')
    config.add_route('ajax_cancel_review', '{url:.*}ajax_cancel_review')
    config.add_route('ajax_review_lock', '{url:.*}ajax_review_lock')
    config.add_route('ajax_revoke_content', '{url:.*}ajax_revoke_content')
    config.add_route('ajax_get_references', '{url:.*}ajax_get_references')
    config.add_route('ajax_set_references', '{url:.*}ajax_set_references')
    config.add_route('ajax_set_seen_statements', '{url:.*}ajax_set_seen_statements')
    config.add_route('ajax_mark_statement_or_argument', '{url:.*}ajax_mark_statement_or_argument')
    config.add_route('ajax_set_discussion_properties', '{url:.*}ajax_set_discussion_properties')

    # logic at the end, otherwise the * pattern will do shit
    config.add_route('discussion_support', '/discuss/{slug}/support/{arg_id_user}/{arg_id_sys}')
    config.add_route('discussion_reaction', '/discuss/{slug}/reaction/{arg_id_user}/{mode}/{arg_id_sys}')
    config.add_route('discussion_justify', '/discuss/{slug}/justify/{statement_or_arg_id}/{mode}*relation')
    config.add_route('discussion_attitude', '/discuss/{slug}/attitude/*statement_id')
    config.add_route('discussion_choose', '/discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids')
    config.add_route('discussion_jump', '/discuss/{slug}/jump/{arg_id}')
    config.add_route('discussion_finish', '/discuss/finish')
    config.add_route('discussion_init', '/discuss*slug')

    # review section
    config.add_route('review_index', '/review')
    config.add_route('review_reputation', '/review/reputation')
    config.add_route('review_history', '/review/history')
    config.add_route('review_ongoing', '/review/ongoing')
    config.add_route('review_content', '/review/{queue}')

    config.scan()

    __write_rss_feeds()

    return config.make_wsgi_app()


def __write_rss_feeds():
    issues = get_not_disabled_issues_as_query().all()
    for issue in issues:
        rewrite_issue_rss(issue.uid, issue.lang, get_global_url())
    create_news_rss(get_global_url(), 'en')


def get_dbas_environs(prefix=""):
    """
    Fetches all environment variables beginning with `prefix` (default: ``).

    Returns a dictionary where the keys are substituted versions of their corresponding environment variables.
    Substitution rules:

    1. The prefix will be stripped.
    2. All single underscores will be substituted with a dot.
    3. All double underscores will be substituted with a single underscore.
    4. uppercase will be lowered.

    Example::

        "TEST_FOO__BAR" ==> "test.foo_bar"

    :param prefix: The prefix of the environment variables.
    :return: The dictionary of parsed environment variables and their values.
    """
    dbas_keys = list(filter(lambda x: x.startswith(prefix), os.environ))
    return dict([(_environs_to_keys(k, prefix), os.environ[k]) for k in dbas_keys])


def _environs_to_keys(key, prefix=""):
    prefix_pattern = '^{prefix}'.format(prefix=prefix)
    single_underscore_pattern = r'(?<!_)_(?!_)'

    striped_of_prefix = re.sub(prefix_pattern, "", key)

    return str(re.sub(single_underscore_pattern, ".", striped_of_prefix).replace('__', '_')).lower()
