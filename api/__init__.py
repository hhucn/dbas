"""
REST API for to communicate with the world. Enables remote discussion from arbitrary locations.
"""
import sys

from pyramid.config import Configurator

# Enable console print when in dockerized environment
ENABLE_DOCKER_PRINT = True

if ENABLE_DOCKER_PRINT:
    class Unbuffered(object):
        def __init__(self, stream):
            self.stream = stream

        def write(self, data):
            self.stream.write(data)
            self.stream.flush()

        def __getattr__(self, attr):
            return getattr(self.stream, attr)


    sys.stdout = Unbuffered(sys.stdout)


def init(config):
    config.include("cornice")
    config.scan("api.views")


def main(global_config, **settings):
    config = Configurator(settings=settings)
    init(config)
    return config.make_wsgi_app()


def includeme(config):
    init(config)


# def setup_package():
#     settings = add_settings_to_appconfig()
#     DBDiscussionSession.remove()
#     DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))


def teardown_package():
    pass
