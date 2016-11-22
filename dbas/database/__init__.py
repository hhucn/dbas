"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension as Zte

DBDiscussionSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False, autocommit=False))
DBNewsSession       = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False, autocommit=False))
DiscussionBase      = declarative_base()
NewsBase            = declarative_base()
DBEngine            = None
DBNewsEngine        = None


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
