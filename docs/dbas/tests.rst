==================
Test Documentation
==================


Requirements
============

Ensure that the following tools are installed (if you want to test locally, without docker:

* Python >= 3.4
* `pipenv <https://pip.pypa.io/en/stable/installing/>`_
* `splinter <https://splinter.readthedocs.org/en/latest/>`_


Backend with WebTest
====================
Backend tests are realized by the use of *WebTest*. A quick tutorial can be found in the
`documentation of pyramid <http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/functional_testing.html>`_
or in the `documentation of WebTest <http://docs.pylonsproject.org/projects/webtest/en/latest/>`_.
Webtests are end-to-end-full-stack tests.

Execute these tests with::

    nosetests


If you want to stay very clean on your machine, you could just run the tests in your container with::

    docker exec dbas_web_1 nosetests


Code
----

.. automodule:: dbas.tests
    :members:


Frontend with Splinter
======================
**DEPRECATED**

Frontend tests are done by *Splinter* and are regardless of DBAS/Pyramid. Splinter is an open source tool for testing web
applications using Python. It lets you automate browser actions, such as visiting URLs and interacting with their items.
If you want to use splinter, please install the latest version of `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_
For running these tests, just execute::

    $ cd tests/
    $ python splinterTests.py

If you want to add a tests, please follow these steps:

1. Open tests/splinterTests.py

2. Add your test into the test list.


3. Define your test function in Webtests by using this skeleton::

    def __test_YOUR_TEST_METHOD(self, browser):
        """
        Please enter a description here
        :param browser: current browser
        :return: 1 if success else 0
        """
        print('Starting tests for XYZ:')
        b = Browser(browser)
        success = True

        # your test routine

        b.quit()
        return 1 if success else 0

Please:
    * replace the name with the chosen name out of 2.
    * enter a short description
    * use the *success*-parameter

4. Have fun!
