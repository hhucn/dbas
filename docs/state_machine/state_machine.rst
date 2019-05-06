===================
D-BAS State Machine
===================

The following image shows D-BAS as a state machine. Every transition needs paremeters
that are either derived from the current state or taken from the discussions database.
The explanation below the state machine documents how those look.

.. image:: src/graph.png


States and Transitions
======================
The described transitions are only available, when the corresponding action is internally possible.
For example: When there are no counter-arguments in the database, a transition depending on showing a counter-argument
will not be available.

start
-----

*shows:* All issues.

*parameters:*

* None

*transitions:*

* choose an issue -> `init(issue)`

init
----

*shows:* Positions for given issue.

*parameters:*

* issue

*transitions:*

* choose a position -> `attitude(issue, position)`
* write own position -> `finish()`

attitude
--------

*shows:* Possible attitudes towards chosen position.

*parameters:*

* issue being discussed
* position

*transitions:*

* agree -> `justify_statement(issue, position, "agree")`
* disagree -> `justify_statement(issue, position, "disagree")`
* show me an argument -> `dont_know(issue, argument)` (with argument chosen by the system)

dont_know
---------

*shows:* Shows an argument after the user did not want to make up their own opinion regarding a position.

*parameters:*

* issue
* argument (premise -> conclusion)

*transitions:*

* "I'm convinced" -> `reaction(issue, argument, relation, related_argument)`
  (relation and related argument are chosen by the system - most often to attack `argument`)
* undermine (attack conclusion) -> `justify_statement(issue, conclusion, "disagree")`
* undercut -> `justify_argument(issue, argument, "agree", undercut)`
* attack premise -> `reaction(issue, argument, relation, related_argument)`
  (relation and related argument are chosen by the system - most often to attack `argument`)

justify_statement
-----------------

*shows:* An argument against / for a statement

*parameters:*

* issue
* statement
* attitude (agree or disagree)

*transitions:*

* select an argument -> `reaction(issue, argument, relation, related_argument)`
  (relation and related argument are chosen by the system - most often to attack `argument`)
* enter your own argument -> `reaction(issue, entered_argument, relation, related_argument)`
  (relation and related argument are chosen by the system - most often to attack `entered_argument`)

justify_argument
----------------

*shows:* An argument against / for an argument

*parameters:*

* issue
* argument
* attitude
* relation

*transitions:*

* select an argument -> `reaction(issue, selected_argument, relation, related_argument)`
  (relation and related argument are chosen by the system - most often to attack `selected_argument`)
* enter your own argument -> `reaction(issue, entered_argument, relation, related_argument)`
  (relation and related argument are chosen by the system - most often to attack `entered_argument`)

reaction
--------
*shows:* An existing argument (a) that reacts to the passed argument (p_a)

*parameters:*

* issue
* argument, which is reacted to (p_a)
* relation
* reacting argument (a)

*transitions:*

* undermine -> `justify_argument(issue, a, "disagree", undermine)`
* "I'm convinced" -> `reaction(issue, a, new_relation, related_argument)`
  (new_relation and related_argument are chosen by the system - most often to attack `a`)
* undercut -> `justify_argument(issue, a, "disagree", undercut)`
* "defend my argument" -> `justify_statement(issue, p_a, "agree")`
* show another argument -> `reaction(issue, p_a, other_relation, other_argument)`
  (other_relation and other_argument are chosen by the system - most often to attack `p_a`)
* one step back -> Go to the last state that was not reaction.

jump
----
*shows:* Display an argument, without previously going through the "traditional" D-BAS
flow.

*parameters:*

* issue
* argument (premise -> conclusion)

*transitions:*

* accept argument -> `reaction(issue, argument, relation, related_argument)`
  (relation and related_argument are chosen by the system - most often to attack `argument`)
* undercut -> `justify_argument(issue, argument, "agree", undercut)`
* attack conclusion -> `justify_statement(issue, conclusion, "disagree")`
* attack premise -> `justify_argument(issue, argument, "disagree", undermine)`
* accept and support argument -> `justify_statement(issue, premise, "agree")`


Special States
==============

finish
------
At every step it is possible to proceed to finish when the things that should be
shown in the new state are not possible to show. (Either because the user would the argue
against themselves, or because there are no fitting statements / arguments or because
the user was already confronted with them)


