=====
D-BAS
=====

D-BAS comes with an an optional, declarative, security system, which is provided by Pyramid itself. You can look it up
on https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html. Long story short, we have four groups:

    - admins: they will have access to the admin menu and full access to every review queue (even the history and ongoing votes)
    - users: users are able to add new statements etc.
    - special: have the same rights as users, but they will be highlighted in the frontend
    - authors: compared the users authors are able to add news

The persmission keywords are seperated as follows:

    - admins: admin, edit, use
    - users: use
    - special: 'use
    - authors: edit, use

You may need them to add new routes.