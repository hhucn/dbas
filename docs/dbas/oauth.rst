===================
Open Authentication
===================

OAuth is an open standard for access delegation, commonly used as a way for Internet users to grant websites
or applications access to their information on other websites but without giving them the passwords. This
mechanism is used by companies such as Google, Facebook, Microsoft and Twitter to permit the users to share
information about their accounts with third party applications or websites.

General
-------

D-BAS offers the possibility to use the open authentication protocoll implemented by Google, Facebook,
Github and Twitter. The shared information of the given providers will be copied and set as new user in D-BAS.
To use this authentications, please add the variables ``OAUTH_**service**_CLIENTID`` and
``OAUTH_**service**_CLIENTKEY`` for each service you want to use, wherey you have to replace **service** with
GOOGLE, GITHUB, TWITTER or FACEBOOK (important: uppercase).

You can set up your id's and keys on these sites:

 * facebook: https://developers.facebook.com/apps/
 * Github: https://github.com/organizations/**YOUR_ACCOUNT**/settings/applications
 * Google: https://console.developers.google.com/apis/credentials
 * Tiwtter: https://apps.twitter.com/

The given parameters of our ``development.env`` are only for development, because the given id's and keys are
authorized only for the website of ``lvh.me`` which is a redirect to ``localhost``.


Development
-----------

If you want to add another provider, please follow these steps:

 1. Add the name of the provider in the both arrays in `dbas/static/js/main/login.py`
 2. Add a button for the login popup `dbas/templates/snippet-popups.pt`
 3. Add the client id and secret in the env-vars
 4. Add the provider key in `dbas/auth/login.py`
 5. And finally and a function for your provider in `dbas/auth/oauth/`

To test your configuration, you can use `ngrok.io` to have secure tunnels to localhost.
Otherwise the redirect from different apps won't work.