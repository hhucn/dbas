USERS = {'editor':'editor',
         'viewer':'viewer',
         'user':'user'}
GROUPS = {'editor':['group:editors'],
          'viewer':['group:viewers'],
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
