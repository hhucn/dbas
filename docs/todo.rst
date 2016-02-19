.. _todo:

======
Todo's
======

API
===

.. todo::
    * Statement beim Start
       * JSON mit

        .. code-block:: python

           'statement': String
           'issue': int

        * Rückgabe enthält

        .. code-block:: python

           'url': String


.. todo::
    * Prämisse beim Start
       * JSON mit

        .. code-block:: python

           'issue': int
           'premisegroups': String[[111],[222],[333,444]]
           'supportive': Boolean
           'conclusion_id': int

        * Rückgabe enthält

        .. code-block:: python

           'url': String

.. todo::
    * Prämisse während der Argumentation
       * JSON mit

        .. code-block:: python

           'issue': int
           'premisegroups': String[[111],[222],[333,444]]
           'arg_uid': int
           'attack_type': String

        * Rückgabe enthält

        .. code-block:: python

           'url': String

.. todo::

    **Login und Logout**

    * Login umschreiben und mehr Funktionen von Pyramid zu nutzen
    * Wie ermöglichen wir die Authentifizierung mit der API...?



Docs
====

.. todo::
    * conf.py
       * version automatsiert auslesen
       * language setzen

D-BAS
=====

.. todo::
    * Docs verlinken