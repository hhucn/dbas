from dbas.database.discussion_model import Issue, User


class ParticipatedInDiscussion(object):
    def __init__(self, user: User, issue: Issue):
        self.user = user
        self.issue = issue