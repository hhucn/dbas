from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension as Zte

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


DBDiscussionSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DBNewsSession       = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DBAPISession        = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DiscussionBase      = declarative_base()
NewsBase            = declarative_base()
APIBase             = declarative_base()
DBEngine            = None
DBNewsEngine        = None
DBAPIEngine         = None


def load_discussion_database(engine):
	db_discussion_engine = engine
	DBDiscussionSession.configure(bind=db_discussion_engine)
	DiscussionBase.metadata.bind = db_discussion_engine
	DiscussionBase.metadata.create_all(db_discussion_engine)


def load_news_database(engine):
	db_news_engine = engine
	DBNewsSession.configure(bind=db_news_engine)
	NewsBase.metadata.bind = db_news_engine
	NewsBase.metadata.create_all(db_news_engine)


def load_api_database(engine):
	db_api_engine = engine
	DBAPISession.configure(bind=db_api_engine)
	APIBase.metadata.bind = db_api_engine
	APIBase.metadata.create_all(db_api_engine)