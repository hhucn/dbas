"""
Common python logging.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

# -*- coding: utf-8 -*-

import logging
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)


def logger(who, when, what, warning=False, error=False, debug=False):
    """
    Log for the console and logfile on disk. Logged format: [who.upper()] when <what>

    :param who: which class
    :param when: which method
    :param what: what message
    :param warning: Boolean, default False
    :param error: Boolean, default False
    :param debug: Boolean, default False
    :return: None
    """

    info = not(warning or error or debug)
    logger = logging.getLogger(__name__)
    try:
        if info:
            logger.info('[{}] {}: {}'.format(who.upper(), when, what))
        if warning:
            logger.warning('[{}] {}: {}'.format(who.upper(), when, what))
        if error:
            logger.error('[{}] {}: {}'.format(who.upper(), when, what))
        if debug:
            logger.debug('[{}] {}: {}'.format(who.upper(), when, what))
    except Exception as e:
        logger.error('[LOGGER] LOGGER ERROR: ' + repr(e))
