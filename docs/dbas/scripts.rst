=========
Scripts
=========

Statistics
===========
The CLI script `statistics.py` can be used to generate first level statistics for D-BAS discussions. The statistics are

======================================================                   ==============================================================
name                                                                     function
======================================================                   ==============================================================
*get_all_participating_users_of_issue*                                   Get all participating users per issue

*get_all_statements_for_user_of_issues*                                  Get all statements for a user of an issue

*get_amount_of_support_and_attack_per_issue*                             Get the amount of supports and attacks per issue

*get_amount_of_support_and_attack_per_issue_per_user*                    Get the amount of supports and attacks of an user per issue

*get_number_of_seen_arguments_per_user_per_issue*                        Get number of seen arguments of an user per issue

*get_statements_which_have_been_used_more_than_once*                     Get the number a statement has been used per issue
======================================================                   ==============================================================

To run the statistics script use::

   $ docker-compose exec web python dbas/statistics.py <prefix>

