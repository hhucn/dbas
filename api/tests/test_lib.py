"""
Unit tests for lib.py
"""
import unittest

from api.lib import flatten, merge_dicts, shallow_patch


def test_flatten():
    l1 = [[1]]
    l2 = [[1, 2]]
    l3 = [[1, 2], [3]]
    l4 = [[1, 2], [3, 4]]
    l5 = [[1, 2], [3], [4]]
    l6 = []
    assert flatten(l1) == [1]
    assert flatten(l2) == [1, 2]
    assert flatten(l3) == [1, 2, 3]
    assert flatten(l4) == [1, 2, 3, 4]
    assert flatten(l5) == [1, 2, 3, 4]
    assert flatten(l6) is None


def test_merge_dicts():
    a = {"foo": "foo"}
    b = {"bar": "bar"}
    c = {"foo": "foo",
         "bar": "bar"}
    assert merge_dicts(a, {}) == a
    assert merge_dicts({}, a) == a
    assert merge_dicts(a, a) == a
    assert merge_dicts(a, None) is None
    assert merge_dicts(a, b) == c


class A(object):
    a = 1
    b = 2
    c = 3


class TestShallowPatch(unittest.TestCase):
    def test_shallow_patch(self):
        a = A()
        allowed_fields = frozenset({"a"})
        patch_value = {"a": 5, "c": 6, "d": 7}
        shallow_patch(a, patch_value, allowed_fields=allowed_fields)
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, 2)
        self.assertEqual(a.c, 3)
        self.assertNotIn("d", dir(A()))
