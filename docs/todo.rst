.. _todo:

======
Todo's
======

API
===

* Statement beim Start
   * JSON mit

    .. code-block:: python

       'statement': String
       'issue': int

    * Rückgabe enthält

    .. code-block:: python

       'url': String


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


* Prämisse während der Argumentation
   * JSON mit

    .. code-block:: python

       'issue': int
       'premisegroups': String[[111],[222],[333,444]]
       'supportive': Boolean
       'arg_uid': int
       'attack_type': String

    * Rückgabe enthält

    .. code-block:: python

       'url': String

* Login

* Logout


Docs
====

* conf.py
   * sys.path.append('/home/n2o/.virtualenvs/dbas/lib/python3.5/site-packages')
   * version automatsiert auslesen
   * language setzen

D-BAS
=====
* Docs verlinken