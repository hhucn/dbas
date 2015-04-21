USERS = {'editor':'editor',
         'viewer':'viewer',
         'user':'user'}
GROUPS = {'editor':['group:editors'],
          'viewer':['group:viewers'],
          'user':['group:users']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
