from pyramid.security import Allow, Everyone
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    firstname = Column(Text)
    surename = Column(Text)
    email = Column(Text)
    password = Column(Text)
    group = Column(Text)

    def __init__(self, firstname, surename, email, password, group):
        self.firstname = firstname
        self.surename = surename
        self.email = email
        self.password = password
        self.group = group

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit'),
                (Allow, 'group:editors', 'use'),
                (Allow, 'group:users', 'use') ]
    def __init__(self, request):
        pass
