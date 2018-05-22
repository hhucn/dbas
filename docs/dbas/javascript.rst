==========
JavaScript
==========

`Libraries <https://dbas.cs.uni-duesseldorf.de/imprint>`_


Management
==========

D-BAS keeps tracking of all JS packages and libraries with the help of https://yarnpkg.com. On default bower is part of
our docker container. You can verify the installation with::

    $ docker exec -i -t dbas_web_1 yarn --version

To add a new dependency, simply type::

    $ yarn add [package]
    $ yarn add [package]@[version]
    $ yarn add [package]@[tag]

To upgrade any dependency, simply type::

    $ yarn upgrade [package]
    $ yarn upgrade [package]@[version]
    $ yarn upgrade [package]@[tag]

And removing is easy with::

    $ yarn remove [package]
