"""
Unit tests for our validators

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""
from cornice import Errors
from pyramid import testing

from dbas.database.discussion_model import ReviewDelete
from dbas.helper.validation import has_keywords, valid_not_executed_review


def test_has_keywords():
    request = testing.DummyRequest(json_body={
        'astring': 'foo'
    })
    request.validated = {}
    checker = has_keywords(('astring', str))
    assert checker(request)
    assert request.validated.get('astring')


def test_has_multiple_keywords():
    request = testing.DummyRequest(json_body={
        'astring': 'foo',
        'abool': True
    })
    request.validated = {}
    checker = has_keywords(('astring', str), ('abool', bool))
    assert checker(request)
    assert request.validated.get('astring')
    assert request.validated.get('abool')


def test_has_numeral_keywords():
    request = testing.DummyRequest(json_body={
        'aint': 4,
        'afloat': 4.0
    })
    request.validated = {}
    checker = has_keywords(('aint', int), ('afloat', float))
    assert checker(request)
    assert request.validated.get('aint')
    assert request.validated.get('afloat')


def test_has_list_keywords():
    request = testing.DummyRequest(json_body={
        'alist': ['<:)']
    })
    request.validated = {}
    checker = has_keywords(('alist', list))
    assert checker(request)
    assert request.validated.get('alist')


def test_has_keywords_with_wrong_type():
    request = testing.DummyRequest(json_body={
        'aint': 4
    })
    setattr(request, 'errors', Errors())
    checker = has_keywords(('aint', float))
    assert not checker(request)


def test_has_keywords_without_keyword():
    request = testing.DummyRequest(json_body={
        'foo': 42
    })
    setattr(request, 'errors', Errors())
    checker = has_keywords(('bar', int))
    assert not checker(request)


def test_valid_not_executed_review():
    request = testing.DummyRequest(json_body={
        'ruid': 4
    })
    request.validated = {}
    checker = valid_not_executed_review('ruid', ReviewDelete)
    assert checker(request)


def test_valid_not_executed_review_error():
    request = testing.DummyRequest(json_body={
        'ruid': 1
    })
    setattr(request, 'errors', Errors())
    checker = valid_not_executed_review('ruid', ReviewDelete)
    assert not checker(request)
