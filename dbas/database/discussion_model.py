"""
D-BAS database Model

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import arrow
from cryptacular.bcrypt import BCRYPTPasswordManager
from dbas.database import DBDiscussionSession, DiscussionBase
from slugify import slugify
from sqlalchemy import Integer, Text, Boolean, Column, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType


def sql_timestamp_pretty_print(ts, lang, humanize=True, with_exact_time=False):
    """
    Pretty printing for sql timestamp in dependence of the language.

    :param ts: timestamp (arrow) as string
    :param lang: language
    :param humanize: Boolean
    :param with_exact_time: Boolean
    :return:
    """
    ts = ts.replace(hours=-2)
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
    return arrow.utcnow().to('local')
    # return arrow.get(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


class Issue(DiscussionBase):
    """
    issue-table with several column.
    Each issue has text and a creation date
    """
    __tablename__ = 'issues'
    uid = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    info = Column(Text, nullable=False)
    long_info = Column(Text, nullable=False)
    date = Column(ArrowType, default=get_now())
    author_uid = Column(Integer, ForeignKey('users.uid'))
    lang_uid = Column(Integer, ForeignKey('languages.uid'))
    is_disabled = Column(Boolean, nullable=False)

    users = relationship('User', foreign_keys=[author_uid])
    languages = relationship('Language', foreign_keys=[lang_uid])

    def __init__(self, title, info, long_info, author_uid, lang_uid, is_disabled=False):
        """
        Initializes a row in current position-table
        """
        self.title = title
        self.info = info
        self.long_info = long_info
        self.author_uid = author_uid
        self.lang_uid = lang_uid
        self.is_disabled = is_disabled

    @classmethod
    def by_text(cls):
        """Return a query of positions sorted by text."""
        return DBDiscussionSession.query(Issue).order_by(Issue.text)

    def get_slug(self):
        return slugify(self.title)

    @hybrid_property
    def lang(self):
        return DBDiscussionSession.query(Language).get(self.lang_uid).ui_locales

    def set_disable(self, is_disabled):
        """

        :param is_disabled:
        :return:
        """
        self.is_disabled = is_disabled


class Language(DiscussionBase):
    """
    language-table with several column.
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

    groups = relationship('Group', foreign_keys=[group_uid], order_by='Group.uid')

    def __init__(self, firstname, surname, nickname, email, password, gender, group_uid, token='', token_timestamp=None):
        """
        Initializes a row in current user-table

        :param firstname:
        :param surname:
        :param nickname:
        :param email:
        :param password:
        :param gender:
        :param group_uid:
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

    @classmethod
    def by_surname(cls):
        """
        Return a query of users sorted by surname.

        :return:
        """
        return DBDiscussionSession.query(User).order_by(User.surname)

    def validate_password(self, password):
        manager = BCRYPTPasswordManager()
        return manager.check(self.password, password)

    def update_last_login(self):
        self.last_login = get_now()

    def update_last_action(self):
        self.last_action = get_now()

    def update_token_timestamp(self):
        self.token_timestamp = get_now()

    def set_token(self, token):
        self.token = token

    def set_public_nickname(self, nick):
        self.public_nickname = nick

    def get_global_nickname(self):
        # TODO CHANGE THIS IF YOU WANT TO SEE OTHER NAMES
        db_settings = DBDiscussionSession.query(Settings).get(self.uid)
        return self.firstname if db_settings.should_show_public_nickname else self.public_nickname


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

    def __init__(self, author_uid, send_mails, send_notifications, should_show_public_nickname=True, lang_uid=2, keep_logged_in=False):
        """
        Initializes a row in current settings-table

        :param author_uid:
        :param send_mails:
        :param send_notifications:
        :param should_show_public_nickname:
        :param lang_uid:
        :param keep_logged_in:
        """
        self.author_uid = author_uid
        self.should_send_mails = send_mails
        self.should_send_notifications = send_notifications
        self.should_show_public_nickname = should_show_public_nickname
        self.last_topic_uid = DBDiscussionSession.query(Issue).first().uid
        self.lang_uid = lang_uid
        self.keep_logged_in = keep_logged_in

    def set_send_mails(self, send_mails):
        self.should_send_mails = send_mails

    def set_send_notifications(self, send_notifications):
        self.should_send_notifications = send_notifications

    def set_show_public_nickname(self, should_show_public_nickname):
        self.should_show_public_nickname = should_show_public_nickname

    def set_last_topic_uid(self, uid):
        self.last_topic_uid = uid

    def set_lang_uid(self, lang_uid):
        self.lang_uid = lang_uid

    def should_hold_the_login(self, keep_logged_in):
        self.keep_logged_in = keep_logged_in


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
    is_disabled = Column(Boolean, nullable=False)

    textversions = relationship('TextVersion', foreign_keys=[textversion_uid])
    issues = relationship('Issue', foreign_keys=[issue_uid])

    def __init__(self, textversion, is_position, issue, is_disabled=False):
        """

        :param textversion:
        :param is_position:
        :param issue:
        :param is_disabled:
        """
        self.textversion_uid = textversion
        self.is_startpoint = is_position
        self.issue_uid = issue
        self.is_disabled = is_disabled

    def set_textversion(self, uid):
        self.textversion_uid = uid

    def set_disable(self, is_disabled):
        """

        :param is_disabled:
        :return:
        """
        self.is_disabled = is_disabled

    def set_position(self, is_position):
        """

        :param is_position:
        :return:
        """
        self.is_startpoint = is_position

    @hybrid_property
    def lang(self):
        return DBDiscussionSession.query(Issue).get(self.issue_uid).lang


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


class StatementSeenBy(DiscussionBase):
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
        self.statement_uid = statement_uid
        self.user_uid = user_uid


class ArgumentSeenBy(DiscussionBase):
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

    statements = relationship('Statement', foreign_keys=[statement_uid])
    users = relationship('User', foreign_keys=[author_uid])

    def __init__(self, content, author, statement_uid=None, is_disabled=False):
        """
        Initializes a row in current text versions-table
        :param content:
        :param author:
        :return:
        """
        self.content = content
        self.author_uid = author
        self.timestamp = get_now()
        self.statement_uid = statement_uid
        self.is_disabled = is_disabled

    def set_statement(self, statement_uid):
        """

        :param statement_uid:
        :return:
        """
        self.statement_uid = statement_uid

    def set_disable(self, is_disabled):
        """

        :param is_disabled:
        :return:
        """
        self.is_disabled = is_disabled


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
    uid = Column(Integer, primary_key=True)
    premisesgroup_uid = Column(Integer, ForeignKey('premisegroups.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    is_negated = Column(Boolean, nullable=False)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    timestamp = Column(ArrowType, default=get_now())
    issue_uid = Column(Integer, ForeignKey('issues.uid'))
    is_disabled = Column(Boolean, nullable=False)

    premisegroups = relationship('PremiseGroup', foreign_keys=[premisesgroup_uid])
    statements = relationship('Statement', foreign_keys=[statement_uid])
    users = relationship('User', foreign_keys=[author_uid])
    issues = relationship('Issue', foreign_keys=[issue_uid])

    def __init__(self, premisesgroup, statement, is_negated, author, issue, is_disabled=False):
        """
        Initializes a row in current premises-table

        :param premisesgroup:
        :param statement:
        :param is_negated:
        :param author:
        :param issue:
        :param is_disabled:
        :return:
        """
        self.premisesgroup_uid = premisesgroup
        self.statement_uid = statement
        self.is_negated = is_negated
        self.author_uid = author
        self.timestamp = get_now()
        self.issue_uid = issue
        self.is_disabled = is_disabled

    def set_disable(self, is_disabled):
        """

        :param is_disabled:
        :return:
        """
        self.is_disabled = is_disabled

    def set_statement(self, statement):
        self.statement_uid = statement

    def set_premisegroup(self, premisegroup):
        self.premisesgroup_uid = premisegroup


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
    timestamp = Column(ArrowType, default=get_now())
    issue_uid = Column(Integer, ForeignKey('issues.uid'))
    is_disabled = Column(Boolean, nullable=False)

    premisegroups = relationship('PremiseGroup', foreign_keys=[premisesgroup_uid])
    conclusion = relationship('Statement', foreign_keys=[conclusion_uid])
    users = relationship('User', foreign_keys=[author_uid])
    arguments = relationship('Argument', foreign_keys=[argument_uid], remote_side=uid)
    issues = relationship('Issue', foreign_keys=[issue_uid])

    def __init__(self, premisegroup, issupportive, author, issue, conclusion=None, argument=None, is_disabled=False):
        """
        Initializes a row in current argument-table
        :param premisegroup:
        :param issupportive:
        :param author:
        :param issue:
        :param conclusion: Default 0, which will be None
        :param argument: Default 0, which will be None
        :param: is_disabled
        :return:
        """
        self.premisesgroup_uid = premisegroup
        self.conclusion_uid = None if conclusion == 0 else conclusion
        self.argument_uid = None if argument == 0 else argument
        self.is_supportive = issupportive
        self.author_uid = author
        self.argument_uid = argument
        self.issue_uid = issue
        self.is_disabled = is_disabled

    def set_conclusions_argument(self, argument):
        self.argument_uid = argument

    def set_conclusion(self, conclusion):
        self.conclusion_uid = conclusion

    def set_disable(self, is_disabled):
        """

        :param is_disabled:
        :return:
        """
        self.is_disabled = is_disabled

    @hybrid_property
    def lang(self):
        return DBDiscussionSession.query(Issue).get(self.issue_uid).lang


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

    users = relationship('User', foreign_keys=[author_uid])

    def __init__(self, author_uid, path):
        """

        :param author_uid:
        :param path:
        :return:
        """
        self.author_uid = author_uid
        self.path = path
        self.timestamp = get_now()


class VoteArgument(DiscussionBase):
    """
    Vote-table with several columns for arguments.
    An argument will be voted, if the user has selected the premise and conclusion of this argument.
    """
    __tablename__ = 'vote_arguments'
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

        :param argument_uid:
        :param author_uid:
        :param is_up_vote:
        :param is_valid:
        :return:
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


class VoteStatement(DiscussionBase):
    """
    Vote-table with several columns for statements.
    A statement will be voted, if the user has selected the statement as justification or if the statement is used as part of an argument.
    """
    __tablename__ = 'vote_statements'
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

        :param statement_uid:
        :param author_uid:
        :param is_up_vote:
        :param is_valid:
        :return:
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


class Message(DiscussionBase):
    """

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


class ReviewDelete(DiscussionBase):
    """

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

    def __init__(self, detector, argument=None, statement=None, reason='', is_executed=False, is_revoked=False):
        """

        :param detector:
        :param argument:
        :param reason:
        :param is_executed:
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

        :param is_executed:
        :return:
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """

        :param is_revoked:
        :return:
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        self.timestamp = get_now()


class ReviewEdit(DiscussionBase):
    """

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

        :param detector:
        :param argument:
        :param is_executed:
        """
        self.detector_uid = detector
        self.argument_uid = argument
        self.statement_uid = statement
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """

        :param is_executed:
        :return:
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """

        :param is_revoked:
        :return:
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        self.timestamp = get_now()


class ReviewEditValue(DiscussionBase):
    __tablename__ = 'review_edit_values'
    uid = Column(Integer, primary_key=True)
    review_edit_uid = Column(Integer, ForeignKey('review_edits.uid'))
    statement_uid = Column(Integer, ForeignKey('statements.uid'))
    typeof = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, review_edit, statement, typeof, content):
        """

        :param review_edit:
        :param statement:
        :param typeof:
        :param content:
        """
        self.review_edit_uid = review_edit
        self.statement_uid = statement
        self.typeof = typeof
        self.content = content


class ReviewOptimization(DiscussionBase):
    """

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

        :param detector:
        :param argument:
        :param is_executed:
        """
        self.detector_uid = detector
        self.argument_uid = argument
        self.statement_uid = statement
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """

        :param is_executed:
        :return:
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """

        :param is_revoked:
        :return:
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        self.timestamp = get_now()


class ReviewDuplicate(DiscussionBase):
    """

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

    def __init__(self, detector, duplicate_statement=None, original_statement=None, is_executed=False, is_revoked=False):
        """

        :param detector:
        :param argument:
        :param is_executed:
        """
        self.detector_uid = detector
        self.duplicate_statement_uid = duplicate_statement
        self.original_statement_uid = original_statement
        self.timestamp = get_now()
        self.is_executed = is_executed
        self.is_revoked = is_revoked

    def set_executed(self, is_executed):
        """

        :param is_executed:
        :return:
        """
        self.is_executed = is_executed

    def set_revoked(self, is_revoked):
        """

        :param is_revoked:
        :return:
        """
        self.is_revoked = is_revoked

    def update_timestamp(self):
        self.timestamp = get_now()


class ReviewDeleteReason(DiscussionBase):
    """

    """
    __tablename__ = 'review_delete_reasons'
    uid = Column(Integer, primary_key=True)
    reason = Column(Text, nullable=False, unique=True)

    def __init__(self, reason):
        self.reason = reason


class LastReviewerDelete(DiscussionBase):
    """

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

        :param reviewer:
        :param review:
        :param is_okay:
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()


class LastReviewerDuplicate(DiscussionBase):
    """

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

        :param reviewer:
        :param review:
        :param is_okay:
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()


class LastReviewerEdit(DiscussionBase):
    """

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

        :param reviewer:
        :param review:
        :param is_okay:
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()


class LastReviewerOptimization(DiscussionBase):
    """

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

        :param reviewer:
        :param review:
        :param is_okay:
        """
        self.reviewer_uid = reviewer
        self.review_uid = review
        self.is_okay = is_okay
        self.timestamp = get_now()


class ReputationHistory(DiscussionBase):
    """

    """
    __tablename__ = 'reputation_history'
    uid = Column(Integer, primary_key=True)
    reputator_uid = Column(Integer, ForeignKey('users.uid'))
    reputation_uid = Column(Integer, ForeignKey('reputation_reasons.uid'))
    timestamp = Column(ArrowType, default=get_now())

    reputators = relationship('User', foreign_keys=[reputator_uid])
    reputations = relationship('ReputationReason', foreign_keys=[reputation_uid])

    def __init__(self, reputator, reputation, timestamp=get_now()):
        """

        :param reputator:
        """
        self.reputator_uid = reputator
        self.reputation_uid = reputation
        self.timestamp = timestamp


class ReputationReason(DiscussionBase):
    """

    """
    __tablename__ = 'reputation_reasons'
    uid = Column(Integer, primary_key=True)
    reason = Column(Text, nullable=False, unique=True)
    points = Column(Integer, nullable=False)

    def __init__(self, reason, points):
        """

        :param reason:
        :param points:
        """
        self.reason = reason
        self.points = points


class OptimizationReviewLocks(DiscussionBase):
    __tablename__ = 'optimization_review_locks'
    author_uid = Column(Integer, ForeignKey('users.uid'), primary_key=True)
    review_optimization_uid = Column(Integer, ForeignKey('review_optimizations.uid'))
    locked_since = Column(ArrowType, default=get_now(), nullable=True)

    authors = relationship('User', foreign_keys=[author_uid])
    review_optimization = relationship('ReviewOptimization', foreign_keys=[review_optimization_uid])

    def __init__(self, author, review_optimization):
        """

        :param author:
        :param review_optimization:
        """
        self.author_uid = author
        self.review_optimization_uid = review_optimization
        self.timestamp = get_now()


class ReviewCanceled(DiscussionBase):
    __tablename__ = 'review_canceled'
    uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    review_edit_uid = Column(Integer, ForeignKey('review_edits.uid'), nullable=True)
    review_delete_uid = Column(Integer, ForeignKey('review_deletes.uid'), nullable=True)
    review_optimization_uid = Column(Integer, ForeignKey('review_optimizations.uid'), nullable=True)
    review_duplicate_uid = Column(Integer, ForeignKey('review_duplicates.uid'), nullable=True)
    was_ongoing = Column(Boolean)
    timestamp = Column(ArrowType, default=get_now())

    authors = relationship('User', foreign_keys=[author_uid])
    edits = relationship('ReviewEdit', foreign_keys=[review_edit_uid])
    deletes = relationship('ReviewDelete', foreign_keys=[review_delete_uid])
    optimizations = relationship('ReviewOptimization', foreign_keys=[review_optimization_uid])
    duplicates = relationship('ReviewDuplicate', foreign_keys=[review_duplicate_uid])

    def __init__(self, author, review_edit=None, review_delete=None, review_optimization=None, review_duplicate=None, was_ongoing=False):
        """

        :param author:
        :param review_edit:
        :param review_delete:
        :param review_optimization:
        """
        self.author_uid = author
        self.review_edit_uid = review_edit
        self.review_delete_uid = review_delete
        self.review_optimization_uid = review_optimization
        self.review_duplicate_uid = review_duplicate
        self.was_ongoing = was_ongoing
        self.timestamp = get_now()


class RevokedContent(DiscussionBase):
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
        self.author_uid = author
        self.argument_uid = argument
        self.statement_uid = statement
        self.timestamp = get_now()


class RevokedContentHistory(DiscussionBase):
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
        self.old_author_uid = old_author_uid
        self.new_author_uid = new_author_uid
        self.textversion_uid = textversion_uid
        self.argument_uid = argument_uid


class RevokedDuplicate(DiscussionBase):
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
        self.review_uid = review
        self.bend_position = bend_position
        self.statement_uid = statement
        self.argument_uid = conclusion_of_argument
        self.premise_uid = premise
        self.timestamp = get_now()


class RSS(DiscussionBase):
    __tablename__ = 'rss'
    uid = Column(Integer, primary_key=True)
    author_uid = Column(Integer, ForeignKey('users.uid'))
    issue_uid = Column(Integer, ForeignKey('issues.uid'))
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(ArrowType, default=get_now())

    authors = relationship('User', foreign_keys=[author_uid])
    issues = relationship('Issue', foreign_keys=[issue_uid])

    def __init__(self, author, issue, title, description):
        self.author_uid = author
        self.issue_uid = issue
        self.title = title
        self.description = description
        self.timestamp = get_now()
