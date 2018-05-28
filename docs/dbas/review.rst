=============
Review System
=============

D-BAS comes with an review system wich is powered by the crowd and driven through reputation. Reputation
is a rough measurement of how work you are doing for the discussion and the community. You can earn it by
using D-BAS and all of its great functions. Basic use of D-BAS does not require any reputation at all.

Every user can gain reputation when she e.g. enters statements, marks arguments, but she will loose reputation
on e.g. the misuse of the flagging function. With these points the user gets privileges to enter specific review
queues.


Queues
======

At the moment we have six different queues, each with an inital hurdle of 30 reputation points as well as a
queue with all reviews from the past with an border of 150 points. At least the admin does not need to have any
points by default. The queues are for:

 * optimizations
 * deletes
 * edits
 * splits
 * merges
 * detecting


Workflow
========

If you want to add a new queue, there are some steps to be done. We will guide through these steps file-by-file:

dbas/database/discussion_model.py
=================================

 1. Add a new table for your review type to the database.
 2. Add a new table for the last reviewer of your new type.
 3. Add a column into the ReviewCanceled table.



dbas/review/reputation.py
=========================
 1. Add an border and icon into the maps at the beginning.
 2. Add a dict (monkey see - monkey do) to the return list of `get_privilege_list()`.


dbas/review/queues.py
=====================
 1. Complete the keys and dicts at the beginning.
 2. Expand the review list of `get_review_queues_as_lists()` with your type
 3. Expand the review count of `get_count_of_all()` / `get_complete_review_count()`. This has some pig's tail to code.


dbas/review/opinions.py
=======================
 1. Now please add a method for the voting in this script. This will affect actions on (un-)successful votes as well!


dbas/review/history.py
======================
 1. Add your data in `__get_data()`.
 2. Offer a possibility to revoke an old decision in `revoke_old_decision()` (Case: the admin wants to undo something).
 3. Offer a possibility to cancel any ongoing decision in `cancel_ongoing_decision()` (Case: the admin wants to cancel something).


dbas/review/flags.py
========================
 1. Now we need a mechanism to add a flag for the new table. Maybe you need a method on your own, maybe you could complement the `flag_element()` method.


dbas/review/subpage.py
======================
 1. Last but not least, be a monkey, have a look at `get_subpage_elements_for()` and add your own code.



======================
Source-Code Docstrings
======================


Flag Helper
===========

.. automodule:: dbas.review.flags
    :members:


History Manager
===============

.. automodule:: dbas.review.history
    :members:


Opinion Manager
==============

.. automodule:: dbas.review.opinions
    :members:


Queues Handler
==============

.. automodule:: dbas.review.queues
    :members:


Reputation Helper
=================

.. automodule:: dbas.review.reputation
    :members:


Subpage Manager
===============

.. automodule:: dbas.review.subpage
    :members:
