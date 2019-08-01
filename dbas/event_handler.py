from pyramid.events import subscriber, NewResponse

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.events import ParticipatedInDiscussion, UserArgumentAgreement, UserStatementAttitude
from dbas.handler.voting import add_click_for_argument, add_click_for_statement


@subscriber(ParticipatedInDiscussion)
def user_participated(event: ParticipatedInDiscussion):
    event.user.participates_in.append(event.issue)


@subscriber(UserArgumentAgreement)
def user_agrees_with_argument(event: UserArgumentAgreement):
    add_click_for_argument(event.argument, event.user)


@subscriber(UserStatementAttitude)
def user_attitude_on_statement(event: UserStatementAttitude):
    add_click_for_statement(event.statement, event.user, event.is_supportive)


@subscriber(NewResponse)
def update_last_action(event: NewResponse):
    user = DBDiscussionSession.query(User).filter_by(nickname=event.request.authenticated_userid).first()
    if user is not None:
        user.update_last_action()
