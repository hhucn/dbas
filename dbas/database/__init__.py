import sqlalchemy.orm as orm
from dbas.database.model import User, Group

from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension as Zte

# init thread safe handler
DBSession = orm.scoped_session(sessionmaker(extension=Zte()))
Base = declarative_base()


class RootFactory(object):
	"""
	Defines the ACL
	"""
	__acl__ = [(Allow, Everyone, 'everybody'), (Allow, 'group:editors', ('edit', 'use')), (Allow, 'group:users', 'use')]

	def __init__(self, request):
		pass

def load_database(engine):
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine
	Base.metadata.create_all(engine)
	try:
		session = DBSession()
		group1 = Group(name='editors')
		group2 = Group(name='users')
		session.add(group1)
		session.add(group2)
		session.flush()

		user1 = User(firstname='superuser', surename='superuser', nickname='superuser', email='', password='basic123')
		user2 = User(firstname='editor', surename='editor', nickname='editor', email='', password='test')
		user3 = User(firstname='user', surename='user', nickname='user', email='', password='test')
		user1.group = group1.uid
		user2.group = group1.uid
		user3.group = group1.uid
		session.add(user1)
		session.add(user2)
		session.add(user3)
		session.flush()

	except IntegrityError:
		pass


