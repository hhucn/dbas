import sqlalchemy as sa

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from dbas.database import DBSession, Base

# ORM Relationships
# Statement : Text              many-to-one     fk on the parent referencing the child, relationship() on the parent
# Statement : Author            many-to-one
# Statement : Premisses         many-to-one
# PremisseGroups : Author       many-to-one
# Argument : Statement          many-to-one
# Argument : Author             many-to-one
# Premisses : Author            many-to-one
# TextValue : TextVersions      one-to-many     fk on the child referencing the parent, relationship() on the parent
# Author : TextVersions         one-to-many
# PremisseGroups : Premisses    one-to-many
# Track : Author                one-to-many
# Track : Statement             one-to-many
# Argument : PremisseGroups     many-to-many    association tables
# Argument : Argument           many-to-many    adjacency list relationship


class Issue(Base):
	"""
	issue-table with several column.
	Each issue has text and a creation date
	"""
	__tablename__ = 'issue'
	uid = sa.Column(sa.Integer, primary_key=True)
	text = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime(timezone=True), default=func.now())

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
	gender = sa.Column(sa.Text, nullable=False)
	password = sa.Column(sa.Text, nullable=False)
	group_uid = sa.Column(sa.Integer, sa.ForeignKey('groups.uid'))
	last_action = sa.Column(sa.DateTime(timezone=True), default=func.now())
	last_login = sa.Column(sa.DateTime(timezone=True), default=func.now())
	registered = sa.Column(sa.DateTime(timezone=True), default=func.now())

	groups = relationship('Group', foreign_keys=[group_uid], order_by='Group.uid')

	def __init__(self, group, firstname, surname, nickname, email, password, gender):
		"""
		Initializes a row in current user-table
		"""
		self.firstname = firstname
		self.surname = surname
		self.nickname = nickname
		self.email = email
		self.gender = gender
		self.password = password
		self.group_uid = group
		self.last_action = func.now()
		self.last_login = func.now()
		self.registered = func.now()

	@classmethod
	def by_surname(cls):
		"""Return a query of users sorted by surname."""
		return DBSession.query(User).order_by(User.surname)

	def validate_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.check(self.password, password)

	def update_last_logged(self):
		self.last_login = func.now()

	def update_last_action(self):
		self.last_action = func.now()


class Statement(Base):
	"""
	Statement-table with several columns.
	Each statement has link to its text
	"""
	__tablename__ = 'statements'
	uid = sa.Column(sa.Integer, primary_key=True)
	text_uid = sa.Column(sa.Integer, sa.ForeignKey('textvalues.uid'))
	isStartpoint = sa.Column(sa.Boolean, nullable=False)

	textvalues = relationship('TextValue', foreign_keys=[text_uid])

	def __init__(self, text, isstartpoint):
		"""
		Initializes a row in current statement-table
		"""
		self.text_uid = text
		self.isStartpoint = isstartpoint


class TextValue(Base):
	"""
	Text-Value-table with several columns.
	Each text value has a link to its most recent text value and a weight
	"""
	__tablename__ = 'textvalues'
	uid = sa.Column(sa.Integer, primary_key=True)
	textVersion_uid = sa.Column(sa.Integer, sa.ForeignKey('textversions.uid'))

	textversions = relationship('TextVersion', foreign_keys=[textVersion_uid])

	def __init__(self, textversion):
		"""
		Initializes a row in current text-value-table
		"""
		self.textVersion_uid = textversion

	def update_textversion(self, textVersion_uid):
		self.textVersion_uid = textVersion_uid


class TextVersion(Base):
	"""
	TextVersions-table with several columns.
	Each text versions has link to the recent link and fields for content, author, timestamp and weight
	"""
	__tablename__ = 'textversions'
	uid = sa.Column(sa.Integer, primary_key=True)
	textValue_uid = sa.Column(sa.Integer, sa.ForeignKey('textvalues.uid'), nullable=True)
	content = sa.Column(sa.Text, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)

	textvalues = relationship('TextValue', foreign_keys=[textValue_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, content, author, weight):
		"""
		Initializes a row in current text versions-table
		"""
		self.content = content
		self.author_uid = author
		self.weight = weight
		self.timestamp = func.now()

	def set_textvalue(self, value):
		self.textValue_uid = value

	@classmethod
	def by_timestamp(cls):
		"""Return a query of text versions sorted by timestamp."""
		return DBSession.query(TextVersion).order_by(TextVersion.timestamp)

	@classmethod
	def by_weight(cls):
		"""Return a query of text versions sorted by wight."""
		return DBSession.query(TextVersion).order_by(TextVersion.weight)


class PremisseGroup(Base):
	"""
	PremisseGroup-table with several columns.
	Each premissesGroup has a id and an author
	"""
	__tablename__ = 'premissegroups'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, author):
		"""
		Initializes a row in current premissesGroup-table
		"""
		self.author_uid = author


class Premisse(Base):
	"""
	Premisses-table with several columns.
	Each premisses has a value pair of group and statement, an author, a timestamp as well as a boolean whether it is negated
	"""
	__tablename__ = 'premisses'
	premissesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premissegroups.uid'), primary_key=True)
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'), primary_key=True)
	isNegated = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())

	premissegroups = relationship('PremisseGroup', foreign_keys=[premissesGroup_uid])
	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, premissesgroup, statement, isnegated, author):
		"""
		Initializes a row in current premisses-table
		"""
		self.premissesGroup_uid = premissesgroup
		self.statement_uid = statement
		self.isNegated = isnegated
		self.author_uid = author
		self.timestamp = func.now()


class Argument(Base):
	"""
	Argument-table with several columns.
	Each argument has justifying statement(s) (premisses) and the the statement-to-be-justified (argument or statement).
	Additionally there is a relation, timestamp, author, weight, ...
	"""
	__tablename__ = 'arguments'
	uid = sa.Column(sa.Integer, primary_key=True)
	premissesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premissegroups.uid'))
	conclusion_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'))
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey('arguments.uid'))
	isSupportive = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey(User.uid))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	weight = sa.Column(sa.Integer, nullable=False)

	premissegroups = relationship('PremisseGroup', foreign_keys=[premissesGroup_uid])
	statements = relationship('Statement', foreign_keys=[conclusion_uid])
	users = relationship('User', foreign_keys=[author_uid])
	arguments = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid)  # TODO

	def __init__(self, premissegroup, issupportive, author, weight, conclusion=0):
		"""
		Initializes a row in current argument-table
		"""
		self.premissesGroup_uid = premissegroup
		self.conclusion_uid = conclusion
		self.argument_uid = None
		self.isSupportive = issupportive
		self.author_uid = author
		self.weight = weight
		self.argument_uid = 0

	def conclusions_argument(self, argument):
		self.argument_uid = argument


class Track(Base):
	"""
	Track-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'track'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'))
	premissesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premissegroups.uid'))
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey('arguments.uid'))
	attacked_by_relation = sa.Column(sa.Integer, sa.ForeignKey('relation.uid'))
	attacked_with_relation = sa.Column(sa.Integer, sa.ForeignKey('relation.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())

	users = relationship('User', foreign_keys=[author_uid])
	statements = relationship('Statement', foreign_keys=[statement_uid])
	premissegroups = relationship('PremisseGroup', foreign_keys=[premissesGroup_uid])
	arguments = relationship('Argument', foreign_keys=[argument_uid])
	attacked_by = relationship('Relation', foreign_keys=[attacked_by_relation])
	attacked_with = relationship('Relation', foreign_keys=[attacked_with_relation])

	def __init__(self, user, statement, premissegroup=0, argument=0, attacked_by=0, attacked_with=0):
		"""
		Initializes a row in current track-table
		"""
		self.author_uid = user
		self.statement_uid = statement
		self.premissesGroup_uid = premissegroup
		self.argument_uid = argument
		self.attacked_by_relation = attacked_by
		self.attacked_with_relation = attacked_with
		self.timestamp = func.now()


class Relation(Base):
	"""
	Relation-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'relation'
	uid = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.Text, nullable=False)

	def __init__(self, name):
		"""
		Initializes a row in current relation-table
		"""
		self.name = name
