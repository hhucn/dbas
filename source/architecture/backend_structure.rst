Backend Structure
-----------------

The backend consists of:

adhocracy_core
   application framework to provide a rest api for participation process platforms

adhocracy_sample
   examples how to customize resource/sheet types

adhocracy_mercator:
   configuration and extensions to run the mercator rest api application


Usage of external dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Webframework `pyramid <http://docs.pylonsproject.org/docs/pyramid/en/latest/index.html>`_

    * object `traversal <http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/traversal.html>`_
      and `authorization <http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/security.html>`_
      based on resource location

    * `configuration <http://pyramid-cookbook.readthedocs.org/en/latest/configuration/whirlwind_tour.html>`_
      imperative  prefered

    * zope component architecture may be used directly if usefull
      (`pyramid zca <http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/zca.html>`_,
      `zope.interfaces <http://docs.zope.org/zope.interface>`_)

* Persistence `zodb <http://zodborg.readthedocs.org/en/latest/index.html>`_

   * file system storage (`relstorage <https://pypi.python.org/pypi/RelStorage/>`_
     has advantages for productive installation but is currently not supported for python 3)

   * Different or additional persistence should be possible.
     To make this easier code relying on persistent object attributes
     should specify them with interfaces (like :class:`adhocray_core.interfaces.IResource`).
     Also make dependency modules pluggable.

* Application server `substanced <http://docs.pylonsproject.org/projects/substanced/en/latest>`_

   * concept: content types are sets of sheets to follow open close principle.
     `resource types` ...

TODO: Here it would be great to have a small overview of what sheets
do and how they work. Maybe give a concrete example of how they are
used in combination with Colander for the JSON serialization and how
they are used by the object factory. Also explain the link between
resources and sheets and how they reference each other could be
explain (with a diagram?). Also the term "content type" is used
instead of "resource".

* Data structures / validation `colander <http://colander.readthedocs.org/en/latest/>`_


Extend/Customize modules
~~~~~~~~~~~~~~~~~~~~~~~~

* use `pyramid extension hooks <http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/extending.html>`_:
  configuration, view overriding, assets overriding, event subscribers.

* make modules/packages pluggable dependencies to allow different implementations
  (other authentication, references storage, sheet data storage, search, ..)

* override resource/sheet metadata, see :mod:`adhocracy_sample`
