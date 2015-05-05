from dbas.views import logger
from dbas.database import DBSession, User, Group

def groupfinder(nick, request):
	'''
	Will find group for the user id in given request
	:param userid: current user id
	:param request: request
	:return: given group or none as list
	'''
	logger('security','groupfinder','parameter nick = ' + nick)
	DBUser = DBSession.query(User).filter_by(nickname=nick).first()
	if (DBUser):
		logger('security','groupfinder','nick is in group id ' + str(DBUser.group))
		DBGroup = DBSession.query(Group).filter_by(uid=DBUser.group).first()
		if (DBGroup):
			logger('security','groupfinder','return group name = group:' + DBGroup.name + '')
			return ['group:'+DBGroup.name]
	logger('security','groupfinder','return []')
	return []

# old function
# def groupfinder(userid, request):
# 	if userid in USERS:
#		return GROUPS.get(userid, [])
