"""
REST API for to communicate with the world. Enables remote discussion from arbitrary locations.

.. sectionauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from pyramid.config import Configurator
from dbas.logger import logger


def init(config):
	config.include("cornice")
	config.add_route("whoami", "/whoami")
	config.scan("api.views")


def main(global_config, **settings):
	config = Configurator(settings=settings)
	init(config)
	return config.make_wsgi_app()


def includeme(config):
	init(config)


if __name__ == "__main__":
	logger("i", "want", "in")
