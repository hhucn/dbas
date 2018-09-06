.. _pyramidspecific:

======================
Pyramid-Specific Stuff
======================

Routes
======

Routes are added in alphabetical order if they are not manually added. This is
also applicable for Cornice and the Services.

See `Github Issue <https://github.com/mozilla-services/cornice/issues/68>`_ and
`official Docs <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html>`_.


D-BAS additional env-vars
=========================

You can configure all entries in the env-file in environment variables (instead of adding variables via code and ini-files in pyramid).
By default D-BAS takes all environment variables with empty prefix and adds them to the configuration, after parsing the .ini file itself.
The name of the environment variable will be the key of the new configuration entry, after some transformations. For more
information please have a look at https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html.

1. The prefix will be stripped.
2. All single underscores will be substituted with a dot.
3. All double underscores will be substituted with a single underscore.
4. uppercase will be lowered.

Example::

    export FOO_BAR__BAZ=fizz
    => foo.bar_baz = fizz


Also you can add pyramid specific variables in the ini-files with `[a:b]` as section parameter. Please add the following
snippet with your keywords to the config in file `dbas/__init__py`::

    sections = ['service']
    log = logging.getLogger(__name__)
    for s in sections:
        try:
            parser = ConfigParser()
            parser.read(global_config['__file__'])
            custom_settings = dict()
            for k, v in parser.items('settings:{}'.format(s)):
                custom_settings['settings:{}:{}'.format(s, k)] = v
            settings.update(custom_settings)
        except NoSectionError as e:
            log.debug(f'__init__(): main() <No {s}-Section> ->{e})

The parameters can now be accessed  via::

    def includeme(config):
        settings = config.registry.settings
        its_something = settings['your_keyword']


