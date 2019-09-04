"""
REST API for websockets.
"""
import logging

from pyramid.config import Configurator

LOG = logging.getLogger(__name__)


def init(config):
    config.scan("websocket.views")


def main(global_config, **settings):
    config = Configurator(settings=settings)
    init(config)
    return config.make_wsgi_app()


def includeme(config):
    init(config)


if __name__ == "__main__":
    LOG.debug("Starting websockets")
