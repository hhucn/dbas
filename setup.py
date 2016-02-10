import os

from setuptools import setup, find_packages

# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
# @copyright Krauthoff 2015

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
	'requests',
	'pyshorteners',
	'slugify',
	'validate_email'
]

setup(name='dbas',
	version='0.5.2',
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
	initialize_discussion_sql = dbas.database.initializedb:main_discussion
	initialize_news_sql = dbas.database.initializedb:main_news
	""",
	)
