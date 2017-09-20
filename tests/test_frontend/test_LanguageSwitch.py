from . import *
import time
browser = None


def setup():
    global browser
    browser = Browser(BROWSER)
    browser.driver.set_window_size(2000, 2000)


def teardown():
    browser.driver.service.process.send_signal(15)
    browser.quit()


def test_english_to_english_other_way():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    html_content = driver.page_source

    assert_in(TEST_ID["ENGLISH"], html_content)

    driver.close()

def test_english_to_german_other_way():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["GERMAN"])
    driver.get(ROOT)
    driver.refresh()

    html_content = driver.page_source

    assert_in(TEST_ID["GERMAN"], html_content)

    driver.close()

def test_german_to_german_other_way():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["GERMAN"])
    driver.get(ROOT)
    driver.refresh()

    html_content = driver.page_source

    assert_in(TEST_ID["GERMAN"], html_content)

    driver.close()

def test_german_to_english_other_way():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    html_content = driver.page_source

    assert_in(TEST_ID["ENGLISH"], html_content)

    driver.close()

"""
This test refresh the browser once.
It won't make sense to refresh the browser every time, because we want to check
if the language had changed after only one refresh.

Therefore it would destroy the results if we refresh in every test.
"""


def test_from_english_to_english():
    browser.visit(ROOT + PATH + LANGUAGE["ENGLISH"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be english
    time.sleep(5)
    # test flag changed from english to english
    assert_in(TEST_ID["ENGLISH"], browser.driver.page_source)
    assert_not_in(TEST_ID["GERMAN"], browser.driver.page_source)


'''
Now test if the language had changed from english to german.
Therefore it is important to refresh the browser to see if there is any change.

It should be clear that the current language is english, because we only refreshed the 
browser at the beginning(test_from_english_to_english()).
'''


def test_from_english_to_german():
    browser.visit(ROOT + PATH + LANGUAGE["GERMAN"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be german
    time.sleep(2)
    # test flag changed from english to german
    assert_in(TEST_ID["GERMAN"], browser.driver.page_source)
    assert_not_in(TEST_ID["ENGLISH"], browser.driver.page_source)


'''
Now let's see if we can change the language from german to german

It should be clear that the current language is german regrading to the 
passing previous tests.
'''


def test_from_german_to_german():
    browser.visit(ROOT + PATH + LANGUAGE["GERMAN"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be german
    time.sleep(2)
    # test flag changed from german to german
    assert_in(TEST_ID["GERMAN"], browser.driver.page_source)
    assert_not_in(TEST_ID["ENGLISH"], browser.driver.page_source)


'''
Let's change the language from german back to english
'''


def test_from_german_to_english():
    browser.visit(ROOT + PATH + LANGUAGE["ENGLISH"])
    browser.visit(ROOT)

    browser.reload()
    # current language should be english
    time.sleep(2)
    # test flag changed from german to english
    assert_in(TEST_ID["ENGLISH"], browser.driver.page_source)
    assert_not_in(TEST_ID["GERMAN"], browser.driver.page_source)


def test_if_this_works():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    html_content = driver.page_source

    assert_in(TEST_ID["ENGLISH"], html_content)

    driver.close()