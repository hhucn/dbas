Installation
============

Installation everything for developing
--------------------------------------

Requirements:

1. python python-setuptools easy_install
2. easy_install nose webtest sqlalchemy pyramid_tm zope.sqlalchemy pyramid_mailer zope.i18n
3. pip3 install validate_email cryptacular

Installation with Vagrant virtual machine
-----------------------------------------

Requirements:

1. virtualbox: https://virtualbox.org/wiki/Downloads
2. vagrant: http://docs.vagrantup.com/v2/installation/index.html

create virtual machine and login:

    (LINUX:)    wget https://raw.githubusercontent.com/liqd/adhocracy3/master/Vagrantfile
    (OSX:)      curl https://raw.githubusercontent.com/liqd/adhocracy3/master/Vagrantfile
    vagrant up
    vagrant ssh


Installation
------------

Requirements (Tested on Debian\Ubuntu,  64-Bit is mandatory):

1. ...


Documentation
-------------

build sphinx documentation ::

     sphinx-build -b html source docs


Run the application
-------------------

Start ... (which manages the ZODB database, the Pyramid application
and the ... websocket server)::

    ... ?

Shutdown everything nicely::

    ./bin/supervisorctl shutdown


Run test suites
---------------

Run pytest suite::

    nosetest dbas
