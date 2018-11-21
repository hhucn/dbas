from pyramid.testing import DummyRequest

from dbas.tests.utils import construct_dummy_request
from dbas.validators import core
from dbas.validators.core import validate


def test_has_keywords():
    request = construct_dummy_request()
    fn = core.has_keywords_in_json_path(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is False

    request = construct_dummy_request({'foo': 'bar'})
    fn = core.has_keywords_in_json_path(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is False

    request = construct_dummy_request({'foo': 2})
    fn = core.has_keywords_in_json_path(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is True


def test_has_keywords_in_path():
    request = construct_dummy_request()
    fn = core.has_keywords_in_path(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is False

    request = construct_dummy_request(match_dict={'foo': 'bar'})
    fn = core.has_keywords_in_path(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is False

    request = construct_dummy_request(match_dict={'foo': 2})
    fn = core.has_keywords_in_path(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is True


def test_has_maybe_keywords():
    request = construct_dummy_request({'foo': 9000})
    fn = core.has_maybe_keywords(('foo', int, 2))
    response = fn(request)
    assert type(response) == bool
    assert len(request.validated) == 1
    assert request.validated.get('foo') == 9000
    assert response is True

    request = construct_dummy_request()
    fn = core.has_maybe_keywords(('foo', int, 2))
    response = fn(request)
    assert type(response) == bool
    assert len(request.validated) == 1
    assert request.validated.get('foo') == 2
    assert response is True

    request = construct_dummy_request({'foo': 'bar'})
    fn = core.has_maybe_keywords(('foo', int, 2))
    response = fn(request)
    assert type(response) == bool
    assert len(request.validated) == 0
    assert response is False


def test_validate():
    request = DummyRequest()
    assert not hasattr(request, 'validated')
    assert not hasattr(request, 'errors')
    assert not hasattr(request, 'info')
    inner = validate()
    func = inner(__dummy_func)
    func(request)
    assert hasattr(request, 'validated')
    assert hasattr(request, 'errors')
    assert hasattr(request, 'info')


def __dummy_func(request):
    return request
