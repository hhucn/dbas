from dataclasses import dataclass

from dbas.database.discussion_model import Issue, User


@dataclass
class ParticipatedInDiscussion:
    user: User
    issue: Issue
