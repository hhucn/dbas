from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from dbas.security import groupfinder

from sqlalchemy import engine_from_config
from .database import *


def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	# authentication and authorization
	authn_policy = AuthTktAuthenticationPolicy(
		'sosecret', callback=groupfinder, hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()

	# load database
	engine = engine_from_config(settings, 'sqlalchemy.')
	load_database(engine)

	# creating the configurator
	settings={'pyramid.default_locale_name':'en',
			  'mail.host':'rohrpostix.cs.uni-duesseldorf.de',
			  'mail.port':'465',
			  'mail.username':'krauthoff',
			  'mail.password':'cs_kraut#1989',
			  'mail.ssl':'True',
	          'mail.tls':'False',
	          'mail.default_sender':'krauthoff@cs.uni-duesseldorf'
			  }
	config = Configurator(settings=settings,root_factory='dbas.database.RootFactory')
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)

	# includings for the config
	config.include('pyramid_chameleon')
	config.include('pyramid_debugtoolbar')
	config.include('pyramid_mailer')

	# adding all routes
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('main_page', '/')
	config.add_route('main_login', '/login')
	config.add_route('main_logout', '/logout')
	config.add_route('main_logout_redirect', '/logout_redirect')
	config.add_route('main_contact', '/contact')
	config.add_route('main_content', '/content')
	config.add_route('main_settings', '/settings')
	config.add_route('main_news', '/news')
	config.add_route('main_impressum', '/impressum')
	config.add_route('404', '/404')
	config.add_route('get_ajax_positions','/ajax_positions')

	# read the input and start
	config.scan()
	return config.make_wsgi_app()
