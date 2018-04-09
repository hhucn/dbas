=====
Logic
=====

Description
===========
Argumentation theory is a wide and complicated field. D-BAS should lead inexperienced users through discussion, therefore
these users are not knowing anyhting about formal argumentation. So we implemented the main interference of logic
argumentation in D-BAS and wrapped them in natural languages.


Dialog-Sequence
===============
Let us assume the user states an supportive argument *arg1*: *A --(+)-> B*. Then the system (other users) has three ways to react:

1. *undermine*: The system disagrees, that A is true. He states an attack *arg2i* against the conclusion *D --(-)-> A*
2. *undercut*: The system disagrees that this leads to accepting the conclusion. He attacks the relation with *arg2ii* *D --(-)-> (A --(+)-> B)*
3. *rebut*: The system disagrees that B holds. He states an attack against the conclusion with *arg2iii* *D --(-)-> B*

Now the system presents the users opinion and the systems attack.

====================  ===============  ================  ==================
user    /    system   undermine        undercut          rebut
====================  ===============  ================  ==================
*undermine*           D --(-)-> C      D --(-)-> C       D --(-)-> C
*support*             next             next              next
*undercut*            D --(-)-> arg2i  D --(-)-> arg2ii  D --(-)-> arg2iii
*rebut*               D --(+)-> A      D --(-)-> arg1    D --(+)-> B
====================  ===============  ================  ==================

In the case of the *support* the users opinion is now the systems attack and the next attack will be displayed.
Otherwise the user has to justify his choose.

*Attention:* The system will never undercut an undercut! So the maximal depth of nested arguments is three, because the user has always the option to undercut an undercut!