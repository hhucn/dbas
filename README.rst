D-BAS
=====

This repository contains the source code of the D-BAS project; This includes frontend cores as well as backend
components.


This project (i.e. all files in this repository if not declared otherwise) is licensed under the MIT License, see
LICENSE.txt.


Further reading :doc:`installation`


Softwarestack
-------------

Server (backend):

- `Pyramid <http://pylonsproject.org>`_  (web framework)

- `Python 3 <http://www.python.org>`_ (programming language)

- `SQLAlchemy <http://www.sqlalchemy.org/>`_ (database)

- `Sphinx <http://sphinx-doc.org/index.html>`_ (documentation)

- `Chameleon <https://chameleon.readthedocs.org/>`_ (html template)


Client (frontend):

- `JavaScript <https://developer.mozilla.org/en-US/docs/Web/JavaScript>`_ (programming language)

- `JQuery <https://jquery.com/>`_ (javascript helper library)

- `HTML5 <http://www.w3.org/TR/html5/>`_ (text markup)

- `Bootstrap <getbootstrap.com/>`_ (css preprocessor)


Internationalization
--------------------

Frontend Javascript:
 - strings.js contains every id
 - i18n-de.js german dict
 - i18n-en.js englisch dict

Frontent HTML:
 - little script i18n.sh which extract all i18n:translate metals
 - locale/de/LC_MESSAGES/dbas.po german dict
 - locale/en/LC_MESSAGES/dbas.po englisch dict

Backend Python:
 - string.py contains all identifiers and dictionaries