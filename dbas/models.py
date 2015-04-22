from pyramid.security import Allow, Everyone
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
from zope.sqlalchemy import ZopeTransactionExtension

# init thread safe handler
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
	'''
	User-class with several arguments
	'''
	__tablename__ = 'users'
	uid = Column(Integer, primary_key=True)
	firstname = Column(Text, nullable=False)
	surename = Column(Text, nullable=False)
	email = Column(Text, nullable=False)
	password = Column(Text, nullable=False)
	group = Column(Text, nullable=False)
	last_logged = Column(DateTime, default=func.now())

	def __init__(self, firstname, surename, email, password, group):
		self.firstname = firstname
		self.surename = surename
		self.email = email
		self.password = password
		self.group = group
		self.last_logged = func.now()

#class Position(Base):
#	__tablename__ = 'positions'
#	uid = Column(Integer, primary_key=True)
#	text = Column(Text, nullable=False)
#	date = Column(DateTime, default=func.now())
#	weight = Column(Integer, nullable=False)
#	author_id = Column(Integer, nullable=False)
#
#	def __init__(self, text, date, weight, author_id):
#		self.text = text
#		self.date = date
#		self.weight = weight
#		self.author_id = author_id

#class Argument(Base):
#	__tablename__ = 'arguments'
#	uid = Column(Integer, primary_key=True)
#	text = Column(Text, nullable=False)
#	date = Column(DateTime, default=func.now())
#	weight = Column(Integer, nullable=False)
#	author_id = Column(Integer, nullable=False)
#
#	def __init__(self, text, date, weight, author_id):
#		self.text = text
#		self.date = date
#		self.weight = weight
#		self.author_id = author_id


class RootFactory(object):
	'''
	Defines the ACL
	'''
	__acl__ = [ (Allow, Everyone, 'view'),
	            (Allow, 'group:editors', 'edit'),
                (Allow, 'group:editors', 'use'),
                (Allow, 'group:users', 'use') ]
	def __init__(self, request):
		pass
