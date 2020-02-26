import os

from setuptools import setup, find_packages

from dbas.views.helper import version

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGELOG.md')) as f:
    CHANGES = f.read()

requires = []
__version__ = version
setup(name='dbas',
      version=__version__,
      description='Novel prototype for a dialog-based online argumentation',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: NGINX :: Application",
      ],
      author='hhucn',
      author_email='dbas@cs.hhu.de',
      url='https://dbas.cs.hhu.de',
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
      promote_to_admin = dbas.console_scripts:promote_user
      demote_to_user = dbas.console_scripts:demote_user
      """,
      )
