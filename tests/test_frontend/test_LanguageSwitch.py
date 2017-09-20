from . import *

def teardown():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()
    driver.close()


def test_english_to_english():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    try:
        html_content = driver.page_source
        assert_in(TEST_ID["ENGLISH"], html_content)
        assert_not_in(TEST_ID["GERMAN"], html_content)

    finally:
        driver.close()


def test_english_to_german():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["GERMAN"])
    driver.get(ROOT)
    driver.refresh()

    try:
        html_content = driver.page_source
        assert_in(TEST_ID["GERMAN"], html_content)
        assert_not_in(TEST_ID["ENGLISH"], html_content)

    finally:
        driver.close()


def test_german_to_german():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["GERMAN"])
    driver.get(ROOT)
    driver.refresh()

    try:
        html_content = driver.page_source
        assert_in(TEST_ID["GERMAN"], html_content)
        assert_not_in(TEST_ID["ENGLISH"], html_content)

    finally:
        driver.close()


def test_german_to_english():
    from selenium import webdriver
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    try:
        html_content = driver.page_source
        assert_in(TEST_ID["ENGLISH"], html_content)
        assert_not_in(TEST_ID["GERMAN"], html_content)
    finally:
        driver.close()
