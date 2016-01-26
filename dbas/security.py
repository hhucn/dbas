from pyramid.security import Allow, Everyone
from dbas.views import logger
from .database import DBDiscussionSession
from .database.discussion_model import User, Group

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

class RootFactory(object):
	"""
	Defines the ACL
	"""
	__acl__ = [(Allow, Everyone, 'everybody'),
	           (Allow, 'group:admins', ('admin', 'edit', 'use')),
	           (Allow, 'group:authors', ('edit', 'use')),
	           (Allow, 'group:editors', ('edit', 'use')),
	           (Allow, 'group:users', 'use')]

	def __init__(self, request):
		pass


def groupfinder(nick, request):
	"""
	Finds group for the user id in given request
	:param userid: current user id
	:param request: request
	:return: given group as list or empty list
	"""
	logger('security', 'groupfinder', 'parameter nick = ' + nick)
	user = DBDiscussionSession.query(User).filter_by(nickname=nick).first()

	if (user):
		logger('security','groupfinder','nick is in group id ' + str(user.group_uid))
		group = DBDiscussionSession.query(Group).filter_by(uid=user.group_uid).first()
		if (group):
			logger('security','groupfinder','return [group:' + group.name + ']')
			return ['group:' + group.name]

	logger('security', 'groupfinder', 'return []')
	return []