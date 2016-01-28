""" Cornice services.
"""
from cornice import Service

_PREFIX = '/api'

# =============================================================================
# HELLO WORLD - exemplary implementation, see http://0.0.0.0:6543/api/hello
# =============================================================================

hello = Service(name='hello', path=_PREFIX+'/hello', description="Simplest app")

@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


# =============================================================================
# POST / GET EXAMPLE
# =============================================================================

values = Service(name='foo', path=_PREFIX+'/values/{value}', description="Cornice Demo")

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