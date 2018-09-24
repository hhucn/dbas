import os

from setuptools import setup, find_packages

from dbas.views.helper import version

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGELOG.md')) as f:
    CHANGES = f.read()

requires = [
    'pyramid_chameleon',
    'pyramid',
    'pyramid_tm',
    'pyramid_mailer',
    'pyramid_redis_sessions',
    'pyramid_beaker',
    'waitress',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'docutils',
    'WebTest',
    'cryptacular',
    'validate_email',
    'splinter',
    'lingua',
    'requests',
    'pyshorteners',
    'python-slugify',
    'db-psycopg2',
]

setup(name='dbas',
      version=version,
      description='Novel prototype for a dialog-based online argumentation',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: NGINX :: Application",
      ],
      author='Tobias Krauthoff',
      author_email='krauthoff@cs.uni-duesseldorf.de',
      url='https://dbas.cs.uni-duesseldorf.de',
      keywords='web pyramid pylons dialog-based argumentation software',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="dbas",
      entry_points="""\
      [paste.app_factory]
      main = dbas:main
      [console_scripts]
      init_discussion_sql = dbas.database.initializedb:main_discussion
      init_field_test_sql = dbas.database.initializedb:main_field_test
      init_news_sql = dbas.database.initializedb:main_news
      init_empty_sql = dbas.database.initializedb:blank_file
      init_drop_sql = dbas.database.initializedb:drop_it
      init_dummy_votes = dbas.database.initializedb:init_dummy_votes
      promote_to_admin = dbas.console_scripts:promote_user
      demote_to_user = dbas.console_scripts:demote_user
      """,
      )
