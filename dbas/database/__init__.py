from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension as Zte

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

DBDiscussionSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DBNewsSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DiscussionBase = declarative_base()
NewsBase = declarative_base()
DBEngine = None
DBNewsEngine = None

def load_discussion_database(engine):
	DBEngine = engine
	DBDiscussionSession.configure(bind=DBEngine)
	DiscussionBase.metadata.bind = DBEngine
	DiscussionBase.metadata.create_all(DBEngine)

def load_news_database(engine):
	DBNewsEngine = engine
	DBNewsSession.configure(bind=DBNewsEngine)
	NewsBase.metadata.bind = DBNewsEngine
	NewsBase.metadata.create_all(DBNewsEngine)