from . import *
browser = None


def setup():
    global browser
    browser = Browser(BROWSER)
    browser.driver.implicitly_wait(10)
    browser.driver.set_window_size(1920, 1080)
    browser.visit(ROOT + '/ajax_switch_language?lang=en')


def teardown():
    browser.driver.service.process.send_signal(15)
    browser.quit()


def test_already_english():
    browser.visit(ROOT)
    assert_in('part of the graduate', browser.driver.page_source)


def test_switch_to_german():
    pass  # won't work with piwik popup
#     browser.visit(ROOT)
#     browser.click_link_by_id('switch-lang')
#     browser.click_link_by_id('link-trans-de')
#     assert_in('Teil des Graduierten-Kollegs', browser.driver.page_source)


def todo_test_switch_back_to_english():
    # TODO
    pass
