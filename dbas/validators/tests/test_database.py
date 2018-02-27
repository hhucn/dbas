from cornice import Errors
from nose.tools import assert_true, assert_equal, assert_false
from pyramid import testing

from dbas.database.discussion_model import Statement
from dbas.validators.database import valid_table_name, valid_database_model


def test_valid_table_name():
    request = testing.DummyRequest(json_body={})
    setattr(request, 'errors', Errors())
    setattr(request, 'cookies', {'_LOCALE_': 'en'})
    response = valid_table_name(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = testing.DummyRequest(json_body={'table': 'Stateme'})
    setattr(request, 'errors', Errors())
    setattr(request, 'cookies', {'_LOCALE_': 'en'})
    response = valid_table_name(request)
    assert_false(response)
    assert_equal(bool, type(response))

    for t in ['statement', 'StAtement']:
        request = testing.DummyRequest(json_body={'table': t})
        setattr(request, 'errors', Errors())
        request.validated = {}
        response = valid_table_name(request)
        assert_true(response)
        assert_equal(bool, type(response))

    setattr(request, 'errors', Errors())
    setattr(request, 'cookies', {'_LOCALE_': 'en'})
    response = valid_table_name(request)
    assert_true(response)
    assert_equal(bool, type(response))


def test_valid_database_model():
    request = testing.DummyRequest(json_body={})
    setattr(request, 'errors', Errors())
    fn = valid_database_model('', '')
    response = fn(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = testing.DummyRequest(json_body={})
    setattr(request, 'errors', Errors())
    fn = valid_database_model('k', '')
    response = fn(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = testing.DummyRequest(json_body={})
    setattr(request, 'errors', Errors())
    fn = valid_database_model('', 't')
    response = fn(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = testing.DummyRequest(json_body={'k': 0})
    setattr(request, 'errors', Errors())
    fn = valid_database_model('k', Statement)
    response = fn(request)
    assert_false(response)
    assert_equal(bool, type(response))

    request = testing.DummyRequest(json_body={'k': 1})
    request.validated = {}
    setattr(request, 'errors', Errors())
    fn = valid_database_model('k', Statement)
    response = fn(request)
    assert_true(response)
    assert_equal(bool, type(response))
