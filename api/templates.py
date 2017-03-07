"""
Templates for API responses.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from .lib import logger
log = logger()


def error(message, logtype=None, logmsg=None):
    """
    Prepare dictionary and add error status code to it.

    :param message: Message to be returned
    :returns: wrapped dictionary
    :rtype: dict
    """
    if logtype:
        log.info("[{}] {}".format(logtype, message))
    elif logtype and logmsg:
        log.info("[{}] {}".format(logtype, logmsg))
    return {"status": "error",
            "message": message}
