# Unit tests for lib.py
# @author Christian Meter
# @email meter@cs.uni-duesseldorf.de

from .lib import flatten


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
