from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension as Zte

DBSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DBNewsSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
Base = declarative_base()
DBEngine = None
DBNewsEngine = None

class RootFactory(object):
	"""
	Defines the ACL
	"""
	__acl__ = [(Allow, Everyone, 'everybody'),
	           (Allow, 'group:admins', ('admin', 'edit', 'use')),
	           (Allow, 'group:editors', ('edit', 'use')),
	           (Allow, 'group:users', 'use')]

	def __init__(self, request):
		pass

def load_discussion_database(engine):
	DBEngine = engine
	DBSession.configure(bind=DBEngine)
	Base.metadata.bind = DBEngine
	Base.metadata.create_all(DBEngine)

def load_news_database(engine):
	DBNewsEngine = engine
	DBNewsSession.configure(bind=DBNewsEngine)
	Base.metadata.bind = DBNewsEngine
	Base.metadata.create_all(DBNewsEngine)