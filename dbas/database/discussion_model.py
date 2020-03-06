"""
D-BAS database Model
"""
import logging
import warnings
from abc import abstractmethod, ABC, ABCMeta
from datetime import datetime
from typing import List, Set, Optional, Dict, Any

import arrow
import bcrypt
from slugify import slugify
from sqlalchemy import Integer, Text, Boolean, Column, ForeignKey, DateTime, String
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType

from dbas.database import DBDiscussionSession, DiscussionBase
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


def sql_timestamp_pretty_print(ts, lang: str = 'en', humanize: bool = True, with_exact_time: bool = False):
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


def get_now() -> ArrowType:
    """
    Returns local server time

    :return: arrow data type
    """
    return arrow.get(datetime.now())


class Issue(DiscussionBase):
    """
    issue-table with several columns.
    Each issue has text and a creation date
    """
    __tablename__ = 'issues'
    uid: int = Column(Integer, primary_key=True)
    title: str = Column(Text, nullable=False)
    slug: str = Column(Text, nullable=False, unique=True)
    info: str = Column(Text, nullable=False)
    long_info: str = Column(Text, nullable=False)
    date = Column(ArrowType, default=get_now())
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    lang_uid: int = Column(Integer, ForeignKey('languages.uid'))
    is_disabled: bool = Column(Boolean, nullable=False)
    is_private: bool = Column(Boolean, nullable=False, server_default="False")
    is_read_only: bool = Column(Boolean, nullable=False, server_default="False")
    is_featured: bool = Column(Boolean, nullable=False, server_default="False")

    users: 'User' = relationship('User', foreign_keys=[author_uid])  # deprecated
    author: 'User' = relationship('User', foreign_keys=[author_uid], back_populates='authored_issues')
    languages = relationship('Language', foreign_keys=[lang_uid])  # deprecated
    language: 'Language' = relationship('Language', foreign_keys=[lang_uid])
    participating_users: List['User'] = relationship('User', secondary='user_participation',
                                                     back_populates='participates_in')

    premises: List['Premise'] = relationship('Premise', back_populates='issue')
    statements = relationship('Statement', secondary='statement_to_issue')
    all_arguments = relationship('Argument', back_populates='issue')

    positions: List['Statement'] = relationship('Statement', secondary='statement_to_issue', viewonly=True,
                                                secondaryjoin="and_(Statement.is_position == True, Statement.uid == StatementToIssue.statement_uid)")

    decision_process: Optional['DecisionProcess'] = relationship('DecisionProcess', back_populates='issue',
                                                                 uselist=False)

    def __init__(self, title: str, info: str, long_info: str, author: 'User', language: 'Language',
                 is_disabled: bool = False,
                 is_private: bool = False,
                 is_read_only: bool = False,
                 is_featured: bool = False,
                 slug: str = None,
                 date: datetime = None):
        """
        Initializes a row in current position-table
        """
        self.title = title
        self.slug = slug if slug else slugify(title)
        self.info = info
        self.long_info = long_info
        self.author = author
        self.language = language
        self.is_disabled = is_disabled
        self.is_private = is_private
        self.is_read_only = is_read_only
        self.date = date if date else get_now()
        self.is_featured = is_featured
        self.participating_users = [author, ]

    def __repr__(self):
        return f"<Issue {self.uid}: {self.slug}>"

    @hybrid_property
    def participating_authors(self) -> Set['User']:
        return set([premise.author for premise in self.premises])

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

    @staticmethod
    def by_slug(slug: str) -> 'Issue':
        return DBDiscussionSession.query(Issue).filter(Issue.slug == slug).one()

    def __json__(self, _request):
        return {
            "title": self.title,
            "slug": self.slug,
            "summary": self.info,
            "description": self.long_info,
            "url": "/" + self.slug,
            "language": self.lang,
            "date": self.date.format(),
            "is_read_only": self.is_read_only,
            "is_private": self.is_private,
            "is_disabled": self.is_disabled,
            "is_featured": self.is_featured
        }


class Language(DiscussionBase):
    """
    language-table with several columns.
    """
    __tablename__ = 'languages'
    uid: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    ui_locales: str = Column(Text, nullable=False, unique=True)

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
    uid: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False, unique=True)

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
    uid: int = Column(Integer, primary_key=True)
    firstname: str = Column(Text, nullable=False)
    surname: str = Column(Text, nullable=False)
    nickname: str = Column(Text, nullable=False, unique=True)
    public_nickname: str = Column(Text, nullable=False)
    email: str = Column(Text, nullable=False)
    gender: str = Column(Text, nullable=False)
    password: str = Column(Text, nullable=False)
    group_uid: int = Column(Integer, ForeignKey('groups.uid'))
    last_action = Column(ArrowType, default=get_now())
    last_login = Column(ArrowType, default=get_now())
    registered = Column(ArrowType, default=get_now())
    oauth_provider: str = Column(Text, nullable=True)
    oauth_provider_id: str = Column(Text, nullable=True)

    group: 'Group' = relationship('Group', foreign_keys=[group_uid], order_by='Group.uid')
    history: List['History'] = relationship('History', back_populates='author', order_by='History.timestamp')
    participates_in: List['Issue'] = relationship('Issue', secondary='user_participation',
                                                  back_populates='participating_users')
    arguments: List['Argument'] = relationship('Argument', back_populates='author')
    authored_issues: List[Issue] = relationship('Issue', back_populates='author')
    settings: 'Settings' = relationship('Settings', back_populates='user', uselist=False)

    clicked_statements: List['ClickedStatement'] = relationship('ClickedStatement', back_populates='user')
    clicked_arguments: List['ClickedArgument'] = relationship('ClickedArgument', back_populates='user')

    def __init__(self, firstname: str, surname: str, nickname: str, email: str, password: str, gender: str,
                 group: 'Group', oauth_provider: Optional[str] = None, oauth_provider_id: Optional[str] = None):
        """
        Initializes a row in current user-table

        :param firstname: String
        :param surname: String
        :param nickname: String
        :param email: String
        :param password: String (hashed)
        :param gender: String
        :param group_uid: int
        """
        self.firstname = firstname
        self.surname = surname
        self.nickname = nickname
        self.public_nickname = nickname
        self.email = email
        self.gender = gender
        self.password = password
        self.group = group
        self.last_action = get_now()
        self.last_login = get_now()
        self.registered = get_now()
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

    def is_anonymous(self):
        return self.uid == 1

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
        self.group = DBDiscussionSession.query(Group).filter_by(name=group_name).one()

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
    def accessible_issues(self) -> List['Issue']:
        db_issues = DBDiscussionSession.query(Issue).filter(Issue.is_disabled == False,
                                                            Issue.is_private == False).all()

        return list(set(db_issues).union(self.participates_in)) if not self.is_anonymous() else db_issues

    @accessible_issues.setter
    def accessible_issues(self, issue: Issue) -> None:
        self.participates_in.append(issue)

    def __json__(self, _request=None):
        return {
            "uid": self.uid,
            "nickname": self.public_nickname
        }

    @staticmethod
    def by_nickname(nickname: str) -> 'User':  # https://www.python.org/dev/peps/pep-0484/#forward-references
        return DBDiscussionSession.query(User).filter_by(nickname=nickname).one()


class UserParticipation(DiscussionBase):
    __tablename__ = 'user_participation'
    user_uid: int = Column(Integer, ForeignKey('users.uid'), primary_key=True)
    issue_uid: int = Column(Integer, ForeignKey('issues.uid'), primary_key=True)

    user: User = relationship('User')
    issue: Issue = relationship('Issue')


class Settings(DiscussionBase):
    """
    Settings-table with several columns.
    """
    __tablename__ = 'settings'
    author_uid: int = Column(Integer, ForeignKey('users.uid'), nullable=True, primary_key=True)
    should_send_mails: bool = Column(Boolean, nullable=False)
    should_send_notifications: bool = Column(Boolean, nullable=False)
    should_show_public_nickname: bool = Column(Boolean, nullable=False)
    last_topic_uid: int = Column(Integer, ForeignKey('issues.uid'), nullable=False)
    lang_uid: int = Column(Integer, ForeignKey('languages.uid'))
    keep_logged_in: bool = Column(Boolean, nullable=False)

    user: User = relationship('User', foreign_keys=[author_uid], back_populates='settings')
    last_topic: Issue = relationship('Issue')
    language: Language = relationship('Language')

    def __init__(self, user: 'User', send_mails, send_notifications, should_show_public_nickname=True,
                 language: 'Language' = None, keep_logged_in=False):
        """
        Initializes a row in current settings-table

        :param user:
        :param send_mails:
        :param send_notifications:
        :param should_show_public_nickname:
        :param lang_uid:
        :param keep_logged_in:
        """
        issue = DBDiscussionSession.query(Issue).first()
        self.user = user
        self.should_send_mails = send_mails
        self.should_send_notifications = send_notifications
        self.should_show_public_nickname = should_show_public_nickname
        self.last_topic_uid = issue.uid if issue else 1
        self.language = language
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

    def set_lang_uid(self, lang_uid):
        """
        Sets users preferred language

        :param lang_uid: Language.uid
        :return: None
        """
        self.lang_uid = lang_uid

    @hybrid_property
    def lang(self) -> str:
        return self.language.ui_locales

    def should_hold_the_login(self, keep_logged_in):
        """
        Should we hold the login?

        :param keep_logged_in: Boolean
        :return: None
        """
        self.keep_logged_in = keep_logged_in


class GraphNode(ABC):

    @abstractmethod
    def to_d3_dict(self) -> Dict[str, str]:
        """Returns the representation for d3 of this node"""
        pass

    @abstractmethod
    def get_sub_nodes(self) -> Set['GraphNode']:
        """Returns a set of all GraphNodes which are one level deeper"""
        pass

    @abstractmethod
    def aif_node(self) -> Dict[str, str]:
        """Returns a dictionary in the form of an AIF node"""
        pass

    @property
    @abstractmethod
    def is_disabled(self) -> bool:
        pass

    def get_sub_tree(self, level=0) -> Set['GraphNode']:
        """Returns a flat set of all reachable nodes in the graph below the current node."""
        nodes = self.get_sub_nodes()

        for node in nodes:
            if not node.is_disabled:
                nodes = nodes.union(node.get_sub_tree(level=level + 1))
        return nodes
        # return nodes.union(*[node.get_sub_tree(level=level + 1) for node in nodes if node.is_disabled])


class GraphNodeMeta(DeclarativeMeta, ABCMeta):
    pass


class Statement(DiscussionBase, GraphNode, metaclass=GraphNodeMeta):
    """
    Statement-table with several columns.
    Each statement has link to its text
    """
    __tablename__ = 'statements'
    uid: int = Column(Integer, primary_key=True)
    is_position: bool = Column(Boolean, nullable=False)
    is_disabled: bool = Column(Boolean, nullable=False)

    issues: List[Issue] = relationship('Issue', secondary='statement_to_issue', back_populates='statements')
    arguments: List['Argument'] = relationship('Argument', back_populates='conclusion')
    premises: List['Premise'] = relationship('Premise', back_populates='statement')
    references: List['StatementReference'] = relationship('StatementReference', back_populates='statement')
    all_textversions: List['TextVersion'] = relationship('TextVersion',
                                                         back_populates='statement',
                                                         cascade="all",
                                                         order_by="TextVersion.timestamp")

    clicks = relationship('ClickedStatement')

    def __init__(self, is_position, is_disabled=False):
        """
        Inits a row in current statement table

        :param is_position: boolean
        :param is_disabled: Boolean
        """
        self.is_position = is_position
        self.is_disabled = is_disabled

    def __repr__(self):
        return f"<Statement: {self.uid} \"{self.get_text()}\">"

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
    def textversion_uid(self) -> Optional[int]:
        """
        The id of the latest textversion, or None if there is no enabled textversion

        :return:
        """

        textversion: TextVersion = DBDiscussionSession.query(TextVersion).filter_by(
            statement_uid=self.uid, is_disabled=False).order_by(TextVersion.timestamp.desc()).first()
        if textversion:
            return textversion.uid
        LOG.warning(f"Statement {self.uid} has no active textversion.")
        return None

    @hybrid_property
    def textversions(self) -> Optional["TextVersion"]:
        return self.get_textversion()

    @hybrid_property
    def issue_uid(self):
        warnings.warn("Use 'issues' instead.", DeprecationWarning)
        return DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=self.uid).first().issue_uid

    def get_textversion(self) -> Optional["TextVersion"]:
        """
        Returns the latest textversion for this statement or None if there is no active textversion.

        :return: TextVersion object
        """
        if self.textversion_uid:
            return DBDiscussionSession.query(TextVersion).get(self.textversion_uid)
        return None

    def get_text(self, html: bool = False) -> Optional[str]:
        """
        Gets the current text from the statement, without trailing punctuation.

        :param html: If True, returns a html span for coloring.
        :return: None if there is no active textversion
        """
        textversion = self.get_textversion()
        if not textversion:
            return None
        text = textversion.content
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
        for argument in argument.attacked_by:
            result_set = result_set.union(Statement.__step_down_argument(argument))
        return result_set

    @staticmethod
    def __step_down_statement(statement: 'Statement') -> Set['Statement']:
        result_set = set()

        for argument in statement.arguments:
            result_set = result_set.union(Statement.__step_down_argument(argument))
        return result_set

    def to_d3_dict(self):
        return {
            'id': 'statement_' + str(self.uid),
            'label': self.get_text(),
            'type': 'position' if self.is_position else 'statement',
            'timestamp': self.get_first_timestamp().timestamp,
            'edge_source': None,
            'edge_target': None
        }

    def get_sub_nodes(self):
        return set([argument for argument in self.arguments if not argument.is_disabled])

    def aif_node(self):
        return {
            "nodeID": f"statement_{self.uid}",
            "text": self.get_text(),
            "type": "I",
            "timestamp": str(self.get_timestamp())
        }


class StatementReference(DiscussionBase):
    """
    From API: Reference to be stored and assigned to a statement.
    """
    __tablename__ = 'statement_references'
    uid: int = Column(Integer, primary_key=True)
    text: str = Column(Text, nullable=False)
    host: str = Column(Text, nullable=False)
    path: str = Column(Text, nullable=False)
    author_uid: int = Column(Integer, ForeignKey('users.uid'), nullable=False)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'), nullable=False)
    issue_uid: int = Column(Integer, ForeignKey('issues.uid'), nullable=False)
    created = Column(ArrowType, default=get_now())

    statement: Statement = relationship('Statement', back_populates='references')
    author: User = relationship('User')
    issue: Issue = relationship('Issue')

    def __init__(self, text: str, host: str, path: str, author_uid: int, statement_uid: int, issue_uid: int):
        """
        Store a real-world text-reference.

        :param text: String
        :param host: Host of URL
        :param path: Path of URL
        :param author_uid: User.uid
        :param statement_uid: Statement.uid
        :param issue_uid: Issue.uid
        :return: None
        """
        self.text = text
        self.host = host
        self.path = path
        self.author_uid = author_uid
        self.statement_uid = statement_uid
        self.issue_uid = issue_uid

    def get_statement_text(self, html: bool = False) -> str:
        """
        Gets the current references text from the statement, without trailing punctuation.

        :param html: If True, returns a html span for coloring.
        :return:
        """
        db_statement = DBDiscussionSession.query(Statement).get(self.statement_uid)
        return db_statement.get_text(html)

    def __json__(self, _request=None):
        return {
            "uid": self.uid,
            "title": self.text,
            "host": self.host,
            "path": self.path,
            "statement-uid": self.statement_uid,
            "author": self.author
        }


class StatementOrigins(DiscussionBase):
    """
    Add an origin to the statement. Comes from external services, like the EDEN-aggregators.
    """
    __tablename__ = 'statement_origins'
    uid: int = Column(Integer, primary_key=True)
    entity_id: str = Column(Text, nullable=True)
    aggregate_id: str = Column(Text, nullable=True)
    version: int = Column(Integer, nullable=True)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'), nullable=False)
    author: str = Column(Text, nullable=True)
    created = Column(ArrowType, default=get_now())

    statement: Statement = relationship('Statement', foreign_keys=[statement_uid])

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
    uid: int = Column(Integer, primary_key=True)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    issue_uid: int = Column(Integer, ForeignKey('issues.uid'))

    statement: Statement = relationship('Statement')
    issue: Issue = relationship('Issue')

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
    uid: int = Column(Integer, primary_key=True)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    user_uid: int = Column(Integer, ForeignKey('users.uid'))

    statement: Statement = relationship('Statement')

    user: User = relationship('User')

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
    uid: int = Column(Integer, primary_key=True)
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    user_uid: int = Column(Integer, ForeignKey('users.uid'))

    argument: 'Argument' = relationship('Argument', foreign_keys=[argument_uid])
    user: User = relationship('User', foreign_keys=[user_uid])

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
    uid: int = Column(Integer, primary_key=True)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'), nullable=True)
    content: str = Column(Text, nullable=False)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_disabled: bool = Column(Boolean, nullable=False)

    statement: Statement = relationship('Statement', foreign_keys=[statement_uid], back_populates='all_textversions')
    author: User = relationship('User', foreign_keys=[author_uid])

    def __init__(self, content, author: User, statement: Statement, is_disabled=False, date: datetime = None):
        """
        Initializes a row in current text versions-table

        :param content: String
        :param author: User.uid
        :return: None
        """
        self.content = content
        self.author = author
        self.timestamp = date or get_now()
        self.statement = statement
        self.is_disabled = is_disabled

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
    uid: int = Column(Integer, primary_key=True)
    premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    is_negated: bool = Column(Boolean, nullable=False)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    issue_uid: int = Column(Integer, ForeignKey('issues.uid'))
    is_disabled: bool = Column(Boolean, nullable=False)

    premisegroup: 'PremiseGroup' = relationship('PremiseGroup', foreign_keys=[premisegroup_uid],
                                                back_populates='premises')
    argument: 'Argument' = relationship('Argument', foreign_keys=[premisegroup_uid],
                                        primaryjoin='Argument.premisegroup_uid == Premise.premisegroup_uid',
                                        back_populates='premises')

    statement: Statement = relationship(Statement, foreign_keys=[statement_uid], back_populates='premises')
    author: User = relationship(User, foreign_keys=[author_uid])
    issue: Issue = relationship(Issue, foreign_keys=[issue_uid], back_populates="premises")

    def __init__(self, premisesgroup: "PremiseGroup", statement: Statement, is_negated: Boolean, author: User,
                 issue: Issue, is_disabled=False):
        """
        Initializes a row in current premises-table

        :param premisesgroup: PremiseGroup
        :param statement: Statement
        :param is_negated: Boolean
        :param author: User
        :param issue: Issue
        :param is_disabled: Boolean
        :return: None
        """
        self.premisegroup = premisesgroup
        self.statement = statement
        self.is_negated = is_negated
        self.author = author
        self.timestamp = get_now()
        self.issue = issue
        self.is_disabled = is_disabled

    def set_disabled(self, is_disabled: Boolean):
        """
        Disables current premise

        :param is_disabled: Boolean
        :return: None
        """
        self.is_disabled = is_disabled

    def set_statement(self, statement: Statement):
        """
        Sets statement fot his Premise

        :param statement: Statement.uid
        :return: None
        """
        self.statement_uid = statement

    def set_premisegroup(self, premisegroup: "PremiseGroup"):
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
            'premisegroup_uid': self.premisegroup.uid,
            'statement_uid': self.statement.uid,
            'is_negated': self.is_negated,
            'author_uid': self.author.uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp),
            'issue_uid': self.issue.uid,
            'is_disabled': self.is_disabled
        }


class PremiseGroup(DiscussionBase):
    """
    PremiseGroup-table with several columns.
    Each premisesGroup has a id and an author
    """
    __tablename__ = 'premisegroups'
    uid: int = Column(Integer, primary_key=True)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))

    author: List[User] = relationship(User, foreign_keys=[author_uid])
    premises: List[Premise] = relationship(Premise, back_populates='premisegroup')
    arguments: List['Argument'] = relationship('Argument', back_populates='premisegroup')

    def __init__(self, author: User):
        """
        Initializes a row in current premisesGroup-table

        :param author: User
        :return: None
        """
        self.author = author

    def get_text(self):
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=self.uid).join(Statement).all()
        texts = [premise.get_text() for premise in db_premises]
        lang = DBDiscussionSession.query(Statement).get(db_premises[0].statement.uid).lang
        return ' {} '.format(Translator(lang).get(_.aand)).join(texts)


class Argument(DiscussionBase, GraphNode, metaclass=GraphNodeMeta):
    """
    Argument-table with several columns.
    Each argument has justifying statement(s) (premises) and the the statement-to-be-justified (argument or statement).
    Additionally there is a relation, timestamp, author, ...
    """
    __tablename__ = 'arguments'
    uid: int = Column(Integer, primary_key=True)
    premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'), nullable=False)
    conclusion_uid: int = Column(Integer, ForeignKey('statements.uid'), nullable=True)
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'), nullable=True)
    is_supportive: bool = Column(Boolean, nullable=False)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp: ArrowType = Column(ArrowType, default=get_now())
    issue_uid: int = Column(Integer, ForeignKey('issues.uid'))
    is_disabled: bool = Column(Boolean, nullable=False)

    premisegroup: PremiseGroup = relationship(PremiseGroup, foreign_keys=[premisegroup_uid], back_populates='arguments')
    premises: List[Premise] = relationship(Premise, foreign_keys=[Premise.premisegroup_uid],
                                           primaryjoin='Argument.premisegroup_uid == Premise.premisegroup_uid',
                                           back_populates='argument')
    conclusion: Optional[Statement] = relationship('Statement', foreign_keys=[conclusion_uid],
                                                   back_populates='arguments')

    issue: Issue = relationship(Issue, foreign_keys=[issue_uid], back_populates='all_arguments')

    author: User = relationship('User', back_populates='arguments')
    attacks: Optional['Argument'] = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid,
                                                 back_populates='attacked_by')
    attacked_by: List['Argument'] = relationship('Argument', remote_side=argument_uid, back_populates='attacks')

    clicks = relationship('ClickedArgument')

    # these are only for legacy support. use attacked_by and author instead
    issues: Issue = relationship(Issue, foreign_keys=[issue_uid], back_populates='all_arguments')
    arguments: List['Argument'] = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid, uselist=True)
    users: User = relationship('User', foreign_keys=[author_uid])

    def __init__(self, premisegroup: PremiseGroup, is_supportive: bool, author: User, issue: Issue,
                 conclusion: Statement = None,
                 argument: int = None,
                 is_disabled: bool = False,
                 timestamp: datetime = None):
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
        self.premisegroup = premisegroup
        self.conclusion = conclusion
        self.argument_uid = None if argument == 0 else argument
        self.is_supportive = is_supportive
        self.author = author
        self.argument_uid = argument
        self.issue = issue
        self.is_disabled = is_disabled
        self.timestamp = arrow.get(timestamp) or get_now()

    def __repr__(self):
        return f"<Argument: {self.uid} {'support' if self.is_supportive else 'attack'}>"

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
        if not self.conclusion:
            return ''
        return self.conclusion.get_text(html)

    def get_premisegroup_text(self) -> str:
        db_premisegroup = DBDiscussionSession.query(PremiseGroup).get(self.premisegroup_uid)
        return db_premisegroup.get_text()

    def get_attacked_argument_text(self) -> Dict[str, str]:
        attacked_argument: 'Argument' = self.attacks
        if attacked_argument:
            return {
                'conclusion': attacked_argument.get_conclusion_text(),
                'premise': attacked_argument.get_premisegroup_text(),
            }
        return {}

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

    def to_d3_dict(self):
        return {
            'id': 'argument_' + str(self.uid),
            'label': '',
            'type': '',
            'edge_source': ['statement_' + str(premise.statement_uid) for premise in self.premises if
                            not premise.is_disabled],
            'edge_target': 'statement_' + str(
                self.conclusion_uid) if self.conclusion_uid else 'argument_' + str(self.argument_uid),
            'timestamp': self.timestamp.timestamp
        }

    def get_sub_nodes(self) -> Set[GraphNode]:
        nodes: Set[GraphNode] = set(
            [premise.statement for premise in self.premises if not premise.is_disabled])

        return nodes.union(set(self.attacked_by))

    def aif_node(self):
        return {
            "nodeID": f"argument_{self.uid}",
            "type": "RA" if self.is_supportive else "CA",
            "timestamp": str(self.timestamp)
        }


class History(DiscussionBase):
    """
    History-table with several columns.
    Each user will be tracked
    """
    __tablename__ = 'history'
    uid: int = Column(Integer, primary_key=True)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    path: str = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())

    author: User = relationship('User', foreign_keys=[author_uid], back_populates='history')

    def __init__(self, author: User, path):
        """
        Inits a row in current history table

        :param author: User.uid
        :param path: String
        :return: None
        """
        self.author_uid = author.uid
        self.path = path
        self.timestamp = get_now()


class ClickedArgument(DiscussionBase):
    """
    Vote-table with several columns for arguments.
    An argument will be voted, if the user has selected the premise and conclusion of this argument.
    """
    __tablename__ = 'clicked_arguments'
    uid: int = Column(Integer, primary_key=True)
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_up_vote: bool = Column(Boolean, nullable=False)
    is_valid: bool = Column(Boolean, nullable=False)

    argument: Argument = relationship('Argument', back_populates='clicks')
    user: User = relationship('User')

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
    uid: int = Column(Integer, primary_key=True)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_up_vote: bool = Column(Boolean, nullable=False)
    is_valid: bool = Column(Boolean, nullable=False)

    statement: Statement = relationship('Statement', back_populates='clicks')
    user: User = relationship('User', foreign_keys=[author_uid], back_populates='clicked_statements')

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

    def to_dict(self, lang: str) -> Dict[str, Any]:
        """
        Returns a dictionary-based representaiton of the ClickedStatement object.

        :param lang: A string representing the language used by the timestamp.
        :return: A dictionary representation of the object.
        """
        return {
            'uid': self.uid,
            'timestamp': sql_timestamp_pretty_print(self.timestamp, lang),
            'is_up_vote': self.is_up_vote,
            'is_valid': self.is_valid,
            'statement_uid': self.statement_uid,
            'content': self.statement.get_text()
        }


class MarkedArgument(DiscussionBase):
    """
    MarkedArgument-table with several columns.
    """
    __tablename__ = 'marked_arguments'
    uid: int = Column(Integer, primary_key=True)
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())

    argument: Argument = relationship('Argument', foreign_keys=[argument_uid])
    user: User = relationship('User', foreign_keys=[author_uid])

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
    uid: int = Column(Integer, primary_key=True)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())

    statement: Statement = relationship('Statement', foreign_keys=[statement_uid])
    user: User = relationship('User', foreign_keys=[author_uid])

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
    uid: int = Column(Integer, primary_key=True)
    from_author_uid: int = Column(Integer, ForeignKey('users.uid'))
    to_author_uid: int = Column(Integer, ForeignKey('users.uid'))
    topic: str = Column(Text, nullable=False)
    content: str = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())
    read: bool = Column(Boolean, nullable=False)
    is_inbox: bool = Column(Boolean, nullable=False)

    sender: User = relationship('User', foreign_keys=[from_author_uid])
    receiver: User = relationship('User', foreign_keys=[to_author_uid])

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

    @abstractmethod
    def get_issues(self) -> [Issue]:
        """Get the issues to which the statements of this review case belong"""
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
    uid: int = Column(Integer, primary_key=True)
    detector_uid: int = Column(Integer, ForeignKey('users.uid'))
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed: bool = Column(Boolean, nullable=False, default=False)
    reason_uid: int = Column(Integer, ForeignKey('review_delete_reasons.uid'))
    is_revoked: bool = Column(Boolean, nullable=False, default=False)

    detector: User = relationship('User', foreign_keys=[detector_uid])
    argument: Optional[Argument] = relationship('Argument', foreign_keys=[argument_uid])
    statement: Optional[Statement] = relationship('Statement', foreign_keys=[statement_uid])
    reason: 'ReviewDeleteReason' = relationship('ReviewDeleteReason', foreign_keys=[reason_uid])

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

    def get_issues(self) -> [Issue]:
        if self.argument:
            return [self.argument.issue]
        return self.statement.issues


class ReviewEdit(AbstractReviewCase):
    """
    -table with several columns.
    """
    __tablename__ = 'review_edits'
    uid: int = Column(Integer, primary_key=True)
    detector_uid: int = Column(Integer, ForeignKey('users.uid'))
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed: bool = Column(Boolean, nullable=False, default=False)
    is_revoked: bool = Column(Boolean, nullable=False, default=False)

    detector: User = relationship('User', foreign_keys=[detector_uid])
    argument: Optional[Argument] = relationship('Argument', foreign_keys=[argument_uid])
    statement: Optional[Statement] = relationship('Statement', foreign_keys=[statement_uid])

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

    def get_issues(self) -> [Issue]:
        if self.argument:
            return [self.argument.issue]
        return self.statement.issues


class ReviewEditValue(DiscussionBase):
    """
    ReviewEditValue-table with several columns.
    """
    __tablename__ = 'review_edit_values'
    uid: int = Column(Integer, primary_key=True)
    review_edit_uid: int = Column(Integer, ForeignKey('review_edits.uid'))
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    typeof: str = Column(Text, nullable=False)
    content: str = Column(Text, nullable=False)

    review: ReviewEdit = relationship('ReviewEdit', foreign_keys=[review_edit_uid])
    statement: Statement = relationship('Statement', foreign_keys=[statement_uid])

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
    uid: int = Column(Integer, primary_key=True)
    detector_uid: int = Column(Integer, ForeignKey('users.uid'))
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed: bool = Column(Boolean, nullable=False, default=False)
    is_revoked: bool = Column(Boolean, nullable=False, default=False)

    detector: User = relationship('User', foreign_keys=[detector_uid])
    argument: Optional[Argument] = relationship('Argument', foreign_keys=[argument_uid])
    statement: Optional[Statement] = relationship('Statement', foreign_keys=[statement_uid])

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

    def get_issues(self) -> [Issue]:
        if self.argument:
            return [self.argument.issue]
        return self.statement.issues

    def is_locked(self) -> bool:
        lock = DBDiscussionSession.query(OptimizationReviewLocks).filter(
            OptimizationReviewLocks.review_optimization_uid == self.uid).one_or_none()
        return lock is not None


class ReviewDuplicate(AbstractReviewCase):
    """
    ReviewDuplicate-table with several columns.
    """
    __tablename__ = 'review_duplicates'
    uid: int = Column(Integer, primary_key=True)
    detector_uid: int = Column(Integer, ForeignKey('users.uid'))
    duplicate_statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    original_statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed: bool = Column(Boolean, nullable=False, default=False)
    is_revoked: bool = Column(Boolean, nullable=False, default=False)

    detector: User = relationship('User', foreign_keys=[detector_uid])
    duplicate_statement: Statement = relationship('Statement', foreign_keys=[duplicate_statement_uid])
    original_statement: Statement = relationship('Statement', foreign_keys=[original_statement_uid])

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

    def get_issues(self) -> [Issue]:
        return self.duplicate_statement.issues


class ReviewMerge(AbstractReviewCase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_merge'
    uid: int = Column(Integer, primary_key=True)
    detector_uid: int = Column(Integer, ForeignKey('users.uid'))
    premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed: bool = Column(Boolean, nullable=False, default=False)
    is_revoked: bool = Column(Boolean, nullable=False, default=False)

    detector: User = relationship('User', foreign_keys=[detector_uid])
    premisegroup: PremiseGroup = relationship('PremiseGroup', foreign_keys=[premisegroup_uid])

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

    def get_issues(self) -> [Issue]:
        return [self.premisegroup.premises[0].issue]


class ReviewSplit(AbstractReviewCase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_split'
    uid: int = Column(Integer, primary_key=True)
    detector_uid: int = Column(Integer, ForeignKey('users.uid'))
    premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())
    is_executed: bool = Column(Boolean, nullable=False, default=False)
    is_revoked: bool = Column(Boolean, nullable=False, default=False)

    detector: User = relationship('User', foreign_keys=[detector_uid])
    premisegroup: PremiseGroup = relationship('PremiseGroup', foreign_keys=[premisegroup_uid])

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

    def get_issues(self) -> [Issue]:
        return [self.premisegroup.premises[0].issue]


class ReviewSplitValues(DiscussionBase):
    """
    Review-table with several columns.
    """
    __tablename__ = 'review_split_values'
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_split.uid'))
    content: str = Column(Text, nullable=False)

    review: ReviewSplit = relationship('ReviewSplit', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_merge.uid'))
    content: str = Column(Text, nullable=False)

    review: ReviewMerge = relationship('ReviewMerge', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reason: str = Column(Text, nullable=False, unique=True)

    def __init__(self, reason: str):
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
    uid: int = Column(Integer, primary_key=True)
    reviewer_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_uid: int = Column(Integer, ForeignKey('review_deletes.uid'))
    is_okay: bool = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer: User = relationship('User', foreign_keys=[reviewer_uid])
    review: ReviewDelete = relationship('ReviewDelete', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reviewer_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_uid: int = Column(Integer, ForeignKey('review_duplicates.uid'))
    is_okay: bool = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer: User = relationship('User', foreign_keys=[reviewer_uid])
    review: ReviewDuplicate = relationship('ReviewDuplicate', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reviewer_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_uid: int = Column(Integer, ForeignKey('review_edits.uid'))
    is_okay: bool = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer: User = relationship('User', foreign_keys=[reviewer_uid])
    review: ReviewEdit = relationship('ReviewEdit', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reviewer_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_uid: int = Column(Integer, ForeignKey('review_optimizations.uid'))
    is_okay: bool = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer: User = relationship('User', foreign_keys=[reviewer_uid])
    review: ReviewOptimization = relationship('ReviewOptimization', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reviewer_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_uid: int = Column(Integer, ForeignKey('review_split.uid'))
    should_split: bool = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer: User = relationship('User', foreign_keys=[reviewer_uid])
    review: ReviewSplit = relationship('ReviewSplit', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reviewer_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_uid: int = Column(Integer, ForeignKey('review_merge.uid'))
    should_merge: bool = Column(Boolean, nullable=False, default=False)
    timestamp = Column(ArrowType, default=get_now())

    reviewer: User = relationship('User', foreign_keys=[reviewer_uid])
    review: ReviewMerge = relationship('ReviewMerge', foreign_keys=[review_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reputator_uid: int = Column(Integer, ForeignKey('users.uid'))
    reputation_uid: int = Column(Integer, ForeignKey('reputation_reasons.uid'))
    timestamp = Column(ArrowType, default=get_now())

    user: User = relationship('User', foreign_keys=[reputator_uid])
    reputations: 'ReputationReason' = relationship('ReputationReason', foreign_keys=[reputation_uid])  # deprecated
    reason_for_reputation: 'ReputationReason' = relationship('ReputationReason', foreign_keys=[reputation_uid])

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
    uid: int = Column(Integer, primary_key=True)
    reason: str = Column(Text, nullable=False, unique=True)
    points: int = Column(Integer, nullable=False)

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
    author_uid: int = Column(Integer, ForeignKey('users.uid'), primary_key=True)
    review_optimization_uid: int = Column(Integer, ForeignKey('review_optimizations.uid'))
    locked_since = Column(ArrowType, default=get_now(), nullable=True)

    author: User = relationship('User', foreign_keys=[author_uid])
    review_optimization: ReviewOptimization = relationship('ReviewOptimization', foreign_keys=[review_optimization_uid])

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
    uid: int = Column(Integer, primary_key=True)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    review_edit_uid: int = Column(Integer, ForeignKey('review_edits.uid'), nullable=True)
    review_delete_uid: int = Column(Integer, ForeignKey('review_deletes.uid'), nullable=True)
    review_optimization_uid: int = Column(Integer, ForeignKey('review_optimizations.uid'), nullable=True)
    review_duplicate_uid: int = Column(Integer, ForeignKey('review_duplicates.uid'), nullable=True)
    review_merge_uid: int = Column(Integer, ForeignKey('review_merge.uid'), nullable=True)
    review_split_uid: int = Column(Integer, ForeignKey('review_split.uid'), nullable=True)
    was_ongoing = Column(Boolean)
    timestamp = Column(ArrowType, default=get_now())

    # deprecated
    author: User = relationship('User', foreign_keys=[author_uid])
    edit: Optional[ReviewEdit] = relationship('ReviewEdit', foreign_keys=[review_edit_uid])
    delete: Optional[ReviewDelete] = relationship('ReviewDelete', foreign_keys=[review_delete_uid])
    optimization: Optional[ReviewOptimization] = relationship('ReviewOptimization',
                                                              foreign_keys=[review_optimization_uid])
    duplicate: Optional[ReviewDuplicate] = relationship('ReviewDuplicate', foreign_keys=[review_duplicate_uid])
    merge: Optional[ReviewMerge] = relationship('ReviewMerge', foreign_keys=[review_merge_uid])
    split: Optional[ReviewSplit] = relationship('ReviewSplit', foreign_keys=[review_split_uid])

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
    uid: int = Column(Integer, primary_key=True)
    author_uid: int = Column(Integer, ForeignKey('users.uid'))
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())

    author: User = relationship('User', foreign_keys=[author_uid])
    argument: Argument = relationship('Argument', foreign_keys=[argument_uid])
    statement: Statement = relationship('Statement', foreign_keys=[statement_uid])

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
    uid: int = Column(Integer, primary_key=True)
    old_author_uid: int = Column(Integer, ForeignKey('users.uid'))
    new_author_uid: int = Column(Integer, ForeignKey('users.uid'))
    textversion_uid: int = Column(Integer, ForeignKey('textversions.uid'), nullable=True)
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'), nullable=True)

    old_author: User = relationship('User', foreign_keys=[old_author_uid])
    new_author: User = relationship('User', foreign_keys=[new_author_uid])
    textversion: TextVersion = relationship('TextVersion', foreign_keys=[textversion_uid])
    argument: Argument = relationship('Argument', foreign_keys=[argument_uid])

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
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_duplicates.uid'))
    bend_position: bool = Column(Boolean, nullable=False)
    statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    premise_uid: int = Column(Integer, ForeignKey('premises.uid'))

    timestamp = Column(ArrowType, default=get_now())
    review: ReviewDuplicate = relationship('ReviewDuplicate', foreign_keys=[review_uid])
    argument: Argument = relationship('Argument', foreign_keys=[argument_uid])
    statement: Statement = relationship('Statement', foreign_keys=[statement_uid])
    premises: Premise = relationship('Premise', foreign_keys=[premise_uid])

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
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_split.uid'))
    old_premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    new_premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())

    review: ReviewSplit = relationship('ReviewSplit', foreign_keys=[review_uid])
    old_premisegroup: PremiseGroup = relationship('PremiseGroup', foreign_keys=[old_premisegroup_uid])
    new_premisegroup: PremiseGroup = relationship('PremiseGroup', foreign_keys=[new_premisegroup_uid])

    def __init__(self, review, old_premisegroup, new_premisegroup: PremiseGroup):
        """
        Inits a row in current table

        :param review: ReviewDuplicate.uid
        :param old_premisegroup: PremiseGroup.uid
        :param new_premisegroup: PremiseGroup.uid
        """
        self.review_uid = review
        self.old_premisegroup_uid = old_premisegroup
        self.new_premisegroup = new_premisegroup
        self.timestamp = get_now()


class PremiseGroupMerged(DiscussionBase):
    """
    Table with several columns to indicate which statement should be merged to a new one
    """
    __tablename__ = 'premisegroup_merged'
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_merge.uid'))
    old_premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    new_premisegroup_uid: int = Column(Integer, ForeignKey('premisegroups.uid'))
    timestamp = Column(ArrowType, default=get_now())

    review: ReviewMerge = relationship('ReviewMerge', foreign_keys=[review_uid])
    old_premisegroup: PremiseGroup = relationship('PremiseGroup', foreign_keys=[old_premisegroup_uid])
    new_premisegroup: PremiseGroup = relationship('PremiseGroup', foreign_keys=[new_premisegroup_uid])

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
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_split.uid'))
    old_statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    new_statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())

    review: ReviewSplit = relationship('ReviewSplit', foreign_keys=[review_uid])
    old_statement: Statement = relationship('Statement', foreign_keys=[old_statement_uid])
    new_statement: Statement = relationship('Statement', foreign_keys=[new_statement_uid])

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
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_split.uid'))
    old_statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    new_statement_uid: int = Column(Integer, ForeignKey('statements.uid'))
    timestamp = Column(ArrowType, default=get_now())

    review: ReviewSplit = relationship('ReviewSplit', foreign_keys=[review_uid])
    old_statement: Statement = relationship('Statement', foreign_keys=[old_statement_uid])
    new_statement: Statement = relationship('Statement', foreign_keys=[new_statement_uid])

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
    uid: int = Column(Integer, primary_key=True)
    review_uid: int = Column(Integer, ForeignKey('review_split.uid'))
    argument_uid: int = Column(Integer, ForeignKey('arguments.uid'))
    timestamp = Column(ArrowType, default=get_now())

    review: ReviewSplit = relationship('ReviewSplit', foreign_keys=[review_uid])
    argument: Argument = relationship('Argument', foreign_keys=[argument_uid])

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
    uid: int = Column(Integer, primary_key=True)
    title: str = Column(Text, nullable=False)
    author: str = Column(Text, nullable=False)
    date = Column(ArrowType, nullable=False)
    news: str = Column(Text, nullable=False)

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
    id: int = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    token: str = Column(String, nullable=False, unique=True)
    owner: str = Column(Text, nullable=False)
    disabled: bool = Column(Boolean, nullable=False, server_default="False")

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
    uid: int = Column(Integer, primary_key=True)
    service: str = Column(Text, nullable=False)
    long_url: str = Column(Text, nullable=False)
    short_url: str = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())

    def __init__(self, service, long_url, short_url):
        self.service = service
        self.long_url = long_url
        self.short_url = short_url
        self.timestamp = get_now()

    def update_short_url(self, short_url):
        self.short_url = short_url
        self.timestamp = get_now()


class DecisionProcess(DiscussionBase):
    __tablename__ = 'decidotron_decision_process'
    issue_id: int = Column(Integer, ForeignKey(Issue.uid), primary_key=True)
    budget: int = Column(Integer, nullable=False, doc="Budget for an issue in cents")
    currency_symbol: str = Column(String, nullable=True)
    positions_end: datetime = Column(DateTime, nullable=True)
    votes_start: datetime = Column(DateTime, nullable=True)
    votes_end: datetime = Column(DateTime, nullable=True)
    host: str = Column(String, nullable=False, doc="The host of the associated decidotron instance")
    max_position_cost: int = Column(Integer, nullable=True)
    min_position_cost: int = Column(Integer, nullable=False, server_default="0")

    issue = relationship(Issue,
                         back_populates='decision_process')  # backref=backref('decision_process', cascade="all, delete-orphan"))

    def __init__(self, issue_id: int, budget: int, host: str, currency_symbol="€",
                 positions_end: datetime = None,
                 votes_start: datetime = None,
                 votes_end: datetime = None,
                 max_position_cost: int = None,
                 min_position_cost: int = 0):
        if budget <= 0:
            raise ValueError("The budget has to be greater than 0!")
        self.issue_id = issue_id
        self.budget = budget
        self.host = host
        self.currency_symbol = currency_symbol
        self.positions_end = positions_end
        self.votes_start = votes_start
        self.votes_end = votes_end
        self.max_position_cost = max_position_cost if max_position_cost and max_position_cost < budget else budget
        self.min_position_cost = min_position_cost if min_position_cost > 0 else 0

    def budget_str(self):
        return "{currency_symbol} {:.2f}".format(self.budget, currency_symbol=self.currency_symbol)

    @staticmethod
    def by_id(issue_id: int) -> 'DecisionProcess':
        return DBDiscussionSession.query(DecisionProcess).get(issue_id)

    def position_ended(self):
        return bool(self.positions_end) and self.positions_end < datetime.now()

    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "budget": self.budget,
            "currency_symbol": self.currency_symbol,
            "budget_string": self.budget_str(),
            "positions_end": self.positions_end,
            "position_ended": self.position_ended(),
            "votes_start": self.votes_start,
            "votes_started": self.votes_start < datetime.now() if bool(self.votes_start) else True,
            "votes_end": self.votes_end,
            "votes_ended": self.votes_end < datetime.now() if bool(self.votes_end) else False,
            "max_position_cost": self.max_position_cost if self.max_position_cost else self.budget,
            "min_position_cost": self.min_position_cost,
        }


class PositionCost(DiscussionBase):
    __tablename__ = 'decidotron_position_cost'
    position_id: int = Column(Integer, ForeignKey(Statement.uid), primary_key=True)
    cost: int = Column(Integer, nullable=False)

    def __init__(self, position: Statement, cost: int):
        self.position_id = position.uid
        self.cost = cost
