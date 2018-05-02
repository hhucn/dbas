"""
Common python logging.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

# -*- coding: utf-8 -*-

import logging
from sys import _getframe
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)


def logger(who: str, what: str, warning: bool=False, error: bool=False, info: bool=False):
    """
    Logs giving strings as debug in the format of: [who.upper()] when <what>

    :param who: which class
    :param what: what message
    :param warning: Boolean, default False
    :param error: Boolean, default False
    :param debug: Boolean, default False
    :return: None
    """

    debug = not(warning or error or info)
    logger = logging.getLogger(__name__)
    try:
        msg = '[{}] {}: {}'.format(who.upper(), _getframe(1).f_code.co_name, what)

        if info:
            logger.info(msg)
        if warning:
            logger.warning(msg)
        if error:
            logger.error(msg)
        if debug:
            logger.debug(msg)
    except Exception as e:
        logger.error('[LOGGER] LOGGER ERROR: ' + repr(e))
