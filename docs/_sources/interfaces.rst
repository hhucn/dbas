Interfaces
==========


Main pages
----------

main_page
+++++++++
* Path: /
* Content: Landing page

main_contact
++++++++++++
* Path: /contact
* Content: Contact page

main_discussion_start
+++++++++++++++++++++
* Path: /discussion/start
* Content: Start a discussion.

main_discussion_issue
+++++++++++++++++++++
* Path: /discussion/start/issue={issue}
* Content: Starts a discussion with the given issue. {issue} in the uid of the issue.

main_discussion
+++++++++++++++
* Path: /discussion/{parameters}/{service}/go
* Content: Wrapper for the complete discussion a discussion.
* Parameters in {service}:
	* *choose_action_for_statement* with parameters *uid=1&issue=1*, whereby *uid* is the unique identifier of the first clicked statement and *issue* is the unique identifier of the issue. This service will call *ajax_get_premises_for_statement*.
	* *get_premises_for_statement* with parameters *uid=1&supportive=true&issue=1*, whereby *XXXXX* This service will call *ajax_get_premises_for_statement*.
    * *reply_for_premisegroup* with parameters *pgroup_id=1&conclusion_id=1&supportive=true&issue=1*, whereby XXXXX This service will call *ajax_reply_for_premisegroup*.
    * *reply_for_response_of_confrontation* with parameters *id=undermine_argument_17&relation=undercut&supportive=true&issue=1*, whereby XXXXX This service will call *ajax_reply_for_response_of_confrontation*.
    * *reply_for_argument* with parameters *id_text=undermine_premisesgroup_68&pgroup_id=17&supportive=true&issue=1*, whereby XXXXX This service will call *ajax_reply_for_argument*.
    * *more_about_argument* with parameters *uid=1&supportive=true&issue=1*, whereby XXXXX This service will call *ajax_get_premise_for_statement*.

main_settings
+++++++++++++
* Path: /settings
* Content: Page with settings of the user. Only available, when the user is logged in

main_news
+++++++++
* Path: /news
* Content: Page with news

main_imprint
++++++++++++
* Path: /imprint
* Content:

404
+++
* Path: /404
* Content: Default 404 page


Discussion Stuff
----------------
ajax_get_start_statements
+++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_start_statements
* Parameters in {url:.*}:
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:

ajax_get_text_for_statement
+++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_text_for_statement
* Parameters in {url:.*}: only necess
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:

ajax_get_premises_for_statement
+++++++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_premises_for_statement
* Parameters in {url:.*}:
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:

ajax_get_premise_for_statement
++++++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_premise_for_statement
* Parameters in {url:.*}:
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:

ajax_reply_for_premisegroup
+++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_reply_for_premisegroup
* Parameters in {url:.*}:
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:

ajax_reply_for_response_of_confrontation
++++++++++++++++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_reply_for_response_of_confrontation
* Parameters in {url:.*}:
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:

ajax_reply_for_argument
+++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_reply_for_argument
* Parameters in {url:.*}:
	* a
	* b
* Parameters in the request:
	* c
	* d
* Content:



User Things
-----------
ajax_user_login
+++++++++++++++
* Path: {url:.*}ajax_user_login

ajax_user_logout
++++++++++++++++
* Path: {url:.*}ajax_user_logout

ajax_user_registration
++++++++++++++++++++++
* Path: {url:.*}ajax_user_registration

ajax_user_password_request
++++++++++++++++++++++++++
* Path: {url:.*}ajax_user_password_request

ajax_all_users
++++++++++++++
* Path: /discussion/{url:.*}ajax_all_users{params:.*}

ajax_delete_user_track
++++++++++++++++++++++
* Path: ajax_delete_user_track

ajax_delete_user_history
++++++++++++++++++++++++
* Path: ajax_delete_user_history



Add new Things
--------------
ajax_set_new_start_statement
++++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_set_new_start_statement{params:.*}

ajax_set_new_start_premise
++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_set_new_start_premise{params:.*}

ajax_set_new_premises_for_x
+++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_set_new_premises_for_x{params:.*}

ajax_set_correcture_of_statement
++++++++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_set_correcture_of_statement{params:.*}



Get Things
----------
ajax_get_logfile_for_statement
++++++++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_logfile_for_statement{params:.*}

ajax_get_shortened_url
++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_shortened_url{params:.*}

ajax_get_attack_overview
++++++++++++++++++++++++
* Path: /discussion/{url:.*}ajax_get_attack_overview{params:.*}

ajax_get_issue_list
+++++++++++++++++++
* Path: {url:.*}ajax_get_issue_list

ajax_get_everything_for_island_view
+++++++++++++++++++++++++++++++++++
* Path: {url:.*}ajax_get_everything_for_island_view{params:.*}

ajax_get_database_dump
++++++++++++++++++++++
* Path: {url:.*}ajax_get_database_dump

ajax_get_user_track
+++++++++++++++++++
* Path: ajax_get_user_track

ajax_get_user_history
+++++++++++++++++++++
* Path: ajax_get_user_history

ajax_get_news
+++++++++++++
* Path: ajax_get_news



Additional Things
-----------------
ajax_fuzzy_search
+++++++++++++++++
* Path: {url:.*}ajax_fuzzy_search

ajax_send_news
++++++++++++++
* Path: ajax_send_news

ajax_switch_language
++++++++++++++++++++
* Path: {url:.*}ajax_switch_language{params:.*}

ajax_additional_service
+++++++++++++++++++++++
* Path: {stuff:.*}additional_service
