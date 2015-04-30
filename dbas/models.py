from pyramid.security import Allow, Everyone
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
from zope.sqlalchemy import ZopeTransactionExtension

# init thread safe handler
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
	'''
	User-table with several columns.
	Each user has a firsstname, lastname, email, password, belongs to a group and has a last loggin date
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
		"""
		Initializes a row in current user-table
		"""
		self.firstname = firstname
		self.surename = surename
		self.email = email
		self.password = password
		self.group = group
		self.last_logged = func.now()

	@classmethod
	def by_surename(class_):
		"""Return a query of users sorted by surename."""
		User = class_
		q = DBSession.query(User)
		q = q.order_by(User.surename)
		return q

class Issue(Base):
	'''
	issue-table with one column.
	Each issue has text and a creation date
	'''
	__tablename__ = 'issue'
	uid = Column(Integer, primary_key=True)
	text = Column(Text, nullable=False)
	date = Column(DateTime, default=func.now())

	def __init__(self, text):
		"""
		Initializes a row in current position-table
		"""
		self.text = text


class Position(Base):
	'''
	User-table with several columns.
	Each user has a firsstname, lastname, email, password, belongs to a group and has a last loggin date
	'''
	__tablename__ = 'positions'
	uid = Column(Integer, primary_key=True)
	text = Column(Text, nullable=False)
	date = Column(DateTime, default=func.now())
	weight = Column(Integer, nullable=False)
	author_id = Column(Integer, nullable=False)

	def __init__(self, text, weight, author_id):
		"""
		Initializes a row in current position-table
		"""
		self.text = text
		self.weight = weight
		self.author_id = author_id

	@classmethod
	def by_text(class_):
		"""Return a query of positions sorted by text."""
		Position = class_
		q = DBSession.query(Position)
		q = q.order_by(Position.text)
		return q


class Argument(Base):
	'''
	Argument-table with several columns.
	Each argument has text, creation date, weight and a author_id
	'''
	__tablename__ = 'arguments'
	uid = Column(Integer, primary_key=True)
	text = Column(Text, nullable=False)
	date = Column(DateTime, default=func.now())
	weight = Column(Integer, nullable=False)
	author_id = Column(Integer, nullable=False)

	def __init__(self, text, weight, author_id):
		"""
		Initializes a row in current argument-table
		"""
		self.text = text
		self.weight = weight
		self.author_id = author_id

	@classmethod
	def by_text(class_):
		"""Return a query of arguments sorted by text."""
		Argument = class_
		q = DBSession.query(Argument)
		q = q.order_by(Argument.text)
		return q


class RelationPosArg(Base):
	'''
	Relation-table between position and arguments with several columns.
	Each relation has creation date, weight, author_id and a boolean whether it is supportive or attacking
	'''
	__tablename__ = 'relation_posarg'
	uid = Column(Integer, primary_key=True)
	arg_uid = Column(Integer, ForeignKey('arguments.uid'), nullable=False)
	pos_uid = Column(Integer, ForeignKey('positions.uid'), nullable=False)
	date = Column(DateTime, default=func.now())
	weight = Column(Integer, nullable=False)
	author_id = Column(Integer, nullable=False)
	is_supportive = Column(Boolean, nullable=False)

	def __init__(self, arg_uid, pos_uid, weight, author_id, is_supportive):
		"""
		Initializes a row in current relation-table
		"""
		self.arg_uid = arg_uid
		self.pos_uid = pos_uid
		self.weight = weight
		self.author_id = author_id
		self.is_supportive = is_supportive

	@classmethod
	def by_date(class_):
		"""Return a query of positions sorted by date."""
		RelationPosArg = class_
		q = DBSession.query(RelationPosArg)
		q = q.order_by(RelationPosArg.date)
		return q

class RelationArgArg(Base):
	'''
	Relation-table between argument with several columns.
	Each relation has creation date, weight, author_id and a boolean whether it is supportive or attacking
	'''
	__tablename__ = 'relation_argarg'
	uid = Column(Integer, primary_key=True)
	arg_uid1 = Column(Integer, ForeignKey('arguments.uid'), nullable=False)
	arg_uid2 = Column(Integer, ForeignKey('arguments.uid'), nullable=False)
	date = Column(DateTime, default=func.now())
	weight = Column(Integer, nullable=False)
	author_id = Column(Integer, nullable=False)
	is_supportive = Column(Boolean, nullable=False)

	def __init__(self, arg_uid1, arg_uid2, weight, author_id, is_supportive):
		"""
		Initializes a row in current relation-table
		"""
		self.arg_uid1 = arg_uid1
		self.arg_uid2 = arg_uid2
		self.weight = weight
		self.author_id = author_id
		self.is_supportive = is_supportive

	@classmethod
	def by_date(class_):
		"""Return a query of positions sorted by date."""
		RelationArgArg = class_
		q = DBSession.query(RelationArgArg)
		q = q.order_by(RelationArgArg.date)
		return q



class RootFactory(object):
	'''
	Defines the ACL
	'''
	#(Allow, Everyone, 'use'),
	__acl__ = [ (Allow, 'group:editors', 'edit'),
                (Allow, 'group:editors', 'use'),
                (Allow, 'group:users', 'use') ]
	def __init__(self, request):
		pass
