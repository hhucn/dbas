======
Docker
======
::

    ______________________________
   < Shipping D-BAS in containers >
    ------------------------------
       \
        \
         \
                       ##        .
                 ## ## ##       ==
              ## ## ## ##      ===
          /""""""""""""""""___/ ===
     ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
          \______ o          __/
           \    \        __/
             \____\______/

This is a small installation instruction to use D-BAS within some Docker containers. All instructions from the "normal"
Installation section are dispensable if you choose this type of installation, because all tools are installed within
the containers.

Advantage: Easy and fast setup; your local machine stays clean

Disadvantage: A bit more complicated to debug

Container handling
==================

Requirements
------------

* `Docker <https://docs.docker.com/engine/installation/>`_

  * Use your package manager! :code:`$ sudo pacman -S docker` -- that's it!
    (sometimes it is called `docker-engine`)

* `docker-compose <https://docs.docker.com/compose/install/>`_

* Start the docker daemon

  * :code:`$ sudo systemctl start docker`

You're ready to create your containers and start hacking.

Build Containers
----------------

Create the containers the first time with this command from dbas-root-directory::

   $ docker-compose build

Hoist up!
---------

You only need to build the containers once. Afterwards you can start your containers with this command::

   $ docker-compose up

Open your browser at `http://localhost:4284/ <http://localhost:4284/>`_ to see
your local D-BAS instance.

Remove old containers
---------------------

docker-compose provides a shortcut to remove its containers::

   $ docker-compose rm

This removes the containers of D-BAS.

Rebuild images
--------------

If there are any changes in the images, you'd best remove the affected images of
this project, e.g.::

   $ docker rmi dbas_db_1 dbas_web_1

The next call to `docker-compose up` will pull the latest image and create fresh
containers.


Docker Tips and Tricks
======================

Connect to a running Container
------------------------------

Sometimes it is useful to connect to running containers with a shell. See your running containers with
:code:`docker ps`::

   $ docker ps
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
   20190f09319e        dbas_web            "/bin/bash docker/cor"   41 minutes ago      Up 9 minutes        0.0.0.0:80->80/tcp       dbas_web_1
   e181d3fdeead        dbas_db             "/docker-entrypoint.s"   3 days ago          Up 9 minutes        0.0.0.0:5433->5432/tcp   dbas_db_1

You can execute any command inside the container, or start a bash with this command (use `CONTAINER_ID` or definition
in `NAMES`::

   $ docker exec -it dbas_web_1 bash

This provides a full bash inside the container::

    $ root@20190f09319e:/code# ls
    CHANGELOG.md  LICENSE      README.rst  api   dbas           dbasrequest.log  docker              docker.ini      docs    graph    production.ini    run.sh    tests
    Dockerfile    MANIFEST.in  README.md  admin       data  dbas.egg-info  development.ini  docker-compose.yml  export  i18n.sh  requirements.txt  setup.py
    $ root@20190f09319e:/code#