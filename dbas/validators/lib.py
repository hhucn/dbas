"""
Common functions shared between the validators.
"""

from dbas.logger import logger


def add_error(request, log_key, verbose_short, verbose_long=None):
    """
    Log and add errors to request. Supports different verbose-messages.

    :param request:
    :param log_key: category in log-description, e.g. the caller function
    :param verbose_short: short description of error
    :param verbose_long: long, verbose description of error
    :return:
    """
    logger('validation', log_key, verbose_short, error=True)
    request.errors.add('body', verbose_short, verbose_long)
    request.errors.status = 400
