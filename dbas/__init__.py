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
		log.debug('__init__() '.upper() + 'main <' + k + ' : ' + v + '>')

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
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	config.set_session_factory(session_factory)

	# includings for the config
	config.include('pyramid_chameleon')
	config.include('pyramid_mailer')
	# config.include('pyramid_beaker') # done in the ini
	# config.add_translation_dirs('dbas:locale')

	# adding all routes
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('main_page', '/')
	config.add_route('main_login', '/login')
	config.add_route('main_logout', '/logout')
	config.add_route('main_contact', '/contact')
	config.add_route('main_content', '/content')
	config.add_route('main_settings', '/settings')
	config.add_route('main_news', '/news')
	config.add_route('main_imprint', '/imprint')
	config.add_route('404', '/404')

	config.add_route('ajax_all_positions', '/ajax_all_positions')
	config.add_route('ajax_all_users', '/ajax_all_users')
	config.add_route('ajax_manage_user_track', '/ajax_manage_user_track')
	config.add_route('ajax_all_arguments_for_island', '/ajax_all_arguments_for_island')

	config.add_route('ajax_args_for_new_discussion_round', '/ajax_args_for_new_discussion_round')
	config.add_route('ajax_arguments_connected_to_position_uid', '/ajax_arguments_connected_to_position_uid')

	config.add_route('ajax_send_new_position', '/ajax_send_new_position')
	config.add_route('ajax_send_new_arguments', '/ajax_send_new_arguments')
	config.add_route('ajax_one_step_back', '/ajax_one_step_back')
	config.add_route('ajax_get_logfile_for_statement', '/ajax_get_logfile_for_statement')
	config.add_route('ajax_send_correcture_of_statement', '/ajax_send_correcture_of_statement')

	# read the input and start
	config.scan()
	return config.make_wsgi_app()
