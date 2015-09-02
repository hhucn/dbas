from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

from dbas.security import groupfinder

from sqlalchemy import engine_from_config
from .database import *

import logging

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
	engine = engine_from_config(settings, 'sqlalchemy.')
	load_database(engine)

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
	config = Configurator(settings=settings,root_factory='dbas.database.RootFactory')
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
	config.add_route('main_page',     '/')
	config.add_route('main_login',    '/login')
	config.add_route('main_logout',   '/logout')
	config.add_route('main_contact',  '/contact')
	config.add_route('main_discussion_start',  '/discussion/start')
	config.add_route('main_discussion',  '/discussion/{parameters}/{service}/go')
	config.add_route('main_settings', '/settings')
	config.add_route('main_news',     '/news')
	config.add_route('main_imprint',  '/imprint')
	config.add_route('404',           '/404')

	# ajax for navigation logic, administraion, settigs and editing/viewing log
	config.add_route('ajax_get_start_statements',                '/discussion/ajax_get_start_statements')
	config.add_route('ajax_get_premisses_for_statement',         '/discussion/{url:.*}/ajax_get_premisses_for_statement')
	config.add_route('ajax_reply_for_premissegroup',             '/discussion/{url:.*}/ajax_reply_for_premissegroup')
	config.add_route('ajax_reply_for_response_of_confrontation', '/discussion/{url:.*}/ajax_reply_for_response_of_confrontation')
	config.add_route('ajax_reply_for_argument',                  '/discussion/{url:.*}/ajax_reply_for_argument')
	config.add_route('ajax_set_new_start_statement',             '/discussion/{url:.*}ajax_set_new_start_statement{params:.*}')
	config.add_route('ajax_set_new_premisses',                   '/discussion/{url:.*}ajax_set_new_premisses{params:.*}')
	config.add_route('ajax_switch_language',                     '/discussion/{url:.*}ajax_switch_language{params:.*}')
	config.add_route('ajax_all_users',                           '/discussion/{url:.*}ajax_all_users{params:.*}')
	config.add_route('ajax_manage_user_track',                   '/discussion/{url:.*}ajax_manage_user_track{params:.*}')
	config.add_route('ajax_get_logfile_for_statement',           '/discussion/{url:.*}ajax_get_logfile_for_statement{params:.*}')
	config.add_route('ajax_set_correcture_of_statement',         '/discussion/{url:.*}ajax_set_correcture_of_statement{params:.*}')
	config.add_route('ajax_get_shortened_url',         '/discussion/{url:.*}ajax_get_shortened_url{params:.*}')


	# read the input and start
	config.scan()
	return config.make_wsgi_app()
