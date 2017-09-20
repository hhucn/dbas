from . import *

browser = None


def setup():
    global browser
    browser = Browser(BROWSER)


def teardown():
    browser.driver.service.process.send_signal(15)
    browser.quit()


"""
This test refresh the browser once.
It won't make sense to refresh the browser every time, because we want to check
if the language had changed after only one refresh.

Therefore it would destroy the results if we refresh in every test.
"""


def test_cookies_changed_from_english_to_english():
    browser.visit(ROOT + PATH + LANGUAGE["ENGLISH"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be english

    assert_in('_LOCALE_', browser.cookies.all())

    assert_in(LANGUAGE["ENGLISH"], browser.cookies.all()['_LOCALE_'])
    assert_not_in(LANGUAGE["GERMAN"], browser.cookies.all()['_LOCALE_'])


def test_string_changed_from_english_to_english():
    browser.reload()
    assert_in(TEST_STRING["ENGLISH"], browser.html)
    assert_not_in(TEST_STRING["GERMAN"], browser.html)


def test_flag_changed_from_english_to_english():
    browser.reload()
    assert_in(TEST_ID["ENGLISH"], browser.driver.page_source)
    assert_not_in(TEST_ID["GERMAN"], browser.driver.page_source)


'''
Now test if the language had changed from english to german.
Therefore it is important to refresh the browser to see if there is any change.

It should be clear that the current language is english, because we only refreshed the 
browser at the beginning(test_cookies_changed_from_english_to_english()).
'''


def test_cookies_changed_from_english_to_german():
    browser.visit(ROOT + PATH + LANGUAGE["GERMAN"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be german

    assert_in('_LOCALE_', browser.cookies.all())

    assert_in(LANGUAGE["GERMAN"], browser.cookies.all()['_LOCALE_'])
    assert_not_in(LANGUAGE["ENGLISH"], browser.cookies.all()['_LOCALE_'])


def test_string_changed_from_english_to_german():
    browser.reload()
    assert_in(TEST_STRING["GERMAN"], browser.html)
    assert_not_in(TEST_STRING["ENGLISH"], browser.html)


def test_flag_changed_from_english_to_german():
    browser.reload()
    assert_in(TEST_ID["GERMAN"], browser.driver.page_source)
    assert_not_in(TEST_ID["ENGLISH"], browser.driver.page_source)


'''
Now let's see if we can change the language from german to german

It should be clear that the current language is german regrading to the 
passing previous tests.
'''


def test_cookies_changed_from_german_to_german():
    browser.visit(ROOT + PATH + LANGUAGE["GERMAN"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be german

    assert_in('_LOCALE_', browser.cookies.all())

    assert_in(LANGUAGE["GERMAN"], browser.cookies.all()['_LOCALE_'])
    assert_not_in(LANGUAGE["ENGLISH"], browser.cookies.all()['_LOCALE_'])


def test_string_changed_from_english_to_english():
    browser.reload()
    assert_in(TEST_STRING["GERMAN"], browser.html)
    assert_not_in(TEST_STRING["ENGLISH"], browser.html)


def test_flag_changed_from_english_to_english():
    browser.reload()
    assert_in(TEST_ID["GERMAN"], browser.driver.page_source)
    assert_not_in(TEST_ID["ENGLISH"], browser.driver.page_source)


'''
Let's change the language from german back to english
'''


def test_cookies_changed_from_german_to_english():
    browser.visit(ROOT + PATH + LANGUAGE["ENGLISH"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be english

    assert_in('_LOCALE_', browser.cookies.all())

    assert_in(LANGUAGE["ENGLISH"], browser.cookies.all()['_LOCALE_'])
    assert_not_in(LANGUAGE["GERMAN"], browser.cookies.all()['_LOCALE_'])


def test_string_changed_from_english_to_german():
    browser.reload()
    assert_in(TEST_STRING["ENGLISH"], browser.html)
    assert_not_in(TEST_STRING["GERMAN"], browser.html)


def test_flag_changed_from_english_to_german():
    browser.reload()
    assert_in(TEST_ID["ENGLISH"], browser.driver.page_source)
    assert_not_in(TEST_ID["GERMAN"], browser.driver.page_source)
