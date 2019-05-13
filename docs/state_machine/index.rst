==========
Core Logic
==========
.. toctree::
    :maxdepth: 2
    :glob:

    state_machine

The core logic of D-BAS can be seen as a kind of state machine. Theoretically
the core only needs a database, and the current state to present you with available
options. At the same time given the above arguments, the choice of an option should
be enough for the core to transition to the next state.

Following we try to illustrate this core a state machine with the corresponding
explanations for the states and transitions.