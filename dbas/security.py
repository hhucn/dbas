USERS = {'editor':'test',
         'user':'test'}
GROUPS = {'editor':['group:editors'],
          'user':['group:users']}

def groupfinder(userid, request):
	'''
	Will find group for the user id in given request
	:param userid: current user id
	:param request: request
	:return: given group or none
	'''
	if userid in USERS:
		return GROUPS.get(userid, [])
