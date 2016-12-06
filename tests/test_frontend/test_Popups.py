from . import *
from time import sleep

_multiprocess_can_split_ = True


class TestAuthorPopup:
    browser = None
    _multiprocess_can_split_ = False

    @classmethod
    def setup_class(cls):
        cls.browser = Browser(BROWSER)
        cls.browser.driver.implicitly_wait(10)
        cls.browser.driver.set_window_size(1920, 1080)
        cls.browser.visit(ROOT)

    @classmethod
    def teardown_class(cls):
        cls.browser.driver.service.process.send_signal(15)
        cls.browser.quit()

    def test_00_open_author_popup(self):
        self.browser.click_link_by_id('link_popup_author')
        assert_in('About me', self.browser.driver.page_source)

    # requires open popup
    def test_01_close_author_popup(self):
        sleep(1)  # skip animation :-/
        self.browser.click_link_by_id('popup_author_btn_close')
        sleep(0.5)
        assert_false(self.browser.is_text_present('About me'))


class TestlicensePopup:
    _multiprocess_can_split_ = False
    browser = None

    @classmethod
    def setup_class(cls):
        cls.browser = Browser(BROWSER)
        cls.browser.driver.implicitly_wait(10)
        cls.browser.driver.set_window_size(1920, 1080)
        cls.browser.visit(ROOT)

    @classmethod
    def teardown_class(cls):
        cls.browser.driver.service.process.send_signal(15)
        cls.browser.quit()

    def test_00_open_license_popup(self):
        self.browser.screenshot('debug.png')
        self.browser.click_link_by_id('link_popup_license')
        assert self.browser.is_text_present('MIT License')

    # requires open popup
    def test_01_close_license_popup(self):
        self.browser.click_link_by_id('popup_license_btn_close')
        assert_in('MIT License', self.browser.driver.page_source)
