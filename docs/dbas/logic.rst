.. _todo:

=====
Logic
=====

Description
===========
....

Dialogsequence
==============
...
Let us assume the user states an supportive argument *arg1*: *A --(+)--> B*. Then the system (other users) has three ways to react:

1. *undermine*: The system disagrees, that A is true. He states an attack *arg2i* against the conclusion *D --(-)--> A*
2. *undercut*: The system disagrees that this leads to accepting the conclusion. He attacks the relation with *arg2ii* *D --(-)--> (A --(+)-- B)*
3. *rebut*: The system disagrees that B holds. He states an attack against the conclusion with *arg2iii* *D --(-)--> B*

Now the system presents the users opinion and the systems attack. Additionally D-BAS offers five differnt feedback possibilities,
where we currently do not know, which overbid will be taken.

====================  ================  =================  ==================
user    /    system   undermine         undercut           rebut
====================  ================  =================  ==================
*undermine*           D --(-)--> A      D ---(-)--> arg1   D --(-)--> B
*support*             next              next               next
*overbid as attack*   D --(-)--> C      D --(-)--> C       D --(-)--> C
*overbid as overbid*  D --(+)--> arg2i  D --(+)--> arg2ii  D --(+)--> arg2iii
*rebut*               D --(+)--> A      D --(-)--> arg1    D --(+)--> B
====================  ================  =================  ==================

In the case of the *support* the users opinion is now the systems attack and the next attack will be displayed.
Otherwise the user has to justify his choose.