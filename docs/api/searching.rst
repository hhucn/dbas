Searching for Statements
========================

D-BAS supports searching for every `statement` in the database.

For querying `statements` D-BAS provides a specific route suffix: /search?q=<value>

For example::

    $ curl http://localhost:4284/api/search?q=cat

This would query `statements` hich are similar to the `cat`.

If `search` is not available `Levensthein` will be used as a default searching algorithm.