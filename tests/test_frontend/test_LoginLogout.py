from . import *

login_url = ROOT + '/ajax_user_login?user={0}&password={1}&keep_login=false&url={2}'
logout_url = ROOT + '/ajax_user_logout'


class TestLoginLogout:
    def setup(self):
        self.browser = Browser(BROWSER)
        self.browser.driver.set_window_size(1920, 1080)
        self.browser.visit(ROOT)

    def teardown(self):
        self.browser.quit()

    def test_wrong_login(self):
        # assert that the user is not logged in
        assert_false(self.browser.is_text_present('Pascal'), 'String \'Pascal\' present')
        # login via loginpage
        self.browser.visit(login_url.format('Pascal', 'wrong password', ROOT))
        # assert that the user is now logged in
        assert_true(self.browser.is_text_present('do not match'))

    def test_right_login(self):
        assert_false(self.browser.is_text_present('Pascal'), 'String \'Pascal\' present')
        self.browser.visit(login_url.format('Pascal', 'iamatestuser2016', ROOT))
        assert_true(self.browser.is_text_present('Pascal'), 'There is no \'Pascal\' on the side')

    def test_logout(self):
        self.test_right_login()
        self.browser.visit(logout_url)
        assert_false(self.browser.is_text_present('Pascal'), 'String \'Pascal\' present')
