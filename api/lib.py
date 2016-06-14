"""
Common, pure functions used by the API.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json
import logging
from functools import reduce
from html import escape

from webob import Response, exc

from dbas import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences


# =============================================================================
# Getting Information from database
# =============================================================================
def get_references_for_url(host=None, path=None):
	"""
	Query database for given URL and return all references.

	:param host: sanitized string of the reference's host
	:type host: str
	:param path: path to article / reference on reference's host
	:type path: str
	:return: list of strings representing quotes from the given site, which were stored in our database
	:rtype: list
	"""
	if host and path:
		return DBDiscussionSession.query(StatementReferences).filter_by(host=host, path=path).all()


def get_reference_by_id(ref_id=None):
	"""
	Query database to get a reference by its id.

	:param ref_id: StatementReferences.uid
	:return:
	"""
	if ref_id:
		return DBDiscussionSession.query(StatementReferences).filter_by(uid=ref_id).first()


# =============================================================================
# Other
# =============================================================================
def logger():
	"""
	Create a logger.
	"""
	log = logging.getLogger()
	log.setLevel(logging.DEBUG)
	return log


def escape_html(evil):
	"""
	Replace html tags.

	:param evil:
	:return: escaped string
	:rtype: str
	"""
	return escape(str(evil))


def json_bytes_to_dict(col):
	"""
	Given a json object as bytes, convert it to a Python dictionary.

	:param col:
	:type col: bytes
	:rtype: dict
	"""
	return json.loads(col.decode("utf-8"))


def flatten(l):
	"""
	Flattens a list.

	:param l: list of lists
	:return:
	"""
	if not l:
		return None
	return reduce(lambda x, y: x + y, l)


def merge_dicts(d1, d2):
	"""
	Merge two dictionaries.

	:param d1: first dictionary
	:param d2: second dictionary, overwriting existing keys in d1
	:return: merged dictionary
	"""
	if isinstance(d1, dict) and isinstance(d2, dict):
		merged = d1.copy()
		merged.update(d2)
		return merged
	return None


def debug_start():
	"""
	Prepare for debug prints.

	:return: Some hashes and linebreaks
	"""
	print("\n\n\n##########\n")


def debug_end():
	"""
	End debug prints.

	:return: Some hashes and linebreaks
	"""
	print("\n##########\n\n\n")


class HTTP204(exc.HTTPError):
	"""
	HTTP 204: Request successful, but no content was provided.

	:return: JSON response
	"""
	def __init__(self, msg='No Content'):
		body = {'status': 204, 'message': msg}
		Response.__init__(self, json.dumps(body))
		self.status = 204
		self.content_type = 'application/json'


class HTTP401(exc.HTTPError):
	"""
	HTTP 401: Not authenticated

	:return: JSON response
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
