"""
Common functions shared between the validators.
"""

from sys import _getframe

import logging
from pyramid.request import Request

from dbas.lib import escape_string

LOG = logging.getLogger(__name__)


def add_error(request: Request, verbose_short: str, verbose_long: str = None, location: str = 'body',
              status_code: int = 400):
    """
    Log and add errors to request. Supports different verbose-messages.

    :param request:
    :param verbose_short: short description of error
    :param verbose_long: long, verbose description of error
    :param location: Where did the error happen? Has to be: body, path, query, ...
    :param status_code: HTTP status code
    :return:
    """
    error_msg = verbose_short if not verbose_long else verbose_short + ', additional infos:' + verbose_long
    LOG.error("%s: %s", _getframe(1).f_code.co_name, error_msg)
    request.errors.add(location, verbose_short, verbose_long)
    request.errors.status = status_code


def escape_if_string(data: dict, key: str):
    """
    Escape string if key exists.

    :param data:
    :param key:
    :return: Return escaped value if it was a string
    """
    val = data.get(key)
    if val and isinstance(val, str):
        return escape_string(val)
    return val
