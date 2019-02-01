from dataclasses import dataclass

from dbas.database.discussion_model import Issue, User, Argument


@dataclass
class ParticipatedInDiscussion:
    user: User
    issue: Issue


@dataclass
class UserArgumentAgreement:
    user: User
    argument: Argument
