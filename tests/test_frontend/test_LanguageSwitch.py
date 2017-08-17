from . import *
browser = None
from time import sleep


def setup():
    global browser
    browser = Browser(BROWSER)
    browser.driver.implicitly_wait(10)
    browser.driver.set_window_size(1920, 1080)


def teardown():
    browser.driver.service.process.send_signal(15)
    browser.quit()


def test_already_english():
    browser.visit(ROOT + '/ajax_switch_language?_LOCALE_=en')
    browser.visit(ROOT)
    sleep(500)
    assert_in('part of the graduate', browser.driver.page_source)


def test_switch_to_german():
    browser.visit(ROOT + '/ajax_switch_language?_LOCALE_=de')
    browser.visit(ROOT)
    sleep(500)
    assert_in('Teil des Graduierten-Kollegs', browser.driver.page_source)


def todo_test_switch_back_to_english():
    browser.visit(ROOT + '/ajax_switch_language?_LOCALE_=en')
    browser.visit(ROOT)
    sleep(500)
    assert_in('part of the graduate', browser.driver.page_source)
