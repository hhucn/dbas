from . import *

_multiprocess_can_split_ = True
browser = None


def setup_func():
    global browser
    browser = Browser(BROWSER)
    browser.visit(ROOT + '/contact')


def teardown_func():
    browser.quit()


@with_setup(setup_func, teardown_func)
def test_name_is_empty():
    browser.fill('name', '')
    browser.fill('mail', 'johnny@example.org')
    browser.fill('content', 'Have a nice day!')
    browser.click_link_by_id('contact-submit')
    assert_in('name is empty', browser.driver.page_source)


@with_setup(setup_func, teardown_func)
def test_mail_is_empty():
    browser.fill('name', 'Johnny')
    browser.fill('mail', '')
    browser.fill('content', 'Have a nice day!')
    browser.click_link_by_id('contact-submit')
    assert_in('mail is invalid', browser.driver.page_source)


@with_setup(setup_func, teardown_func)
def test_content_is_empty():
    browser.fill('name', 'Johnny')
    browser.fill('mail', 'bjoern.ebbinghaus@uni-duesseldorf.de')
    browser.fill('content', '')
    browser.click_link_by_id('contact-submit')
    assert_in('content is empty', browser.driver.page_source)
