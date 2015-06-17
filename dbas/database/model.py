import os
import sqlalchemy as sa

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.sql import func
from dbas.database import DBSession, Base


class Issue(Base):
	"""
	issue-table with several column.
	Each issue has text and a creation date
	"""
	__tablename__ = 'issue'
	uid = sa.Column(sa.Integer, primary_key=True)
	text = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime, default=func.now())

	def __init__(self, text):
		"""
		Initializes a row in current position-table
		"""
		self.text = text

	@classmethod
	def by_text(cls):
		"""Return a query of positions sorted by text."""
		return DBSession.query(Issue).order_by(Issue.text)


class Group(Base):
	"""
	group-table with several column.
	Each group has a name
	"""
	__tablename__ = 'groups'
	uid = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.Text, nullable=False, unique=True)

	#author = orm.relationship("User", backref=__tablename__) # one-to-many

	def __init__(self, name):
		"""
		Initializes a row in current group-table
		"""
		self.name = name

	@classmethod
	def by_name(cls):
		"""Return a query of positions sorted by text."""
		return DBSession.query(Group).order_by(Group.name)

	def group_by_id(group):
		return DBSession.query(Group).filter(Group.name == group).first()


class User(Base):
	"""
	User-table with several columns.
	Each user has a firsstname, lastname, email, password, belongs to a group and has a last loggin date
	"""
	__tablename__ = 'users'
	uid = sa.Column(sa.Integer, primary_key=True)
	firstname = sa.Column(sa.Text, nullable=False)
	surname = sa.Column(sa.Text, nullable=False)
	nickname = sa.Column(sa.Text, nullable=False)
	email = sa.Column(sa.Text, nullable=False, unique=True)
	password = sa.Column(sa.Text, nullable=False)
	group = sa.Column(sa.Integer, sa.ForeignKey(Group.uid))
	last_logged = sa.Column(sa.DateTime, default=func.now())
	registered = sa.Column(sa.DateTime, default=func.now())

	def __init__(self, firstname, surname, nickname, email, password):
		"""
		Initializes a row in current user-table
		"""
		self.firstname = firstname
		self.surname = surname
		self.nickname = nickname
		self.email = email
		self.password = password
		self.last_logged = func.now()

	@classmethod
	def by_surname(cls):
		"""Return a query of users sorted by surname."""
		return DBSession.query(User).order_by(User.surname)

	def validate_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.check(self.password, password)

	def update_last_logged(self):
		self.last_logged = func.now()


class Position(Base):
	"""
	Position-table with several columns.
	Each position hast text, date, weight, author
	"""
	__tablename__ = 'positions'
	uid = sa.Column(sa.Integer, primary_key=True)
	text = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = sa.Column(sa.Integer, sa.ForeignKey(User.uid))

	def __init__(self, text, weight):
		"""
		Initializes a row in current position-table
		"""
		self.text = text
		self.weight = weight

	@classmethod
	def by_text(cls):
		"""Return a query of positions sorted by text."""
		return DBSession.query(Position).order_by(Position.text)


class Argument(Base):
	"""
	Argument-table with several columns.
	Each argument has text, creation date, weight and a author
	"""
	__tablename__ = 'arguments'
	uid = sa.Column(sa.Integer, primary_key=True)
	text = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = sa.Column(sa.Integer, sa.ForeignKey(User.uid))

	def __init__(self, text, weight, ):
		"""
		Initializes a row in current argument-table
		"""
		self.text = text
		self.weight = weight

	@classmethod
	def by_text(cls):
		"""Return a query of arguments sorted by text."""
		return DBSession.query(Argument).order_by(Argument.text)

	@classmethod
	def by_date(cls):
		"""Return a query of arguments sorted by text."""
		return DBSession.query(Argument).order_by(Argument.date)

	@classmethod
	def by_authorid(cls, author):
		"""Return a query of arguments sorted by authorid."""
		return DBSession.query(Argument).filter(Argument.author == author)


class RelationArgPos(Base):
	"""
	Relation-table between position and arguments with several columns.
	Each relation has creation date, weight, author and a boolean whether it is supportive or attacking
	"""
	__tablename__ = 'relation_argpos'
	uid = sa.Column(sa.Integer, primary_key=True)
	arg_uid = sa.Column(sa.Integer, sa.ForeignKey(Argument.uid))
	pos_uid = sa.Column(sa.Integer, sa.ForeignKey(Position.uid))
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	is_supportive = sa.Column(sa.Boolean, nullable=False)

	def __init__(self, weight, is_supportive):
		"""
		Initializes a row in current relation-table
		"""
		self.weight = weight
		self.is_supportive = is_supportive

	@classmethod
	def by_date(cls):
		"""Return a query of positions sorted by date."""
		return DBSession.query(RelationArgPos).order_by(RelationArgPos.date)


class RelationPosArg(Base):
	"""
	Relation-table between arguments and position with several columns.
	Each relation has creation date, weight, author and a boolean whether it is supportive or attacking
	"""
	__tablename__ = 'relation_posarg'
	uid = sa.Column(sa.Integer, primary_key=True)
	pos_uid = sa.Column(sa.Integer, sa.ForeignKey(Position.uid))
	arg_uid = sa.Column(sa.Integer, sa.ForeignKey(Argument.uid))
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	is_supportive = sa.Column(sa.Boolean, nullable=False)

	def __init__(self, weight, is_supportive):
		"""
		Initializes a row in current relation-table
		"""
		self.weight = weight
		self.is_supportive = is_supportive

	@classmethod
	def by_date(cls):
		"""Return a query of positions sorted by date."""
		return DBSession.query(RelationArgPos).order_by(RelationArgPos.date)


class RelationArgArg(Base):
	"""
	Relation-table between argument with several columns.
	Each relation has creation date, weight, author and a boolean whether it is supportive or attacking
	"""
	__tablename__ = 'relation_argarg'
	uid = sa.Column(sa.Integer, primary_key=True)
	arg_uid1 = sa.Column(sa.Integer, sa.ForeignKey(Argument.uid))
	arg_uid2 = sa.Column(sa.Integer, sa.ForeignKey(Argument.uid))
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	is_supportive = sa.Column(sa.Boolean, nullable=False)

	def __init__(self, weight, is_supportive):
		"""
		Initializes a row in current relation-table
		"""
		self.weight = weight
		self.is_supportive = is_supportive

	@classmethod
	def by_date(cls):
		"""Return a query of positions sorted by date."""
		return DBSession.query(RelationArgArg).order_by(RelationArgArg.date)


class RelationPosPos(Base):
	"""
	Relation-table between positions with several columns.
	Each relation has creation date, weight, author and a boolean whether it is supportive or attacking
	"""
	__tablename__ = 'relation_pospos'
	uid = sa.Column(sa.Integer, primary_key=True)
	pos_uid1 = sa.Column(sa.Integer, sa.ForeignKey(Position.uid))
	pos_uid2 = sa.Column(sa.Integer, sa.ForeignKey(Position.uid))
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	is_supportive = sa.Column(sa.Boolean, nullable=False)

	def __init__(self, weight, is_supportive):
		"""
		Initializes a row in current relation-table
		"""
		self.weight = weight
		self.is_supportive = is_supportive

	@classmethod
	def by_date(cls):
		"""Return a query of positions sorted by date."""
		return DBSession.query(RelationPosPos).order_by(RelationPosPos.date)


class Track(Base):
	"""
	Track-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'track'
	uid = sa.Column(sa.Integer, primary_key=True)
	user_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	date = sa.Column(sa.DateTime, default=func.now())
	pos_uid = sa.Column(sa.Integer, sa.ForeignKey(Position.uid))
	arg_uid = sa.Column(sa.Integer, sa.ForeignKey(Argument.uid))
	is_argument = sa.Column(sa.Boolean, nullable=False)

	def __init__(self, user_uid, pos_uid, arg_uid, is_argument):
		"""
		Initializes a row in current position-table
		"""
		self.user_uid = user_uid
		self.pos_uid = pos_uid
		self.arg_uid = arg_uid
		self.is_argument = is_argument
