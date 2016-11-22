from tests.test_frontend import *
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

browser = Browser(BROWSER)


def setup():
    browser.driver.implicitly_wait(10)
    browser.visit(ROOT)


def teardown():
    browser.quit()


def test_open_author_popup():
    browser.click_link_by_id('link_popup_author')
    assert_true(browser.is_text_present('About me'))


# requires open popup
def test_close_author_popup():
    browser.click_link_by_id('popup_author_btn_close')
    sleep(0.5)
    assert_false(browser.is_text_present('About me'))


def test_open_license_popup():
    browser.screenshot('debug.png')
    browser.click_link_by_id('link_popup_license')
    assert browser.is_text_present('MIT License')


# requires open popup
def test_close_license_popup():
    browser.driver.find_element_by_id('popup_license_btn_close').click()
    assert_in('MIT License', browser.driver.page_source)
