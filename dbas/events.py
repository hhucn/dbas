from dataclasses import dataclass

from dbas.database.discussion_model import Issue, User, Argument, Statement


@dataclass
class ParticipatedInDiscussion:
    user: User
    issue: Issue


@dataclass
class UserArgumentAgreement:
    user: User
    argument: Argument


@dataclass
class UserStatementAttitude:
    user: User
    statement: Statement
    is_supportive: bool
