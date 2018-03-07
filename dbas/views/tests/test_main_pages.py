import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler.password import get_hashed_password
from dbas.helper.test import verify_dictionary_of_view


class MainImprintViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_imprint as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        # place for additional stuff


class MainFieldexperimentViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_experiment as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        # place for additional stuff


class MainMyDiscussionViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_discussions_overview as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        self.assertIn('layout', response)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('issues', response)


class MainMyDiscussionViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_discussions_overview as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        self.assertIn('layout', response)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('issues', response)


class MainNewsViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_news as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        # place for additional stuff


class MainNotificationsViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_notifications as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        # place for additional stuff


class MainPageViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_page

        request = testing.DummyRequest()
        response = main_page(request)
        verify_dictionary_of_view(response)

        # place for additional stuff


class MainReviewViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_review as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('reputation', response)
        self.assertFalse(response['reputation']['has_all_rights'])
        self.assertTrue(response['reputation']['count'] == 0)


class MainReviewViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_review as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('reputation', response)
        self.assertTrue(response['reputation']['has_all_rights'])
        self.assertTrue(type(response['reputation']['count']) is int)


class MainSettingsViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest()
        self.assertEqual(400, d(request).status_code)


class MainSettingsViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest()
        response = d(request)
        verify_dictionary_of_view(response)

        # check settings
        self.assertIn('send_notifications', response['settings'])
        self.assertIn('send_mails', response['settings'])
        self.assertIn('public_nick', response['settings'])


class MainSettingsViewTestsPassword(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page_failure(self):
        from dbas.views import main_settings as d

        request = testing.DummyRequest(params={
            'form.passwordchange.submitted': '',
            'passwordold': 'tobia',
            'password': 'tobias',
            'passwordconfirm': 'tobias'
        })
        response = d(request)
        verify_dictionary_of_view(response)

        # check settings
        self.assertTrue(len(response['settings']['passwordold']) != 0)
        self.assertTrue(len(response['settings']['password']) != 0)
        self.assertTrue(len(response['settings']['passwordconfirm']) != 0)

    def test_page_success(self):
        from dbas.views import main_settings as d

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()

        request = testing.DummyRequest(params={
            'form.passwordchange.submitted': '',
            'passwordold': 'tobias',
            'password': 'tobiass',
            'passwordconfirm': 'tobiass'
        })
        response = d(request)
        verify_dictionary_of_view(response)

        # check settings
        self.assertTrue(len(response['settings']['passwordold']) == 0)
        self.assertTrue(len(response['settings']['password']) == 0)
        self.assertTrue(len(response['settings']['passwordconfirm']) == 0)

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()


class MainUserView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_settings = db_user.get_settings()
        db_settings.set_show_public_nickname(True)
        transaction.commit()

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        from dbas.views import main_user as d
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        request = testing.DummyRequest(matchdict={'uid': db_user.uid})
        response = d(request)
        verify_dictionary_of_view(response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertFalse(response['can_send_notification'])

    def test_page_myself(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

        request = testing.DummyRequest(matchdict={'uid': db_user.uid})
        response = d(request)
        verify_dictionary_of_view(response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertFalse(response['can_send_notification'])

    def test_page_other(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Christian').first()

        request = testing.DummyRequest(matchdict={'uid': db_user.uid})
        response = d(request)
        verify_dictionary_of_view(response)
        self.assertIn('user', response)
        self.assertIn('can_send_notification', response)
        self.assertTrue(response['can_send_notification'])

    def test_page_error1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid': 0})
        try:
            d(request)
        except HTTPNotFound:
            pass

    def test_page_error2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid': 1000})
        try:
            d(request)
        except HTTPNotFound:
            pass

    def test_page_error3(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid1': 3})
        try:
            d(request)
        except HTTPNotFound:
            pass

    def test_page_error4(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import main_user as d

        request = testing.DummyRequest(matchdict={'uid': 'a'})
        try:
            d(request)
        except HTTPNotFound:
            pass
