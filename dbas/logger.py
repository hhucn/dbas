"""
Common python logging.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)


def logger(who, when, what, warn=False, error=False, debug=False):
    """
    Log for the console and logfile on disk. Logged format: [who.upper()] when <what>

    :param who: which class
    :param when: which method
    :param what: what mesage
    :param warn: Boolean, default False
    :param error: Boolean, default False
    :param debug: Boolean, default False
    :return: None
    """
    if who != 'VotingHelper':
        return

    info = not(warn or error or debug)
    logger = logging.getLogger(__name__)
    try:
        if info:
            logger.info('[' + who.upper() + '] ' + when + ': ' + what)
        if warn:
            logger.warn('[' + who.upper() + '] ' + when + ': ' + what)
        if error:
            logger.error('[' + who.upper() + '] ' + when + ': ' + what)
        if debug:
            logger.debug('[' + who.upper() + '] ' + when + ': ' + what)
    except Exception as e:
        logger.error('[LOGGER] LOGGER ERROR: ' + repr(e))
