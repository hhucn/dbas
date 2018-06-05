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
        a. Add a new table for your review type to the database, respect the common pattern (Review<Queuename> with tablename = review_<queuename>)!
        b. Add a new table for the last reviewer of your new type, respect the common pattern (LastReviewer<Queuename> with tablename = last_reviewers__<queuename>)!
        c. Add a column into the ReviewCanceled table, respect the common pattern!
    2. Add the necessary `keys` in `dbas/review/queue/__init__.py`
    3. Create a new script in `dbas/review/queue/<your_queue_name>.py` based on the `abc_queue.py`
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


Queues
======

.. automodule:: dbas.review.queues
    :members:

Stuff
=====

.. automodule:: dbas.review
    :members:
