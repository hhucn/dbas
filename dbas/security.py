"""
Security module of D-BAS, where the groups are set

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
from pyramid.security import Allow, Everyone
from sqlalchemy.exc import InternalError

from .database import DBDiscussionSession
from .database.discussion_model import User, Group


class RootFactory():
    """
    Defines the ACL
    """
    __acl__ = [(Allow, Everyone, 'everybody'),
               (Allow, 'group:admins', ('admin', 'edit', 'use')),
               (Allow, 'group:authors', ('edit', 'use')),
               (Allow, 'group:users', 'use'),
               (Allow, 'group:special', 'use')]

    def __init__(self, _):
        pass


def groupfinder(nick, _):
    """
    Finds group for the user id in given request
    :param nick: current user id
    :param request: request
    :return: given group as list or empty list
    """
    log = logging.getLogger(__name__)
    log.debug("nick: %s", nick)
    try:
        user = DBDiscussionSession.query(User).filter_by(nickname=nick).first()
    except InternalError as i:
        log.error("%s", i)
        return []

    if user:
        group = DBDiscussionSession.query(Group).get(user.group_uid)
        if group:
            log.debug("return [group: %s]", group.name)
            return ['group:' + group.name]

    log.debug("return []")
    return []
