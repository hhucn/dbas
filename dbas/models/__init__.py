import os
import transaction
import sqlalchemy as sa
import sqlalchemy.orm as orm

from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from zope.sqlalchemy import ZopeTransactionExtension as Zte
from hashlib import sha1

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


def load_database(db_string):
	engine = sa.create_engine(db_string, echo=True)
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine
	Base.metadata.create_all(engine)
	try:
		session = DBSession()
		user1 = User(firstname='superuser', surename='superuser', email='', password='basic123')
		user2 = User(firstname='editor', surename='editor', email='', password='test')
		user3 = User(firstname='user', surename='user', email='', password='test')
		group1 = Group('editors')
		group2 = Group('users')
		session.add(group1, group2)
		user1.group.append(group1, group2)
		user2.group.append(group1, group2)
		user3.group.append(group1, group2)
		session.add(user1, user2, user3)
		transaction.commit()
	except IntegrityError:
		pass


class Group(Base):
	"""
	group-table with several column.
	Each group has a name
	"""
	__tablename__ = 'groups'
	uid = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.Text, nullable=False, unique=True)

	def __init__(self, name):
		"""
		Initializes a row in current group-table
		"""
		self.name = name

	@classmethod
	def by_name(cls):
		"""Return a query of positions sorted by text."""
		return DBSession.query(Group).order_by(Group.name)


class User(Base):
	"""
	User-table with several columns.
	Each user has a firsstname, lastname, email, password, belongs to a group and has a last loggin date
	"""
	__tablename__ = 'users'
	uid = sa.Column(sa.Integer, primary_key=True)
	firstname = sa.Column(sa.Text, nullable=False)
	surename = sa.Column(sa.Text, nullable=False)
	email = sa.Column(sa.Text, nullable=False, unique=True)
	password = sa.Column(sa.Text, nullable=False)
	group = orm.relationship(Group, secondary='user_group')
	last_logged = sa.Column(sa.DateTime, default=func.now())

	def __init__(self, firstname, surename, email, password):
		"""
		Initializes a row in current user-table
		"""
		self.firstname = firstname
		self.surename = surename
		self.email = email
		self.password = password
		self.last_logged = func.now()

	@classmethod
	def by_surename(cls):
		"""Return a query of users sorted by surename."""
		return DBSession.query(User).order_by(User.surename)

	def _set_password(self, password):
		if isinstance(password, sa.Unicode):
			password_8bit = password.encode('UTF-8')
		else:
			password_8bit = password

		salt = sha1()
		salt.update(os.urandom(60))
		hash = sha1()
		hash.update(password_8bit + salt.hexdigest())
		hashed_password = salt.hexdigest() + hash.hexdigest()

		if not isinstance(hashed_password, sa.Unicode):
			hashed_password = hashed_password.decode('UTF-8')

		self.password = hashed_password

	def validate_password(self, password):
		hashed_pass = sha1()
		hashed_pass.update(password + self.password[:40])
		return self.password[40:] == hashed_pass.hexdigest()


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


class Position(Base):
	"""
	User-table with several columns.
	Each user has a firsstname, lastname, email, password, belongs to a group and has a last loggin date
	"""
	__tablename__ = 'positions'
	uid = sa.Column(sa.Integer, primary_key=True)
	text = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = orm.relationship(User, secondary='user_position')

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
	author = orm.relationship(User, secondary='user_argument')

	def __init__(self, text, weight,):
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
		return DBSession.query(Argument).filter(Argument.author==author)


class RelationArgPos(Base):
	"""
	Relation-table between position and arguments with several columns.
	Each relation has creation date, weight, author and a boolean whether it is supportive or attacking
	"""
	__tablename__ = 'relation_argpos'
	uid = sa.Column(sa.Integer, primary_key=True)
	arg_uid = orm.relationship(Argument, secondary='argument_position')
	pos_uid = orm.relationship(Position, secondary='argument_position')
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = orm.relationship(User, secondary='user_relation_argpos')
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
	arg_uid1 = orm.relationship(Argument, secondary='argument_position')
	pos_uid2 = orm.relationship(Argument, secondary='argument_position')
	date = sa.Column(sa.DateTime, default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)
	author = orm.relationship(User, secondary='user_relation_argarg')
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


user_group_table = sa.Table('user_group', Base.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(User.uid)),
    sa.Column('group_id', sa.Integer, sa.ForeignKey(Group.uid)),
)
user_position_table = sa.Table('user_position', Base.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(User.uid)),
    sa.Column('position_id', sa.Integer, sa.ForeignKey(Position.uid)),
)
user_argument_table = sa.Table('user_argument', Base.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(User.uid)),
    sa.Column('argument_id', sa.Integer, sa.ForeignKey(Argument.uid)),
)
user_relation_argarg_table = sa.Table('user_relation_argarg', Base.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(User.uid)),
    sa.Column('relation_argarg_id', sa.Integer, sa.ForeignKey(RelationArgArg.uid)),
)
user_relation_argpos_table = sa.Table('user_relation_argpos', Base.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey(User.uid)),
    sa.Column('relation_argpos_id', sa.Integer, sa.ForeignKey(RelationArgPos.uid)),
)
argument_argument_table = sa.Table('argument_argument', Base.metadata,
    sa.Column('argument_id', sa.Integer, sa.ForeignKey(Argument.uid)),
    sa.Column('argument_id', sa.Integer, sa.ForeignKey(Argument.uid)),
)
argument_position_table = sa.Table('argument_position', Base.metadata,
    sa.Column('argument_id', sa.Integer, sa.ForeignKey(Argument.uid)),
    sa.Column('position_id', sa.Integer, sa.ForeignKey(Position.uid)),
)