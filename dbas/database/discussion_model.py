import sqlalchemy as sa

from slugify import slugify

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from dbas.database import DBDiscussionSession, DiscussionBase

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015-2016


class Issue(DiscussionBase):
	"""
	issue-table with several column.
	Each issue has text and a creation date
	"""
	__tablename__ = 'issues'
	uid = sa.Column(sa.Integer, primary_key=True)
	title = sa.Column(sa.Text, nullable=False)
	info = sa.Column(sa.Text, nullable=False)
	date = sa.Column(sa.DateTime(timezone=True), default=func.now())

	def __init__(self, title, info):
		"""
		Initializes a row in current position-table
		"""
		self.title = title
		self.info = info

	@classmethod
	def by_text(cls):
		"""Return a query of positions sorted by text."""
		return DBDiscussionSession.query(Issue).order_by(Issue.text)

	def get_slug(self):
		return slugify(self.title)


class Group(DiscussionBase):
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
		return DBDiscussionSession.query(Group).order_by(Group.name)


class User(DiscussionBase):
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

	def __init__(self, firstname, surname, nickname, email, password, gender, group=0):
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
		return DBDiscussionSession.query(User).order_by(User.surname)

	def validate_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.check(self.password, password)

	def update_last_logged(self):
		self.last_login = func.now()

	def update_last_action(self):
		self.last_action = func.now()


class Statement(DiscussionBase):
	"""
	Statement-table with several columns.
	Each statement has link to its text
	"""
	__tablename__ = 'statements'
	uid = sa.Column(sa.Integer, primary_key=True)
	textversion_uid = sa.Column(sa.Integer, sa.ForeignKey('textversions.uid'))
	is_startpoint = sa.Column(sa.Boolean, nullable=False)
	issue_uid = sa.Column(sa.Integer, sa.ForeignKey('issues.uid'))

	textversions = relationship('TextVersion', foreign_keys=[textversion_uid])
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, textversion, isstartpoint, issue=0):
		"""
		Initializes a row in current statement-table
		:param text:
		:param isstartpoint:
		:param issue:
		:return:
		"""
		self.textversion_uid = textversion
		self.is_startpoint = isstartpoint
		self.issue_uid = issue
		self.weight_uid = 0

	def set_textversion(self, uid):
		self.textversion_uid = uid


class TextVersion(DiscussionBase):
	"""
	TextVersions-table with several columns.
	Each text versions has link to the recent link and fields for content, author, timestamp and weight
	"""
	__tablename__ = 'textversions'
	uid = sa.Column(sa.Integer, primary_key=True)
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'), nullable=True)
	content = sa.Column(sa.Text, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())

	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, content, author):
		"""
		Initializes a row in current text versions-table
		:param content:
		:param author:
		:return:
		"""
		self.content = content
		self.author_uid = author
		self.timestamp = func.now()

	def set_statement(self, value):
		self.statement_uid = value

	@classmethod
	def by_timestamp(cls):
		"""Return a query of text versions sorted by timestamp."""
		return DBDiscussionSession.query(TextVersion).order_by(TextVersion.timestamp)


class PremiseGroup(DiscussionBase):
	"""
	PremiseGroup-table with several columns.
	Each premisesGroup has a id and an author
	"""
	__tablename__ = 'premisegroups'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))

	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, author):
		"""
		Initializes a row in current premisesGroup-table
		:param author:
		:return:
		"""
		self.author_uid = author


class Premise(DiscussionBase):
	"""
	Premises-table with several columns.
	Each premises has a value pair of group and statement, an author, a timestamp as well as a boolean whether it is negated
	"""
	__tablename__ = 'premises'
	premisesgroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premisegroups.uid'), primary_key=True)
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'), primary_key=True)
	is_negated = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	issue_uid = sa.Column(sa.Integer, sa.ForeignKey('issues.uid'))

	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesgroup_uid])
	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, premisesgroup, statement, isnegated, author, issue):
		"""
		Initializes a row in current premises-table
		:param premisesgroup:
		:param statement:
		:param isnegated:
		:param author:
		:param issue:
		:return:
		"""
		self.premisesgroup_uid = premisesgroup
		self.statement_uid = statement
		self.is_negated = isnegated
		self.author_uid = author
		self.timestamp = func.now()
		self.issue_uid = issue


class Argument(DiscussionBase):
	"""
	Argument-table with several columns.
	Each argument has justifying statement(s) (premises) and the the statement-to-be-justified (argument or statement).
	Additionally there is a relation, timestamp, author, weight, ...
	"""
	__tablename__ = 'arguments'
	uid = sa.Column(sa.Integer, primary_key=True)
	premisesgroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premisegroups.uid'))
	conclusion_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'))
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey('arguments.uid'))
	is_supportive = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	issue_uid = sa.Column(sa.Integer, sa.ForeignKey('issues.uid'))

	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesgroup_uid])
	statements = relationship('Statement', foreign_keys=[conclusion_uid])
	users = relationship('User', foreign_keys=[author_uid])
	arguments = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid)
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, premisegroup, issupportive, author, issue, conclusion=0):
		"""
		Initializes a row in current argument-table
		:param premisegroup:
		:param issupportive:
		:param author:
		:param issue:
		:param conclusion:
		:return:
		"""
		self.premisesgroup_uid = premisegroup
		self.conclusion_uid = conclusion
		self.argument_uid = None
		self.is_supportive = issupportive
		self.author_uid = author
		self.argument_uid = 0
		self.issue_uid = issue

	def conclusions_argument(self, argument):
		self.argument_uid = argument


class History(DiscussionBase):
	"""
	History-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'history'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	url = sa.Column(sa.Text, nullable=False)
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	session_id = sa.Column(sa.Integer)

	def __init__(self, user, url, session_id=0):
		"""
		Initializes a row in current history-table
		:param user:
		:param url:
		:param session_id:
		:return:
		"""
		self.author_uid = user
		self.url = url
		self.timestamp = func.now()
		self.session_id = session_id


class Vote(DiscussionBase):
	"""
	Vote-table with several columns.
	The combination of the both FK is a PK
	"""
	__tablename__ = 'votes'
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey('arguments.uid'), primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'), primary_key=True)
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	is_up_vote = sa.Column(sa.Boolean, nullable=False)
	is_valid = sa.Column(sa.Boolean, nullable=False)

	arguments = relationship('Argument', foreign_keys=[argument_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, argument_uid=0, author_uid=0, is_up_vote=True, is_valid=True):
		"""
		Initializes a row
		:param weight_uid:
		:param author_uid:
		:return:
		"""
		self.argument_uid = argument_uid
		self.author_uid = author_uid
		self.is_up_vote = is_up_vote
		self.timestamp = func.now()
		self.is_valid = is_valid

	def set_up_vote(self, is_up_vote):
		"""
		Sets up/down vote of this record
		:param is_up_vote: boolean
		:return: None
		"""
		self.is_up_vote = is_up_vote

	def set_valid(self, is_valid):
		"""
		Sets validity of this record
		:param is_valid: boolean
		:return: None
		"""
		self.is_valid = is_valid

	def update_timestamp(self):
		"""
		Updates timestamp of this record
		:return: None
		"""
		self.timestamp = func.now()
