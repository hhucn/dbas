from html import escape


# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


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
