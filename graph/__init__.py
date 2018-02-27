"""
REST API for exporting different data from D-BAS into the world.

.. sectionauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""
from pyramid.config import Configurator
from dbas.logger import logger


def init(config):
    config.scan("graph.views")


def main(global_config, **settings):
    config = Configurator(settings=settings)
    init(config)
    return config.make_wsgi_app()


def includeme(config):
    init(config)


if __name__ == "__main__":
    logger("i", "in too")
