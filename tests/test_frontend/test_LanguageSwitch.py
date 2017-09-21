from . import *
from selenium import webdriver
import time

"""
author: Marc Feger <marc.feger@uni-duesseldorf.de>


meta:
    This tests need a short timeout at the beginning to make sure everything has loaded correctly.
    Please visit __init__.py for more details about the parameters.
    
    There may be some problems with the pipeline if it runs the tests.
    This may have the cases.
        1: PhantomJs has SSL certificate errors -> add service_args 
            Also visit: http://phantomjs.org/api/command-line.html for more details
        2: Pipeline is not ready with all its previous jobs -> add more TIME_TO_PREPARE
        
    The tests if the language had changed by checking the source page and the cookies.
    It is important to simulate a correct browser behavior -> visit Path -> refresh -> show data.
    If the browser changes the correctly the changed language should be visible after every refresh regarding to 
    the previous changes( english -> german a.s.o)
    
    It will be tests in the cookies and the page_source:
        english -> english
        english -> german
        german  -> german
        german  -> english

"""


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


def test_english_to_english_cookies():
    """
    service_args:  to prevent ssl v3 error
    cookies[len(cookies) - 1].get('value'): because the value of the language is always a dictionary
                                            at the last place of cookies.
    :return: Test in the cookies if the language changed from english to english
    """
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    try:
        cookies = driver.get_cookies()
        language_value = cookies[len(cookies) - 1].get('value')

        if language_value is not None:
            assert_in(LANGUAGE["ENGLISH"], language_value)
            assert_not_in(LANGUAGE["GERMAN"], language_value)
        else:
            raise Exception("Cookie language value is empty")

    finally:
        driver.close()


def test_english_to_german_cookies():
    """
    service_args:  to prevent ssl v3 error
    cookies[len(cookies) - 1].get('value'): because the value of the language is always a dictionary
                                            at the last place of cookies.
    :return: Test in the cookies if the language changed from english to german
    """
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["GERMAN"])
    driver.get(ROOT)
    driver.refresh()

    try:
        cookies = driver.get_cookies()
        language_value = cookies[len(cookies) - 1].get('value')

        if language_value is not None:
            assert_in(LANGUAGE["GERMAN"], language_value)
            assert_not_in(LANGUAGE["ENGLISH"], language_value)
        else:
            raise Exception("Cookie language value is empty")

    finally:
        driver.close()


def test_german_to_german_cookies():
    """
    service_args:  to prevent ssl v3 error
    cookies[len(cookies) - 1].get('value'): because the value of the language is always a dictionary
                                            at the last place of cookies.
    :return: Test in the cookies if the language changed from german to german
    """
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["GERMAN"])
    driver.get(ROOT)
    driver.refresh()

    try:
        cookies = driver.get_cookies()
        language_value = cookies[len(cookies) - 1].get('value')

        if language_value is not None:
            assert_in(LANGUAGE["GERMAN"], language_value)
            assert_not_in(LANGUAGE["ENGLISH"], language_value)
        else:
            raise Exception("Cookie language value is empty")

    finally:
        driver.close()


def test_german_to_english_cookies():
    """
    service_args:  to prevent ssl v3 error
    cookies[len(cookies) - 1].get('value'): because the value of the language is always a dictionary
                                            at the last place of cookies.
    :return: Test in the cookies if the language changed from german to english
    """
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get(ROOT + PATH + LANGUAGE["ENGLISH"])
    driver.get(ROOT)
    driver.refresh()

    try:
        cookies = driver.get_cookies()
        language_value = cookies[len(cookies) - 1].get('value')

        if language_value is not None:
            assert_in(LANGUAGE["ENGLISH"], language_value)
            assert_not_in(LANGUAGE["GERMAN"], language_value)
        else:
            raise Exception("Cookie language value is empty")

    finally:
        driver.close()
