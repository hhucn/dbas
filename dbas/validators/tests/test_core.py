from dbas.tests.utils import construct_dummy_request
from dbas.validators import core


def test_has_keywords():
    request = construct_dummy_request()
    fn = core.has_keywords(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is False

    request = construct_dummy_request({'foo': 'bar'})
    fn = core.has_keywords(('foo', int))
    response = fn(request)
    assert type(response) == bool
    assert response is False

    request = construct_dummy_request({'foo': 2})
    fn = core.has_keywords(('foo', int))
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
