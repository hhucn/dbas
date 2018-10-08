====================
Search Documentation
====================

Search is used by D-BAS to give useful searching results to the user.
The microservice 'Search' works with Elasticsearch and can be found `here <https://gitlab.cs.uni-duesseldorf.de/cn-tsn/project/dbas/search>`_.

Environment-Variables
=====================
Search needs to the following env-vars to communicate with D-BAS and its database.

+-------------------------------------+--------------------------------------------------------------------------------+
| APPLICATION_HOST                    | This is the host of the D-BAS application (web)                                |
+-------------------------------------+--------------------------------------------------------------------------------+
| APPLICATION_PORT                    | This is the port where the D-BAS application is reachable at (4284)            |
+-------------------------------------+--------------------------------------------------------------------------------+
| APPLICATION_PROTOCOL                | This is the protocol which is used by search to reach GraphQl (http)           |
+-------------------------------------+--------------------------------------------------------------------------------+
| DATABASE_NAME                       | This is the name of D-BAS's database (discuss)                                 |
+-------------------------------------+--------------------------------------------------------------------------------+
| DATABASE_PASSWORD                   | This is the password of D-BAS's database (can be found in .env)                |
+-------------------------------------+--------------------------------------------------------------------------------+
| DATABASE_HOST                       | This is the host of D-BAS's database (db)                                      |
+-------------------------------------+--------------------------------------------------------------------------------+
| DATABASE_PORT                       | This is the port where D-BAS's database is reachable at (5432)                 |
+-------------------------------------+--------------------------------------------------------------------------------+
| DATABASE_USER                       | This is the user of D-BAS's database (postgres)                                |
+-------------------------------------+--------------------------------------------------------------------------------+


D-BAS sided
===========
On D-BAS side there is the folder `/search` which is used by D-BAS to query search-results.
D-BAS on its side needs some env-vars as well to get search-results.

+-------------------------------------+--------------------------------------------------------------------------------+
| SEARCH_PROTOCOL                     |  The protocol which is used by search to provide results (default http)        |
+-------------------------------------+--------------------------------------------------------------------------------+
| SEARCH_NAME                         |  The name of the search container (default search)                             |
+-------------------------------------+--------------------------------------------------------------------------------+
| SEARCH_PORT                         |  The port where the search container provides results at (default 5000)        |
+-------------------------------------+--------------------------------------------------------------------------------+

Those env-vars above are directly set to there default value in `/search/__init__.py`.