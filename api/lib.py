# Common library for API Component
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import json
import logging

from webob import Response, exc


def logger():
	"""
	Create a logger.
	:return:
	"""
	log = logging.getLogger()
	log.setLevel(logging.DEBUG)
	return log


def json_bytes_to_dict(col):
	"""
	Given a json object as bytes, convert it to a Python dictionary.
	:param col: bytes
	:return: dict
	"""
	return json.loads(col.decode("utf-8"))
