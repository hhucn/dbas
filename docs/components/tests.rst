==================
Test Documentation
==================

Every module has his own test class.

Requirements
============

Ensure that the following tools are installed:

* Python >= 3.4
* `pip <https://pip.pypa.io/en/stable/installing/>`_
* `splinter <https://splinter.readthedocs.org/en/latest/>`_


Backend with WebTest
====================
Backend tests are realized by the use of *WebTest*. A quick tutorial can be found in the
`documentation of pyramid <http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/functional_testing.html>`_
or in the `documentation of WebTest <http://docs.pylonsproject.org/projects/webtest/en/latest/>`_.
Webtests are end-to-end-full-stack tests.

Execute these tests with::

    nosetests _modulename_
