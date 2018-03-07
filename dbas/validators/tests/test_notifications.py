import unittest

from cornice import Errors
from nose.tools import assert_false, assert_equal, assert_true
from pyramid import testing

from dbas.lib import nick_of_anonymous_user
from dbas.validators.notifications import valid_notification_title, valid_notification_text, \
    valid_notification_recipient


class NotificationsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def __prepare_dict(self, jbody):
        request = testing.DummyRequest(json_body=jbody)
        setattr(request, 'errors', Errors())
        setattr(request, 'cookies', {'_LOCALE_': 'en'})
        request.validated = {}
        return request

    def __test_valid_notification_key(self, key, func):
        request = self.__prepare_dict({})
        response = func(request)
        assert_false(response)
        assert_equal(bool, type(response))

        for k, v in [('wrong_key', 'loooooooong striiiing'),
                     (key, 1234567890),
                     (key, 'shrt')]:
            request = self.__prepare_dict({k: v})
            response = func(request)
            assert_false(response)
            assert_equal(bool, type(response))

        request = self.__prepare_dict({key: 'this is just right'})
        response = func(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_notification_title(self):
        self.__test_valid_notification_key('title', valid_notification_title)

    def test_valid_notification_text(self):
        self.__test_valid_notification_key('text', valid_notification_text)

    def test_valid_notification_recipient(self):
        for id in ['', 'Tobias']:
            self.config.testing_securitypolicy(userid=id, permissive=True)
            request = self.__prepare_dict({})
            response = valid_notification_recipient(request)
            assert_false(response)
            assert_equal(bool, type(response))

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        for recipient in ['no_one', 'admin', nick_of_anonymous_user, 'Tobias']:
            request = self.__prepare_dict({'recipient': recipient})
            response = valid_notification_recipient(request)
            assert_false(response)
            assert_equal(bool, type(response))

        request = self.__prepare_dict({'recipient': 'Bob'})
        response = valid_notification_recipient(request)
        assert_true(response)
        assert_equal(bool, type(response))
