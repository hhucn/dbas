from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

from dbas.security import groupfinder

from sqlalchemy import engine_from_config
from .database import *

import logging

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""

	# authentication and authorization
	authn_policy = AuthTktAuthenticationPolicy('89#s3cr3t_15', callback=groupfinder, hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()

	# log settings
	log = logging.getLogger(__name__)
	for k, v in settings.items():
		log.debug('__init__() '.upper() + 'main() <' + str(k) + ' : ' + str(v) + '>')

	# load database
	discussionEngine = engine_from_config(settings, 'sqlalchemy-discussion.')
	load_discussion_database(discussionEngine)
	newsEngine = engine_from_config(settings, 'sqlalchemy-news.')
	load_news_database(newsEngine)

	# session management and cache region support with pyramid_beaker
	session_factory = session_factory_from_settings(settings)
	set_cache_regions_from_settings(settings)

	# creating the configurator
	settings={'pyramid.default_locale_name':'en',
			  'mail.host':'imap.googlemail.com',
			  'mail.port':'465',
			  'mail.username':'dbas.hhu@gmail.com',
			  'mail.password':'dbas_System#2015',
			  'mail.ssl':'True',
	          'mail.tls':'False',
	          'mail.default_sender':'dbas.hhu@gmail.com'
			  }

	# creating the configurator	cache_regions = set_cache_regions_from_settings
	config = Configurator(settings=settings,root_factory='dbas.security.RootFactory')
	config.add_translation_dirs('dbas:locale') # add this before the locale negotiator

	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	config.set_session_factory(session_factory)

	# includings for the config
	config.include('pyramid_chameleon')
	config.include('pyramid_mailer')
	config.include('pyramid_beaker')

	# adding all routes
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('main_page',               '/')
	config.add_route('main_contact',            '/contact')
	config.add_route('main_discussion_start',   '/discussion/start')                        # TODO WILL BE KILLED!
	config.add_route('main_discussion_issue',   '/discussion/start/issue={issue}')          # TODO WILL BE KILLED!
	config.add_route('main_discussion',         '/discussion/{parameters}/{service}/go')    # TODO WILL BE KILLED!
	config.add_route('main_settings',           '/settings')
	config.add_route('main_admin',              '/admin')
	config.add_route('main_news',               '/news')
	config.add_route('main_imprint',            '/imprint')
	config.add_route('404',                     '/404')

	# ajax for navigation logic, administraion, settigs and editing/viewing log
	config.add_route('ajax_user_login',                          '{url:.*}ajax_user_login')
	config.add_route('ajax_user_logout',                         '{url:.*}ajax_user_logout')

	# TODO KILL THESE
	config.add_route('ajax_get_start_statements',                '/{prefix}/{url:.*}ajax_get_start_statements')
	config.add_route('ajax_get_text_for_statement',              '/{prefix}/{url:.*}ajax_get_text_for_statement')
	config.add_route('ajax_get_premises_for_statement',          '/{prefix}/{url:.*}ajax_get_premises_for_statement')
	config.add_route('ajax_get_premise_for_statement',           '/{prefix}/{url:.*}ajax_get_premise_for_statement')
	config.add_route('ajax_reply_for_premisegroup',              '/{prefix}/{url:.*}ajax_reply_for_premisegroup')
	config.add_route('ajax_reply_for_response_of_confrontation', '/{prefix}/{url:.*}ajax_reply_for_response_of_confrontation')
	config.add_route('ajax_reply_for_argument',                  '/{prefix}/{url:.*}ajax_reply_for_argument')

	config.add_route('ajax_set_new_start_statement',             '/{prefix}/{url:.*}ajax_set_new_start_statement{params:.*}')
	config.add_route('ajax_set_new_start_premise',               '/{prefix}/{url:.*}ajax_set_new_start_premise{params:.*}')
	config.add_route('ajax_set_new_premises_for_x',              '/{prefix}/{url:.*}ajax_set_new_premises_for_x{params:.*}')
	config.add_route('ajax_set_correcture_of_statement',         '/{prefix}/{url:.*}ajax_set_correcture_of_statement{params:.*}')
	config.add_route('ajax_all_users',                           '/{prefix}/{url:.*}ajax_all_users{params:.*}')
	config.add_route('ajax_get_logfile_for_statement',           '/{prefix}/{url:.*}ajax_get_logfile_for_statement{params:.*}')
	config.add_route('ajax_get_shortened_url',                   '/{prefix}/{url:.*}ajax_get_shortened_url{params:.*}')
	config.add_route('ajax_get_attack_overview',                 '/{prefix}/{url:.*}ajax_get_attack_overview{params:.*}')

	config.add_route('ajax_user_registration',                   '{url:.*}ajax_user_registration')
	config.add_route('ajax_user_password_request',               '{url:.*}ajax_user_password_request')
	config.add_route('ajax_fuzzy_search',                        '{url:.*}ajax_fuzzy_search')
	config.add_route('ajax_get_issue_list',                      '{url:.*}ajax_get_issue_list')
	config.add_route('ajax_switch_language',                     '{url:.*}ajax_switch_language{params:.*}')
	config.add_route('ajax_get_everything_for_island_view',      '{url:.*}ajax_get_everything_for_island_view{params:.*}')
	config.add_route('ajax_get_database_dump',                   '{url:.*}ajax_get_database_dump')
	config.add_route('ajax_get_user_track',                      'ajax_get_user_track')
	config.add_route('ajax_delete_user_track',                   'ajax_delete_user_track')
	config.add_route('ajax_get_user_history',                    'ajax_get_user_history')
	config.add_route('ajax_delete_user_history',                 'ajax_delete_user_history')
	config.add_route('ajax_get_news',                            'ajax_get_news')
	config.add_route('ajax_send_news',                           'ajax_send_news')

	config.add_route('ajax_additional_service',                  '{stuff:.*}additional_service')

	# ajax for navigation logic at the end, otherwise the * pattern will do shit
	# config.add_route('discussion_init',       '/d')                                               # Route 1 aus den Unterlagen
	# config.add_route('discussion_init',       '/d/{slug}')                                        # Route 2 aus den Unterlagen
	# config.add_route('discussion_attitude',   '/d/{slug}/{statement_id}')                         # Route 3 aus den Unterlagen
	# config.add_route('discussion_justify',    '/d/{slug}/j/{statement_id}/{supportive}')          # Route 4 aus den Unterlagen
	# config.add_route('discussion_justify',    '/d/{slug}/j/{text_id}/{supportive}/{relation}')    # Route 6 aus den Unterlagen
	# config.add_route('discussion_reaction',   '/d/{slug}/r/{pgroup_id}/{supportive}/{text_id}')   # Route 5 aus den Unterlagen
	# config.add_route('discussion_reaction',   '/d/{slug}/r/{pgroup_id}/{supportive}/{text_id}')   # Route 7 aus den Unterlagen

	config.add_route('discussion_justify',    '/a/{slug}/j/{statement_or_text_id}/{mode}*relation') # Route 4,6 aus den Unterlagen
	config.add_route('discussion_attitude',   '/a/{slug}/a/{statement_id}')                               # Route   3 aus den Unterlagen
	config.add_route('discussion_init',       '/a*slug')                                                  # Route 1,2 aus den Unterlagen
	# config.add_route('discussion_reaction',   '/a/{slug}/r/{pgroup_id}/{supportive}/{text_id}')           # Route 5,7 aus den Unterlagen

	# read the input and start
	config.scan()
	return config.make_wsgi_app()
