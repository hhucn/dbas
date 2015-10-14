import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
	'pyramid',
	'pyramid_tm',
	'pyramid_chameleon',
	'pyramid_debugtoolbar',
	'pyramid_mailer',
	'waitress',
	'SQLAlchemy',
	'transaction',
	'zope.sqlalchemy',
	'docutils',
	'WebTest',
	'cryptacular',
    'validate_email',
	'splinter',
    'pyramid_beaker',
	'lingua',
]

setup(name='D-BAS',
	version='0.3.6',
	description='Novel prototype for a dialogue based argumentation software',
	long_description=README + '\n\n' + CHANGES,
	classifiers=[
		"Programming Language :: Python",
		"Framework :: Pyramid",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Internet :: WWW/HTTP :: WSGI :: NGINX :: Application",
		],
	author='Tobias Krauthoff',
	author_email='krauthoff@cs.uni-duesseldorf.de',
	url='http://dbas.cs.uni-duesseldorf.de',
	keywords='web pyramid pylons dialogue-based argumentation software',
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
	initialize_sql = dbas.database.initializedb:main
	""",
	)
