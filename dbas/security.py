"""
Security module of D-BAS, where the groups are set
"""

import logging

from pyramid.security import Allow, Everyone
from sqlalchemy.exc import InternalError

from .database import DBDiscussionSession
from .database.discussion_model import User

LOG = logging.getLogger(__name__)


class RootFactory():
    """
    Defines the ACL
    """
    __acl__ = [(Allow, Everyone, 'everybody'),
               (Allow, 'group:ADMIN', ('admin', 'edit', 'use')),
               (Allow, 'group:AUTHOR', ('edit', 'use')),
               (Allow, 'group:USER', 'use'),
               (Allow, 'group:SPECIAL', 'use')]

    def __init__(self, _):
        pass


def groupfinder(nick, _):
    """
    Finds group for the user id in given request
    :param nick: current user id
    :param request: request
    :return: given group as list or empty list
    """
    LOG.debug("nick: %s", nick)
    try:
        user = DBDiscussionSession.query(User).filter_by(nickname=nick).first()
    except InternalError as i:
        LOG.error("%s", i)
        return []

    if user:
        group = user.group
        LOG.debug("return [group: %s]", group.name)
        return ['group:' + group.name]

    LOG.debug("return []")
    return []
