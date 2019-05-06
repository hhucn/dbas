===================
D-BAS State Machine
===================

The following image shows D-BAS as a state machine. Every transition needs paremeters
that are either derived from the current state or taken from the discussions database.
The explanation below the state machine documents how those look.

.. image:: src/graph.png


States and Transitions
======================

start
-----

*shows:* All issues.

*parameters:*

* None

*transitions:*

* choose an issue -> `init(issue)`

init
----

*shows:* Positions for given issue

*parameters:*

* issue

*transitions:*

* choose a position -> `attitude(issue, position)`
* write own position -> `finish()`

Special States
==============

lorem ipsum
