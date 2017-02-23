==================
Test Documentation
==================

Every module has his own test class.


Backend with WebTest
====================
Backend tests are realized by the use of *WebTest*. A quick tutorial can be found in the
`documentation of pyramid <http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/functional_testing.html>`_
or in the `documentation of WebTest <http://docs.pylonsproject.org/projects/webtest/en/latest/>`_.
Webtests are end-to-end-full-stack tests.

Execute these tests with::

    nosetests _modulename_


Unit Test
=========
Unit test are suppored by Pyramid with http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/testing.html.
