""" Cornice services.
"""
from cornice import Service
from dbas.views import Dbas

# =============================================================================
# HELLO WORLD - exemplary implementation, see http://0.0.0.0:6543/api/hello
# =============================================================================

hello = Service(name='api', path='/hello', description="Simplest app")
news = Service(name='api_news', path='/get_news', description="News app")

reaction = Service(name='api_reaction', path='/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys', description="Discussion Reaction")
justify  = Service(name='api_justify', path='/{slug}/justify/{statement_or_arg_id}/{mode}*relation', description="Discussion Justify")
attitude = Service(name='api_attitude', path='/{slug}/attitude/*statement_id', description="Discussion Attitude")
init     = Service(name='api_init', path='/*slug', description="Discussion Init")
empty    = Service(name='api_empty', path='', description="Discussion Empty Init")


@hello.get()
def get_info(request):
	"""Returns Hello in JSON."""
	return {'Hello': 'World'}


@news.get()
def get_news(request):
	"""Returns news from DBAS in JSON."""
	return Dbas(request).get_news()


@reaction.get()
def discussion_reaction(request):
	"""Return data from DBas discussion_reaction page"""
	return Dbas(request).discussion_reaction(True)


@justify.get()
def discussion_justify(request):
	"""Return data from DBas discussion_justify page"""
	return Dbas(request).discussion_justify(True)


@attitude.get()
def discussion_attitude(request):
	"""Return data from DBas discussion_attitude page"""
	return Dbas(request).discussion_attitude(True)


@init.get()
def discussion_init(request):
	"""Return data from DBas discussion_init page"""
	return Dbas(request).discussion_init(True)


@empty.get()
def discussion_init(request):
	"""Return data drom DBas discussion_init page"""
	return Dbas(request).discussion_init(True)



# =============================================================================
# POST / GET EXAMPLE
# =============================================================================

values = Service(name='foo', path='/values/{value}', description="Cornice Demo")

_VALUES = {}


@values.get()
def get_value(request):
	"""Returns the value."""
	key = request.matchdict['value']
	return _VALUES.get(key)


@values.post()
def set_value(request):
	"""Set the value.

	Returns *True* or *False*.
	"""
	key = request.matchdict['value']
	try:
		# json_body is JSON-decoded variant of the request body
		_VALUES[key] = request.json_body
	except ValueError:
		return False
	return True
