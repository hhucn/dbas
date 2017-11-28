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


def json_to_dict(col):
    """
    Given a json object as bytes, convert it to a Python dictionary.

    :param col:
    :type col: bytes
    :rtype: dict
    """
    if isinstance(col, dict):
        return col
    elif isinstance(col, bytes):
        col = col.decode("utf-8")
    return json.loads(col)


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


class HTTP400(exc.HTTPError):
    """
    HTTP 400: Bad Request

    :return: JSON response
    """
    def __init__(self, msg='Bad Request'):
        body = {'status': 400, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 400
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
