from pyramid.events import subscriber, NewResponse

from dbas.events import ParticipatedInDiscussion, UserArgumentAgreement
from dbas.handler.voting import add_click_for_argument


@subscriber(ParticipatedInDiscussion)
def user_participated(event: ParticipatedInDiscussion):
    event.user.participates_in.append(event.issue)


@subscriber(UserArgumentAgreement)
def user_agrees_with_argument(event: UserArgumentAgreement):
    add_click_for_argument(event.argument, event.user)


@subscriber(NewResponse)
def update_last_action(event: NewResponse):
    user = event.request.validated.get('user')
    if user is not None:
        user.update_last_action()
