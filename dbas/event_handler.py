from pyramid.events import subscriber

from dbas.events import ParticipatedInDiscussion


@subscriber(ParticipatedInDiscussion)
def user_participated(event: ParticipatedInDiscussion):
    event.user.participates_in.append(event.issue)
