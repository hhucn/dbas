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


class HTTP204(exc.HTTPError):
	"""
	HTTP 204: Request successful, but no content was provided.
	:return:
	"""
	def __init__(self, msg='No Content'):
		body = {'status': 204, 'message': msg}
		Response.__init__(self, json.dumps(body))
		self.status = 204
		self.content_type = 'application/json'


class HTTP401(exc.HTTPError):
	"""
	Return a 401 HTTP Error message if user is not authenticated.
	:return:
	"""
	def __init__(self, msg='Unauthorized'):
		body = {'status': 401, 'message': msg}
		Response.__init__(self, json.dumps(body))
		self.status = 401
		self.content_type = 'application/json'


class HTTP501(exc.HTTPError):
	"""
	HTTP 501: Not implemented.
	:return:
	"""
	def __init__(self, msg='Not Implemented'):
		body = {'status': 501, 'message': msg}
		Response.__init__(self, json.dumps(body))
		self.status = 501
		self.content_type = 'application/json'
