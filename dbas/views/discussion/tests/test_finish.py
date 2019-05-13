import unittest
from unittest import mock

from pyramid import testing

from dbas.database.discussion_model import User, Argument
from dbas.events import UserArgumentAgreement
from dbas.helper.test import verify_dictionary_of_view
from dbas.tests.utils import construct_dummy_request
from dbas.views import finish, DBDiscussionSession


class DiscussionFinishViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def test_page(self):
        argument_uid = 10
        request = construct_dummy_request(matchdict={'argument_id': argument_uid, 'slug': 'cat-or-dog'})
        request.registry.notify = mock.Mock()
        response = finish(request)
        verify_dictionary_of_view(response)
        anonymous_user: User = DBDiscussionSession.query(User).get(1)
        argument: Argument = DBDiscussionSession.query(Argument).filter(Argument.uid == argument_uid).first()
        request.registry.notify.assert_called_with(UserArgumentAgreement(anonymous_user, argument))
