from dbas.views import logger
from .database import DBSession
from .database.model import User, Group

def groupfinder(nick, request):
	"""
	Finds group for the user id in given request
	:param userid: current user id
	:param request: request
	:return: given group as list or empty list
	"""
	logger('security', 'groupfinder', 'parameter nick = ' + nick)
	user = DBSession.query(User).filter_by(nickname=nick).first()

	if (user):
		logger('security','groupfinder','nick is in group id ' + str(user.group_uid))
		group = DBSession.query(Group).filter_by(uid=user.group_uid).first()
		if (group):
			logger('security','groupfinder','return [group:' + group.name + ']')
			return ['group:' + group.name]

	logger('security', 'groupfinder', 'return []')
	return []