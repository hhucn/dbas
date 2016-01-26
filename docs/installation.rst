Installation
============

Installation everything for developing
--------------------------------------

Requirements:

1. python python-setuptools easy_install python-levensthein
2. easy_install nose webtest sqlalchemy pyramid_tm zope.sqlalchemy pyramid_mailer zope.i18n babel lingua mock
3. pip3 install validate_email cryptacular pyramid_redis_sessions pyramid_beaker pyshorteners
4. sudo apt-get install npm; npm install -g mocha; npm install chai sinon jasmine

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

1. Create virtualenv with python3
   $ mkvirtualenv --python=$(which python3) dbas
2. Install all requirements
   $ pip install -r requirements.txt
3. Develop application
   $ python setup.py develop
4. Create database
   $ initialize_sql development.ini
5. Start development webserver
   $ pserve development.ini --reload


Documentation
-------------

build sphinx documentation ::

     sphinx-build -b html source docs


Run the application
-------------------

Start ... (which manages the ZODB database, the Pyramid application
and the ... websocket server)::

    ... ?


Run test suites
---------------

Run pytest suite::

    nosetest dbas
