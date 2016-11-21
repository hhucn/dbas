from . import *
from splinter import Browser
from nose.tools import *

ROOT = 'http://localhost:4284'
error_text = 'test string not present on website'
browser = Browser(BROWSER)


def setup():
    browser.visit(ROOT)
    # TODO switch explicit to english


def teardown():
    browser.quit()


def test_main_page():
    browser.visit(ROOT + '/')
    assert_true(browser.is_text_present('part of the graduate school'), error_text)


def test_contact_page():
    browser.visit(ROOT + '/contact')
    assert_true(browser.is_text_present('Feel free to drop us a'), error_text)


def test_news_page():
    browser.visit(ROOT + '/news')
    assert_true(browser.is_text_present('COMMA16'), error_text)


def test_imprint_page():
    browser.visit(ROOT + '/imprint')
    assert_true(browser.is_text_present('Haftung für Inhalte'), error_text)


def test_discuss_page():
    browser.visit(ROOT + '/discuss')
    assert_true(browser.is_text_present('discussion is about'), error_text)


def test_settings_page():
    browser.visit(ROOT + '/settings')
    assert_true(browser.is_text_present('part of the graduate school'), error_text)


def test_notifications_page():
    browser.visit(ROOT + '/notifications')
    assert_true(browser.is_text_present('part of the graduate school'), error_text)


def test_admin_pages():
    browser.visit(ROOT + '/admin/')
    assert_true(browser.is_text_present('Nickname'), error_text)


def test_user_pages():
    browser.visit(ROOT + '/user/Tobias')
    assert_true(browser.is_text_present('Tobias'), error_text)
