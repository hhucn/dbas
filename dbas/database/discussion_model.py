"""
D-BAS database Model

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import warnings
from abc import abstractmethod
from typing import List, Set

import arrow
import bcrypt
from slugify import slugify
from sqlalchemy import Integer, Text, Boolean, Column, ForeignKey, DateTime, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType

from dbas.database import DBDiscussionSession, DiscussionBase
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def sql_timestamp_pretty_print(ts, lang='en', humanize=True, with_exact_time=False):
    """
    Pretty printing for sql timestamp in dependence of the language.

    :param ts: timestamp (arrow) as string
    :param lang: language
    :param humanize: Boolean
    :param with_exact_time: Boolean
    :return: String
    """
    if humanize:
        # if lang == 'de':
        ts = ts.to('Europe/Berlin')
        # else:
        #    ts = ts.to('US/Pacific')
        return ts.humanize(locale=lang)
    else:
        if lang == 'de':
            return ts.format('DD.MM.YYYY' + (', HH:mm:ss ' if with_exact_time else ''))
        else:
            return ts.format('YYYY-MM-DD' + (', HH:mm:ss ' if with_exact_time else ''))


def get_now():
    """
    Returns local server time

    :return: arrow data type
    """
    return arrow.utcnow().to('local')


class Issue(DiscussionBase):
    """
    issue-table with several columns.
    Each issue has text and a creation date
    """
    __tablename__ = 'issues'
    uid = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True)
    info = Column(Text, nullable=False)
    long_info = Column(Text, nullable=False)
    date = Column(ArrowType, default=get_now())
    author_uid = Column(Integer, ForeignKey('users.uid'))
    lang_uid = Column(Integer, ForeignKey('languages.uid'))
    is_disabled = Column(Boolean, nullable=False)
    is_private = Column(Boolean, nullable=False, server_default="False")
    is_read_only = Column(Boolean, nullable=False, server_default="False")

    users = relationship('User', foreign_keys=[author_uid])
    languages = relationship('Language', foreign_keys=[lang_uid])
    participating_users = relationship('User', secondary='user_participation')
    statements = relationship('Statement', secondary='statement_to_issue')

    positions = relationship('Statement', secondary='statement_to_issue', viewonly=True,
                             secondaryjoin="and_(Statement.is_position == True, Statement.uid == StatementToIssue.statement_uid)")

    def __init__(self, title, info, long_info, author_uid, lang_uid, is_disabled=False, is_private=False,
                 is_read_only=False):
        """
        Initializes a row in current position-table
        """
        self.title = title
        self.slug = slugify(self.title)
        self.info = info
        self.long_info = long_info
        self.author_uid = author_uid
        self.lang_uid = lang_uid
        self.is_disabled = is_disabled
        self.is_private = is_private
        self.is_read_only = is_read_only
        self.date = get_now()

    @hybrid_property
    def lang(self):
        """
        Returns ui_locale abbreviation of current language

        :return: String
        """
        return DBDiscussionSession.query(Language).get(self.lang_uid).ui_locales

    def set_disabled(self, is_disabled):
        """
        Disabled current issue

        :param is_disabled: Boolean
        :return: None
        """
        self.is_disabled = is_disabled

    def set_private(self, is_private):
        """
        Set issue as private

        :param is_private: Boolean
        :return: None
        """
        self.is_private = is_private

    def set_read_only(self, is_read_only):
        """
        Set issue as read only

        :param is_read_only: Boolean
        :return: None
        """
        self.is_read_only = is_read_only

    def __json__(self, _request):
        return {
            "title": self.title,
            "slug": self.slug,
            "summary": self.info,
            "description": self.long_info,
            "url": "/" + self.slug,
            "language": self.lang,
            "date": self.date.format(),
        }


class Language(DiscussionBase):
    """
    language-table with several columns.
    """
    __tablename__ = 'languages'
    uid = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    ui_locales = Column(Text, nullable=False, unique=True)

    def __init__(self, name, ui_locales):
        """
        Initializes a row in current table
        """
        self.name = name
        self.ui_locales = ui_locales


class Group(DiscussionBase):
    """
    group-table with several columns.
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
    """
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    firstname = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    nickname = Column(Text, nullable=False, unique=True)
    public_nickname = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    gender = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    group_uid = Column(Integer, ForeignKey('groups.uid'))
    last_action = Column(ArrowType, default=get_now())
    last_login = Column(ArrowType, default=get_now())
    registered = Column(ArrowType, default=get_now())
    token = Column(Text, nullable=True)
    token_timestamp = Column(ArrowType, nullable=True)
    oauth_provider = Column(Text, nullable=True)
    oauth_provider_id = Column(Text, nullable=True)

    groups: List['Group'] = relationship('Group', foreign_keys=[group_uid], order_by='Group.uid')
    history: List['History'] = relationship('History', back_populates='author')
    participates_in: List['Issue'] = relationship('Issue', secondary='user_participation')
    arguments: List['Argument'] = relationship('Argument', back_populates='author')

    def __init__(self, firstname, surname, nickname, email, password, gender, group_uid, token='',
                 token_timestamp=None, oauth_provider='', oauth_provider_id=''):
        """
        Initializes a row in current user-table

        :param firstname: String
        :param surname: String
        :param nickname: String
        :param email: String
        :param password: String (hashed)
        :param gender: String
        :param group_uid: int
        :param token:
        :param token_timestamp:
        """
        self.firstname = firstname
        self.surname = surname
        self.nickname = nickname
        self.public_nickname = nickname
        self.email = email
        self.gender = gender
        self.password = password
        self.group_uid = group_uid
        self.last_action = get_now()
        self.last_login = get_now()
        self.registered = get_now()
        self.token = token
        self.token_timestamp = token_timestamp
        self.oauth_provider = oauth_provider
        self.oauth_provider_id = oauth_provider_id

    def __str__(self):
        return self.public_nickname

    def validate_password(self, password: str) -> bool:
        """
        Validates given password with against the saved one

        :param password: String
        :return: Boolean
        """
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

    def change_password(self, new_password: str):
        """
        Sets a new password for a user.

        :param new_password: The new *unhashed* password for the user
        :return: Nothing
        """
        self.password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')

    def update_last_login(self):
        """
        Refreshed timestamp of last login

        :return: None
        """
        self.last_login = get_now()

    def update_last_action(self):
        """
        Refreshed timestamp of last action

        :return: None
        """
        self.last_action = get_now()

    def update_token_timestamp(self):
        """
        Refreshed tokens timestamp

        :return: None
        """
        self.token_timestamp = get_now()

    def set_token(self, token):
        """
        Set token

        :return: None
        """
        self.token = token

    def set_public_nickname(self, nick):
        """
        Set public nickname

        :return: None
        """
        self.public_nickname = nick

    @hybrid_property
    def global_nickname(self):
        """
        Return the first name if the user set this in his settings, otherwise the public nickname

        :return:
        """
        return self.firstname if self.settings.should_show_public_nickname else self.public_nickname

    def to_small_dict(self):
        """
        Returns some uid and nickname of the row as dictionary.

        :return: dict()
        """
        return {
            'uid': self.uid,
            'nickname': self.nickname
        }

    def is_admin(self):
        """
        Check, if the user is member of the admin group

        :return: True, if the user is member of the admin group
        """
        return DBDiscussionSession.query(Group).filter_by(name='admins').first().uid == self.group_uid

    def set_group(self, group_name: str):
        """
        Sets the group of a user based of the name for the group.
        :param group_name:
        :return:
        """
        self.groups = DBDiscussionSession.query(Group).filter_by(name=group_name).one()

    def promote_to_admin(self):
        """
        Promotes the user to an admin. WOW
        :return:
        """
        self.set_group("admins")

    def demote_to_user(self):
        """
        Demotes the user to a regular user.
        :return:
        """
        self.set_group("users")

    def is_special(self):
        """
        Check, if the user is member of the special group

        :return: True, if the user is member of the admin group
        """
        return DBDiscussionSession.query(Group).filter_by(name='specials').first().uid == self.group_uid

    def is_author(self):
        """
        Check, if the user is member of the authors group

        :return: True, if the user is member of the authors group
        """
        return DBDiscussionSession.query(Group).filter_by(name='authors').first().uid == self.group_uid

    @hybrid_property
    def settings(self):
        """
        Check, if the user is member of the admin group

        :return: True, if the user is member of the admin group
        """
        return DBDiscussionSession.query(Settings).filter_by(author_uid=self.uid).first()

    @staticmethod
    def by_nickname(nickname: str) -> 'User':  # https://www.python.org/dev/peps/pep-0484/#forward-references
        return DBDiscussionSession.query(User).filter_by(nickname=nickname).one()


class UserParticipation(DiscussionBase):
    __tablename__ = 'user_participation'
    user_uid = Column(Integer, ForeignKey('users.uid'), primary_key=True)
    issue_uid = Column(Integer, ForeignKey('issues.uid'), primary_key=True)

    user = relationship('User')
    issue = relationship('Issue')


class Settings(DiscussionBase):
    """
    Settings-table with several columns.
    """
    __tablename__ = 'settings'
    author_uid = Column(Integer, ForeignKey('users.uid'), nullable=True, primary_key=True)
    should_send_mails = Column(Boolean, nullable=False)
    should_send_notifications = Column(Boolean, nullable=False)
    should_show_public_nickname = Column(Boolean, nullable=False)
    last_topic_uid = Column(Integer, ForeignKey('issues.uid'), nullable=False)
    lang_uid = Column(Integer, ForeignKey('languages.uid'))
    keep_logged_in = Column(Boolean, nullable=False)

    users = relationship('User', foreign_keys=[author_uid])
    issues = relationship('Issue', foreign_keys=[last_topic_uid])
    languages = relationship('Language', foreign_keys=[lang_uid])

    def __init__(self, author_uid, send_mails, send_notifications, should_show_public_nickname=True, lang_uid=2,
                 keep_logged_in=False):
        """
        Initializes a row in current settings-table

        :param author_uid:
        :param send_mails:
        :param send_notifications:
        :param should_show_public_nickname:
        :param lang_uid:
        :param keep_logged_in:
        """
        issue = DBDiscussionSession.query(Issue).first()
        self.author_uid = author_uid
        self.should_send_mails = send_mails
        self.should_send_notifications = send_notifications
        self.should_show_public_nickname = should_show_public_nickname
        self.last_topic_uid = issue.uid if issue else 1
        self.lang_uid = lang_uid
        self.keep_logged_in = keep_logged_in

    def set_send_mails(self, send_mails):
        """
        Set boolean value whether mails should be send

        :param send_mails: Boolean
        :return: None
        """
        self.should_send_mails = send_mails

    def set_send_notifications(self, send_notifications):
        """
        Set boolean value whether notifications should be send

        :param send_notifications:
        :return: None
        """
        self.should_send_notifications = send_notifications

    def set_show_public_nickname(self, should_show_public_nickname):
        """
        Set boolean value whether the users nickname should be public

        :param should_show_public_nickname: Boolean
        :return: None
        """
        self.should_show_public_nickname = should_show_public_nickname

    def set_last_topic_uid(self, uid):
        """
        Updates last used topic of user

        :param uid: issue.uid
        :return: None
        """
        self.last_topic_uid = uid

    def set_lang_uid(self, lang_uid):
        """
        Sets users preferred language

        :param lang_uid: Language.uid
        :return: None
        """
        self.lang_uid = lang_uid

    @hybrid_property
    def lang(self) -> str:
        return self.languages.ui_locales

    def should_hold_the_login(self, keep_logged_in):
        """
        Should we hold the login?

        :param keep_logged_in: Boolean
        :return: None
        """
        self.keep_logged_in = keep_logged_in


class Statement(DiscussionBase):
    """
    Statement-table with several columns.
    Each statement has link to its text
    """
    __tablename__ = 'statements'
    uid = Column(Integer, primary_key=True)
    is_position = Column(Boolean, nullable=False)
    is_disabled = Column(Boolean, nullable=False)

    issues: List[Issue] = relationship('Issue', secondary='statement_to_issue', back_populates='statements')
    arguments: List['Argument'] = relationship('Argument', back_populates='conclusion')
    premises: List['Premise'] = relationship('Premise', back_populates='statement')

    def __init__(self, is_position, is_disabled=False):
        """
        Inits a row in current statement table

        :param is_position: boolean
        :param is_disabled: Boolean
        """
        self.is_position = is_position
        self.is_disabled = is_disabled

    def set_disabled(self, is_disabled):
        """
        Disables current Statement

        :param is_disabled: Boolean
        :return: None
        """
        self.is_disabled = is_disabled

    def set_position(self, is_position):
        """
        Sets boolean whether this statement is a position

        :param is_position: boolean
        :return: None
        """
        self.is_position = is_position

    def get_timestamp(self):
        """
        Return timestamp

        :return: Textversions Timestamp
        """
        return DBDiscussionSession.query(TextVersion).get(self.textversion_uid).timestamp

    def get_first_timestamp(self):
        """
        Return timestamp

        :return: Textversions Timestamp
        """
        return DBDiscussionSession.query(TextVersion).filter_by(statement_uid=self.uid).first().timestamp

    def get_first_author(self):
        """
        Return timestamp

        :return: Textversions Timestamp
        """
        return DBDiscussionSession.query(TextVersion).filter_by(statement_uid=self.uid).first().author_uid

    @hybrid_property
    def lang(self):
        """
        Returns ui_locale of Issues language

        :return: string
        """
        db_statement2issues = DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=self.uid).first()
        return DBDiscussionSession.query(Issue).get(db_statement2issues.issue_uid).lang

    @hybrid_property
    def textversion_uid(self):
        """
        The id of the latest textversion

        :return:
        """

        return DBDiscussionSession.query(TextVersion).filter_by(statement_uid=self.uid, is_disabled=False).order_by(
            TextVersion.timestamp.desc()).first().uid

    @hybrid_property
    def textversions(self):
        return self.get_textversion()

    @hybrid_property
    def issue_uid(self):
        warnings.warn("Use 'issues' instead.", DeprecationWarning)
        return DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=self.uid).first().issue_uid

    def get_textversion(self):
        """
        Returns the latest textversion for this statement.

        :return: TextVersion object
        """
        return DBDiscussionSession.query(TextVersion).get(self.textversion_uid)

    def get_text(self, html: bool = False) -> str:
        """
        Gets the current text from the statement, without trailing punctuation.

        :param html: If True, returns a html span for coloring.
        :return:
        """
        text = self.get_textversion().content
        while text.endswith(('.', '?', '!')):
            text = text[:-1]

        if html:
            return '<span data-argumentation-type="position">{}</span>'.format(text)
        else:
            return text

    def get_html(self) -> str:
        return self.get_text(html=True)

    def flat_statements_below(self) -> Set['Statement']:
        """Recursively steps down through a discussion starting at a statement to get all statements below."""
        return Statement.__step_down_statement(self)

    @staticmethod
    def __step_down_argument(argument: 'Argument') -> Set['Statement']:
        result_set = set()
        if argument.premisegroup:
            for premise in argument.premisegroup.premises:
                size_before = len(result_set)
                result_set.add(premise.statement)

                # check if we have run above this statement once in the past, should prevent loops
                if len(result_set) != size_before:
                    result_set = result_set.union(Statement.__step_down_statement(premise.statement))
        for argument in argument.arguments:
            result_set = result_set.union(Statement.__step_down_argument(argument))
        return result_set

    @staticmethod
    def __step_down_statement(statement: 'Statement') -> Set['Statement']:
        result_set = set()

        for argument in statement.arguments:
            result_set = result_set.union(Statement.__step_down_argument(argument))
        return result_set


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
    created = Column(ArrowType, default=get_now())

    statements = relationship('Statement', foreign_keys=[statement_uid])
    users = relationship('User', foreign_keys=[author_uid])
    issues = relationship('Issue', foreign_keys=[issue_uid])

    def __init__(self, reference: str, host: str, path: str, author_uid: int, statement_uid: int, issue_uid: int):
        """
        Store a real-world text-reference.

        :param reference: String
        :param host: Host of URL
        :param path: Path of URL
        :param author_uid: User.uid
        :param statement_uid: Statement.uid
        :param issue_uid: Issue.uid
        :return: None
        """
        self.reference = reference
        self.host = host
        self.path = path
        self.author_uid = author_uid
        self.statement_uid = statement_uid
        self.issue_uid = issue_uid

    @hybrid_property
    def issue(self) -> Issue:
        return DBDiscussionSession.query(Issue).get(self.issue_uid)

    @hybrid_property
    def statement(self) -> Statement:
        return DBDiscussionSession.query(Statement).get(self.statement_uid)

    def get_statement_text(self, html: bool = False) -> str:
        """
        Gets the current references text from the statement, without trailing punctuation.

        :param html: If True, returns a html span for coloring.
        :return:
        """
        db_statement = DBDiscussionSession.query(Statement).get(self.statement_uid)
        return db_statement.get_text(html)


class StatementOrigins(DiscussionBase):
    """
    Add an origin to the statement. Comes from external services, like the EDEN-aggregators.
    """
    __tablename__ = 'statement_origins'
    uid = Column(Integer, primary_key=True)
    entity_id = Column(Text, nullable=True)
    aggregate_id = Column(Text, nullable=True)
    version = Column(Integer, nullable=True)
    statement_uid = Column(Integer, ForeignKey('statements.uid'), nullable=False)
    author = Column(Text, nullable=True)
    created = Column(ArrowType, default=get_now())

    statement = relationship('Statement', foreign_keys=[statement_uid])

    def __init__(self, entity_id: str, aggregate_id: str, version: int, author: str, statement_uid: int):
        """
        Initialize the origin.

        :param entity_id: external id of the entity, e.g. a statement
        :param aggregate_id: the original host where the entity was first introduced into the system
        :param author: author of the statement
        :param version: current version, might be different from 1 if the entity was updated
        :param statement_uid: local statement where this origin needs to be assigned to
        """
        self.entity_id = entity_id
        self.aggregate_id = aggregate_id
        self.author = author
        self.version = version
        self.statement_uid = statement_uid


class StatementToIssue(DiscussionBase):
    __tablename__ = 'statement_to_issue'
    uid = Column(Integer, primary_key=True)
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    issue_uid = Column(Integer, ForeignKey('issues.uid'))

    statements = relationship('Statement', foreign_keys=[statement_uid])
    issues = relationship('Issue', foreign_keys=[issue_uid])

    def __init__(self, statement, issue):
        """

        :param statement:
        :param issue:
        """
        warnings.warn("Use Statement.issues and Issue.statements instead.", DeprecationWarning)
        self.statement_uid = statement
        self.issue_uid = issue


class SeenStatement(DiscussionBase):
    """
    List of users, which have seen a statement
    A statement is marked as seen, if it is/was selectable during the justification steps
    """
    __tablename__ = 'seen_statements'
    uid = Column(Integer, primary_key=True)
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    user_uid = Column(Integer, ForeignKey('users.uid'))

    statements = relationship('Statement', foreign_keys=[statement_uid])
    users = relationship('User', foreign_keys=[user_uid])

    def __init__(self, statement_uid, user_uid):
        """
        Inits a row in current statement seen by table

        :param statement_uid: Statement.uid
        :param user_uid: User.uid
        """
        self.statement_uid = statement_uid
        self.user_uid = user_uid


class SeenArgument(DiscussionBase):
    """
    List of users, which have seen a argument
    An argument is marked as seen, if the user has vote for it or if the argument is presented as attack
    """
    __tablename__ = 'seen_arguments'
    uid = Column(Integer, primary_key=True)
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    user_uid = Column(Integer, ForeignKey('users.uid'))

    arguments = relationship('Argument', foreign_keys=[argument_uid])
    users = relationship('User', foreign_keys=[user_uid])

    def __init__(self, argument_uid, user_uid):
        """
        Inits a row in current argument seen by table

        :param argument_uid: Argument.uid
        :param user_uid: User.uid
        """
        self.argument_uid = argument_uid
        self.user_uid = user_uid


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
    timestamp = Column(ArrowType, default=get_now())
    is_disabled = Column(Boolean, nullable=False)

    statement = relationship('Statement', foreign_keys=[statement_uid])
    author = relationship('User', foreign_keys=[author_uid])

    def __init__(self, content, author, statement_uid=None, is_disabled=False):
        """
        Initializes a row in current text versions-table

        :param content: String
        :param author: User.uid
        :return: None
        """
        self.content = content
        self.author_uid = author
        self.timestamp = get_now()
        self.statement_uid = statement_uid
        self.is_disabled = is_disabled

    def set_statement(self, statement_uid):
        """
        Set the statement of the textversion

        :param statement_uid: Statement.uid
        :return: None
        """
        self.statement_uid = statement_uid

    def set_disabled(self, is_disabled):
        """
        Disables current textversion

        :param is_disabled: Boolean
        :return: None
        """
        self.is_disabled = is_disabled

    def to_dict(self):
        """
        Returns the row as dictionary.

        :return: dict()
        """
        return {
            'uid': self.uid,
            'statement_uid': self.statement_uid,
            'content': self.content,
            'author_uid': self.author_uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp),
            'is_disabled': self.is_disabled
        }


class Premise(DiscussionBase):
    """
    Each premises has a value pair of group and statement, an author,
    a timestamp as well as a boolean whether it is negated
    """
    __tablename__ = 'premises'
    uid = Column(Integer, primary_key=True)
    premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    is_negated = Column(Boolean, nullable=False)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    issue_uid = Column(Integer, ForeignKey('issues.uid'))
    is_disabled = Column(Boolean, nullable=False)

    premisegroup = relationship('PremiseGroup', foreign_keys=[premisegroup_uid], back_populates='premises')
    statement = relationship(Statement, foreign_keys=[statement_uid], back_populates='premises')
    author = relationship(User, foreign_keys=[author_uid])
    issue = relationship(Issue, foreign_keys=[issue_uid])

    def __init__(self, premisesgroup, statement, is_negated, author, issue, is_disabled=False):
        """
        Initializes a row in current premises-table

        :param premisesgroup: PremiseGroup.uid
        :param statement: Statement.uid
        :param is_negated: Boolean
        :param author: User.uid
        :param issue: Issue.uid
        :param is_disabled: Boolean
        :return: None
        """
        self.premisegroup_uid = premisesgroup
        self.statement_uid = statement
        self.is_negated = is_negated
        self.author_uid = author
        self.timestamp = get_now()
        self.issue_uid = issue
        self.is_disabled = is_disabled

    def set_disabled(self, is_disabled):
        """
        Disables current premise

        :param is_disabled: Boolean
        :return: None
        """
        self.is_disabled = is_disabled

    def set_statement(self, statement):
        """
        Sets statement fot his Premise

        :param statement: Statement.uid
        :return: None
        """
        self.statement_uid = statement

    def set_premisegroup(self, premisegroup):
        """
        Set premisegroup for this premise

        :param premisegroup: Premisegroup.uid
        :return: None
        """
        self.premisegroup_uid = premisegroup

    def get_text(self, html: bool = False) -> str:
        """
        Gets the current premise text from the statement, without trailing punctuation.

        :param html: If True, returns a html span for coloring.
        :return:
        """
        db_statement = DBDiscussionSession.query(Statement).get(self.statement_uid)
        return db_statement.get_text(html)

    def get_html(self) -> str:
        return self.get_text(html=True)

    def to_dict(self):
        """
        Returns the row as dictionary.

        :return: dict()
        """
        return {
            'premisegroup_uid': self.premisegroup_uid,
            'statement_uid': self.statement_uid,
            'is_negated': self.is_negated,
            'author_uid': self.author_uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp),
            'issue_uid': self.issue_uid,
            'is_disabled': self.is_disabled
        }


class PremiseGroup(DiscussionBase):
    """
    PremiseGroup-table with several columns.
    Each premisesGroup has a id and an author
    """
    __tablename__ = 'premisegroups'
    uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer, ForeignKey('users.uid'))

    author: List[User] = relationship(User, foreign_keys=[author_uid])
    premises: List[Premise] = relationship(Premise, back_populates='premisegroup')
    arguments: List['Argument'] = relationship('Argument', back_populates='premisegroup')

    def __init__(self, author: int):
        """
        Initializes a row in current premisesGroup-table

        :param author: User.id
        :return: None
        """
        self.author_uid = author

    def get_text(self):
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=self.uid).join(Statement).all()
        texts = [premise.get_text() for premise in db_premises]
        lang = DBDiscussionSession.query(Statement).get(db_premises[0].statement.uid).lang
        return ' {} '.format(Translator(lang).get(_.aand)).join(texts)


class Argument(DiscussionBase):
    """
    Argument-table with several columns.
    Each argument has justifying statement(s) (premises) and the the statement-to-be-justified (argument or statement).
    Additionally there is a relation, timestamp, author, weight, ...
    """
    __tablename__ = 'arguments'
    uid = Column(Integer, primary_key=True)
    premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'), nullable=False)
    conclusion_uid = Column(Integer, ForeignKey('statements.uid'), nullable=True)
    argument_uid = Column(Integer, ForeignKey('arguments.uid'), nullable=True)
    is_supportive = Column(Boolean, nullable=False)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    issue_uid = Column(Integer, ForeignKey('issues.uid'))
    is_disabled = Column(Boolean, nullable=False)

    premisegroup = relationship(PremiseGroup, foreign_keys=[premisegroup_uid], back_populates='arguments')
    conclusion = relationship('Statement', foreign_keys=[conclusion_uid], back_populates='arguments')
    issues = relationship(Issue, foreign_keys=[issue_uid])

    author = relationship('User', back_populates='arguments')
    argument: 'Argument' = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid,
                                        back_populates='arguments')

    arguments: List['Argument'] = relationship('Argument', remote_side=argument_uid, back_populates='argument')

    def __init__(self, premisegroup, is_supportive, author, issue: int, conclusion=None, argument=None,
                 is_disabled=False):
        """
        Initializes a row in current argument-table

        :param premisegroup: PremiseGroup.uid
        :param is_supportive: Boolean
        :param author: User.uid
        :param issue: Issue.uid
        :param conclusion: Default 0, which will be None
        :param argument: Default 0, which will be None
        :param is_disabled: Boolean
        :return: None
        """
        self.premisegroup_uid = premisegroup
        self.conclusion_uid = None if conclusion == 0 else conclusion
        self.argument_uid = None if argument == 0 else argument
        self.is_supportive = is_supportive
        self.author_uid = author
        self.argument_uid = argument
        self.issue_uid = issue
        self.is_disabled = is_disabled
        self.timestamp = get_now()

    def set_conclusions_argument(self, argument):
        """
        Sets an argument as conclusion for this argument

        :param argument: Argument.uid
        :return:
        """
        self.argument_uid = argument

    def set_conclusion(self, conclusion):
        """
        Sets a conclusion for the argument

        :param conclusion: Statement.uid
        :return: None
        """
        self.conclusion_uid = conclusion

    def set_premisegroup(self, premisegroup):
        """
        Sets a premisegroup for the argument

        :param premisegroup: PremiseGroup.uid
        :return: None
        """
        self.premisegroup_uid = premisegroup

    def set_disabled(self, is_disabled):
        """
        Disables current argument

        :param is_disabled: boolean
        :return: None
        """
        self.is_disabled = is_disabled

    @hybrid_property
    def lang(self):
        """
        Returns ui_locales of current Argument

        :return: String
        """
        return self.issues.lang

    def get_conclusion_text(self, html: bool = False) -> str:
        """
        Gets the current conclusion text from the argument, without trailing punctuation.

        :param html: If True, returns a html span for coloring.
        :return:
        """
        if not self.conclusion_uid:
            return ''
        db_statement = DBDiscussionSession.query(Statement).get(self.conclusion_uid)
        return db_statement.get_text(html)

    def get_premisegroup_text(self) -> str:
        db_premisegroup = DBDiscussionSession.query(PremiseGroup).get(self.premisegroup_uid)
        return db_premisegroup.get_text()

    def to_dict(self):
        """
        Returns the row as dictionary.

        :return: dict()
        """
        return {
            'uid': self.uid,
            'premisegroup_uid': self.premisegroup_uid,
            'conclusion_uid': self.conclusion_uid,
            'argument_uid': self.argument_uid,
            'is_supportive': self.is_supportive,
            'author_uid': self.author_uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp),
            'issue_uid': self.issue_uid,
            'is_disabled': self.is_disabled,
        }


class History(DiscussionBase):
    """
    History-table with several columns.
    Each user will be tracked
    """
    __tablename__ = 'history'
    uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    path = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())

    author = relationship('User', foreign_keys=[author_uid], back_populates='history')

    def __init__(self, author_uid, path):
        """
        Inits a row in current history table

        :param author_uid: User.uid
        :param path: String
        :return: None
        """
        self.author_uid = author_uid
        self.path = path
        self.timestamp = get_now()


class ClickedArgument(DiscussionBase):
    """
    Vote-table with several columns for arguments.
    An argument will be voted, if the user has selected the premise and conclusion of this argument.
    """
    __tablename__ = 'clicked_arguments'
    uid = Column(Integer, primary_key=True)
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_up_vote = Column(Boolean, nullable=False)
    is_valid = Column(Boolean, nullable=False)

    arguments = relationship('Argument', foreign_keys=[argument_uid])
    users = relationship('User', foreign_keys=[author_uid])

    def __init__(self, argument_uid, author_uid, is_up_vote=True, is_valid=True):
        """
        Inits a row in current clicked argument table

        :param argument_uid: Argument.uid
        :param author_uid: User.uid
        :param is_up_vote: Boolean
        :param is_valid: Boolean
        :return: None
        """
        self.argument_uid = argument_uid
        self.author_uid = author_uid
        self.is_up_vote = is_up_vote
        self.timestamp = get_now()
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
        self.timestamp = get_now()


class ClickedStatement(DiscussionBase):
    """
    Vote-table with several columns for statements.
    A statement will be voted, if the user has selected the statement as justification
    or if the statement is used as part of an argument.
    """
    __tablename__ = 'clicked_statements'
    uid = Column(Integer, primary_key=True)
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_up_vote = Column(Boolean, nullable=False)
    is_valid = Column(Boolean, nullable=False)

    statements = relationship('Statement', foreign_keys=[statement_uid])
    users = relationship('User', foreign_keys=[author_uid])

    def __init__(self, statement_uid, author_uid, is_up_vote=True, is_valid=True):
        """
        Inits a row in current clicked statement table

        :param statement_uid: Statement.uid
        :param author_uid: User.uid
        :param is_up_vote: Boolean
        :param is_valid: Boolean
        :return: None
        """
        self.statement_uid = statement_uid
        self.author_uid = author_uid
        self.is_up_vote = is_up_vote
        self.timestamp = get_now()
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
        self.timestamp = get_now()


class MarkedArgument(DiscussionBase):
    """
    MarkedArgument-table with several columns.
    """
    __tablename__ = 'marked_arguments'
    uid = Column(Integer, primary_key=True)
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())

    arguments = relationship('Argument', foreign_keys=[argument_uid])
    users = relationship('User', foreign_keys=[author_uid])

    def __init__(self, argument, user):
        """
        Inits a row in current statement table

        :param argument: Argument.uid
        :param user: User.uid
        """
        self.argument_uid = argument
        self.author_uid = user
        self.timestamp = get_now()

    def to_dict(self):
        """
        Returns the row as dictionary.

        :return: dict()
        """
        return {
            'argument_uid': self.argument_uid,
            'author_uid': self.author_uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp)
        }


class MarkedStatement(DiscussionBase):
    """
    MarkedStatement-table with several columns.
    """
    __tablename__ = 'marked_statements'
    uid = Column(Integer, primary_key=True)
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())

    statements = relationship('Statement', foreign_keys=[statement_uid])
    users = relationship('User', foreign_keys=[author_uid])

    def __init__(self, statement, user):
        """
        Inits a row in current marked statement table

        :param statement: Statement.uid
        :param user: User.uid
        """
        self.statement_uid = statement
        self.author_uid = user
        self.timestamp = get_now()

    def to_dict(self):
        """
        Returns the row as dictionary.

        :return: dict()
        """
        return {
            'statement_uid': self.statement_uid,
            'author_uid': self.author_uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp)
        }


class Message(DiscussionBase):
    """
    Message-table with several columns.
    """
    __tablename__ = 'messages'
    uid = Column(Integer, primary_key=True)
    from_author_uid = Column(Integer, ForeignKey('users.uid'))
    to_author_uid = Column(Integer, ForeignKey('users.uid'))
    topic = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())
    read = Column(Boolean, nullable=False)
    is_inbox = Column(Boolean, nullable=False)

    from_users = relationship('User', foreign_keys=[from_author_uid])
    to_users = relationship('User', foreign_keys=[to_author_uid])

    def __init__(self, from_author_uid, to_author_uid, topic, content, is_inbox=True, read=False):
        """
        Inits a row in current message table

        :param from_author_uid: user.uid
        :param to_author_uid: user.uid
        :param topic: String
        :param content: String
        :param is_inbox: Boolean
        :param read: Boolean
        """
        self.from_author_uid = from_author_uid
        self.to_author_uid = to_author_uid
        self.topic = topic
        self.content = content
        self.timestamp = get_now()
        self.read = read
        self.is_inbox = is_inbox

    def set_read(self, was_read):
        """
        Sets validity of this record.

        :param was_read: boolean
        :return: None
        """
        self.read = was_read


class AbstractReviewCase(DiscussionBase):
    __abstract__ = True  # Needed for SQLAlchemy
    uid = NotImplemented
    detector_uid = NotImplemented
    timestamp = NotImplemented

    @abstractmethod
    def set_executed(self, is_executed):
        pass

    @abstractmethod
    def set_revoked(self, is_revoked):
        pass

    @abstractmethod
    def update_timestamp(self):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.uid is NotImplemented or \
                cls.detector_uid is NotImplemented or \
                cls.timestamp is NotImplemented:
            raise NotImplementedError("Your subclass of AbstractReviewCase did not define all columns")


class ReviewDelete(AbstractReviewCase):
    """
    ReviewDelete-table with several columns.
    """
    __tablename__ = 'review_deletes'
    uid = Column(Integer, primary_key=True)
    detector_uid = Column(Integer, ForeignKey('users.uid'))
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed = Column(Boolean, nullable=False, default=False)
    reason_uid = Column(Integer, ForeignKey('review_delete_reasons.uid'))
    is_revoked = Column(Boolean, nullable=False, default=False)

    detectors = relationship('User', foreign_keys=[detector_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])
    reasons = relationship('ReviewDeleteReason', foreign_keys=[reason_uid])

    def __init__(self, detector, argument=None, statement=None, reason=None, is_executed=False, is_revoked=False):
        """
        Inits a row in current review delete table

        :param detector: User.uid
        :param argument: Argument.uid
        :param reason: ReviewDeleteReason.uid
        :param is_executed: Boolean
        """
        self.detector_uid = detector
        self.argument_uid = argument
        self.statement_uid = statement
        self.reason_uid = reason
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """
        Set this review as executed

        :param is_executed: Boolean
        :return: None
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """
        Set this review as revoked

        :param is_revoked: Boolean
        :return: None
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        """
        Updates timestamp of current row

        :return:
        """
        self.timestamp = get_now()


class ReviewEdit(AbstractReviewCase):
    """
    -table with several columns.
    """
    __tablename__ = 'review_edits'
    uid = Column(Integer, primary_key=True)
    detector_uid = Column(Integer, ForeignKey('users.uid'))
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed = Column(Boolean, nullable=False, default=False)
    is_revoked = Column(Boolean, nullable=False, default=False)

    detectors = relationship('User', foreign_keys=[detector_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])

    def __init__(self, detector, argument=None, statement=None, is_executed=False, is_revoked=False):
        """
        Inits a row in current review edit table

        :param detector: User.uid
        :param argument: Argument.uid
        :param statement: Statement.uid
        :param is_executed: Boolean
        :param is_revoked: Boolean
        """
        self.detector_uid = detector
        self.argument_uid = argument
        self.statement_uid = statement
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """
        Sets current review as executed

        :param is_executed: Boolean
        :return: None
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """
        Sets current review as revoked

        :param is_revoked: Boolean
        :return: None
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        """
        Update timestamp

        :return: None
        """
        self.timestamp = get_now()


class ReviewEditValue(DiscussionBase):
    """
    ReviewEditValue-table with several columns.
    """
    __tablename__ = 'review_edit_values'
    uid = Column(Integer, primary_key=True)
    review_edit_uid = Column(Integer, ForeignKey('review_edits.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    typeof = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    reviews = relationship('ReviewEdit', foreign_keys=[review_edit_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])

    def __init__(self, review_edit, statement, typeof, content):
        """
        Inits a row in current review edit value table

        :param review_edit: ReviewEdit.uid
        :param statement: Statement.uid
        :param typeof: String
        :param content: String
        """
        self.review_edit_uid = review_edit
        self.statement_uid = statement
        self.typeof = typeof
        self.content = content


class ReviewOptimization(AbstractReviewCase):
    """
    ReviewOptimization-table with several columns.
    """
    __tablename__ = 'review_optimizations'
    uid = Column(Integer, primary_key=True)
    detector_uid = Column(Integer, ForeignKey('users.uid'))
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed = Column(Boolean, nullable=False, default=False)
    is_revoked = Column(Boolean, nullable=False, default=False)

    detectors = relationship('User', foreign_keys=[detector_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])

    def __init__(self, detector, argument=None, statement=None, is_executed=False, is_revoked=False):
        """
        Inits a row in current review optimization table

        :param detector: User.uid
        :param argument: Argument.uid
        :param statement: Statement.uid
        :param is_executed: Boolean
        :param is_revoked: Boolean
        """
        self.detector_uid = detector
        self.argument_uid = argument
        self.statement_uid = statement
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """
        Sets current review as executed

        :param is_executed: Boolean
        :return: None
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """
        Sets current review as revoked

        :param is_revoked: Boolean
        :return: None
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        """
        Update timestamp

        :return: None
        """
        self.timestamp = get_now()


class ReviewDuplicate(AbstractReviewCase):
    """
    ReviewDuplicate-table with several columns.
    """
    __tablename__ = 'review_duplicates'
    uid = Column(Integer, primary_key=True)
    detector_uid = Column(Integer, ForeignKey('users.uid'))
    duplicate_statement_uid = Column(Integer, ForeignKey('statements.uid'))
    original_statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed = Column(Boolean, nullable=False, default=False)
    is_revoked = Column(Boolean, nullable=False, default=False)

    detectors = relationship('User', foreign_keys=[detector_uid])
    duplicate_statement = relationship('Statement', foreign_keys=[duplicate_statement_uid])
    original_statement = relationship('Statement', foreign_keys=[original_statement_uid])

    def __init__(self, detector, duplicate_statement=None, original_statement=None, is_executed=False,
                 is_revoked=False):
        """
        Inits a row in current review duplicate table

        :param detector: User.uid
        :param duplicate_statement: Statement.uid
        :param original_statement: Statement.uid
        :param is_executed: Boolean
        :param is_revoked: Boolean
        """
        self.detector_uid = detector
        self.duplicate_statement_uid = duplicate_statement
        self.original_statement_uid = original_statement
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """
        Sets current review as executed

        :param is_executed: Boolean
        :return: None
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """
        Sets current review as revoked

        :param is_revoked: Boolean
        :return: None
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        """
        Update timestamp

        :return: None
        """
        self.timestamp = get_now()


class ReviewMerge(AbstractReviewCase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_merge'
    uid = Column(Integer, primary_key=True)
    detector_uid = Column(Integer, ForeignKey('users.uid'))
    premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed = Column(Boolean, nullable=False, default=False)
    is_revoked = Column(Boolean, nullable=False, default=False)

    detectors = relationship('User', foreign_keys=[detector_uid])
    premisegroups = relationship('PremiseGroup', foreign_keys=[premisegroup_uid])

    def __init__(self, detector, premisegroup, is_executed=False, is_revoked=False):
        """
        Inits a row in current review merge table

        :param detector: User.uid
        :param premisegroup: PremiseGroup.uid
        :param is_executed: Boolean
        :param is_revoked: Boolean
        """
        self.detector_uid = detector
        self.premisegroup_uid = premisegroup
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """
        Sets current review as executed

        :param is_executed: Boolean
        :return: None
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """
        Sets current review as revoked

        :param is_revoked: Boolean
        :return: None
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        """
        Update timestamp

        :return: None
        """
        self.timestamp = get_now()


class ReviewSplit(AbstractReviewCase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_split'
    uid = Column(Integer, primary_key=True)
    detector_uid = Column(Integer, ForeignKey('users.uid'))
    premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed = Column(Boolean, nullable=False, default=False)
    is_revoked = Column(Boolean, nullable=False, default=False)

    detectors = relationship('User', foreign_keys=[detector_uid])
    premisegroups = relationship('PremiseGroup', foreign_keys=[premisegroup_uid])

    def __init__(self, detector, premisegroup, is_executed=False, is_revoked=False):
        """
        Inits a row in current review split table

        :param detector: User.uid
        :param premisegroup: PremiseGroup.uid
        :param is_executed: Boolean
        :param is_revoked: Boolean
        """
        self.detector_uid = detector
        self.premisegroup_uid = premisegroup
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """
        Sets current review as executed

        :param is_executed: Boolean
        :return: None
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """
        Sets current review as revoked

        :param is_revoked: Boolean
        :return: None
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        """
        Update timestamp

        :return: None
        """
        self.timestamp = get_now()


class ReviewSplitValues(DiscussionBase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_split_values'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_split.uid'))
    content = Column(Text, nullable=False)

    reviews = relationship('ReviewSplit', foreign_keys=[review_uid])

    def __init__(self, review, content):
        """
        Inits a row in current review merge value table

        :param review: ReviewSplit.uid
        :param content: String
        """
        self.review_uid = review
        self.content = content


class ReviewMergeValues(DiscussionBase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_merge_values'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_merge.uid'))
    content = Column(Text, nullable=False)

    reviews = relationship('ReviewMerge', foreign_keys=[review_uid])

    def __init__(self, review, content):
        """
        Inits a row in current review merge value table

        :param review: ReviewMerge.uid
        :param content: String
        """
        self.review_uid = review
        self.content = content


class ReviewDeleteReason(DiscussionBase):
    """
    ReviewDeleteReason-table with several columns.
    """
    __tablename__ = 'review_delete_reasons'
    uid = Column(Integer, primary_key=True)
    reason = Column(Text, nullable=False, unique=True)

    def __init__(self, reason):
        """
        Inits a row in current review delete reason table

        :param reason: String
        """
        self.reason = reason


class AbstractLastReviewerCase(DiscussionBase):
    __abstract__ = True  # Needed for SQLAlchemy
    uid = NotImplemented
    reviewer_uid = NotImplemented
    review_uid = NotImplemented
    timestamp = NotImplemented

    @abstractmethod
    def __eq__(self, other):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.uid is NotImplemented or \
                cls.review_uid is NotImplemented or \
                cls.reviewer_uid is NotImplemented or \
                cls.timestamp is NotImplemented:
            raise NotImplementedError("Your subclass of AbstractLastReviewerCase did not define all columns")


class LastReviewerDelete(AbstractLastReviewerCase):
    """
    LastReviewerDelete-table with several columns.
    """
    __tablename__ = 'last_reviewers_delete'
    uid = Column(Integer, primary_key=True)
    reviewer_uid = Column(Integer, ForeignKey('users.uid'))
    review_uid = Column(Integer, ForeignKey('review_deletes.uid'))
    is_okay = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer = relationship('User', foreign_keys=[reviewer_uid])
    review = relationship('ReviewDelete', foreign_keys=[review_uid])

    def __init__(self, reviewer, review, is_okay):
        """
        Inits a row in current last reviewer delete table

        :param reviewer: User.uid
        :param review: ReviewDelete.uid
        :param is_okay: Boolean
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()

    def __eq__(self, other):
        return self.uid == other.uid


class LastReviewerDuplicate(AbstractLastReviewerCase):
    """
    LastReviewerDuplicate-table with several columns.
    """
    __tablename__ = 'last_reviewers_duplicates'
    uid = Column(Integer, primary_key=True)
    reviewer_uid = Column(Integer, ForeignKey('users.uid'))
    review_uid = Column(Integer, ForeignKey('review_duplicates.uid'))
    is_okay = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer = relationship('User', foreign_keys=[reviewer_uid])
    review = relationship('ReviewDuplicate', foreign_keys=[review_uid])

    def __init__(self, reviewer, review, is_okay):
        """
        Inits a row in current last reviewer duplicate table

        :param reviewer: User.uid
        :param review: ReviewDuplicate.uid
        :param is_okay: Boolean
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()

    def __eq__(self, other):
        return self.uid == other.uid


class LastReviewerEdit(AbstractLastReviewerCase):
    """
    LastReviewerEdit-table with several columns.
    """
    __tablename__ = 'last_reviewers_edit'
    uid = Column(Integer, primary_key=True)
    reviewer_uid = Column(Integer, ForeignKey('users.uid'))
    review_uid = Column(Integer, ForeignKey('review_edits.uid'))
    is_okay = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer = relationship('User', foreign_keys=[reviewer_uid])
    review = relationship('ReviewEdit', foreign_keys=[review_uid])

    def __init__(self, reviewer, review, is_okay):
        """

        :param reviewer: User.uid
        :param review: ReviewEdit.uid
        :param is_okay: Boolean
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()

    def __eq__(self, other):
        return self.uid == other.uid


class LastReviewerOptimization(AbstractLastReviewerCase):
    """
    Inits a row in current last reviewer edit table
    """
    __tablename__ = 'last_reviewers_optimization'
    uid = Column(Integer, primary_key=True)
    reviewer_uid = Column(Integer, ForeignKey('users.uid'))
    review_uid = Column(Integer, ForeignKey('review_optimizations.uid'))
    is_okay = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer = relationship('User', foreign_keys=[reviewer_uid])
    review = relationship('ReviewOptimization', foreign_keys=[review_uid])

    def __init__(self, reviewer, review, is_okay):
        """
        Inits a row in current last reviewer optimization  table

        :param reviewer: User.uid
        :param review: ReviewOptimization.uid
        :param is_okay: boolean
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()

    def __eq__(self, other):
        return self.uid == other.uid


class LastReviewerSplit(AbstractLastReviewerCase):
    """
    Inits a row in current last reviewer split table
    """
    __tablename__ = 'last_reviewers_split'
    uid = Column(Integer, primary_key=True)
    reviewer_uid = Column(Integer, ForeignKey('users.uid'))
    review_uid = Column(Integer, ForeignKey('review_split.uid'))
    should_split = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer = relationship('User', foreign_keys=[reviewer_uid])
    review = relationship('ReviewSplit', foreign_keys=[review_uid])

    def __init__(self, reviewer, review, should_split):
        """
        Inits a row in current last reviewer Split  table

        :param reviewer: User.uid
        :param review: ReviewSplit.uid
        :param should_split: boolean
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.should_split = should_split
        self.timestamp = get_now()

    def __eq__(self, other):
        return self.uid == other.uid


class LastReviewerMerge(AbstractLastReviewerCase):
    """
    Inits a row in current last reviewer merge table
    """
    __tablename__ = 'last_reviewers_merge'
    uid = Column(Integer, primary_key=True)
    reviewer_uid = Column(Integer, ForeignKey('users.uid'))
    review_uid = Column(Integer, ForeignKey('review_merge.uid'))
    should_merge = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer = relationship('User', foreign_keys=[reviewer_uid])
    review = relationship('ReviewMerge', foreign_keys=[review_uid])

    def __init__(self, reviewer, review, should_merge):
        """
        Inits a row in current last reviewer merge  table

        :param reviewer: User.uid
        :param review: ReviewMerge.uid
        :param should_merge: boolean
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.should_merge = should_merge
        self.timestamp = get_now()

    def __eq__(self, other):
        return self.uid == other.uid


class ReputationHistory(DiscussionBase):
    """
    ReputationHistory-table with several columns.
    """
    __tablename__ = 'reputation_history'
    uid = Column(Integer, primary_key=True)
    reputator_uid = Column(Integer, ForeignKey('users.uid'))
    reputation_uid = Column(Integer, ForeignKey('reputation_reasons.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reputators = relationship('User', foreign_keys=[reputator_uid])
    reputations = relationship('ReputationReason', foreign_keys=[reputation_uid])

    def __init__(self, reputator, reputation):
        """
        Inits a row in current reputation history table

        :param reputator: User.uid
        :param reputation: ReputationReason.uid
        """
        self.reputator_uid = reputator
        self.reputation_uid = reputation
        self.timestamp = get_now()


class ReputationReason(DiscussionBase):
    """
    ReputationReason-table with several columns.
    """
    __tablename__ = 'reputation_reasons'
    uid = Column(Integer, primary_key=True)
    reason = Column(Text, nullable=False, unique=True)
    points = Column(Integer, nullable=False)

    def __init__(self, reason, points):
        """
        Inits a row in current reputation reason table

        :param reason: String
        :param points: Ont
        """
        self.reason = reason
        self.points = points


class OptimizationReviewLocks(DiscussionBase):
    """
    OptimizationReviewLocks-table with several columns.
    """
    __tablename__ = 'optimization_review_locks'
    author_uid = Column(Integer, ForeignKey('users.uid'), primary_key=True)
    review_optimization_uid = Column(Integer, ForeignKey('review_optimizations.uid'))
    locked_since = Column(ArrowType, default=get_now(), nullable=True)

    authors = relationship('User', foreign_keys=[author_uid])
    review_optimization = relationship('ReviewOptimization', foreign_keys=[review_optimization_uid])

    def __init__(self, author, review_optimization):
        """
        Inits a row in current optimization review locks table

        :param author: User.uid
        :param review_optimization: ReviewOptimization.uid
        """
        self.author_uid = author
        self.review_optimization_uid = review_optimization
        self.timestamp = get_now()


class ReviewCanceled(DiscussionBase):
    """
    ReviewCanceled-table with several columns.
    """
    __tablename__ = 'review_canceled'
    uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    review_edit_uid = Column(Integer, ForeignKey('review_edits.uid'), nullable=True)
    review_delete_uid = Column(Integer, ForeignKey('review_deletes.uid'), nullable=True)
    review_optimization_uid = Column(Integer, ForeignKey('review_optimizations.uid'), nullable=True)
    review_duplicate_uid = Column(Integer, ForeignKey('review_duplicates.uid'), nullable=True)
    review_merge_uid = Column(Integer, ForeignKey('review_merge.uid'), nullable=True)
    review_split_uid = Column(Integer, ForeignKey('review_split.uid'), nullable=True)
    was_ongoing = Column(Boolean)
    timestamp = Column(ArrowType, default=get_now())

    authors = relationship('User', foreign_keys=[author_uid])
    edits = relationship('ReviewEdit', foreign_keys=[review_edit_uid])
    deletes = relationship('ReviewDelete', foreign_keys=[review_delete_uid])
    optimizations = relationship('ReviewOptimization', foreign_keys=[review_optimization_uid])
    duplicates = relationship('ReviewDuplicate', foreign_keys=[review_duplicate_uid])
    merges = relationship('ReviewMerge', foreign_keys=[review_merge_uid])
    plits = relationship('ReviewSplit', foreign_keys=[review_split_uid])

    def __init__(self, author, review_data, was_ongoing=False):
        """
        Inits a row in current review locks table

        :param author: User.uid
        :param review_data: dict with possible review uids
        :param was_ongoing: Boolean
        """
        self.author_uid = author
        self.review_edit_uid = review_data.get('edit')
        self.review_delete_uid = review_data.get('delete')
        self.review_optimization_uid = review_data.get('optimization')
        self.review_duplicate_uid = review_data.get('duplicate')
        self.review_merge_uid = review_data.get('merge')
        self.review_split_uid = review_data.get('split')
        self.was_ongoing = was_ongoing
        self.timestamp = get_now()


class RevokedContent(DiscussionBase):
    """
    RevokedContent-table with several columns.
    """
    __tablename__ = 'revoked_content'
    uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())

    authors = relationship('User', foreign_keys=[author_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])

    def __init__(self, author, argument=None, statement=None):
        """
        Inits a row in current revoked content table

        :param author: User.uid
        :param argument: Argument.uid
        :param statement: Statement.uid
        """
        self.author_uid = author
        self.argument_uid = argument
        self.statement_uid = statement
        self.timestamp = get_now()


class RevokedContentHistory(DiscussionBase):
    """
    RevokedContentHistory-table with several columns.
    """
    __tablename__ = 'revoked_content_history'
    uid = Column(Integer, primary_key=True)
    old_author_uid = Column(Integer, ForeignKey('users.uid'))
    new_author_uid = Column(Integer, ForeignKey('users.uid'))
    textversion_uid = Column(Integer, ForeignKey('textversions.uid'), nullable=True)
    argument_uid = Column(Integer, ForeignKey('arguments.uid'), nullable=True)

    old_authors = relationship('User', foreign_keys=[old_author_uid])
    new_authors = relationship('User', foreign_keys=[new_author_uid])
    textversions = relationship('TextVersion', foreign_keys=[textversion_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])

    def __init__(self, old_author_uid, new_author_uid, textversion_uid=None, argument_uid=None):
        """
        Inits a row in current revoked content history table

        :param old_author_uid: User.uid
        :param new_author_uid: User.uid
        :param textversion_uid: TextVersion.uid
        :param argument_uid: Argument.uid
        """
        self.old_author_uid = old_author_uid
        self.new_author_uid = new_author_uid
        self.textversion_uid = textversion_uid
        self.argument_uid = argument_uid


class RevokedDuplicate(DiscussionBase):
    """
    RevokedDuplicate-table with several columns.
    """
    __tablename__ = 'revoked_duplicate'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_duplicates.uid'))

    bend_position = Column(Boolean, nullable=False)
    statement_uid = Column(Integer, ForeignKey('statements.uid'))

    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    premise_uid = Column(Integer, ForeignKey('premises.uid'))

    timestamp = Column(ArrowType, default=get_now())
    review = relationship('ReviewDuplicate', foreign_keys=[review_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])
    premises = relationship('Premise', foreign_keys=[premise_uid])

    def __init__(self, review, bend_position=False, statement=None, conclusion_of_argument=None, premise=None):
        """
        Inits a row in current revoked duplicate table

        :param review: ReviewDuplicate.uid
        :param bend_position: Boolean
        :param statement: Statement.uid
        :param conclusion_of_argument: Argument.uid
        :param premise: Premise.uid
        """
        self.review_uid = review
        self.bend_position = bend_position
        self.statement_uid = statement
        self.argument_uid = conclusion_of_argument
        self.premise_uid = premise
        self.timestamp = get_now()


class PremiseGroupSplitted(DiscussionBase):
    """
    PremiseGroupSplitted-table with several columns.
    """
    __tablename__ = 'premisegroup_splitted'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_split.uid'))
    old_premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    new_premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reviews = relationship('ReviewSplit', foreign_keys=[review_uid])
    old_premisegroups = relationship('PremiseGroup', foreign_keys=[old_premisegroup_uid])
    new_premisegroups = relationship('PremiseGroup', foreign_keys=[new_premisegroup_uid])

    def __init__(self, review, old_premisegroup, new_premisegroup):
        """
        Inits a row in current table

        :param review: ReviewDuplicate.uid
        :param old_premisegroup: PremiseGroup.uid
        :param new_premisegroup: PremiseGroup.uid
        """
        self.review_uid = review
        self.old_premisegroup_uid = old_premisegroup
        self.new_premisegroup_uid = new_premisegroup
        self.timestamp = get_now()


class PremiseGroupMerged(DiscussionBase):
    """
    Table with several columns to indicate which statement should be merged to a new one
    """
    __tablename__ = 'premisegroup_merged'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_merge.uid'))
    old_premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    new_premisegroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reviews = relationship('ReviewMerge', foreign_keys=[review_uid])
    old_premisegroups = relationship('PremiseGroup', foreign_keys=[old_premisegroup_uid])
    new_premisegroups = relationship('PremiseGroup', foreign_keys=[new_premisegroup_uid])

    def __init__(self, review, old_premisegroup, new_premisegroup):
        """
        Inits a row in current statement splitted table

        :param review: ReviewMerge.uid
        :param old_premisegroup: PremiseGroup.uid
        :param new_premisegroup: PremiseGroup.uid
        """
        self.review_uid = review
        self.old_premisegroup_uid = old_premisegroup
        self.new_premisegroup_uid = new_premisegroup
        self.timestamp = get_now()


class StatementReplacementsByPremiseGroupSplit(DiscussionBase):
    """
    List of replaced statements through split action of a pgroup
    """
    __tablename__ = 'statement_replacements_by_premisegroup_split'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_split.uid'))
    old_statement_uid = Column(Integer, ForeignKey('statements.uid'))
    new_statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reviews = relationship('ReviewSplit', foreign_keys=[review_uid])
    old_statements = relationship('Statement', foreign_keys=[old_statement_uid])
    new_statements = relationship('Statement', foreign_keys=[new_statement_uid])

    def __init__(self, review, old_statement, new_statement):
        """
        Inits a row in current table

        :param review: ReviewSplit.uid
        :param old_statement: Statement.uid
        :param new_statement: Statement.uid
        """
        self.review_uid = review
        self.old_statement_uid = old_statement
        self.new_statement_uid = new_statement
        self.timestamp = get_now()


class StatementReplacementsByPremiseGroupMerge(DiscussionBase):
    """
    List of replaced statements through merge action of a pgroup
    """
    __tablename__ = 'statement_replacements_by_premisegroups_merge'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_split.uid'))
    old_statement_uid = Column(Integer, ForeignKey('statements.uid'))
    new_statement_uid = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reviews = relationship('ReviewSplit', foreign_keys=[review_uid])
    old_statements = relationship('Statement', foreign_keys=[old_statement_uid])
    new_statements = relationship('Statement', foreign_keys=[new_statement_uid])

    def __init__(self, review, old_statement, new_statement):
        """
        Inits a row in current table

        :param review: ReviewMerge.uid
        :param old_statement: Statement.uid
        :param new_statement: Statement.uid
        """
        self.review_uid = review
        self.old_statement_uid = old_statement
        self.new_statement_uid = new_statement
        self.timestamp = get_now()


class ArgumentsAddedByPremiseGroupSplit(DiscussionBase):
    """
    List of added arguments through the split of a pgroup
    """
    __tablename__ = 'arguments_added_by_premisegroups_split'
    uid = Column(Integer, primary_key=True)
    review_uid = Column(Integer, ForeignKey('review_split.uid'))
    argument_uid = Column(Integer, ForeignKey('arguments.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reviews = relationship('ReviewSplit', foreign_keys=[review_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid])

    def __init__(self, review, argument):
        """
        Inits a row in current table

        :param review: ReviewMerge.uid
        :param argument: Argument.uid
        """
        self.review_uid = review
        self.argument_uid = argument
        self.timestamp = get_now()


class News(DiscussionBase):
    """
    News-table with several columns.
    """
    __tablename__ = 'news'
    __table_args__ = {'schema': 'news'}
    uid = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    date = Column(ArrowType, nullable=False)
    news = Column(Text, nullable=False)

    def __init__(self, title, author, news, date):
        """
        Initializes a row in current news-table
        """
        self.title = title
        self.author = author
        self.news = news
        self.date = date


class APIToken(DiscussionBase):
    """
        Hashes of tokens generated by an admin
    """
    __tablename__ = 'api_tokens'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    token = Column(String, nullable=False, unique=True)
    owner = Column(Text, nullable=False)
    disabled = Column(Boolean, nullable=False, server_default="False")

    def __init__(self, created, token, owner, disabled=False):
        """
        Adds a row to api tokens

        :param created: When was the token created.
        :param token: The SHA-256 hash of the token.
        :param owner: The name of the owner of the token.
        :param disabled: Is the token disabled or not. (defaults to not)
        """
        self.created = created
        self.token = token
        self.owner = owner

    def __str__(self):
        return "API-Token for {} created {}".format(self.owner, self.created)


class ShortLinks(DiscussionBase):
    """
    Shortened link with several columns.
    """
    __tablename__ = 'short_links'
    uid = Column(Integer, primary_key=True)
    service = Column(Text, nullable=False)
    long_url = Column(Text, nullable=False)
    short_url = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())

    def __init__(self, service, long_url, short_url):
        self.service = service
        self.long_url = long_url
        self.short_url = short_url
        self.timestamp = get_now()

    def update_short_url(self, short_url):
        self.short_url = short_url
        self.timestamp = get_now()
