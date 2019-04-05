========
Language
========

D-BAS was developed for the german and english language. During the development we separated the frontend strings and
the backend strings from each other.

Frontend
========

JavaScript
----------

You can find the strings referenced by JS in `dbas/static/js/main/strings.js`. There you will find the keywords as well
as the dictionary for both languages.


Templates (Chameleon)
---------------------

If you want to add or modify a string of any chameleon template, just look for the `i18n:translate` attributes.
After adding/editing any attribute, please execute the `i18n.sh` script of the module. Afterwards you can find your
changes in the `locale`-folder of the module. After any change in the `po`-files of the locales, please run the
i18n-script again.

Backend
=======

Every string and language setting for the backend can be found in `dbas/strings`. There you can add a new language on
your own. Please keep in mind, that you have to add a switch for your language in `templates/snippet/header.pt`.

