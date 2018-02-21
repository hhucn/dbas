from dbas.validators.lib import escape_if_string


def test_escape_if_string():
    test_dict = {'foo': 'bar',
                 'js-tag': '<script>',
                 'int-stays-int': 42,
                 'list-stays-list': [1, 2, 3]}
    assert 'bar' == escape_if_string(test_dict, 'foo')
    assert '&lt;script&gt;' == escape_if_string(test_dict, 'js-tag')
    assert 42 == escape_if_string(test_dict, 'int-stays-int')
    assert [1, 2, 3] == escape_if_string(test_dict, 'list-stays-list')
