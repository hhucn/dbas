from nose.tools import assert_equals, assert_is_not_none, assert_is_none, assert_in

from api.references import store_reference, get_complete_reference, \
    get_all_references_by_reference_text, get_references_for_url, get_reference_by_id
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences


def test_store_reference():
    api_data = {
        'reference': None,
        'user_uid': 2,
        'host': 'www.host.com',
        'path': 'my-path',
        'issue_id': '3'
    }
    assert_is_none(store_reference(api_data))
    assert_is_none(store_reference(api_data, 2))

    api_data['reference'] = 'some reference text'
    assert_is_none(store_reference(api_data))
    assert_is_not_none(store_reference(api_data, 2))


def test_get_complete_reference():
    assert_is_none(get_complete_reference())
    reference, user, issue, textversion = get_complete_reference(1)
    assert_is_not_none(reference)
    assert_is_not_none(user)
    assert_is_not_none(issue)
    assert_is_not_none(textversion)


def test_get_all_references_by_reference_text():
    assert_is_none(get_all_references_by_reference_text())
    assert_is_none(get_all_references_by_reference_text(''))

    text = DBDiscussionSession.query(StatementReferences).get(1).reference
    ref = get_all_references_by_reference_text(text)
    assert_equals(1, len(ref))
    assert_in('reference', ref[0])
    assert_in('author', ref[0])
    assert_in('issue', ref[0])
    assert_in('arguments', ref[0])
    assert_in('statement', ref[0])


def test_get_references_for_url():
    url = 'http://www.faz.net/'
    path = 'aktuell/beruf-chance/campus/pro-und-contra-brauchen-wir-den-numerus-clausus-13717801.html'
    assert_is_none(get_references_for_url(''))
    assert_is_none(get_references_for_url(url))
    assert_is_none(get_references_for_url(url, ''))
    assert_is_not_none(get_references_for_url(url, path))


def test_get_reference_by_id():
    assert_is_none(get_reference_by_id())
    assert_is_not_none(get_reference_by_id(1))
