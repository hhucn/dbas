from nose.tools import assert_true

from dbas.lib import nick_of_anonymous_user
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request
from dbas.validators.notifications import valid_notification_title, valid_notification_text, \
    valid_notification_recipient


class NotificationsTest(TestCaseWithConfig):
    def __test_valid_notification_key(self, key, func):
        request = construct_dummy_request()
        response = func(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        for k, v in [('wrong_key', 'loooooooong striiiing'),
                     (key, 1234567890),
                     (key, 'shrt')]:
            request = construct_dummy_request(json_body={k: v})
            response = func(request)
            self.assertFalse(response)
            self.assertIsInstance(response, bool)

        request = construct_dummy_request(json_body={key: 'this is just right'})
        response = func(request)
        assert_true(response)
        self.assertIsInstance(response, bool)

    def test_valid_notification_title(self):
        self.__test_valid_notification_key('title', valid_notification_title)

    def test_valid_notification_text(self):
        self.__test_valid_notification_key('text', valid_notification_text)

    def test_valid_notification_recipient(self):
        for id in ['', 'Tobias']:
            self.config.testing_securitypolicy(userid=id, permissive=True)
            request = construct_dummy_request()
            response = valid_notification_recipient(request)
            self.assertFalse(response)
            self.assertIsInstance(response, bool)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        for recipient in ['no_one', 'admin', nick_of_anonymous_user, 'Tobias']:
            request = construct_dummy_request(json_body={'recipient': recipient})
            response = valid_notification_recipient(request)
            self.assertFalse(response)
            self.assertIsInstance(response, bool)

        request = construct_dummy_request(json_body={'recipient': 'Bob'})
        response = valid_notification_recipient(request)
        assert_true(response)
        self.assertIsInstance(response, bool)
