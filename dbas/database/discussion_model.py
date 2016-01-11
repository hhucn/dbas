import sqlalchemy as sa

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
		return DBDiscussionSession.query(Issue).order_by(Issue.text)


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

	def group_by_id(group):
		return DBDiscussionSession.query(Group).filter(Group.name == group).first()


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
	isStartpoint = sa.Column(sa.Boolean, nullable=False)
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
		self.isStartpoint = isstartpoint
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
	premisesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premisegroups.uid'), primary_key=True)
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'), primary_key=True)
	isNegated = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	issue_uid = sa.Column(sa.Integer, sa.ForeignKey('issues.uid'))

	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesGroup_uid])
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
		self.premisesGroup_uid = premisesgroup
		self.statement_uid = statement
		self.isNegated = isnegated
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
	premisesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premisegroups.uid'))
	conclusion_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'))
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey('arguments.uid'))
	isSupportive = sa.Column(sa.Boolean, nullable=False)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	issue_uid = sa.Column(sa.Integer, sa.ForeignKey('issues.uid'))
	weight_uid = sa.Column(sa.Integer, sa.ForeignKey('weights.uid'))

	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesGroup_uid])
	statements = relationship('Statement', foreign_keys=[conclusion_uid])
	users = relationship('User', foreign_keys=[author_uid])
	arguments = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid)
	issues = relationship('Issue', foreign_keys=[issue_uid])
	weights = relationship('Weight', foreign_keys=[weight_uid])

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
		self.premisesGroup_uid = premisegroup
		self.conclusion_uid = conclusion
		self.argument_uid = None
		self.isSupportive = issupportive
		self.author_uid = author
		self.argument_uid = 0
		self.issue_uid = issue
		self.weight_uid = 0

	def conclusions_argument(self, argument):
		self.argument_uid = argument

	def set_weight_uid(self, weight_uid):
		self.weight_uid = weight_uid


class Track(DiscussionBase):
	"""
	Track-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'track'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	statement_uid = sa.Column(sa.Integer, sa.ForeignKey('statements.uid'))
	premisesGroup_uid = sa.Column(sa.Integer, sa.ForeignKey('premisegroups.uid'))
	argument_uid = sa.Column(sa.Integer, sa.ForeignKey('arguments.uid'))
	attacked_by_relation = sa.Column(sa.Integer, sa.ForeignKey('relation.uid'))
	attacked_with_relation = sa.Column(sa.Integer, sa.ForeignKey('relation.uid'))
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	session_id = sa.Column(sa.Integer)

	users = relationship('User', foreign_keys=[author_uid])
	statements = relationship('Statement', foreign_keys=[statement_uid])
	premisegroups = relationship('PremiseGroup', foreign_keys=[premisesGroup_uid])
	arguments = relationship('Argument', foreign_keys=[argument_uid])
	attacked_by = relationship('Relation', foreign_keys=[attacked_by_relation])
	attacked_with = relationship('Relation', foreign_keys=[attacked_with_relation])

	def __init__(self, user, statement, premisegroup=0, argument=0, attacked_by=0, attacked_with=0, session_id=0):
		"""
		Initializes a row in current track-table
		:param user:
		:param statement:
		:param premisegroup:
		:param argument:
		:param attacked_by:
		:param attacked_with:
		:param session_id:
		:return:
		"""
		self.author_uid = user
		self.statement_uid = statement
		self.premisesGroup_uid = premisegroup
		self.argument_uid = argument
		self.attacked_by_relation = attacked_by
		self.attacked_with_relation = attacked_with
		self.timestamp = func.now()
		self.session_id = session_id


class History(DiscussionBase):
	"""
	History-table with several columns.
	Each user will be tracked
	"""
	__tablename__ = 'history'
	uid = sa.Column(sa.Integer, primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'))
	url = sa.Column(sa.Text, nullable=False)
	keyword_after_decission = sa.Column(sa.Text, nullable=False)
	keyword_before_decission = sa.Column(sa.Text, nullable=False)
	timestamp = sa.Column(sa.DateTime(timezone=True), default=func.now())
	session_id = sa.Column(sa.Integer)

	def __init__(self, user, url, keyword_after_decission='', keyword_before_decission='', session_id=0):
		"""
		Initializes a row in current history-table
		:param user:
		:param url:
		:param keyword_after_decission:
		:param keyword_before_decission:
		:param session_id:
		:return:
		"""
		self.author_uid = user
		self.url = url
		self.keyword_after_decission = keyword_after_decission
		self.keyword_before_decission = keyword_before_decission
		self.timestamp = func.now()
		self.session_id = session_id

	def set_keyword_after_decission(self, keyword_after_decission):
		"""
		Refrehses the value
		:param keyword_after_decission: current keyword
		:return:
		"""
		self.keyword_after_decission = keyword_after_decission

	def set_keyword_before_decission(self, keyword_before_decission):
		"""
		Refrehses the value
		:param keyword_before_decission: current keyword
		:return:
		"""
		self.keyword_before_decission = keyword_before_decission


class Relation(DiscussionBase): # TODO IS THIS NECESSARY ?
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
		:param name:
		:return:
		"""
		self.name = name


class Weight(DiscussionBase):
	"""
	Weight-table with several columns.
	Each weight uid is mapped with a vote.
	"""
	__tablename__ = 'weights'
	uid = sa.Column(sa.Integer, primary_key=True)


class Vote(DiscussionBase):
	"""
	Vote-table with several columns.
	The combination of the both FK is a PK
	"""
	__tablename__ = 'votes'
	weight_uid = sa.Column(sa.Integer, sa.ForeignKey('weights.uid'), primary_key=True)
	author_uid = sa.Column(sa.Integer, sa.ForeignKey('users.uid'), primary_key=True)
	isUpVote = sa.Column(sa.Boolean, nullable=False)

	weights = relationship('Weight', foreign_keys=[weight_uid])
	users = relationship('User', foreign_keys=[author_uid])

	def __init__(self, weight_uid=0, author_uid=0, isUpVote=0):
		"""
		Initializes a row
		:param weight_uid:
		:param author_uid:
		:return:
		"""
		self.weight_uid = weight_uid
		self.author_uid = author_uid
		self.isUpVote = isUpVote

	def set_up_vote(self, isUpVote):
		self.isUpVote = isUpVote
