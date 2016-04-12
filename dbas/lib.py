"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import locale
from datetime import datetime
from html import escape


def escape_string(text):
	"""
	Escapes all html special chars

	:param text: string
	:return: html.escape(text)
	"""
	return escape(text)


def get_language(request, current_registry):
	"""
	Returns current ui locales code which is saved in current cookie or the registry

	:param request: self.request
	:param current_registry: get_current_registry()
	:return: language abrreviation
	"""
	try:
		lang = str(request.cookies['_LOCALE_'])
	except KeyError:
		lang = str(current_registry.settings['pyramid.default_locale_name'])
	return lang


def sql_timestamp_pretty_print(ts, lang):
	"""
	Bla

	:param ts: timestamp as string
	:param lang: language
	:return:
	"""

	formatter = '%-I:%M %p, %d. %b. %Y'
	if lang == 'de':
		try:
			locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
			formatter = '%-H:%M Uhr, %d. %b. %Y'
		except locale.Error:
			locale.setlocale(locale.LC_TIME, 'en_US.UTF8')

	try:  # sqlite
		time = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
	except ValueError:  # postgres
		time = datetime.strptime(ts[:-6], '%Y-%m-%d %H:%M:%S.%f')

	return time.strftime(formatter)
