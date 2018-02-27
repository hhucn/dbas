"""
Common functions shared between the validators.
"""

from dbas.lib import escape_string
from dbas.logger import logger
from sys import _getframe


def add_error(request, verbose_short, verbose_long=None):
    """
    Log and add errors to request. Supports different verbose-messages.

    :param request:
    :param verbose_short: short description of error
    :param verbose_long: long, verbose description of error
    :return:
    """
    logger('validation', _getframe(1).f_code.co_name, verbose_short, error=True)
    request.errors.add('body', verbose_short, verbose_long)
    request.errors.status = 400


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
