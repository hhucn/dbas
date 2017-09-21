from . import *
from selenium import webdriver
import time


def setup():
    time.sleep(TIME_TO_PREPARE)  # very ugly but important to prepare the tests


def teardown():
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()
    driver.close()


def test_english_to_english_page_source():
    """
    service_args:  to prevent ssl v3 error
    :return: Test in the page_source if the national flag changed from english to english
    """
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


def test_english_to_german_page_source():
    """
    service_args:  to prevent ssl v3 error
    :return: Test in the page_source if the national flag changed from english to german
    """
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


def test_german_to_german_page_source():
    """
    service_args:  to prevent ssl v3 error
    :return: Test in the page_source if the national flag changed from german to german
    """
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


def test_german_to_english_page_source():
    """
    service_args:  to prevent ssl v3 error
    :return: Test in the page_source if the national flag changed from german to english
    """
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
