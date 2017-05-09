from . import *
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User

ROOT = 'http://localhost:4284'
error_text = 'test string not present on website'
browser = Browser(BROWSER)
_multiprocess_can_split_ = False


def setup():
    browser.driver.implicitly_wait(10)
    browser.driver.set_window_size(1920, 1080)
    browser.visit(ROOT + '/ajax_switch_language?_LOCALE_=en')


def teardown():
    browser.driver.service.process.send_signal(15)
    browser.quit()


def test_main_page():
    browser.visit(ROOT + '/')
    # TODO use assert_in with browser.driver.page_source
    assert_true(browser.is_text_present('part of the graduate school'), error_text)


def test_contact_page():
    browser.visit(ROOT + '/contact')
    assert_true(browser.is_text_present('Feel free to drop us a'), error_text)


# def test_news_page():
#     browser.visit(ROOT + '/news')
#     xpath = '//span[text()="Docker"]'
#     description = browser.find_by_xpath(xpath).first
#     assert_true(description is not None, error_text)


# def test_imprint_page():
#     browser.visit(ROOT + '/imprint')
#     disclaimer_text = browser.is_text_present('Disclaimer') or browser.is_text_present('Haftung')
#     assert_true(disclaimer_text, error_text)

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
    db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
    browser.visit('{}/user/{}'.format(ROOT, db_user.uid))
    assert_true(browser.is_text_present('Tobias'), error_text)
