from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension as Zte

DBSession = scoped_session(sessionmaker(extension=Zte()))
Base = declarative_base()

class RootFactory(object):
	"""
	Defines the ACL
	"""
	__acl__ = [(Allow, Everyone, 'everybody'), (Allow, 'group:editors', ('edit', 'use')), (Allow, 'group:users', 'use')]

	def __init__(self, request):
		pass

def load_database(engine):
	DBEngine = engine;
	DBSession.configure(bind=DBEngine)
	Base.metadata.bind = DBEngine
	Base.metadata.create_all(DBEngine)
	#try:
	#	session = DBSession()
	#	group1 = Group(name='editors')
	#	group2 = Group(name='users')
	#	session.add(group1)
	#	session.add(group2)
	#	session.flush()

	#	user1 = User(firstname='superuser', surname='superuser', nickname='superuser', email='', password='basic123')
	#	user2 = User(firstname='editor', surname='editor', nickname='editor', email='', password='test')
	#	user3 = User(firstname='user', surname='user', nickname='user', email='', password='test')
	#	user1.group = group1.uid
	#	user2.group = group1.uid
	#	user3.group = group1.uid
	#	session.add_all([user1, user2, user3])
	#	session.flush()

	#except IntegrityError:
	#	pass


