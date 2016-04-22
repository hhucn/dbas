"""
D-BAS database Model

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""


from slugify import slugify
from sqlalchemy import func, Integer, Text, DateTime, Boolean, Column, ForeignKey
from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.orm import relationship
from dbas.database import DBDiscussionSession, DiscussionBase


class Issue(DiscussionBase):
	"""
	issue-table with several column.
	Each issue has text and a creation date
	"""
	__tablename__ = 'issues'
	uid = Column(Integer, primary_key=True)
	title = Column(Text, nullable=False)
	info = Column(Text, nullable=False)
	date = Column(DateTime(timezone=True), default=func.now())
	author_uid = Column(Integer, ForeignKey('users.uid'))

	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, title, info, author_uid):
		"""
		Initializes a row in current position-table
		"""
		self.title = title
		self.info = info
		self.author_uid = author_uid

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
	uid = Column(Integer, primary_key=True)
	name = Column(Text, nullable=False, unique=True)

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
	Each user has a firstname, lastname, email, password, belongs to a group and has a last login date
	"""
	__tablename__ = 'users'
	uid = Column(Integer, primary_key=True)
	firstname = Column(Text, nullable=False)
	surname = Column(Text, nullable=False)
	nickname = Column(Text, nullable=False)
	email = Column(Text, nullable=False, unique=True)
	gender = Column(Text, nullable=False)
	password = Column(Text, nullable=False)
	group_uid = Column(Integer, ForeignKey('groups.uid'))
	last_action = Column(DateTime(timezone=True), default=func.now())
	last_login = Column(DateTime(timezone=True), default=func.now())
	registered = Column(DateTime(timezone=True), default=func.now())
	token = Column(Text, nullable=True)
	token_timestamp = Column(DateTime(timezone=True), nullable=True)
	keep_logged_in = Column(Boolean, nullable=False)

	groups = relationship('Group', foreign_keys=[group_uid], order_by='Group.uid')

	def __init__(self, firstname, surname, nickname, email, password, gender, group, token='', token_timestamp=None, keep_logged_in=False):
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
		self.token = token
		self.token_timestamp = token_timestamp
		self.keep_logged_in = keep_logged_in

	@classmethod
	def by_surname(cls):
		"""Return a query of users sorted by surname."""
		return DBDiscussionSession.query(User).order_by(User.surname)

	def validate_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.check(self.password, password)

	def update_last_login(self):
		self.last_login = func.now()

	def update_last_action(self):
		self.last_action = func.now()

	def update_token_timestamp(self):
		self.token_timestamp = func.now()

	def set_token(self, token):
		self.token = token

	def should_hold_the_login(self, keep_logged_in):
		self.keep_logged_in = keep_logged_in


class Settings(DiscussionBase):
	"""
	Settings-table with several columns.
	"""
	__tablename__ = 'settings'
	author_uid = Column(Integer, ForeignKey('users.uid'), nullable=True, primary_key=True)
	should_send_mails = Column(Boolean, nullable=False)
	should_send_notifications = Column(Boolean, nullable=False)

	def __init__(self, author_uid, send_mails, send_notifications):
		"""
		Initializes a row in current settings-table
		"""
		self.author_uid = author_uid
		self.should_send_mails = send_mails
		self.should_send_notifications = send_notifications

	def set_send_mails(self, send_mails):
		self.should_send_mails = send_mails

	def set_send_notifications(self, send_notifications):
		self.should_send_notifications = send_notifications


class Statement(DiscussionBase):
	"""
	Statement-table with several columns.
	Each statement has link to its text
	"""
	__tablename__ = 'statements'
	uid = Column(Integer, primary_key=True)
	textversion_uid = Column(Integer, ForeignKey('textversions.uid'))
	is_startpoint = Column(Boolean, nullable=False)
	issue_uid = Column(Integer, ForeignKey('issues.uid'))

	textversions = relationship('TextVersion', foreign_keys=[textversion_uid])
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, textversion, is_startpoint, issue):
		"""

		:param textversion:
		:param is_startpoint:
		:param issue:
		:return:
		"""
		self.textversion_uid = textversion
		self.is_startpoint = is_startpoint
		self.issue_uid = issue
		self.weight_uid = 0

	def set_textversion(self, uid):
		self.textversion_uid = uid


class StatementReferences(DiscussionBase):
	"""
	From API: Reference to be stored and assigned to a statement.
	"""
	__tablename__ = 'statement_references'
	uid = Column(Integer, primary_key=True)
	reference = Column(Text, nullable=False)
	host = Column(Text, nullable=False)
	path = Column(Text, nullable=False)
	author_uid = Column(Integer, ForeignKey('users.uid'), nullable=False)
	statement_uid = Column(Integer, ForeignKey('statements.uid'), nullable=False)
	issue_uid = Column(Integer, ForeignKey('issues.uid'), nullable=False)
	created = Column(DateTime(timezone=True), default=func.now())

	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, reference, host, path, author_uid, statement_uid, issue_uid):
		"""
		Create Reference.

		:param reference:
		:param host:
		:param path:
		:param author_uid:
		:param statement_uid:
		:param issue_uid:
		:return:
		"""
		self.reference = reference
		self.host = host
		self.path = path
		self.author_uid = author_uid
		self.statement_uid = statement_uid
		self.issue_uid = issue_uid


class TextVersion(DiscussionBase):
	"""
	TextVersions-table with several columns.
	Each text versions has link to the recent link and fields for content, author, timestamp and weight
	"""
	__tablename__ = 'textversions'
	uid = Column(Integer, primary_key=True)
	statement_uid = Column(Integer, ForeignKey('statements.uid'), nullable=True)
	content = Column(Text, nullable=False)
	author_uid = Column(Integer, ForeignKey('users.uid'))
	timestamp = Column(DateTime(timezone=True), default=func.now())

	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, content, author, statement_uid=None):
		"""
		Initializes a row in current text versions-table
		:param content:
		:param author:
		:return:
		"""
		self.content = content
		self.author_uid = author
		self.timestamp = func.now()
		self.statement_uid = statement_uid

	def set_statement(self, statement_uid):
		"""

		:param statement_uid:
		:return:
		"""
		self.statement_uid = statement_uid


class PremiseGroup(DiscussionBase):
	"""
	PremiseGroup-table with several columns.
	Each premisesGroup has a id and an author
	"""
	__tablename__ = 'premisegroups'
	uid = Column(Integer, primary_key=True)
	author_uid = Column(Integer, ForeignKey('users.uid'))

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
	premisesgroup_uid = Column(Integer, ForeignKey('premisegroups.uid'), primary_key=True)
	statement_uid = Column(Integer, ForeignKey('statements.uid'), primary_key=True)
	is_negated = Column(Boolean, nullable=False)
	author_uid = Column(Integer, ForeignKey('users.uid'))
	timestamp = Column(DateTime(timezone=True), default=func.now())
	issue_uid = Column(Integer, ForeignKey('issues.uid'))

	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesgroup_uid])
	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, premisesgroup, statement, is_negated, author, issue):
		"""
		Initializes a row in current premises-table
		:param premisesgroup:
		:param statement:
		:param is_negated:
		:param author:
		:param issue:
		:return:
		"""
		self.premisesgroup_uid = premisesgroup
		self.statement_uid = statement
		self.is_negated = is_negated
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
	uid = Column(Integer, primary_key=True)
	premisesgroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
	conclusion_uid = Column(Integer, ForeignKey('statements.uid'), nullable=True)
	argument_uid = Column(Integer, ForeignKey('arguments.uid'), nullable=True)
	is_supportive = Column(Boolean, nullable=False)
	author_uid = Column(Integer, ForeignKey('users.uid'))
	timestamp = Column(DateTime(timezone=True), default=func.now())
	issue_uid = Column(Integer, ForeignKey('issues.uid'))

	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesgroup_uid])
	statements = relationship('Statement', foreign_keys=[conclusion_uid])
	users = relationship('User', foreign_keys=[author_uid])
	arguments = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid)
	issues = relationship('Issue', foreign_keys=[issue_uid])

	def __init__(self, premisegroup, issupportive, author, issue, conclusion=None, argument=None):
		"""
		Initializes a row in current argument-table
		:param premisegroup:
		:param issupportive:
		:param author:
		:param issue:
		:param conclusion: Default 0, which will be None
		:param argument: Default 0, which will be None
		:return:
		"""
		self.premisesgroup_uid = premisegroup
		self.conclusion_uid = None if conclusion == 0 else conclusion
		self.argument_uid = None if argument == 0 else argument
		self.is_supportive = issupportive
		self.author_uid = author
		self.argument_uid = argument
		self.issue_uid = issue

	def conclusions_argument(self, argument):
		self.argument_uid = None if argument == 0 else argument


class History(DiscussionBase):
	"""
	History-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'bubbles'
	uid = Column(Integer, primary_key=True)
	author_uid = Column(Integer, ForeignKey('users.uid'))
	path = Column(Text, nullable=False)
	timestamp = Column(DateTime(timezone=True), default=func.now())

	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, author_uid, path):
		"""

		:param author_uid:
		:param path:
		:return:
		"""
		self.author_uid = author_uid
		self.path = path


class VoteArgument(DiscussionBase):
	"""
	Vote-table with several columns for arguments.
	The combination of the both FK is a PK
	"""
	__tablename__ = 'vote_arguments'
	uid = Column(Integer, primary_key=True)
	argument_uid = Column(Integer, ForeignKey('arguments.uid'))
	author_uid = Column(Integer, ForeignKey('users.uid'))
	timestamp = Column(DateTime(timezone=True), default=func.now())
	is_up_vote = Column(Boolean, nullable=False)
	is_valid = Column(Boolean, nullable=False)

	arguments = relationship('Argument', foreign_keys=[argument_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, argument_uid, author_uid, is_up_vote=True, is_valid=True):
		"""

		:param argument_uid:
		:param author_uid:
		:param is_up_vote:
		:param is_valid:
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


class VoteStatement(DiscussionBase):
	"""
	Vote-table with several columns for statements.
	The combination of the both FK is a PK
	"""
	__tablename__ = 'vote_statements'
	uid = Column(Integer, primary_key=True)
	statement_uid = Column(Integer, ForeignKey('statements.uid'))
	author_uid = Column(Integer, ForeignKey('users.uid'))
	timestamp = Column(DateTime(timezone=True), default=func.now())
	is_up_vote = Column(Boolean, nullable=False)
	is_valid = Column(Boolean, nullable=False)

	statements = relationship('Statement', foreign_keys=[statement_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, statement_uid, author_uid, is_up_vote=True, is_valid=True):
		"""

		:param statement_uid:
		:param author_uid:
		:param is_up_vote:
		:param is_valid:
		:return:
		"""
		self.statement_uid = statement_uid
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


class Notification(DiscussionBase):
	"""

	"""
	__tablename__ = 'messages'
	uid = Column(Integer, primary_key=True)
	from_author_uid = Column(Integer, ForeignKey('users.uid'))
	to_author_uid = Column(Integer, ForeignKey('users.uid'))
	topic = Column(Text, nullable=False)
	content = Column(Text, nullable=False)
	timestamp = Column(DateTime(timezone=True), default=func.now())
	read = Column(Boolean, nullable=False)

	def __init__(self, from_author_uid, to_author_uid, topic, content):
		self.from_author_uid = from_author_uid
		self.to_author_uid = to_author_uid
		self.topic = topic
		self.content = content
		self.timestamp = func.now()
		self.read = False

	def set_read(self, was_read):
		"""
		Sets validity of this record.

		:param was_read: boolean
		:return: None
		"""
		self.read = was_read
