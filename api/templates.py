"""
Templates for API responses.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from .lib import logger

log = logger()


def error(message):
    """
    Prepare dictionary and add error status code to it.

    :param message: Message to be returned
    :returns: wrapped dictionary
    :rtype: dict
    """
    log.error(message)
    return {"status": "error",
            "message": message}
