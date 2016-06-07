.. _docker:

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

Starting the Container
======================

Requirements
------------

* `Docker <https://docs.docker.com/engine/installation/>`_

  * Use your package manager! :code:`$ sudo pacman -S docker` -- that's it!

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

You can find a connect-string in your console, which has to be copied to your web browser. It looks like this::

   web_1  | ###################################################
   web_1  | # Connect to this client via http://172.18.0.3/
   web_1  | ###################################################

Open your browser at `http://172.18.0.3/ <http://172.18.0.3/>`_ to see your local D-BAS instance. Keep in mind: your
ip address might be a different one than this. But each time you start the containers, the local ip address is printed
to the console.

Connect to a running Container
==============================

Sometimes it is useful to connect to running containers with a shell. See your running containers with
:code:`docker ps`::

   $ docker ps
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
   20190f09319e        dbas_web            "/bin/bash docker/cor"   41 minutes ago      Up 9 minutes        0.0.0.0:80->80/tcp       dbas_web_1
   e181d3fdeead        dbas_db             "/docker-entrypoint.s"   3 days ago          Up 9 minutes        0.0.0.0:5433->5432/tcp   dbas_db_1

You can execute any command inside the container, or start a bash with this command (use `CONTAINER_ID` or definition
in `NAMES`::

   $ docker exec -it dbas_web_1 bash
