from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings={'pyramid.default_locale_name':'en'})
    config.include('pyramid_chameleon')
    config.include('pyramid_debugtoolbar')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('main_page', '/')
    config.add_route('main_login', '/login')
    config.add_route('main_contact', '/contact')
    config.add_route('404', '/404')
    config.scan()
    return config.make_wsgi_app()
