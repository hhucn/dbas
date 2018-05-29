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
 * detecting duplicates


Workflow
========

If you want to add a new queue, there are some steps to be done. We will guide through these steps file-by-file:

    1. Visit `dbas/database/discussion_model.py` and:
        a. Add a new table for your review type to the database.
        b. Add a new table for the last reviewer of your new type.
        c. Add a column into the ReviewCanceled table.
    2. Add the necessary `keys` in `dbas/review/__init__.py`
    3. Create a new script in `dbas/review/<your_queue_name>.py` based on the `__interface__.py`
    4. Implement it!
    5. Add the strings for `priv_access_x_queue` and `<queueY>`
    6. Do not forget to implement the frontend: Most of the parts are just copy / paste / rename.
        a. Add a subpage section in the `review/qeueue.pt`-template
        b. Add your queue in `review/type/<queue>.pt`
        c. Add click events for the buttons in `queue.js` and the methods in `review.js`.
        d. Be nice, we never had time to refactor the frontend.
    7. Please add tests!



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
